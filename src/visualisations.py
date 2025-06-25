<<<<<<< HEAD
import matplotlib.pyplot as plt
from collections import Counter
import csv
from datetime import datetime, timedelta

# 1. Diagramme circulaire - % des livres par genre
def diagramme_genre(livres: dict):
    genres = [livre.genre for livre in livres.values()]
    compteur = Counter(genres)
    if not compteur:
        print("Pas de données pour afficher le graphique.")
        return None
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(compteur.values(), labels=compteur.keys(), autopct='%1.1f%%', startangle=140)
    ax.set_title("Répartition des Livres par Genre")
    fig.tight_layout()
    plt.savefig("Stats_genre.png")
    return fig

# 2. Histogramme - Top 10 des auteurs les plus populaires
def histogramme_auteurs(livres: dict):
    auteurs = [livre.auteur for livre in livres.values()]
    compteur = Counter(auteurs).most_common(10)
    if not compteur:
        print("Pas de données pour afficher le graphique !")
        return None
    noms, quantiter = zip(*compteur)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(noms, quantiter, color='pink')
    ax.set_title("Top 10 Auteurs les Plus Populaires")
    ax.set_ylabel("Nombre de Livres")

    # Fixer les positions des ticks
    ax.set_xticks(range(len(noms)))
    # Fixer les labels des ticks
    ax.set_xticklabels(noms, rotation=45, ha="right")
    plt.savefig("stats_Auteurs",dpi=300)
    fig.tight_layout()
    return fig

# 3. Courbe temporelle - Emprunts sur les 30 derniers jours
def courbe_emprunts(chemin="historiques"):
    jours = [datetime.today() - timedelta(days=i) for i in range(29, -1, -1)]
    datesL = [j.strftime("%Y-%m-%d") for j in jours]
    emprunts_par_jour = {d: 0 for d in datesL}
    try:
        with open(chemin, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) == 4:
                    dateL, _, _, action = row
                    if action.strip().upper() == "EMPRUNT" and dateL in emprunts_par_jour:
                        emprunts_par_jour[dateL] += 1
        fig, ax = plt.subplots(figsize=(10, 5))
        dates = list(emprunts_par_jour.keys())
        valeurs = list(emprunts_par_jour.values())
        ax.plot(dates, valeurs, marker='o')
        ax.set_title("Emprunts - 30 Derniers Jours")

        # Fixer les positions des ticks
        ax.set_xticks(range(len(dates)))
        # Fixer les labels des ticks
        ax.set_xticklabels(dates, rotation=45, ha="right")

        ax.set_ylabel("Nombre")
        fig.tight_layout()
        return fig
    except FileNotFoundError:
        print("Aucun historique trouvé.")
        return None


=======
import matplotlib.pyplot as plt
from collections import Counter
import csv
from datetime import datetime, timedelta

# 1. Diagramme circulaire - % des livres par genre
def diagramme_genre(livres: dict):
    genres = [livre.genre for livre in livres.values()]
    compteur = Counter(genres)
    if not compteur:
        print("Pas de données pour afficher le graphique.")
        return None
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(compteur.values(), labels=compteur.keys(), autopct='%1.1f%%', startangle=140)
    ax.set_title("Répartition des Livres par Genre")
    fig.tight_layout()
    plt.savefig("Stats_genre.png")
    return fig

# 2. Histogramme - Top 10 des auteurs les plus populaires
def histogramme_auteurs(livres: dict):
    auteurs = [livre.auteur for livre in livres.values()]
    compteur = Counter(auteurs).most_common(10)
    if not compteur:
        print("Pas de données pour afficher le graphique !")
        return None
    noms, quantiter = zip(*compteur)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(noms, quantiter, color='pink')
    ax.set_title("Top 10 Auteurs les Plus Populaires")
    ax.set_ylabel("Nombre de Livres")

    # Fixer les positions des ticks
    ax.set_xticks(range(len(noms)))
    # Fixer les labels des ticks
    ax.set_xticklabels(noms, rotation=45, ha="right")
    plt.savefig("stats_Auteurs",dpi=300)
    fig.tight_layout()
    return fig

# 3. Courbe temporelle - Emprunts sur les 30 derniers jours
def courbe_emprunts(chemin="historiques"):
    jours = [datetime.today() - timedelta(days=i) for i in range(29, -1, -1)]
    datesL = [j.strftime("%Y-%m-%d") for j in jours]
    emprunts_par_jour = {d: 0 for d in datesL}
    try:
        with open(chemin, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) == 4:
                    dateL, _, _, action = row
                    if action.strip().upper() == "EMPRUNT" and dateL in emprunts_par_jour:
                        emprunts_par_jour[dateL] += 1
        fig, ax = plt.subplots(figsize=(10, 5))
        dates = list(emprunts_par_jour.keys())
        valeurs = list(emprunts_par_jour.values())
        ax.plot(dates, valeurs, marker='o')
        ax.set_title("Emprunts - 30 Derniers Jours")

        # Fixer les positions des ticks
        ax.set_xticks(range(len(dates)))
        # Fixer les labels des ticks
        ax.set_xticklabels(dates, rotation=45, ha="right")

        ax.set_ylabel("Nombre")
        fig.tight_layout()
        return fig
    except FileNotFoundError:
        print("Aucun historique trouvé.")
        return None


>>>>>>> c6d11aa (Premier commit)
