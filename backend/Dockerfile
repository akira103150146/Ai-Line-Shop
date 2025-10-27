# Dockerfile

# 1. 使用官方的 Python 3.10 slim 鏡像
FROM python:3.10-slim

# 2. 設定環境變數，讓 Python 輸出更即時
ENV PYTHONUNBUFFERED 1

# 3. 在容器內建立一個工作目錄
WORKDIR /app

# 4. 安裝 PostgreSQL 客戶端 (psycopg2 需要)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# 5. 複製 requirements.txt 並安裝依賴
# (這一步會被快取，未來如果只改程式碼，這一步會跳過，加快部署速度)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製整個專案程式碼到工作目錄
COPY . .

# 7. 執行 collectstatic，收集所有靜態檔案 (例如 Admin 的 CSS)
RUN python3 manage.py collectstatic --noinput

# 8. 設定 Gunicorn 啟動指令
# Cloud Run 會自動設定 $PORT 環境變數
# Gunicorn 會監聽 0.0.0.0 (所有 IP) 上的 $PORT
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 ai_service_project.wsgi:application