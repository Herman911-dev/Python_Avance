# 🌍 Base de Données des Pays & Visualisation Graphique

Ce projet est une application de bureau complète développée en **Python** utilisant **Tkinter** pour l'interface graphique, **SQLite** pour le stockage local des données, et **Matplotlib** pour la visualisation statistique. L'application permet de récupérer des données démographiques mondiales via une API, de les analyser et de générer un graphique des pays les plus peuplés.

---

## 📑 Sommaire
1. [Fonctionnalités Clés](#-fonctionnalités-clés)
2. [Architecture du Projet](#-architecture-du-projet)
3. [Structure de la Base de Données](#-structure-de-la-base-de-données)
4. [Détail des Modules et Fonctions](#-détail-des-modules-et-fonctions)
5. [Prérequis et Installation](#-prérequis-et-installation)
6. [Guide d'Utilisation Pas à Pas](#-guide-dutilisation-pas-à-pas)
7. [Dépannage et Notes Techniques](#-dépannage-et-notes-techniques)

---

## 🚀 Fonctionnalités Clés

* **Collecte automatisée** : Connexion à une API REST pour récupérer dynamiquement les informations des pays (Nom, Population, Région).
* **Persistance des données** : Stockage local dans une base de données SQLite3 robuste avec gestion des doublons et options d'écrasement/remise à zéro.
* **Calculs statistiques** : Agrégation SQL pour calculer instantanément la population mondiale totale avec un formatage de lecture fluide (séparateurs d'espaces).
* **Visualisation interactive** : Génération d'un diagramme en barres via Matplotlib intégré directement dans la fenêtre Tkinter (Top 10 des nations les plus peuplés).
* **Personnalisation de l'IHM** : Intégration d'un sélecteur de couleurs (`colorchooser`) permettant de modifier dynamiquement la couleur de fond de l'application.

---

## 🏗️ Architecture du Projet

Le projet est entièrement contenu dans le fichier `main.py` et s'articule autour de 5 sections logiques claires :
1. **Gestion de la Base de Données (SQLite3)** : Initialisation et nettoyage.
2. **Téléchargement et Stockage (Requests)** : Requêtes HTTP externes et parsing JSON.
3. **Calculs et Graphiques (Matplotlib & TkAgg)** : Extraction statistique et rendu visuel.
4. **Options de l'IHM** : Personnalisation graphique.
5. **Interface Graphique (Tkinter)** : Organisation des conteneurs (`Frames`), menus et boutons.

---

## 🗄️ Structure de la Base de Données

L'application s'appuie sur une base de données locale nommée `donnees.db`. Lors du premier lancement, la table suivante est créée automatiquement :

### Table : `pays`
| Colonne | Type | Attributs | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identifiant unique du pays |
| `nom` | TEXT | - | Nom commun du pays |
| `population` | INTEGER | - | Nombre d'habitants |
| `region` | TEXT | - | Continent ou région géographique |

---

## 🔍 Détail des Modules et Fonctions

Voici l'explication technique du comportement de chaque fonction du code source :

### 1. Gestion de la BDD
* `initialiser_bdd()` : Se connecte à `donnees.db`, crée la table `pays` si elle n'existe pas, puis ferme proprement la connexion. Elle est appelée dès le démarrage de l'application.
* `effacer_donnees(frame_graphique, label_resultat)` : Demande une confirmation à l'utilisateur (pop-up Yes/No). Si validé, elle vide la table `pays`, efface le texte de calcul de population et détruit tous les widgets enfants du cadre graphique pour réinitialiser complètement l'affichage.

### 2. Flux de Données API
* `telecharger_donnees()` : 
  * Vérifie d'abord si la base contient déjà des données. Si oui, un avertissement propose de les écraser ou d'annuler.
  * Effectue une requête `GET` sur l'API (`https://www.apicountries.com/countries`).
  * Gère de manière sécurisée la structure du JSON reçu (extraction robuste du nom commun ou alternatif via des vérifications de types).
  * Insère en masse les données récupérées à l'aide de requêtes préparées (`INSERT INTO ... VALUES (?, ?, ?)`).
  * Comporte un bloc de capture d'erreurs (`try/except`) pour intercepter les pannes réseau (`requests.exceptions.RequestException`).

### 3. Statistiques & Rendu Visuel
* `afficher_aggregation(label_resultat)` : Exécute une fonction d'agrégation SQL `SUM(population)`. Si le résultat existe, elle formate le nombre avec des espaces comme séparateurs de milliers pour une lisibilité optimale.
* `afficher_graphique(frame)` : 
  * Nettoie le cadre graphique existant pour éviter les superpositions.
  * Récupère le Top 10 via un tri décroissant combiné à une clause de limitation (`ORDER BY population DESC LIMIT 10`).
  * Instancie un objet `Figure` Matplotlib à 100 DPI, configure un diagramme à barres de couleur `skyblue`, incline les étiquettes à 45° pour éviter les chevauchements, et utilise `tight_layout()` pour ajuster les marges.
  * Intègre le composant dans Tkinter via `FigureCanvasTkAgg`.

### 4. Personnalisation & Fenêtre Principale
* `changer_couleur_fond(fenetre)` : Ouvre la boîte de dialogue système de choix de couleur et applique la couleur sélectionnée au fond (`bg`) de l'application.
* `main()` : Configure la fenêtre principale (`900x750`), initialise les menus déroulants (**Base de données** et **Options**), configure l'arborescence des `Frames` principaux et démarre la boucle événementielle `mainloop()`.

---

## 🛠️ Prérequis et Installation

### Prérequis systèmes
* **Python 3.7 ou supérieur**
* Connexion Internet (pour le premier chargement des données).
* *Note Linux (Ubuntu/Debian)* : Assurez-vous d'avoir installé Tkinter sur votre système via la commande : `sudo apt-get install python3-tk`

### Installation pas à pas

1. **Cloner ou télécharger le code**
   ```bash
   git clone [https://github.com/votre-utilisateur/nom-du-repo.git](https://github.com/votre-utilisateur/nom-du-repo.git)
   cd nom-du-repo