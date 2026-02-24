from django.urls import path
from .views import register, profile,logout
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile),
    path('logout/', logout, name='logout'),
    path('files/', views.list_files, name='list_files'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('files/<uuid:pk>/', views.get_file, name='get_file'),
    path('files/<uuid:pk>/update/', views.update_file, name='update_file'),
    path('files/<uuid:pk>/delete/', views.delete_file, name='delete_file'),
]
