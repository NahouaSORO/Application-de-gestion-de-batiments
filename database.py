
import sqlite3
from contextlib import contextmanager
import os

class Database:
    """Singleton pour gérer la connexion à la base de données"""
    _instance = None
    _chemin = "D:/Atlas_Bâtiment/Atlas.db"
    _callback = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
           # print(f"📍CHEMIN ABSOLU DE LA DB : {os.path.abspath(cls._chemin)}")
        return cls._instance
    
    @classmethod
    def set_callback(cls, func):
        """Permet à l'interface de définir la fonction à appeler après modification"""
        cls._callback = func

    @contextmanager
    def get_cursor(self):
        """Gestionnaire de contexte pour les requêtes SQL"""
        conn = sqlite3.connect(self._chemin)
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
            if Database._callback:
                Database._callback()
                
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        """Initialise la base de données avec toutes les tables"""
        with self.get_cursor() as cur:
            # Table users
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id_users INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT UNIQUE NOT NULL,
                    role TEXT DEFAULT 'Manager'
                )
            """)
            
            # Table admins
            cur.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id_admins INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    mot_de_passe TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            """)
            
            # Table employes
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employes (
                    id_emp INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    poste TEXT NOT NULL, 
                    id_dept INTEGER NOT NULL,
                    salaire REAL NOT NULL,
                    tel VARCHAR(15) NOT NULL
                )
            """)
            
            # Table taches
            cur.execute("""
                CREATE TABLE IF NOT EXISTS taches (
                    id_taches INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    titre TEXT NOT NULL,
                    statut TEXT DEFAULT 'A faire',
                    date_debut DATE DEFAULT (DATE('now')),
                    date_fin DATE,
                    FOREIGN KEY (nom) REFERENCES employes(nom)
                )
            """)
            
            # Table problemes
            cur.execute("""
                CREATE TABLE IF NOT EXISTS problemes (
                    id_problemes INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_dept INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    statut TEXT DEFAULT 'Ouvert',
                    date_declaration DATE DEFAULT (DATE('now')),
                    FOREIGN KEY (id_dept) REFERENCES departements(id_dept)
                )
            """)
            
            # Table departements
            cur.execute("""
                CREATE TABLE IF NOT EXISTS departements (
                    id_dept INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_dept TEXT NOT NULL
                )
            """)
            
            # Table clients
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id_clients INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    tel VARCHAR(15) NOT NULL,
                    adresse VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL
                )
            """)
            
            # Table projets
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
            
            # Table batiments
            cur.execute("""
                CREATE TABLE IF NOT EXISTS batiments (
                    id_bat INTEGER PRIMARY KEY AUTOINCREMENT,
                    type_bat TEXT NOT NULL,
                    prix REAL NOT NULL
                )
            """)
            
            # Table fournisseurs
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
            
            # Table ventes
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ventes (
                    id_ventes INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_vente DATE DEFAULT (DATE('now')),
                    montant REAL NOT NULL
                )
            """)
            
            # Table logs (pour le journal d'activité)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
                    utilisateur TEXT NOT NULL,
                    action TEXT NOT NULL,
                    date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT
                )
            """)
            #cur.execute("DELETE FROM logs")

            # Utilisateur admin par défaut (mot de passe: 1234)
            cur.execute("""
                INSERT OR REPLACE INTO users (username, password, role) 
                VALUES ('soro', '1234', 'Admin')
            """)
            # Utilisateur employe par défaut (mot de passe: 0000)
            cur.execute("""
                INSERT OR REPLACE INTO users (username, password, role) 
                VALUES ('Ali', '0000', 'Employe')
                """)
            
    
    def logger_action(self, utilisateur, action, details=""):
        """Enregistre une action dans les logs"""
        with self.get_cursor() as cur:
            cur.execute(
                "INSERT INTO logs (utilisateur, action, details) VALUES (?,?,?)",
                (utilisateur, action, details)
            )
           
    
    def get_logs(self, limit=50):
        """Récupère les derniers logs"""
        with self.get_cursor() as cur:
            cur.execute(
                "SELECT utilisateur, action, date_heure, details FROM logs ORDER BY date_heure DESC LIMIT ?",
                (limit,)
            )
            return cur.fetchall()

