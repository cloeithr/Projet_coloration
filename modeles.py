from dataclasses import dataclass

@dataclass
class Operation:
    centre: str
    codprod: str
    codof: str
    sequence: int
    codop: str
    dtedeb: int  # on garde int pour le moment
    dtefin: int  # pareil

@dataclass
class Machine:
    centre: str

# jeu de données simplifié 
exemple_operations = [
    Operation("M1", "P1", "OF1", 1, "OP10", 0, 3),
    Operation("M1", "P1", "OF1", 2, "OP20", 3, 7),
    Operation("M2", "P2", "OF2", 1, "OP10", 1, 6),
    Operation("M1", "P3", "OF3", 1, "OP10", 7, 9)
]

exemple_machines = [
    Machine("M1"),
    Machine("M2")
]


def test_operations(operations):
    """Vérifie que le jeu de données est bien chargé"""
    assert len(operations) == 4, "Nombre d'opérations incorrect"
    assert operations[0].centre == "M1", "Premier centre incorrect"
    print("Opérations chargées correctement")

def calcul_voisins(operations):
    """
    Calcule les voisins immédiats : opérations sur le même centre
    Retourne un dictionnaire {codop: [voisins]}
    """
    voisins = {}
    for op1 in operations:
        voisins[op1.codop] = []
        for op2 in operations:
            if op1 != op2 and op1.centre == op2.centre:
                voisins[op1.codop].append(op2.codop)
    return voisins

def affiche_operations(operations):
    """Affiche les opérations pour vérification"""
    print("\nListe des opérations :")
    for op in operations:
        print(op)

def affiche_voisins(voisins):
    """Affiche les voisins de manière lisible"""
    print("\nVoisins immédiats :")
    for codop, voisins_list in voisins.items():
        print(f"{codop} -> {voisins_list}")


if __name__ == "__main__":
    test_operations(exemple_operations) # vérif des opérations
    
    affiche_operations(exemple_operations) #affichage contenu des opé
    
    voisins = calcul_voisins(exemple_operations) # calcul + affichage des voisins
    affiche_voisins(voisins)

# ATTENTION :
# On obient des voisins immédiats mais ils sont répétés et les "codop" sont identiques
# pcq là il y a comparaison des CENTRES et pas comparaison de L'UNICITE DANS LA LISTE. 
# C'est ok je pense pour les trucs à faire de la semaine 1 mais par contre faudra changer pour après
# pcq pour la coloration du diagramme de Gantt chaque opération doit être unique (sinon on va 
# se retrouver avec des couleurs identiques à des opérations qui devraient pas avoir la même couleur).