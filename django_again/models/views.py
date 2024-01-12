from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View, ListView, DetailView, DeleteView, UpdateView
from .models import *
from django.urls import reverse_lazy


class home(View):
    def get(self, request):
        num = request.session.get("num", 0) + 1
        request.session['num'] = num
        print(num)
        return render(request, 'models/home.html')

class UploadMouseDetails(View):
    def get(self, request):
        created = request.session.get("created", False)
        ctx = {"created": created}
        if created: del(request.session['created'])
        return render(request, 'models/upload_mouse.html', ctx)
    def post(self, request):
        brand_str = request.POST.get("brand")
        category_str = request.POST.get("category")
        name_str = request.POST.get("name")
        price = int(request.POST.get("price"))

        brand, c = Brand.objects.get_or_create(name=brand_str)
        category, c = Category.objects.get_or_create(name=category_str)
        brand.save()
        category.save()
        mouse = Mouse(name=name_str, brand=brand, category=category, price=price)
        mouse.save()

        request.session["created"] = True

        print(brand_str, category_str, name_str, price)


        return redirect(request.path)
# Create your views here.

class MouseList(ListView):
    model = Mouse

class MouseDetail(DetailView):
    model = Mouse

class MouseDelete(DeleteView):
    model = Mouse
    success_url = reverse_lazy("models:mouse_delete_confirmed")
    template_name = 'models/confirm_delete.html'

    
class MouseUpdate(UpdateView):
    model = Mouse
    fields = ['name', "category"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("models:mouse_update_confirmed")
