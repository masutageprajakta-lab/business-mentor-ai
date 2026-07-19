"""
response_generator.py

Takes the card retriever.py found and turns the raw dict into a
readable, friendly answer. Handles both card formats you have in your
knowledge files ("tips": [...] and the older "ai_tip": "...").
"""


def generate_response(card, topic_key=None):
    if not card:
        return None

    lines = []

    if topic_key:
        lines.append(f"**{topic_key.title()}**\n")

    lines.append(card.get("definition", "").strip())

    if card.get("importance"):
        lines.append(f"\n**Why it matters:** {card['importance']}")

    if card.get("example"):
        lines.append(f"\n**Example:** {card['example']}")

    if card.get("common_mistakes"):
        mistakes = "\n".join(f"- {m}" for m in card["common_mistakes"])
        lines.append(f"\n**Common mistakes to avoid:**\n{mistakes}")

    # support both "tips" (list) and older "ai_tip" (single string)
    tips = card.get("tips")
    if not tips and card.get("ai_tip"):
        tips = [card["ai_tip"]]

    if tips:
        tip_lines = "\n".join(f"- {t}" for t in tips)
        lines.append(f"\n**Tips:**\n{tip_lines}")

    return "\n".join(lines)
