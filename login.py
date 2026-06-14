import customtkinter as ctk
from tkinter import messagebox, Toplevel
import sqlite3
from database import Database
from utils import *
from PIL import Image

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.db.init_db()  
        self.trycount = 3
        
        # Configuration de la fenêtre
        self.root.title("Atlas Login")
        self.root.configure(bg=BLEU)
        self.root.geometry("900x600")
        self.root.iconbitmap(chemin_logo)

        # ✅ Lancer l'écran de chargement au démarrage
        self._show_loading()

    # ==========================================
    #  MÉTHODES DE CHARGEMENT 
    # ==========================================
    def _show_loading(self):
        """Affiche un écran de chargement avant la page de connexion"""
        self.loading_frame = ctk.CTkFrame(self.root, fg_color=BLEU)
        self.loading_frame.place(relwidth=1, relheight=1)

        ctk.CTkLabel(self.loading_frame, text="Bienvenue sur Atlas Bâtiment. Tout se met en place pour votre session...", 
                     font=("Times New Roman", 22, "bold"), text_color=BLANC).pack(pady=(80, 5))

        # ⏳ Label pour l'animation des points
        self.waiting_lbl = ctk.CTkLabel(self.loading_frame, text="Veuillez patienter.", 
                                        font=("Times New Roman", 16), text_color="#d0d0d0")
        self.waiting_lbl.pack(pady=(0, 15))
        self.dot_count = 0  # Compteur cyclique (0 à 3)

        self.progress = ctk.CTkProgressBar(self.loading_frame, width=350, mode="determinate", 
                                           progress_color=ORANGE)
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.percent_lbl = ctk.CTkLabel(self.loading_frame, text="0%", 
                                        text_color=BLANC, font=("Times New Roman", 14, "bold"))
        self.percent_lbl.pack()

        # Lancer les deux processus en parallèle
        self._update_progress(0)
        self._animate_dots()

    def _animate_dots(self):
        """Anime les points de suspension : . .. ... (répétition)"""
        self.dot_count = (self.dot_count + 1) % 4
        self.waiting_lbl.configure(text=f"Veuillez patienter{'.' * self.dot_count}")
        # Relance toutes les 500ms 
        self.dot_job = self.root.after(500, self._animate_dots)

    def _update_progress(self, value):
        """Met à jour la barre de progression (0 à 100)"""
        self.progress.set(value / 100)
        self.percent_lbl.configure(text=f"{value}%")
        
        if value < 100:
            # 100 étapes × 100ms = 10 secondes de chargement total
            self.root.after(200, self._update_progress, value + 1)
        else:
            self.root.after(600, self._show_login_form)

    def _show_login_form(self):
        """Détruit l'écran de chargement et affiche le formulaire de connexion"""
        # Arrête proprement l'animation pour éviter les erreurs après destruction
        if hasattr(self, 'dot_job'):
            self.root.after_cancel(self.dot_job)
        self.loading_frame.destroy()
        self._build_ui()
    
    def _build_ui(self):
        """Crée l'interface de connexion (appelée après le chargement)"""
        # Chargement du logo
        try:
            mon_image = ctk.CTkImage(
                light_image=Image.open("D:/Atlas_Bâtiment/logo.ico"), 
                dark_image=Image.open("D:/Atlas_Bâtiment/logo.ico"),
                size=(150, 150) 
            )
        except FileNotFoundError:
            print("Erreur : Image non trouvée. Vérifiez le chemin.")
            mon_image = None

        # Frame principale
        main = ctk.CTkFrame(self.root, fg_color=BLEU)
        main.pack(expand=True)
        
        # Carte de connexion
        card = ctk.CTkFrame(main, fg_color=BLANC, width=400, height=500)
        card.pack()
        card.pack_propagate(False)
            
        if mon_image:
            self.logo_label = ctk.CTkLabel(card, image=mon_image, text="")
            self.logo_label.pack(side="top", pady=(10, 2)) 
        else:
            self.logo_label = ctk.CTkLabel(card, text="[LOGO ICI]", font=("Arial", 20, "bold"))
            self.logo_label.pack(side="top", pady=(2, 10))
       
        # Titre
        ctk.CTkLabel(card, text="Se connecter", font=("Times New Roman", 22, "bold"), 
                     text_color=BLEU).pack(pady=5)
           
        # Champ utilisateur
        self.us = ctk.CTkEntry(card, width=250, placeholder_text="Nom d'utilisateur",
                               fg_color="#f0f0f0", border_color=BLEU)
        self.us.pack(pady=10)

        # Champ mot de passe
        self.pw = ctk.CTkEntry(card, width=250, show="*", placeholder_text="Mot de passe",
                               fg_color="#f0f0f0", border_color=BLEU)
        self.pw.pack(pady=10)

        # Checkbox afficher mdp
        self.show = ctk.BooleanVar()
        ctk.CTkCheckBox(card, text="Afficher mot de passe", variable=self.show,
                        font=("Times New Roman", 14),
                        command=lambda: self.pw.configure(show="" if self.show.get() else "*"),
                        text_color=BLEU).pack(pady=5)
    
        # Bouton Connexion
        ctk.CTkButton(card, width=250, fg_color=ORANGE, hover_color="#e66e00",
                      text="Connexion", font=("Times New Roman", 14, "bold"), 
                      command=self.connect).pack(pady=15)
        
        # Bouton Mot de passe oublié
        ctk.CTkButton(card, width=250, fg_color=BLEU, hover_color="#1a3d5c",
                      text="Mot de passe oublié", font=("Times New Roman", 14), 
                      command=self.forgot_password).pack(pady=5)

        # Label d'information (erreurs, tentatives)
        self.info = ctk.CTkLabel(card, text="", text_color="red", 
                                 font=("Times New Roman", 15), justify="center")
        self.info.pack(pady=10)

    # ========================================================================
    # 🔐 TES MÉTHODES EXISTANTES (inchangées)
    # ========================================================================

    def login(self, username, password):
        """Vérifie les identifiants dans la BDD"""
        try:
            conn = sqlite3.connect(chemin_db)
            cur = conn.cursor()
            
            # Vérifier dans users
            cur.execute('SELECT username, password, role FROM users WHERE username=?', (username,))
            result = cur.fetchone()

            if result and result[1] == password:
                conn.close()
                return (result[0], result[1], result[2])
            
            # Vérifier dans admins
            cur.execute('SELECT nom, mot_de_passe, role FROM admins WHERE nom=?', (username,))
            result = cur.fetchone()
            
            if result and result[1] == password:
                conn.close()
                return (result[0], result[1], result[2])
                
            conn.close()
            return None
            
        except sqlite3.Error as e:
            return {"error": str(e)}

    def connect(self):
        """Gère la connexion utilisateur"""
        username = self.us.get().strip()
        password = self.pw.get().strip()

        # Validation des champs vides
        if not username or not password:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis", parent=self.root)
            return 
        
        # Vérification des identifiants
        res = self.login(username, password)
      
        if isinstance(res, dict) and res.get("error"):
            messagebox.showerror("Erreur BDD", res.get("error"))
            return
        
        if res:
            # Connexion réussie
            messagebox.showinfo("Succès", "Connexion réussie")
            logger(self.db, username, "CONNEXION", "Succès")
            
            role = res[2] if len(res) >= 3 else None
            self.root.withdraw()  # Cacher la fenêtre de login
            
            if role in ["Admin", "PDG", "DRH", "Manager"]:
                from admin import Admin
                Admin(self.root)
            else:
                from employe import Employe
                Employe(self.root, username)
        else:
            # Échec de connexion
            self.trycount -= 1
            logger(self.db, username, "ECHEC_CONNEXION", f"Tentative {4 - self.trycount}")
            
            if self.trycount > 0:
                self.info.configure(text=f" Identifiants incorrects.\nTentatives restantes: {self.trycount}")
                self.pw.delete(0, 'end')
            else:
                messagebox.showerror("Bloqué", "Trop de tentatives échouées.\nVeuillez réessayer plus tard.")
                logger(self.db, username, "COMPTE_BLOQUE", "3 échecs de connexion")
                self.root.destroy()

    def forgot_password(self):
        """Ouvre la fenêtre de réinitialisation du mot de passe"""
        username = self.us.get().strip()
        if not username:
            messagebox.showerror("Erreur", "Veuillez entrer votre nom d'utilisateur.")
            return
        
        # Vérifier si l'utilisateur existe
        conn = sqlite3.connect(chemin_db)
        cur = conn.cursor()
        cur.execute('SELECT username FROM users WHERE username=?', (username,))
        row = cur.fetchone()
        conn.close()
        
        if row is None:
            messagebox.showerror("Erreur", "Nom d'utilisateur non trouvé.")
            return
        
        # Ouvrir la fenêtre de réinitialisation
        self.root.withdraw()
        self.root1 = Toplevel(self.root)
        self.root1.title("Réinitialisation du mot de passe")
        self.root1.geometry("400x300")
        self.root1.configure(bg=BLEU)
        self.root1.iconbitmap(chemin_logo)
        
        ctk.CTkLabel(self.root1, text="Nouveau mot de passe", text_color=BLANC,
                     font=("Times New Roman", 14)).pack(pady=15)
        
        self.entry_mdp = ctk.CTkEntry(self.root1, show="*", placeholder_text="Nouveau mot de passe", width=250)
        self.entry_mdp.pack(pady=10)
        
        self.entry_confirm = ctk.CTkEntry(self.root1, show="*", placeholder_text="Confirmer", width=250)
        self.entry_confirm.pack(pady=10)
        
        ctk.CTkButton(self.root1, text="Réinitialiser", command=self.rein_mdp, 
                      fg_color=ORANGE, width=250).pack(pady=15)
        
        # Gérer la fermeture de la fenêtre
        def on_close():
            self.root1.destroy()
            self.root.deiconify()
        
        self.root1.protocol("WM_DELETE_WINDOW", on_close)

    def rein_mdp(self):
        """Réinitialise le mot de passe"""
        new_password = self.entry_mdp.get()
        confirm_password = self.entry_confirm.get()
        
        if not new_password or not confirm_password:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return
        
        # Validation de la force du mot de passe
        from utils import valider_mot_de_passe
        is_valid, message = valider_mot_de_passe(new_password)
        if not is_valid:
            messagebox.showerror("Erreur", message)
            return
        
        try:
            conn = sqlite3.connect(chemin_db)
            cur = conn.cursor()
            cur.execute('UPDATE users SET password=? WHERE username=?', (new_password, self.us.get()))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Succès", "Mot de passe réinitialisé avec succès.")
            self.root1.destroy()
            self.root.deiconify()
            self.pw.delete(0, 'end')
            self.us.delete(0, 'end')
            self.info.configure(text="")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")