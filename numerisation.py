import csv
import os
from datetime import datetime
from models import Operation


# Format de date détecté dans votre fichier : 2025-11-24 10:48:00.000
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f' 
# Note: %f sert à lire les millisecondes (.000)

def charger_donnees(chemin_machines, chemin_operations):
    """
    Lit les CSV et retourne une liste d'objets Operation et une liste de Machines.
    """
    liste_machines = []
    liste_operations = []

    # 1. Chargement des Machines (Référence)
    try:
        with open(chemin_machines, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Sauter l'en-tête 'centre'
            for row in reader:
                if row: # Vérifie que la ligne n'est pas vide
                    liste_machines.append(row[0])
        print(f"✅ {len(liste_machines)} machines chargées.")
    except Exception as e:
        print(f"❌ Erreur lecture machines: {e}")

    # 2. Chargement des Opérations (Planning)
    uid_compteur = 1
    try:
        with open(chemin_operations, 'r', encoding='utf-8') as f:
            # Le fichier utilise des points-virgules ';'
            reader = csv.DictReader(f, delimiter=';') 
            
            for row in reader:
                # Conversion des textes en Dates (Indispensable pour le tri !)
                try:
                    d_debut = datetime.strptime(row['dtedeb'], DATE_FORMAT)
                    d_fin = datetime.strptime(row['dtefin'], DATE_FORMAT)
                    
                    # Création de l'objet (Instance du Modèle)
                    nouvelle_op = Operation(
                        machine=row['centre'],
                        code_produit=row['codprod'],
                        job_id=row['codof'],
                        date_debut=d_debut,
                        date_fin=d_fin,
                        uid=uid_compteur
                    )
                    uid_compteur += 1
                    
                    # On ne garde l'opération que si la machine existe (Validation simple)
                    if nouvelle_op.machine in liste_machines:
                        liste_operations.append(nouvelle_op)
                        
                except ValueError as e:
                    print(f"⚠️ Erreur de date sur une ligne : {e}")
                    
        print(f"✅ {len(liste_operations)} opérations numérisées avec succès.")
        
    except Exception as e:
        print(f"❌ Erreur lecture opérations: {e}")

    return liste_machines, liste_operations

# --- ZONE DE TEST (À exécuter pour vérifier) ---
if __name__ == "__main__":
    # Remplacez par les noms exacts de vos fichiers s'ils sont dans le même dossier
    machines, operations = charger_donnees('DataMachine.csv', 'operations.csv')
    
    # Test : Afficher les 3 premières opérations pour voir si le modèle fonctionne
    print("\n--- Aperçu des données numérisées ---")
    for op in operations[:3]:
        print(op)
