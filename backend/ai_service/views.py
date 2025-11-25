from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
import sys

class UserSerializer(serializers.ModelSerializer):
    """
    序列化 User 模型。

    這個類別會指定將 User 物件的哪些欄位轉換為 JSON 格式。
    我們刻意排除了 'password' 欄位，以確保不會洩露敏感資料。
    """
    class Meta:
        model = User
        # 僅回傳這些安全的欄位
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']


# ==============================================================================
# 【新增】API：根據使用者名稱獲取使用者資料
# ==============================================================================
@api_view(['GET']) # 指定這個 view 只接受 GET 請求
def get_user_by_username(request, username):
    """
    一個 API 端點，用於根據 URL 中提供的 'username' 獲取使用者資料。
    """
    try:
        # 1. 嘗試從資料庫中找出該使用者
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 2. 如果找不到，回傳 404 錯誤
        return Response(
            {"error": f"使用者 '{username}' 不存在"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3. 如果找到了，使用 Serializer 將 User 物件轉換為 JSON
    serializer = UserSerializer(user)

    # 4. 回傳 200 OK 和 JSON 資料
    return Response(serializer.data, status=status.HTTP_200_OK)
# ==============================================================================
# 【新增】API：回報當前運行的環境和資料庫設定
# ==============================================================================
@api_view(['GET']) # 指定這個 view 只接受 GET 請求
def debug_environment(request):
    """
    一個除錯 API 端點，用來回報服務當前運行的環境資訊。
    """
    try:
        # 1. 獲取 'default' 資料庫的設定
        db_config = settings.DATABASES.get('default', {})
        
        # 2. 提取我們關心的資訊 (絕不回傳密碼)
        connection_info = {
            "engine": db_config.get('ENGINE'),
            "host": db_config.get('DB_HOST'),
            "port": db_config.get('PORT'),
            "name": db_config.get('NAME'),
            "user": db_config.get('USER'),
        }

        # 3. 執行一個簡單的 SQL 查詢來確認連線是否真的暢通
        query_test = "尚未測試"
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                # 執行一個 PostgreSQL 特定的查詢
                cursor.execute("SELECT version();") 
                # 讀取查詢結果
                db_version = cursor.fetchone()
                query_test = f"連線成功！資料庫版本: {db_version[0]}"
        except Exception as e:
            query_test = f"連線測試失敗: {str(e)}"

        # 4. 組合所有回傳資訊
        debug_data = {
            "message": "這是我目前運行的環境狀態",
            "running_python_version": sys.version, # 回報 Python 版本
            "database_settings": connection_info, # 回報 Django 的資料庫設定
            "database_connection_test": query_test, # 回報實際查詢結果
            # "gcp_id": settings.GCP_PROJECT_ID,
            # "env_type": settings.ENV_TYPE,
            # "secret_manager": settings.SECRET_MANAGER_PAYLOAD,
        }

        return Response(debug_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        # 如果連線或查詢失敗，回傳錯誤
        return Response({
            "error": "獲取除錯資訊時發生嚴重錯誤",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_posting_helper_page(request):
    return render(request, 'posting-helper.html')

def get_ang_khun_tek_page(request):
    return render(request, 'lut2/Ang-Khun-tek.html')

def get_chen_cheng_po_lumbermill(request):
    return render(request, 'lut2/Chen-Cheng-Po（lumbermill).html')

def get_chen_cheng_po_roundaout(request):
    return render(request, 'lut2/Chen-Cheng-Po（roundabout).html')

def get_fang_qing_mian(request):
    return render(request, 'lut2/Fang-Qing-Mian.html')
