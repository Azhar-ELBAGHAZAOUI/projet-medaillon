seed:
python3 scripts/generate
_
sample
_
data.py --out data/raw --nodes 1000000 --edges
5000000
bronze:
python3 scripts/to
_parquet.py --in data/raw --out data/bronze
silver:
python3 scripts/partition
_
edges.py --in data/bronze --out data/silver --partitions 8
import:
bash scripts/neo4j_
bulk
_
import.sh
up:
docker compose up -d
down:
docker compose down -v
e2e:
seed bronze silver import