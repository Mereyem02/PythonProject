<<<<<<< HEAD

from exception import *
from datetime import datetime

from src.bibliotheques import StatutLivre, Livre, Bibliotheque, Membre

#Fonction de choix
def menu():
    print("\n=== Gestion de Bibliotheques ===")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Lister tous les livres")
    print("6. Afficher les statistiques")
    print("7. Sauvegarder et quitter")

    choix = input("Choisissez une option entre (1-7) : ")
    return choix

#Fonction pour affichage de statistiques
def afficher_statistiques(biblio):
    total_livres = len(biblio.livres)
    livres_empruntes = sum(1 for livre in biblio.livres.values() if livre.statut == StatutLivre.EMPRUNTE)
    membres = len(biblio.membres)
    print(f"\nStatistiques :")
    print(f"Total de livres : {total_livres}")
    print(f"Livres empruntés : {livres_empruntes}")
    print(f"Membres inscrits : {membres}")

#Fonction principale
def main():
    biblio = Bibliotheque()
    biblio.charger_livres()
    biblio.charger_membres()

    while True: #Donne le personne le choix j'ausque le choix de 7 qui permet de quitter la boucle grace a break
        choix = menu()

        if choix == "1":
            print("\n-- Ajouter un livre --")
            isbn = input("ISBN : ").strip()
            titre = input("Titre : ").strip()
            auteur = input("Auteur : ").strip()
            annee = input("Année : ").strip()
            genre = input("Genre : ").strip()
            try:
                annee = int(annee)
                if isbn in biblio.livres:
                    print("Un livre avec cet ISBN existe déjà.")
                else:
                    livre = Livre(isbn, titre, auteur, annee, genre)
                    biblio.ajouter_livre(livre)
                    biblio.sauvegarder_livres()  # Sauvegarde immédiate de livre dans le fichier
                    print("Livre ajouté avec succès.")
            except ValueError:
                print("Année invalide, veuillez saisir un nombre.")

        elif choix == "2":
            print("\n-- Inscrire un membre --")
            id_membre = input("ID membre : ").strip()
            nom = input("Nom : ").strip()
            if id_membre in biblio.membres:
                print("Ce membre existe déjà.")
            else:
                membre = Membre(id_membre, nom)
                biblio.enregistrer_membre(membre)
                biblio.sauvegarder_membres()  # Sauvegarde immédiate
                print("Membre inscrit avec succès.")

        elif choix == "3":
            print("\n-- Emprunter un livre --")
            id_membre = input("ID membre : ").strip()
            isbn = input("ISBN du livre : ").strip()
            try:
                biblio.emprunter_livre(id_membre, isbn)
                biblio.sauvegarder_livres()    # Sauvegarde immédiate
                biblio.sauvegarder_membres()
                print("Emprunt réussi.")
            except Exception as e:
                print(f"Erreur : {e}")

        elif choix == "4":
            print("\n-- Rendre un livre --")
            id_membre = input("ID membre : ").strip()
            isbn = input("ISBN du livre : ").strip()
            try:
                biblio.retourner_livre(id_membre, isbn)
                biblio.sauvegarder_livres()    # Sauvegarde immédiate
                biblio.sauvegarder_membres()
                print("Livre rendu avec succès.")
            except Exception as e:
                print(f"Erreur : {e}")

        elif choix == "5":
            print("\n-- Liste des livres --")
            if not biblio.livres:
                print("Aucun livre dans la bibliothèque.")
            else:
                for livre in biblio.livres.values():
                    print(livre)

        elif choix == "6":
            afficher_statistiques(biblio)

        elif choix == "7":
            biblio.sauvegarder_livres()
            biblio.sauvegarder_membres()
            print("Données sauvegardées. Au revoir !")
            break



        else:
            print("Option invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()

=======

from exception import *
from datetime import datetime

from src.bibliotheques import StatutLivre, Livre, Bibliotheque, Membre


def menu():
    print("\n=== Gestion de Bibliotheques ===")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Lister tous les livres")
    print("6. Afficher les statistiques")
    print("7. Sauvegarder et quitter")

    choix = input("Choisissez une option entre (1-7) : ")
    return choix


def afficher_statistiques(biblio):
    total_livres = len(biblio.livres)
    livres_empruntes = sum(1 for livre in biblio.livres.values() if livre.statut == StatutLivre.EMPRUNTE)
    membres = len(biblio.membres)
    print(f"\nStatistiques :")
    print(f"Total de livres : {total_livres}")
    print(f"Livres empruntés : {livres_empruntes}")
    print(f"Membres inscrits : {membres}")


def main():
    biblio = Bibliotheque()
    biblio.charger_livres()
    biblio.charger_membres()

    while True:
        choix = menu()

        if choix == "1":
            print("\n-- Ajouter un livre --")
            isbn = input("ISBN : ").strip()
            titre = input("Titre : ").strip()
            auteur = input("Auteur : ").strip()
            annee = input("Année : ").strip()
            genre = input("Genre : ").strip()
            try:
                annee = int(annee)
                if isbn in biblio.livres:
                    print("Un livre avec cet ISBN existe déjà.")
                else:
                    livre = Livre(isbn, titre, auteur, annee, genre)
                    biblio.ajouter_livre(livre)
                    biblio.sauvegarder_livres()  # Sauvegarde immédiate de livre dans le fichier
                    print("Livre ajouté avec succès.")
            except ValueError:
                print("Année invalide, veuillez saisir un nombre.")

        elif choix == "2":
            print("\n-- Inscrire un membre --")
            id_membre = input("ID membre : ").strip()
            nom = input("Nom : ").strip()
            if id_membre in biblio.membres:
                print("Ce membre existe déjà.")
            else:
                membre = Membre(id_membre, nom)
                biblio.enregistrer_membre(membre)
                biblio.sauvegarder_membres()  # Sauvegarde immédiate
                print("Membre inscrit avec succès.")

        elif choix == "3":
            print("\n-- Emprunter un livre --")
            id_membre = input("ID membre : ").strip()
            isbn = input("ISBN du livre : ").strip()
            try:
                biblio.emprunter_livre(id_membre, isbn)
                biblio.sauvegarder_livres()    # Sauvegarde immédiate
                biblio.sauvegarder_membres()
                print("Emprunt réussi.")
            except Exception as e:
                print(f"Erreur : {e}")

        elif choix == "4":
            print("\n-- Rendre un livre --")
            id_membre = input("ID membre : ").strip()
            isbn = input("ISBN du livre : ").strip()
            try:
                biblio.retourner_livre(id_membre, isbn)
                biblio.sauvegarder_livres()    # Sauvegarde immédiate
                biblio.sauvegarder_membres()
                print("Livre rendu avec succès.")
            except Exception as e:
                print(f"Erreur : {e}")

        elif choix == "5":
            print("\n-- Liste des livres --")
            if not biblio.livres:
                print("Aucun livre dans la bibliothèque.")
            else:
                for livre in biblio.livres.values():
                    print(livre)

        elif choix == "6":
            afficher_statistiques(biblio)

        elif choix == "7":
            biblio.sauvegarder_livres()
            biblio.sauvegarder_membres()
            print("Données sauvegardées. Au revoir !")
            break



        else:
            print("Option invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()

>>>>>>> c6d11aa (Premier commit)
