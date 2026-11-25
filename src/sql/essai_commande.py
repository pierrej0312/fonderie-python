from sql_connect import connecter_sql
from mssql_python import connect

conn = connecter_sql()
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO essais_commandes (poste, biere, quantite) "
    'VALUES (%(poste)s, %(biere)s, %(quantite)s)',
    {"poste": "Poste 07", "biere": "B03", "quantite": 2}
)
conn.commit()
cursor.close()
conn.close()