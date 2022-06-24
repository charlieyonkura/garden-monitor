from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

class PlantData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_recorded = db.Column(db.DateTime, default = datetime.now())
    humidity = db.Column(db.Float, nullable = False)
    temperature = db.Column(db.Float, nullable = False)

class WateringEvent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_watered = db.Column(db.DateTime, default = datetime.now())

@app.route("/")
def index():
    pd = PlantData.query.paginate()
    we = WateringEvent.query.paginate()
    return render_template("index.html", plantdata=pd.query.get(pd.total), waterdata=we.query.get(we.total)) #sends most recent records from each table

if __name__ == "__main__":
    app.run(debug = True)
