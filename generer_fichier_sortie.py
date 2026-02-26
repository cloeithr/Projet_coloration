import csv
from datetime import datetime

def generer_fichier_sortie(liste_operations, nom_fichier_sortie, critere='code_produit'):
    """
    Génère un fichier de sortie CSV (séparateur ';') contenant toutes les colonnes 
    initiales, plus la nouvelle colonne 'Couleur_ID'.
    
    Args:
        liste_operations (list[Operation]): La liste globale des objets Operation, 
                                            maintenant mis à jour avec 'couleur_assignee'.
        nom_fichier_sortie (str): Le nom du fichier de sortie (ex: 'resultat_colore.txt').
        critere (str): Le champ utilisé comme critère (pour identifier le champ clé).
    """
    
    # Étape A: Définir les EN-TÊTES de colonnes (basé sur operations.csv)
    # Assurez-vous que l'ordre est correct
    champs_originaux = [
        'centre', 'codprod', 'codof', 'sequence', 'codop', 'dtedeb', 'dtefin'
    ]
    # Ajout de notre nouvelle colonne
    nouveaux_champs = champs_originaux + ['Couleur_ID']

    # B. Ouverture du fichier de sortie en mode écriture (gestion automatique du séparateur)
    try:
        with open(nom_fichier_sortie, 'w', newline='', encoding='utf-8') as fichier_sortie:
            # Création de l'objet Writer avec le point-virgule comme délimiteur
            writer = csv.writer(fichier_sortie, delimiter=';') 
            
            # C. Écrire l'en-tête
            writer.writerow(nouveaux_champs)
            
            # D. Itération et E. Formatage/Écriture des lignes
            for op in liste_operations:
                
                # Récupérer les données dans le bon ordre
                ligne_data = [
                    op.machine,
                    op.code_produit,
                    op.job_id,
                    # Attention: les champs 'sequence' et 'codop' n'ont pas été stockés dans la classe Operation
                    # Si ces champs sont importants, vous devez les ajouter à la classe Operation lors de la numérisation.
                    # Pour cet exemple, nous allons utiliser les placeholders si non disponibles.
                    '0', # Placeholder pour sequence
                    '0', # Placeholder pour codop
                    op.date_debut.strftime('%Y-%m-%d %H:%M:%S.000'), # Format de date original
                    op.date_fin.strftime('%Y-%m-%d %H:%M:%S.000'),   # Format de date original
                    str(op.couleur_assignee) # La valeur de couleur
                ]
                
                writer.writerow(ligne_data)
        
        print(f"Fichier de sortie généré avec succès : {nom_fichier_sortie}")
        
    except Exception as e:
        print(f"Erreur lors de la génération du fichier de sortie : {e}")
