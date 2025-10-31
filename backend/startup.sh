#!/bin/sh
# 啟動腳本

# 1. 執行資料庫遷移
# 我們加上 --noinput 參數，告訴 Django 不要詢問任何問題
echo "--- Running Database Migrations ---"
python3 manage.py migrate --noinput

# 2. 啟動 Gunicorn 伺服器
# 這會接收 Cloud Run 傳入的 $PORT 環境變數
echo "--- Starting Gunicorn Server ---"
gunicorn --bind 0.0.0.0:$PORT --workers 2 ai_service.wsgi:application
