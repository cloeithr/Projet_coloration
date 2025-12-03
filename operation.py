class Operation:
    def __init__(self, id, machine, start, end, criterion):
        self.id = id
        self.machine = machine
        self.start = start
        self.end = end
        self.criterion = criterion

    def __repr__(self):
        return f"Operation({self.id}, {self.machine}, {self.start}, {self.end}, {self.criterion})"
