import mysql.connector
from mysql.connector import Error
import time
from contextlib import contextmanager
from src.config import Config

class GestionnaireBaseDeDonnees:
    """
    Gère les connexions et les interactions avec la base de données MySQL.
    
    Cette classe encapsule la logique de connexion, y compris les mécanismes de
    nouvelle tentative (retry) pour assurer la résilience au démarrage des conteneurs.
    """

    def __init__(self):
        """Initialise les paramètres de configuration de la base de données."""
        self.hote = Config.DB_HOST
        self.port = Config.DB_PORT
        self.base_de_donnees = Config.DB_NAME
        self.utilisateur = Config.DB_USER
        self.mot_de_passe = Config.DB_PASSWORD

    def _creer_connexion(self):
        """
        Crée une nouvelle connexion brute à la base de données.
        
        Retourne:
            mysql.connector.connection.MySQLConnection: L'objet de connexion.
        """
        return mysql.connector.connect(
            host=self.hote,
            port=self.port,
            database=self.base_de_donnees,
            user=self.utilisateur,
            password=self.mot_de_passe
        )

    def obtenir_connexion_avec_tentative(self, tentatives_max=30, delai=2):
        """
        Tente d'établir une connexion à la base de données avec plusieurs essais.
        
        Cette méthode est cruciale pour l'orchestration Docker, car la base de données
        peut ne pas être prête immédiatement au lancement du script.

        Arguments:
            tentatives_max (int): Nombre maximum d'essais de connexion.
            delai (int): Temps d'attente en secondes entre chaque essai.

        Retourne:
            mysql.connector.connection.MySQLConnection: Une connexion active si réussie.

        Lève:
            Exception: Si aucune connexion n'est possible après le nombre max d'essais.
        """
        for essai in range(tentatives_max):
            try:
                connexion = self._creer_connexion()
                if connexion.is_connected():
                    print(f"[BDD] Connexion établie avec succès.")
                    return connexion
            except Error as erreur:
                print(f"[BDD] En attente du service MySQL (Essai {essai+1}/{tentatives_max})...")
                time.sleep(delai)
        
        raise Exception("[ERREUR FATALE] Impossible de se connecter à la base de données après plusieurs tentatives.")

    @contextmanager
    def session_base_de_donnees(self):
        """
        Gestionnaire de contexte pour une session de base de données sécurisée.
        
        Garantit que la connexion est fermée proprement et que les transactions
        sont validées (commit) ou annulées (rollback) en cas d'erreur.

        Yields:
            mysql.connector.connection.MySQLConnection: La connexion active.
        """
        connexion = self.obtenir_connexion_avec_tentative()
        try:
            yield connexion
            connexion.commit()
        except Exception as e:
            connexion.rollback()
            print(f"[BDD] Erreur de transaction, annulation (rollback) effectuée : {e}")
            raise e
        finally:
            if connexion.is_connected():
                connexion.close()
                # print("[BDD] Connexion fermée.") # Optionnel pour ne pas polluer les logs

# Instance globale pour utilisation simplifiée (optionnel, mais pratique pour la compatibilité)
gestionnaire_bdd = GestionnaireBaseDeDonnees()
database_connection = gestionnaire_bdd.session_base_de_donnees
