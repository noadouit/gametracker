import mysql.connector

class ChargeurDeDonnees:
    """
    Gère le chargement (insertion et mise à jour) des données transformées vers MySQL.
    Utilise la stratégie 'ON DUPLICATE KEY UPDATE' (Upsert) pour gérer les conflits.
    """

    def charger_liste_joueurs(self, dataframe_joueurs, connexion_bdd):
        """
        Insère ou met à jour les enregistrements des joueurs dans la base de données.
        
        Arguments:
            dataframe_joueurs (pd.DataFrame): Données nettoyées des joueurs.
            connexion_bdd: Objet de connexion MySQL actif.
        """
        curseur = connexion_bdd.cursor()
        
        requete_sql = """
        INSERT INTO players (player_id, username, email, registration_date, country, level)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            username = VALUES(username),
            email = VALUES(email),
            country = VALUES(country),
            level = VALUES(level);
        """
        
        # Conversion du DataFrame en liste de tuples pour l'insertion par lot
        donnees_a_inserer = []
        for _, ligne in dataframe_joueurs.iterrows():
            donnees_a_inserer.append((
                ligne['player_id'], 
                ligne['username'], 
                ligne['email'], 
                ligne['registration_date'], 
                ligne['country'], 
                ligne['level']
            ))
        
        curseur.executemany(requete_sql, donnees_a_inserer)
        print(f"[CHARGEMENT] Succès : {curseur.rowcount} opérations sur la table 'players'.")

    def charger_liste_scores(self, dataframe_scores, connexion_bdd):
        """
        Insère ou met à jour les scores de jeu dans la base de données.
        
        Arguments:
            dataframe_scores (pd.DataFrame): Données nettoyées des scores.
            connexion_bdd: Objet de connexion MySQL actif.
        """
        curseur = connexion_bdd.cursor()
        
        requete_sql = """
        INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            score = VALUES(score),
            duration_minutes = VALUES(duration_minutes),
            platform = VALUES(platform);
        """
        
        donnees_a_inserer = []
        for _, ligne in dataframe_scores.iterrows():
            donnees_a_inserer.append((
                ligne['score_id'], 
                ligne['player_id'], 
                ligne['game'], 
                ligne['score'], 
                ligne['duration_minutes'], 
                ligne['played_at'], 
                ligne['platform']
            ))
        
        curseur.executemany(requete_sql, donnees_a_inserer)
        print(f"[CHARGEMENT] Succès : {curseur.rowcount} opérations sur la table 'scores'.")
