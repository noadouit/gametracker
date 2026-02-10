#!/bin/bash
set -e

host="${DB_HOST:-db}"
user="${DB_USER:-root}"
password="${DB_PASSWORD:-root}"

echo "En attente de MySQL ($host)..."

# Boucle de 30 tentatives (Exigence du sujet)
for i in {1..30}; do
  # L'option --skip-ssl est vitale pour ton environnement Docker
  if mysql -h "$host" -u "$user" -p"$password" --skip-ssl -e 'SELECT 1' > /dev/null 2>&1; then
    echo "MySQL est prêt !"
    exit 0
  fi
  echo "Tentative $i/30..."
  sleep 2
done

echo "Erreur : Timeout connexion MySQL."
exit 1