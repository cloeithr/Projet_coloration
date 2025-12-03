from dataclasses import dataclass
from datetime import datetime

@dataclass
class Operation:
    centre: str
    product: str
    of: str
    sequence: str
    op: str
    start: datetime
    end: datetime

@dataclass
class Machine:
    name: str
    order: int
