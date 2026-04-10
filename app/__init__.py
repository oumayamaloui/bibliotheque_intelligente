from flask import Flask
from config import DATABASE, SECRET_KEY, DEBUG

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG
    app.config['DATABASE'] = DATABASE

    # Importer les routes
    from app.routes import books_bp
    app.register_blueprint(books_bp)

    return app