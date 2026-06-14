
# admin.py
from tkinter import  *
import customtkinter as ctk
from tkinter import messagebox
import sqlite3

from database import Database
from utils import *

class Admin:
    def __init__(self, root):
        self.root_parent = root
        self.root = Toplevel(root)
        self.db = Database()

        self.db.set_callback(self.actualiser_dashboard)
        self.root.title("ADMIN ATLAS")
        self.root.geometry("1600x800")
        self.root.configure(bg=BLEU)
        self.root.iconbitmap(chemin_logo)

        
        # Frame principale 
        main_frame = ctk.CTkFrame(self.root, fg_color=BLEU)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
        # === COLONNE GAUCHE : Menu des boutons ===
        left_frame = ctk.CTkFrame(main_frame, fg_color=BLEU, width=250, )
        left_frame.pack(side="left", fill="y", padx=(0, 20))
         

           # === COLONNE DROITE : Dashboard ===
        right_frame = ctk.CTkFrame(main_frame, fg_color=BLEU)
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)
        
        # Titre
        ctk.CTkLabel(left_frame, text="Espace\nAdministrateur", 
                    font=("Times New Roman", 20, "bold"),
                    text_color=BLANC, justify="center").pack(pady=20)
    
            # Boutons du menu
        ctk.CTkButton(left_frame, text="👥 Ajouter Employé", width=230, height=40,
                    fg_color=ORANGE, hover_color="#e66e00",
                    command=self.add_emp).pack(pady=8)
    
        ctk.CTkButton(left_frame, text="🔍 Rechercher Employé", width=230, height=40,
                    fg_color=ORANGE, hover_color="#e66e00",
                    command=self.rechercher_employes).pack(pady=8)
    
        ctk.CTkButton(left_frame, text="🏢 Ajouter Département", width=230, height=40,
                    fg_color=ORANGE, hover_color="#e66e00",
                    command=self.add_dept).pack(pady=8)
        
        ctk.CTkButton(left_frame, text="📋 Créer Tâche", width=230, height=40,
                    fg_color=ORANGE, hover_color="#e66e00",
                    command=self.add_task).pack(pady=8)
        
        ctk.CTkButton(left_frame, text="⚠️ Déclarer Problème", width=230, height=40,
                    fg_color=ORANGE, hover_color="#e66e00",
                    command=self.add_prob).pack(pady=8)
        
        ctk.CTkButton(left_frame, text="🔑 Ajouter Administrateur", width=230, height=40,
                  fg_color=ORANGE, hover_color="#e66e00",
                  command=self.add_admin).pack(pady=8)
        
    
        ctk.CTkButton(left_frame, text="👤 Ajouter Utilisateur", width=230, height=40,
                  fg_color=ORANGE, hover_color="#e66e00",
                  command=self.add_user).pack(pady=8)
    
        ctk.CTkButton(left_frame, text="📊 Voir les Logs", width=230, height=40,
                    fg_color=BLEU, hover_color="#1a3d5c",
                    command=self.view_logs).pack(pady=8)
        
        ctk.CTkButton(left_frame, text="🚪Déconnexion", width=230, height=40,
                    fg_color="red", hover_color="#cc0000",
                    command=self.logout).pack(pady=20)
        
         
        # Titre du dashboard
        ctk.CTkLabel(right_frame, text="Tableau de Bord", 
                    font=("Times New Roman", 24, "bold"),
                 text_color=BLANC).pack(pady=10)
    
        # Afficher le dashboard
        self.afficher_dashboard(right_frame)
        # Vérifier les notifications
        self.verifier_notifications()
            
        # Gérer la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
            
        logger(self.db, "Admin", "ACCES_ADMIN", "Ouverture de l'interface admin")

    def add_emp(self):
        """Ajouter un employé"""
        w = Toplevel(self.root)
        w.title("Ajouter Employé")
        w.geometry("900x600")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)

        ctk.CTkLabel(w, text="Nom employé", text_color=BLANC).pack(pady=5)
        emp = ctk.CTkEntry(w, width=300)
        emp.pack(pady=5)
        
        ctk.CTkLabel(w, text="Poste", text_color=BLANC).pack(pady=5)
        poste = ctk.CTkEntry(w, width=300)
        poste.pack(pady=5)
        
        ctk.CTkLabel(w, text="Département", text_color=BLANC).pack(pady=5)
        conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
        cur = conn.cursor()
        cur.execute("SELECT id_dept, nom_dept FROM departements WHERE nom_dept IS NOT NULL AND nom_dept != ''ORDER BY nom_dept ASC""")
        dept = cur.fetchall()
        conn.close()
        if not dept:
            messagebox.showwarning("Attention", "Aucun département disponible.\nVeuillez d'abord créer un département.", parent=w)
            w.destroy()
            return
     
        dept_names = [nom for id_, nom in dept]
    
    # Variable pour stocker le choix
        selected_dept = ctk.StringVar(value="")
    
    # Menu déroulant
        dept_menu = ctk.CTkOptionMenu(w, values=dept_names, variable=selected_dept, 
                                      width=300,fg_color="#f0f0f0",
                                      text_color= "#000000",
                                      button_color= "#ffffff",button_hover_color=ORANGE)
        dept_menu.pack(pady=5)

        ctk.CTkLabel(w, text="Salaire", text_color=BLANC).pack(pady=5)
        salaire = ctk.CTkEntry(w, width=300)
        salaire.pack(pady=5)
        
        ctk.CTkLabel(w, text="Téléphone", text_color=BLANC).pack(pady=5)
        tel = ctk.CTkEntry(w, width=300)
        tel.pack(pady=5)
            
        def save():
            if not all([emp.get(), poste.get(), salaire.get(), tel.get()]):
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis !")
                return
            
            selected_text = selected_dept.get()
            conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
            cur = conn.cursor()
            cur.execute("SELECT id_dept FROM departements WHERE nom_dept = ?",(selected_text,))
            result = cur.fetchone()
            conn.close()
            if not result:
                messagebox.showerror("Erreur", "Veuillez sélectionner un département")
                return
        
            id_dept = result[0]
            
            try:
                float(salaire.get())
            except ValueError:
                messagebox.showerror("Erreur", "Le salaire doit être un nombre !")
                return

            if not valider_telephone(tel.get()):
                messagebox.showerror("Erreur", "Le téléphone doit contenir 10 chiffres !")
                return

            try:
                conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO employes VALUES (NULL, ?, ?, ?, ?, ?)", 
                            (emp.get(), poste.get(), id_dept, salaire.get(), tel.get()))
                conn.commit()
                conn.close()
                logger(self.db, "Admin", "AJOUT_EMPLOYE", f"Nom: {emp.get()}, Dept ID: {id_dept}")
                messagebox.showinfo("OK", "Employé ajouté")
                w.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        ctk.CTkButton(w, text="Enregistrer", command=save, fg_color=ORANGE).pack(pady=20)

       
    def add_dept(self):
        """Ajouter un département"""
        w = Toplevel(self.root)
        w.title("Ajouter Département")
        w.geometry("900x600")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)

        ctk.CTkLabel(w, text="Nom du département", text_color=BLANC).pack(pady=15)
        nom_dept = ctk.CTkEntry(w, width=300, placeholder_text="Ex: Ressources Humaines")
        nom_dept.pack(pady=10)

        def save():
            nom = nom_dept.get().strip()  
        
            if not nom:
                messagebox.showerror("Erreur", "Le nom est obligatoire")
                return
        
            try:
                conn = sqlite3.connect(chemin_db)
                cur = conn.cursor()
                nom=nom_dept.get()
                cur.execute("INSERT INTO departements (nom_dept) VALUES (?)", (nom,))  
                conn.commit()
                conn.close()
            
                messagebox.showinfo("OK", "Département ajouté", parent=w)
                w.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e), parent=w)

        ctk.CTkButton(w, text="Enregistrer", command=save, fg_color=ORANGE).pack(pady=20)
                              
    def add_task(self):
        """Créer une tâche"""
        w = Toplevel(self.root)
        w.title("Créer Tâche")
        w.geometry("900x600")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)
        
        ctk.CTkLabel(w, text="Nom Employé", text_color=BLANC).pack(pady=5)
        emp = ctk.CTkEntry(w, width=300)
        emp.pack(pady=5)

        ctk.CTkLabel(w, text="Titre tâche", text_color=BLANC).pack(pady=5)
        t = ctk.CTkEntry(w, width=300)
        t.pack(pady=5)
        
        ctk.CTkLabel(w, text="Date début (DD-MM-YYYY)", text_color=BLANC).pack(pady=5)
        dd = ctk.CTkEntry(w, width=300)
        dd.pack(pady=5)
        
        ctk.CTkLabel(w, text="Date fin (DD-MM-YYYY)", text_color=BLANC).pack(pady=5)
        df = ctk.CTkEntry(w, width=300)
        df.pack(pady=5)

        def save():
            if not all([emp.get(), t.get(), dd.get(), df.get()]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                return

            try:
                conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO taches (nom, titre, statut, date_debut, date_fin) VALUES (?,?,?,?,?)", 
                            (emp.get(), t.get(), "A faire", dd.get(), df.get()))
                conn.commit()
                conn.close()
                logger(self.db, "Admin", "CREATION_TACHE", f"Titre: {t.get()}")
                messagebox.showinfo("OK", "Tâche créée")
                w.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ctk.CTkButton(w, text="Créer", command=save, fg_color=ORANGE).pack(pady=20)

    def add_prob(self):
        """Déclarer un problème"""
        w = Toplevel(self.root)
        w.title("Déclarer Problème")
        w.geometry("900x600")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)

        ctk.CTkLabel(w, text="Nom Département", text_color=BLANC).pack(pady=5)
        nd = ctk.CTkEntry(w, width=300)
        nd.pack(pady=5)

        ctk.CTkLabel(w, text="Description", text_color=BLANC).pack(pady=5)
        desc = ctk.CTkEntry(w, width=300)
        desc.pack(pady=5)

        def save():
            if not nd.get() or not desc.get():
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
                return
            try:
                conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO problemes ( nom_dept, description, statut) VALUES (?,?,?)", 
                            (nd.get(), desc.get(), "Ouvert"))
                conn.commit()
                conn.close()
                logger(self.db, "Admin", "DECLARATION_PROBLEME", f"Dept: {nd.get()}")
                messagebox.showinfo("OK", "Problème enregistré")
                w.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        ctk.CTkButton(w, text="Valider", command=save, fg_color=ORANGE).pack(pady=20)

    def add_user(self):
        """Ajouter un utilisateur"""
        w = Toplevel(self.root)
        w.geometry("900x600")
        w.title("Ajouter Utilisateur")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)

        ctk.CTkLabel(w, text="Nom d'utilisateur", text_color=BLANC).pack(pady=5)
        us = ctk.CTkEntry(w, width=300)
        us.pack(pady=5)

        ctk.CTkLabel(w, text="Mot de passe", text_color=BLANC).pack(pady=5)
        pw = ctk.CTkEntry(w, show="*", width=300)
        pw.pack(pady=5)
        
        ctk.CTkLabel(w, text="Confirmer mot de passe", text_color=BLANC).pack(pady=5)
        pw_confirm = ctk.CTkEntry(w, show="*", width=300)
        pw_confirm.pack(pady=5)

        ctk.CTkLabel(w, text="Rôle (Admin / PDG / DRH / Manager)", text_color=BLANC).pack(pady=5)
        r = ctk.CTkEntry(w, width=300)
        r.pack(pady=5)

        def save():
            username = us.get().strip()
            password = pw.get().strip()
            password_confirm = pw_confirm.get().strip()
            role = r.get().strip()
            
            if not all([username, password, role]):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return
            
            if password != password_confirm:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                return
            
            # Validation de la force du mot de passe
            from utils import valider_mot_de_passe
            is_valid, message = valider_mot_de_passe(password)
            if not is_valid:
                messagebox.showerror("Erreur", message)
                return

            conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
            cur = conn.cursor()
            cur.execute("SELECT username FROM users WHERE username = ?", (username,))
            result = cur.fetchone()
            if result:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà")
                conn.close()
                return
           
            cur.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", 
                        (username, password, role))
            conn.commit()  
            conn.close()
            logger(self.db, "Admin", "AJOUT_UTILISATEUR", f"Username: {username}")
            messagebox.showinfo("OK", "Utilisateur créé")
            w.destroy()

        ctk.CTkButton(w, text="Enregistrer", command=save, fg_color=ORANGE).pack(pady=20)

    def add_admin(self):
        """Ajouter un administrateur"""
        w = Toplevel(self.root)
        w.geometry("900x600")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)
        w.title("Ajouter Administrateur")

        ctk.CTkLabel(w, text="Nom Administrateur", text_color=BLANC).pack(pady=5)
        us = ctk.CTkEntry(w, width=300)
        us.pack(pady=5)

        ctk.CTkLabel(w, text="Mot de passe", text_color=BLANC).pack(pady=5)
        pw = ctk.CTkEntry(w, show="*", width=300)
        pw.pack(pady=5)
        
        ctk.CTkLabel(w, text="Confirmer mot de passe", text_color=BLANC).pack(pady=5)
        pw_confirm = ctk.CTkEntry(w, show="*", width=300)
        pw_confirm.pack(pady=5)

        ctk.CTkLabel(w, text="Rôle (PDG / DRH / Manager)", text_color=BLANC).pack(pady=5)
        r = ctk.CTkEntry(w, width=300)
        r.pack(pady=5)

        def save():
            nom = us.get().strip()
            mot_de_passe = pw.get().strip()
            mot_de_passe_confirm = pw_confirm.get().strip()
            role = r.get().strip()
            
            if not all([nom, mot_de_passe, role]):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return
            
            if mot_de_passe != mot_de_passe_confirm:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                return
            
            # Validation de la force du mot de passe
            from utils import valider_mot_de_passe
            is_valid, message = valider_mot_de_passe(mot_de_passe)
            if not is_valid:
                messagebox.showerror("Erreur", message)
                return
            
            conn = sqlite3.connect("D:/Atlas_Bâtiment/Atlas.db")
            cur = conn.cursor()
            cur.execute("SELECT nom FROM admins WHERE nom = ?", (nom,))
            result = cur.fetchone()
            if result:
                messagebox.showerror("Erreur", "Ce nom d'administrateur existe déjà")
                conn.close()
                return
            
           
            cur.execute("INSERT INTO admins (nom, mot_de_passe, role) VALUES (?,?,?)", 
                        (nom, mot_de_passe, role))
            conn.commit()  
            conn.close()
            logger(self.db, "Admin", "AJOUT_ADMIN", f"Nom: {nom}")
            messagebox.showinfo("OK", "Administrateur ajouté avec succès")
            w.destroy()

        ctk.CTkButton(w, text="Enregistrer", command=save, fg_color=ORANGE).pack(pady=20)

    def view_logs(self):
        """Afficher les logs d'activité"""
        w = Toplevel(self.root)
        w.title("Journal d'Activité")
        w.geometry("900x600")
        w.iconbitmap(chemin_logo)
        w.configure(bg=BLEU)
        
        ctk.CTkLabel(w, text="📋 Journal d'Activité", font=("Times New Roman", 16, "bold"),
                     text_color=BLANC).pack(pady=10)
        
        # Frame pour les logs avec scrollbar
        logs_frame = ctk.CTkScrollableFrame(w, width=650, height=350, fg_color=BLANC)
        logs_frame.pack(pady=10)
        
        logs = self.db.get_logs(50)
        if not logs:
            ctk.CTkLabel(logs_frame, text="Aucun log enregistré", text_color=BLEU).pack(pady=20)
        else:
            for log in logs:
                utilisateur, action, date_heure, details = log
                log_text = f"[{date_heure}] {utilisateur} - {action}"
                if details:
                    log_text += f" ({details})"
                ctk.CTkLabel(logs_frame, text=log_text, text_color=BLEU, 
                             anchor="w", justify="left").pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def logout(self):
        """Déconnexion"""
        logger(self.db, "Admin", "DECONNEXION", "Fin de session admin")
        self.root.destroy()
        self.root_parent.deiconify()

    def afficher_dashboard(self, parent):
        """Affiche les statistiques principales"""
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()

        # Nombre d'employés
        cur.execute("SELECT COUNT(*) FROM employes")
        nb_employes = cur.fetchone()[0]
        
        # Nombre de tâches à faire
        cur.execute("SELECT COUNT(*) FROM taches WHERE statut = 'A faire'")
        nb_taches_a_faire = cur.fetchone()[0]
    
        # Nombre de problèmes ouverts
        cur.execute("SELECT COUNT(*) FROM problemes WHERE statut = 'Ouvert'")
        nb_problemes_ouverts = cur.fetchone()[0]
        
        # Nombre de départements
        cur.execute("SELECT COUNT(*) FROM departements")
        nb_departements = cur.fetchone()[0]
        
        # Nombre de tâches en cours
        cur.execute("SELECT COUNT(*) FROM taches WHERE statut = 'En cours'")
        nb_taches_en_cours = cur.fetchone()[0]
        
        # Nombre total de tâches
        cur.execute("SELECT COUNT(*) FROM taches")
        nb_taches_total = cur.fetchone()[0]

        # Nombre d'administrateurs
        cur.execute("SELECT COUNT(*) FROM admins")
        nb_admins = cur.fetchone()[0]
        
        # Nombre d'utilisateurs
        cur.execute("SELECT COUNT(*) FROM users")
        nb_users = cur.fetchone()[0]
        
        conn.close()

        # Création du frame de statistiques
        stats_frame = ctk.CTkFrame(parent, fg_color=BLEU)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Frame pour les cartes
        row1 = ctk.CTkFrame(stats_frame, fg_color=BLEU)
        row1.pack(fill="x", pady=10)

        # Carte 1 : Employés
        card1 = ctk.CTkFrame(row1, fg_color="#1a5f7a", width=200, height=120)
        card1.pack(side="left", padx=15)
        card1.pack_propagate(False)

        # Événement de clic
        card1.bind("<Button-1>", lambda e: self.afficher_details_employes())
        card1.configure(cursor="hand2")

        # Effet de survol
        def on_enter_card1(e):
            card1.configure(fg_color="#247a9a")
        def on_leave_card1(e):
            card1.configure(fg_color="#1a5f7a")

        card1.bind("<Enter>", on_enter_card1)
        card1.bind("<Leave>", on_leave_card1)

        # Contenu
        ctk.CTkLabel(card1, text="👥", font=("Arial", 40)).pack(pady=5)
        ctk.CTkLabel(card1, text=f"{nb_employes}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card1, text="Employés", 
             font=("Arial", 14), text_color=BLANC).pack()
        
        # Carte 2 : Tâches
        card2 = ctk.CTkFrame(row1, fg_color="#ff7a00", width=200, height=120)
        card2.pack(side="left", padx=15)
        card2.pack_propagate(False)
        # Événement de clic
        card2.bind("<Button-1>", lambda e: self.afficher_details_taches())
        card2.configure(cursor="hand2")
        # Effet de survol
        def on_enter_card2(e):
            card2.configure(fg_color="#F57C00")
        def on_leave_card2(e):
            card2.configure(fg_color="#1a5f7a")

        card2.bind("<Enter>", on_enter_card2)
        card2.bind("<Leave>", on_leave_card2)

        ctk.CTkLabel(card2, text="📋", font=("Arial",40)).pack(pady=5)
        ctk.CTkLabel(card2, text=f"{nb_taches_a_faire}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card2, text="Tâches à faire", 
                    font=("Arial", 14), text_color=BLANC).pack()
        
        # Carte 3 : Problèmes
        card3 = ctk.CTkFrame(row1, fg_color="#d32f2f", width=200, height=120 )
        card3.pack(side="left", padx=15)
        card3.pack_propagate(False)
        # Événement de clic
        card3.bind("<Button-1>", lambda e: self.afficher_details_problemes())
        card3.configure(cursor="hand2")

        # Effet de survol
        def on_enter_card3(e):
            card3.configure(fg_color="#C62828")
        def on_leave_card3(e):
            card1.configure(fg_color="#D32F2F")

        card3.bind("<Enter>", on_enter_card3)
        card3.bind("<Leave>", on_leave_card3)

        ctk.CTkLabel(card3, text="⚠️", font=("Arial", 40)).pack(pady=5)
        ctk.CTkLabel(card3, text=f"{nb_problemes_ouverts}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card3, text="Problèmes ouverts", 
                    font=("Arial", 14), text_color=BLANC).pack()
        
        # Carte 4 : Départements
        card4 = ctk.CTkFrame(row1, fg_color="#388e3c", width=200, height=120)
        card4.pack(side="left", padx=15)
        card4.pack_propagate(False)
        # Événement de clic
        card4.bind("<Button-1>", lambda e: self.afficher_details_departements())
        card4.configure(cursor="hand2")

        # Effet de survol
        def on_enter_card4(e):
            card4.configure(fg_color="#2E7D32")
        def on_leave_card4(e):
            card4.configure(fg_color="#388E3C")

        card4.bind("<Enter>", on_enter_card4)
        card4.bind("<Leave>", on_leave_card4)

        ctk.CTkLabel(card4, text="🏢", font=("Arial", 40)).pack(pady=5)
        ctk.CTkLabel(card4, text=f"{nb_departements}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card4, text="Départements", 
                    font=("Arial", 14), text_color=BLANC).pack()
        
        # Ligne 2 : Tâches en cours
        row2 = ctk.CTkFrame(stats_frame, fg_color=BLEU)
        row2.pack(fill="x", pady=10)

        card5 = ctk.CTkFrame(row2, fg_color="#1976d2", width=200, height=120)
        card5.pack(side="left", padx=15)
        card5.pack_propagate(False)
        # Événement de clic
        card5.bind("<Button-1>", lambda e: self.afficher_details_taches())
        card5.configure(cursor="hand2")

        # Effet de survol
        def on_enter_card5(e):
            card5.configure(fg_color="#1565C0")
        def on_leave_card5(e):
            card5.configure(fg_color="#1976D2")

        card5.bind("<Enter>", on_enter_card5)
        card5.bind("<Leave>", on_leave_card5)

        ctk.CTkLabel(card5, text="⏳", font=("Arial", 40)).pack(pady=5)
        ctk.CTkLabel(card5, text=f"{nb_taches_en_cours}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card5, text="Tâches en cours", 
                    font=("Arial", 14), text_color=BLANC).pack()
        # Carte 6 : Total tâches
        card6 = ctk.CTkFrame(row2, fg_color="#7b1fa2", width=200, height=120)
        card6.pack(side="left", padx=15)
        card6.pack_propagate(False)
        # Événement de clic
        card6.bind("<Button-1>", lambda e: self.afficher_details_total_taches())
        card6.configure(cursor="hand2")
        # Effet de survol
        def on_enter_card6(e):
            card6.configure(fg_color="#6A1B9A")
        def on_leave_card6(e):
            card6.configure(fg_color="#7B1FA2")

        card6.bind("<Enter>", on_enter_card6)
        card6.bind("<Leave>", on_leave_card6)

        ctk.CTkLabel(card6, text="📊", font=("Arial", 40)).pack(pady=5)
        ctk.CTkLabel(card6, text=f"{nb_taches_total}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card6, text="Total tâches", 
                    font=("Arial", 14), text_color=BLANC).pack()
            
        # Carte 7 : Administrateurs
        card7 = ctk.CTkFrame(row2, fg_color="#00796b", width=200, height=120)
        card7.pack(side="left", padx=15)
        card7.pack_propagate(False)
        # Événement de clic
        card7.bind("<Button-1>", lambda e: self.afficher_details_admins())
        card7.configure(cursor="hand2")

        # Effet de survol
        def on_enter_card7(e):
            card7.configure(fg_color="#00695C")
        def on_leave_card7(e):
            card7.configure(fg_color="#00796B")

        card7.bind("<Enter>", on_enter_card7)
        card7.bind("<Leave>", on_leave_card7)

        ctk.CTkLabel(card7, text="🔑", font=("Arial", 40)).pack(pady=5)
        ctk.CTkLabel(card7, text=f"{nb_admins}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card7, text="Administrateurs", 
                    font=("Arial", 14), text_color=BLANC).pack()
            
        # Carte 8 : Utilisateurs
        card8 = ctk.CTkFrame(row2, fg_color="#5d4037", width=200, height=120)
        card8.pack(side="left", padx=15)
        card8.pack_propagate(False)
        # Événement de clic
        card8.bind("<Button-1>", lambda e: self.afficher_details_users())
        card8.configure(cursor="hand2")

        # Effet de survol
        def on_enter_card8(e):
            card8.configure(fg_color="#5D4037")
        def on_leave_card8(e):
            card8.configure(fg_color="#6D4C41")

        card8.bind("<Enter>", on_enter_card8)
        card8.bind("<Leave>", on_leave_card8)

        ctk.CTkLabel(card8, text="👤", font=("Arial", 40)).pack(pady=5)
        ctk.CTkLabel(card8, text=f"{nb_users}", 
                    font=("Arial", 32, "bold"), text_color=BLANC).pack()
        ctk.CTkLabel(card8, text="Utilisateurs", 
                    font=("Arial", 14), text_color=BLANC).pack() 
            
    def actualiser_dashboard(self):
        """Met à jour les compteurs du tableau de bord"""
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()

        # Nombre d'employés
        cur.execute("SELECT COUNT(*) FROM employes")
        nb_employes = cur.fetchone()[0]
        
        # Nombre de tâches à faire
        cur.execute("SELECT COUNT(*) FROM taches WHERE statut = 'A faire'")
        nb_taches_a_faire = cur.fetchone()[0]
        
        # Nombre de problèmes ouverts
        cur.execute("SELECT COUNT(*) FROM problemes WHERE statut = 'Ouvert'")
        nb_problemes_ouverts = cur.fetchone()[0]
        
        # Nombre de départements
        cur.execute("SELECT COUNT(*) FROM departements")
        nb_departements = cur.fetchone()[0]
        
        # Nombre de tâches en cours
        cur.execute("SELECT COUNT(*) FROM taches WHERE statut = 'En cours'")
        nb_taches_en_cours = cur.fetchone()[0]
        
        # Nombre total de tâches
        cur.execute("SELECT COUNT(*) FROM taches")
        nb_taches_total = cur.fetchone()[0]

        # Nombre d'administrateurs
        cur.execute("SELECT COUNT(*) FROM admins")
        nb_admins = cur.fetchone()[0]
        
        # Nombre d'utilisateurs
        cur.execute("SELECT COUNT(*) FROM users")
        nb_users = cur.fetchone()[0]

        conn.close()

        if hasattr(self, 'nb_employes'):
            self.nb_employes.configure(text=str(nb_employes))
        if hasattr(self, 'nb_taches_a_faire'):
            self.nb_taches_a_faire.configure(text=str(nb_taches_a_faire))
        if hasattr(self, 'nb_problemes_ouverts'):
            self.nb_problemes_ouverts.configure(text=str(nb_problemes_ouverts))
        if hasattr(self, 'nb_departements'):
            self.nb_departements.configure(text=str(nb_departements))
        if hasattr(self,'nb_taches_en_cours'):
            self.nb_taches_en_cours.configure(text=str(nb_taches_en_cours))
        if hasattr(self, 'nb_taches_total'):
            self.nb_taches_total.configure(text=(nb_taches_total))
        if hasattr(self, 'nb_admins'):
            self.nb_admins.configure(text=str(nb_admins))
        if hasattr(self, 'nb_users'):
            self.nb_users.configure(text=str(nb_users))
    

    def afficher_details_employes(self):
        """Affiche la liste complète des employés"""
        w = Toplevel(self.root)
        w.title("Liste des Employés")
        w.geometry("900x600")
        w.iconbitmap(chemin_logo)
        w.configure(bg=BLEU)
        
        ctk.CTkLabel(w, text="👥 Liste des Employés", 
                    font=("Times New Roman", 18, "bold"),
                    text_color=BLANC).pack(pady=15)
        
        # Frame scrollable
        scroll_frame = ctk.CTkScrollableFrame(w, width=750, height=450, fg_color=BLANC)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
        cur.execute("""
            SELECT e.nom, e.poste, d.nom_dept, e.salaire, e.tel
            FROM employes e
            JOIN departements d ON e.id_dept = d.id_dept
            ORDER BY e.nom ASC
            """)
        employes = cur.fetchall()
        conn.close()
        
        if not employes:
            ctk.CTkLabel(scroll_frame, text="Aucun employé enregistré", 
                        text_color=BLEU).pack(pady=20)
        else:
            # En-têtes
            header = ctk.CTkFrame(scroll_frame, fg_color=BLEU, height=30)
            header.pack(fill="x", pady=5)
            ctk.CTkLabel(header, text="Nom", width=200, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Poste", width=200, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Département", width=150, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Salaire", width=100, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Tél", width=120, text_color=BLANC).pack(side="left", padx=5)
            
            # Liste des employés
            for i, emp in enumerate(employes):
                nom, poste, dept, salaire, tel = emp
                bg_color = "#f0f0f0" if i % 2 == 0 else "#e0e0e0"
                row = ctk.CTkFrame(scroll_frame, fg_color=bg_color, height=40)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=nom, width=200, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=poste, width=200, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=dept, width=150, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=f"{salaire} MAD", width=100, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=tel, width=120, text_color=BLEU).pack(side="left", padx=5)
        
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def afficher_details_taches(self, statut=None):
        """Affiche les tâches (filtrées par statut si précisé)"""
        w = Toplevel(self.root)
        w.title("Liste des Tâches")
        w.iconbitmap(chemin_logo)
        w.geometry("900x600")
        w.configure(bg=BLEU)
    
        titre = "Toutes les Tâches" if not statut else f"Tâches : {statut}"
        ctk.CTkLabel(w, text=f"📋 {titre}", 
                 font=("Times New Roman", 18, "bold"),
                 text_color=BLANC).pack(pady=15)
    
        scroll_frame = ctk.CTkScrollableFrame(w, width=750, height=450, fg_color=BLANC)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
    
        if statut:
            cur.execute("""
            SELECT t.titre, t.statut, t.date_debut, t.date_fin, e.nom
            FROM taches t
            JOIN employes e ON t.id_emp = e.id_emp
            WHERE t.statut = ?
            ORDER BY t.date_fin ASC
        """, (statut,))
        else:
            cur.execute("""
            SELECT t.titre, t.statut, t.date_debut, t.date_fin, e.nom
            FROM taches t
            JOIN employes e ON t.id_emp = e.id_emp
            ORDER BY t.date_fin ASC
        """)
    
        taches = cur.fetchall()
        conn.close()
    
        if not taches:
            ctk.CTkLabel(scroll_frame, text="Aucune tâche trouvée", text_color=BLEU).pack(pady=20)
        else:
            for t in taches:
                titre, statut, debut, fin, employe = t
                row = ctk.CTkFrame(scroll_frame, fg_color="#f0f0f0", height=50)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=f"📌 {titre}", width=250, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=f"👤 {employe}", width=150, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=f"📊 {statut}", width=100, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=f"📅 {fin}", width=120, text_color=BLEU).pack(side="left", padx=5)
    
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def afficher_details_problemes(self):
        """Affiche la liste des problèmes ouverts"""
        w = Toplevel(self.root)
        w.title("Problèmes Ouverts")
        w.geometry("900x600")
        w.iconbitmap(chemin_logo)
        w.configure(bg=BLEU)
    
        ctk.CTkLabel(w, text="⚠️ Problèmes Ouverts", 
                    font=("Times New Roman", 18, "bold"),
                    text_color=BLANC).pack(pady=15)
        
        scroll_frame = ctk.CTkScrollableFrame(w, width=650, height=350, fg_color=BLANC)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
        cur.execute("""
            SELECT description, date_declaration, statut
            FROM problemes
            WHERE statut = 'Ouvert'
            ORDER BY date_declaration DESC
        """)
        problemes = cur.fetchall()
        conn.close()
    
        if not problemes:
            ctk.CTkLabel(scroll_frame, text="Aucun problème ouvert", text_color=BLEU).pack(pady=20)
        else:
            for desc, date, statut in problemes:
                row = ctk.CTkFrame(scroll_frame, fg_color="#f0f0f0", height=60)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=f"📝 {desc[:50]}...", width=400, text_color=BLEU, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(row, text=f"📅 {date}", width=150, text_color=BLEU).pack(side="left", padx=5)
        
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def afficher_details_departements(self):
        """Affiche la liste des départements dans un tableau propre"""
        w = Toplevel(self.root)
        w.title("Liste des Départements")
        w.geometry("900x600")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)
    
        # Titre
        ctk.CTkLabel(w, text="🏢 Départements", 
                    font=("Times New Roman", 18, "bold"),
                 text_color=BLANC).pack(pady=15)
        
        # Frame scrollable
        scroll_frame = ctk.CTkScrollableFrame(w, width=550, height=350, fg_color=BLANC)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
        cur.execute("SELECT id_dept, nom_dept FROM departements ORDER BY nom_dept ASC")
        depts = cur.fetchall()
        conn.close()
    
        if not depts:
            ctk.CTkLabel(scroll_frame, text="Aucun département enregistré", 
                     text_color=BLEU, font=("Arial", 14)).pack(pady=20)
        else:
        # === EN-TÊTES DU TABLEAU ===
            header = ctk.CTkFrame(scroll_frame, fg_color=BLEU, height=35)
            header.pack(fill="x", pady=(5, 2))
        
        ctk.CTkLabel(header, text="ID", width=80, 
                     font=("Arial", 12, "bold"), 
                     text_color=BLANC).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Nom du Département", width=400, 
                     font=("Arial", 12, "bold"), 
                     text_color=BLANC).pack(side="left", padx=10)
        
        # === LIGNES DU TABLEAU ===
        for i, dept in enumerate(depts):
            id_dept, nom_dept = dept
            
            # Couleur alternée pour meilleure lisibilité
            bg_color = "#f0f0f0" if i % 2 == 0 else "#e0e0e0"
            
            row = ctk.CTkFrame(scroll_frame, fg_color=bg_color, height=40)
            row.pack(fill="x", pady=1)
            
            ctk.CTkLabel(row, text=f"{id_dept}", width=80, 
                         text_color=BLEU, font=("Arial", 11)).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=nom_dept, width=400, 
                         text_color=BLEU, font=("Arial", 11)).pack(side="left", padx=10)
        ctk.CTkButton(w, text="Fermer", command=w.destroy, 
                  fg_color=ORANGE, width=150).pack(pady=10)
        
    def afficher_details_total_taches(self):
        """Affiche TOUTES les tâches (tous statuts confondus)"""
        w = Toplevel(self.root)
        w.title("Toutes les Tâches")
        w.geometry("900x600")
        w.iconbitmap(chemin_logo)
        w.configure(bg=BLEU)
            
        ctk.CTkLabel(w, text="📊 Toutes les Tâches", 
                    font=("Times New Roman", 18, "bold"),
                    text_color=BLANC).pack(pady=15)
        
        # Frame de filtres
        filter_frame = ctk.CTkFrame(w, fg_color=BLEU)
        filter_frame.pack(fill="x", padx=20, pady=5)
    
        ctk.CTkLabel(filter_frame, text="Filtrer par statut :", 
                 text_color=BLANC).pack(side="left", padx=5)
    
        statut_var = ctk.StringVar(value="Tous")
        filter_menu = ctk.CTkOptionMenu(filter_frame, values=["Tous", "A faire", "En cours", "Terminé"],
                                     variable=statut_var, width=150,
                                     command=lambda x: self._rafraichir_taches(scroll_frame, statut_var.get()))
        filter_menu.pack(side="left", padx=5)
    
        # Frame scrollable pour les tâches
        scroll_frame = ctk.CTkScrollableFrame(w, width=850, height=450, fg_color=BLANC)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
        self._afficher_taches(scroll_frame, "Tous")
    
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def _afficher_taches(self, parent, statut):
        """Remplit le parent (scroll_frame) avec la liste des tâches selon le statut"""
            
        for widget in parent.winfo_children():
            widget.destroy()

        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()

        if statut == "Tous":
            cur.execute("""
                    SELECT t.titre, t.statut, t.date_debut, t.date_fin, e.nom
                    FROM taches t
                    JOIN employes e ON t.id_emp = e.id_emp
                    ORDER BY t.date_fin ASC
                """)
        else:
            cur.execute("""
                    SELECT t.titre, t.statut, t.date_debut, t.date_fin, e.nom
                    FROM taches t
                    JOIN employes e ON t.id_emp = e.id_emp
                    WHERE t.statut = ?
                    ORDER BY t.date_fin ASC
                """, (statut,))

        taches = cur.fetchall()
        conn.close()

        if not taches:
                ctk.CTkLabel(parent, text="Aucune tâche trouvée",
                            text_color=BLEU, font=("Arial", 14)).pack(pady=20)
        else:
                # En-têtes
            header = ctk.CTkFrame(parent, fg_color=BLEU, height=30)
            header.pack(fill="x", pady=5)
            ctk.CTkLabel(header, text="Titre", width=250, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Employé", width=150, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Statut", width=100, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Début", width=100, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Fin", width=100, text_color=BLANC).pack(side="left", padx=5)

                # Liste des tâches
            for t in taches:
                titre, statut, debut, fin, employe = t
                couleur_statut = "green" if statut == "Terminé" else "orange" if statut == "En cours" else "red"

                row = ctk.CTkFrame(parent, fg_color="#f0f0f0", height=40)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=titre[:40], width=250, text_color=BLEU, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(row, text=employe, width=150, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=statut, width=100, text_color=couleur_statut).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=debut, width=100, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=fin, width=100, text_color=BLEU).pack(side="left", padx=5)

    def _rafraichir_taches(self, parent, statut):
        self._afficher_taches(parent, statut)

    def afficher_details_admins(self):
        """Affiche la liste des administrateurs"""
        w = Toplevel(self.root)
        w.title("Liste des Administrateurs")
        w.geometry("900x600")
        w.iconbitmap(chemin_logo)
        w.configure(bg=BLEU)
    
        ctk.CTkLabel(w, text="🔑 Administrateurs", 
                 font=("Times New Roman", 18, "bold"),
                 text_color=BLANC).pack(pady=15)
    
        scroll_frame = ctk.CTkScrollableFrame(w, width=550, height=350, fg_color=BLANC)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
        cur.execute("SELECT nom, role FROM admins ORDER BY nom ASC")
        admins = cur.fetchall()
        conn.close()
    
        if not admins:
            ctk.CTkLabel(scroll_frame, text="Aucun administrateur enregistré", 
                     text_color=BLEU).pack(pady=20)
        else:
            # En-têtes
            header = ctk.CTkFrame(scroll_frame, fg_color=BLEU, height=30)
            header.pack(fill="x", pady=5)
            ctk.CTkLabel(header, text="Nom", width=300, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Rôle", width=200, text_color=BLANC).pack(side="left", padx=5)
        
            # Liste des admins
            for admin in admins:
                nom, role = admin
                row = ctk.CTkFrame(scroll_frame, fg_color="#f0f0f0", height=40)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=nom, width=300, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=role, width=200, text_color=BLEU).pack(side="left", padx=5)
    
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def afficher_details_users(self):
        """Affiche la liste de tous les utilisateurs"""
        w = Toplevel(self.root)
        w.title("Liste des Utilisateurs")
        w.geometry=("900x600")
        w.iconbitmap(chemin_logo)
        w.configure(bg=BLEU)
    
        ctk.CTkLabel(w, text="👤 Utilisateurs", 
                 font=("Times New Roman", 18, "bold"),
                 text_color=BLANC).pack(pady=15)
    
        scroll_frame = ctk.CTkScrollableFrame(w, width=550, height=350, fg_color=BLANC)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
        cur.execute("SELECT username, role FROM users ORDER BY username ASC")
        users = cur.fetchall()
        conn.close()
    
        if not users:
            ctk.CTkLabel(scroll_frame, text="Aucun utilisateur enregistré", 
                     text_color=BLEU).pack(pady=20)
        else:
        # En-têtes
            header = ctk.CTkFrame(scroll_frame, fg_color=BLEU, height=30)
            header.pack(fill="x", pady=5)
            ctk.CTkLabel(header, text="Nom d'utilisateur", width=300, text_color=BLANC).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Rôle", width=200, text_color=BLANC).pack(side="left", padx=5)
        
            # Liste des utilisateurs
            for user in users:
                username, role = user
                row = ctk.CTkFrame(scroll_frame, fg_color="#f0f0f0", height=40)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=username, width=300, text_color=BLEU).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=role, width=200, text_color=BLEU).pack(side="left", padx=5)
    
        ctk.CTkButton(w, text="Fermer", command=w.destroy, fg_color=ORANGE).pack(pady=10)

    def rechercher_employes(self):
        """Ouvre une fenêtre de recherche d'employés"""
        w = Toplevel(self.root)
        w.title("Rechercher un Employé")
        w.geometry("900x600")
        w.configure(bg=BLEU)
        w.iconbitmap(chemin_logo)
    
        # Titre
        ctk.CTkLabel(w, text="🔍 Recherche d'Employés", 
                    font=("Times New Roman", 18, "bold"),
                    text_color=BLANC).pack(pady=15)
        
        # Frame de recherche
        search_frame = ctk.CTkFrame(w, fg_color=BLEU)
        search_frame.pack(fill="x", padx=20, pady=10)
        
    # Champ de recherche
        ctk.CTkLabel(search_frame, text="Rechercher :", 
                    text_color=BLANC).pack(side="left", padx=5)
        
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, width=300, 
                                    placeholder_text="Nom, poste ou département...",
                                    textvariable=search_var)
        search_entry.pack(side="left", padx=5)
        
    # Bouton rechercher
        ctk.CTkButton(search_frame, text="Rechercher", 
                    command=lambda: self.afficher_resultats_recherche(w, search_var.get()),
                    fg_color=ORANGE).pack(side="left", padx=10)
        
        ctk.CTkButton(search_frame, text="Voir tout", 
                    command=lambda: self.afficher_resultats_recherche(w, ""),
                    fg_color=BLEU).pack(side="left", padx=5)
        
    # Frame pour les résultats (scrollable)
        results_frame = ctk.CTkScrollableFrame(w, width=750, height=400, fg_color=BLANC)
        results_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
    # Stocker la référence pour mise à jour
        self.results_frame = results_frame
        
        # Afficher tous les employés au démarrage
        self.afficher_resultats_recherche(w, "")
        
    # Bouton fermer
        ctk.CTkButton(w, text="Fermer", command=w.destroy, 
                    fg_color="gray").pack(pady=10)

    def afficher_resultats_recherche(self, parent, terme_recherche):
        """Affiche les résultats de recherche"""
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()

        # Nettoyer les anciens résultats
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Requête avec jointure pour avoir le nom du département
        if terme_recherche:
            # Recherche floue sur nom, poste ou département
            cur.execute("""
                SELECT e.nom, e.poste, d.nom_dept, e.salaire, e.tel
                FROM employes e
                JOIN departements d ON e.id_dept = d.id_dept
                WHERE e.nom LIKE ? OR e.poste LIKE ? OR d.nom_dept LIKE ?
                ORDER BY e.nom ASC
            """, (f'%{terme_recherche}%', f'%{terme_recherche}%', f'%{terme_recherche}%'))
        else:
            cur.execute("""
                SELECT e.nom, e.poste, d.nom_dept, e.salaire, e.tel
                FROM employes e
                JOIN departements d ON e.id_dept = d.id_dept
                ORDER BY e.nom ASC
            """)
        
        employes = cur.fetchall()
        conn.close()
        
        if not employes:
            ctk.CTkLabel(self.results_frame, 
                        text="Aucun employé trouvé",
                        text_color=BLEU, font=("Arial", 14)).pack(pady=20)
            return
        
        # En-têtes
        header = ctk.CTkFrame(self.results_frame, fg_color=BLEU, height=30)
        header.pack(fill="x", pady=5)
        ctk.CTkLabel(header, text="Nom", width=200, text_color=BLANC).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Poste", width=200, text_color=BLANC).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Département", width=150, text_color=BLANC).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Salaire", width=100, text_color=BLANC).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Téléphone", width=120, text_color=BLANC).pack(side="left", padx=5)
        
        # Afficher chaque employé
        for emp in employes:
            nom, poste, dept, salaire, tel = emp
            row = ctk.CTkFrame(self.results_frame, fg_color="#f0f0f0", height=40)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=nom, width=200, text_color=BLEU).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=poste, width=200, text_color=BLEU).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=dept, width=150, text_color=BLEU).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"{salaire} MAD", width=100, text_color=BLEU).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=tel, width=120, text_color=BLEU).pack(side="left", padx=5)
    
    def verifier_notifications(self):
        """Vérifie et affiche les notifications importantes"""
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
        
        # Tâches qui arrivent à échéance dans moins de 3 jours
        cur.execute("""
            SELECT titre, date_fin, e.nom
            FROM taches t
            JOIN employes e ON t.id_emp = e.id_emp
            WHERE t.statut != 'Terminé'
            AND t.date_fin <= date('now', '+3 days')
            AND t.date_fin >= date('now')
            ORDER BY t.date_fin ASC
        """)
        taches_urgentes = cur.fetchall()
        
        # Tâches en retard
        cur.execute("""
            SELECT titre, date_fin, e.nom
            FROM taches t
            JOIN employes e ON t.id_emp = e.id_emp
            WHERE t.statut != 'Terminé'
            AND t.date_fin < date('now')
            ORDER BY t.date_fin ASC
        """)
        taches_retard = cur.fetchall()
        
        # Problèmes non résolus
        cur.execute("""
            SELECT COUNT(*) FROM problemes WHERE statut = 'Ouvert'
        """)
        nb_problemes = cur.fetchone()[0]
        
        conn.close()
        
        # Afficher les alertes
        messages = []
        
        if taches_retard:
            messages.append(f" {len(taches_retard)} tâche(s) en retard !")
        
        if taches_urgentes:
            messages.append(f"🟠 {len(taches_urgentes)} tâche(s) arrivent à échéance sous 3 jours")
        
        if nb_problemes > 0:
            messages.append(f"⚠️ {nb_problemes} problème(s) non résolu(s)")
        
        if messages:
            # Créer une frame de notifications en haut
            notif_frame = ctk.CTkFrame(self.root, fg_color="#fff3cd", border_width=2, 
                                    border_color="#ffc107")
            notif_frame.pack(fill="x", padx=20, pady=5, before=self.root.winfo_children()[0] if self.root.winfo_children() else None)
            
            ctk.CTkLabel(notif_frame, text="🔔 Notifications", 
                        font=("Arial", 12, "bold"), 
                        text_color="#856404").pack(pady=5)
            
            for msg in messages:
                ctk.CTkLabel(notif_frame, text=msg, 
                            text_color="#856404").pack(pady=2)
            
            # Bouton voir détails
            ctk.CTkButton(notif_frame, text="Voir détails", 
                        command=lambda: self.afficher_details_notifications(taches_urgentes, taches_retard),
                        fg_color="#ffc107", text_color="#856404",
                        hover_color="#ffb300").pack(pady=5)
        
        # Programmer une vérification toutes les 5 minutes
        self.root.after(300000, self.verifier_notifications)

    def afficher_details_notifications(self, taches_urgentes, taches_retard):
        """Affiche les détails des notifications"""
        w = Toplevel(self.root)
        w.title("Notifications")
        w.geometry("600x500")
        w.configure(bg=BLEU)
        
        ctk.CTkLabel(w, text="🔔 Détails des Notifications", 
                    font=("Times New Roman", 16, "bold"),
                    text_color=BLANC).pack(pady=10)
        
        # Frame scrollable
        details_frame = ctk.CTkScrollableFrame(w, width=550, height=350, fg_color=BLANC)
        details_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Tâches en retard
        if taches_retard:
            ctk.CTkLabel(details_frame, text="🔴 TÂCHES EN RETARD", 
                        font=("Arial", 12, "bold"), text_color="red").pack(pady=5)
            for titre, date_fin, employe in taches_retard:
                ctk.CTkLabel(details_frame, 
                            text=f"• {titre} - {employe} (Échéance: {date_fin})",
                            text_color=BLEU, anchor="w").pack(fill="x", padx=10, pady=2)
        
        # Tâches urgentes
        if taches_urgentes:
            ctk.CTkLabel(details_frame, text="🟠 TÂCHES URGENTES", 
                        font=("Arial", 12, "bold"), text_color="orange").pack(pady=5)
            for titre, date_fin, employe in taches_urgentes:
                ctk.CTkLabel(details_frame, 
                            text=f"• {titre} - {employe} (Échéance: {date_fin})",
                            text_color=BLEU, anchor="w").pack(fill="x", padx=10, pady=2)
        
    
        ctk.CTkButton(w, text="Fermer", command=w.destroy, 
                    fg_color=ORANGE).pack(pady=10)
                          



