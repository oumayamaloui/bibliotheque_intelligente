# 📚 Bibliothèque Intelligente avec Chatbot IA

Une application de gestion de bibliothèque moderne avec un assistant IA intégré.

## 🛠️ Technologies utilisées

- **Python 3.14**
- **Flask** — Backend / API REST
- **SQLite** — Base de données
- **CustomTkinter** — Interface graphique
- **Google Gemini** — Chatbot IA

## 🚀 Installation et lancement

### 1. Cloner le projet
```
git clone https://github.com/oumayamaloui/bibliotheque_intelligente.git
cd bibliotheque_intelligente
```

### 2. Créer l'environnement virtuel
```
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les bibliothèques
```
pip install -r requirements.txt
```

### 4. Configurer la clé API
Créer un fichier `.env` et ajouter :
```
GEMINI_API_KEY=ta_clé_api_gemini
```

### 5. Lancer l'application
Terminal 1 — Serveur Flask :
```
venv\Scripts\python.exe main.py
```
Terminal 2 — Interface :
```
venv\Scripts\python.exe ui.py
```

## ✨ Fonctionnalités

- ➕ Ajouter des livres
- 📚 Afficher tous les livres
- ✏️ Modifier un livre
- 🗑️ Supprimer un livre
- 🤖 Chatbot IA pour répondre aux questions

## 👤 Auteur
- **oumayamaloui**