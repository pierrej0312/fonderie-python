from connect_neo4j import connecter_neo4j

with connecter_neo4j() as driver:
    driver.verify_connectivity()
    records, summary, keys = driver.execute_query(
        "MATCH (c:Client {ville: $ville})<-[r:LIVRE]-(l:Livraison) "
        "RETURN c.nom AS nom, count(l) AS nb_livraison",
        ville="Seraing", database_="neo4j"
    )
    for r in records:
        print(r["nom"], r["nb_livraison"])