from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_conn():
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
    try:
        data = request.get_json()
        temperature = float(data["temperature"])

        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS temperatures (id SERIAL PRIMARY KEY, temperature REAL, timestamp TIMESTAMPTZ DEFAULT NOW())")
        cur.execute("INSERT INTO temperatures (temperature) VALUES (%s)", (temperature,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "OK", "received": temperature})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
