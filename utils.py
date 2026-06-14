# utils.py
import bcrypt
import re

# ===== COULEURS =====
ORANGE = "#ff7a00"
BLEU = "#0f2a44"
BLANC = "#ffffff"

# ===== CHEMINS =====
chemin_db = "D:/Atlas_Bâtiment/Atlas.db"
chemin_logo = "D:/Atlas_Bâtiment/logo.ico"

# ===== VALIDATION DES INPUTS =====
def valider_email(email: str) -> bool:
    """Valide un format d'email"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def valider_telephone(tel: str) -> bool:
    """Valide un numéro de téléphone (10 chiffres)"""
    return tel.isdigit() and len(tel) == 10

def valider_mot_de_passe(mdp: str) -> tuple:
    """
    Valide la force d'un mot de passe
    Retourne (bool, message)
    """
    if len(mdp) < 4:
        return False, "Le mot de passe doit contenir au moins 3 caractères"
    #if not re.search(r'[A-Z]', mdp):
        #return False, "Le mot de passe doit contenir au moins une majuscule"
    if not re.search(r'[0-9]', mdp):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    return True, "Mot de passe valide"

# ===== JOURNALISATION =====
def logger(db, utilisateur, action, details=""):
    """Fonction raccourcie pour logger une action"""
    db.logger_action(utilisateur, action, details)