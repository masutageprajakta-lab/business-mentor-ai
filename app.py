"""
app.py

Run with:  streamlit run app.py

This is your whole product in one file:
1. A short onboarding form (your `questions` dict, as real form fields).
2. A readiness report (scoring.py) shown right after.
3. A chat box below it where the user can ask anything — answered by
   pipeline.py, which uses your hardcoded knowledge first and the
   Gemini API as a fallback for anything not covered.
"""

import streamlit as st

from scoring import questions, compute_scores, generate_report, generate_ai_recommendations
from pipeline import answer_question

st.set_page_config(page_title="Business Mentor", page_icon="💡")
st.title("💡 Business Mentor")
st.caption("A starter guide for first-generation entrepreneurs")

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False
    st.session_state.chat_history = []

# ---------- Step 1: onboarding ----------
if not st.session_state.onboarded:
    st.subheader("Tell me about your business idea")

    with st.form("onboarding"):
        business_idea = st.text_input(questions["business_idea"])
        budget = st.number_input(questions["budget"], min_value=0, step=1000)
        funding_source = st.selectbox(
            questions["funding_source"],
            ["own savings", "loan", "family support", "mixed"],
        )
        other_income = st.selectbox(questions["other_income"], ["yes", "no"])
        target_customer = st.text_input(questions["target_customer"])
        competitor_knowledge = st.selectbox(
            questions["competitor_knowledge"], ["no", "1-2", "3 and more"]
        )
        customer_validation = st.selectbox(
            questions["customer_validation"], ["no", "a few", "many"]
        )
        differentiation = st.selectbox(
            questions["differentiation"], ["not sure", "a little", "yes, clearly"]
        )
        emergency_fund = st.selectbox(
            questions["emergency_fund"], ["yes", "no", "some money"]
        )
        risk_taking = st.selectbox(
            questions["risk_taking"], ["low", "medium", "high"]
        )
        communication = st.selectbox(
            questions["communication"], ["shy", "okay", "good"]
        )
        prior_experience = st.selectbox(
            questions["prior_experience"], ["none", "some", "significant"]
        )
        time_commitment = st.selectbox(
            questions["time_commitment"], ["side project", "part-time", "full-time"]
        )
        submitted = st.form_submit_button("Get my readiness report")

    if submitted:
        missing = []
        if not business_idea.strip():
            missing.append("business idea")
        if not target_customer.strip():
            missing.append("target customer")
        if budget <= 0:
            missing.append("budget")

        if missing:
            st.warning(
                "Please fill in: " + ", ".join(missing)
                + " — these are needed to give you an accurate report."
            )
        else:
            user = {
                "business_idea": business_idea,
                "budget": budget,
                "funding_source": funding_source,
                "other_income": other_income,
                "target_customer": target_customer,
                "competitor_knowledge": competitor_knowledge,
                "customer_validation": customer_validation,
                "differentiation": differentiation,
                "emergency_fund": emergency_fund,
                "risk_taking": risk_taking,
                "communication": communication,
                "prior_experience": prior_experience,
                "time_commitment": time_commitment,
            }
            st.session_state.user = user
            st.session_state.scores = compute_scores(user)
            st.session_state.onboarded = True
            st.rerun()

# ---------- Step 2: report + chat ----------
else:
    st.success("Here's where you stand:")
   
    st.markdown(generate_report(st.session_state.user, st.session_state.scores))

    st.markdown("**Recommendations for you:**")
    if "recommendations" not in st.session_state:
        with st.spinner("Working out your next steps..."):
            st.session_state.recommendations = generate_ai_recommendations(
                st.session_state.user, st.session_state.scores
            )
    st.markdown(st.session_state.recommendations)

    if st.button("Start over"):
        st.session_state.onboarded = False
        st.session_state.chat_history = []
        st.session_state.pop("recommendations", None)
        st.rerun()

    st.divider()
    st.subheader("Ask me anything about starting your business")

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    question = st.chat_input("e.g. How do I price my product?")
    if question:
        st.session_state.chat_history.append(("user", question))
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = answer_question(question)
            st.markdown(answer)

        st.session_state.chat_history.append(("assistant", answer))
