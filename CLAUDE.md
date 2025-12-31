# CustomizeGPT

CustomizeGPT 是一個輕量的對話式 AI 服務範例，靈感來自 ChatGPT/Claude 等聊天機器人，目標提供一個可自訂、易於擴充的本地化示範專案。

主要功能
- 支援前端頁面（首頁與登入頁面），透過簡單的 Web UI 與使用者互動。
- 與本地或外部工作流程（例如 n8n webhook）整合，將輸入傳送給後端流程並回傳處理結果。
- 使用安全隨機 token（`secrets.token_urlsafe`）作為簡易的 session/token 範例。

目前狀態與已知改善點
- 目前核心功能已完成，包含基本的登入流程、帳號讀取/更新，以及向 webhook 發送請求的範例呼叫。
- 登入（`/login`）相關流程還有加強空間：目前採用簡單的帳號/密碼驗證與 token 更新，建議加入輸入驗證、錯誤處理、HTTPS、以及更完善的 session 管理或第三方驗證整合（OAuth、JWT 等）。

快速上手
1. 安裝相依套件（例如 Flask 與 requests）：

```bash
pip install -r requirements.txt
```

2. 啟動應用程式：

```bash
python app.py
```

3. 開啟瀏覽器並前往 `http://localhost:5050`。

延伸建議
- 將敏感設定（如 webhook URL）移至環境變數或設定檔，不要硬編碼。
- 新增單元測試與整合測試，確保 webhook 整合與登入流程穩定。
- 若要上線服務，請搭配 WSGI 伺服器（gunicorn/uWSGI）與反向代理（nginx），並啟用 TLS/HTTPS。

授權與貢獻
- 此專案為示範範例，歡迎 Fork 與改進，並在 Pull Request 中說明變更內容。
