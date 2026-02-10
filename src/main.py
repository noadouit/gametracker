from src.config import Config
from src.database import database_connection
from src.extract import ExtracteurDeDonnees
from src.transform import TransformateurDeDonnees
from src.load import ChargeurDeDonnees
from src.report import GenerateurDeRapport
import os

def orchestrer_pipeline_etl():
    """
    Fonction principale d'orchestration du flux de données GameTracker.
    Coordonne l'extraction, la transformation, le chargement et le reporting.
    """
    print("@" * 60)
    print("   LANCEMENT DU SYSTEME DE TRAITEMENT DE DONNEES GAMETRACKER")
    print("@" * 60)
    
    # Instanciation des services
    service_extraction = ExtracteurDeDonnees()
    service_transformation = TransformateurDeDonnees()
    service_chargement = ChargeurDeDonnees()
    service_rapport = GenerateurDeRapport()

    # Définition des chemins de fichiers
    chemin_fichier_joueurs = os.path.join(Config.DATA_DIR, 'Players.csv')
    chemin_fichier_scores = os.path.join(Config.DATA_DIR, 'Scores.csv')

    # Utilisation du gestionnaire de contexte pour la connexion DB
    with database_connection() as connexion_active:
        
        # --- ETAPE 1 : TRAITEMENT DES JOUEURS ---
        print("\n>>> ETAPE 1/3 : Importation des profils joueurs")
        donnees_brutes_joueurs = service_extraction.extraire_depuis_csv(chemin_fichier_joueurs)
        joueurs_propres = service_transformation.nettoyer_donnees_joueurs(donnees_brutes_joueurs)
        service_chargement.charger_liste_joueurs(joueurs_propres, connexion_active)
        
        # Extraction des IDs valides pour référence future
        liste_ids_joueurs = joueurs_propres['player_id'].tolist()
        
        # --- ETAPE 2 : TRAITEMENT DES SCORES ---
        print("\n>>> ETAPE 2/3 : Importation des historiques de jeu")
        donnees_brutes_scores = service_extraction.extraire_depuis_csv(chemin_fichier_scores)
        # Injection des IDs valides pour le nettoyage
        scores_propres = service_transformation.nettoyer_donnees_scores(donnees_brutes_scores, liste_ids_joueurs)
        service_chargement.charger_liste_scores(scores_propres, connexion_active)
        
    # --- ETAPE 3 : GENERATION RAPPORT ---
    # Hors du bloc 'with' car le rapport gère sa propre connexion de lecture
    print("\n>>> ETAPE 3/3 : Synthèse et Reporting")
    service_rapport.construire_rapport_final()
    
    print("\n" + "@" * 60)
    print("   PROCESSUS TERMINE AVEC SUCCES - BASE A JOUR")
    print("@" * 60)

if __name__ == "__main__":
    orchestrer_pipeline_etl()
