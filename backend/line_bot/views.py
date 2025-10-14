# line_bot/views.py

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings # 引入 settings

import openai

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from .models import Business

@csrf_exempt
def line_webhook(request, business_id):
    # 根據 business_id 從資料庫找出對應的商家
    try:
        business = Business.objects.get(id=business_id)
    except Business.DoesNotExist:
        return HttpResponseBadRequest("Business not found")

    handler = WebhookHandler(business.channel_secret)
    configuration = Configuration(access_token=business.channel_access_token)

    # 這是一個裝飾器，告訴 handler 當收到「文字訊息」時，要執行這個函式
    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_message(event):
        # 取得用戶傳來的文字
        user_message = event.message.text
        # 準備要回覆的訊息
        reply_text = get_ai_response(user_message, business)

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )
    if request.method == 'POST':
        # 取得請求的簽章
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            # 驗證簽章並處理 webhook
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest("Invalid signature")

        return HttpResponse("OK")
    else:
        return HttpResponseBadRequest("Invalid request method")

openai.api_key = settings.OPENAI_API_KEY # 設定 OpenAI 金鑰 
def get_ai_response(prompt, business):
    try:
        try:
            system_prompt = business.system_prompt
            database_content = business.database_content
        except Business.DoesNotExist:
            # 如果資料庫是空的或找不到，給一個預設值
            system_prompt = "你是一個有幫助的 AI 助理。"
            database_content = "目前沒有可用的商家資料。"

        # 組合更完整的提示
        full_prompt = f"""
        # 商家資料庫:
        {database_content}

        # 用戶問題:
        {prompt}
        """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=250,
            temperature=0.7,
        )
        ai_message = response.choices[0].message.content.strip()
        return ai_message
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "抱歉，AI 系統目前有點問題，請稍後再試。"