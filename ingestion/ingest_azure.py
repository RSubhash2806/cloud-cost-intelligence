"""Azure cost data ingestion module."""

import pandas as pd
from typing import List, Dict

def load_azure_data(file_path: str) -> pd.DataFrame:
    """Load Azure cost data from Excel file."""
    df = pd.read_excel("data_samples/focusazure_anon_transformed.xls")

    # Normalize column names for consistency
    df.columns = [c.strip().lower() for c in df.columns]

    return df

def derive_cost_record_id(row: pd.Series) -> str:
    return f"{row['billingaccountid']}_{row['subaccountid']}_{row['resourceid']}_{row['chargeperiodstart']}_{row['chargecategory']}"

def derive_cost_intent_azure(charge_category: str, effective_cost: float, billed_cost: float) -> str:
    if not charge_category:
        return "Unknown"

    c = charge_category.lower()

    if "usage" in c:
        if billed_cost > 0 and effective_cost < billed_cost:
            return "CommitmentCoveredUsage"
        return "Usage"

    if "reservation" in c or "commitment" in c:
        return "CommitmentPurchase"

    if "discount" in c or "credit" in c:
        return "Adjustment"

    if "tax" in c:
        return "Tax"

    return "Other"

def transform_azure_data(data: pd.DataFrame) -> List[Dict]:
    """Transform Azure data to knowledge graph format."""
    records: List[Dict] = []

    for _, row in data.iterrows():
        record = {
            "costRecordId": derive_cost_record_id(row),
            "effectiveCost": float(row["effectivecost"]),
            "billedCost": float(row["billedcost"]),
            "currency": row.get("billingcurrency", "USD"),
            "resourceId": str(row["resourceid"]),
            "serviceName": row["servicename"],
            "chargePeriodStart": str(row["chargeperiodstart"]),
            "chargePeriodEnd": str(row["chargeperiodend"]),
            "costIntent": derive_cost_intent_azure(
                row["chargecategory"],
                float(row["effectivecost"]),
                float(row["billedcost"]),
            ),
        }
        records.append(record)

    return records

from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "infleratechnologies"


def ingest_to_graph(data: List[Dict]):
    """Ingest transformed data into Neo4j."""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

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
        for row in data:
            session.execute_write(ingest_row, row)

    driver.close()

if __name__ == "__main__":
    df = load_azure_data("data_samples/focusazure_anon_transformed.xls")
    records = transform_azure_data(df)
    ingest_to_graph(records)
