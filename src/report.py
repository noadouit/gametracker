from src.database import database_connection
from datetime import datetime

class GenerateurDeRapport:
    """
    Classe utilitaire pour la génération de rapports statistiques basés sur les données SQL.
    """

    def construire_rapport_final(self):
        """
        Interroge la base de données et écrit un rapport de synthèse formatté.
        Le fichier de sortie est écrasé à chaque exécution.
        """
        chemin_fichier_sortie = "/app/output/rapport.txt"
        
        print(f"[RAPPORT] Initialisation de l'écriture vers {chemin_fichier_sortie}...")
        
        with database_connection() as connexion:
            curseur = connexion.cursor()
            
            with open(chemin_fichier_sortie, 'w', encoding='utf-8') as fichier:
                # --- EN-TÊTE STYLISÉ ---
                date_actuelle = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                
                fichier.write("#" * 60 + "\n")
                fichier.write(f"# {'METRIQUES GAMETRACKER - ANALYSE DETAILLEE':^56} #\n")
                fichier.write(f"# {date_actuelle:^56} #\n")
                fichier.write("#" * 60 + "\n\n")
                
                # --- 1. INDICATEURS CLÉS (KPI) ---
                curseur.execute("SELECT COUNT(*) FROM players")
                nombre_joueurs = curseur.fetchone()[0]
                
                curseur.execute("SELECT COUNT(*) FROM scores")
                nombre_scores = curseur.fetchone()[0]
                
                curseur.execute("SELECT COUNT(DISTINCT game) FROM scores")
                nombre_jeux = curseur.fetchone()[0]
                
                fichier.write("* SECTION 1 : VOLUMETRIE GLOBALE\n")
                fichier.write("~" * 35 + "\n")
                fichier.write(f" -> Total Joueurs Enregistrés : {nombre_joueurs}\n")
                fichier.write(f" -> Total Sessions de Jeu     : {nombre_scores}\n")
                fichier.write(f" -> Catalogue de Jeux         : {nombre_jeux}\n\n")
                
                # --- 2. CLASSEMENT ÉLITE (TOP 5) ---
                fichier.write("* SECTION 2 : PALMARES DES MEILLEURS SCORES\n")
                fichier.write("~" * 70 + "\n")
                # Formatage du tableau avec des barres verticales
                fichier.write(f"| {'RANG':<5} | {'PSEUDONYME':<20} | {'TITRE DU JEU':<25} | {'SCORE':>10} |\n")
                fichier.write("+" + "-"*7 + "+" + "-"*22 + "+" + "-"*27 + "+" + "-"*12 + "+\n")
                
                requete_top_5 = """
                    SELECT p.username, s.game, s.score 
                    FROM scores s
                    JOIN players p ON s.player_id = p.player_id
                    ORDER BY s.score DESC 
                    LIMIT 5
                """
                curseur.execute(requete_top_5)
                compteur = 1
                for pseudo, jeu, score in curseur.fetchall():
                    fichier.write(f"| {compteur:<5} | {pseudo:<20} | {jeu:<25} | {score:>10} |\n")
                    compteur += 1
                fichier.write("~" * 70 + "\n\n")
                
                # --- 3. PERFORMANCE MOYENNE ---
                fichier.write("* SECTION 3 : MOYENNES PAR JEU\n")
                fichier.write("~" * 40 + "\n")
                curseur.execute("SELECT game, AVG(score) FROM scores GROUP BY game")
                for jeu, moyenne in curseur.fetchall():
                    fichier.write(f" * {jeu:<25} : {moyenne:>8.1f} pts\n")
                fichier.write("\n")
                
                # --- 4. RÉPARTITION GÉOGRAPHIQUE ---
                fichier.write("* SECTION 4 : ORIGINE DES JOUEURS\n")
                fichier.write("~" * 40 + "\n")
                curseur.execute("SELECT country, COUNT(*) FROM players GROUP BY country")
                for pays, compte in curseur.fetchall():
                    nom_pays = pays if pays else "Non spécifié"
                    fichier.write(f" * {nom_pays:<25} : {compte:>5} inscrits\n")
                fichier.write("\n")
    
                # --- 5. ANALYSE DES PLATEFORMES ---
                fichier.write("* SECTION 5 : POPULARITE DES PLATEFORMES\n")
                fichier.write("~" * 40 + "\n")
                curseur.execute("SELECT platform, COUNT(*) FROM scores GROUP BY platform")
                for plateforme, compte in curseur.fetchall():
                    nom_plateforme = plateforme if plateforme else "Inconnue"
                    fichier.write(f" * {nom_plateforme:<25} : {compte:>5} sessions\n")
                    
                fichier.write("\n" + "#" * 60 + "\n")
    
        print("[RAPPORT] Finalisation : Document généré et sauvegardé.")
