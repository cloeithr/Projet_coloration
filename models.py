from datetime import datetime

class Operation:
    def __init__(self, machine, code_produit, job_id, date_debut, date_fin):
        """
        Constructeur du modèle Operation.
        C'est ici qu'on transforme les colonnes du CSV en attributs utilisables.
        """
        self.machine = machine          # Colonne 'centre'
        self.code_produit = code_produit # Colonne 'codprod' (Ce sera notre Noeud !)
        self.job_id = job_id            # Colonne 'codof'
        self.date_debut = date_debut    # Colonne 'dtedeb' (Objet datetime)
        self.date_fin = date_fin        # Colonne 'dtefin' (Objet datetime)
        
        # Attribut futur pour la coloration (initialisé à None)
        self.couleur_assignee = None 

    def __repr__(self):
        """Affiche l'objet proprement pour le débogage"""
        return f"<Op {self.code_produit} sur {self.machine} ({self.date_debut.time()} -> {self.date_fin.time()})>"

    @property
    def duree(self):
        """Calcule la durée automatiquement (utile pour le Gantt plus tard)"""
        return self.date_fin - self.date_debut