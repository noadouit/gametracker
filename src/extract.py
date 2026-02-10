import pandas as pd
import os
import sys

class ExtracteurDeDonnees:
    """
    Responsable de l'extraction des données brutes depuis des fichiers sources CSV.
    """

    def extraire_depuis_csv(self, chemin_fichier_source: str) -> pd.DataFrame:
        """
        Lit un fichier CSV et le convertit en DataFrame pandas.
        
        Arguments:
            chemin_fichier_source (str): Le chemin absolu ou relatif vers le fichier CSV.

        Retourne:
            pd.DataFrame: Les données brutes extraites du fichier.

        Lève:
            SystemExit: Si le fichier n'existe pas ou est illisible (arrêt critique).
        """
        if not os.path.exists(chemin_fichier_source):
            print(f"[ERREUR CRITIQUE] Le fichier source est introuvable : {chemin_fichier_source}")
            sys.exit(1)

        try:
            tableau_donnees = pd.read_csv(chemin_fichier_source)
            lignes, colonnes = tableau_donnees.shape
            print(f"[EXTRACTION] Succès : {lignes} lignes chargées depuis {os.path.basename(chemin_fichier_source)}.")
            return tableau_donnees
        except Exception as erreur:
            print(f"[ERREUR CRITIQUE] Échec de lecture du CSV {chemin_fichier_source} : {erreur}")
            sys.exit(1)
