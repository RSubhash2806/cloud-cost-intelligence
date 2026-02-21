def build_prompt(user_question: str, concept_hits, facts_by_concept):
    context_blocks = []

    for hit in concept_hits:
        name = hit["name"]
        desc = hit["description"]
        facts = facts_by_concept.get(name, {})

        block = f"""
Concept: {name}
Meaning: {desc}
Facts:
- Records: {facts.get('recordCount', 0)}
- Total Effective Cost: {facts.get('totalEffectiveCost', 0)}
- Total Billed Cost: {facts.get('totalBilledCost', 0)}
"""
        context_blocks.append(block)

    context = "\n".join(context_blocks)

    prompt = f"""
You are a FinOps-aware assistant.

Answer the question using ONLY the context below.
Explain the reasoning clearly and avoid speculation.

Context:
{context}

Question:
{user_question}

Answer:
"""

    return prompt
