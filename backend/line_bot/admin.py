# line_bot/admin.py

from django.contrib import admin
from .models import Business

# 使用裝飾器來註冊 Business 模型
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    # 在列表頁面顯示的欄位
    list_display = ('name', 'channel_id', 'updated_at')
    # 可以被搜尋的欄位
    search_fields = ('name', 'channel_id')
