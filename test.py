
import pyodbc

def readAccountFromDB(account, password):
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=CustmizeGPT;"
        "UID=sa;"
        "PWD=Str0ng!Passw0rd;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        query = "SELECT * FROM accounts WHERE account = ? AND password = ?"
        cursor.execute(query, (account, password))
        
        row = cursor.fetchone()
        
        print(row)

        if row:
            result = {
                "account": row.account,
                "password": row.password
            }
        else:
            result = {}
        
        print(row.account, row.password)

        cursor.close()
        conn.close()
        
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return {}


def updateAccountTokenInDB(account, token):
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=CustmizeGPT;"
        "UID=sa;"
        "PWD=Str0ng!Passw0rd;"
        "Encrypt=no;"
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


def insertAccountToDB(account, password, token=None):
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=CustmizeGPT;"
        "UID=sa;"
        "PWD=Str0ng!Passw0rd;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )

    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = "INSERT INTO accounts (account, password, token) VALUES (?, ?, ?)"
        cursor.execute(query, (account, password, token))
        conn.commit()

        return True
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
    


print(updateAccountTokenInDB('user1', 'pass2'))