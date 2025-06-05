from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/meteo")
def get_meteo():
    return jsonify({"Paris": "Clear"})

# Execution via Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
