# SQL DB Connection
import pyodbc
import os

class Database:
    def __init__(self):
        self.conn_str = os.getenv("SQL_CONN_STRING")

    def query(self, query, params):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results