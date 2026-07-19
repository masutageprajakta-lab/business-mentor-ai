# Business Mentor App

## Setup
1. python3 -m venv venv && source venv/bin/activate   (Windows: venv\Scripts\activate)
2. pip install -r requirements.txt
3. Get a FREE API key at https://aistudio.google.com/app/apikey (sign in
   with any Google account — no credit card required)
4. Set it as an environment variable before running locally:
   export GEMINI_API_KEY="AIzaSy..."   (Mac/Linux)
   setx GEMINI_API_KEY "AIzaSy..."     (Windows, then restart terminal)
5. Run: streamlit run app.py

## Deploying (free, no server needed)
1. Push this folder to a GitHub repo.
2. Go to https://share.streamlit.io, connect the repo, set app.py as the entry file.
3. In the app's "Secrets" settings, add:
   GEMINI_API_KEY = "AIzaSy..."
4. Deploy. search_engine.py automatically reads from st.secrets in that environment.

## How a question flows through the app
1. User types a question in the chat box (app.py).
2. classifier.py scores the question against every module's keywords
   and picks the best-matching module (e.g. "finance").
3. retriever.py searches that module's cards for the closest match.
4. response_generator.py formats the card into a friendly answer.
5. If step 2 or 3 comes back empty (nothing matched well), pipeline.py
   falls back to search_engine.py, which asks the Gemini API instead.

## Adding more knowledge
Each file in knowledge/ is just a Python dict of "topic name" -> card.
Follow the exact card shape already used (definition, importance,
example, common_mistakes, tips) and add new keys to the dict — nothing
else needs to change, retriever.py will pick it up automatically.

## Files still worth filling in
communication.py, finance.py, growth.py, legal.py, market.py,
marketing.py, mindset.py each currently have only ONE example card so
the app runs end-to-end. Fill them out the same way business.py,
risk.py, and sales.py already are.
