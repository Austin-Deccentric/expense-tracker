import pytest
from tracker.core import ExpenseTracker
from tracker.storage import Storage
from tracker.models import Expense

class FakeStorage(Storage):
    """In-memory storage for tests — no real files."""
    def __init__(self):
        self.data: list[Expense] = []
    def load(self):
        return list(self.data)
    def save(self, expenses):
        self.data = list(expenses)

@pytest.fixture
def tracker():
    return ExpenseTracker(FakeStorage())

def test_add_returns_expense(tracker):
    e = tracker.add_expense(12.5, "food", "Lunch")
    assert e.amount == 12.5
    assert e.category == "food"

def test_add_persists(tracker):
    tracker.add_expense(10, "food")
    tracker.add_expense(5, "food")
    assert len(tracker.list_expenses()) == 2

def test_summary_groups_by_category(tracker):
    tracker.add_expense(10, "food")
    tracker.add_expense(40, "transport")
    tracker.add_expense(5, "food")
    assert tracker.summary() == {"food": 15, "transport": 40}

def test_total(tracker):
    tracker.add_expense(10, "food")
    tracker.add_expense(40, "transport")
    assert tracker.total_expense() == 50

@pytest.mark.parametrize("amount", [0, -5, -0.01])
def test_rejects_non_positive_amount(tracker, amount):
    with pytest.raises(ValueError):
        tracker.add_expense(amount, "food")

def test_rejects_blank_category(tracker):
    with pytest.raises(ValueError):
        tracker.add_expense(10, "   ")