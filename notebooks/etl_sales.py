# Databricks notebook source
dbutils.widgets.text("catalog", "dev")
catalog = dbutils.widgets.get("catalog")

import sys
sys.path.append("/Workspace" + "/".join(dbutils.notebook.entry_point.getDbutils()
    .notebook().getContext().notebookPath().get().split("/")[:-2]) + "/src")

from transform import clean_and_aggregate

# Simulated source data (replace with real ingestion later)
sample_rows = [
    {"region": "APAC", "amount": 120.5, "qty": 3},
    {"region": "APAC", "amount": 80.0, "qty": 1},
    {"region": "EMEA", "amount": 300.0, "qty": 7},
    {"region": "AMER", "amount": -5.0, "qty": 1},   # bad record, should be dropped
]

aggregated = clean_and_aggregate(sample_rows)

df = spark.createDataFrame(aggregated)
df.write.mode("overwrite").saveAsTable(f"{catalog}.sales.region_totals")

# Inline integration check — fails the job (and the pipeline) if this doesn't hold
count = spark.table(f"{catalog}.sales.region_totals").count()
assert count == 2, f"Expected 2 aggregated regions, got {count}"
print(f"ETL succeeded for catalog={catalog}, rows={count}")