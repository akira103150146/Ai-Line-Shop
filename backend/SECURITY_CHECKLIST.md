# GCP 部署安全檢查清單

## ✅ 已修復的安全問題

### 1. SECRET_KEY 驗證
- **問題**：如果 SECRET_KEY 未設定，Django 會使用預設值或崩潰
- **修復**：添加了明確的驗證，如果 SECRET_KEY 未設定會立即拋出錯誤
- **位置**：`settings.py` 第 65-66 行

### 2. 安全 HTTP 標頭
- **問題**：缺少生產環境的安全標頭設定
- **修復**：添加了以下安全標頭：
  - `SESSION_COOKIE_SECURE = True` - 僅通過 HTTPS 傳輸 session cookie
  - `CSRF_COOKIE_SECURE = True` - 僅通過 HTTPS 傳輸 CSRF cookie
  - `SECURE_BROWSER_XSS_FILTER = True` - 啟用瀏覽器 XSS 過濾
  - `SECURE_CONTENT_TYPE_NOSNIFF = True` - 防止 MIME 類型嗅探
  - `X_FRAME_OPTIONS = 'DENY'` - 防止點擊劫持
  - `SECURE_HSTS_*` - HTTP 嚴格傳輸安全
- **位置**：`settings.py` 第 265-275 行

### 3. 文件上傳驗證
- **問題**：缺少文件大小和類型驗證
- **修復**：添加了以下驗證：
  - 文件大小限制：10MB
  - 文件類型檢查：僅允許 JPEG, PNG, GIF, WebP
  - 文件擴展名檢查：防止偽裝的文件類型
- **位置**：`lut2/views.py` 第 85-110 行

## ⚠️ 需要注意的問題

### 1. 媒體文件存儲（重要）
- **問題**：使用本地文件系統存儲媒體文件
- **風險**：在 Cloud Run 中，容器是無狀態的，文件會在容器重啟後丟失
- **建議**：
  - 使用 Google Cloud Storage (GCS) 來存儲媒體文件
  - 安裝 `django-storages[google]` 套件
  - 配置 `STORAGES['default']` 使用 GCS
  - 參考：https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
- **位置**：`settings.py` 第 242-256 行（已添加警告）

### 2. CSRF 豁免
- **問題**：`upload_image` 視圖使用了 `@csrf_exempt`
- **風險**：可能受到 CSRF 攻擊
- **建議**：
  - 如果可能，移除 `@csrf_exempt` 並在前端正確處理 CSRF token
  - 或者添加其他驗證機制（如 API key、rate limiting）
- **位置**：`lut2/views.py` 第 61 行

### 3. ALLOWED_HOSTS
- **當前設定**：生產環境使用 `ALLOWED_HOSTS = ['*']`
- **風險**：允許任何主機訪問
- **建議**：
  - 如果可能，指定具體的 Cloud Run 服務 URL
  - 例如：`ALLOWED_HOSTS = ['your-service-xxxxx.run.app']`
- **位置**：`settings.py` 第 77 行

### 4. 速率限制
- **問題**：沒有防止暴力上傳或 API 濫用的機制
- **建議**：
  - 考慮使用 `django-ratelimit` 或 `django-axes`
  - 對上傳端點實施速率限制
  - 例如：每 IP 每小時最多上傳 10 張圖片

### 5. Dockerfile 安全性
- **當前狀態**：使用 root 用戶運行（雖然 slim 鏡像已經比較安全）
- **建議**：
  - 考慮創建非 root 用戶運行應用
  - 但要注意文件權限問題

## ✅ 已正確配置的項目

1. **環境變數管理**：使用 GCP Secret Manager
2. **DEBUG 模式**：生產環境正確關閉
3. **靜態文件**：使用 WhiteNoise 正確配置
4. **資料庫**：使用環境變數配置，支援 Cloud SQL
5. **密鑰管理**：敏感信息不提交到 Git（.gitignore 已配置）

## 📋 部署前檢查清單

- [ ] 確認 GCP Secret Manager 中有以下密鑰：
  - `SECRET_KEY`
  - `DATABASE_URL`（如果使用 Cloud SQL）
  - `OPENAI_API_KEY`
  - `SERVICE_URL`（Cloud Run 服務 URL）
- [ ] 確認 Cloud Run 服務已配置正確的環境變數
- [ ] 確認資料庫遷移已執行
- [ ] 確認靜態文件已收集（Dockerfile 中已自動執行）
- [ ] 考慮設置媒體文件存儲到 GCS
- [ ] 考慮添加速率限制
- [ ] 測試上傳功能是否正常工作
- [ ] 檢查日誌輸出是否正常

## 🔒 額外安全建議

1. **定期更新依賴**：使用 `pip list --outdated` 檢查過時的套件
2. **啟用 Cloud Run 的 IAM 認證**：限制誰可以訪問服務
3. **設置 Cloud Armor**：防止 DDoS 攻擊
4. **啟用審計日誌**：監控異常活動
5. **定期備份資料庫**：使用 Cloud SQL 自動備份功能
6. **設置監控告警**：監控錯誤率和性能指標

