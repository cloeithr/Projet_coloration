from dataclasses import dataclass

# Modèles
@dataclass
class Operation:
    centre: str
    codprod: str
    codof: str
    sequence: int
    codop: str
    dtedeb: int
    dtefin: int

@dataclass
class Machine:
    centre: str

# exemple
example_operations = [
    Operation("M1", "P1", "OF1", 1, "OP10", 0, 3),
    Operation("M1", "P1", "OF1", 2, "OP20", 3, 7),
    Operation("M2", "P2", "OF2", 1, "OP10", 1, 6),
    Operation("M1", "P3", "OF3", 1, "OP10", 7, 9)
]

example_machines = [
    Machine("M1"),
    Machine("M2")
]

# Fonction de test simple
def test_operations_loaded(operations):
    assert len(operations) == 4
    assert operations[0].centre == "M1"
    print("Test OK : opérations chargées correctement")

# je crois que c'est pas à faire dans la semaine 1    
def test_voisins(operations):
    voisins = {}
    for op1 in operations:
        voisins[op1.codop] = []
        for op2 in operations:
            if op1 != op2 and op1.centre == op2.centre:
                voisins[op1.codop].append(op2.codop)
    return voisins

voisins = test_voisins(example_operations)
print(voisins)



if __name__ == "__main__":
    test_operations_loaded(example_operations)


#verif contenu des objets
for op in example_operations:
    print(op)

