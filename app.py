from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def home():
    return render_template('login.html')

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