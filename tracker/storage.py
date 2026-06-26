"""Persistence adapters for expense storage."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from .models import Expense


class Storage(ABC):
    """Abstract interface for expense persistence backends."""

    @abstractmethod
    def load(self) -> list[Expense]:
        """Load expenses from storage."""
        pass

    @abstractmethod
    def save(self, expenses: list[Expense]) -> None:
        """Save the provided list of expenses to storage."""
        pass


class JSONStorage(Storage):
    """Store expenses in a JSON file."""

    def __init__(self, file_path: str = "expenses.json"):
        """Initialize the storage adapter with a target JSON file path."""
        self.file_path = Path(file_path)

    def load(self) -> list[Expense]:
        """Read expenses from the configured JSON file."""
        if not self.file_path.exists():
            return []

        try:
            data = json.loads(self.file_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {self.file_path}") from e

        return [Expense.from_dict(item) for item in data]

    def save(self, expenses: list[Expense]) -> None:
        """Serialize expenses to JSON and write them to disk."""
        data = [expense.to_dict() for expense in expenses]
        self.file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
