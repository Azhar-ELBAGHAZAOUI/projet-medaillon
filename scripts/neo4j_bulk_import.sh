#!/bin/bash
set -e  # Arrête le script dès qu’une commande échoue

SILVER_DIR="./data/silver" # Dossier source Parquet
GOLD_DIR="./data/gold"     # Dossier cible CSV

# Convertir les fichiers Parquet Silver en CSV 
python3 - <<END
import pandas as pd
import os

silver_dir = "$SILVER_DIR"
gold_dir = "$GOLD_DIR"

# Crée le dossier gold s'il n'existe pas
os.makedirs(gold_dir, exist_ok=True)

#Export des nodes
nodes_file = os.path.join(silver_dir, "nodes.parquet")
nodes_df = pd.read_parquet(nodes_file)

# Renommer les colonnes 
nodes_df = nodes_df.rename(columns={"id":"id:ID","name":"name","label":"label"})

# Sauvegarde en CSV
nodes_csv_file = os.path.join(gold_dir, "nodes.csv")
nodes_df.to_csv(nodes_csv_file, index=False)
print("Nodes exportés")

# Export des edges (8 shards)
for shard in range(8):
    edges_file = os.path.join(silver_dir, f"shard={shard}", "edges.parquet")
    edges_df = pd.read_parquet(edges_file)

    # Renommer les colonnes de connexion
    edges_df = edges_df.rename(columns={"src":":START_ID","dst":":END_ID"})

    # Sauvegarde en CSV
    edges_csv_file = os.path.join(gold_dir, f"edges_shard{shard}.csv")
    edges_df.to_csv(edges_csv_file, index=False)
print("Edges shard exportés")
END


# COPIE DES CSV DANS LE CONTENEUR Neo4j
docker cp $GOLD_DIR/. neo4j:/var/lib/neo4j/import
docker exec neo4j rm -rf /data/databases/neo4j /data/transactions/neo4j
docker restart neo4j
sleep 10  # Attendre que Neo4j soit prêt

# INSERTION VIA CYPHER
# Import des nœuds
docker exec -i neo4j cypher-shell <<EOF
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
CREATE (n:Entity {
    id: row["id:ID"],
    name: row.name,
    type: row.label
});
EOF
echo "Nœuds importés"

# Import des relations
for shard in {0..7}; do
    EDGE_FILE="file:///edges_shard${shard}.csv"
    docker exec -i neo4j cypher-shell <<EOF
LOAD CSV WITH HEADERS FROM '$EDGE_FILE' AS row
MATCH (a:Entity {id: row[":START_ID"]})
MATCH (b:Entity {id: row[":END_ID"]})
CREATE (a)-[r:RELATED_TO]->(b);
EOF
done
echo "Relations importées"
