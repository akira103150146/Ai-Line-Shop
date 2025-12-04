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
    """上傳的圖片模型"""
    
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
    
    # 圖片儲存 (僅保留文件系統儲存)
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True,
        verbose_name='圖片檔案'
    )
    
    # --- 新增：詩詞資訊 ---
    poem_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='詩詞標題'
    )

    poem_author = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='詩詞作者'
    )

    poem_content = models.TextField(
        null=True,
        blank=True,
        verbose_name='詩詞內容'
    )
    # -------------------
    
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