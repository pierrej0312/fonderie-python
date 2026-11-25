import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

def connecter_neo4j():
    """Connecter neo4j"""
    load_dotenv()
    
    manquantes = [nom for nom in ("NEO4J_URI", "NEO4J_login", "NEO4J_MDP") if not os.getenv(nom)]
    if manquantes:
        raise ValueError(f"Variables absentes du fichier .env : {', '.join(manquantes)}")
    uri = os.getenv("NEO4J_URI")
    auth = (os.getenv("NEO4J_login"), os.getenv("NEO4J_MDP"))
    return GraphDatabase.driver(uri, auth=auth)

if __name__ == "__main__":
    with connecter_neo4j() as driver:
        driver.verify_connectivity()
        print("Connexion à neo4j réussie")