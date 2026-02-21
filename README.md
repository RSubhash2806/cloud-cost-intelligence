# Cloud Cost Intelligence using FOCUS 1.0

## Overview
This project implements a cloud cost intelligence system based on the **FOCUS 1.0 specification**, a **knowledge graph**, and a **graph-augmented reasoning pipeline**.  
The goal is to explain *why* cloud costs occur using grounded, dataset-specific reasoning rather than generic summaries.

The system focuses on **explainability, reliability, and auditability** of cloud cost analysis across multiple cloud providers.

---

## Problem Statement
Cloud billing data is:
- Vendor-specific
- High-volume
- Difficult to interpret without context

Most tools focus on reporting totals, but do not explain **cost drivers** or **optimization opportunities** in a reliable way.

This project addresses that gap by:
- Normalizing cloud billing data using FOCUS 1.0
- Modeling costs as a semantic knowledge graph
- Answering questions using graph-grounded reasoning (no hallucination)

---

## Datasets Used (Provided Files)
The system explicitly uses the following provided datasets:

- **AWS**:  
  `data_samples/aws_test-focus-00001.snappy_transformed.xls`

- **Azure**:  
  `data_samples/focusazure_anon_transformed.xls`

These files are ingested directly and are the sole source of cost data used in the analysis.

---

## Solution Architecture

### 1. Ontology (FOCUS 1.0 aligned)
Core concepts:
- `CostRecord`
- `Resource`
- `Service`
- `TimeFrame`
- `CostIntent` (Usage, CommitmentPurchase, Adjustment)

Defined in:
- `ontology/ontology.md`

---

### 2. Knowledge Graph (Neo4j)
- Costs, resources, services, and intents are modeled as nodes
- Relationships capture how costs are incurred and categorized
- Constraints ensure data integrity

Defined in:
- `graph/schema.cypher`
- `graph/constraints.cypher`

---

### 3. Data Ingestion
- AWS and Azure billing data are ingested separately
- Fields are mapped into a common semantic model
- Cost intent is derived deterministically from billing attributes

Implemented in:
- `ingestion/ingest_aws.py`
- `ingestion/ingest_azure.py`
- `ingestion/mappings.py`

---

### 4. Reasoning & RAG Pipeline
- Embeddings are generated **offline** and stored in the graph
- Runtime reasoning uses:
  - Graph aggregation
  - Dataset dominance analysis
  - Explicit absence detection
- No generative model hallucinates facts

Implemented in:
- `rag/retriever.py`
- `rag/generator.py`
- `rag/prompt_builder.py`

---

### 5. Confidence & Recommendations
- Each answer includes a **confidence score**
- Recommendations are generated only when supported by dataset signals
- Follow-up questions reuse the same reasoning signals for consistency

---

### 6. Minimal UI
- A simple Streamlit UI demonstrates interactive querying
- UI is intentionally minimal to emphasize reasoning correctness

Implemented in:
- `ui/app.py`

---

## Example Question & Answer

**Question**  
> Why did my cloud costs increase this month?

**Answer (derived from dataset)**  
- Usage accounts for ~100% of effective cost
- No commitment purchases are present
- No discounts or credits are applied  
→ Costs are driven entirely by on-demand usage

**Confidence**  
High — based on cost dominance and absence of alternative cost drivers

---

## Deliverables Checklist
- [x] Ontology definition (FOCUS 1.0 aligned)
- [x] Knowledge graph schema & constraints
- [x] AWS and Azure ingestion pipelines
- [x] Graph-augmented reasoning pipeline
- [x] Dataset-grounded explanations
- [x] Confidence scores and recommendations
- [x] Minimal interactive UI
- [x] References to provided datasets

---

## How to Run (High-Level)
1. Start Neo4j
2. Ingest AWS and Azure datasets
3. Generate embeddings (offline)
4. Run Streamlit UI

(Exact commands are documented in code comments.)

---

## References
- FOCUS 1.0 Specification
- Provided AWS and Azure transformed billing datasets
- Neo4j Graph Database
- Streamlit

---

## Notes
This project prioritizes **explainability and correctness** over UI polish or generic conversational responses.
