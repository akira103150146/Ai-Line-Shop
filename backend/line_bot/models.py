from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="商家名稱")

    # 【新增】儲存每個商家自己的 LINE 金鑰
    channel_secret = models.CharField(max_length=200, verbose_name="Channel Secret")
    channel_access_token = models.CharField(max_length=300, verbose_name="Channel Access Token")

    system_prompt = models.TextField(max_length=1000,
        verbose_name="AI 系統提示",
        help_text="例如：你是一個友善的餐廳客服，名叫「小助手」。請根據以下資料庫內容回答問題。")
    database_content = models.TextField(max_length=5000,
        verbose_name="商家資料庫",
        help_text="請條列式輸入所有商家資訊，例如：營業時間、停車位資訊、最新促銷活動等。")
     # 建立時間與更新時間
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)