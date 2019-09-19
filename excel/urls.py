from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('excel',views.excel,name="excel"),
    path('emp',views.emp,name="excel"),
    path('excelfilter',views.excelfilter,name="excelfilter"),
    path('upload',views.upload,name="upload"),
    path('upload_file', views.upload_file, name="upload_file")
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)