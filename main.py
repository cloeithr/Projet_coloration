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
    
    # PHASE 2 : CONSTRUCTION DU GRAPHE
    print(f"\n--- Construction du Graphe (Mode Voisinage = {NIVEAU_VOISINAGE_CIBLE}) ---")
    graphe_conflit = construire_graphe_conflits(
        operations_triees,
        CRITERE_DE_COLORATION,
        niveau_voisinage=NIVEAU_VOISINAGE_CIBLE,
    )
    
    # PHASE 3 : COLORATION
    couleur_mapping = colorier_graphe(graphe_conflit)
    nombre_chromatique = calculer_nombre_chromatique(couleur_mapping)
    
    print(f"\n*** RÉSULTAT FINAL : Nombre Chromatique = {nombre_chromatique} ***")
    
    # PHASE 4 : SORTIES
    operations_colorees = affecter_couleurs(toutes_les_operations, couleur_mapping, CRITERE_DE_COLORATION)
    generer_fichier_sortie(operations_colorees, FICHIER_SORTIE)
    
    # --- MODIFICATION ICI : FILTRAGE POUR SEMAINES 48 ET 49 ---
    
    SEMAINES_CIBLES = [48, 49] # Tu peux changer ça facilement 
    ANNEE_CIBLE = 2025         # Important de préciser l'année
    
    print(f"\n--- Filtrage des données pour les semaines {SEMAINES_CIBLES} ---")
    
    operations_filtrees = []
    for op in operations_colorees:
        # On récupère le numéro de semaine ISO de la date de début
        # isocalendar() renvoie (année, semaine, jour)
        annee_op, semaine_op, _ = op.date_debut.isocalendar()
        
        # On garde l'opération si elle commence dans une des semaines ciblées
        # OU si elle finit dedans (pour ne pas couper les opérations à cheval)
        annee_fin, semaine_fin, _ = op.date_fin.isocalendar()
        
        if annee_op == ANNEE_CIBLE and (semaine_op in SEMAINES_CIBLES or semaine_fin in SEMAINES_CIBLES):
            operations_filtrees.append(op)
            
    print(f"   {len(operations_filtrees)} opérations trouvées sur cette période.")

    # Fenêtre stricte : semaines 48-49 uniquement
    debut_fenetre = datetime.fromisocalendar(ANNEE_CIBLE, SEMAINES_CIBLES[0], 1)
    fin_fenetre = datetime.fromisocalendar(ANNEE_CIBLE, SEMAINES_CIBLES[-1], 7) + timedelta(days=1)
    
    # Lancement du Gantt avec la liste FILTRÉE et l'option d'affichage réel
    generer_gantt(
        operations_filtrees,
        nombre_chromatique,
        affichage_semaines_reelles=True,
        fenetre_temps=(debut_fenetre, fin_fenetre),
    )

if __name__ == "__main__":
    main()
