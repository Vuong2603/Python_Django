from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index , name = 'index'),
    re_path(r'^formpage/',views.form_name_view,name='form'),
]