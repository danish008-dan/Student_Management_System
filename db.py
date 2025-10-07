# db.py
# Small helper functions (optional). The rest of code still uses pymysql.connect directly to match original behavior.

import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    """
    Returns a new pymysql connection using values from config.py
    """
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
