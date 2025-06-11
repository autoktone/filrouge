from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
		dbname=os.getenv("DATABASE_NAME"),
		user=os.getenv("DATABASE_USER"),
		password=os.getenv("DATABASE_PASSWORD"),
		host=os.getenv("DATABASE_HOST")
    )

@app.route("/events", methods=["GET"])
def get_events():
    sports = request.args.get("sports")
    participation = request.args.get("participation")

    if not sports or not participation:
        return jsonify({"error": "Missing required query parameters"}), 400

    sport_list = [s.strip().capitalize() for s in sports.split(",") if s.strip()]
    participation_list = [p.strip().capitalize() for p in participation.split(",") if p.strip()]

    query = """
        SELECT * FROM events
        WHERE sport_type = ANY(%s) AND participation_type = ANY(%s)
        ORDER BY event_date ASC
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (sport_list, participation_list))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)