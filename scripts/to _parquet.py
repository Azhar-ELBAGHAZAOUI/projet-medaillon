import pandas as pd
import os

RAW_DIR = "data/raw"        
BRONZE_DIR = "data/bronze"  

# Conversion des nodes
nodes_csv = os.path.join(RAW_DIR, "nodes.csv")       
nodes_parquet = os.path.join(BRONZE_DIR, "nodes.parquet")  

# Lire en df
nodes_df = pd.read_csv(nodes_csv)

# Convertir en Parquet compressé (snappy)
nodes_df.to_parquet(
    nodes_parquet,
    index=False,        
    engine='pyarrow',   
    compression='snappy'  
)


# Conversion des edges
edges_csv = os.path.join(RAW_DIR, "edges.csv")      
edges_parquet = os.path.join(BRONZE_DIR, "edges.parquet")  

# Lire le CSV en df 
edges_df = pd.read_csv(edges_csv)

# Convertir en Parquet compressé 
edges_df.to_parquet(
    edges_parquet,
    index=False,
    engine='pyarrow',
    compression='snappy'
)

