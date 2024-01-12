from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "static"
urlpatterns = [
    path("", views.home.as_view(), name="home"),
    path("products", views.products.as_view(), name="products"),
    path("services", views.services.as_view(), name="services"),
    path("contact-us", views.contact.as_view(), name="contact"),
    path("about-us", views.about.as_view(), name="about"),
]
