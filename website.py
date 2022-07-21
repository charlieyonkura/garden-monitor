from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

DATA_INTERVAL = 5 #minutes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):    
    humidity = db.Column(db.Float, nullable = False)
    temperature = db.Column(db.Float, nullable = False)
    time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key = True)

    def __repr__(Self):
        return "<Data " + Self.id + ">"

@app.route("/")
def index():
    d = Data.query.paginate()
    return render_template("index.html", data=d.query.get(d.total)) #sends most recent record

@app.route("/data/")
def data():
    d = Data.query.all()
    nextDateTime = d[len(d) - 1].time + timedelta(minutes = DATA_INTERVAL)
    return render_template("data.html", data = d, nextDT = nextDateTime) #sends all records

if __name__ == "__main__":
    app.run(debug = True)