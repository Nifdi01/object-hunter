from django.shortcuts import render

# Create your views here.

def list_models(request):
    return render(request, 'models/model_list.html')

