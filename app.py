import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, url_for, render_template

app = Flask(__name__)

# Load the model and scaler
regmodel = pickle.load(open("regmodel.pkl", "rb"))
scalar = pickle.load(open("scaling.pkl", "rb"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict_api", methods=["POST"])
def predict_api():
    data = request.json["data"]
    print(data)

    # Convert data to array
    new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)[0]

    # Convert numpy type to Python float
    return jsonify({"prediction": float(output)})


@app.route("/predict", methods=["POST"])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scalar.transform(np.array(data).reshape(1, -1))

    output = regmodel.predict(final_input)[0]

    return render_template(
        "home.html", prediction_text=f"The House price prediction is {output}"
    )


if __name__ == "__main__":
    app.run(debug=True)
