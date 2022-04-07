from rest_framework.routers import DefaultRouter

from favourites.views import FavouritesViewSet

router = DefaultRouter()
router.register('', FavouritesViewSet, basename='favourites')

urlpatterns = router.urls
