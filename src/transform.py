import pandas as pd
import numpy as np

class TransformateurDeDonnees:
    """
    Contient la logique métier pour nettoyer et transformer les DataFrames bruts.
    """

    def nettoyer_donnees_joueurs(self, tableau_joueurs: pd.DataFrame) -> pd.DataFrame:
        """
        Applique les règles de nettoyage pour les données des joueurs.
        
        Règles appliquées :
        1. Suppression des doublons sur l'identifiant.
        2. Nettoyage des espaces dans les pseudos.
        3. Conversion et validation des dates d'inscription.
        4. Validation du format des emails.
        5. Gestion des valeurs nulles pour compatibilité SQL.

        Arguments:
            tableau_joueurs (pd.DataFrame): Les données brutes des joueurs.

        Retourne:
            pd.DataFrame: Les données nettoyées et prêtes pour le chargement.
        """
        # Création d'une copie de travail pour ne pas modifier l'original
        donnees_propres = tableau_joueurs.copy()
        
        # 1. Gestion des doublons d'identifiants
        donnees_propres.drop_duplicates(subset=['player_id'], keep='first', inplace=True)
        
        # 2. Nettoyage des chaînes de caractères (Surnoms)
        if 'username' in donnees_propres.columns:
            donnees_propres['username'] = donnees_propres['username'].str.strip()

        # 3. Normalisation des dates
        # 'coerce' permet de transformer les erreurs en NaT (Not a Time)
        donnees_propres['registration_date'] = pd.to_datetime(donnees_propres['registration_date'], errors='coerce')
        
        # 4. Validation des adresses email
        if 'email' in donnees_propres.columns:
            masque_email_valide = donnees_propres['email'].str.contains('@', na=False)
            donnees_propres.loc[~masque_email_valide, 'email'] = np.nan

        # 5. Gestion des valeurs manquantes (NaN -> None pour SQL)
        donnees_propres = donnees_propres.replace({np.nan: None})
        
        nombre_restant = len(donnees_propres)
        print(f"[TRANSFORMATION] Joueurs traités : {nombre_restant} profils valides conservés.")
        return donnees_propres

    def nettoyer_donnees_scores(self, tableau_scores: pd.DataFrame, liste_ids_joueurs_valides: list) -> pd.DataFrame:
        """
        Nettoie et valide les données de scores de jeu.
        
        Règles appliquées :
        1. Suppression des doublons d'identifiants de score.
        2. Conversion des types numériques et temporels.
        3. Exclusion des scores incohérents (<= 0).
        4. Vérification de l'intégrité référentielle (joueur existant).

        Arguments:
            tableau_scores (pd.DataFrame): Données brutes des scores.
            liste_ids_joueurs_valides (list): Liste des IDs de joueurs confirmés présents en base.

        Retourne:
            pd.DataFrame: Les scores validés.
        """
        donnees_scores = tableau_scores.copy()
        
        # 1. Unicité des scores
        donnees_scores.drop_duplicates(subset=['score_id'], keep='first', inplace=True)

        # 2. Conversions de types robustes
        donnees_scores['score'] = pd.to_numeric(donnees_scores['score'], errors='coerce')
        donnees_scores['duration_minutes'] = pd.to_numeric(donnees_scores['duration_minutes'], errors='coerce')
        donnees_scores['played_at'] = pd.to_datetime(donnees_scores['played_at'], errors='coerce')

        # 3. Filtrage logique (Scores positifs uniquement)
        donnees_scores = donnees_scores[donnees_scores['score'] > 0]

        # 4. Nettoyage des entrées incomplètes
        donnees_scores.dropna(subset=['score', 'player_id'], inplace=True)

        # 5. Vérification de l'intégrité référentielle (Orphelins)
        nombre_initial = len(donnees_scores)
        donnees_scores = donnees_scores[donnees_scores['player_id'].isin(liste_ids_joueurs_valides)]
        
        scores_orphelins = nombre_initial - len(donnees_scores)
        if scores_orphelins > 0:
            print(f"[TRANSFORMATION] Attention : {scores_orphelins} scores ignorés (joueur inconnu).")

        # 6. Finalisation pour SQL
        donnees_scores = donnees_scores.replace({np.nan: None})

        print(f"[TRANSFORMATION] Scores traités : {len(donnees_scores)} entrées valides conservées.")
        return donnees_scores