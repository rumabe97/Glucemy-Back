from django.urls.conf import path
from rest_framework_simplejwt import views as jwt_views

from authentication.views import RegisterView, GoogleLogin

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
]
