import os
import streamlit as st
from streamlit import session_state as ss
from src.llm import get_llm_answer, calculate_openai_cost
from src.db import save_conversation, save_feedback
import hashlib


def calculate_sha256(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

if 'answer' not in ss:
    ss.answer = None
if 'question' not in ss:
    ss.question = None

st.title("movie-assistant")

def generate_response(input_text):
    ss.answer, stats = get_llm_answer(input_text)

    save_conversation(
        calculate_sha256(input_text),
        input_text,
        {
            "answer": ss.answer,
            "response_time": stats["response_time"],
            "prompt_tokens": stats["prompt_tokens"],
            "completion_tokens": stats["completion_tokens"],
            "total_tokens": stats["total_tokens"],
            "openai_cost": calculate_openai_cost(stats),
        }
    )


with st.form("my_form"):
    ss.question = st.text_area("Enter your question:", "How many Avatar movies they are and what are they about?")
    submitted = st.form_submit_button("Submit")
    if not os.getenv("OPENAI_API_KEY"):
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(ss.question)

if ss.answer is not None:
    with st.container(border=True):
        st.write('Assistant Response:')
        st.info(ss.answer)

    with st.container(border=True):
        rating = st.selectbox(f"Rate the answer to question:", [None, 1, 2, 3, 4, 5], index=0)
        if rating:
            save_feedback(calculate_sha256(ss.question), rating)