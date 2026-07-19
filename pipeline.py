"""
pipeline.py

Coordinates the complete question-answering pipeline by connecting
the classifier, retriever, response generator, and AI fallback.
"""
from classifier import get_best_module
from retriever import retrieve_card, retrieve_best_effort
from response_generator import generate_response
from search_engine import ask_ai

# Snippets that mean "the AI call itself failed" — used to detect
# when we should fall back to the knowledge base one more time instead
# of just showing the user an apology.
_AI_FAILURE_SIGNALS = (
    "couldn't reach the ai service",
    "temporarily overloaded",
    "request limit for the ai fallback",
    "fallback isn't set up",
)

COMMON_SPELLING = {
    "govermnent":"government",
    "goverment":"government",
    "regestration":"registration",
    "registeration":"registration",
    "licence":"license",
    "sale":"sales",
    "seles":"sales",
    "markting":"marketing",
    "finanace":"finance",
    "bussiness":"business",
    "swot":"swot",
    "gstt":"gst",
}
def answer_question(question):
    for wrong, correct in COMMON_SPELLING.items():
        question = question.replace(wrong, correct)
    module = get_best_module(question)

    if module != "unknown":
        topic_key, card = retrieve_card(module, question)
        if card:
            return generate_response(card, topic_key)

    # nothing hardcoded matched confidently -> ask the AI
    ai_answer = ask_ai(question)
    if not ai_answer:
       return (
        "I couldn't understand your question.\n\n"
        "Please check the spelling and try again."
    )

    if not any(signal in ai_answer.lower() for signal in _AI_FAILURE_SIGNALS):
        return ai_answer

    # AI is unavailable right now -> last resort: loosest possible
    # match across ALL knowledge modules, so we still say something
    # relevant instead of just the error message.
    fallback_module, fallback_key, fallback_card = retrieve_best_effort(question)
    if fallback_card:
        related = generate_response(fallback_card, fallback_key)
        return (
            "The AI service is briefly unavailable, but here's the "
            "closest related info from my knowledge base:\n\n" + related
        )

    return ai_answer


if __name__ == "__main__":
    print(answer_question("How do I price my gift boxes?"))
    print("\n---\n")
    print(answer_question("Do I need to trademark my shop's name?"))
