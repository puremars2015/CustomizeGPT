from flask import Flask, jsonify, render_template, request
import requests
import secrets

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login-action', methods=['POST'])
def login_action():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')

    response = readAccount(account, password)

    if response.get("account") is None:
        return jsonify({"status": "error", "message": "Invalid credentials"})
    
    token = generate_token()
    updateAccount(account, token)

    return jsonify({"status": "success", "token": token})


def generate_token():
    return secrets.token_urlsafe(32)


@app.route('/callAI', methods=['GET'])
def call_ai():
    # Here you would add the logic to handle the AI call
    message = request.args.get("message")
    message = calln8n(message)
    return jsonify({"message": message["output"]})

def readAccount(account, password):
    response = requests.post("http://localhost:5678/webhook/read-account", params={"account": account, "password": password})
    message = response.json()
    return message

def updateAccount(account, token):
    response = requests.post("http://localhost:5678/webhook/update-account", params={"account": account, "token": token})
    message = response.json()
    return message

def calln8n(prompt):
    response = requests.get("http://localhost:5678/webhook/95cfdc22-80fc-4ffc-95ab-504f9b5c7403", params={"content": prompt})
    message = response.json()
    return message


if __name__ == '__main__':
    app.run(port=5050, debug=True)