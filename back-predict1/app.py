from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def root():
    return {"message": "Service de prédiction opérationnel"}

@app.route("/predict1", methods=["POST"])
def predict1():
    input_data = request.get_json()
    # Exemple simple : retourner le même message avec une mention
    return jsonify({"service": "predict1", "input": input_data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
