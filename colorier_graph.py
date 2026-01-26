from collections import defaultdict

# --- Phase 3.1 : Coloration du Graphe ---

def colorier_graphe(graphe_conflit):
    """
    Applique l'algorithme de coloration gloutonne (Greedy) au graphe de conflit 
    pour déterminer le nombre minimal de couleurs nécessaires (nombre chromatique) 
    et attribuer une couleur à chaque nœud (critère).
    
    Args:
        graphe_conflit (dict): Le graphe où Clé = Critère (e.g., 'codprod'), 
                               Valeur = Ensemble des voisins.
                               
    Returns:
        dict: Le mapping couleur/critère. Clé = Critère, Valeur = Couleur ID (int).
    """
    
    # Dictionnaire qui va stocker le résultat : {'PROD01': 1, 'PROD02': 2, ...}
    couleur_mapping = {} 
    
    # 1. On récupère la liste de tous les nœuds (critères uniques)
    # L'ordre du parcours peut affecter le résultat final avec l'algorithme glouton.
    # Pour l'instant, on prend un ordre simple.
    noeuds = list(graphe_conflit.keys())
    
    # 2. Parcourir chaque nœud
    for noeud in noeuds:
        
        # Ensemble des couleurs déjà utilisées par les voisins de ce nœud
        couleurs_voisines = set() 
        
        # 3. Regarder les couleurs de tous les voisins
        for voisin in graphe_conflit.get(noeud, set()):
            # Si le voisin a déjà reçu une couleur...
            if voisin in couleur_mapping:
                couleurs_voisines.add(couleur_mapping[voisin])
                
        # 4. Trouver la plus petite couleur disponible (la 'Couleur 1', 'Couleur 2', etc.)
        couleur_disponible = 1
        while couleur_disponible in couleurs_voisines:
            couleur_disponible += 1
            
        # 5. Attribuer la couleur trouvée au nœud actuel
        couleur_mapping[noeud] = couleur_disponible
        
    return couleur_mapping

# --- FIN DE LA FONCTION ---

if __name__ == "__main__":
    # --- Création du Graphe Test K3 (Triangle A-B-C-A) ---
    # ProdA, ProdB, ProdC sont mutuellement voisins
    graphe_test_k3 = {
        'ProdA': {'ProdB', 'ProdC'},
        'ProdB': {'ProdA', 'ProdC'},
        'ProdC': {'ProdA', 'ProdB'},
        # Ajout d'un nœud isolé (non voisin) pour vérifier si la couleur est réutilisée
        'ProdD': set() 
    }
    
    # 1. Exécution de la coloration
    resultat_coloration = colorier_graphe(graphe_test_k3)
    
    print("\n--- Résultat de la Coloration Gloutonne ---")
    print(resultat_coloration)
    
    # 2. Validation (Test 3 de votre architecture)
    couleurs_uniques = set(resultat_coloration.values())
    
    # Pour le triangle K3 (ProdA, B, C), on s'attend à 3 couleurs.
    # On s'attend à ce que ProdD réutilise la Couleur 1.
    
    assert len(couleurs_uniques) >= 3, "Le triangle n'a pas été colorié avec au moins 3 couleurs."
    assert resultat_coloration['ProdD'] == 1, "Le nœud isolé (ProdD) n'a pas réutilisé la Couleur 1."
    print(f"✅ Test 3: Coloration du Graphe (Nombre chromatique = {len(couleurs_uniques)}) OK.")



print("\n--- Fin des Tests de Coloration du Graphe ---\n")