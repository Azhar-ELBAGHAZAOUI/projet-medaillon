import pandas as pd
import os
import shutil


BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"

#Lire les fichiers bronze
edges_df = pd.read_parquet(os.path.join(BRONZE_DIR, "edges.parquet"))
nodes_df = pd.read_parquet(os.path.join(BRONZE_DIR, "nodes.parquet"))

# Partitionner les edges en 8 shards
NUM_SHARDS = 8

for shard_id in range(NUM_SHARDS):
    # Créer le dossier pour le shard
    shard_dir = os.path.join(SILVER_DIR, f"shard={shard_id}")
    os.makedirs(shard_dir, exist_ok=True)
    
    # Sélection des edges correspondant au shard 
    shard_edges = edges_df.iloc[shard_id::NUM_SHARDS]  # prend un edge sur 8 pour ce shard
    
    # Sauvegarde en Parquet
    shard_edges.to_parquet(
        os.path.join(shard_dir, "edges.parquet"),
        index=False,
        engine='pyarrow',
        compression='snappy'
    )

# Copier nodes.parquet tel quel dans Silver
shutil.copy(
    os.path.join(BRONZE_DIR, "nodes.parquet"),
    os.path.join(SILVER_DIR, "nodes.parquet")
)
