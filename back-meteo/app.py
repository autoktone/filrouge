from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Input param : userlocation (town) au moment de l'appel à cet URI
@app.route("/meteo", methods=["GET"])
def get_meteo():
	
	# What is the location of the user ?
    town = request.args.get("town", "Paris")
	# OpenWeatherMap.org service API key 
    API_KEY = request.args.get("API_KEY")
	
    if not API_KEY:
        return jsonify({"error": "API_KEY is required"}), 400

    # Input param : userlocation au moment de l'appel
    url = f"http://api.openweathermap.org/data/2.5/weather?q={town}&appid={API_KEY}&lang=fr&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": f"Erreur API météo: {response.status_code}"}

    # Exemple : 'Rain', 'Clear', 'Clouds'...
    data = response.json()
    condition = data['weather'][0]['main'].lower()
    return jsonify({"weather": condition})	

# Execution via Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
