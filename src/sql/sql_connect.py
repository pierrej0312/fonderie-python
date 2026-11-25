import os
from dotenv import load_dotenv
from mssql_python import connect

def connecter_sql():
    """Connexion à SQL Server"""
    load_dotenv()

    manquantes = [nom for nom in ("SQL_BASE", "SQL_LOGIN", "SQL_MDP") if not os.getenv(nom)]
    if manquantes:
        raise ValueError(f"Variables absentes du fichier .env : {', '.join(manquantes)}")

    serveur = os.getenv("SQL_HOTE", "localhost")
    instance = os.getenv("SQL_INSTANCE")
    if instance:                      # vide pour l'instance par défaut (MSSQLSERVER)
        serveur += "\\" + instance

    return connect(
        f"Server={serveur};Database={os.getenv('SQL_BASE')};"
        f"UID={os.getenv('SQL_LOGIN')};PWD={os.getenv('SQL_MDP')};"
        "Encrypt=yes;TrustServerCertificate=yes"
    )
    
if __name__ == "__main__":
    conn = connecter_sql()
    print("Connexion SQL Server réussie")
    conn.close()