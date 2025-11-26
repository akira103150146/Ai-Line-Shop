from django.db import models
from django.utils import timezone
import os
import uuid


def upload_to(instance, filename):
    """生成上傳文件的儲存路徑"""
    # 根據 orientation 分類儲存
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"lut2/{instance.orientation}/{filename}"


class UploadedImage(models.Model):
    """上傳的圖片模型
    
    支援兩種儲存方式：
    1. 文件系統儲存（推薦）：使用 image 欄位，儲存在 MEDIA_ROOT
    2. Base64 儲存：使用 image_base64 欄位，將 base64 字串存在資料庫
    """
    
    ORIENTATION_CHOICES = [
        ('portrait', '直式'),
        ('landscape', '橫式'),
    ]
    
    # 基本資訊
    orientation = models.CharField(
        max_length=10, 
        choices=ORIENTATION_CHOICES, 
        default='portrait',
        verbose_name='方向'
    )
    
    # 方式1：文件系統儲存（推薦）- 使用 ImageField
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True,
        verbose_name='圖片檔案'
    )
    
    # 方式2：Base64 儲存（備選）- 使用 TextField
    # 如果使用 base64，請將 image 設為 null，並使用 image_base64
    image_base64 = models.TextField(
        null=True,
        blank=True,
        verbose_name='Base64 圖片資料'
    )
    
    # 元資料
    original_filename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='原始檔名'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新時間'
    )
    
    class Meta:
        verbose_name = '上傳圖片'
        verbose_name_plural = '上傳圖片'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.orientation} - {self.original_filename or '未命名'}"
    
    def get_image_url(self):
        """取得圖片的 URL"""
        if self.image:
            return self.image.url
        return None
    
    def get_image_base64(self):
        """取得 base64 格式的圖片（如果使用 base64 儲存）"""
        return self.image_base64
    
    def get_base64_data_uri(self):
        """組出 data URI，方便前端直接顯示 base64 圖片"""
        if not self.image_base64:
            return None
        mime_type = 'image/jpeg'
        if self.original_filename:
            ext = os.path.splitext(self.original_filename)[1].lower()
            if ext in ['.png']:
                mime_type = 'image/png'
            elif ext in ['.gif']:
                mime_type = 'image/gif'
            elif ext in ['.webp']:
                mime_type = 'image/webp'
        return f"data:{mime_type};base64,{self.image_base64}"
