# Image de base demandée 
FROM python:3.11-slim

# Installation du client MySQL (nécessaire pour le futur script wait-for-db.sh) 
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie et installation des dépendances 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le code source 
COPY . .

# Rendre les scripts exécutables (Bonne pratique Linux)
RUN chmod +x scripts/*.sh

# Commande par défaut (Garde le conteneur en vie)
CMD ["bash"]