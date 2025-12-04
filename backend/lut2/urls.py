from django.urls import path
from . import views

app_name = "lut2"

urlpatterns = [
    path("ang-khun-tek", views.get_ang_khun_tek_page, name="ang-khun-tek"),
    path("chen-cheng-po-lumbermill", views.get_chen_cheng_po_lumbermill, name="chen-cheng-po-lumbermill"),
    path("chen-cheng-po-roundaout", views.get_chen_cheng_po_roundaout, name="chen-cheng-po-roundaout"),
    path("fang-qing-mian", views.get_fang_qing_mian, name="fang-qing-mian"),
    path("gallery", views.get_gallery_page, name="gallery"),
    path("gallery-data", views.get_gallery_data, name="gallery-data"), 
    path("upload", views.get_upload_page, name="upload"),
    path("upload-image", views.upload_image, name="upload-image"),
]