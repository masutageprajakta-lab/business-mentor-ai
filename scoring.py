
print("NEW SCORING FILE LOADED")
from search_engine import ask_ai

questions = {
    "business_idea": "What's your business idea?",
    "budget": "What's your starting budget (in ₹)?",
    "funding_source": "Where is this budget mainly coming from? (own savings / loan / family support / mixed)",
    "other_income": "Do you have another steady source of income right now? (yes / no)",
    "target_customer": "Who are your target customers?",
    "competitor_knowledge": "Have you seen any shop near you doing the same business? (no / 1-2 / 3 and more)",
    "customer_validation": "Have you talked to potential customers about this idea? (no / a few / many)",
    "differentiation": "Do you offer something different from nearby competitors? (not sure / a little / yes, clearly)",
    "emergency_fund": "What if your business faces a loss for a few months — do you have emergency funds? (yes / no / some money)",
    "risk_taking": "Are you comfortable taking risks? (low / medium / high)",
    "communication": "How comfortable are you talking to customers? (shy / okay / good)",
    "prior_experience": "Have you run or worked closely in any business before? (none / some / significant)",
    "time_commitment": "How much time can you give this business right now? (side project / part-time / full-time)",
}


def _budget_points(budget):

    if budget<=0:
        return -20

    elif budget<5000:
        return -18

    elif budget<20000:
        return -15

    elif budget<50000:
        return -10

    elif budget<100000:
        return 0

    elif budget<300000:
        return 10

    elif budget<500000:
        return 15

    elif budget<1000000:
        return 18

    else:
        return 20


def compute_scores(user):
    scores = {
        "market": 50,
        "financial": 50,
        "founder": 50,
    }

    budget = user.get("budget") or 0
    scores["financial"] += _budget_points(budget)

    if user.get("emergency_fund") == "yes":
        scores["financial"] += 15
    elif user.get("emergency_fund") == "some money":
        scores["financial"] += 7
    else:
        scores["financial"] -= 5

    funding_source = (user.get("funding_source") or "").lower()
    if funding_source == "own savings":
        scores["financial"] += 8
    elif funding_source == "family support":
        scores["financial"] += 5
    elif funding_source == "mixed":
        scores["financial"] += 3
    elif funding_source == "loan":
        scores["financial"] -= 5  # repayment pressure from day one

    other_income = (user.get("other_income") or "").lower()
    if other_income == "yes":
        scores["financial"] += 7  # safety net if the business is slow to start

    competitor_knowledge = user.get("competitor_knowledge")
    if competitor_knowledge=="no":
       scores["market"]-=5

    elif competitor_knowledge=="1-2":
       scores["market"]+=8

    elif competitor_knowledge=="3 and more":
        scores["market"]+=15

    target = user.get("target_customer", "").strip()

    if len(target.split()) >= 2:
       scores["market"] += 10
    else:
       scores["market"] += 0
    customer_validation = (user.get("customer_validation") or "").lower()
    if customer_validation == "no":
        scores["market"] -= 10
    elif customer_validation == "a few":
        scores["market"] += 5
    elif customer_validation=="many":
        scores["market"]+=15 # idea untested against real customers

    differentiation = (user.get("differentiation") or "").lower()
    if differentiation == "a little":
        scores["market"] += 5
    elif differentiation == "yes, clearly":
        scores["market"] += 12

    risk_taking = (user.get("risk_taking") or "").lower()
    if risk_taking == "low":
        scores["founder"] += 5
    elif risk_taking == "medium":
        scores["founder"] += 15
    elif risk_taking == "high":
        scores["founder"] += 10

    communication = (user.get("communication") or "").lower()
    if communication=="shy":
      scores["founder"]-=5

    elif communication=="okay":
      scores["founder"]+=8

    elif communication=="good":
      scores["founder"]+=15

    prior_experience = (user.get("prior_experience") or "").lower()
    if prior_experience == "some":
        scores["founder"] += 8
    elif prior_experience == "significant":
        scores["founder"] += 15

    time_commitment = (user.get("time_commitment") or "").lower()
    if time_commitment == "part-time":
        scores["founder"] += 5
    elif time_commitment == "full-time":
        scores["founder"] += 10

    # keep every score within 0-100
    for key in scores:
        scores[key] = max(0, min(100, scores[key]))
    scores["overall"] = round(
    (scores["financial"] +
     scores["market"] +
     scores["founder"]) / 3
)    

    return scores

def get_level(score):
    if score >= 80:
        return "🟢 Excellent"
    elif score >= 65:
        return "🟡 Good"
    elif score >= 50:
        return "🟠 Average"
    else:
        return "🔴 Needs Improvement"
    
def generate_report(user, scores):

    lines=[]

    lines.append("# 📊 Business Readiness Report\n")

    lines.append(f"### Business Idea")
    lines.append(user["business_idea"])
    lines.append("")

    lines.append(f"### Overall Readiness : **{scores['overall']}/100**")
    lines.append(get_level(scores["overall"]))
    lines.append("")

    lines.append("| Category | Score | Status |")
    lines.append("|----------|-------|--------|")
    lines.append(f"| Financial | {scores['financial']}/100 | {get_level(scores['financial'])} |")
    lines.append(f"| Market | {scores['market']}/100 | {get_level(scores['market'])} |")
    lines.append(f"| Founder | {scores['founder']}/100 | {get_level(scores['founder'])} |")

    return "\n".join(lines)

RECOMMENDATION_SYSTEM_PROMPT = (
    "You are a warm, encouraging business mentor for first-generation "
    "entrepreneurs in India. You'll be given a founder's business idea "
    "and three readiness scores out of 100 (financial, market, founder). "
    "Write 3-5 short, specific, practical next-step recommendations "
    "tailored to THIS founder's actual weak spots — not generic advice. "
    "Reference their business idea directly where relevant. Use simple "
    "language, a bullet per recommendation, no long intro or outro."
)


def generate_ai_recommendations(user, scores):
    """
    Builds a prompt from this specific founder's answers and scores,
    and asks Gemini for tailored next-step recommendations — instead
    of the same 3 canned lines for everyone.
    Falls back to simple rule-based lines if the AI call fails.
    """
    prompt = (
        f"Business idea: {user.get('business_idea', 'not specified')}\n"
        f"Budget: ₹{user.get('budget', 0)}\n"
        f"Target customer: {user.get('target_customer', 'not specified')}\n"
        f"Competitors nearby: {user.get('competitor_knowledge', 'not specified')}\n"
        f"Emergency fund: {user.get('emergency_fund', 'not specified')}\n"
        f"Risk comfort: {user.get('risk_taking', 'not specified')}\n"
        f"Comfort talking to customers: {user.get('communication', 'not specified')}\n"
        f"Prior business experience: {user.get('prior_experience', 'not specified')}\n"
        f"Time commitment: {user.get('time_commitment', 'not specified')}\n"
        f"Scores — Financial: {scores['financial']}/100, "
        f"Market: {scores['market']}/100, Founder: {scores['founder']}/100\n\n"
        "Give this founder tailored next steps, in order of urgency — "
        "if the budget is very low relative to their business idea, "
        "address that first before anything else."
    )

    try:
      answer = ask_ai(
        prompt,
        system_prompt=RECOMMENDATION_SYSTEM_PROMPT
      )

      if answer and len(answer.strip()) > 30:
        return answer

    except Exception:
      pass

    return _fallback_recommendations(user, scores)


def _fallback_recommendations(user,scores):

    

    recommendations=[]

    # ---------- Financial ----------

    if scores["financial"]<50:

        recommendations.append(
            "💰 Your financial readiness is low. Consider starting with a smaller version of your business."
        )

        recommendations.append(
            "💰 Build an emergency fund before investing heavily."
        )

    elif scores["financial"]<70:

        recommendations.append(
            "💰 Keep a monthly budget and track every business expense."
        )



    # ---------- Market ----------

    if scores["market"]<50:

        recommendations.append(
            "📊 Talk to at least 20 potential customers before launching."
        )

        recommendations.append(
            "📊 Study nearby competitors and identify your unique selling point."
        )

    elif scores["market"]<70:

        recommendations.append(
            "📊 Improve your understanding of customer needs and competitors."
        )



    # ---------- Founder ----------

    if scores["founder"]<50:

        recommendations.append(
            "🧠 Improve your communication and confidence by interacting with customers regularly."
        )

        recommendations.append(
            "🧠 Start with small calculated risks instead of avoiding challenges."
        )

    elif scores["founder"]<70:

        recommendations.append(
            "🧠 Continue improving leadership and decision-making skills."
        )



    # ---------- Business specific ----------

    idea=user.get("business_idea","").lower()

    if "gift" in idea:

        recommendations.append(
            "🎁 Research trending gift products before purchasing inventory."
        )

    elif "restaurant" in idea:

        recommendations.append(
            "🍽️ Focus on food quality and customer reviews."
        )

    elif "clothing" in idea:

        recommendations.append(
            "👕 Keep inventory small initially and monitor fast-selling designs."
        )



    if scores["overall"]>=80:

        recommendations.append(
            "🚀 Your business shows strong readiness. Focus on execution."
        )



    if not recommendations:

        recommendations.append(
            "✅ Your business is in a good position. Continue validating your idea and start with a small launch."
        )



    return "\n\n".join(recommendations)
