from collections import defaultdict

def construire_graphe_conflits(operations_par_machine, critere='codprod'):
    """
    Construit le graphe de conflit de Niveau 1 (voisins directs).
    Les nœuds du graphe sont les valeurs uniques du 'critere' choisi (ex: 'codprod').
    Une arête relie deux nœuds si leurs opérations sont consécutives sur une machine.
    
    Args:
        operations_par_machine (dict): Dictionnaire de machines contenant des listes 
                                       d'objets Operation triés chronologiquement.
        critere (str): Le champ de l'objet Operation à utiliser comme nœud (ex: 'codprod').
        
    Returns:
        dict: Le graphe de conflit. Clé = Nœud (str), Valeur = Ensemble des voisins (set[str]).
    """
    
    # Utilise defaultdict(set) pour que chaque nœud (critère) ait un ensemble de voisins,
    # ce qui garantit qu'il n'y a pas de doublons dans la liste des voisins.
    graphe_conflit = defaultdict(set)
    
    # 1. Parcourir chaque machine
    for machine, operations in operations_par_machine.items():
        
        # 2. Parcourir la liste TRIÉE des opérations de cette machine
        # On compare l'opération i avec l'opération i+1
        for i in range(len(operations) - 1):
            op_courante = operations[i]
            op_suivante = operations[i + 1]
            
            # --- RÈGLE DU VOISINAGE (NIVEAU 1) ---
            
            # A. Récupérer les valeurs du critère pour les deux opérations
            # (Utilisation de getattr car le critère ('codprod') est une variable)
            critere_courant = getattr(op_courante, critere)
            critere_suivant = getattr(op_suivante, critere)
            
            # B. Vérifier si les deux opérations sont bien consécutives (dtefin = dtedeb)
            # ET si les critères sont différents (sinon, pas de conflit de couleur)
            est_consecutif = (op_courante.date_fin == op_suivante.date_debut)
            est_conflit = (critere_courant != critere_suivant)
            
            if est_consecutif and est_conflit:
                # 3. Créer l'arête de conflit
                
                # Le nœud A a B comme voisin
                graphe_conflit[critere_courant].add(critere_suivant)
                
                # Le nœud B a A comme voisin (le graphe est non orienté)
                graphe_conflit[critere_suivant].add(critere_courant)
                
    return dict(graphe_conflit)




# --- ZONE DE TEST & INTÉGRATION ---

from numerisation import charger_donnees
from regrouper_par_machine import regrouper_par_machine

if __name__ == "__main__":
    # 1. Préparation des données (Phase 1)
    _, toutes_les_operations = charger_donnees('DataMachine.csv', 'operations.csv')
    operations_triees = regrouper_par_machine(toutes_les_operations)
    
    # 2. Construction du Graphe (Phase 2.1)
    graphe = construire_graphe_conflits(operations_triees, critere='code_produit')
    
    print("\n--- Aperçu du Graphe de Conflit (Niveau 1) ---")
    
    # Vérification de notre cas de test MAC106 (PROD03 vs PROD01)
    if 'PROD03' in graphe:
        voisins_prod03 = graphe['PROD03']
        print(f"Les voisins de PROD03 sont : {voisins_prod03}")
        
        # Test 2 : Validation du Graphe (comme dans l'architecture)
        assert 'PROD01' in voisins_prod03
        print("✅ Test de validation PROD03 <-> PROD01 réussi.")
    else:
        print("Le PROD03 n'a pas été trouvé comme nœud dans le graphe.")