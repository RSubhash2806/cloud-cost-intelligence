# Cloud Cost Intelligence using FOCUS 1.0

## Overview
This project implements a **Cloud Cost Intelligence system** based on the **FOCUS 1.0 specification**, a **Neo4j knowledge graph**, and a **graph-augmented reasoning pipeline**.

The objective of this system is to **explain why cloud costs occur** using **dataset-grounded reasoning**, rather than providing generic summaries or dashboards.

The solution prioritizes:
- Explainability  
- Reliability  
- Auditability  

across multiple cloud providers.

---

## Problem Statement
Cloud billing data is:
- Vendor-specific  
- High-volume  
- Difficult to interpret without context  

Most existing tools focus on reporting totals, but they do not clearly explain:
- What is driving costs  
- Whether costs are avoidable  
- What actions can be taken  

This project addresses the problem by:
- Normalizing cloud billing data using **FOCUS 1.0**
- Modeling cost data as a **semantic knowledge graph**
- Answering questions using **graph-grounded reasoning (no hallucination)**

---

## Datasets Used (Provided Files)

The system uses **only the datasets provided as part of the assignment**:

### AWS Dataset

data_samples/aws_test-focus-00001.snappy_transformed.xls


### Azure Dataset

data_samples/focusazure_anon_transformed.xls


These datasets are ingested directly and act as the **single source of truth** for all analysis and explanations.

---

## Solution Architecture

### 1. Ontology (FOCUS 1.0 Aligned)
Core concepts modeled:
- CostRecord  
- Resource  
- Service  
- TimeFrame  
- CostIntent (Usage, CommitmentPurchase, Adjustment)

Defined in:

ontology/ontology.md


---

### 2. Knowledge Graph (Neo4j)
- Costs, resources, services, and intents are modeled as nodes  
- Relationships capture how costs are incurred and categorized  
- Constraints ensure data integrity  

Defined in:

graph/schema.cypher
graph/constraints.cypher


---

### 3. Data Ingestion
- AWS and Azure billing data are ingested separately  
- Fields are mapped into a common semantic model  
- Cost intent is derived deterministically from billing attributes  

Implemented in:

ingestion/ingest_aws.py
ingestion/ingest_azure.py
ingestion/mappings.py


---

### 4. Reasoning & RAG Pipeline
- Embeddings are generated **offline** and stored in the graph  
- Runtime reasoning uses:
  - Graph aggregation  
  - Dataset dominance analysis  
  - Explicit absence detection  

No generative model fabricates facts; all answers are derived from the dataset.

Implemented in:

rag/retriever.py
rag/generator.py
rag/prompt_builder.py


---

### 5. Confidence & Recommendations
- Each answer includes a **confidence score**
- Recommendations are generated **only when supported by data**
- Follow-up questions reuse the same reasoning signals for consistency

---

### 6. Minimal UI
A simple **Streamlit UI** is provided to demonstrate interactive querying.

The UI is intentionally minimal to focus on reasoning correctness rather than presentation.

Implemented in:

ui/app.py


---

## Example Question and Answer

**Question**  
Why did my cloud costs increase this month?

**Answer (derived from dataset)**  
- Usage accounts for ~100% of effective cost  
- No commitment purchases are present  
- No discounts or credits are applied  

**Conclusion:**  
Costs are driven entirely by on-demand usage.

**Confidence:**  
High — based on cost dominance and absence of alternative cost drivers.

---

## Deliverables Checklist
- Ontology definition (FOCUS 1.0 aligned)  
- Knowledge graph schema and constraints  
- AWS and Azure ingestion pipelines  
- Graph-augmented reasoning pipeline  
- Dataset-grounded explanations  
- Confidence scores and recommendations  
- Minimal interactive UI  
- Explicit references to provided datasets  

---

## How to Run the Project (Step-by-Step)

> This project is intended as a **working prototype** to demonstrate system design and reasoning.

### Prerequisites
- Python 3.9 or above  
- Neo4j Desktop (local instance)  
- Git  

---

### Step 1: Clone the Repository

git clone https://github.com/RSubhash2806/cloud-cost-intelligence.git
cd cloud-cost-intelligence
Step 2: Create and Activate Virtual Environment
python -m venv venv

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Start Neo4j

Open Neo4j Desktop

Start a local Neo4j instance

Ensure Bolt is running on:

bolt://localhost:7687
Step 5: Apply Graph Schema and Constraints

Open Neo4j Browser and run:

:source graph/schema.cypher
:source graph/constraints.cypher
Step 6: Ingest Cloud Cost Data
AWS
python -m ingestion.ingest_aws
Azure
python -m ingestion.ingest_azure
Step 7: Generate Embeddings
python embeddings/generate_embeddings.py
Step 8: Run the Demo UI
streamlit run ui/app.py

You can now ask questions such as:

Why did my cloud costs increase?

Which cost category contributes the most?

References

FOCUS 1.0 Specification

Provided AWS and Azure transformed billing datasets

Neo4j Graph Database

Streamlit
