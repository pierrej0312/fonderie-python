"""Démo J3-41 et corrigé de J3-43 : lire les adresses et les secrets dans .env (à la racine du projet)."""
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("MONGO_URI"))
print(os.getenv("NEO4J_URI"))
print(os.getenv("SQL_HOTE") is not None)   # True : la chaîne existe, sans l'afficher
