from tkinter import messagebox, ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.bibliotheques import *
from src.visualisations import *

class ApplicationPython:
    def __init__(self, root):
        self.root = root
        self.root.title("Bibliothèque - Tableau de bord")
        self.root.geometry("1000x600")
        self.root.configure(bg="#faf3e0")


        style = ttk.Style(self.root)
        style.theme_use('vista')
        style.configure("Treeview.Heading", font=("Calibri", 12, "bold"), foreground="#9C27B0")
        style.configure("Treeview", font=("Calibri", 10))
        style.configure("TButton", font=("Calibri", 12, "bold"), foreground="white", background="#9C27B0")
        style.map("TButton",
                  foreground=[('active', 'white')],
                  background=[('active', '#ad1457')])

        self.biblio = Bibliotheque()
        self.biblio.charger_livres()
        self.biblio.charger_membres()
        self.livres = self.biblio.livres
        self.membres = self.biblio.membres
        self.synchroniser_statuts()
        self.canvas = None
        self.setup_ui()

    def synchroniser_statuts(self):

        from src.bibliotheques import StatutLivre

        # Remettre tous les livres en disponible
        for livre in self.livres.values():
            livre.statut = StatutLivre.DISPONIBLE

        # Mettre à jour les livres empruntés
        for membre in self.membres.values():
            for isbn in membre.liste_livres_empruntes:
                if isbn in self.livres:
                    self.livres[isbn].statut = StatutLivre.EMPRUNTE

        # Sauvegarder les changements si nécessaire
        self.biblio.sauvegarder_livres()

    def setup_ui(self):
        self.sidebar = tk.Frame(self.root, bg="#2c2c54", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.main = tk.Frame(self.root, bg="#faf3e0")
        self.main.pack(side="right", fill="both", expand=True)

        btns = [
            ("Livres", self.show_livres),
            ("Ajouter Livre", self.show_ajouter_livre),
            ("Membres", self.show_membres),
            ("Résumé Statistique", self.afficher_resume_stats),
            ("Emprunter Livre", self.show_emprunt_livre),
            ("Rendre Livre", self.show_retour_livre),

        ]

        for text, command in btns:
            b = tk.Button(self.sidebar, text=text, command=command,
                          bg="#F06292",
                          fg="white",
                          font=("Montserrat", 12, "bold"),
                          relief="flat",
                          bd=0,
                          padx=20,  # Espacement horizontal
                          cursor="hand2",  # Curseur main au survol
                          activebackground="#EC407A",  # Rose légèrement plus foncé au clic
                          activeforeground="white",
                          height=2)  # Hauteur fixe pour uniformité
            b.pack(fill="x", pady=8, padx=12)  # Espacement ajusté


            def on_enter(e, button=b):
                button.config(bg="#EC407A")  # Rose plus foncé au survol

            def on_leave(e, button=b):
                button.config(bg="#F06292")  # Retour au rose initial

            b.bind("<Enter>", on_enter)
            b.bind("<Leave>", on_leave)
        self.show_livres()

    def clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def show_emprunt_livre(self):
        self.clear_main()
        ttk.Label(self.main, text="Emprunter un Livre", font=("calibri", 16, "bold"),
                  foreground="#2c2c54").pack(pady=15)

        form_frame = tk.Frame(self.main, bg="#f7f7f7")
        form_frame.pack(pady=10)

        # Champ ID Membre
        tk.Label(form_frame, text="ID Membre", bg="#f7f7f7",
                 font=("calibri", 12)).grid(row=0, column=0, padx=5, pady=7)
        self.entry_id_emprunt = tk.Entry(form_frame, font=("calibri", 12))
        self.entry_id_emprunt.grid(row=0, column=1, padx=5, pady=7)

        # Champ ISBN Livre
        tk.Label(form_frame, text="ISBN Livre", bg="#f7f7f7",
                 font=("calibri", 12)).grid(row=1, column=0, padx=5, pady=7)
        self.entry_isbn_emprunt = tk.Entry(form_frame, font=("calibri", 12))
        self.entry_isbn_emprunt.grid(row=1, column=1, padx=5, pady=7)

        # Bouton de validation
        tk.Button(self.main, text="Valider l'emprunt",
                  bg="#e91e63", fg="white",
                  font=("calibri", 14, "bold"),
                  command=self.valider_emprunt,
                  relief="flat", bd=0,
                  activebackground="#ad1457",
                  activeforeground="white").pack(pady=20)

    def show_retour_livre(self):
        self.clear_main()
        ttk.Label(self.main, text="Retour d'un Livre", font=("calibri", 16, "bold"), foreground="#FFC0CB").pack(pady=15)

        form_frame = tk.Frame(self.main, bg="#f7f7f7")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="ID Membre", bg="#f7f7f7", font=("calibri", 12)).grid(row=0, column=0, padx=5, pady=7)
        self.entry_id_retour = tk.Entry(form_frame, font=("calibri", 12))
        self.entry_id_retour.grid(row=0, column=1, padx=5, pady=7)

        tk.Label(form_frame, text="ISBN Livre", bg="#f7f7f7", font=("calibri", 12)).grid(row=1, column=0, padx=5,
                                                                                         pady=7)
        self.entry_isbn_retour = tk.Entry(form_frame, font=("calibri", 12))
        self.entry_isbn_retour.grid(row=1, column=1, padx=5, pady=7)

        tk.Button(self.main, text="Valider le retour", bg="#FFC0CB", fg="white", font=("calibri", 14, "bold"),
                  command=self.valider_retour, relief="flat", bd=0,
                  activebackground="#f7f7f7", activeforeground="white").pack(pady=20)


    def valider_emprunt(self):
        from src.bibliotheques import StatutLivre

        id_membre = self.entry_id_emprunt.get().strip()
        isbn = self.entry_isbn_emprunt.get().strip()

        # Vérification des champs vides
        if not id_membre or not isbn:
            messagebox.showwarning("Champs manquants",
                                   "Veuillez remplir tous les champs.")
            return

        # Vérification de l'existence du membre
        if id_membre not in self.membres:
            messagebox.showerror("Erreur",
                                 f"Membre avec ID {id_membre} introuvable.")
            return

        # Vérification de l'existence du livre
        if isbn not in self.livres:
            messagebox.showerror("Erreur",
                                 f"Livre avec ISBN {isbn} introuvable.")
            return

        livre = self.livres[isbn]
        membre = self.membres[id_membre]

        # Vérification du nombre de livres empruntés
        if len(membre.liste_livres_empruntes) >= 3:
            messagebox.showerror("Erreur",
                                 f"Le membre {membre.nom} a déjà atteint la limite de 3 livres empruntés.")
            return

        # Vérification si le livre n'est pas déjà emprunté par ce membre
        if isbn in membre.liste_livres_empruntes:
            messagebox.showerror("Erreur",
                                 f"Le membre {membre.nom} a déjà emprunté ce livre.")
            return

        # Vérification si le livre est disponible
        if livre.statut == StatutLivre.EMPRUNTE:
            # Recherche de qui a emprunté le livre
            emprunteur = None
            for m in self.membres.values():
                if isbn in m.liste_livres_empruntes:
                    emprunteur = m
                    break

            if emprunteur:
                messagebox.showerror("Erreur",
                                     f"Le livre '{livre.titre}' est déjà emprunté par {emprunteur.nom}.")
            else:
                messagebox.showerror("Erreur",
                                     f"Le livre '{livre.titre}' n'est pas disponible.")
            return

        # Effectuer l'emprunt
        livre.statut = StatutLivre.EMPRUNTE
        membre.liste_livres_empruntes.append(isbn)
        self.biblio.sauvegarder_livres()
        self.biblio.sauvegarder_membres()
        # Enregistrer dans l'historique
        self.biblio.enregistrer_historique(id_membre=id_membre, ISBN=isbn, action="EMPRUNT")

        # Message de confirmation détaillé
        messagebox.showinfo("Succès",
                            f"Le livre '{livre.titre}' a été emprunté par {membre.nom}.\n"
                            f"Nombre de livres empruntés : {len(membre.liste_livres_empruntes)}/3")

        # Réinitialisation des champs
        self.entry_id_emprunt.delete(0, tk.END)
        self.entry_isbn_emprunt.delete(0, tk.END)

        # Rafraîchir l'affichage
        self.show_livres()

    def valider_retour(self):
        from src.bibliotheques import StatutLivre

        id_membre = self.entry_id_retour.get().strip()
        isbn = self.entry_isbn_retour.get().strip()

        if not id_membre or not isbn:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        if id_membre not in self.membres:
            messagebox.showerror("Erreur", f"Membre avec ID {id_membre} introuvable.")
            return

        if isbn not in self.livres:
            messagebox.showerror("Erreur", f"Livre avec ISBN {isbn} introuvable.")
            return

        membre = self.membres[id_membre]
        livre = self.livres[isbn]

        if isbn not in membre.liste_livres_empruntes:
            messagebox.showerror("Erreur", f"Ce livre n'a pas été emprunté par {membre.nom}.")
            return

        membre.liste_livres_empruntes.remove(isbn)
        livre.statut = StatutLivre.DISPONIBLE
        self.biblio.sauvegarder_livres()
        self.biblio.sauvegarder_membres()
        # Enregistrer dans l'historique
        self.biblio.enregistrer_historique(id_membre=id_membre, ISBN=isbn, action="RETOUR")

        messagebox.showinfo("Succès", f"Le livre '{livre.titre}' a été retourné par {membre.nom}.")
        self.entry_id_retour.delete(0, tk.END)
        self.entry_isbn_retour.delete(0, tk.END)
        self.show_livres()

    def afficher_resume_stats(self):
        from src.bibliotheques import StatutLivre

        auteurs = set(l.auteur for l in self.livres.values())
        nb_auteurs = len(auteurs)
        nb_livres = len(self.livres)
        nb_empruntes = sum(1 for l in self.livres.values() if l.statut == StatutLivre.EMPRUNTE)

        self.clear_main()

        ttk.Label(self.main, text="Résumé Statistiques", font=("calibri", 20, "bold"), foreground="#e91e63").pack(
            pady=15)

        frame_barres = tk.Frame(self.main, bg="#f7f7f7")
        frame_barres.pack(padx=30, pady=30, fill="x")

        def barre_stat(label, valeur, max_val=nb_livres):
            lbl = tk.Label(frame_barres, text=f"{label}:", bg="#f7f7f7",
                           font=("calibri", 14, "bold"), fg="#e91e63")
            lbl.pack(anchor="w", pady=(15, 0))
            canvas = tk.Canvas(frame_barres, height=25, bg="#dcdde1", highlightthickness=0)
            canvas.pack(fill="x", pady=7)
            largeur = int((valeur / max_val) * 450) if max_val else 0
            canvas.create_rectangle(0, 0, largeur, 25, fill="#e91e63")
            canvas.create_text(largeur + 50, 13, text=str(valeur), anchor="w",
                               font=("calibri", 14, "bold"), fill="#2f3640")

        barre_stat("Nombre d'auteurs", nb_auteurs)
        barre_stat("Nombre de livres", nb_livres)
        barre_stat("Livres empruntés", nb_empruntes)

        btn = tk.Button(self.main, text="Voir Graphiques", command=self.show_stats,
                        bg="#e91e63", fg="white", font=("calibri", 14, "bold"), relief="flat", bd=0,
                        activebackground="#ad1457", activeforeground="white")
        btn.pack(pady=25)

    def show_livres(self):
        self.clear_main()
        ttk.Label(self.main, text="Liste des Livres", font=("calibri", 16, "bold"), foreground="#2c2c54").pack(pady=15)
        columns = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Statut")
        tree = ttk.Treeview(self.main, columns=columns, show="headings", height=18)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        for l in self.livres.values():
            statut_affiche = l.statut.value if isinstance(l.statut, StatutLivre) else l.statut
            tree.insert("", "end", values=(
                l.ISBN, l.titre, l.auteur, l.annee, l.genre, statut_affiche
            ))

        tree.pack(fill="both", expand=True, padx=20, pady=15)

    def show_ajouter_livre(self):
        self.clear_main()
        ttk.Label(self.main, text="Ajouter un Livre", font=("calibri", 16, "bold"), foreground="#2c2c54").pack(pady=15)

        form_frame = tk.Frame(self.main, bg="#f7f7f7")
        form_frame.pack(pady=10)

        labels = ["ISBN", "Titre", "Auteur", "Année", "Genre", "Statut (Disponible/Emprunté)"]
        self.entries_livre = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#f7f7f7", font=("calibri", 12)).grid(row=i, column=0, padx=5, pady=7, sticky="e")
            entry = tk.Entry(form_frame, font=("calibri", 12))
            entry.grid(row=i, column=1, padx=5, pady=7, sticky="w")
            self.entries_livre[label] = entry

        btn_frame = tk.Frame(self.main, bg="#f7f7f7")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Ajouter", bg="#e91e63", fg="white", font=("calibri", 14, "bold"),
                  command=self.ajouter_livre, relief="flat", bd=0,
                  activebackground="#ad1457", activeforeground="white").pack()

    def ajouter_livre(self):
        isbn = self.entries_livre["ISBN"].get().strip()
        titre = self.entries_livre["Titre"].get().strip()
        auteur = self.entries_livre["Auteur"].get().strip()
        annee = self.entries_livre["Année"].get().strip()
        genre = self.entries_livre["Genre"].get().strip()
        statut_str = self.entries_livre["Statut (Disponible/Emprunté)"].get().strip().lower()

        if not (isbn and titre and auteur and annee and genre and statut_str):
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        if not annee.isdigit() or int(annee) < 0:
            messagebox.showerror("Erreur", "Année invalide.")
            return

        statut_valide = {"disponible", "emprunté", "emprunte"}
        if statut_str not in statut_valide:
            messagebox.showerror("Erreur", "Statut doit être 'Disponible' ou 'Emprunté'.")
            return

        statut = "Disponible" if statut_str == "disponible" else "Emprunté"

        if isbn in self.livres:
            messagebox.showerror("Erreur", f"Le livre avec ISBN {isbn} existe déjà.")
            return

        from src.bibliotheques import Livre

        livre = Livre(isbn, titre, auteur, int(annee), genre)
        livre.statut = statut

        self.biblio.ajouter_livre(livre)
        self.biblio.sauvegarder_livres()
        self.livres = self.biblio.livres

        messagebox.showinfo("Succès", f"Livre '{titre}' ajouté avec succès.")
        self.show_livres()

    def show_membres(self):
        self.clear_main()
        ttk.Label(self.main, text="Gestion des Membres", font=("calibri", 16, "bold"),
                  foreground="#e91e63").pack(pady=15)

        # Frame pour le formulaire d'ajout
        form_frame = tk.Frame(self.main, bg="#f7f7f7")
        form_frame.pack(pady=10)

        # Champs de saisie
        tk.Label(form_frame, text="ID", bg="#f7f7f7",
                 font=("calibri", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(form_frame, font=("calibri", 12))
        self.entry_id.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Nom", bg="#f7f7f7",
                 font=("calibri", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.entry_nom = tk.Entry(form_frame, font=("calibri", 12))
        self.entry_nom.grid(row=0, column=3, padx=5)

        # Configuration du tableau
        columns = ("ID", "Nom", "Livres Empruntés")
        self.tree_membres = ttk.Treeview(self.main, columns=columns, show="headings", height=15)

        # Configuration des colonnes
        self.tree_membres.heading("ID", text="ID")
        self.tree_membres.heading("Nom", text="Nom")
        self.tree_membres.heading("Livres Empruntés", text="Livres Empruntés")

        # Ajustement de la largeur des colonnes
        self.tree_membres.column("ID", anchor="center", width=100)
        self.tree_membres.column("Nom", anchor="center", width=150)
        self.tree_membres.column("Livres Empruntés", anchor="w", width=400)

        # Remplissage du tableau
        for m in self.membres.values():
            # Conversion des ISBN en titres de livres
            livres_empruntes = []
            for isbn in m.liste_livres_empruntes:
                if isbn in self.livres:
                    livre = self.livres[isbn]
                    livres_empruntes.append(f"{livre.titre} ({isbn})")

            livres_text = " | ".join(livres_empruntes) if livres_empruntes else "Aucun livre emprunté"

            self.tree_membres.insert("", "end", values=(m.id, m.nom, livres_text))

        # Ajout d'une barre de défilement horizontale
        scrollbar_x = ttk.Scrollbar(self.main, orient="horizontal",
                                    command=self.tree_membres.xview)
        self.tree_membres.configure(xscrollcommand=scrollbar_x.set)

        # Placement du tableau et de la barre de défilement
        self.tree_membres.pack(fill="both", expand=True, padx=20, pady=(15, 0))
        scrollbar_x.pack(fill="x", padx=20, pady=(0, 15))

        # Frame pour les boutons
        btn_frame = tk.Frame(self.main, bg="#f7f7f7")
        btn_frame.pack(pady=10)

        # Boutons d'action
        tk.Button(btn_frame, text="Ajouter Membre",
                  bg="#e91e63", fg="white",
                  font=("calibri", 14, "bold"),
                  command=self.ajouter_membre,
                  relief="flat", bd=0,
                  activebackground="#ad1457",
                  activeforeground="white").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Supprimer Sélection",
                  bg="#c0392b", fg="white",
                  font=("calibri", 14, "bold"),
                  command=self.supprimer_membre,
                  relief="flat", bd=0,
                  activebackground="#a93226",
                  activeforeground="white").pack(side="left", padx=10)

    def ajouter_membre(self):
        id_ = self.entry_id.get().strip()
        nom = self.entry_nom.get().strip()

        if not id_ or not nom:
            messagebox.showwarning("Champs manquants", "Veuillez remplir les champs ID et Nom.")
            return

        if id_ in self.membres:
            messagebox.showerror("Erreur", f"Le membre avec l'ID {id_} existe déjà.")
            return

        membre = Membre(id_, nom)
        self.biblio.enregistrer_membre(membre)
        self.tree_membres.insert("", "end", values=(id_, nom, ""))
        self.biblio.sauvegarder_membres()
        messagebox.showinfo("Ajout", f"Membre '{nom}' ajouté.")

        self.entry_id.delete(0, tk.END)
        self.entry_nom.delete(0, tk.END)

    def supprimer_membre(self):
        selection = self.tree_membres.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un membre à supprimer.")
            return

        for item in selection:
            id_ = self.tree_membres.item(item, "values")[0]
            del self.membres[id_]
            self.tree_membres.delete(item)

        self.biblio.sauvegarder_membres()
        messagebox.showinfo("Suppression", "Membre supprimé avec succès.")

    def show_stats(self):
        self.clear_main()
        ttk.Label(self.main, text="Statistiques", font=("calibri", 16, "bold"), foreground="#e91e63").pack(pady=25)

        btn_frame = tk.Frame(self.main, bg="#f7f7f7")
        btn_frame.pack()

        btn1 = tk.Button(btn_frame, text="Diagramme par Genre", command=self.afficher_diagramme_genre,
                         bg="#e91e63", fg="white", font=("calibri", 12, "bold"), relief="flat", bd=0,
                         activebackground="#ad1457", activeforeground="white")
        btn2 = tk.Button(btn_frame, text="Top Auteurs", command=self.afficher_histogramme_auteurs,
                         bg="#e91e63", fg="white", font=("calibri", 12, "bold"), relief="flat", bd=0,
                         activebackground="#ad1457", activeforeground="white")
        btn3 = tk.Button(btn_frame, text="Emprunts 30 jours", command=self.afficher_courbe_emprunts,
                         bg="#e91e63", fg="white", font=("calibri", 12, "bold"), relief="flat", bd=0,
                         activebackground="#ad1457", activeforeground="white")

        for b in (btn1, btn2, btn3):
            b.pack(side="left", padx=15, pady=15)

        self.fig_frame = tk.Frame(self.main, bg="#f7f7f7")
        self.fig_frame.pack(fill="both", expand=True, padx=30, pady=30)

    def afficher_diagramme_genre(self):
        fig = diagramme_genre(self.livres)
        self.afficher_figure(fig)

    def afficher_histogramme_auteurs(self):
        fig = histogramme_auteurs(self.livres)
        self.afficher_figure(fig)

    def afficher_courbe_emprunts(self):
        fig = courbe_emprunts()
        self.afficher_figure(fig)

    def afficher_figure(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if fig is None:
            messagebox.showinfo("Information", "Aucune donnée disponible pour ce graphique.")
            return
        self.canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)  # Fermeture de la figure poue liberation de memoire


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationPython(root)
    root.mainloop()
