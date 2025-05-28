from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def root():
    return {"message": "Service de prédiction opérationnel"}

@app.route("/predict")
def predict():
    return jsonify({"prediction": "chat", "confidence": 0.92})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
