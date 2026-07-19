"""
classifier.py

Takes a raw question typed by the user and decides which knowledge
module (finance, sales, risk, etc.) it belongs to.

How it works:
1. For every module, count how many of its keywords appear in the
   question (as whole words/phrases, not substrings — so "sale" in
   keywords doesn't accidentally match "wholesale").
2. Multi-word phrases (e.g. "emergency fund") count MORE than single
   words, since they're a stronger signal of the topic.
3. If a word isn't an EXACT match (e.g. the user typed "governemt"
   instead of "government"), we also try a fuzzy match — this catches
   typos so a single misspelled word doesn't derail classification.
4. The module with the highest score wins. If nothing scores above
   the threshold, return None — this tells the pipeline to fall back
   to search_engine.py (the AI API) instead of guessing wrong.
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
