import pytest

from tracker.core import ExpenseTracker
from tracker.models import Expense


class DummyStorage:
    def __init__(self, initial=None):
        self._initial = list(initial or [])
        self.saved = None

    def load(self):
        return list(self._initial)

    def save(self, expenses):
        # store a shallow copy for inspection
        self.saved = list(expenses)


def test_add_expense_valid_saves_and_returns_expense():
    storage = DummyStorage()
    t = ExpenseTracker(storage)

    e = t.add_expense(3.25, "Coffee", "morning")
    assert isinstance(e, Expense)
    assert e.amount == 3.25
    assert e.category == "Coffee"
    assert t.list_expenses() == [e]
    # storage.saved should have been called with the list containing the Expense
    assert storage.saved is not None
    assert storage.saved[0].amount == 3.25


def test_add_expense_invalid_amount_and_category():
    storage = DummyStorage()
    t = ExpenseTracker(storage)

    with pytest.raises(ValueError):
        t.add_expense(0, "Food")

    with pytest.raises(ValueError):
        t.add_expense(-5, "Rent")

    with pytest.raises(ValueError):
        t.add_expense(10, "   ")


def test_summary_and_total_calculation():
    initial = [Expense(2.0, "A"), Expense(3.0, "B"), Expense(1.5, "A")]
    storage = DummyStorage(initial=initial)
    t = ExpenseTracker(storage)

    assert t.total_expense() == pytest.approx(6.5)
    summary = t.summary()
    assert summary == {"A": pytest.approx(3.5), "B": pytest.approx(3.0)}
