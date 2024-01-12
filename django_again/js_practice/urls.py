from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name = "js_practice"

urlpatterns = [
    path('', TemplateView.as_view(template_name='js_practice/home.html'),name="home"),
    path('grid', TemplateView.as_view(template_name='js_practice/grid.html'),name="grid"),

]