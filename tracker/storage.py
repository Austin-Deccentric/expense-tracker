import json
from abc import ABC, abstractmethod
from pathlib import Path
from .models import Expense

class Storage(ABC):
    @abstractmethod
    def load(self) -> list[Expense]:
        pass
    @abstractmethod
    def save(self, expenses: list[Expense]) -> None:
        pass

class JSONStorage(Storage):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> list[Expense]:
        if not self.file_path.exists():
            return []               # If the file doesn't exist, return an empty list
        try:
            data = json.loads(self.file_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {self.file_path}") from e
    
        return [Expense.from_dict(item) for item in data]
        
        

    def save(self, expenses: list[Expense]) -> None:
        data = [expense.to_dict() for expense in expenses]
        self.file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')