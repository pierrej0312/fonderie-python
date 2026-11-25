from sql.sql_connect import connecter_sql
from mssql_python import connect

conn = connecter_sql()
cursor = conn.cursor()
cursor.execute(
    "SELECT * FROM essais_commandes"
)
for ligne in cursor.fetchall():
    print(ligne)
cursor.close()
conn.close()