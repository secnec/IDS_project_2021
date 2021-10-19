from flask import Flask, render_template
from bikePrediction import predict_balancing

app = Flask(__name__)


@app.route("/")
def index():  
    prediction = predict_balancing()
    return render_template("index.html", prediction = prediction)


@app.route("/about")
def presentation():
    return render_template("index.html")

@app.route("/project")
def project():
    return render_template("index.html")

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port='5000')