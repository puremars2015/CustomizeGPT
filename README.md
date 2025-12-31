# CustomizeGPT

CustomizeGPT 是一個輕量的對話式 AI 服務範例，靈感來自 ChatGPT/Claude 等聊天機器人，提供一個可自訂、易於擴充的本地化示範專案。

## 主要功能

- 支援前端頁面（首頁與登入頁面），透過簡單的 Web UI 與使用者互動
- 與本地或外部工作流程（例如 n8n webhook）整合，將輸入傳送給後端流程並回傳處理結果
- 使用安全隨機 token（`secrets.token_urlsafe`）進行 session 管理
- 完整的輸入驗證和錯誤處理機制
- 環境變數配置管理
- 生產環境部署支援（Gunicorn + Nginx）

## 專案結構

```
CustomizeGPT/
├── app.py                    # Flask 主應用程式
├── config.py                 # 配置管理
├── wsgi.py                   # WSGI 入口點
├── gunicorn_config.py        # Gunicorn 配置
├── test_app.py               # 單元測試
├── requirements.txt          # Python 套件依賴
├── .env.example              # 環境變數範例
├── .gitignore                # Git 忽略規則
├── nginx.conf.example        # Nginx 配置範例
├── DEPLOYMENT.md             # 部署指南
├── CLAUDE.md                 # 專案說明
├── README.md                 # 本檔案
└── templates/                # HTML 模板
    ├── index.html            # 聊天介面
    └── login.html            # 登入頁面
```

## 快速開始

### 環境需求

- Python 3.8 或更高版本
- pip（Python 套件管理工具）
- n8n 服務（用於 webhook 整合）

### 安裝步驟

#### 1. 複製專案

```bash
git clone https://github.com/yourusername/CustomizeGPT.git
cd CustomizeGPT
```

#### 2. 建立虛擬環境

```bash
python -m venv .venv
```

**重要提示**：venv 如果用複製的方式會容易造成錯誤，因為 venv 產生時會與當時的路徑相關，如果複製到新位置就會出錯。請務必在專案目錄下重新建立虛擬環境。

#### 3. 啟動虛擬環境

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

確認終端機提示符前面顯示 `(.venv)` 表示已成功啟動虛擬環境。

#### 4. 安裝相依套件

```bash
pip install -r requirements.txt
```

#### 5. 設定環境變數

複製環境變數範例檔案：

```bash
cp .env.example .env
```

編輯 `.env` 檔案，設定你的配置：

```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5050
SECRET_KEY=your-secret-key-change-this

N8N_BASE_URL=http://localhost:5678
N8N_READ_ACCOUNT_WEBHOOK=/webhook/read-account
N8N_UPDATE_ACCOUNT_WEBHOOK=/webhook/update-account
N8N_AI_WEBHOOK=/webhook/your-webhook-id
```

#### 6. 啟動應用程式

開發環境：

```bash
python app.py
```

應用程式將在 `http://localhost:5050` 啟動。

## 測試

執行單元測試：

```bash
pytest test_app.py -v
```

執行測試並查看覆蓋率：

```bash
pytest test_app.py --cov=app --cov-report=html
```

## 安全特性

本專案已實施以下安全措施：

1. **輸入驗證**：所有使用者輸入都經過嚴格驗證
2. **XSS 防護**：輸入資料經過清理處理
3. **電子郵件驗證**：使用正則表達式驗證電子郵件格式
4. **長度限制**：防止過長的輸入造成問題
5. **錯誤處理**：完善的異常處理機制
6. **環境變數**：敏感資訊不硬編碼在代碼中
7. **安全 Token**：使用 `secrets` 模組產生隨機 token

## API 端點

### 頁面路由

- `GET /` - 首頁（聊天介面）
- `GET /login` - 登入頁面

### API 路由

- `POST /login-action` - 處理登入請求
  - 請求體：`{"account": "email", "password": "password"}`
  - 回應：`{"status": "success", "token": "..."}`

- `GET /callAI?message=<message>` - 呼叫 AI 服務
  - 回應：`{"message": "AI 回覆內容"}`

## 與 n8n 整合

本專案設計用於與 n8n 工作流程整合。你需要在 n8n 中設定以下 webhook：

1. **讀取帳號 webhook**：驗證使用者帳號密碼
2. **更新帳號 webhook**：更新使用者 token
3. **AI webhook**：處理 AI 對話請求

詳細的 n8n 設定說明請參考專案文件。

## 生產環境部署

詳細的部署步驟請參考 [DEPLOYMENT.md](DEPLOYMENT.md)。

簡要步驟：

1. 設定生產環境變數（`.env`）
2. 使用 Gunicorn 啟動應用：`gunicorn -c gunicorn_config.py wsgi:app`
3. 配置 Nginx 作為反向代理
4. 啟用 HTTPS（建議使用 Let's Encrypt）
5. 設定 systemd 服務以自動管理應用程式

## 技術架構

### 前端

- 純 HTML/CSS/JavaScript
- ChatGPT 風格的對話介面
- 響應式設計

### 後端

- Flask（Python Web 框架）
- Gunicorn（WSGI HTTP 伺服器）
- Requests（HTTP 客戶端）

### 部署

- Nginx（反向代理）
- systemd（服務管理）
- Let's Encrypt（SSL/TLS）

## 專案改進記錄

### 已完成的改進

根據 CLAUDE.md 的建議，已完成以下改進：

- ✅ 建立 `requirements.txt` 管理套件依賴
- ✅ 實施環境變數配置（`.env` 和 `config.py`）
- ✅ 加入完整的輸入驗證機制
- ✅ 實施錯誤處理和日誌記錄
- ✅ 移除硬編碼的測試帳號密碼
- ✅ 建立單元測試套件
- ✅ 完善 `.gitignore` 檔案
- ✅ 建立 Gunicorn 和 Nginx 配置
- ✅ 撰寫部署文件

### 未來改善建議

- 加入 CSRF 保護
- 實施速率限制（Rate Limiting）
- 整合 OAuth 或 JWT 驗證
- 加入資料庫支援（SQLAlchemy）
- 實施 WebSocket 支援即時對話
- 加入使用者會話管理
- 實施快取機制（Redis）
- 加入更多的整合測試

## 常見問題

### Q: 為什麼虛擬環境啟動失敗？

A: 請確保你在專案目錄下建立虛擬環境，而不是複製現有的 venv 資料夾。venv 與建立時的路徑綁定。

### Q: 如何更改應用程式運行的端口？

A: 修改 `.env` 檔案中的 `FLASK_PORT` 參數。

### Q: 無法連接到 n8n webhook？

A: 請檢查：
1. n8n 服務是否正在運行
2. webhook URL 是否正確配置在 `.env` 檔案中
3. 網路連接是否正常
4. 防火牆是否允許連接

### Q: 如何在生產環境中運行？

A: 請參考 [DEPLOYMENT.md](DEPLOYMENT.md) 獲取詳細的部署指南。

## 貢獻

歡迎提交 Pull Request 來改進這個專案！請確保：

1. 代碼符合 PEP 8 規範
2. 加入適當的測試
3. 更新相關文件
4. 在 Pull Request 中說明變更內容

## 授權

此專案為示範範例，歡迎 Fork 與改進。

## 聯絡方式

如有問題或建議，請在 GitHub 上開啟 Issue。

## 致謝

感謝所有為這個專案做出貢獻的開發者。
