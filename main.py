import tkinter as tk
from tkinter import messagebox, colorchooser
import requests
import sqlite3

# Nouveaux imports pour le graphique
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- 1. GESTION DE LA BASE DE DONNÉES ---

def initialiser_bdd():
    conn = sqlite3.connect("donnees.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            population INTEGER,
            region TEXT
        )
    ''')
    conn.commit()
    conn.close()

def effacer_donnees(frame_graphique, label_resultat):
    reponse = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir effacer toutes les données ?")
    if reponse:
        conn = sqlite3.connect("donnees.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pays")
        conn.commit()
        conn.close()
        
        # On efface aussi l'écran
        label_resultat.config(text="")
        for widget in frame_graphique.winfo_children():
            widget.destroy()
            
        messagebox.showinfo("Succès", "La base de données a été vidée.")

# --- 2. TÉLÉCHARGEMENT ET STOCKAGE ---

def telecharger_donnees():
    conn = sqlite3.connect("donnees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pays")
    nb_lignes = cursor.fetchone()[0]
    
    if nb_lignes > 0:
        reponse = messagebox.askyesno(
            "Base non vide", 
            f"La base contient déjà {nb_lignes} pays. Voulez-vous les écraser ?"
        )
        if not reponse:
            conn.close()
            return 
        else:
            cursor.execute("DELETE FROM pays")
            conn.commit()

    url = "https://www.apicountries.com/countries"
    
    try:
        reponse_web = requests.get(url)
        reponse_web.raise_for_status() 
        donnees = reponse_web.json()
        
        if isinstance(donnees, dict):
            messagebox.showerror("Erreur API", "L'API a renvoyé une erreur inattendue.")
            conn.close()
            return 
        
        for pays in donnees:
            nom_data = pays.get('name', 'Inconnu')
            nom = nom_data.get('common', 'Inconnu') if isinstance(nom_data, dict) else nom_data
            population = pays.get('population', 0)
            region = pays.get('region', 'Inconnue')
            
            cursor.execute("INSERT INTO pays (nom, population, region) VALUES (?, ?, ?)", (nom, population, region))
            
        conn.commit()
        messagebox.showinfo("Succès", f"{len(donnees)} pays sauvegardés !")
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur de connexion", f"Impossible de télécharger :\n{e}")
    finally:
        conn.close()

# --- 3. CALCULS ET GRAPHIQUES ---

def afficher_aggregation(label_resultat):
    conn = sqlite3.connect("donnees.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(population) FROM pays")
        total = cursor.fetchone()[0]
        if total:
            label_resultat.config(text=f"Population totale : {total:,} d'habitants".replace(',', ' '))
        else:
            label_resultat.config(text="La base de données est vide.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur SQL", f"Impossible de calculer : {e}")
    finally:
        conn.close()

def afficher_graphique(frame):
    """Génère un graphique des 10 pays les plus peuplés et l'intègre dans la fenêtre."""
    # Nettoyer l'ancien graphique s'il y en a un
    for widget in frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("donnees.db")
    cursor = conn.cursor()
    
    try:
        # On récupère les 10 pays avec la plus grande population
        cursor.execute("SELECT nom, population FROM pays ORDER BY population DESC LIMIT 10")
        resultats = cursor.fetchall()
        
        if not resultats:
            messagebox.showwarning("Base vide", "Aucune donnée à afficher. Téléchargez d'abord les données.")
            return

        # Séparation des données pour le graphique (x = noms, y = populations)
        noms = [ligne[0] for ligne in resultats]
        populations = [ligne[1] for ligne in resultats]

        # Création de la figure Matplotlib
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111) # Ajout d'un système d'axes
        ax.bar(noms, populations, color='skyblue')
        
        # Mise en forme du graphique
        ax.set_title("Top 10 des pays les plus peuplés")
        ax.set_ylabel("Population")
        ax.tick_params(axis='x', rotation=45) # Incliner les noms pour la lisibilité
        fig.tight_layout() # Ajuster les marges pour que le texte ne soit pas coupé

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except sqlite3.Error as e:
        messagebox.showerror("Erreur SQL", f"Erreur lors de la récupération : {e}")
    finally:
        conn.close()

# --- 4. OPTIONS ---

def changer_couleur_fond(fenetre):
    couleur = colorchooser.askcolor(title="Choisir une couleur")
    if couleur[1]: 
        fenetre.config(bg=couleur[1])

# --- 5. INTERFACE GRAPHIQUE ---

def main():
    initialiser_bdd() 
    
    root = tk.Tk()
    root.title("Mon Application Python Avancé")
    root.geometry("900x750") # Fenêtre un peu plus grande pour le graphique

    # --- Cadres (Frames) pour organiser la fenêtre ---
    frame_haut = tk.Frame(root)
    frame_haut.pack(pady=10)
    
    frame_graphique = tk.Frame(root) # Ce cadre accueillera le dessin
    frame_graphique.pack(pady=10, fill=tk.BOTH, expand=True)

    # --- Menus ---
    barre_menu = tk.Menu(root)
    menu_bdd = tk.Menu(barre_menu, tearoff=0)
    menu_bdd.add_command(label="Obtenir des données sur Internet", command=telecharger_donnees)
    menu_bdd.add_command(label="Effacer le contenu", command=lambda: effacer_donnees(frame_graphique, label_resultat_agg))
    barre_menu.add_cascade(label="Base de données", menu=menu_bdd)

    menu_options = tk.Menu(barre_menu, tearoff=0)
    menu_options.add_command(label="Couleur de fond", command=lambda: changer_couleur_fond(root))
    barre_menu.add_cascade(label="Options", menu=menu_options)
    root.config(menu=barre_menu)

    # --- Éléments visuels ---
    tk.Label(frame_haut, text="Base de données des Pays", font=("Arial", 16, "bold")).pack(pady=10)

    label_resultat_agg = tk.Label(frame_haut, text="", font=("Arial", 14, "italic"))
    
    # Boutons placés côte à côte
    frame_boutons = tk.Frame(frame_haut)
    frame_boutons.pack(pady=5)
    
    btn_agg = tk.Button(frame_boutons, text="Calculer population mondiale", 
                        command=lambda: afficher_aggregation(label_resultat_agg), bg="lightgreen")
    btn_agg.pack(side=tk.LEFT, padx=10)
    
    btn_graph = tk.Button(frame_boutons, text="Afficher le graphique (Top 10)", 
                          command=lambda: afficher_graphique(frame_graphique), bg="lightpink")
    btn_graph.pack(side=tk.LEFT, padx=10)

    label_resultat_agg.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()