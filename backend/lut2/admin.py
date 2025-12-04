from django.contrib import admin
from .models import UploadedImage


from django.contrib import admin
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'orientation', 'poem_title', 'poem_author', 'created_at']
    list_filter = ['orientation', 'created_at']
    search_fields = ['original_filename', 'poem_title', 'poem_content']
    readonly_fields = ['created_at', 'updated_at']
