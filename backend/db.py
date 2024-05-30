import psycopg2
from config import db_config


def db_connection():
    conn = psycopg2.connect(**db_config)
    return conn

def init_table():
    conn = db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(250) NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    
