import sqlite3
from config import DATABASE

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livres (
            id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            categorie TEXT NOT NULL,
            annee_publication INTEGER,
            quantite_disponible INTEGER DEFAULT 1,
            statut TEXT DEFAULT 'disponible'
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données initialisée ✅")

# CRUD

def ajouter_livre(titre, auteur, categorie, annee, quantite, statut):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO livres (titre, auteur, categorie, annee_publication, quantite_disponible, statut)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titre, auteur, categorie, annee, quantite, statut))
    conn.commit()
    conn.close()

def get_all_livres():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    livres = cursor.fetchall()
    conn.close()
    return livres

def get_livre_by_id(id_livre):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE id_livre = ?', (id_livre,))
    livre = cursor.fetchone()
    conn.close()
    return livre

def modifier_livre(id_livre, titre, auteur, categorie, annee, quantite, statut):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE livres 
        SET titre=?, auteur=?, categorie=?, annee_publication=?, 
            quantite_disponible=?, statut=?
        WHERE id_livre=?
    ''', (titre, auteur, categorie, annee, quantite, statut, id_livre))
    conn.commit()
    conn.close()

def supprimer_livre(id_livre):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id_livre = ?', (id_livre,))
    conn.commit()
    conn.close()

def rechercher_livres(query):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM livres 
        WHERE titre LIKE ? OR auteur LIKE ?
    ''', (f'%{query}%', f'%{query}%'))
    livres = cursor.fetchall()
    conn.close()
    return livres