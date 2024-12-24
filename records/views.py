import datetime
from datetime import timedelta

from django.db.models import Sum
from django.http import FileResponse, JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from fpdf import FPDF
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from records.fullSerializers import UpdateRecordSerializer, CreateRecordSerializer, FullRecordSerializer, \
    PatchRecordSerializer
from records.serializers import PDFSerializer
from shared.mixins import DynamicSerializersMixin, DynamicPermissionsMixin
from records.models import Records
from shared.permissions import IsOwner


@extend_schema_view(
    list=extend_schema(description='Get paginated list of records.'),
    update=extend_schema(description='Update record data.'),
    partial_update=extend_schema(description='Partially update record data.'),
    destroy=extend_schema(description='Delete a record.'),
    create=extend_schema(description='Create a new record.'),
)
class RecordViewSet(DynamicSerializersMixin, DynamicPermissionsMixin, viewsets.ModelViewSet):
    queryset = Records.objects.all()
    serializer_class = FullRecordSerializer

    serializer_classes_by_action = {
        'update': UpdateRecordSerializer,
        'create': CreateRecordSerializer,
        'partial_update': PatchRecordSerializer,
        'get_pdf': PDFSerializer,
    }

    permission_classes_by_action = {
        'create': (permissions.IsAuthenticated,),
        'update': (permissions.IsAdminUser | IsOwner,),
        'partial_update': (permissions.IsAdminUser | IsOwner,),
        'destroy': (permissions.IsAdminUser | IsOwner,),
        'charts': (permissions.IsAdminUser | IsOwner,),
        'records_day': (permissions.IsAdminUser | IsOwner,),
        'get_pdf': (permissions.IsAdminUser | IsOwner,),
    }

    @action(methods=['post'], detail=False, url_path='quick/glucose', url_name="quick_glucose")
    def quick_glucose(self, arg):
        glucose = arg.data['glucose']
        if not glucose:
            return JsonResponse({"error": "Glucose is required"}, status=400)
        record = Records.objects.create(blood_glucose=glucose, user=arg.user)
        serializer = self.get_serializer(record, many=False)
        return JsonResponse(serializer.data, safe=False)

    @action(methods=['get'], detail=False, url_path='day/(?P<day>[^/.]+)', url_name="record_day")
    def records_day(self, request, day):
        if not day:
            return JsonResponse({"error": "Day is required"}, status=400)
        start_date = datetime.datetime.strptime(day, "%Y-%m-%d").date()
        end_date = start_date + timedelta(days=1)
        records = Records.objects.filter(created_date__range=[start_date, end_date], user=request.user)
        serializer = self.get_serializer(records, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(methods=["get"], detail=False, url_path='chart/(?P<start_date>[^/.]+)/(?P<end_date>[^/.]+)',
            url_name="charts")
    def charts(self, arg, start_date, end_date):
        labels = []
        blood_glucose_data = []
        carbohydrates_data = []

        queryset = Records.objects.values('created_date').annotate(
            totalBlood=Sum('blood_glucose')
        ).order_by('created_date').filter(
            created_date__range=[start_date, end_date],
            user=arg.user
        )

        total_carbohydrates = Records.objects.raw(
            """
                SELECT id, created_date, SUM(value) AS total_carbohydrates
                FROM (
                SELECT id, created_date, unnest(carbohydrates) AS value
                FROM records_records
                order by created_date
                ) subquery group by created_date, id;
            """
        )
        aux = []
        for t in total_carbohydrates:
            aux2 = {
                "date": t.created_date,
                "total": t.total_carbohydrates
            }
            aux.append(aux2)
        for record in queryset:
            labels.append(record['created_date']),
            blood_glucose_data.append(record['totalBlood']),
            carbohydratesValue = [item for item in aux if item['date'] == record['created_date']]
            carbohydrates_data.append(carbohydratesValue[0].get('total') if len(carbohydratesValue) > 0 else 0)

        return JsonResponse(data={
            'blood_glucose_data': blood_glucose_data,
            'carbohydrates_data': carbohydrates_data,
            'labels': labels,
        })

    @action(methods=["post"], detail=False, url_path='report', url_name="report")
    def get_pdf(self, arg):
        data = []

        # Query
        queryset = Records.objects.all().filter(user=arg.user).order_by('created_date')

        if arg.data['start_date'] and arg.data['end_date']:
            queryset = queryset.filter(created_date__range=[arg.data['start_date'], arg.data['end_date']])
        for record in list(queryset):
            data.append(record)

        # PDF
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 16)
        pdf.cell(0, 10, 'Glucose reports:', 0, 1, 'C')
        pdf.cell(0, 10, '', 0, 1)  # Espacio extra
        pdf.line(10, 30, 200, 30)

        # Table Header
        line_height = pdf.font_size * 1.5
        effective_page_width = pdf.w - pdf.l_margin - pdf.r_margin
        col_width = effective_page_width / 6
        pdf.set_font('helvetica', 'B', 11)

        # Dibujamos los encabezados de la tabla
        headers = ['Food name', 'Blood glucose', 'Rations', 'Unities', 'Phase day', 'Date']
        for header in headers:
            pdf.cell(col_width, line_height, header, border=1, align='C')
        pdf.ln(line_height)  # Salto de línea después de los encabezados

        # Data
        pdf.set_font('helvetica', '', 10)
        for record in data:
            for food in list(record.foods.all()):
                foodN = (str(food.name)[:13] + '...') if len(str(food.name)) > 13 else str(food.name)
                lista = [
                    foodN,
                    str(round(record.blood_glucose)),
                    str(round(food.hc_rations)),
                    str(round(record.units)),
                    str(record.phasesDay.name),
                    str(record.created_date.strftime('%m/%d/%Y, %H:%M'))
                ]
                # Dibujar cada fila de la tabla
                for item in lista:
                    pdf.cell(col_width, line_height, item, border=1, align='C')  # Alineación centrada
                pdf.ln(line_height)  # Salto de línea después de cada fila

        # Output
        pdf.output('report.pdf', 'F')
        return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
