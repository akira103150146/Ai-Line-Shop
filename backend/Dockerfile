# 1. 使用官方的 Python 3.12 slim 鏡像
FROM python:3.12.3-slim

# 2. 設定環境變數
ENV PYTHONUNBUFFERED 1

# 3. 設定工作目錄
WORKDIR /app

# 4. 安裝系統依賴
RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 5. 安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 安裝 Node.js 依賴
COPY package.json package-lock.json* tailwind.config.js ./
RUN npm ci --no-audit || npm install --no-audit

# 7. (移除舊的 Step 7 和 Step 8)

# 8. [重要修改] 先複製所有專案程式碼
# 這樣確保 Tailwind 可以掃描到所有的 .html 和 .py 檔案 (包含 App 裡的 templates)
# 且確保之後生成的 CSS 不會被覆寫
COPY . .

# 9. [重要修改] 現在才開始構建 Tailwind CSS
# 確保這一步驟在 COPY . . 之後執行
RUN npm run build-css

# 10. 執行 collectstatic
# 為了避免 collectstatic 報錯，這裡給一個假的 SECRET_KEY 僅供構建使用
RUN SECRET_KEY=build_time_secret_key python3 manage.py collectstatic --noinput

CMD ["./startup.sh"]