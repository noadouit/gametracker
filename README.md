🎮 GameTracker : Pipeline ETL Automatisé
Python Docker MySQL

Ce projet déploie une solution robuste d'intégration de données (ETL) conçue pour l'analyse des performances de joueurs de jeux vidéo. L'architecture permet l'extraction de données CSV, un nettoyage rigoureux, le stockage dans une base MySQL et la génération automatique d'un bilan statistique, le tout orchestré via Docker.

🛠️ Configuration Requise
Avant de commencer, assurez-vous d'avoir :

Docker et Docker Compose installés et fonctionnels.
Les sources de données présentes : data/raw/Players.csv et data/raw/Scores.csv.
🚀 Guide de Démarrage
1. Initialisation de l'infrastructure
La commande suivante construit l'image, lance la base de données et exécute le pipeline automatiquement une première fois au démarrage.

docker compose up -d --build
2. Relancer le Pipeline (Mode Manuel)
Si vous modifiez les fichiers CSV ou souhaitez régénérer le rapport sans redémarrer les conteneurs, utilisez cette commande :

Bash
docker compose exec app ./scripts/run_pipeline.sh
Résultat : Le rapport statistique est généré dans le fichier : output/rapport.txt.

📂 Organisation du Répertoire
Plaintext
gametracker/
├── docker-compose.yml     # Orchestration des services
├── Dockerfile             # Image Python
├── requirements.txt       # Dépendances Python
├── .gitignore             # Fichiers ignorés par Git
├── README.md              # Documentation
├── data/
│   └── raw/
│       ├── Players.csv    # Données brutes Joueurs
│       └── Scores.csv     # Données brutes Scores
├── scripts/
│   ├── init-db.sql        # Création des tables SQL
│   ├── wait-for-db.sh     # Script d'attente BDD
│   └── run_pipeline.sh    # Script lanceur global
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration (Env vars)
│   ├── database.py        # Gestion connexion BDD
│   ├── extract.py         # Module d'extraction
│   ├── transform.py       # Module de nettoyage
│   ├── load.py            # Module d'insertion SQL
│   ├── report.py          # Générateur de rapport
│   └── main.py            # Point d'entrée principal
└── output/
    └── (rapports générés ici)
🧹 Traitement et Nettoyage des Données
Le module de transformation (src/transform.py) garantit l'intégrité des données via 7 règles d'assainissement :

Gestion des doublons : Élimination des entrées redondantes (Joueurs & Scores).

Validation des courriels : Identification des formats invalides (absence de @) convertis en NULL.

Normalisation temporelle : Standardisation des formats de dates ISO.

Nettoyage textuel : Suppression des espaces parasites (trimming) sur les pseudos.

Filtrage des anomalies : Exclusion automatique des scores négatifs ou nuls.

Gestion des manques : Conversion des valeurs NaN pour assurer la stabilité SQL.

Contrôle de cohérence : Suppression des scores "orphelins" liés à des joueurs inexistants.