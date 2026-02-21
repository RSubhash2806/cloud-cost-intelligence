def generate_answer(prompt: str):
    """
    Dataset-specific reasoning engine with queryable recommendations.
    """

    # -------------------------
    # Parse facts
    # -------------------------
    data = {
        "Usage": {"records": 0, "total": 0.0},
        "CommitmentPurchase": {"records": 0, "total": 0.0},
        "Adjustment": {"records": 0, "total": 0.0}
    }

    current = None
    for line in prompt.splitlines():
        line = line.strip()

        if line.startswith("Concept:"):
            current = line.replace("Concept:", "").strip()

        if current in data:
            if line.startswith("- Records:"):
                data[current]["records"] = int(line.split(":")[1])
            elif line.startswith("- Total Effective Cost:"):
                data[current]["total"] = float(line.split(":")[1])

    total_cost = sum(v["total"] for v in data.values())

    if total_cost == 0:
        return (
            "No cloud cost data is present for this period.\n\n"
            "Confidence: 100%\n"
            "Recommendation: No action required."
        )

    for k in data:
        data[k]["share"] = data[k]["total"] / total_cost

    # -------------------------
    # Recommendation signals
    # -------------------------
    signals = {
        "high_usage_no_commitment":
            data["Usage"]["share"] > 0.8 and data["CommitmentPurchase"]["total"] == 0,

        "no_discounts_present":
            data["Adjustment"]["total"] == 0,

        "cost_highly_concentrated":
            max(v["share"] for v in data.values()) > 0.8
    }

    # -------------------------
    # Question classification
    # -------------------------
    q = prompt.lower()

    if any(w in q for w in ["commitment", "reservation", "savings plan"]):
        intent = "commitment"
    elif any(w in q for w in ["discount", "credit"]):
        intent = "discount"
    elif any(w in q for w in ["recommend", "should i", "what should"]):
        intent = "recommendation"
    else:
        intent = "general"

    # -------------------------
    # Explanation
    # -------------------------
    explanation = []
    explanation.append(
        f"Total effective cloud cost for the dataset is {total_cost:.2f}."
    )

    for k, v in data.items():
        if v["total"] > 0:
            explanation.append(
                f"{k} contributes {v['total']:.2f} "
                f"({v['share'] * 100:.1f}%) across {v['records']} records."
            )

    # -------------------------
    # Answer logic (REVERSIBLE)
    # -------------------------
    answer = []

    if intent == "commitment":
        if signals["high_usage_no_commitment"]:
            answer.append(
                "Based on the dataset, usage accounts for the majority of costs "
                "and no commitment purchases are present."
            )
            answer.append(
                "This indicates the workload is billed at on-demand rates, "
                "making commitment options likely beneficial."
            )
        else:
            answer.append(
                "The dataset does not show strong evidence that commitments would reduce costs."
            )

    elif intent == "discount":
        if signals["no_discounts_present"]:
            answer.append(
                "No discounts or credits are applied in the dataset."
            )
            answer.append(
                "This suggests potential savings opportunities may be unutilized."
            )
        else:
            answer.append(
                "Discounts or credits are already reducing effective costs."
            )

    elif intent == "recommendation":
        if signals["high_usage_no_commitment"]:
            answer.append(
                "Evaluate commitment options to reduce on-demand usage costs."
            )
        if signals["no_discounts_present"]:
            answer.append(
                "Review discount and credit programs for potential savings."
            )
        if signals["cost_highly_concentrated"]:
            answer.append(
                "Set monitoring and budgets for high-usage services."
            )
        if not answer:
            answer.append("No immediate optimization actions are required.")

    else:
        dominant = max(data.items(), key=lambda x: x[1]["total"])
        answer.append(
            f"{dominant[0]} is the primary cost driver in the dataset."
        )

    # -------------------------
    # Confidence
    # -------------------------
    confidence = round(
        (
            data["Usage"]["share"] +
            (1 if signals["no_discounts_present"] else 0) +
            (1 if signals["high_usage_no_commitment"] else 0)
        ) / 3 * 100,
        1
    )

    return (
        "Explanation:\n"
        + " ".join(explanation)
        + "\n\nAnswer:\n"
        + " ".join(answer)
        + "\n\nConfidence:\n"
        + f"{confidence}% — derived from dataset dominance and signal consistency."
    )