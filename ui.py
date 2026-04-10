import customtkinter as ctk
import requests

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BASE_URL = "http://127.0.0.1:5000"

COLORS = {
    "primary": "#1a73e8",
    "secondary": "#e8f0fe",
    "success": "#34a853",
    "danger": "#ea4335",
    "warning": "#fbbc04",
    "bg": "#f8f9fa",
    "card": "#ffffff",
    "text": "#202124",
    "subtext": "#5f6368"
}

class BibliothequeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📚 Bibliothèque Intelligente")
        self.geometry("1200x750")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])

        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS["primary"], height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📚  Bibliothèque Intelligente",
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=30, pady=15)

        ctk.CTkLabel(
            header,
            text="Gestion moderne avec IA",
            font=ctk.CTkFont(size=13),
            text_color="#c5d8ff"
        ).pack(side="right", padx=30)

        # Onglets
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLORS["card"],
            segmented_button_fg_color=COLORS["secondary"],
            segmented_button_selected_color=COLORS["primary"],
            segmented_button_selected_hover_color="#1557b0",
            segmented_button_unselected_color=COLORS["secondary"],
            segmented_button_unselected_hover_color="#d2e3fc",
            text_color=COLORS["text"],
            corner_radius=15
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=15)

        self.tabview.add("📚  Livres")
        self.tabview.add("➕  Ajouter")
        self.tabview.add("✏️  Modifier")
        self.tabview.add("🤖  Chatbot")

        self.build_livres_tab()
        self.build_ajouter_tab()
        self.build_modifier_tab()
        self.build_chatbot_tab()

    # ─── Onglet Livres ───
    def build_livres_tab(self):
        tab = self.tabview.tab("📚  Livres")
        tab.configure(fg_color=COLORS["bg"])

        # Barre du haut
        top = ctk.CTkFrame(tab, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            top,
            text="Liste des livres",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text"]
        ).pack(side="left")

        ctk.CTkButton(
            top,
            text="🔄  Actualiser",
            command=self.charger_livres,
            fg_color=COLORS["primary"],
            hover_color="#1557b0",
            corner_radius=8,
            width=130,
            height=35
        ).pack(side="right")

        # Zone livres
        self.livres_text = ctk.CTkTextbox(
            tab,
            fg_color=COLORS["card"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Courier", size=13),
            corner_radius=10,
            border_width=1,
            border_color="#e0e0e0"
        )
        self.livres_text.pack(fill="both", expand=True, padx=15, pady=5)
        self.charger_livres()

    def charger_livres(self):
        try:
            response = requests.get(f"{BASE_URL}/livres")
            livres = response.json()
            self.livres_text.delete("1.0", "end")
            if not livres:
                self.livres_text.insert("end", "  📭  Aucun livre dans la bibliothèque.")
                return
            self.livres_text.insert("end", f"  {'ID':<6} {'Titre':<30} {'Auteur':<25} {'Catégorie':<15} {'Statut'}\n")
            self.livres_text.insert("end", f"  {'─'*90}\n")
            for livre in livres:
                statut_icon = "✅" if livre['statut'] == 'disponible' else "❌"
                self.livres_text.insert("end",
                    f"  {livre['id_livre']:<6} {livre['titre']:<30} {livre['auteur']:<25} "
                    f"{livre['categorie']:<15} {statut_icon} {livre['statut']}\n"
                )
        except:
            self.livres_text.insert("end", "  ❌  Erreur de connexion au serveur.")

    # ─── Onglet Ajouter ───
    def build_ajouter_tab(self):
        tab = self.tabview.tab("➕  Ajouter")
        tab.configure(fg_color=COLORS["bg"])

        # Carte formulaire
        card = ctk.CTkFrame(tab, fg_color=COLORS["card"], corner_radius=15,
                            border_width=1, border_color="#e0e0e0")
        card.pack(padx=80, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            card,
            text="➕  Ajouter un nouveau livre",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(pady=20)

        fields = [("Titre du livre", "Ex: Le Petit Prince"),
                  ("Auteur", "Ex: Antoine de Saint-Exupéry"),
                  ("Catégorie", "Ex: Roman, Science, Histoire..."),
                  ("Année de publication", "Ex: 1943"),
                  ("Quantité disponible", "Ex: 3")]

        self.entries = {}
        for label, placeholder in fields:
            frame = ctk.CTkFrame(card, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=5)
            ctk.CTkLabel(frame, text=label,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=COLORS["text"], width=180,
                         anchor="w").pack(side="left")
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder,
                                 width=350, height=38, corner_radius=8,
                                 border_color="#dadce0")
            entry.pack(side="left", padx=10)
            self.entries[label] = entry

        # Statut
        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="x", padx=40, pady=5)
        ctk.CTkLabel(frame, text="Statut",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=COLORS["text"], width=180,
                     anchor="w").pack(side="left")
        self.statut_var = ctk.StringVar(value="disponible")
        ctk.CTkOptionMenu(frame, values=["disponible", "emprunté", "réservé"],
                          variable=self.statut_var, width=350, height=38,
                          fg_color=COLORS["secondary"],
                          button_color=COLORS["primary"],
                          corner_radius=8).pack(side="left", padx=10)

        ctk.CTkButton(
            card,
            text="➕  Ajouter le livre",
            command=self.ajouter_livre,
            fg_color=COLORS["primary"],
            hover_color="#1557b0",
            height=42,
            width=250,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20)

        self.msg_label = ctk.CTkLabel(card, text="",
                                       font=ctk.CTkFont(size=13))
        self.msg_label.pack()

    def ajouter_livre(self):
        data = {
            "titre": self.entries["Titre du livre"].get(),
            "auteur": self.entries["Auteur"].get(),
            "categorie": self.entries["Catégorie"].get(),
            "annee_publication": int(self.entries["Année de publication"].get() or 0),
            "quantite_disponible": int(self.entries["Quantité disponible"].get() or 1),
            "statut": self.statut_var.get()
        }
        try:
            response = requests.post(f"{BASE_URL}/livres", json=data)
            if response.status_code == 201:
                self.msg_label.configure(text="✅  Livre ajouté avec succès !",
                                         text_color=COLORS["success"])
                for entry in self.entries.values():
                    entry.delete(0, "end")
            else:
                self.msg_label.configure(text="❌  Erreur lors de l'ajout",
                                         text_color=COLORS["danger"])
        except:
            self.msg_label.configure(text="❌  Erreur de connexion",
                                     text_color=COLORS["danger"])

    # ─── Onglet Modifier ───
    def build_modifier_tab(self):
        tab = self.tabview.tab("✏️  Modifier")
        tab.configure(fg_color=COLORS["bg"])

        card = ctk.CTkFrame(tab, fg_color=COLORS["card"], corner_radius=15,
                            border_width=1, border_color="#e0e0e0")
        card.pack(padx=80, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            card,
            text="✏️  Modifier ou Supprimer un livre",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(pady=20)

        # ID + bouton charger
        id_frame = ctk.CTkFrame(card, fg_color=COLORS["secondary"], corner_radius=10)
        id_frame.pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(id_frame, text="ID du livre :",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=COLORS["text"]).pack(side="left", padx=15, pady=10)
        self.modifier_id = ctk.CTkEntry(id_frame, placeholder_text="Entrez l'ID",
                                         width=200, height=35, corner_radius=8)
        self.modifier_id.pack(side="left", padx=10)
        ctk.CTkButton(id_frame, text="🔍  Charger",
                      command=self.charger_livre,
                      fg_color=COLORS["primary"],
                      hover_color="#1557b0",
                      height=35, width=120,
                      corner_radius=8).pack(side="left", padx=10)

        # Champs
        fields = [("Titre", ""), ("Auteur", ""), ("Catégorie", ""),
                  ("Année", ""), ("Quantité", "")]
        self.modifier_entries = {}
        for label, _ in fields:
            frame = ctk.CTkFrame(card, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=4)
            ctk.CTkLabel(frame, text=label,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=COLORS["text"], width=120,
                         anchor="w").pack(side="left")
            entry = ctk.CTkEntry(frame, width=400, height=35, corner_radius=8,
                                 border_color="#dadce0")
            entry.pack(side="left", padx=10)
            self.modifier_entries[label] = entry

        # Statut
        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="x", padx=40, pady=4)
        ctk.CTkLabel(frame, text="Statut",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=COLORS["text"], width=120,
                     anchor="w").pack(side="left")
        self.modifier_statut = ctk.StringVar(value="disponible")
        ctk.CTkOptionMenu(frame, values=["disponible", "emprunté", "réservé"],
                          variable=self.modifier_statut, width=400, height=35,
                          fg_color=COLORS["secondary"],
                          button_color=COLORS["primary"],
                          corner_radius=8).pack(side="left", padx=10)

        # Boutons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="💾  Modifier",
                      command=self.modifier_livre,
                      fg_color=COLORS["success"],
                      hover_color="#2d8f47",
                      height=42, width=180,
                      corner_radius=10,
                      font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15)

        ctk.CTkButton(btn_frame, text="🗑️  Supprimer",
                      command=self.supprimer_livre,
                      fg_color=COLORS["danger"],
                      hover_color="#c62828",
                      height=42, width=180,
                      corner_radius=10,
                      font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15)

        self.modifier_msg = ctk.CTkLabel(card, text="",
                                          font=ctk.CTkFont(size=13))
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
                self.modifier_msg.configure(text="✅  Livre chargé !",
                                            text_color=COLORS["success"])
            else:
                self.modifier_msg.configure(text="❌  Livre non trouvé",
                                            text_color=COLORS["danger"])
        except:
            self.modifier_msg.configure(text="❌  Erreur de connexion",
                                        text_color=COLORS["danger"])

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
                self.modifier_msg.configure(text="✅  Livre modifié avec succès !",
                                            text_color=COLORS["success"])
            else:
                self.modifier_msg.configure(text="❌  Erreur de modification",
                                            text_color=COLORS["danger"])
        except:
            self.modifier_msg.configure(text="❌  Erreur de connexion",
                                        text_color=COLORS["danger"])

    def supprimer_livre(self):
        id_livre = self.modifier_id.get()
        try:
            response = requests.delete(f"{BASE_URL}/livres/{id_livre}")
            if response.status_code == 200:
                self.modifier_msg.configure(text="✅  Livre supprimé avec succès !",
                                            text_color=COLORS["success"])
                self.modifier_id.delete(0, "end")
                for entry in self.modifier_entries.values():
                    entry.delete(0, "end")
            else:
                self.modifier_msg.configure(text="❌  Erreur de suppression",
                                            text_color=COLORS["danger"])
        except:
            self.modifier_msg.configure(text="❌  Erreur de connexion",
                                        text_color=COLORS["danger"])

    # ─── Onglet Chatbot ───
    def build_chatbot_tab(self):
        tab = self.tabview.tab("🤖  Chatbot")
        tab.configure(fg_color=COLORS["bg"])

        ctk.CTkLabel(
            tab,
            text="🤖  Assistant Bibliothèque IA",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(pady=10)

        self.chat_text = ctk.CTkTextbox(
            tab,
            fg_color=COLORS["card"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Helvetica", size=13),
            corner_radius=12,
            border_width=1,
            border_color="#e0e0e0"
        )
        self.chat_text.pack(fill="both", expand=True, padx=20, pady=5)
        self.chat_text.insert("end", "🤖  Bonjour ! Je suis votre assistant bibliothèque.\n"
                                      "     Posez-moi une question sur nos livres ! 😊\n\n")

        # Barre d'envoi
        bottom = ctk.CTkFrame(tab, fg_color=COLORS["card"],
                               corner_radius=12, border_width=1,
                               border_color="#e0e0e0")
        bottom.pack(fill="x", padx=20, pady=10)

        self.question_entry = ctk.CTkEntry(
            bottom,
            placeholder_text="💬  Posez votre question ici...",
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            border_width=0,
            height=45
        )
        self.question_entry.pack(side="left", fill="x", expand=True, padx=15)
        self.question_entry.bind("<Return>", lambda e: self.envoyer_question())

        ctk.CTkButton(
            bottom,
            text="Envoyer 🚀",
            command=self.envoyer_question,
            fg_color=COLORS["primary"],
            hover_color="#1557b0",
            height=38,
            width=130,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="right", padx=10, pady=5)

    def envoyer_question(self):
        question = self.question_entry.get()
        if not question:
            return
        self.chat_text.insert("end", f"👤  Vous : {question}\n")
        self.question_entry.delete(0, "end")
        self.chat_text.insert("end", "⏳  En attente de réponse...\n")
        self.update()
        try:
            response = requests.post(f"{BASE_URL}/chat",
                                     json={"question": question})
            data = response.json()
            reponse = data.get("reponse", "Erreur ❌")
            # Supprimer le message d'attente
            self.chat_text.delete("end-2l", "end-1l")
            self.chat_text.insert("end", f"🤖  Assistant : {reponse}\n\n")
        except:
            self.chat_text.delete("end-2l", "end-1l")
            self.chat_text.insert("end", "❌  Erreur de connexion au serveur.\n\n")
        self.chat_text.see("end")

if __name__ == "__main__":
    app = BibliothequeApp()
    app.mainloop()