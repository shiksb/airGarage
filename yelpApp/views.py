from django.shortcuts import render

# Create your views here.
def index(request):
    location = request.GET.get('location')

    return render(request, 'index.html', {'location_fill' : location})