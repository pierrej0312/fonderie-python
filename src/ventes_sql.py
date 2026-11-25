import os 
from dotenv import load_dotenv
from mssql_python import connect

load_dotenv()
serveur = os.getenv("SQL_HOTE")
if os.getenv("SQL_INSTANCE"):
    serveur += "\\" + os.getenv("SQL_INSTANCE")
    
conn = connect(
    f"Server={serveur};Database={os.getenv("SQL_BASE")};"
    f"UID={os.getenv("SQL_LOGIN")};PWD={os.getenv("SQL_MDP")};"
    f"Encrypt=yes;TrustServerCertificate=yes"
)
format = "fut"
cursor = conn.cursor()
cursor.execute(
        "SELECT biere, SUM(quantite) as total "
        "FROM ventes "
        "WHERE format= %(format)s GROUP BY biere " 
        "ORDER BY SUM(quantite)",
        {"format": format}
)
for ligne in cursor.fetchall():
    print(ligne.biere, ligne.total)
cursor.close()
conn.close()