import csv
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import random as random


# =================================================================
# FONCTION PRINCIPALE (MAIN)
# =================================================================
from models import Operation
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
    
    FICHIER_OPERATIONS = 'operations.csv' 
    FICHIER_MACHINES = 'DataMachine.csv'
    CRITERE_DE_COLORATION = 'code_produit' 
    FICHIER_SORTIE = 'resultat_colore.txt'

    print("--- Démarrage du Programme de Coloration de Gantt ---")
    
    # PHASE 1 : CHARGEMENT & PRÉPARATION
    machines_ref, toutes_les_operations = charger_donnees(FICHIER_MACHINES, FICHIER_OPERATIONS)
    print(f"✅ Total des opérations numérisées : {len(toutes_les_operations)}")
    
    operations_triees_par_machine = regrouper_par_machine(toutes_les_operations)
    print(f"✅ Opérations regroupées et triées par machine.")
    
    # PHASE 2 : CONSTRUCTION DU GRAPHE
    graphe_conflit = construire_graphe_conflits(operations_triees_par_machine, CRITERE_DE_COLORATION)
    print(f"✅ Graphe de conflit N1 construit. Nœuds uniques (produits) : {len(graphe_conflit)}")
    
    # PHASE 3 : COLORATION
    couleur_mapping = colorier_graphe(graphe_conflit)
    
    operations_colorees = affecter_couleurs(toutes_les_operations, couleur_mapping, CRITERE_DE_COLORATION)
    print("✅ Couleurs affectées aux objets Operation.")
    
    # PHASE 4 : SORTIES ET VISUALISATION
    
    nombre_chromatique = calculer_nombre_chromatique(couleur_mapping)
    print(f"\n*** RÉSULTAT CLÉ : Nombre Chromatique Minimal : {nombre_chromatique} ***")
    
    generer_fichier_sortie(operations_colorees, FICHIER_SORTIE)
    
    # Génération de la visualisation Gantt (limité aux 4 premières semaines)
    generer_gantt(operations_colorees, nombre_chromatique)


if __name__ == "__main__":
    main()