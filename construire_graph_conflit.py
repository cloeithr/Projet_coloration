from collections import defaultdict

def construire_graphe_conflits(operations_par_machine, critere='code_produit', niveau_voisinage=1):
    """
    Construit le graphe de conflit de manière DYNAMIQUE.
    Si niveau_voisinage = 3, il vérifiera (i+1), (i+2) et (i+3).
    """
    graphe_conflit = defaultdict(set)
    
    # Compteur global pour le debug
    stats = {"conflits_ajoutes": 0}

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

            # --- NIVEAU DYNAMIQUE (La magie opère ici) ---
            # On boucle de 1 jusqu'au niveau_voisinage demandé
            for saut in range(1, niveau_voisinage + 1):
                
                # On vérifie qu'on ne déborde pas de la liste
                if i + saut < n:
                    op_voisine = operations[i + saut]
                    val_voisine = getattr(op_voisine, critere)
                    
                    # Si le critère est différent, il y a conflit
                    if val_courante != val_voisine:
                        
                        # Ajout au graphe (le set évite automatiquement les doublons)
                        if val_voisine not in graphe_conflit[val_courante]:
                            stats["conflits_ajoutes"] += 1
                            
                        graphe_conflit[val_courante].add(val_voisine)
                        graphe_conflit[val_voisine].add(val_courante)

    print(f"   [DEBUG GRAPHE] Niveau {niveau_voisinage} appliqué -> Nombre de conflits uniques créés : {stats['conflits_ajoutes']}")
    return dict(graphe_conflit)