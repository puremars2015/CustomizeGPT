"""Gunicorn 配置檔案"""
import os
import multiprocessing

# 伺服器綁定
bind = f"0.0.0.0:{os.getenv('FLASK_PORT', '5050')}"

# Worker 設定
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# 日誌設定
accesslog = os.getenv('GUNICORN_ACCESS_LOG', 'logs/access.log')
errorlog = os.getenv('GUNICORN_ERROR_LOG', 'logs/error.log')
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 進程命名
proc_name = 'customizegpt'

# 重新載入
reload = os.getenv('FLASK_ENV', 'production') == 'development'

# 預載入應用程式
preload_app = True

# Daemon 模式
daemon = False

# PID 檔案
pidfile = 'gunicorn.pid'

# 環境變數
raw_env = [
    f"FLASK_ENV={os.getenv('FLASK_ENV', 'production')}"
]
