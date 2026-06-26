"""Data model definitions for the expense tracker application."""

from dataclasses import dataclass, asdict

@dataclass
class Expense:
    """Represents an individual expense entry."""

    amount: float
    category: str
    note: str = ""

    def to_dict(self) -> dict[str, object]:
        """Convert the expense to a JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Create an Expense from a dictionary.

        Missing keys are replaced with sensible defaults and amount values
        are converted to float.
        """
        return cls(
            amount=float(data['amount']),
            category=str(data['category']),
            note=str(data.get("note", "") or ""),
        )
