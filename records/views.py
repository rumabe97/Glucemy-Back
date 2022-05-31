from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.http import FileResponse, JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from fpdf import FPDF
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from records.fullSerializers import UpdateRecordSerializer, CreateRecordSerializer, FullRecordSerializer
from shared.mixins import DynamicSerializersMixin
from records.models import Records
from records.serializers import RecordSerializer
from shared.permissions import IsOwner


@extend_schema_view(
    list=extend_schema(description='Get paginated list of records.'),
    update=extend_schema(description='Update record data.'),
    partial_update=extend_schema(description='Partially update record data.'),
    destroy=extend_schema(description='Delete a record.'),
    create=extend_schema(description='Create a new record.'),
)
class RecordViewSet(DynamicSerializersMixin, viewsets.ModelViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordSerializer

    serializer_classes_by_action = {
        'update': UpdateRecordSerializer,
        'create': CreateRecordSerializer,
        'partial_update': UpdateRecordSerializer,
        'get_object': FullRecordSerializer,
    }

    permission_classes_by_action = {
        'create': (permissions.IsAuthenticated,),
        'update': (permissions.IsAdminUser | IsOwner,),
        'partial_update': (permissions.IsAdminUser | IsOwner,),
        'destroy': (permissions.IsAdminUser | IsOwner,),
        'charts': (permissions.IsAdminUser | IsOwner,),
    }

    @action(methods=["get"], detail=False, url_path='(?P<start_date>[^/.]+)/(?P<end_date>[^/.]+)',
            url_name="charts")
    def charts(self, arg, start_date, end_date):
        labels = []
        blood_glucose_data = []
        carbohydrates_data = []

        queryset = Records.objects.annotate(day=TruncDay('created_date')).values('day').annotate(
            totalBlood=Sum('blood_glucose'), totalCarbohydrates=Sum('carbohydrates')).order_by('day').filter(
            created_date__range=[start_date, end_date])

        for record in queryset:
            labels.append(record['day'].strftime("%d/%m/%Y"))
            blood_glucose_data.append(record['totalBlood']),
            carbohydrates_data.append(record['totalCarbohydrates'])

        return JsonResponse(data={
            'blood_glucose_data': blood_glucose_data,
            'carbohydrates_data': carbohydrates_data,
            'labels': labels,
        })

    @action(methods=["get"], detail=False, url_path='report', url_name="report")
    def report(self, arg):
        data = []
        queryset = Records.objects.all()
        for record in queryset:
            data.append(record)

        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font('courier', 'B', 16)
        pdf.cell(40, 10, 'Glucose charts:', 0, 1)
        pdf.cell(40, 10, '', 0, 1)
        pdf.line(10, 30, 200, 30)
        pdf.set_font('courier', '', 12)
        pdf.cell(100, 8, f"{'Food name'.ljust(15)}  "
                         f"{'Blood glucose'.ljust(15)}  "
                         f"{'Rations'.ljust(15)}  "
                         f"{'Unities'.ljust(15)}  "
                         f"{'Phase day'.ljust(15)}  "
                         f"{'Date'.ljust(20)}", 0, 1)

        pdf.line(10, 38, 200, 38)
        for line in data:
            food_name = (str(line.foods.name)[:75] + '...') if len(str(line.foods.name)) > 75 else str(line.foods.name)

            pdf.cell(100, 8, f"{str(food_name).ljust(15)} "
                             f"{str(line.blood_glucose).ljust(15)}  "
                             f"{str('hc_rations').ljust(15)}  "
                             f"{'test'.ljust(15)}  "
                             f"{str(line.phasesDay.name).ljust(15)}  "
                             f"{str(line.phasesDay.created_at.strftime('%m/%d/%y, %H:%M')).ljust(20)}", 0, 1)
        pdf.output('report.pdf', 'F')
        return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
