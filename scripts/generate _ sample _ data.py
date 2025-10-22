import pandas as pd
import numpy as np
import os

RAW_DIR = "data/raw"

# Crée le dossier s'il n'existe pas
os.makedirs(RAW_DIR, exist_ok=True)

# Paramètres
NUM_NODES = 1_000
NUM_EDGES = 5_000

# Labels possibles pour les nœuds
LABELS = ["Person", "Org", "Paper"]

# Génération nodes
nodes = pd.DataFrame({
    "id": np.arange(NUM_NODES),
    "label": np.random.choice(LABELS, size=NUM_NODES),
    "name": ["name_" + str(i) for i in range(NUM_NODES)]
})

nodes.to_csv(os.path.join(RAW_DIR, "nodes.csv"), index=False)

# Génération edges
edges = pd.DataFrame({
    "src": np.random.randint(0, NUM_NODES, size=NUM_EDGES),
    "dst": np.random.randint(0, NUM_NODES, size=NUM_EDGES),
    "type": "REL"
})

edges.to_csv(os.path.join(RAW_DIR, "edges.csv"), index=False)