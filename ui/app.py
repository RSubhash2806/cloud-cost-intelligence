import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from rag.retriever import answer_question

st.set_page_config(
    page_title="Cloud Cost Intelligence",
    layout="centered"
)

st.title("Cloud Cost Intelligence")
st.caption("Graph-grounded explanations for cloud costs")

st.divider()

question = st.text_input(
    "Ask a question about your cloud costs:",
    placeholder="Why did my cloud costs increase this month?"
)

if st.button("Explain"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing costs..."):
            answer = answer_question(question)

        st.subheader("Explanation")
        st.write(answer)

st.divider()

st.caption(
    "This explanation is generated using semantic retrieval and graph-grounded facts. "
    "No estimates or hallucinated values are used."
)
