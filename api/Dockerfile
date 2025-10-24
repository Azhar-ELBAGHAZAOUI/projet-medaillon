FROM python:3.10-slim
# Répertoire de travail à l'intérieur du conteneur
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copier le code source de l’API
COPY . .
#Exposer le port sur lequel tourne FastAPI
EXPOSE 8000
# Commande de démarrage du serveur Uvicorn
# Uvicorn lance l'application FastAPI définie dans main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
