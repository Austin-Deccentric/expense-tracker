import json
import pytest

from tracker.models import Expense


def test_to_dict_and_from_dict_roundtrip():
    e = Expense(5.5, "Food", "lunch")
    d = e.to_dict()
    assert d["amount"] == 5.5
    assert d["category"] == "Food"
    assert d["note"] == "lunch"

    restored = Expense.from_dict(d)
    assert restored == e


def test_from_dict_coerces_types_and_defaults():
    payload = {"amount": "10", "category": "Transport", "note": None}
    e = Expense.from_dict(payload)
    assert isinstance(e.amount, float)
    assert e.amount == 10.0
    assert e.category == "Transport"
    assert e.note == ""


def test_from_dict_missing_keys_raises_keyerror():
    with pytest.raises(KeyError):
        Expense.from_dict({"amount": "1.0"})
