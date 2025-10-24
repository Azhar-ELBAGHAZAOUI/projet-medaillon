import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase

# Récupérer l'URI Neo4j depuis les variables d'environnement
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
# Initialiser le driver Neo4j sans authentification
driver = GraphDatabase.driver(NEO4J_URI, auth=None)
# Créer l'application FastAPI
app = FastAPI(title="API Graph médaillon", version="1.0")

# Modèle pour requête Cypher
class CypherQuery(BaseModel):
    query: str

# Endpoint pour exécuter requête Cypher
@app.post("/query/cypher")
def query_cypher(query: CypherQuery):
    """
    Exécute une requête Cypher et retourne les résultats
    """
    try:
        with driver.session() as session:
            result = session.run(query.query)
            return [dict(record) for record in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour récupérer un nœud et ses voisins
@app.get("/entity/{id}")
def get_entity(id: int):
    """
    Retourne un nœud et ses relations limit 25
    """
    cypher_query = f"""
    MATCH (n)-[r]-(m)
    WHERE id(n) = {id}
    RETURN n, r, m
    LIMIT 25
    """
    try:
        with driver.session() as session:
            result = session.run(cypher_query)
            return [dict(record) for record in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
