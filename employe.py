
# employe.py
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import sqlite3

from database import Database
from utils import *

class Employe:
    def __init__(self, root, nom):
        self.nom = nom
        self.root_parent = root
        self.root = Toplevel(root)
        self.db = Database()
        
        self.root.title("ESPACE EMPLOYE")
        self.root.geometry("900x600")
        self.root.configure(bg=BLEU)
        self.root.iconbitmap(chemin_logo)
    
        # Titre
        Label(self.root, text=f"👤 Bienvenue {nom}", font=("Times New Roman", 20, "bold"),
              bg=BLEU, fg=BLANC).pack(pady=30)
        
        # Boutons
        ctk.CTkButton(self.root, text="📋 Voir mes tâches", fg_color=ORANGE, 
                      width=200, command=self.tasks).pack(pady=10)
        
        ctk.CTkButton(self.root, text="⚠️ Déclarer un problème", fg_color=ORANGE, 
                      width=200, command=self.declarer_probleme).pack(pady=10)
        
        ctk.CTkButton(self.root, text="🚪 Déconnexion", fg_color="red", 
                      width=200, command=self.logout).pack(pady=20)
        
        # Gérer la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        
        logger(self.db, nom, "ACCES_EMPLOYE", "Ouverture de l'interface employé")

    def tasks(self):
        """Afficher les tâches de l'employé"""
        w = Toplevel(self.root)
        w.title("Mes Tâches")
        w.iconbitmap(chemin_logo)
        w.geometry("900x600")
        w.configure(bg=BLEU)
        
        ctk.CTkLabel(w, text="📋 Mes Tâches", font=("Times New Roman", 16, "bold"),
                     text_color=BLANC).pack(pady=10)
        
        conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
        cur = conn.cursor()
        
        # Recherche par nom d'employé 
        cur.execute("""
            SELECT titre, statut, date_debut, date_fin 
            FROM taches 
            WHERE id_emp IN (SELECT id_emp FROM employes WHERE nom=?)
        """, (self.nom,))
        
        t = cur.fetchall()
        conn.close()
        
        if not t:
            ctk.CTkLabel(w, text="Aucune tâche assignée", text_color=BLANC).pack(pady=20)
        else:
            # Frame scrollable pour les tâches
            tasks_frame = ctk.CTkScrollableFrame(w, width=650, height=350, fg_color=BLANC)
            tasks_frame.pack(pady=10)
            
            for i, x in enumerate(t):
                titre, statut, date_debut, date_fin = x
                couleur_statut = "green" if statut == "Terminé" else "orange" if statut == "En cours" else "red"
                
                ctk.CTkLabel(tasks_frame, 
                            text=f"📌 {titre} | 📊 {statut} | 📅 {date_debut} → {date_fin}", 
                            text_color=BLEU, anchor="w").pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def declarer_probleme(self):
        """Déclarer un problème"""
        w = Toplevel(self.root)
        w.title("Déclarer un Problème")
        w.iconbitmap(chemin_logo)
        w.geometry("900x600")
        w.configure(bg=BLEU)
        
        ctk.CTkLabel(w, text="Description du problème", text_color=BLANC).pack(pady=10)
        desc = ctk.CTkTextbox(w, width=400, height=150)
        desc.pack(pady=10)
        
        def save():
            description = desc.get("1.0", "end").strip()
            if not description:
                messagebox.showerror("Erreur", "La description est obligatoire")
                return
            
            try:
                conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO problemes (id_dept, description, statut) VALUES (?,?,?)", 
                            (1, description, "Ouvert"))  # ID dept par défaut = 1
                conn.commit()
                conn.close()
                logger(self.db, self.nom, "DECLARATION_PROBLEME", description[:50])
                messagebox.showinfo("OK", "Problème déclaré avec succès")
                w.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        ctk.CTkButton(w, text="Valider", command=save, fg_color=ORANGE).pack(pady=10)

    def logout(self):
        """Déconnexion"""
        logger(self.db, self.nom, "DECONNEXION", "Fin de session employé")
        self.root.destroy()
        self.root_parent.deiconify()  # Réafficher la fenêtre de login (fenette de connexion)

