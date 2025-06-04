from flask import Flask, request, jsonify
import jwt
import datetime
import os

app = Flask(__name__)
SECRET_KEY = os.getenv("JWT_SECRET", "changeme")

@app.route("/auth", methods=["POST"])
def login():
    data = request.get_json()
	
	# A vérifier dans une base réelle des utilisateurs (version future)
    if data.get("username") == "admin" and data.get("password") == "password":
        token = jwt.encode({
            "sub": "admin",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"access_token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
		
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)		