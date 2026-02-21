# Cloud Cost Knowledge Graph Ontology

## Entities

### Cost Entities
- **ServiceCost**: Represents cost associated with a service
- **ResourceCost**: Cost of individual cloud resources
- **Account**: Cloud account/subscription

### Resource Entities
- **Service**: AWS/Azure/GCP service (e.g., EC2, Storage)
- **Resource**: Individual infrastructure resources
- **Region**: Geographic region

### Time Entities
- **BillingPeriod**: Monthly billing period
- **TimePoint**: Specific time in cost data

## Relationships
- `INCURS`: Service incurs cost
- `USES`: Account uses service
- `LOCATED_IN`: Resource located in region
- `BILLED_IN`: Cost billed in period

## Purpose of the Ontology

The ontology models cloud costs as **financial events**, not just numerical records.
It is designed to:
- Prevent double counting
- Normalize AWS and Azure billing semantics
- Enable explainable cost analysis using graph traversal
- Support FinOps-style reasoning, not just reporting

## Dataset Observations & Cost Semantics

### AWS (FOCUS-aligned CUR)
- AWS represents cloud costs as multiple financial line items for the same resource.
- Usage, commitment-covered usage, commitment purchases, and adjustments appear as separate cost records.
- Commitment purchases and usage can coexist, which creates a risk of double counting.
- Vendor-specific fields (e.g., service code, usage type) explain *why* a cost exists, not *what* the cost is.

### Azure (FOCUS-aligned Cost Details)
- Azure embeds pricing and commitment benefits directly into SKU and meter metadata.
- Commitment benefits are often reflected as reduced or zero EffectiveCost rather than explicit discount line items.
- Unit price × quantity may not equal ContractedCost due to implicit benefits.

### Cross-Vendor Insight
Although both datasets conform to FOCUS 1.0, AWS externalizes financial mechanics while Azure internalizes them.
FOCUS normalizes the **outcome of cost**, not the **mechanism of pricing**.

## Core Modeling Decisions

### CostRecord
A CostRecord represents an **atomic financial event**, not a resource.
Multiple CostRecords may exist for the same resource within the same time period.

### Resource
A Resource represents a technical entity (VM, storage account, database, etc.).
It does not directly own cost — costs are incurred *by* resources.

### Charge & CostIntent
ChargeCategory is used to derive CostIntent:
- Usage
- CommitmentPurchase
- CommitmentCoveredUsage
- Adjustment
- Tax

CostIntent is critical to avoid double counting and to explain cost behavior.

### Vendor-Specific Attributes
AWS and Azure vendor fields are isolated under vendor-specific nodes.
These fields are used for explainability and audit, not aggregation logic.

## Explicit Non-Goals

- Raw billing data is not fully loaded into the graph; only semantic metadata is stored.
- Vendor-specific columns are not used to drive cost aggregation.
- The system avoids vendor-to-vendor direct cost comparison without semantic normalization.

## Ontology Classes

### CostRecord
Represents an atomic financial event.
Properties:
- costRecordId (unique)
- effectiveCost
- billedCost
- listCost
- contractedCost
- currency
- consumedQuantity
- consumedUnit

### Resource
Represents a technical entity that incurs cost.
Properties:
- resourceId
- resourceName
- resourceType

### Service
Represents a vendor service.
Properties:
- serviceName
- serviceCategory

### Account
Represents billing and sub-accounts.
Properties:
- billingAccountId
- billingAccountName
- subAccountId
- subAccountName

### TimeFrame
Represents billing and charge periods.
Properties:
- chargePeriodStart
- chargePeriodEnd
- billingPeriodStart
- billingPeriodEnd

### Charge
Represents the nature of a cost.
Properties:
- chargeCategory
- chargeFrequency
- chargeClass
- chargeDescription

### Location
Represents geographical deployment.
Properties:
- regionId
- regionName

### CostAllocation
Represents cost distribution logic.
Properties:
- allocationRuleName
- allocationMethod
- allocationTargetType
- allocationBasis
- isSharedCost

Derived Properties:
- allocatedCost
- sourceCostPool

### VendorSpecificAttributes
Abstract parent class.

Subclasses:
- AWSVendorAttributes
- AzureVendorAttributes

### PricingModel
Normalizes pricing semantics across vendors.
Examples:
- OnDemand
- ReservedInstance
- SavingsPlan
- AzureReservation
- Spot

### Commitment
Represents contractual cost commitments.
Properties:
- commitmentType
- commitmentStart
- commitmentEnd
- commitmentQuantity

### CostIntent
Derived semantic classification.
Values:
- Usage
- CommitmentPurchase
- CommitmentCoveredUsage
- Adjustment
- Tax

## Ontology Relationships

- (CostRecord)-[:INCURRED_BY]->(Resource)
- (Resource)-[:USES_SERVICE]->(Service)
- (Resource)-[:DEPLOYED_IN]->(Location)

- (CostRecord)-[:BELONGS_TO_ACCOUNT]->(Account)
- (CostRecord)-[:IN_TIMEFRAME]->(TimeFrame)
- (CostRecord)-[:HAS_CHARGE]->(Charge)

- (CostRecord)-[:HAS_VENDOR_ATTRS]->(VendorSpecificAttributes)

- (CostRecord)-[:HAS_COST_INTENT]->(CostIntent)
- (CostRecord)-[:USES_PRICING_MODEL]->(PricingModel)

- (CostRecord)-[:ALLOCATED_VIA]->(CostAllocation)

## Cardinality Constraints

- Each CostRecord relates to exactly one Resource.
- Each CostRecord relates to exactly one Charge.
- Each CostRecord relates to exactly one TimeFrame.
- A Resource may have many CostRecords.
- A Service may be used by many Resources.
- A CostAllocation may apply to many CostRecords.

## Validation & Derivation Rules

- effectiveCost ≥ 0
- billedCost ≥ 0
- contractedCost may differ from unitPrice × quantity due to commitments.
- CostIntent is derived using ChargeCategory and vendor attributes.
- Commitment purchases are excluded from usage analysis to avoid double counting.
