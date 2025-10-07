# create_data_tables.py
# Reads schema.sql and executes it to create database and tables (if privileges allow)

import pymysql
import os

SQL_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")

def run_schema():
    try:
        # connect to server (without selecting database) so we can create database if missing
        con = pymysql.connect(host="localhost", user="root", password="", charset='utf8mb4', autocommit=True)
        cur = con.cursor()
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql = f.read()
        for stmt in sql.split(';'):
            s = stmt.strip()
            if s:
                cur.execute(s)
        con.close()
        print("Schema executed successfully.")
    except Exception as e:
        print("Failed to execute schema:", e)

if __name__ == "__main__":
    run_schema()
