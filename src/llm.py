from time import time
from src.db import init_db
from src.elastic_search import rephrase_query, elastic_search_knn
from src.ingest import get_embedding_model
from openai import OpenAI

init_db()
# Initialize the OpenAI client
gpt_client = OpenAI()

embedding_model = get_embedding_model()

prompt = """
You are a movie recommendation assistant. You must answer the QUESTION based on the CONTEXT. If you cannot find the answer to the question, just say "I don't know", don't try to make up an answer. Do not make up an answer if you cannot find the answer to the question. Don't mention the source of the information. Avoid using the words context and dataset.

QUESTION:
{question}

CONTEXT: 
{context}
"""

def get_llm_answer(question, num_results=10):
    t0 = time()
    rephrased_question, rephrase_stats = rephrase_query(question)
    rephrased_question_vector = embedding_model.encode(rephrased_question)
    res = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt.format(
            question=question,
            context = elastic_search_knn(rephrased_question, rephrased_question_vector, num_results))}]
    )
    t1 = time()
    token_stats = {
        "prompt_tokens": res.usage.prompt_tokens + rephrase_stats["prompt_tokens"],
        "completion_tokens": res.usage.completion_tokens + rephrase_stats["completion_tokens"],
        "total_tokens": res.usage.total_tokens + rephrase_stats["total_tokens"],
        "response_time": t1 - t0,
    }
    return res.choices[0].message.content, token_stats


def calculate_openai_cost(tokens):
    return (
        tokens["prompt_tokens"] * 0.00015 + tokens["completion_tokens"] * 0.0006
    ) / 1000
