import pyodbc
import secrets

conn_str = (
	"Driver={ODBC Driver 17 for SQL Server};"
	"Server=localhost\\SQLEXPRESS;"
	"Database=PracticeDB;"
	"Trusted_Connection=yes;"
	"Pooling=False;"
	"Connection Timeout=30;"
	"Encrypt=yes;"
	"TrustServerCertificate=yes;"
	"Application Name=vscode-mssql;"
	"Application Intent=ReadWrite;"
)

def readAccountFromDB(account, password):
    """
    讀取資料庫中與給定 account 與 password 相符的帳號資料。
    參數:
        account (str): 要查詢的帳號識別字串。
        password (str): 與帳號比對的密碼（程式中以明文傳入；建議在儲存與比對前使用安全哈希）。
    回傳:
        tuple | None: 若找到相符資料，回傳 cursor.fetchone() 所得到的一列（通常為 tuple）；若無則回傳 None。
    例外:
        pyodbc.Error: 若連線或查詢發生錯誤，會向上拋出 pyodbc 的例外。
        NameError: 若未定義 conn_str 或未引入 pyodbc，可能會發生 NameError。
    備註:
        - 使用參數化查詢 ("?") 以避免 SQL 注入。
        - 函式會開啟資料庫連線並在完成後關閉 cursor 與 connection。
        - 建議不要以明文儲存或比對密碼，改用安全的雜湊與驗證機制。
    """
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    query = "SELECT * FROM accounts WHERE account = ? AND password = ?"
    cursor.execute(query, (account, password))

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def updateAccountFromDB(account, password, token):
    """
    更新指定 account 與 password 的帳號列，將其 token 欄位設為提供的值。

    參數:
        account (str): 帳號識別。
        password (str): 密碼（目前為明文比對，建議改用雜湊）。
        token (str): 要更新到資料表的 token 值。

    回傳:
        bool: 若有任一列被更新則回傳 True，否則回傳 False。

    例外:
        pyodbc.Error: 若資料庫操作發生錯誤，例外會被拋出給呼叫者處理。
    """
    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = "UPDATE accounts SET token = ? WHERE account = ? AND password = ?"
        cursor.execute(query, (token, account, password))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return affected > 0
    except pyodbc.Error:
        raise
    finally:
        if conn:
            conn.close()

print(readAccountFromDB('sean.ma@thetainformation.com', 'A1234567890'))

token = secrets.token_hex(16)

print(updateAccountFromDB('sean.ma@thetainformation.com', 'A1234567890', token))