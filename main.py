import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


from numerisation import charger_donnees
from regrouper_par_machine import regrouper_par_machine
from construire_graph_conflit import construire_graphe_conflits
from colorier_graph import colorier_graphe
from affecter_couleurs import affecter_couleurs
from calculer_nb_chromatiques import calculer_nombre_chromatique
from generer_fichier_sortie import generer_fichier_sortie
from gantt_generer import generer_gantt


def main():
    """Orchestre toutes les étapes du programme."""
    
    # --- CONFIGURATION ---
    FICHIER_OPERATIONS = 'operations.csv' 
    FICHIER_MACHINES = 'DataMachine.csv'
    # Pour le voisinage 2 entre opérations (y compris mêmes produits), on colore par opération.
    CRITERE_DE_COLORATION = 'uid' 
    FICHIER_SORTIE = 'resultat_colore.txt'
    
    # ICI : On force le niveau 2
    NIVEAU_VOISINAGE_CIBLE = 2 

    print("--- Démarrage du Programme de Coloration de Gantt ---")
    
    # PHASE 1 : CHARGEMENT
    machines_ref, toutes_les_operations = charger_donnees(FICHIER_MACHINES, FICHIER_OPERATIONS)
    operations_triees = regrouper_par_machine(toutes_les_operations)
    print(f"✅ Données chargées et triées.")
    
    # PHASE 2 : CONSTRUCTION DU GRAPHE (SUR TOUT LE JEU DE DONNÉES)
    print(f"\n--- Construction du Graphe (Mode Voisinage = {NIVEAU_VOISINAGE_CIBLE}) ---")
    graphe_conflit = construire_graphe_conflits(
        operations_triees,
        CRITERE_DE_COLORATION,
        niveau_voisinage=NIVEAU_VOISINAGE_CIBLE,
    )
    
    # PHASE 3 : COLORATION (SUR TOUT LE JEU DE DONNÉES)
    couleur_mapping = colorier_graphe(graphe_conflit)
    nombre_chromatique = calculer_nombre_chromatique(couleur_mapping)
    
    print(f"\n*** RÉSULTAT FINAL : Nombre Chromatique = {nombre_chromatique} ***")
    print(f"Nombre de couleurs nécessaires (jeu complet) : {nombre_chromatique}")
    
    # PHASE 4 : SORTIES (TOUTES LES OPÉRATIONS)
    operations_colorees = affecter_couleurs(toutes_les_operations, couleur_mapping, CRITERE_DE_COLORATION)
    generer_fichier_sortie(operations_colorees, FICHIER_SORTIE)
    
    # Lancement du Gantt sur TOUT le jeu de données
    generer_gantt(
        operations_colorees,
        nombre_chromatique,
        affichage_semaines_reelles=True,
        navigation_semaines=True,
    )

if __name__ == "__main__":
    main()
