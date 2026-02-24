from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('register/', views.register),

     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Refresh token
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add/<int:a>/<int:b>/', views.add),
    path('subtract/<int:a>/<int:b>/', views.subtract),
    path('multiply/<int:a>/<int:b>/', views.multiply),
    path('divide/<int:a>/<int:b>/', views.divide),

]
