from django.urls import path
from django.views.generic import TemplateView
from .views import *


app_name = "login"
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create/type', CreateType.as_view(), name='create_type'),
    path('create/condition', CreateCondition.as_view(), name='create_condition'),
    path('create/item', CreateItem.as_view(), name='create_item'),
    path('register', Register.as_view(), name='register'),
    path('items', ListItems.as_view(), name='items'),
    path('items/<pk>/details', ItemDetail.as_view(), name='item_detail'),
    path('json_items', ListItemsJson.as_view(), name='item_list_json'),
]