from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'visualData/home.html')

def contact(request):
    return render(request, 'visualData/basic.html', {'app_name':'visualData','content':['Do you have the data I\'m looking for?', 'Please contact me!','email@example.com']})

def sources(request):
    return render(request, 'visualData/sources.html')
