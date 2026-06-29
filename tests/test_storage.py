import json
import pytest
from pathlib import Path

from tracker.storage import JSONStorage
from tracker.models import Expense


def test_jsonstorage_missing_file_returns_empty(tmp_path):
    fp = tmp_path / "noexist.json"
    s = JSONStorage(str(fp))
    assert s.load() == []


def test_jsonstorage_reads_and_writes(tmp_path):
    fp = tmp_path / "expenses.json"
    # prepare file
    payload = [{"amount": 1.5, "category": "X", "note": "n"}]
    fp.write_text(json.dumps(payload), encoding="utf-8")

    s = JSONStorage(str(fp))
    loaded = s.load()
    assert isinstance(loaded, list)
    assert len(loaded) == 1
    assert loaded[0].amount == 1.5
    assert loaded[0].category == "X"

    # now save a different set
    new_exp = Expense(4.0, "Y", "o")
    s.save([new_exp])
    raw = json.loads(fp.read_text(encoding="utf-8"))
    assert raw[0]["amount"] == 4.0
    assert raw[0]["category"] == "Y"


def test_jsonstorage_invalid_json_raises_valueerror(tmp_path):
    fp = tmp_path / "bad.json"
    fp.write_text("not-a-json", encoding="utf-8")
    s = JSONStorage(str(fp))
    with pytest.raises(ValueError):
        s.load()
