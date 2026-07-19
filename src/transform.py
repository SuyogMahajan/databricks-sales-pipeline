def clean_and_aggregate(rows):
    """
    rows: list of dicts like {"region": "APAC", "amount": 120.5, "qty": 3}
    Returns: list of dicts aggregated by region: total_amount, total_qty
    """
    agg = {}
    for r in rows:
        if r.get("amount") is None or r["amount"] < 0:
            continue  # drop bad records
        region = r["region"]
        agg.setdefault(region, {"region": region, "total_amount": 0.0, "total_qty": 0})
        agg[region]["total_amount"] += r["amount"]
        agg[region]["total_qty"] += r.get("qty", 0)
    return list(agg.values())