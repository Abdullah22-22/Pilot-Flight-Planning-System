import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="private_jet",
        auth_plugin="mysql_native_password"
    )
    return conn

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor(dictionary=True)
