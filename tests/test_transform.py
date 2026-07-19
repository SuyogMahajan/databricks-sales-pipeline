from src.transform import clean_and_aggregate

def test_aggregates_by_region():
    rows = [
        {"region": "APAC", "amount": 100, "qty": 1},
        {"region": "APAC", "amount": 50, "qty": 2},
        {"region": "EMEA", "amount": 200, "qty": 5},
    ]
    result = {r["region"]: r for r in clean_and_aggregate(rows)}
    assert result["APAC"]["total_amount"] == 150
    assert result["APAC"]["total_qty"] == 3
    assert result["EMEA"]["total_amount"] == 200

def test_drops_negative_amounts():
    rows = [{"region": "APAC", "amount": -10, "qty": 1}]
    result = clean_and_aggregate(rows)
    assert result == []