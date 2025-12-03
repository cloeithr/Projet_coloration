import csv
import json
from .models import Operation

def load_from_csv(path):
    operations = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            operations.append(
                Operation(
                    id=row["id"],
                    machine=row["machine"],
                    start=int(row["start"]),
                    end=int(row["end"]),
                    criterion=row["criterion"]
                )
            )
    return operations

def load_from_json(path):
    with open(path) as f:
        data = json.load(f)
    operations = []
    for op in data["operations"]:
        operations.append(
            Operation(
                id=op["id"],
                machine=op["machine"],
                start=int(op["start"]),
                end=int(op["end"]),
                criterion=op["criterion"]
            )
        )
    return operations
