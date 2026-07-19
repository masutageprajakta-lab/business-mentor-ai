"""
classifier.py

Classifies a user's business-related question into the most relevant
knowledge module (such as finance, marketing, sales, legal, or risk).

Working:
1. Compares the user's question against predefined keywords for each module.
2. Gives higher importance to multi-word phrases (e.g., "emergency fund")
   because they provide stronger context.
3. Uses fuzzy matching to handle minor spelling mistakes and typing errors.
4. Returns the module with the highest confidence score.
5. If no suitable module is found, the system returns None so the
   application can use the AI fallback instead of making an incorrect match.
"""

import re
from difflib import SequenceMatcher
from keywords import KEYWORDS

FUZZY_THRESHOLD = 0.82  # how close a word must be to count as a typo-match


def _fuzzy_word_match(word, question_words):
    for qw in question_words:
        if abs(len(qw) - len(word)) > 2:
            continue  # quick skip, avoids comparing very different lengths
        if SequenceMatcher(None, word, qw).ratio() >= FUZZY_THRESHOLD:
            return True
    return False


def _score_module(question_lower, terms):
    question_words = question_lower.split()
    score = 0
    for term in terms:
        term_lower = term.lower()
        term_words = term_lower.split()
        weight = 2 if len(term_words) > 1 else 1

        pattern = r"\b" + re.escape(term_lower) + r"\b"
        if re.search(pattern, question_lower):
            score += weight
        elif all(_fuzzy_word_match(tw, question_words) for tw in term_words):
            # every word of the phrase has a close-enough typo match
            score += weight * 0.75  # slightly discount fuzzy matches
    return score


def classify_question(question, keywords=KEYWORDS):
    """
    Returns a list of (module_name, score) sorted highest first.
    Empty list if no module matched at all.
    """
    q = question.lower()
    results = []
    for module, terms in keywords.items():
        score = _score_module(q, terms)
        if score > 0:
            results.append((module, score))
    results.sort(key=lambda pair: pair[1], reverse=True)
    return results


def get_best_module(question, min_score=1):
    ranked = classify_question(question)

    if not ranked:
        return None

    if ranked[0][1] < min_score:
        return None

    return ranked[0][0]


if __name__ == "__main__":
    # quick manual test
    tests = [
        "How do I price my gift boxes?",
        "Do I need GST registration for my shop?",
        "What if my competitor undercuts my prices?",
        "I feel too shy to talk to customers",
        "what are governemt scheme for buisness",  # typos, should still -> legal
        "What's the weather today?",  # should return None -> fallback
    ]
    for t in tests:
        print(t, "->", get_best_module(t))
