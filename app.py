from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/callAI', methods=['GET'])
def callAI():
    message = request.args.get('message', '')
    data = callAIApi(message)
    
    if data is None:
        return jsonify({'error': 'AI 服務暫時無法使用，請稍後再試'}), 500
    
    return jsonify(data)

# 呼叫 AI 服務的邏輯可以在這裡實現 AI的URL是 http://localhost:5678/webhook-test
def callAIApi(prompt):
    try:
        response = requests.get('http://localhost:5678/webhook-test/ai', params={'prompt': prompt}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to AI service at localhost:5678")
        return None
    except requests.exceptions.Timeout:
        print(f"Error: AI service request timeout")
        return None
    except Exception as e:
        print(f"Error calling AI API: {e}")
        return None
    

if __name__ == '__main__':
    app.run(port=5050, debug=True)