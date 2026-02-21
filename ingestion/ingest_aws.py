import pandas as pd
from neo4j import GraphDatabase
from ingestion.mappings import derive_cost_intent

URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "infleratechnologies"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

df = pd.read_excel("data_samples/aws_test-focus-00001.snappy_transformed.xls")

# Normalize columns
df.columns = [c.strip().lower() for c in df.columns]

def derive_cost_record_id(row):
    return f"{row['billingaccountid']}_{row['subaccountid']}_{row['resourceid']}_{row['chargeperiodstart']}_{row['chargecategory']}"

def ingest_row(tx, row):
    tx.run("""
    MERGE (c:CostRecord {costRecordId: $costRecordId})
      SET c.effectiveCost = $effectiveCost,
          c.billedCost = $billedCost,
          c.currency = $currency

    MERGE (r:Resource {resourceId: $resourceId})
    MERGE (s:Service {serviceName: $serviceName})
    MERGE (t:TimeFrame {
        chargePeriodStart: $chargePeriodStart,
        chargePeriodEnd: $chargePeriodEnd
    })
    MERGE (ci:CostIntent {name: $costIntent})

    MERGE (c)-[:INCURRED_BY]->(r)
    MERGE (r)-[:USES_SERVICE]->(s)
    MERGE (c)-[:IN_TIMEFRAME]->(t)
    MERGE (c)-[:HAS_COST_INTENT]->(ci)
    """, **row)

with driver.session() as session:
    for _, row in df.iterrows():
        row_data = {
    "costRecordId": derive_cost_record_id(row),
    "effectiveCost": float(row["effectivecost"]),
    "billedCost": float(row["billedcost"]),
    "currency": row["billingcurrency"],
    "resourceId": str(row["resourceid"]),
    "serviceName": row["servicename"],
    "chargePeriodStart": str(row["chargeperiodstart"]),
    "chargePeriodEnd": str(row["chargeperiodend"]),
    "costIntent": derive_cost_intent(row["chargecategory"]),
}
        session.execute_write(ingest_row, row_data)

