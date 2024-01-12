from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = "models"
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('upload-mouse-details', views.UploadMouseDetails.as_view(), name='mouse_upload'),
    path('mouse-list', views.MouseList.as_view(), name='mouse_list'),
    path('mouse/<pk>', views.MouseDetail.as_view(), name='mouse_detail'),
    path('<pk>/delete', views.MouseDelete.as_view(), name='mouse_delete'),
    path('<pk>/update', views.MouseUpdate.as_view(), name='mouse_update'),
    path('delete-succes', TemplateView.as_view(template_name="models/delete_confirmed.html"), name='mouse_delete_confirmed'),
    path('update-succes', TemplateView.as_view(template_name="models/update_confirmed.html"), name='mouse_update_confirmed'),
]