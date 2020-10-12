from django.shortcuts import render

# Create your views here.
def home(request):
    mapbox_access_token = 'pk.eyJ1IjoiYmVsb25nYXJvYmVydCIsImEiOiJja2c2cWd2N3IwdGluMnBwaWV5ZzU2bjhnIn0.QgRdSLNmSGfcu1CMWF7vhw'
    return render(request, "home.html",
    {'mapbox_access_token': mapbox_access_token })