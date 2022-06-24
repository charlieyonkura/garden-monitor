from importlib.resources import contents
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import exifread

webcamPath = os.path.relpath("static\images")
imagePrefix = "img"
numberLength = 3 #abcdxxx.jpg -> numberLength = 3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model): #setting columns for database
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self): #function to return string
        return "<Task %r>" % self.id


@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"] #id from form
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task) #add to database
            db.session.commit()
            return redirect("/")
        except:
            return "Error adding task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #returns all task objects
        return render_template("index.html", tasks=tasks) #checks in \templates\

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Error deleting task"

@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"] #set task's content to input from form
        try:
            db.session.commit() #no need to add new entry, only commit changes
            return redirect("/")
        except:
            return "Error updating task"
    else:
        return render_template("update.html", task=task)

@app.route("/webcam/")
def webcam():
    contents = os.listdir(webcamPath)
    files = [image for image in contents if image[:len(imagePrefix)] == imagePrefix] #if it contains the prefix, allow through filter
    image = str(max([int(n[len(imagePrefix):-4]) for n in files])) #removes prefix & file extension, returns max image number
    
    path = os.path.join(webcamPath, imagePrefix + ("0" * (numberLength - len(image))) + image + files[0][-4:]) #frankenstein together the path
    tags = exifread.process_file(open(path, "rb"))
    datetime_obj = datetime.strptime(tags["Image DateTime"].printable, "%Y:%m:%d %H:%M:%S")
    
    return render_template("webcam.html", img = path.replace("\\", "/"), date = datetime_obj)

if __name__ == "__main__":
    app.run(debug = True)