from google import genai
from app.models import get_all_livres
from config import GEMINI_API_KEY

# Configurer Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

def get_context_bibliotheque():
    livres = get_all_livres()
    if not livres:
        return "La bibliothèque est vide pour le moment."
    
    context = "Voici les livres disponibles dans la bibliothèque :\n\n"
    for livre in livres:
        context += f"""
        - ID: {livre['id_livre']}
          Titre: {livre['titre']}
          Auteur: {livre['auteur']}
          Catégorie: {livre['categorie']}
          Année: {livre['annee_publication']}
          Quantité: {livre['quantite_disponible']}
          Statut: {livre['statut']}
        """
    return context

def poser_question(question):
    context = get_context_bibliotheque()
    
    prompt = f"""
    Tu es un assistant intelligent pour une bibliothèque.
    Tu dois répondre aux questions des utilisateurs en te basant 
    uniquement sur les données réelles de la bibliothèque.
    
    Données actuelles de la bibliothèque :
    {context}
    
    Question de l'utilisateur : {question}
    
    Réponds de manière claire et précise en français.
    """
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=prompt
    )
    return response.text