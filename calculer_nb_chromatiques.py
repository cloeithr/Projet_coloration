from colorier_graph import colorier_graphe

def calculer_nombre_chromatique(couleur_mapping):
    """
    Calcule le nombre chromatique (nombre minimal de couleurs) 
    à partir du résultat de la coloration.
    
    Args:
        couleur_mapping (dict): Le résultat de la coloration {Critère: Couleur_ID (int)}.
        
    Returns:
        int: Le nombre chromatique du graphe de conflit.
    """
    
    if not couleur_mapping:
        return 0 # Retourne 0 s'il n'y a pas de produits à colorier
    
    # Étape A & B: Récupérer toutes les valeurs (IDs de couleur) et trouver le maximum
    # C'est l'opération la plus rapide pour ce calcul !
    nombre_chromatique = max(couleur_mapping.values())
    
    return nombre_chromatique

# --- ZONE DE TEST & INTÉGRATION ---

if __name__ == "__main__":
    # --- Création du Graphe Test K3 (Triangle A-B-C-A) ---
    graphe_test_k3 = {
        'ProdA': {'ProdB', 'ProdC'},
        'ProdB': {'ProdA', 'ProdC'},
        'ProdC': {'ProdA', 'ProdB'},
        'ProdD': set() 
    }
    
    # Simuler la Phase 3.1: Coloration
    # (Nous utilisons la fonction colorier_graphe définie précédemment)
    resultat_coloration = colorier_graphe(graphe_test_k3)
    
    # 1. Exécution du calcul du nombre chromatique (Phase 4.1)
    nombre_chromatique = calculer_nombre_chromatique(resultat_coloration)
    
    print("\n--- Résultat du Nombre Chromatique ---")
    print(f"Le mapping des couleurs est : {resultat_coloration}")
    print(f"Le nombre minimal de couleurs nécessaire est : {nombre_chromatique}")

    # 2. Validation (Test 4)
    # Nous nous attendons à ce que le max soit 3 (Couleurs 1, 2, 3)
    assert nombre_chromatique == 3, f"Erreur: Nombre chromatique attendu 3, obtenu {nombre_chromatique}"
    print("Test du calcul du nombre chromatique réussi.")

