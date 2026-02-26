from collections import defaultdict

def construire_graphe_conflits(operations_par_machine, critere='code_produit', niveau_voisinage=1):
    """
    Construit le graphe de conflit.
    Niveau 1 : Opérations adjacentes (i, i+1).
    Niveau 2 : Opérations séparées par une (i, i+2).
    
    Correction : On utilise la position dans la liste (séquence) plutôt que
    l'égalité stricte des dates, pour gérer les pauses entre opérations.
    """
    graphe_conflit = defaultdict(set)
    
    # Compteurs pour le debug
    stats = {"N1": 0, "N2": 0}

    for machine, operations in operations_par_machine.items():
        # 1. Initialiser les nœuds (pour ne pas oublier les produits isolés)
        for op in operations:
            valeur_critere = getattr(op, critere)
            if valeur_critere not in graphe_conflit:
                graphe_conflit[valeur_critere] = set()

        n = len(operations)
        
        # 2. Parcours de la séquence
        for i in range(n):
            op_courante = operations[i]
            val_courante = getattr(op_courante, critere)

            # --- NIVEAU 1 : Voisin direct (i + 1) ---
            if i + 1 < n:
                op_suivante = operations[i + 1]
                val_suivante = getattr(op_suivante, critere)
                
                # Si les produits sont différents, il y a conflit
                if val_courante != val_suivante:
                    if val_suivante not in graphe_conflit[val_courante]:
                        stats["N1"] += 1
                    
                    graphe_conflit[val_courante].add(val_suivante)
                    graphe_conflit[val_suivante].add(val_courante)

            # --- NIVEAU 2 : Voisin à 2 sauts (i + 2) ---
            # On active ceci uniquement si demandé
            if niveau_voisinage >= 2 and i + 2 < n:
                op_loin = operations[i + 2]
                val_loin = getattr(op_loin, critere)

                # Conflit si ce n'est pas le même produit
                if val_courante != val_loin:
                    # On ajoute l'arête 
                    if val_loin not in graphe_conflit[val_courante]:
                        stats["N2"] += 1
                        
                    graphe_conflit[val_courante].add(val_loin)
                    graphe_conflit[val_loin].add(val_courante)

    print(f"   [DEBUG GRAPHE] Nouveaux conflits détectés -> Voisins Directs: {stats['N1']}, Voisins distants (N2): {stats['N2']}")
    return dict(graphe_conflit)