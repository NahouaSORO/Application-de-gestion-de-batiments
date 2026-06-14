# main.py
import customtkinter as ctk
from tkinter import Tk
from database import Database

# Configuration de l'apparence
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    # Initialiser la base de données
    db = Database()
    db.init_db()
    
    # Créer la fenêtre principale
    root = Tk()
    #root = ctk.CTk()  
    
    # Importer et lancer la page de login
    from login import LoginPage
    LoginPage(root)
    
    # Lancer l'application
    root.mainloop()