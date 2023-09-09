from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.user_dashboard , name='dashboard'),
    path('registration/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('api/model_use_count/', views.ModelUseCountAPI.as_view(), name='model_use_count_api')
]
