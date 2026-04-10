import customtkinter as ctk
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BASE_URL = "http://127.0.0.1:5000"

class BibliothequeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📚 Bibliothèque Intelligente")
        self.geometry("1100x700")
        self.resizable(False, False)
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tabview.add("📚 Livres")
        self.tabview.add("➕ Ajouter")
        self.tabview.add("✏️ Modifier/Supprimer")
        self.tabview.add("🤖 Chatbot")
        
        self.build_livres_tab()
        self.build_ajouter_tab()
        self.build_modifier_tab()
        self.build_chatbot_tab()

    def build_livres_tab(self):
        tab = self.tabview.tab("📚 Livres")
        ctk.CTkButton(tab, text="🔄 Actualiser", command=self.charger_livres).pack(pady=10)
        self.livres_text = ctk.CTkTextbox(tab, width=1000, height=500)
        self.livres_text.pack(pady=10)
        self.charger_livres()

    def charger_livres(self):
        try:
            response = requests.get(f"{BASE_URL}/livres")
            livres = response.json()
            self.livres_text.delete("1.0", "end")
            if not livres:
                self.livres_text.insert("end", "Aucun livre dans la bibliothèque.")
                return
            for livre in livres:
                self.livres_text.insert("end",
                    f"📖 ID: {livre['id_livre']} | {livre['titre']} "
                    f"— {livre['auteur']} | {livre['categorie']} "
                    f"| {livre['statut']}\n"
                    f"{'─'*80}\n"
                )
        except:
            self.livres_text.insert("end", "❌ Erreur de connexion au serveur.")

    def build_ajouter_tab(self):
        tab = self.tabview.tab("➕ Ajouter")
        fields = ["Titre", "Auteur", "Catégorie", "Année", "Quantité"]
        self.entries = {}
        for field in fields:
            ctk.CTkLabel(tab, text=field).pack(pady=5)
            entry = ctk.CTkEntry(tab, width=400)
            entry.pack(pady=5)
            self.entries[field] = entry
        ctk.CTkLabel(tab, text="Statut").pack(pady=5)
        self.statut_var = ctk.StringVar(value="disponible")
        ctk.CTkOptionMenu(tab, values=["disponible", "emprunté", "réservé"],
                          variable=self.statut_var).pack(pady=5)
        ctk.CTkButton(tab, text="➕ Ajouter le livre",
                      command=self.ajouter_livre).pack(pady=20)
        self.msg_label = ctk.CTkLabel(tab, text="")
        self.msg_label.pack()

    def ajouter_livre(self):
        data = {
            "titre": self.entries["Titre"].get(),
            "auteur": self.entries["Auteur"].get(),
            "categorie": self.entries["Catégorie"].get(),
            "annee_publication": int(self.entries["Année"].get() or 0),
            "quantite_disponible": int(self.entries["Quantité"].get() or 1),
            "statut": self.statut_var.get()
        }
        try:
            response = requests.post(f"{BASE_URL}/livres", json=data)
            if response.status_code == 201:
                self.msg_label.configure(text="✅ Livre ajouté avec succès !", text_color="green")
                for entry in self.entries.values():
                    entry.delete(0, "end")
            else:
                self.msg_label.configure(text="❌ Erreur lors de l'ajout", text_color="red")
        except:
            self.msg_label.configure(text="❌ Erreur de connexion", text_color="red")

    def build_modifier_tab(self):
        tab = self.tabview.tab("✏️ Modifier/Supprimer")
        ctk.CTkLabel(tab, text="ID du livre").pack(pady=5)
        self.modifier_id = ctk.CTkEntry(tab, width=400,
                                         placeholder_text="Entrez l'ID du livre")
        self.modifier_id.pack(pady=5)
        ctk.CTkButton(tab, text="🔍 Charger le livre",
                      command=self.charger_livre).pack(pady=10)
        fields = ["Titre", "Auteur", "Catégorie", "Année", "Quantité"]
        self.modifier_entries = {}
        for field in fields:
            ctk.CTkLabel(tab, text=field).pack(pady=3)
            entry = ctk.CTkEntry(tab, width=400)
            entry.pack(pady=3)
            self.modifier_entries[field] = entry
        ctk.CTkLabel(tab, text="Statut").pack(pady=3)
        self.modifier_statut = ctk.StringVar(value="disponible")
        ctk.CTkOptionMenu(tab, values=["disponible", "emprunté", "réservé"],
                          variable=self.modifier_statut).pack(pady=3)
        frame = ctk.CTkFrame(tab)
        frame.pack(pady=15)
        ctk.CTkButton(frame, text="💾 Modifier", command=self.modifier_livre,
                      fg_color="green").pack(side="left", padx=10)
        ctk.CTkButton(frame, text="🗑️ Supprimer", command=self.supprimer_livre,
                      fg_color="red").pack(side="left", padx=10)
        self.modifier_msg = ctk.CTkLabel(tab, text="")
        self.modifier_msg.pack()

    def charger_livre(self):
        id_livre = self.modifier_id.get()
        if not id_livre:
            return
        try:
            response = requests.get(f"{BASE_URL}/livres/{id_livre}")
            if response.status_code == 200:
                livre = response.json()
                self.modifier_entries["Titre"].delete(0, "end")
                self.modifier_entries["Titre"].insert(0, livre['titre'])
                self.modifier_entries["Auteur"].delete(0, "end")
                self.modifier_entries["Auteur"].insert(0, livre['auteur'])
                self.modifier_entries["Catégorie"].delete(0, "end")
                self.modifier_entries["Catégorie"].insert(0, livre['categorie'])
                self.modifier_entries["Année"].delete(0, "end")
                self.modifier_entries["Année"].insert(0, livre['annee_publication'])
                self.modifier_entries["Quantité"].delete(0, "end")
                self.modifier_entries["Quantité"].insert(0, livre['quantite_disponible'])
                self.modifier_statut.set(livre['statut'])
                self.modifier_msg.configure(text="✅ Livre chargé !", text_color="green")
            else:
                self.modifier_msg.configure(text="❌ Livre non trouvé", text_color="red")
        except:
            self.modifier_msg.configure(text="❌ Erreur de connexion", text_color="red")

    def modifier_livre(self):
        id_livre = self.modifier_id.get()
        data = {
            "titre": self.modifier_entries["Titre"].get(),
            "auteur": self.modifier_entries["Auteur"].get(),
            "categorie": self.modifier_entries["Catégorie"].get(),
            "annee_publication": int(self.modifier_entries["Année"].get() or 0),
            "quantite_disponible": int(self.modifier_entries["Quantité"].get() or 1),
            "statut": self.modifier_statut.get()
        }
        try:
            response = requests.put(f"{BASE_URL}/livres/{id_livre}", json=data)
            if response.status_code == 200:
                self.modifier_msg.configure(text="✅ Livre modifié avec succès !", text_color="green")
            else:
                self.modifier_msg.configure(text="❌ Erreur de modification", text_color="red")
        except:
            self.modifier_msg.configure(text="❌ Erreur de connexion", text_color="red")

    def supprimer_livre(self):
        id_livre = self.modifier_id.get()
        try:
            response = requests.delete(f"{BASE_URL}/livres/{id_livre}")
            if response.status_code == 200:
                self.modifier_msg.configure(text="✅ Livre supprimé avec succès !", text_color="green")
                self.modifier_id.delete(0, "end")
                for entry in self.modifier_entries.values():
                    entry.delete(0, "end")
            else:
                self.modifier_msg.configure(text="❌ Erreur de suppression", text_color="red")
        except:
            self.modifier_msg.configure(text="❌ Erreur de connexion", text_color="red")

    def build_chatbot_tab(self):
        tab = self.tabview.tab("🤖 Chatbot")
        self.chat_text = ctk.CTkTextbox(tab, width=1000, height=450)
        self.chat_text.pack(pady=10)
        self.chat_text.insert("end", "🤖 Bonjour ! Je suis votre assistant bibliothèque. Posez-moi une question !\n\n")
        frame = ctk.CTkFrame(tab)
        frame.pack(fill="x", padx=10, pady=10)
        self.question_entry = ctk.CTkEntry(frame,
                                            placeholder_text="Posez votre question ici...",
                                            width=850)
        self.question_entry.pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Envoyer 🚀",
                      command=self.envoyer_question).pack(side="left")

    def envoyer_question(self):
        question = self.question_entry.get()
        if not question:
            return
        self.chat_text.insert("end", f"👤 Vous : {question}\n")
        self.question_entry.delete(0, "end")
        try:
            response = requests.post(f"{BASE_URL}/chat", json={"question": question})
            data = response.json()
            reponse = data.get("reponse", "Erreur ❌")
            self.chat_text.insert("end", f"🤖 Assistant : {reponse}\n\n")
        except:
            self.chat_text.insert("end", "❌ Erreur de connexion au serveur.\n\n")
        self.chat_text.see("end")

if __name__ == "__main__":
    app = BibliothequeApp()
    app.mainloop()