from django.shortcuts import render, HttpResponse
from django.views.generic import View


# Create your views here.
def test(request):
    return HttpResponse("HEllo")

def boot(request):
    return render(request, "test.html")

class home(View):
    def get(self, request):
        return render(request, 'static/home.html')

class products(View):
    def get(self, request):
        return render(request, 'static/products.html')

class services(View):
    def get(self, request):
        return render(request, 'static/services.html')

class contact(View):
    def get(self, request):
        return render(request, 'static/contact.html')

class about(View):
    def get(self, request):
        return render(request, 'static/about.html')
