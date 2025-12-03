from pathlib import Path
from datetime import datetime
from models import Operation, Machine

def load_operations(path: Path) -> list[Operation]:
    operations = []
    with path.open(encoding="utf-8") as f:
        header = True
        for line in f:
            if header:
                header = False
                continue

            line = line.strip()
            if not line:
                continue

            parts = line.split(";")
            if len(parts) < 7:
                continue

            centre, codprod, codof, sequence, codop, dtedeb, dtefin = parts

            # conversion date
            start = datetime.fromisoformat(dtedeb.replace(" ", "T"))
            end = datetime.fromisoformat(dtefin.replace(" ", "T"))

            operations.append(Operation(
                centre=centre,
                product=codprod,
                of=codof,
                sequence=sequence,
                op=codop,
                start=start,
                end=end,
            ))

    return operations


def load_machines(path: Path) -> list[Machine]:
    machines = []
    with path.open(encoding="utf-8") as f:
        header = True
        order = 0
        for line in f:
            if header:
                header = False
                continue

            name = line.strip()
            if not name:
                continue

            machines.append(Machine(name=name, order=order))
            order += 1

    return machines
