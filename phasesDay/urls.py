from rest_framework.routers import DefaultRouter

from phasesDay.views import PhasesDayViewSet

router = DefaultRouter()
router.register('', PhasesDayViewSet, basename='phases_day')

urlpatterns = router.urls
