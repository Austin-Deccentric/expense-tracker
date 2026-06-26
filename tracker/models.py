from dataclasses import dataclass, asdict

@dataclass
class Expense:
    amount: float
    category: str
    note: str = ""

def to_dict(self) -> dict:
    return asdict(self)

@classmethod
def from_dict(cls, data: dict) -> 'Expense':
    return cls(
        amount=float(data.get('amount', 0.0)),
        category=data.get('category', ''),
        note=data.get('note', '')
    )