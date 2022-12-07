from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'scratch': "sratch"}
    return render(request, 'ourtube/index.html', context)