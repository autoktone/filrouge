from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/meteo")
def get_meteo():
	
	# Input param : userlocation au moment de l'appel
    return jsonify({"weather": "Rainy"})

# Execution via Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
