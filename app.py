from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login1')
def login1():
    return render_template('login1.html')

@app.route('/login-action', methods=['GET', 'POST'])
def login_action():

    # 依照請求方式取得帳密
    if request.method == 'GET':
        account = request.args.get('account')
        password = request.args.get('password')
    else:
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')

    # 驗證帳密
    if account != 'sean.ma@thetainformation.com' or password != '1234567890':
        return jsonify({
            "status": "error",
            "message": "Invalid credentials"
        }), 401

    # 登入成功
    return jsonify({
        "status": "success",
        "token": "JDFHBVWHSJDHKS;12JNWTELVT"
    })


@app.route('/callAI', methods=['GET'])
def call_ai():
    # Here you would add the logic to handle the AI call
    message = request.args.get("message")
    message = calln8n(message)
    return jsonify({"message": message["output"]})

def calln8n(prompt):
    response = requests.get("http://localhost:5678/webhook/95516d69-b590-46bf-84e5-bc0ed6fd2fb9", params={"content": prompt})
    message = response.json()
    return message


if __name__ == '__main__':
    app.run(port=5050, debug=True)