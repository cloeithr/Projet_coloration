from collections import defaultdict
from numerisation import charger_donnees

def regrouper_par_machine(liste_operations):
    """
    Regroupe les opérations par machine (centre) et trie la liste 
    d'opérations de chaque machine par date de début (dtedeb).
    
    Args:
        liste_operations (list[Operation]): La liste de tous les objets Operation.
        
    Returns:
        dict: Un dictionnaire où la clé est le nom de la machine (str) 
              et la valeur est une liste d'objets Operation triés chronologiquement.
    """
    
    # Utilise defaultdict pour créer automatiquement une liste vide si la clé n'existe pas
    operations_par_machine = defaultdict(list)
    
    # 1. Regroupement
    for op in liste_operations:
        operations_par_machine[op.machine].append(op)
        
    # 2. Tri Chronologique par Machine
    # C'est l'étape la plus CRUCIALE pour le voisinage de Niveau 1
    for machine in operations_par_machine:
        # Trie la liste des opérations de CETTE machine en utilisant 'date_debut'
        operations_par_machine[machine].sort(key=lambda op: op.date_debut)
        
    return dict(operations_par_machine)

# --- ZONE DE TEST & INTÉGRATION ---

# Il faut maintenant intégrer cette fonction au déroulement de votre programme.

if __name__ == "__main__":
    # Assumons que la fonction numerisation (charger_donnees) retourne les opérations
    # (Remplacez 'numerisation' par le nom exact si vous l'avez renommé)
    machines_ref, toutes_les_operations = charger_donnees('DataMachine.csv', 'operations.csv')
    
    # Exécution de l'étape de regroupement et de tri
    operations_triees = regrouper_par_machine(toutes_les_operations)
    
    print("\n--- Aperçu du Regroupement et du Tri ---")
    
    # Affichage d'une machine spécifique pour vérifier l'ordre
    machine_test = 'MAC101'
    if machine_test in operations_triees:
        print(f"Machine {machine_test} (Total: {len(operations_triees[machine_test])} opérations) :")
        
        # Afficher la date de début de la première et la dernière opération
        # pour s'assurer que le tri est correct
        premiere_op = operations_triees[machine_test][0]
        derniere_op = operations_triees[machine_test][-1]
        
        print(f"  - Première op. : {premiere_op.code_produit} à {premiere_op.date_debut}")
        print(f"  - Dernière op. : {derniere_op.code_produit} à {derniere_op.date_debut}")
        print("✅ Le tri semble correct si la première date est antérieure à la dernière.")
    else:
        print(f"La machine {machine_test} n'a pas été trouvée dans les données triées.")