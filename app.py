from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/callAI', methods=['GET'])
def call_ai():
    # Here you would add the logic to handle the AI call
    return jsonify({"message":"Hi there! I'm not online yet, but I'll be here soon!"})

if __name__ == '__main__':
    app.run(port=5050, debug=True)