from rest_framework.routers import DefaultRouter

from foods.views import FoodsViewSet

router = DefaultRouter()
router.register('', FoodsViewSet, basename='foods')

urlpatterns = router.urls
