from flask import Flask, render_template, request
import pickle
import os
from database import init_db, insert_log, get_counts

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    duration = int(request.form["duration"])
    src_bytes = int(request.form["src_bytes"])
    dst_bytes = int(request.form["dst_bytes"])
    count = int(request.form["count"])

    features = [[duration, src_bytes, dst_bytes, count]]
    prediction = model.predict(features)

    # Threat Classification
    if prediction[0] == 1:
        if count > 80 or src_bytes > 15000:
            risk = "Critical 🔴"
        elif count > 50:
            risk = "High 🟠"
        else:
            risk = "Medium 🟡"
        result = "⚠ Attack Detected"
    else:
        risk = "Low 🟢"
        result = "✅ Secure Traffic"

    insert_log(duration, src_bytes, dst_bytes, count, risk)

    counts = get_counts()

    return render_template("result.html",
                           result=result,
                           risk=risk,
                           counts=counts)

@app.route("/simulate")
def simulate():
    duration = 500
    src_bytes = 20000
    dst_bytes = 15000
    count = 120

    risk = "Critical 🔴"
    insert_log(duration, src_bytes, dst_bytes, count, risk)

    return render_template("result.html",
                           result="🚨 Simulated Critical Attack",
                           risk=risk,
                           counts=get_counts())
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)