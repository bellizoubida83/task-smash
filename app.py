from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'atlasatlas-secret-key-2024'

db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form["content"].strip()
        if current_task:
            new_task = MyTask(content=current_task)
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
    tasks = MyTask.query.order_by(MyTask.created.desc()).all()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = MyTask.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"].strip()
        db.session.commit()
        return redirect("/")
    return render_template("update.html", task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
