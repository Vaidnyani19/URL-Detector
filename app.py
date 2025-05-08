# Updated app.py
from flask import Flask, request, jsonify
import joblib
import xgboost as xgb

app = Flask(__name__)

vectorizer = joblib.load("vectorizer.pkl")
model = joblib.load("url_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    transformed_url = vectorizer.transform([url])
    prediction = model.predict(transformed_url)[0]
    
    label_map = {0: 'benign', 1: 'defacement', 2: 'phishing', 3: 'malware'}
    result = label_map.get(prediction, "unknown")

    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
