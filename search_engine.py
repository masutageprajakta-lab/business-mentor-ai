"""
search_engine.py

Fallback for any question the classifier/retriever couldn't confidently
answer from your hardcoded knowledge files. Instead of saying "I don't
know", this calls Google's Gemini API (free tier) to generate an answer
in the same friendly, beginner-first tone as your knowledge cards.

SETUP (one-time, no credit card needed):
1. Go to https://aistudio.google.com/app/apikey and sign in with any
   Google account.
2. Click "Create API key". Copy it — it looks like: AIzaSy...
3. Install the SDK:  pip install google-genai
4. Store the key as an environment variable (never paste it directly
   into this file):
       Mac/Linux:   export GEMINI_API_KEY="AIzaSy..."
       Windows:     setx GEMINI_API_KEY "AIzaSy..."
                    (then close and reopen your terminal)
   Streamlit Cloud deployment: add GEMINI_API_KEY under the app's
   "Secrets" panel instead — st.secrets below picks it up automatically.

Free tier limits (as of mid-2026): roughly 1,500 requests/day on Flash
models — more than enough for a project/demo. Note: Google retires
specific model versions periodically (this file was updated in July
2026 after "gemini-2.5-flash" was retired for new users ahead of its
originally announced date) — using the "gemini-flash-latest" alias
below means Google always routes you to a current free Flash model
instead of one that can suddenly disappear.
"""

import os
import time

try:
    import streamlit as st
except ImportError:
    st = None

from google import genai


def _get_api_key():
    # Prefer Streamlit secrets when running inside a deployed app,
    # fall back to a plain environment variable for local testing.
    if st is not None:
        try:
            return st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    return os.environ.get("GEMINI_API_KEY")


SYSTEM_PROMPT = (
    "You are a warm, encouraging business mentor for first-generation "
    "entrepreneurs in India who are just starting out and may have no "
    "prior business background. Explain things in simple, jargon-free "
    "language, like you would to a smart friend who is new to business. "
    "Keep answers under 150 words. Use a short example where it helps. "
    "End with one clear, practical next step."
)

# Simple in-memory cache: same question asked twice in one running app
# reuses the first answer instead of calling the API again. This is
# mainly useful for demos/interviews where you might re-ask the same
# thing, or accidentally double-click — it does NOT persist between
# separate runs of the app (it resets each time you restart Streamlit).
_response_cache = {}


def ask_ai(question, system_prompt=SYSTEM_PROMPT):
    """
    Returns a string answer from the Gemini API, or a graceful
    fallback message if the API key is missing or the call fails.
    Accepts a custom system_prompt so other modules (like scoring.py's
    recommendation generator) can reuse this same connection with a
    different persona/instructions.
    """
    cache_key = (question.strip().lower(), system_prompt)
    if cache_key in _response_cache:
        return _response_cache[cache_key]

    api_key = _get_api_key()
    if not api_key:
        return None 

    client = genai.Client(api_key=api_key)
    last_error = None

    # Retry a couple of times if Gemini's servers are just temporarily
    # overloaded (503 UNAVAILABLE) — this is common on the free tier
    # during peak hours and has nothing to do with your own usage.
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=question,
                config={"system_instruction": system_prompt},
            )
            _response_cache[cache_key] = response.text
            return response.text
        except Exception as e:
            last_error = e
            print(f"GEMINI API ERROR (attempt {attempt + 1}/3):", repr(e))
            is_overloaded = "503" in str(e) or "UNAVAILABLE" in str(e)
            is_rate_limited = "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)
            if (is_overloaded or is_rate_limited) and attempt < 2:
                time.sleep(2 * (attempt + 1))  # wait 2s, then 4s
                continue
            break
    return None 


if __name__ == "__main__":
    print(ask_ai("What insurance do I actually need for a small bakery?"))
