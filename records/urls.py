from rest_framework.routers import DefaultRouter

from records.views import RecordViewSet

router = DefaultRouter()
router.register('', RecordViewSet, basename='records')

urlpatterns = router.urls
