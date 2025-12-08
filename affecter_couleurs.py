def affecter_couleurs(liste_operations, couleur_mapping, critere='code_produit'):
    """
    Affecte l'ID de couleur (entier) à chaque objet Operation en utilisant 
    le résultat de la coloration du graphe.
    
    Args:
        liste_operations (list[Operation]): La liste globale de tous les objets Operation.
        couleur_mapping (dict): Le résultat de la coloration {Critère: Couleur_ID}.
        critere (str): Le champ utilisé comme critère de coloration (par défaut 'code_produit').
        
    Returns:
        list[Operation]: La liste des opérations mise à jour.
    """
    
    # Étape A: Itérer sur la liste de toutes les opérations
    for op in liste_operations:
        
        # Étape B: Identifier la clé (le Code Produit)
        # On utilise getattr pour rester générique, même si c'est 'code_produit'
        valeur_critere = getattr(op, critere) 
        
        # Étape C: Récupérer l'ID de couleur
        # On utilise .get() pour éviter une erreur si, par accident, un critère n'est pas dans le mapping
        couleur_id = couleur_mapping.get(valeur_critere, 0) # 0 = couleur par défaut/erreur
        
        # Étape D: Affecter l'ID de couleur à l'attribut de l'objet
        op.couleur_assignee = couleur_id
        
    return liste_operations


# --- ZONE DE TEST ET INTÉGRATION ---

if __name__ == "__main__":
    # --- 0. Préparation du mapping de test (résultat de colorier_graphe) ---
    mapping_test = {
        'ProdA': 1,
        'ProdB': 2,
        'ProdC': 3,
        'ProdD': 1
    }
    
    # --- 1. Création d'opérations de test (Simule les objets Operation) ---
    # Nous utilisons de simples dictionnaires pour le test sans l'objet complet
    # dans cet exemple, mais en réalité, vous utiliserez votre liste 'toutes_les_operations'
    operations_test = [
        {'code_produit': 'ProdA', 'machine': 'MAC1', 'couleur_assignee': None},
        {'code_produit': 'ProdC', 'machine': 'MAC2', 'couleur_assignee': None},
        {'code_produit': 'ProdA', 'machine': 'MAC3', 'couleur_assignee': None},
        {'code_produit': 'ProdD', 'machine': 'MAC4', 'couleur_assignee': None},
    ]

    # Pour que le test fonctionne avec la fonction réelle, 
    # nous devons mocker le résultat de la Phase 1:
    class MockOperation:
        def __init__(self, code, couleur=None):
            self.code_produit = code
            self.couleur_assignee = couleur
    
    mock_operations = [
        MockOperation('ProdA'), MockOperation('ProdC'), 
        MockOperation('ProdA'), MockOperation('ProdD')
    ]
    
    # 2. Exécution de l'affectation (Phase 3.2)
    operations_colorees = affecter_couleurs(mock_operations, mapping_test)
    
    print("\n--- Résultat de l'Affectation des Couleurs ---")

    # 3. Validation (Test : Utilisation des asserts)
    
    # Vérification 1 : ProdA doit avoir la Couleur 1
    assert operations_colorees[0].couleur_assignee == 1, "Erreur: ProdA n'a pas la couleur 1."
    
    # Vérification 2 : ProdC doit avoir la Couleur 3
    assert operations_colorees[1].couleur_assignee == 3, "Erreur: ProdC n'a pas la couleur 3."
    
    # Vérification 3 : ProdD doit avoir la Couleur 1 (réutilisation)
    assert operations_colorees[3].couleur_assignee == 1, "Erreur: ProdD n'a pas la couleur 1."
    
    print("✅ Test d'affectation des couleurs réussi.")
    for op in operations_colorees:
        print(f"Opération {op.code_produit}: Couleur {op.couleur_assignee}")