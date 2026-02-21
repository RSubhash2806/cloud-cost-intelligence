from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "infleratechnologies"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
model = SentenceTransformer(MODEL_NAME)


def embed_and_store(label: str, text_field: str = "description"):
    query = f"""
    MATCH (n:{label})
    WHERE n.{text_field} IS NOT NULL
    RETURN id(n) AS node_id, n.{text_field} AS text
    """

    with driver.session() as session:
        records = session.run(query).data()

        for r in records:
            embedding = model.encode(r["text"]).tolist()

            session.run(
                f"""
                MATCH (n:{label})
                WHERE id(n) = $id
                SET n.embedding = $embedding
                """,
                id=r["node_id"],
                embedding=embedding,
            )


if __name__ == "__main__":
    embed_and_store("CostIntent")
    embed_and_store("Service")
    embed_and_store("CanonicalService")
    embed_and_store("Charge")
