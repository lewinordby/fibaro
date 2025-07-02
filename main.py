from flask import Flask, request
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

def get_db_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def get_db_conn():
    # Debug-utskrift for å se verdier
    print("DB_NAME =", os.getenv("DB_NAME"))
    print("DB_USER =", os.getenv("DB_USER"))
    print("DB_PASS =", os.getenv("DB_PASS"))
    print("DB_HOST =", os.getenv("DB_HOST"))
    print("DB_PORT =", os.getenv("DB_PORT"))
    
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route("/log", methods=["POST"])
def log_temp():
    data = request.json
    temp = float(data.get("temperature", 0.0))
    now = datetime.now()

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            temperature REAL
        )
    """)
    cur.execute("INSERT INTO temperatures (timestamp, temperature) VALUES (%s, %s)", (now, temp))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "OK", "received": temp}, 200
