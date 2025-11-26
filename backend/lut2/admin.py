from django.contrib import admin
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'orientation', 'original_filename', 'created_at', 'has_image_file', 'has_base64']
    list_filter = ['orientation', 'created_at']
    search_fields = ['original_filename']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_image_file(self, obj):
        """顯示是否有文件儲存"""
        return bool(obj.image)
    has_image_file.boolean = True
    has_image_file.short_description = '有文件'
    
    def has_base64(self, obj):
        """顯示是否有 Base64 儲存"""
        return bool(obj.image_base64)
    has_base64.boolean = True
    has_base64.short_description = '有 Base64'
