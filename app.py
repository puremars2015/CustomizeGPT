from flask import Flask, jsonify, render_template, request
import requests
import secrets
import pyodbc

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

def readAccountFromDB(account, password):
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=master;"
        "UID=sa;"
        "PWD=Str0ng!Passw0rd;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        query = "SELECT * FROM accounts WHERE account = ? AND password = ?"
        cursor.execute(query, (account, password))
        
        row = cursor.fetchone()
        
        if row:
            result = {
                "account": row.account,
                "password": row.password
            }
        else:
            result = {}
        
        cursor.close()
        conn.close()
        
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return {}

def updateAccountFromDB(account, token):
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=master;"
        "UID=sa;"
        "PWD=Str0ng!Passw0rd;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = "UPDATE accounts SET token = ? WHERE account = ?"
        cursor.execute(query, (token, account))
        conn.commit()

        return cursor.rowcount > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if conn is not None:
                conn.close()

def calln8n(prompt):
    response = requests.get("http://localhost:5678/webhook/3ba0092d-cc71-4227-91c5-565ca262c097", params={"content": prompt})
    message = response.json()
    return message


if __name__ == '__main__':
    app.run(port=5050, debug=True)