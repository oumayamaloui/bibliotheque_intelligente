from flask import Blueprint, request, jsonify
from app.models import (ajouter_livre, get_all_livres, get_livre_by_id,
                        modifier_livre, supprimer_livre, rechercher_livres)
from app.chatbot import poser_question
books_bp = Blueprint('books', __name__)

# Ajouter un livre
@books_bp.route('/livres', methods=['POST'])
def add_livre():
    data = request.get_json()
    ajouter_livre(
        data['titre'], data['auteur'], data['categorie'],
        data['annee_publication'], data['quantite_disponible'], data['statut']
    )
    return jsonify({'message': 'Livre ajouté avec succès ✅'}), 201

# Afficher tous les livres
@books_bp.route('/livres', methods=['GET'])
def list_livres():
    livres = get_all_livres()
    return jsonify([dict(l) for l in livres])

# Afficher un livre par ID
@books_bp.route('/livres/<int:id>', methods=['GET'])
def get_livre(id):
    livre = get_livre_by_id(id)
    if livre:
        return jsonify(dict(livre))
    return jsonify({'message': 'Livre non trouvé ❌'}), 404

# Modifier un livre
@books_bp.route('/livres/<int:id>', methods=['PUT'])
def update_livre(id):
    data = request.get_json()
    modifier_livre(
        id, data['titre'], data['auteur'], data['categorie'],
        data['annee_publication'], data['quantite_disponible'], data['statut']
    )
    return jsonify({'message': 'Livre modifié avec succès ✅'})

# Supprimer un livre
@books_bp.route('/livres/<int:id>', methods=['DELETE'])
def delete_livre(id):
    supprimer_livre(id)
    return jsonify({'message': 'Livre supprimé avec succès ✅'})

# Rechercher un livre
@books_bp.route('/livres/recherche', methods=['GET'])
def search_livre():
    query = request.args.get('q', '')
    livres = rechercher_livres(query)
    return jsonify([dict(l) for l in livres])
# Chatbot
@books_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'message': 'Question vide ❌'}), 400
    
    reponse = poser_question(question)
    return jsonify({'reponse': reponse})