from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf.urls import include
from config import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('dj-rest-auth/', include('dj_rest_auth.urls')),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                  path('api/users/', include('users.urls')),
                  path('api/records/', include('records.urls')),
                  path('api/foods/', include('foods.urls')),
                  path('api/phases_day/', include('phasesDay.urls')),
                  path('api/favourites/', include('favourites.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
