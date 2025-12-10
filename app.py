from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/callAI', methods=['GET'])
def call_ai():
    # Here you would add the logic to handle the AI call
    message = request.args.get("message")
    message = calln8n(message)
    return jsonify({"message": message["output"]})

def calln8n(prompt):
    response = requests.get("http://localhost:5678/webhook/408aed93-9609-4378-b2d3-7a1b22eb9abe", params={"content": prompt})
    message = response.json()
    return message


if __name__ == '__main__':
    app.run(port=5050, debug=True)