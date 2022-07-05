from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Data(db.Model):    
    humidity = db.Column(db.Float, nullable = False)
    temperature = db.Column(db.Float, nullable = False)
    time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key = True)

@app.route("/")
def index():
    d = Data.query.paginate()
    return render_template("index.html", data=d.query.get(d.total)) #sends most recent records

if __name__ == "__main__":
    app.run(debug = True)
