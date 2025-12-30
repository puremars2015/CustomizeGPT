from flask import Flask, jsonify, render_template, request
import requests
import secrets
import re
from config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY


def validate_input(data, required_fields):
    """驗證輸入資料"""
    if not data:
        return False, "無效的請求資料"

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"缺少必要欄位: {field}"

        # 檢查是否為字串且長度合理
        if not isinstance(data[field], str) or len(data[field].strip()) == 0:
            return False, f"欄位 {field} 格式不正確"

        # 基本的長度限制
        if len(data[field]) > 255:
            return False, f"欄位 {field} 超過長度限制"

    return True, None


def validate_email(email):
    """驗證電子郵件格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_input(text):
    """清理輸入資料，防止 XSS"""
    if not isinstance(text, str):
        return ""
    return text.strip()


@app.route('/')
def home():
    """首頁路由"""
    return render_template('index.html')


@app.route('/login')
def login():
    """登入頁面路由"""
    return render_template('login.html')


@app.route('/login-action', methods=['POST'])
def login_action():
    """處理登入請求"""
    try:
        data = request.get_json()

        # 驗證輸入
        is_valid, error_message = validate_input(data, ['account', 'password'])
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": error_message
            }), 400

        account = sanitize_input(data.get('account'))
        password = sanitize_input(data.get('password'))

        # 驗證電子郵件格式（如果帳號是電子郵件）
        if '@' in account and not validate_email(account):
            return jsonify({
                "status": "error",
                "message": "電子郵件格式不正確"
            }), 400

        # 呼叫帳號驗證
        response = readAccount(account, password)

        if not response or response.get("account") is None:
            return jsonify({
                "status": "error",
                "message": "帳號或密碼錯誤"
            }), 401

        # 產生新的 token
        token = generate_token()
        update_result = updateAccount(account, token)

        if not update_result:
            return jsonify({
                "status": "error",
                "message": "登入處理失敗，請稍後再試"
            }), 500

        return jsonify({
            "status": "success",
            "token": token
        })

    except requests.exceptions.RequestException as e:
        app.logger.error(f"登入時網路請求錯誤: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "連線失敗，請檢查網路或稍後再試"
        }), 503

    except Exception as e:
        app.logger.error(f"登入時發生錯誤: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "系統錯誤，請稍後再試"
        }), 500


def generate_token():
    """產生安全的隨機 token"""
    return secrets.token_urlsafe(32)


@app.route('/callAI', methods=['GET'])
def call_ai():
    """呼叫 AI 服務"""
    try:
        message = request.args.get("message")

        # 驗證訊息
        if not message or not message.strip():
            return jsonify({
                "message": "請輸入訊息"
            }), 400

        # 檢查訊息長度
        if len(message) > 5000:
            return jsonify({
                "message": "訊息過長，請縮短後再試"
            }), 400

        message = sanitize_input(message)

        # 呼叫 n8n webhook
        result = calln8n(message)

        if not result or "output" not in result:
            return jsonify({
                "message": "AI 服務暫時無法回應，請稍後再試"
            }), 503

        return jsonify({
            "message": result["output"]
        })

    except requests.exceptions.Timeout:
        app.logger.error("呼叫 AI 服務逾時")
        return jsonify({
            "message": "請求逾時，請稍後再試"
        }), 504

    except requests.exceptions.RequestException as e:
        app.logger.error(f"呼叫 AI 時網路請求錯誤: {str(e)}")
        return jsonify({
            "message": "連線失敗，請檢查網路或稍後再試"
        }), 503

    except Exception as e:
        app.logger.error(f"呼叫 AI 時發生錯誤: {str(e)}")
        return jsonify({
            "message": "系統錯誤，請稍後再試"
        }), 500


def readAccount(account, password):
    """讀取帳號資訊"""
    try:
        response = requests.post(
            config.read_account_url,
            params={"account": account, "password": password},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"讀取帳號時發生錯誤: {str(e)}")
        return None


def updateAccount(account, token):
    """更新帳號 token"""
    try:
        response = requests.post(
            config.update_account_url,
            params={"account": account, "token": token},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"更新帳號時發生錯誤: {str(e)}")
        return None


def calln8n(prompt):
    """呼叫 n8n AI webhook"""
    try:
        response = requests.get(
            config.ai_webhook_url,
            params={"content": prompt},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"呼叫 n8n webhook 時發生錯誤: {str(e)}")
        return None


@app.errorhandler(404)
def not_found(error):
    """處理 404 錯誤"""
    return jsonify({
        "status": "error",
        "message": "找不到請求的資源"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """處理 500 錯誤"""
    return jsonify({
        "status": "error",
        "message": "伺服器內部錯誤"
    }), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )
