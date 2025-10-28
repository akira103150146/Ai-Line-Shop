import os
import io 
from pathlib import Path
import dj_database_url 
print("DEBUG: settings.py - Top level START") # <--- 加入點 1

BASE_DIR = Path(__file__).resolve().parent.parent

# --- 環境判斷 ---
ENV_TYPE = 'dev'
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT") 

print(f"DEBUG: settings.py - Detected GCP_PROJECT_ID: {GCP_PROJECT_ID}") # <--- 加入點 2

if GCP_PROJECT_ID:
    ENV_TYPE = 'prod'
    print("DEBUG: settings.py - Running in PROD mode") # <--- 加入點 3
    try:
        print("DEBUG: settings.py - Attempting to import GCP libs...") # <--- 加入點 4
        from google.cloud import secretmanager
        from dotenv import load_dotenv 
        print("DEBUG: settings.py - GCP libs imported successfully") # <--- 加入點 5

        client = secretmanager.ServiceClient()
        settings_name = "ai-bot-django-settings" 
        name = f"projects/{GCP_PROJECT_ID}/secrets/{settings_name}/versions/latest"

        print(f"DEBUG: settings.py - Attempting to access secret: {name}") # <--- 加入點 6
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        print("DEBUG: settings.py - Secret accessed successfully") # <--- 加入點 7

        print("DEBUG: settings.py - Attempting to load secrets into environ...") # <--- 加入點 8
        load_dotenv(stream=io.StringIO(payload)) 
        print("DEBUG: settings.py - Secrets loaded into environ successfully") # <--- 加入點 9
    except Exception as e:
        print(f"CRITICAL: 無法從 GCP Secret Manager 載入金鑰: {e}") 
        raise
else:
    ENV_TYPE = 'dev' # 確保 DEV 模式設定
    print("DEBUG: settings.py - Running in DEV mode") # <--- 加入點 10 (本地用)
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, '.env'))
    print("DEBUG: settings.py - Loaded .env file.") 

SECRET_KEY = os.getenv("SECRET_KEY")
print(f"DEBUG: settings.py - SECRET_KEY loaded: {'Yes' if SECRET_KEY else 'NO!'}") # <--- 加入點 11

if ENV_TYPE == 'prod':
    DEBUG = False
    ALLOWED_HOSTS = ['*'] 
    SERVICE_URL = os.getenv('SERVICE_URL', '')
    print(f"DEBUG: settings.py - SERVICE_URL loaded: {SERVICE_URL}") # <--- 加入點 12
    if SERVICE_URL:
        CSRF_TRUSTED_ORIGINS = [SERVICE_URL]
else:
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ... (INSTALLED_APPS, MIDDLEWARE 等保持不變) ...

# --- 資料庫 ---
print("DEBUG: settings.py - Configuring DATABASES...") # <--- 加入點 13
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", 
        conn_max_age=600 
    )
}
print(f"DEBUG: settings.py - DATABASES configured. Engine: {DATABASES['default']['ENGINE']}") # <--- 加入點 14

# ... (剩下的設定保持不變) ...
print("DEBUG: settings.py - Bottom level END") # <--- 加入點 15