from elasticsearch import Elasticsearch

# Initialize the Elasticsearch client
es_client = Elasticsearch("http://elasticsearch:9200")
index_name = "movies-database"


def elastic_search_knn(question, vector, num_results):
    knn = {
        "field": "name_descr_genre_director_star_vector",
        "query_vector": vector,
        "k": num_results,
        "num_candidates": 10000,
    }

    search_query = {
        "knn": knn,
        "_source": ['movie_name', 'year', 'runtime', 'genre', 'rating',
            'description', 'director', 'star', 'votes', 'id']
    }

    es_results = es_client.search(
        index=index_name,
        body=search_query,
    )
    
    result_docs = []
    
    for hit in es_results['hits']['hits']:
        result_docs.append(hit['_source'])
        result_docs[-1]['score'] = hit['_score']


    return result_docs


def rephrase_query(question):
    from src.llm import gpt_client
    query = f"""
        Given a QUESTION, extract one or more words from the QUESTION that can indicate one or more of 
        following fields: movie_name, year, runtime, genre, rating, description,
        director, star, votes.
        Output the extracted words separated by a space.

        QUESTION
        {question}
    """
    res = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
    )
    token_stats = {
        "prompt_tokens": res.usage.prompt_tokens,
        "completion_tokens": res.usage.completion_tokens,
        "total_tokens": res.usage.total_tokens,
    }
    return res.choices[0].message.content, token_stats