# quality/gx_checkpoint.py

import great_expectations as gx
import pandas as pd
from pathlib import Path

#  Charger les données Silver
BRONZE_DIR = Path("data/bronze")

nodes_path = BRONZE_DIR / "nodes.parquet"
edges_path = BRONZE_DIR / "edges.parquet"

nodes_df = pd.read_parquet(nodes_path)
edges_df = pd.read_parquet(edges_path)

context = gx.get_context()

data_source = context.data_sources.add_pandas("bronze_source")

# Créer deux Data Assets : nodes et edges
nodes_asset = data_source.add_dataframe_asset(name="nodes_asset")
edges_asset = data_source.add_dataframe_asset(name="edges_asset")

# Créer les Batch Definitions et Batches
nodes_batch_def = nodes_asset.add_batch_definition_whole_dataframe("nodes_batch_def")
edges_batch_def = edges_asset.add_batch_definition_whole_dataframe("edges_batch_def")

nodes_batch = nodes_batch_def.get_batch(batch_parameters={"dataframe": nodes_df})
edges_batch = edges_batch_def.get_batch(batch_parameters={"dataframe": edges_df})

# Définir les attentes
# id doit être unique et non nul
expect_unique_id = gx.expectations.ExpectColumnValuesToBeUnique(column="id", severity="critical")
expect_not_null_id = gx.expectations.ExpectColumnValuesToNotBeNull(column="id", severity="critical")

# src et dst ne doivent pas être nuls
expect_not_null_src = gx.expectations.ExpectColumnValuesToNotBeNull(column="src", severity="critical")
expect_not_null_dst = gx.expectations.ExpectColumnValuesToNotBeNull(column="dst", severity="critical")

#  Valider les données
validation_nodes_id_unique = nodes_batch.validate(expect_unique_id)
validation_nodes_not_null = nodes_batch.validate(expect_not_null_id)

validation_edges_src_not_null = edges_batch.validate(expect_not_null_src)
validation_edges_dst_not_null = edges_batch.validate(expect_not_null_dst)

# Afficher les résultats
print('Résultat test id unique : ', validation_nodes_id_unique.success)
print('Résultat test id not null : ', validation_nodes_not_null.success)
print('Résultat test src not null : ', validation_edges_src_not_null.success)
print('Résultat test dst not null : ', validation_edges_dst_not_null.success)