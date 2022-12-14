from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user import views

app_name = 'user'

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('verify/', views.VerifyJSONWebToken.as_view(), name='verify'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('activate/', views.ActivateUserView.as_view(), name='activate'),
]

