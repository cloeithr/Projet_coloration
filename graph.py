def overlap(op1, op2):
    return not (op1.end <= op2.start or op2.end <= op1.start)

def build_graph(operations):
    graph = {op.id: [] for op in operations}

    for i, op1 in enumerate(operations):
        for op2 in operations[i+1:]:
            if overlap(op1, op2) and op1.criterion != op2.criterion:
                graph[op1.id].append(op2.id)
                graph[op2.id].append(op1.id)

    return graph
