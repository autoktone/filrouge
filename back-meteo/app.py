from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Input param : userlocation (town) au moment de l'appel à cet URI
@app.route("/meteo")
def get_meteo(town: str = "Paris"):

    # Google API Key can be stores in .env file
    API_KEY = "7e0f2a976c6290e910b8ffcd4236982d"

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
