
from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
import sqlite3

ctk.set_appearance_mode("light")
   #couleurs
ORANGE = "#ff7a00"
BLEU = "#0f2a44"
BLANC = "#ffffff" 

# chemin de la base de données
chemin ="D:/Atlas_Bâtiment/Atlas.db"
def init_db():
    conn = sqlite3.connect(chemin)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id_users INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Manager'
        )
    """
    )
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employes (
            id_emp INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            poste TEXT NOT NULL,
            id_dept INTEGER NOT NULL,
            salaire REAL NOT NULL,
            tel VARCHAR(15) NOT NULL,
            FOREIGN KEY (id_dept) REFERENCES departements(id_dept)
        )
    """
    )
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id_admins INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            mot_de_passe TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """       
    )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS taches (
            id_taches INTEGER PRIMARY KEY AUTOINCREMENT,
            id_emp INTEGER NOT NULL,
            titre TEXT NOT NULL,
            statut TEXT DEFAULT 'A faire',
            date_debut DATE DEFAULT (DATE('now')),
            date_fin DATE,
            FOREIGN KEY (id_emp) REFERENCES employes(id_emp)
        )
    """
    )
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS problemes (
            id_problemes INTEGER PRIMARY KEY AUTOINCREMENT,
            id_dept INTEGER NOT NULL,
            description TEXT NOT NULL,
            statut TEXT DEFAULT 'Ouvert',
            date_declaration DATE DEFAULT (DATE('now')),
            FOREIGN KEY (id_dept) REFERENCES departements(id_dept)
        )
    """
    )
    cur.execute("""
            CREATE TABLE IF NOT EXISTS batiments (
                id_bat INTEGER PRIMARY KEY AUTOINCREMENT,
                type_bat TEXT NOT NULL,
                prix REAL NOT NULL)
                """
                )
    cur.execute("""            
            CREATE TABLE IF NOT EXISTS clients (
                id_clients INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                tel VARCHAR(15) NOT NULL,
                adresse VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS projets (
                id_projets INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_projet TEXT NOT NULL,
                id_clients INTEGER NOT NULL,
                date_debut DATE NOT NULL,
                date_fin DATE NOT NULL,
                statut TEXT DEFAULT 'En cours',
                budget REAL NOT NULL,
                FOREIGN KEY (id_clients) REFERENCES clients(id_clients)
            )
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS departements (
                id_dept INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_dept TEXT NOT NULL    
            )
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS fournisseurs (
                id_fourn INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_fourn TEXT NOT NULL,
                ville VARCHAR(255) NOT NULL,
                tel VARCHAR(15) NOT NULL,
                adresse VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS ventes (
                id_ventes INTEGER PRIMARY KEY AUTOINCREMENT,
                date_vente DATE DEFAULT (DATE('now')),
                montant REAL NOT NULL
                
            )
    """)          

    conn.commit()
    conn.close()
    
    conn = sqlite3.connect(chemin)
    cur = conn.cursor()
    # ajout dans users pour la connexion
    cur.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES (?,?,?)", ("soro","1234","Admin"))
    conn.commit()
    conn.close()

class LoginPage:
    def __init__(self, root, ):
        self.root = root
        self.chemin="D:/Atlas_Bâtiment/Atlas.db"
        self.logo="D:/Atlas_Bâtiment/logo.ico"
        
        self.trycount = 3 
        self.root.title("Atlas Login")
        self.root.configure(bg='skyblue')
        self.root.geometry("900x600")
        self.root.iconbitmap(self.logo)

        main = Frame(root,bg=BLEU)
        main.pack(expand=True)
        card = Frame(main,bg='white',width=350,height=420)
        card.pack()
        card.pack_propagate(False)
       
        ctk.CTkLabel(card, text="Se connecter", font=("Times New Roman", 22), anchor='w').pack(pady=10)
           
        self.us = ctk.CTkEntry(card, width=250, placeholder_text="Entrez votre nom d'utilisateur")
        self.us.pack(pady=10)

        self.pw = ctk.CTkEntry(card, width=250, show="*", placeholder_text="Entrez votre mot de passe")
        self.pw.pack(pady=10)

        self.show = IntVar()
        ctk.CTkCheckBox(card, text="Afficher mot de passe", variable=self.show,font=("Times New Roman", 20),
                    command=lambda: self.pw.configure(show="" if self.show.get() else "*")).pack()
    
        ctk.CTkButton(card,width=250, fg_color=ORANGE, text="Connexion", font=("Times New Roman", 14), command=self.connect).pack(pady=10)
        ctk.CTkButton(card,width=250, fg_color=ORANGE, text="Mot de passe oublié", font=("Times New Roman", 14),  command=self.forgot_password).pack(pady=10)
        self.info = ctk.CTkLabel(card,text="", font=("Times New Roman", 15), justify='center')
        self.info.pack(pady=5)

    def login(self, username=None, password=None):
        
        if username is None:
            username = self.us.get()
        if password is None:
            password = self.pw.get()
        result=None

        try:
            conn = sqlite3.connect(chemin)
            cur = conn.cursor()
            cur.execute('SELECT username,password,role FROM users WHERE username=? AND password=?', (username, password))
            result=cur.fetchone()
            
            if not result:
                cur.execute('SELECT nom,mot_de_passe,role FROM admins WHERE nom=? AND mot_de_passe=?', (username, password))
                result = cur.fetchone()
        except sqlite3.Error as e:
            return {"error": str(e)}
        finally:
            conn.close()

        return result    

    def connect(self):
        username = self.us.get()
        password = self.pw.get()

        if username=="" or password=="":
            messagebox.showerror("Erreur","Tous les champs doivent être remplis",parent=self.root)
            return 
        
       
        res = self.login(self.us.get(), self.pw.get())
        if isinstance(res, dict) and res.get("error"):
            messagebox.showerror("Erreur de connexion à la base de données", res.get("error"))
            return
        if res:
            messagebox.showinfo("Succès", "Connexion réussie")
    
            role = None
            if isinstance(res, (list, tuple)) and len(res) >= 1:
                role = res[-1]
            self.root.withdraw()
            if role == "Admin":
                Admin(self.root)
            else:
                Employe(self.root,username)
        else:
            self.trycount -= 1
            if self.trycount > 0:
                self.info.configure(text=f"Nom d'utilisateur ou mot de passe incorrect.\nTentatives restantes: {self.trycount}",  text_color="red")
            else:
                messagebox.showerror("Bloqué", "Trop de tentatives")
                self.root.destroy()

    def forgot_password(self):
        if self.us.get() == "":
            messagebox.showerror("Erreur", "Veuillez entrer votre nom d'utilisateur pour réinitialiser votre mot de passe.")
            return
        else:
            try:
                conn = sqlite3.connect(chemin)
                cur = conn.cursor()
                cur.execute('SELECT username FROM users WHERE username=?', (self.us.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "Nom d'utilisateur non trouvé.")
                    
                else:
                    self.root.withdraw()
                    self.root1=Toplevel()
                    self.root1.title("Réinitialisation du mot de passe")
                    self.root1.geometry("1000x1000")

                    ctk.CTkLabel(master=self.root1, text="Nouveau mot de passe").pack(pady=10)
                    self.entry_mdp = ctk.CTkEntry(master=self.root1, show="*", placeholder_text="Entrez le nouveau mot de passe")
                    self.entry_mdp.pack(pady=10)
                    self.btn = ctk.CTkButton(master=self.root1, text="Réinitialiser", command=self.rein_mdp, font=("Times New Roman", 14),cursor="hand2")
                    self.btn.pack(pady=10)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur de connexion à la base de données", str(e))
                conn.close()

    def rein_mdp(self):
        new_password = self.entry_mdp.get()
        if new_password == "" :          
            messagebox.showerror("Erreur", "Le mot de passe ne peut pas être vide.", parent=self.root1)
            return
        try:
            conn = sqlite3.connect(chemin)
            cur = conn.cursor()
            cur.execute('UPDATE users SET password=? WHERE username=?', (new_password, self.us.get()))
            conn.commit()
            messagebox.showinfo("Succès", "Mot de passe réinitialisé avec succès.",parent=self.root1)
            self.root1.destroy()
        except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}", parent=self.root1)
        finally:
            conn.close()
        
#  ADMIN
class Admin:
    def __init__(self,root):
        self.root=Toplevel(root)
        self.root.title("ADMIN ATLAS")
        self.root.geometry("900x600")
        self.root.configure(bg=BLEU)
        self.root.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")

        Label(text="Espace Administrateur", font=("Times New Roman", 14,"bold"),bg=BLEU, fg=BLANC ).pack(pady=30)
        self.btn1=ctk.CTkButton(self.root, text="Ajouter Employé", width=28, fg_color=ORANGE, command=self.add_emp)
        self.btn1.pack(pady=10)

        self.btn2=ctk.CTkButton(self.root, text="Créer Tâche", width=28, fg_color=ORANGE, command=self.add_task)
        self.btn2.pack(pady=10)

        self.btn3=ctk.CTkButton(self.root, text="Déclarer Problème", width=28,fg_color=ORANGE, command=self.add_prob)
        self.btn3.pack(pady=10)

        self.btn4=ctk.CTkButton(self.root,text="Ajouter Administrateur", width=28,fg_color=ORANGE, command=self.add_admin)
        self.btn4.pack(pady=10)
        
        self.btn5=ctk.CTkButton(self.root, text="Ajouter un utilisateur", width=28,fg_color=ORANGE, command=self.add_user)
        self.btn5.pack(pady=10)
        

    def add_emp(self):

        self.root= Toplevel(self.root)
        self.root.title("Ajouter Employé")
        self.root.geometry("900x600")
        self.root.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")

        Label(self.root, text="Nom employé").pack()
        emp = Entry(self.root)
        emp.pack()
        Label(self.root, text="Poste").pack()
        poste = Entry(self.root)
        poste.pack()
        Label(self.root, text="Département").pack()
        dept = Entry(self.root)
        dept.pack()
        Label(self.root, text="Salaire").pack()
        salaire = Entry(self.root)
        salaire.pack()
        Label(self.root, text="Téléphone").pack()
        tel = Entry(self.root) 
        tel.pack()


        def save():
            if emp.get() == "" or poste.get() == "" or dept.get() == "" or salaire.get() == "" or tel.get() == "":
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis !")
                return
            try:
                float(salaire.get())
            except ValueError:
                messagebox.showerror("Erreur", "Le salaire doit être un nombre !")
                return

           #Vérifier que le téléphone a 10 chiffres 
            if not tel.get().isdigit() or len(tel.get()) != 10:
                messagebox.showerror("Erreur", "Le téléphone doit contenir 10 chiffres !")
                return

            conn = sqlite3.connect(chemin)
            cur = conn.cursor()
            cur.execute("INSERT INTO employes VALUES (NULL, ?, ?, ?, ?, ?)", 
                        (emp.get(), poste.get(), dept.get(), salaire.get(), tel.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("OK", "Employé ajouté")
        Button(self.root, text="Enregistrer", command=save).pack()

    def add_task(self):
        w = Toplevel(root)
        w.title("Créer Tâche")
        w.geometry("900x600")
        
        w.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")
    
        Label(w, text="Employé chargé de la tâche").pack()
        emp = Entry(w)
        emp.pack()

        Label(w, text="Titre tâche").pack()
        t = Entry(w)
        t.pack()
        Label(w, text="Statut").pack()
        s = Entry(w)
        s.pack()
        Label(w, text="Date début").pack()
        dd = Entry(w)
        dd.pack()
        Label(w, text="Date fin").pack()    
        df = Entry(w)
        df.pack()


        def save():
            conn = sqlite3.connect(chemin)
            cur = conn.cursor()
            cur.execute("INSERT INTO taches VALUES(NULL,?,?,?,?,?)", (emp.get(), t.get(), "A faire",  dd.get(), df.get()))
            if (emp.get() == "" or t.get() == ""):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                return

            conn.commit()
            conn.close()
            messagebox.showinfo("OK", "Tâche créée")
            w.destroy()

        Button(w, text="Créer", command=save).pack()

    def add_prob(self):
        w = Toplevel(root)
        w.title("Déclarer Problème")
        w.geometry("900x600")
        w.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")

        Label(w, text="Département").pack()
        d = Entry(w)
        d.pack()

        Label(w, text="Description").pack()
        password_entry = Entry(w)
        password_entry.pack()

        Label(w, text="Statut").pack()
        s = Entry(w)
        s.pack()

        Label(w, text="Date déclaration").pack()
        dd = Entry(w)
        dd.pack()

        def save():
            try:

                conn = sqlite3.connect(chemin)
                cur = conn.cursor()
                cur.execute("INSERT INTO problemes VALUES(NULL,?,?,?)", (d.get(), password_entry.get(), "Ouvert",dd.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("OK", "Problème enregistré")
                w.destroy()

            except sqlite3.OperationalError as e:
        
                messagebox.showerror("Erreur", f"Base de données verrouillée : {e}")
        
            finally:
                if 'conn' in locals():
                    conn.close()
        Button(w, text="Valider", command=save).pack()
    def add_user(self):

        w = Toplevel(root)
        w.geometry("900x600")
        w.title("Ajouter Utilisateur")
        w.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")

        Label(w, text="Nom d'utilisateur").pack()
        us = Entry(w)
        us.pack()

        Label(w, text="Mot de passe").pack()
        pw = Entry(w, show="*")
        pw.pack()

        Label(w, text="Rôle (Admin / PDG / DRH / Manager)").pack()
        r = Entry(w)
        r.pack()

        def save():
            username = us.get().strip()
            password = pw.get().strip()
            role = r.get().strip()
            if not username or not password or not role:
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return

            conn = sqlite3.connect(chemin)
            cur = conn.cursor()
            cur.execute("SELECT username FROM users WHERE username = ?", (username,))
            result = cur.fetchone()
            if result:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà")
                conn.close()
                return

            cur.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (username, password, role))
            conn.commit()  
            conn.close()
            messagebox.showinfo("OK", "Utilisateur créé")
            w.destroy()

        Button(w, text="Enregistrer", command=save).pack(pady=5)



    # ---- NOUVELLE OPTION : CREER ADMIN ----
    def add_admin(self):
        w = Toplevel(root)
        w.geometry("900x600")
        w.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")
        w.title("Ajouter Administrateur")

        Label(w, text="Nom Administrateur").pack()
        us = Entry(w)
        us.pack()

        Label(w, text="Mot de passe").pack()
        pw = Entry(w, show="*")
        pw.pack()

        Label(w, text="Rôle (PDG / DRH / Manager)").pack()
        r = Entry(w)
        r.pack()

        def save():
            nom = us.get().strip()
            mot_de_passe = pw.get().strip()
            role = r.get().strip()
            if not nom or not mot_de_passe or not role:
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return
            
            conn = sqlite3.connect(chemin)
            cur = conn.cursor()
            cur.execute("SELECT nom FROM admins WHERE nom = ?", (nom,))
            result = cur.fetchone()
            if result:
                messagebox.showerror("Erreur", "Ce nom d'administrateur existe déjà")
                return
            
            cur.execute("INSERT INTO admins (nom, mot_de_passe, role) VALUES (?,?,?)", (nom, mot_de_passe, role))
            conn.commit()  
            conn.close()
            messagebox.showinfo("OK", "Administrateur créé")
            w.destroy()

        Button(w, text="Enregistrer", command=save).pack(pady=5)


#  EMPLOYE
class Employe:
    def __init__(self,root, nom):

        self.nom = nom
        self.root = Toplevel(root)
        self.root.geometry("900x600")
        self.root.configure(bg=BLEU)
        self.root.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")
    
        self.root.title("ESPACE EMPLOYE")
        self.root.geometry("1000x1000")
        self.root.iconbitmap("D:\\Atlas_Bâtiment\\logo.ico")

        Label(text=f"Bienvenue {nom}", font=("Arial", 20),bg=BLEU, fg=BLANC).pack(pady=30)
        ctk.CTkButton(self.root, text="Voir mes tâches", fg_color=ORANGE, command=self.tasks).pack()
        

    def tasks(self):
        w = Toplevel(self.root)
        w.title("Mes Tâches")
        w.geometry("900x600")
        conn = sqlite3.connect(chemin)
        cur = conn.cursor()
        cur.execute("SELECT titre, statut, date_debut, date_fin FROM taches WHERE id_emp=?", (self.nom,))
        t = cur.fetchall()
        if not t:
            Label(w, text="Aucune tâche assignée").pack()
        else:

            for x in t:
                Label(w, text=f"{x[0]} | {x[1]} | {x[2]} | {x[3]}").pack()
            conn.close()




if __name__ == "__main__":
    # initialiser la base de données une seule fois au démarrage
    init_db()
    root = Tk()
    LoginPage(root)  
    root.mainloop()