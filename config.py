import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """應用程式配置類別"""

    # Flask 基本設定
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('FLASK_PORT', 5050))

    # n8n Webhook 設定
    N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
    N8N_READ_ACCOUNT_WEBHOOK = os.getenv('N8N_READ_ACCOUNT_WEBHOOK', '/webhook/read-account')
    N8N_UPDATE_ACCOUNT_WEBHOOK = os.getenv('N8N_UPDATE_ACCOUNT_WEBHOOK', '/webhook/update-account')
    N8N_AI_WEBHOOK = os.getenv('N8N_AI_WEBHOOK', '/webhook/95cfdc22-80fc-4ffc-95ab-504f9b5c7403')

    # Session 設定
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 3600))

    @property
    def read_account_url(self):
        """取得讀取帳號的完整 URL"""
        return f"{self.N8N_BASE_URL}{self.N8N_READ_ACCOUNT_WEBHOOK}"

    @property
    def update_account_url(self):
        """取得更新帳號的完整 URL"""
        return f"{self.N8N_BASE_URL}{self.N8N_UPDATE_ACCOUNT_WEBHOOK}"

    @property
    def ai_webhook_url(self):
        """取得 AI Webhook 的完整 URL"""
        return f"{self.N8N_BASE_URL}{self.N8N_AI_WEBHOOK}"


config = Config()
