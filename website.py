from importlib.resources import contents
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import exifread

imagesPath = os.path.relpath("static\images")
imagePrefix = "img"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Image():
    images = []
    def __init__(self, path):
        self.path = path
        self.parsePath()
        self.getDateTime()
    def parsePath(self):
        split = os.path.splitext(os.path.split(self.path)[1])
        name = split[0]
        self.ext = split[1]
        i = 0
        while(not name[i:].isdigit()):
            i += 1
        self.number = name[i:]
        self.prefix = name[:i]
    def getDateTime(self):
        tags = exifread.process_file(open(self.path, "rb"))
        self.datetime = datetime.strptime(tags["Image DateTime"].printable, "%Y:%m:%d %H:%M:%S")
    def getImages(path, prefix): #returns array of files if prefix matches
        contents = os.listdir(path)
        Image.images = [Image(os.path.join(path, image)) for image in contents if image[:len(prefix)] == prefix]
    def getMostRecent():
        dates = [image.datetime for image in Image.images]
        mostRecentDate = max(dates)
        mostRecentImage = Image.images[dates.index(mostRecentDate)]
        return mostRecentImage

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
    Image.getImages(imagesPath, imagePrefix)
    img = Image.getMostRecent()
    return render_template("webcam.html", imgPath = img.path.replace("\\", "/"), imgDateTime = img.datetime)

if __name__ == "__main__":
    app.run(debug = True)