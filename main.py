import os
from dotenv import load_dotenv
from app import create_app
from app.models import init_db

# Charger les variables d'environnement (.env)
load_dotenv()

# Créer l'application Flask
app = create_app()

if __name__ == '__main__':
    # Initialiser la base de données
    init_db()
    # Lancer l'application
    app.run(debug=True)