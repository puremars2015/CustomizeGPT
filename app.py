from flask import Flask, jsonify, render_template, request
import requests

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
    if account != 'sean.ma@thetainformation.com' or password != '1234567890':
        return '{"status": "error", "message": "Invalid credentials"}'
    return '{"status": "success", "token": "JDFHBVWHSJDHKS;12JNWTELVT"}'

@app.route('/callAI', methods=['GET'])
def call_ai():
    # Here you would add the logic to handle the AI call
    message = request.args.get("message")
    message = calln8n(message)
    return jsonify({"message": message["output"]})

def calln8n(prompt):
    response = requests.get("http://localhost:5678/webhook/95cfdc22-80fc-4ffc-95ab-504f9b5c7403", params={"content": prompt})
    message = response.json()
    return message


if __name__ == '__main__':
    app.run(port=5050, debug=True)