// CostRecord
CREATE CONSTRAINT costrecord_id_unique IF NOT EXISTS
FOR (c:CostRecord)
REQUIRE c.costRecordId IS UNIQUE;

// Resource
CREATE CONSTRAINT resource_id_unique IF NOT EXISTS
FOR (r:Resource)
REQUIRE r.resourceId IS UNIQUE;

// Service
CREATE CONSTRAINT service_name_unique IF NOT EXISTS
FOR (s:Service)
REQUIRE s.serviceName IS UNIQUE;

// Account
CREATE CONSTRAINT billing_account_unique IF NOT EXISTS
FOR (a:Account)
REQUIRE a.billingAccountId IS UNIQUE;

// TimeFrame
CREATE CONSTRAINT timeframe_unique IF NOT EXISTS
FOR (t:TimeFrame)
REQUIRE (t.chargePeriodStart, t.chargePeriodEnd) IS UNIQUE;

// Location
CREATE CONSTRAINT region_unique IF NOT EXISTS
FOR (l:Location)
REQUIRE l.regionId IS UNIQUE;

// CostAllocation
CREATE CONSTRAINT allocation_rule_unique IF NOT EXISTS
FOR (ca:CostAllocation)
REQUIRE ca.allocationRuleName IS UNIQUE;
