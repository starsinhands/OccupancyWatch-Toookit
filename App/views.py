from django.shortcuts import render
from App.models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def configureroom(request):
    classes = ApplianceClass.objects.all()
    types = ApplianceType.objects.all()
    return render(request, 'Configure Room and Appliances.html',{'classes':classes,'types':types})
def details(request):
    return render(request, 'Configure Appliance Details.html')
def configureoccupants(request):
    return render(request, 'Configure Occupants.html')
def exhibit(request):
    return render(request, 'Exhibit appliance-level and aggregate consumption.html')
def generate(request):
    return render(request, 'Generate CSV.html')
# def get_classes(request):
#     classes = ApplianceClass.objects.all()
#     return render(request,'try.html',{'classes':classes})
