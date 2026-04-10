import os

# Clé API Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Base de données
DATABASE = "bibliotheque.db"

# Configuration Flask
DEBUG = True
SECRET_KEY = "bibliotheque_secret_key_2025"