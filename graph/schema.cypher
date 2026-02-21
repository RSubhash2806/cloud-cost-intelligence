// Core Relationships

// CostRecord relationships
MATCH (c:CostRecord), (r:Resource)
MERGE (c)-[:INCURRED_BY]->(r);

MATCH (c:CostRecord), (a:Account)
MERGE (c)-[:BELONGS_TO_ACCOUNT]->(a);

MATCH (c:CostRecord), (t:TimeFrame)
MERGE (c)-[:IN_TIMEFRAME]->(t);

MATCH (c:CostRecord), (ch:Charge)
MERGE (c)-[:HAS_CHARGE]->(ch);

// Resource relationships
MATCH (r:Resource), (s:Service)
MERGE (r)-[:USES_SERVICE]->(s);

MATCH (r:Resource), (l:Location)
MERGE (r)-[:DEPLOYED_IN]->(l);

// Vendor-specific
MATCH (c:CostRecord), (v:VendorSpecificAttributes)
MERGE (c)-[:HAS_VENDOR_ATTRS]->(v);

// Cost semantics
MATCH (c:CostRecord), (ci:CostIntent)
MERGE (c)-[:HAS_COST_INTENT]->(ci);

MATCH (c:CostRecord), (pm:PricingModel)
MERGE (c)-[:USES_PRICING_MODEL]->(pm);

// Allocation
MATCH (c:CostRecord), (ca:CostAllocation)
MERGE (c)-[:ALLOCATED_VIA]->(ca);
