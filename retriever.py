"""
retriever.py

Once classifier.py has decided WHICH module a question belongs to
(e.g. "finance"), retriever.py's job is to find the single best card
INSIDE that module to answer the question.

Each module is a dict like:
    {
      "emergency fund": {"definition": ..., "importance": ..., ...},
      "cash flow": {...},
    }

We compare the user's question against each card's topic name +
definition text, using simple word-overlap plus a fuzzy string match
(difflib), and return the best one if it clears a minimum score.
"""

from difflib import SequenceMatcher, get_close_matches

from knowledge.business import business_knowledge
from knowledge.communication import communication_knowledge
from knowledge.finance import finance_knowledge
from knowledge.growth import growth_knowledge
from knowledge.legal import legal_knowledge
from knowledge.market import market_knowledge
from knowledge.marketing import marketing_knowledge
from knowledge.mindset import mindset_knowledge
from knowledge.operations import operations_knowledge
from knowledge.risk import risk_knowledge
from knowledge.sales import sales_knowledge
from knowledge_aliases import CARD_ALIASES

# Central registry: classifier's module name -> that module's dict.
# This is the one place that has to know every module that exists.
MODULES = {
    "business": business_knowledge,
    "communication": communication_knowledge,
    "finance": finance_knowledge,
    "growth": growth_knowledge,
    "legal": legal_knowledge,
    "market": market_knowledge,
    "marketing": marketing_knowledge,
    "mindset": mindset_knowledge,
    "operations": operations_knowledge,
    "risk": risk_knowledge,
    "sales": sales_knowledge,
}


def _similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# generic words that shouldn't count toward "this card matches" —
# without this, "what is X" cards can wrongly outscore the real match
# just because they share filler words with the question.
STOPWORDS = {
    "a", "an", "the", "is", "are", "do", "does", "how", "what", "when",
    "where", "why", "who", "should", "i", "my", "for", "of", "to", "in",
    "on", "and", "or", "it", "be", "can", "you", "your", "me", "we",
}


def _content_words(text):
    return {w for w in text.lower().split() if w not in STOPWORDS}


def _fuzzy_overlap(q_words, s_words, threshold=0.90):
    """
    Like set overlap, but a word counts as matching even with small
    typos/plurals (e.g. "gsts" vs "gst", "registeration" vs
    "registration") — not just an exact string match.
    """
    if not q_words:
        return 0.0
    matched = 0
    for qw in q_words:
        if qw in s_words:
            matched += 1
            continue
        for sw in s_words:
            if SequenceMatcher(None, qw, sw).ratio() >= threshold:
                matched += 1
                break
    return matched / len(q_words)


def retrieve_card(module_name, question, min_score=0.22):
    """
    Returns (topic_key, card_dict) for the best-matching card in the
    given module, or (None, None) if nothing matches well enough.
    """
    module = MODULES.get(module_name)
    if not module:
        return None, None

    q_lower = question.lower().replace("_", " ").replace("-", " ")
    COMMON_TYPOS = {
    "saled": "sales",
    "salee": "sales",
    "saless": "sales",
    "sellling": "selling",

    "govermnent": "government",
    "goverment": "government",
    "governement": "government",

    "custmer": "customer",
    "custmor": "customer",

    "markting": "marketing",

    "invesment": "investment",

    "profitt": "profit",

    "gstt": "gst",
    "swott": "swot",
     }

    for wrong, correct in COMMON_TYPOS.items():
      q_lower = q_lower.replace(wrong, correct)
    q_words = _content_words(q_lower)
    # Check aliases before fuzzy matching
    for alias, actual_key in CARD_ALIASES.items():
      if alias in q_lower and actual_key in module:
        return actual_key, module[actual_key]
      
  

    # -------- Small spelling correction --------

    all_words = []

    for topic in module.keys():
        all_words.extend(
            topic.lower().replace("_", " ").split()
    )

    corrected_words = []

    for word in q_words:

       match = get_close_matches(
        word,
        all_words,
        n=1,
        cutoff=0.82
    )

       if match:
         corrected_words.append(match[0])
       else:
          corrected_words.append(word)

    q_words = set(corrected_words)   
     # First pass: find any topic names that literally appear in the
    # question (e.g. question mentions "business idea" and a card is
    # named exactly that). If several match ("business" AND "business
    # idea" both appear), prefer the longest/most specific one.
    substring_matches = []

    for topic_key, card in module.items():
      topic_lower = topic_key.lower().replace("_", " ")
      
      if topic_lower == q_lower.strip():
          return topic_key, card
      if f" {topic_lower} " in f" {q_lower} ":
        substring_matches.append((topic_key, card))

    if substring_matches:
        return max(substring_matches, key=lambda pair: len(pair[0]))

    best_key = None
    best_card = None
    best_score = 0

    for topic_key, card in module.items():

         topic_lower = topic_key.lower().replace("_", " ")

         searchable = (
            topic_lower
            + " "
            + card.get("definition", "")
          ).lower()

         s_words = _content_words(searchable)

         overlap = _fuzzy_overlap(q_words, s_words)
         name_sim = _similarity(q_lower, topic_lower)

         score = max(overlap, name_sim)

    # Ignore weak matches
         if score < 0.60:
           continue

         if score > best_score:
           best_score = score
           best_key = topic_key
           best_card = card

    if best_score < max(min_score,0.72):
        return None, None

    return best_key, best_card


def retrieve_best_effort(question):
    """
    Last-resort search across EVERY module, with a much lower
    confidence bar than retrieve_card(). Only meant to be used when
    the AI fallback itself is unavailable (rate limited / overloaded) —
    so the app can still say something useful and on-topic instead of
    a dead-end error message.

    Returns (module_name, topic_key, card_dict) or (None, None, None).
    """
    best_module, best_key, best_card, best_score = None, None, None, 0.0

    for module_name, module in MODULES.items():
        key, card = retrieve_card(module_name, question, min_score=0.10)
        if not card:
            continue
        # retrieve_card doesn't return its own score, so re-score
        # lightly here just to compare across modules
        q_words = _content_words(question.lower().replace("_", " ").replace("-", " "))
        searchable = key + " " + card.get("definition", "")
        score = _fuzzy_overlap(q_words, _content_words(searchable))
        if score >= best_score:
            best_module, best_key, best_card, best_score = module_name, key, card, score

    return best_module, best_key, best_card
