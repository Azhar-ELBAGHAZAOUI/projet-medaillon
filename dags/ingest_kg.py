from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta

import os

BASE_DIR = "/opt/airflow"
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Arguments par défaut du DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

# Définition du DAG
with DAG(
    dag_id="ingest_kg_make",               
    description="Pipeline d’ingestion via Makefile",
    start_date=datetime(2025, 10, 23),      # Date de début du DAG
    schedule=None,                           # Lancement manuel
    catchup=False,                          
    default_args=default_args,               
    tags=["pipeline"],                       
) as dag:

    seed_task = BashOperator(
        task_id="seed",
        bash_command=f"make -C {BASE_DIR} seed" # Exécute `make seed` dans le répertoire du projet
    )

    bronze_task = BashOperator(
        task_id="bronze",
        bash_command=f"make -C {BASE_DIR} bronze"
    )

    silver_task = BashOperator(
        task_id="silver",
        bash_command=f"make -C {BASE_DIR} silver"
    )

    gold_task = BashOperator(
        task_id="gold",
        bash_command=f"make -C {BASE_DIR} import",
        execution_timeout=timedelta(minutes=30) 
    )

# Pipeline : seed -> bronze -> silver -> gold
    seed_task >> bronze_task >> silver_task >> gold_task
