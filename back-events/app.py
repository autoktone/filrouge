from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

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

    availability = request.args.get('availability')  # Morning, Afternoon, Evening, Night
    sports = request.args.get("sports")
    participation = request.args.get("participation")
    now = datetime.utcnow()
    params = [now]

    query = """
        SELECT id, event_date, location, name, participation_type, popularity_score, sport_type FROM events
        WHERE event_date > %s
    """

    #if not sports or not participation:
        #return jsonify({"error": "Missing required query parameters"}), 400

    if sports:
        query += " AND sport_type = ANY(%s)"
        sport_list = [s.strip().capitalize() for s in sports.split(",") if s.strip()]
        params.append(sport_list)

    if participation:
        query += " AND participation_type = ANY(%s)"
        participation_list = [p.strip().capitalize() for p in participation.split(",") if p.strip()]
        params.append(participation_list)

    if availability:
        if availability == "Morning":
            query += " AND CAST(strftime('%H', event_date) AS INTEGER) BETWEEN 6 AND 11"
        elif availability == "Afternoon":
            query += " AND CAST(strftime('%H', event_date) AS INTEGER) BETWEEN 12 AND 16"
        elif availability == "Evening":
            query += " AND CAST(strftime('%H', event_date) AS INTEGER) BETWEEN 17 AND 21"
        elif availability == "Night":
            query += " AND (CAST(strftime('%H', event_date) AS INTEGER) >= 22 OR CAST(strftime('%H', event_date) AS INTEGER) <= 5)"

    query += " ORDER BY event_date ASC, popularity_score DESC LIMIT 9"

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        # Récupération automatique des noms de colonnes
        #columns = [desc[0] for desc in cur.description]
        
        # Construction Objet JSON contenant un tableau d'objets "event"
        result = []
        for row in rows:
            #event = dict(zip(columns, row))
            event = dict(row) # row se comporte comme un dictionnaire

            # Conversion de la date en format HTTP/JSON
            if isinstance(event['event_date'], datetime):
                event['event_date'] = event['event_date'].strftime('%a, %d %b %Y %H:%M:%S GMT')
            result.append(event)
        return jsonify({"events": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)