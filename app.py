# ============================================================
# Task Smash 2.0 - Flask Application
# Déployé sur PythonAnywhere : atlasatlas.pythonanywhere.com
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

# ============================================================
# Initialisation de l'Application
# ============================================================

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'atlasatlas-secret-key-change-in-production-2024'

# ✅ Initialisation de la base de données (niveau du module)
db = SQLAlchemy(app)

# ============================================================
# Modèle de Base de Données
# ============================================================

class MyTask(db.Model):
    """Modèle pour les tâches"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Task {self.id}>"

# ============================================================
# Routes
# ============================================================

@app.route("/", methods=["POST", "GET"])
def index():
    """Page d'accueil - Liste et ajout de tâches"""
    if request.method == "POST":
        current_task = request.form["content"].strip()
        
        if current_task:
            new_task = MyTask(content=current_task)
            try:
                db.session.add(new_task)
                db.session.commit()
                flash("✅ Tâche ajoutée avec succès !", "success")
                return redirect("/")
            except Exception as e:
                db.session.rollback()
                flash(f"❌ Erreur: {e}", "error")
        else:
            flash("⚠️ Veuillez entrer une tâche valide", "error")
    
    # Récupérer toutes les tâches
    tasks = MyTask.query.order_by(MyTask.created.desc()).all()
    return render_template("index.html", tasks=tasks)

# -------------------------------------------------------------

@app.route("/delete/<int:id>")
def delete(id):
    """Supprimer une tâche"""
    task = MyTask.query.get_or_404(id)
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash("🗑️ Tâche supprimée", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Erreur lors de la suppression: {e}", "error")
    
    return redirect("/")

# -------------------------------------------------------------

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    """Mettre à jour une tâche"""
    task = MyTask.query.get_or_404(id)
    
    if request.method == "POST":
        new_content = request.form["content"].strip()
        
        if new_content:
            task.content = new_content
            try:
                db.session.commit()
                flash("✏️ Tâche mise à jour", "success")
                return redirect("/")
            except Exception as e:
                db.session.rollback()
                flash(f"❌ Erreur lors de la mise à jour: {e}", "error")
        else:
            flash("⚠️ Le contenu ne peut pas être vide", "error")
    
    return render_template("update.html", task=task)

# -------------------------------------------------------------

@app.route("/toggle-complete/<int:id>", methods=["POST"])
def toggle_complete(id):
    """Marquer une tâche comme complétée (AJAX)"""
    task = MyTask.query.get_or_404(id)
    
    try:
        task.complete = not task.complete
        db.session.commit()
        return jsonify({"success": True, "complete": task.complete})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# -------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    """Gestion des erreurs 404"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    """Gestion des erreurs 500"""
    db.session.rollback()
    return render_template("500.html"), 500

# ============================================================
# Point d'Entrée Principal
# ============================================================

if __name__ == "__main__":
    # Créer le dossier instance s'il n'existe pas
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # Créer les tables de la base de données
    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")
    
    # Lancer le serveur de développement
    app.run(debug=True, host='0.0.0.0', port=5000)