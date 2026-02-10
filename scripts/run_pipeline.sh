#!/bin/bash
set -e

echo "=== GAMETRACKER PIPELINE ==="

# 1. Attente BDD
./scripts/wait-for-db.sh

# 2. Initialisation BDD
echo "[AUTO] Initialisation des tables..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" --skip-ssl "$DB_NAME" < scripts/init-db.sql

# 3. Lancement Python (C'est la ligne qu'on active !)
echo "[AUTO] Lancement du traitement Python (ETL)..."
python -m src.main