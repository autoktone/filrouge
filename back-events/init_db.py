import psycopg2
import os
import csv
from datetime import datetime

conn = psycopg2.connect(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST")
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS events;")
cur.execute("""
    CREATE TABLE events (
        id SERIAL PRIMARY KEY,
        name TEXT,
        date TIMESTAMP,
        location TEXT,
        sport_type TEXT,
        participation_type TEXT,
        popularity_score INT
    );
""")

with open('data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        name = row['name']
        location = row['location']
        sport_type = row['sport_type']
        participation_type = row['participation_type']
        popularity_score = int(row['popularity_score'])

        # Conversion date (ex: 07/11/2025 06:22 PM)
        date = datetime.strptime(row['date'], "%d/%m/%Y %I:%M %p")

        cur.execute("""
            INSERT INTO events (name, date, location, sport_type, participation_type, popularity_score)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, date, location, sport_type, participation_type, popularity_score))

conn.commit()
cur.close()
conn.close()