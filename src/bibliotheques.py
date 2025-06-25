<<<<<<< HEAD
from datetime import datetime
from enum import Enum
from exception import *

 #Je choisi de travailler avec livre et membre et historiques sans extension a cause d'un erreur sans solution donc j'adapte a cette idee

class StatutLivre(Enum):
    DISPONIBLE = "Disponible"
    EMPRUNTE = "Emprunté"


class Livre:
    def __init__(self, ISBN, titre, auteur, annee, genre):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = StatutLivre.DISPONIBLE

    def __str__(self):
        return f"{self.ISBN} | {self.titre} - {self.auteur} ({self.annee}) [{self.genre}] [{self.statut.value}]"


class Membre:
    def __init__(self, id_membre, nom):
        self.id = id_membre
        self.nom = nom
        self.liste_livres_empruntes = []

    def __str__(self):
        return f"{self.id} - {self.nom} | Livres : {self.liste_livres_empruntes}"


class Bibliotheque:
    MAX_EMPRUNTS = 3

    def __init__(self):
        self.livres = {}
        self.membres = {}
        self.charger_livres()
        self.charger_membres()
#Permet d'ajouter un livre dans le fichier
    def ajouter_livre(self, livre: Livre):
        self.livres[livre.ISBN] = livre
#Permet de supprimer un livre dans le fichier livre
    def supprimer_livre(self, livre: Livre):
        if livre.ISBN in self.livres:
            del self.livres[livre.ISBN]
#Permet d'enregistrer un membre dans le fichier membre
    def enregistrer_membre(self, membre: Membre):
        self.membres[membre.id] = membre

    def emprunter_livre(self, id_membre, ISBN):
        
        if id_membre not in self.membres:
            raise MembreInexistantError("Membre non trouvé.")
        if ISBN not in self.livres:
            raise LivreInexistantError("Livre non trouvé.")

        livre = self.livres[ISBN]
        membre = self.membres[id_membre]

        if livre.statut == StatutLivre.EMPRUNTE:
            for m in self.membres.values():
                if ISBN in m.liste_livres_empruntes:
                    raise LivreIndisponibleError(f"Livre déjà emprunté par {m.nom}.")
            raise LivreIndisponibleError("Livre déjà emprunté.")

        if len(membre.liste_livres_empruntes) >= self.MAX_EMPRUNTS:
            raise QuotaEmpruntDepasseError("Quota dépassé.") #ou QuotaEmpruntDepasseError()

        livre.statut = StatutLivre.EMPRUNTE
        membre.liste_livres_empruntes.append(ISBN)
        self.sauvegarder_livres()
        self.sauvegarder_membres()
        #Permet de synchroniser application
        self.enregistrer_historique(id_membre, ISBN, "EMPRUNT")

    def retourner_livre(self, id_membre, ISBN):
        if id_membre not in self.membres:
            raise MembreInexistantError("Membre non trouvé.")
        if ISBN not in self.livres:
            raise LivreInexistantError("Livre non trouvé.")

        livre = self.livres[ISBN]
        membre = self.membres[id_membre]

        if ISBN in membre.liste_livres_empruntes:
            membre.liste_livres_empruntes.remove(ISBN)
            livre.statut = StatutLivre.DISPONIBLE
            self.sauvegarder_livres()
            self.sauvegarder_membres()
            self.enregistrer_historique(id_membre, ISBN, "RETOUR")
        else:
            raise Exception("Ce membre n'a pas emprunté ce livre !")

    def sauvegarder_livres(self, chemin="livres"):
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                for l in self.livres.values():
                    statut = l.statut.value if isinstance(l.statut, StatutLivre) else l.statut
                    f.write(f"{l.ISBN};{l.titre};{l.auteur};{l.annee};{l.genre};{statut}\n")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des livres : {e}")

    def charger_livres(self, chemin="livres"):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                livres = {}
                for ligne in f:
                    parts = ligne.strip().split(";")
                    if len(parts) == 6:
                        isbn, titre, auteur, annee, genre, statut_str = parts
                        livre = Livre(isbn, titre, auteur, annee, genre)

                        statut_str = statut_str.strip().lower()
                        if statut_str == "emprunté":
                            livre.statut = StatutLivre.EMPRUNTE
                        else:
                            livre.statut = StatutLivre.DISPONIBLE

                        livres[isbn] = livre
                self.livres = livres
                return livres
        except FileNotFoundError:
            print(f"Le fichier {chemin} n'existe pas.")
            self.livres = {}
            return {}

    def sauvegarder_membres(self, chemin="membres"):
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                for m in self.membres.values():
                    livres_empruntes = ",".join(m.liste_livres_empruntes)
                    f.write(f"id:{m.id};nom:{m.nom};livres_empruntes:{livres_empruntes}\n")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des membres : {e}")

    def charger_membres(self, chemin="membres"):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                membres = {}
                for ligne in f:
                    donnees = {}
                    parts = ligne.strip().split(";")
                    for part in parts:
                        if ":" in part:
                            cle, valeur = part.split(":", 1)
                            donnees[cle] = valeur

                    if "id" in donnees and "nom" in donnees:
                        membre = Membre(donnees["id"], donnees["nom"])
                        if "livres_empruntes" in donnees and donnees["livres_empruntes"]:
                            membre.liste_livres_empruntes = donnees["livres_empruntes"].split(",")
                        else:
                            membre.liste_livres_empruntes = []
                        membres[membre.id] = membre

                self.membres = membres
                return membres
        except FileNotFoundError:
            print(f"Le fichier {chemin} n'existe pas.")
            self.membres = {}
            return {}

    def enregistrer_historique(self, id_membre, ISBN, action):
        date = datetime.now().strftime("%Y-%m-%d")
        ligne = f"{date};{ISBN};{id_membre};{action}\n"
        try:
            with open("historiques", "a", encoding="utf-8") as f:
                f.write(ligne)
        except IOError as e:
            print(f"Erreur enregistrement historique : {e}")
=======
from datetime import datetime
from enum import Enum
from exception import *


class StatutLivre(Enum):
    DISPONIBLE = "Disponible"
    EMPRUNTE = "Emprunté"


class Livre:
    def __init__(self, ISBN, titre, auteur, annee, genre):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = StatutLivre.DISPONIBLE

    def __str__(self):
        return f"{self.ISBN} | {self.titre} - {self.auteur} ({self.annee}) [{self.genre}] [{self.statut.value}]"


class Membre:
    def __init__(self, id_membre, nom):
        self.id = id_membre
        self.nom = nom
        self.liste_livres_empruntes = []

    def __str__(self):
        return f"{self.id} - {self.nom} | Livres : {self.liste_livres_empruntes}"


class Bibliotheque:
    MAX_EMPRUNTS = 3

    def __init__(self):
        self.livres = {}
        self.membres = {}
        self.charger_livres()
        self.charger_membres()

    def ajouter_livre(self, livre: Livre):
        self.livres[livre.ISBN] = livre

    def supprimer_livre(self, livre: Livre):
        if livre.ISBN in self.livres:
            del self.livres[livre.ISBN]

    def enregistrer_membre(self, membre: Membre):
        self.membres[membre.id] = membre

    def emprunter_livre(self, id_membre, ISBN):
        if id_membre not in self.membres:
            raise MembreInexistantError("Membre non trouvé.")
        if ISBN not in self.livres:
            raise LivreInexistantError("Livre non trouvé.")

        livre = self.livres[ISBN]
        membre = self.membres[id_membre]

        if livre.statut == StatutLivre.EMPRUNTE:
            for m in self.membres.values():
                if ISBN in m.liste_livres_empruntes:
                    raise LivreIndisponibleError(f"Livre déjà emprunté par {m.nom}.")
            raise LivreIndisponibleError("Livre déjà emprunté.")

        if len(membre.liste_livres_empruntes) >= self.MAX_EMPRUNTS:
            raise QuotaEmpruntDepasseError("Quota dépassé.")

        livre.statut = StatutLivre.EMPRUNTE
        membre.liste_livres_empruntes.append(ISBN)
        self.sauvegarder_livres()
        self.sauvegarder_membres()
        self.enregistrer_historique(id_membre, ISBN, "EMPRUNT")

    def retourner_livre(self, id_membre, ISBN):
        if id_membre not in self.membres:
            raise MembreInexistantError("Membre non trouvé.")
        if ISBN not in self.livres:
            raise LivreInexistantError("Livre non trouvé.")

        livre = self.livres[ISBN]
        membre = self.membres[id_membre]

        if ISBN in membre.liste_livres_empruntes:
            membre.liste_livres_empruntes.remove(ISBN)
            livre.statut = StatutLivre.DISPONIBLE
            self.sauvegarder_livres()
            self.sauvegarder_membres()
            self.enregistrer_historique(id_membre, ISBN, "RETOUR")
        else:
            raise Exception("Ce membre n'a pas emprunté ce livre.")

    def sauvegarder_livres(self, chemin="livres"):
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                for l in self.livres.values():
                    statut = l.statut.value if isinstance(l.statut, StatutLivre) else l.statut
                    f.write(f"{l.ISBN};{l.titre};{l.auteur};{l.annee};{l.genre};{statut}\n")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des livres : {e}")

    def charger_livres(self, chemin="livres"):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                livres = {}
                for ligne in f:
                    parts = ligne.strip().split(";")
                    if len(parts) == 6:
                        isbn, titre, auteur, annee, genre, statut_str = parts
                        livre = Livre(isbn, titre, auteur, annee, genre)

                        statut_str = statut_str.strip().lower()
                        if statut_str == "emprunté":
                            livre.statut = StatutLivre.EMPRUNTE
                        else:
                            livre.statut = StatutLivre.DISPONIBLE

                        livres[isbn] = livre
                self.livres = livres
                return livres
        except FileNotFoundError:
            print(f"Le fichier {chemin} n'existe pas.")
            self.livres = {}
            return {}

    def sauvegarder_membres(self, chemin="membres"):
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                for m in self.membres.values():
                    livres_empruntes = ",".join(m.liste_livres_empruntes)
                    f.write(f"id:{m.id};nom:{m.nom};livres_empruntes:{livres_empruntes}\n")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des membres : {e}")

    def charger_membres(self, chemin="membres"):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                membres = {}
                for ligne in f:
                    donnees = {}
                    parts = ligne.strip().split(";")
                    for part in parts:
                        if ":" in part:
                            cle, valeur = part.split(":", 1)
                            donnees[cle] = valeur

                    if "id" in donnees and "nom" in donnees:
                        membre = Membre(donnees["id"], donnees["nom"])
                        if "livres_empruntes" in donnees and donnees["livres_empruntes"]:
                            membre.liste_livres_empruntes = donnees["livres_empruntes"].split(",")
                        else:
                            membre.liste_livres_empruntes = []
                        membres[membre.id] = membre

                self.membres = membres
                return membres
        except FileNotFoundError:
            print(f"Le fichier {chemin} n'existe pas.")
            self.membres = {}
            return {}

    def enregistrer_historique(self, id_membre, ISBN, action):
        date = datetime.now().strftime("%Y-%m-%d")
        ligne = f"{date};{ISBN};{id_membre};{action}\n"
        try:
            with open("historiques", "a", encoding="utf-8") as f:
                f.write(ligne)
        except IOError as e:
            print(f"Erreur enregistrement historique : {e}")
>>>>>>> c6d11aa (Premier commit)
