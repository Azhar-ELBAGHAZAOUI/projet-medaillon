import pandas as pd
import sys
import os

# chemins des fichiers Bronze
BRONZE_DIR = "data/bronze"
nodes_parquet = os.path.join(BRONZE_DIR, "nodes.parquet")
edges_parquet = os.path.join(BRONZE_DIR, "edges.parquet")

#Vérification des nodes
nodes_df = pd.read_parquet(nodes_parquet)

# Vérifier que tous les id sont uniques
if nodes_df['id'].duplicated().any():
    print("IDs dupliqués trouvés dans nodes")
    sys.exit(1)  
else:
    print("Node IDs uniques")

# Vérification des edges
edges_df = pd.read_parquet(edges_parquet)

# Vérifier qu'il n'y a pas de null dans src ou dst
if edges_df[['src', 'dst']].isnull().any().any():
    print("Valeurs null trouvées dans src/dst des edges!")
    sys.exit(1)
else:
    print("Edges sans nulls dans src/dst")
