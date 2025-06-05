from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Input param : userlocation (town) au moment de l'appel à cet URI
@app.route("/meteo")
def get_meteo():
	
	# Mode bouchon
	town = "Paris"
	
	# Google API Key can be stores in .env file
	api_key = "7e0f2a976c6290e910b8ffcd4236982d"
	
	# Input param : userlocation au moment de l'appel
    url = f"http://api.openweathermap.org/data/2.5/weather?q="+town+"&appid="+api_key+"&lang=fr&units=metric"
    response = requests.get(url)
    data = response.json()

    # Exemple : 'Rain', 'Clear', 'Clouds'...
    condition = data['weather'][0]['main'].lower()
    return jsonify({"weather": condition})

# Execution via Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
