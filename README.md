# PythonProject
#  Application de Gestion de Bibliothèque avec Tkinter

##  Réalisé par :
**Mereyem Elhaouzi**  
Étudiante en 3ᵉ année Génie Informatique  
ENSAO – École Nationale des Sciences Appliquées d’Oujda

## 🛠️ Guide d'installation

### ✅ Prérequis :
- Python 3.10 ou supérieur
- Les bibliothèques suivantes :
  - `tkinter`
  - `matplotlib`

### 📦 Installation des dépendances :
pip install matplotlib
#Tkinter est deja inclus dans la version de python

📁 Structure du projet :

PythonProject/
│
├── .venv/                            # Environnement virtuel Python
│
├── assets/                           # Ressources multimédia (présentation et graphiques)
│   ├── presentation.mp4
│   ├── stats_Auteurs.png
│   └── Stats_genre.png
│
├── docs/                             # Documents (rapports, livrables)
│   └── Rapport_de_projetpython.pdf
│
├── src/                              # Code source du projet
│   ├── bibliotheques.py              # Classe Livre, Membre, Bibliothèque
│   ├── exception.py                  # Exceptions personnalisées
│   ├── visualisations.py             # Fonctions matplotlib
│   ├── main.py                       # Lancement de l'application graphique
│   ├── mainlignecommNDE.py           # Lancement de l'execution en ligne de commande
│   ├── historiques                   # Fichier texte (log emprunts/retours)
│   ├── livres                        # Fichier texte (base de données des livres)
│   └── membres                       # Fichier texte (base de données des membres)
│
└── README.md                         # Documentation du projet (à créer)


▶️ Exécution de l'application
Pour lancer l'application :

python mainlignecommNDE.py

✨ Fonctionnalités principales:

📖 Gestion des livres : ajout, suppression, affichage

👤 Gestion des membres : inscription, suppression

📚 Emprunt et retour de livres

📊 Statistiques interactives :

Diagramme par genre

Top auteurs

Évolution des emprunts sur 30 jours

💾 Sauvegarde automatique dans des fichiers .txt

📅 Historique des emprunts et retours

📌 Exemple d'utilisation

Ajouter un livre :
Remplir le formulaire (ISBN, Titre, Auteur, Année, Genre)

Choisir le statut (Disponible/Emprunté)

Cliquer sur Ajouter

Emprunter un livre :

Entrer l'ID du membre et l'ISBN du livre

Cliquer sur Valider l'emprunt

📝 Exemple d’enregistrement dans le fichier historiques:

2025-06-25;9781234567890;M001;EMPRUNT
2025-06-26;9781234567890;M001;RETOUR
