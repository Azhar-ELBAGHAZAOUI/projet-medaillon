# Graph Pipeline - Médaillon Architecture

## Objectif

Implémenter une pipeline de données complète suivant l'architecture **médaillon** (Bronze / Silver / Gold) pour ingérer et traiter un **graphe de connaissances ** à grande échelle.



## Contexte : Architecture Médaillon

| Couche | Description | Format | Exemple |
|--------|------------|--------|---------|
| 🥉 Bronze | Données brutes, non transformées | Parquet | CSV → Parquet (nodes, edges) |
| 🥈 Silver | Données nettoyées, validées, partitionnées | Parquet | Partitions par shard, qualité validée |
| 🥇 Gold | Données prêtes pour la consommation | CSV / Neo4j | Import dans Neo4j, API exposée |

---

## Stack Technique

| Outil | Rôle | Port |
|-------|------|------|
| Neo4j | Base de données graphe | 7474 (UI), 7687 (Bolt) |
| Apache Airflow | Orchestration des pipelines | 8080 |
| Marquez | Traçabilité (lineage) | 5000 |
| Prometheus | Collecte de métriques | 9090 |
| Grafana | Visualisation des métriques | 3000 |
| FastAPI | API REST | 8000 |

---


## Détails des dossiers

- **docker-compose.yaml** : configuration des services Docker (Neo4j, Airflow, API) et variables d’environnement.  
- **Makefile** : commandes pratiques pour lancer les services (`make up`) ou générer les données (`make seed`).  
- **api/** : code de l’API FastAPI. Contient `main.py` (endpoints), `requirements.txt` (dépendances) et `Dockerfile`.  
- **dags/** : DAGs Airflow pour orchestrer la pipeline (Bronze → Silver → Gold).  
- **data/** : stockage des données selon les couches :  
  - `raw/` : CSV bruts  
  - `bronze/` : Parquet brut  
  - `silver/` : Parquet partitionné  
  - `gold/` : CSV final pour Neo4j  
- **scripts/** : scripts de génération et transformation des données (`generate_sample_data.py`, `to_parquet.py`, `partition_edges.py`, `neo4j_bulk_import.sh`).  
- **quality/** : validation des données avec Great Expectations (`gx_checkpoint.py`).  
- **schema/**  
- **lineage/** 
- **grafana/** 

💡 **Flux des données** :  
1. Données synthétiques → `data/raw/`  
2. Bronze : CSV → Parquet + validation → `data/bronze/`  
3. Silver : Partitionnement → `data/silver/`  
4. Gold : Préparation CSV + import Neo4j → `data/gold/`  
5. API FastAPI expose les données  

---

## Installation & Exécution

### Prérequis

- Docker  
- Docker Compose  
- Git  
- Python 3.10+  

### Installation

```bash
git clone https://votre-repo-github/knowledge-graph-pipeline.git
make up
```
### Services accessibles :
Neo4j : http://localhost:7474
Airflow : http://localhost:8080
Accès API: http://localhost:8000


## Auteur

**Nom Prénom**  
- GitHub : [Azhar-ELBAGHAZAOUI](https://github.com/Azhar-ELBAGHAZAOUI)  