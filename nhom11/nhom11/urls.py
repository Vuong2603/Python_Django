"""
URL configuration for nhom11 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path,include,re_path
#from apptwo import views
from appfour import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^apptwo/', include('apptwo.urls')),
    re_path(r'^$', views.index,name='index'),
    re_path(r'^login$', views.user_login , name = 'login'),
    re_path(r'^register/$',views.register,name='register'),
    re_path(r'^register1/$',views.register1,name='register1'),
    #re_path(r'^formpage/',views.form_name_view,name='form'),
    re_path(r'^appfour/',include('appfour.urls')),
    re_path(r'^page2/$',views.page2,name='page2'),
    re_path(r'^special/',views.special, name='special'),
    re_path(r'^logout/',views.user_logout, name='logout'),
    re_path(r'^post/',views.post, name='post'),
    re_path(r'^post_list/$',views.post_list,name='post_list'),
    # re_path(r'^comment/$',views.comment,name='comment'),
    path('post_update/<int:pk>/', views.post_update, name='post_update'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
    # path('comment/<int:post_id>/', views.post_comment, name='comment'),
    re_path(r'^comment_list/$',views.comment_list,name='comment_list'),
    path('comment/create/', views.create_comment, name='create_comment'),
    re_path(r'^draft/$',views.draft_view,name='draft'),
    path('draft/<int:pk>/', views.draft, name='draft'),
    path('draft_update/<int:pk>/', views.draft_update, name='draft_update'),
    path('draft_delete/<int:pk>/', views.draft_delete, name='draft_delete'),
    path('comment/<int:pk>/', views.comment, name='comment'),
    path('comment_update/<int:pk>/', views.comment_update, name='comment_update'),
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    re_path(r'list_blog/$',views.list_blog,name='list_blog'),
    path('search/', views.search, name='search'),


] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)