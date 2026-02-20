# imports
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_scss import Scss  
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

# my app
app = Flask(__name__)

# Configuration # Configuration - Adaptée pour PythonAnywhere
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'votre-clé-secrète-unique'  # Changez ceci !

db = SQLAlchemy(app)

# Modèle
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)  # ✅ Boolean au lieu de Integer
    created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self) -> str:
        return f"<Task {self.id}>"


# Routes principales
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form["content"].strip()
        
        if not current_task:
            flash("Veuillez entrer une tâche valide", "error")
            return redirect("/")
        
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("✅ Tâche ajoutée avec succès !", "success")
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Erreur: {e}", "error")
            return redirect("/")
    
    tasks = MyTask.query.order_by(MyTask.created.desc()).all()
    return render_template("index.html", tasks=tasks)

# Route pour supprimer
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("🗑️ Tâche supprimée", "success")
        return redirect("/")
    except:
        flash("❌ Erreur lors de la suppression", "error")
        return redirect("/")

# Route pour mettre à jour
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = MyTask.query.get_or_404(id)
    
    if request.method == "POST":
        new_content = request.form["content"].strip()
        if new_content:
            task.content = new_content
            try:
                db.session.commit()
                flash("✏️ Tâche mise à jour", "success")
                return redirect("/")
            except:
                flash("❌ Erreur lors de la mise à jour", "error")
    
    return render_template("update.html", task=task)

# ✅ Route AJAX pour marquer comme terminé (sans rechargement)
@app.route("/toggle-complete/<int:id>", methods=["POST"])
def toggle_complete(id):
    task = MyTask.query.get_or_404(id)
    task.complete = not task.complete
    try:
        db.session.commit()
        return jsonify({"success": True, "complete": task.complete})
    except:
        return jsonify({"success": False}), 500

# Initialisation
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)