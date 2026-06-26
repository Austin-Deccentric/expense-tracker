"""Core business logic for the expense tracker application."""

from collections import defaultdict
from .models import Expense
from .storage import Storage


class ExpenseTracker:
    """Manage expense entries using a persistence backend."""

    def __init__(self, storage: Storage):
        """Load existing expenses from storage into the tracker."""
        self.__storage = storage
        self.__expenses: list[Expense] = list(self.__storage.load())

    def add_expense(self, amount: float, category: str, note: str = "") -> Expense:
        """Validate and record a new expense.

        Raises:
            ValueError: If the amount is not positive or the category is empty.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not category.strip():
            raise ValueError("Category is required.")

        expense = Expense(amount, category.strip(), note)
        self.__expenses.append(expense)
        self.__storage.save(self.__expenses)
        return expense

    def list_expenses(self) -> list[Expense]:
        """Return a copy of all tracked expense objects."""
        return list(self.__expenses)

    def summary(self) -> dict[str, float]:
        """Return total spending grouped by expense category."""
        summary_dict: dict[str, float] = defaultdict(float)
        for expense in self.__expenses:
            summary_dict[expense.category] += expense.amount
        return dict(summary_dict)

    def total_expense(self) -> float:
        """Return the total sum of all expense amounts."""
        return sum(expense.amount for expense in self.__expenses)
