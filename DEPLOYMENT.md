# CustomizeGPT 部署指南

本文檔說明如何將 CustomizeGPT 部署到生產環境。

## 系統需求

- Python 3.8 或更高版本
- pip（Python 套件管理工具）
- Gunicorn（WSGI HTTP 伺服器）
- Nginx（反向代理，推薦）
- n8n 服務（用於 webhook 整合）

## 本地開發環境設定

### 1. 安裝依賴套件

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安裝套件
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 為 `.env` 並修改配置：

```bash
cp .env.example .env
```

編輯 `.env` 檔案，設定以下參數：

```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5050
SECRET_KEY=your-secret-key-change-this-in-production

N8N_BASE_URL=http://localhost:5678
N8N_READ_ACCOUNT_WEBHOOK=/webhook/read-account
N8N_UPDATE_ACCOUNT_WEBHOOK=/webhook/update-account
N8N_AI_WEBHOOK=/webhook/your-webhook-id
```

### 3. 執行開發伺服器

```bash
python app.py
```

應用程式將在 `http://localhost:5050` 啟動。

### 4. 執行測試

```bash
pytest test_app.py -v
```

## 生產環境部署

### 1. 環境準備

在生產環境中，建議使用以下配置：

```env
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=5050
SECRET_KEY=<使用強密碼產生器產生的密鑰>

N8N_BASE_URL=https://your-n8n-domain.com
# ... 其他配置
```

### 2. 使用 Gunicorn 啟動應用

建立日誌目錄：

```bash
mkdir -p logs
```

啟動 Gunicorn：

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

或使用背景執行：

```bash
gunicorn -c gunicorn_config.py wsgi:app --daemon
```

### 3. 使用 systemd 管理服務（Linux）

建立服務檔案 `/etc/systemd/system/customizegpt.service`：

```ini
[Unit]
Description=CustomizeGPT Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/CustomizeGPT
Environment="PATH=/path/to/CustomizeGPT/.venv/bin"
ExecStart=/path/to/CustomizeGPT/.venv/bin/gunicorn -c gunicorn_config.py wsgi:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

啟動服務：

```bash
sudo systemctl daemon-reload
sudo systemctl start customizegpt
sudo systemctl enable customizegpt
sudo systemctl status customizegpt
```

### 4. 配置 Nginx 反向代理

複製並修改 nginx 配置：

```bash
sudo cp nginx.conf.example /etc/nginx/sites-available/customizegpt
sudo ln -s /etc/nginx/sites-available/customizegpt /etc/nginx/sites-enabled/
```

編輯配置檔案，修改以下內容：
- `server_name`：你的網域名稱
- 靜態檔案路徑
- SSL 憑證路徑（如果使用 HTTPS）

測試並重新載入 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 設定 HTTPS（推薦使用 Let's Encrypt）

```bash
# 安裝 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 獲取憑證
sudo certbot --nginx -d your-domain.com

# 自動更新憑證
sudo certbot renew --dry-run
```

## 監控與維護

### 查看日誌

```bash
# 應用程式日誌
tail -f logs/error.log
tail -f logs/access.log

# systemd 日誌
sudo journalctl -u customizegpt -f

# Nginx 日誌
sudo tail -f /var/log/nginx/customizegpt_error.log
```

### 重新啟動服務

```bash
sudo systemctl restart customizegpt
```

### 更新應用程式

```bash
# 拉取最新代碼
git pull origin main

# 安裝新的依賴
source .venv/bin/activate
pip install -r requirements.txt

# 重新啟動服務
sudo systemctl restart customizegpt
```

## 安全建議

1. **使用 HTTPS**：在生產環境中務必啟用 HTTPS
2. **強密鑰**：使用強隨機密鑰作為 `SECRET_KEY`
3. **防火牆**：配置防火牆只開放必要的端口（80, 443）
4. **定期更新**：保持系統和套件更新
5. **備份**：定期備份資料庫和配置檔案
6. **監控**：設定應用程式和系統監控
7. **限流**：使用 Nginx 或應用層實施請求限流
8. **日誌管理**：定期輪替和清理日誌檔案

## 疑難排解

### 應用程式無法啟動

- 檢查 `.env` 檔案是否存在且配置正確
- 確認虛擬環境已啟動
- 查看錯誤日誌：`tail -f logs/error.log`

### 無法連接到 n8n webhook

- 確認 n8n 服務正在運行
- 檢查 webhook URL 是否正確
- 確認網路連接和防火牆規則

### Nginx 502 錯誤

- 確認 Gunicorn 正在運行：`sudo systemctl status customizegpt`
- 檢查 Gunicorn 是否監聽正確的端口
- 查看 Nginx 錯誤日誌

## 效能優化

1. **調整 Worker 數量**：根據 CPU 核心數調整 `GUNICORN_WORKERS`
2. **啟用快取**：考慮使用 Redis 或 Memcached
3. **CDN**：將靜態資源部署到 CDN
4. **資料庫優化**：如果使用資料庫，確保適當的索引
5. **連線池**：配置適當的資料庫連線池大小

## 聯絡與支援

如有問題或建議，請在 GitHub 開啟 Issue。
