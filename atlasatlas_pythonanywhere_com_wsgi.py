# /var/www/atlasatlas_pythonanywhere_com_wsgi.py

import sys
import os

# Ajouter le chemin de votre projet
path = '/home/atlasatlas/myflaskapp'
if path not in sys.path:
    sys.path.append(path)

# Importer l'application Flask directement
from app import app as application