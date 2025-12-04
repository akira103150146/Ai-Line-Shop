# Dockerfile

# 1. 使用官方的 Python 3.10 slim 鏡像
FROM python:3.12.3-slim

# 2. 設定環境變數，讓 Python 輸出更即時
ENV PYTHONUNBUFFERED 1

# 3. 在容器內建立一個工作目錄
WORKDIR /app

# 4. 安裝系統依賴：PostgreSQL 客戶端和 Node.js
RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 5. 複製 requirements.txt 並安裝 Python 依賴
# (這一步會被快取，未來如果只改程式碼，這一步會跳過，加快部署速度)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製 package.json 和 Tailwind 配置文件並安裝 Node.js 依賴（用於構建 Tailwind CSS）
# 先只複製這些文件以利用 Docker 快取層
COPY package.json package-lock.json* tailwind.config.js ./
RUN npm ci --no-audit || npm install --no-audit

# 7. 複製 Tailwind 源文件和模板文件（用於構建 CSS）
# 這些文件變化時才需要重新構建 CSS
COPY static/src/input.css ./static/src/
COPY templates/ ./templates/

# 8. 構建 Tailwind CSS
RUN npm run build-css

# 9. 複製其餘專案程式碼到工作目錄
# 注意：這會覆蓋之前複製的 templates/，但 CSS 已經構建完成，所以沒問題
COPY . .

# 10. 執行 collectstatic，收集所有靜態檔案 (包含 Tailwind CSS 和 Admin 的 CSS)
RUN SECRET_KEY=build_time_secret_key python3 manage.py collectstatic --noinput

CMD ["./startup.sh"]
