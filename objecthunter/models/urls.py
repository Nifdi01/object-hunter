from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_models, name='model_list')
]
