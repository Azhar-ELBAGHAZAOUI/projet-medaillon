FROM apache/airflow:3.1.0

USER root
#Installer make dans le conteneur Airflow
RUN apt-get update && apt-get install -y make 
RUN pip install fastapi uvicorn[standard]
USER airflow
