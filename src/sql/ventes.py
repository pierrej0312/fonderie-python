# Script généré par une IA à la demande d'un stagiaire :
# « écris un script Python qui affiche les ventes d'un client dans ma base SQL Server Fonderie »
from sql_connect import connecter_sql

try:
    conn = connecter_sql()
except Exception as e:
    print("Connexion impossible :", e)
else:
    try:
        cursor = conn.cursor()
        code = input("Code du client : ")
        cursor.execute(
            "SELECT date_vente, biere, format, quantite "
            "FROM ventes "
            "WHERE client = %(code)s "
            "ORDER BY date_vente", 
            {"code": code}
        )
        rows = cursor.fetchall()
        for ligne in rows:
            print(ligne.date_vente, ligne.biere, ligne.format, ligne.quantite)
        print(len(rows))
        cursor.close()
    finally:
        conn.close()
finally:
    print("aurevoir")