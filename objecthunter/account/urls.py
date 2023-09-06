from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.landing_page, name='landing_page'),
    path('', views.dashboard, name='dashboard'),
    path('registration/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('upload/', views.image_upload_view, name='upload')
]
