from neo4j import GraphDatabase
from rag.prompt_builder import build_prompt
from rag.generator import generate_answer

# -------------------------
# Neo4j configuration
# -------------------------
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "infleratechnologies"  # <-- replace

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# -------------------------
# Lightweight intent routing (NO ML AT RUNTIME)
# -------------------------
def retrieve_relevant_cost_intents(question: str, k: int = 3):
    """
    Rule-based intent routing for UI demo.
    This is intentionally deterministic and avoids ML at runtime.
    """

    q = question.lower()

    # Question-type routing
    if any(word in q for word in ["increase", "went up", "spike", "higher"]):
        intents = ["Usage"]

    elif any(word in q for word in ["commitment", "reservation", "savings plan"]):
        intents = ["CommitmentPurchase", "Usage"]

    elif any(word in q for word in ["discount", "credit", "adjustment"]):
        intents = ["Adjustment"]

    elif any(word in q for word in ["what", "breakdown", "contributing", "most"]):
        intents = ["Usage", "CommitmentPurchase", "Adjustment"]

    else:
        intents = ["Usage"]

    cypher = """
    MATCH (ci:CostIntent)
    WHERE ci.name IN $intents
    RETURN ci.name AS name, ci.description AS description
    """

    with driver.session(database="neo4j") as session:
        return session.run(
            cypher,
            intents=intents
        ).data()


# -------------------------
# Graph-grounded facts
# -------------------------
def fetch_grounded_cost_facts(intent_name: str):
    cypher = """
    MATCH (c:CostRecord)-[:HAS_COST_INTENT]->(ci:CostIntent {name: $intent})
    RETURN
        count(c) AS recordCount,
  sum(c.effectiveCost) AS totalEffectiveCost,
  sum(c.billedCost) AS totalBilledCost,
  avg(c.effectiveCost) AS avgEffectiveCost,
  min(c.effectiveCost) AS minEffectiveCost,
  max(c.effectiveCost) AS maxEffectiveCost
    """

    with driver.session(database="neo4j") as session:
        record = session.run(cypher, intent=intent_name).single()

    return dict(record) if record else {}


# -------------------------
# End-to-end RAG
# -------------------------
def answer_question(user_question: str):
    concept_hits = retrieve_relevant_cost_intents(user_question)

    facts_by_concept = {}
    for hit in concept_hits:
        facts_by_concept[hit["name"]] = fetch_grounded_cost_facts(hit["name"])

    prompt = build_prompt(
        user_question=user_question,
        concept_hits=concept_hits,
        facts_by_concept=facts_by_concept
    )

    return generate_answer(prompt)
