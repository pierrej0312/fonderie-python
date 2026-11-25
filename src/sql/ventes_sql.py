from sql.sql_connect import connecter_sql
from mssql_python import connect

conn = connecter_sql()
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