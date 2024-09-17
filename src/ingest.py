import pandas as pd
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

def read_data(file_path='data/movies.csv'):
    data = pd.read_csv(file_path)
    return data

def configure_elasticsearch(index_name):
    es_client = Elasticsearch('http://elasticsearch:9200') 

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "movie_name": {"type": "text"},
                "year": {"type": "text"},
                "runtime": {"type": "text"},
                "genre": {"type": "text"},
                "rating": {"type": "text"},
                "description": {"type": "text"},
                "director": {"type": "text"},
                "star": {"type": "text"},
                "votes": {"type": "text"},
                "id": {"type": "keyword"},
                "name_descr_genre_director_star_vector": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine"
                },
            }
        }
    }

    es_client.indices.delete(index=index_name, ignore_unavailable=True)
    es_client.indices.create(index=index_name, body=index_settings)
    return es_client

def get_embedding_model(model_name="multi-qa-distilbert-cos-v1"):
    embedding_model = SentenceTransformer(model_name)
    return embedding_model

def process_and_index_data(df, es_client, model_name="multi-qa-distilbert-cos-v1", index_name="movies-database"):
    embedding_model = get_embedding_model(model_name)
    df["name_descr_genre_director_star"] = df.apply(lambda row: f'{row.movie_name} {row.description} {row.genre} {row.director} {row.star}', axis=1)
    df["name_descr_genre_director_star_vector"] = embedding_model.encode(df["name_descr_genre_director_star"]).tolist()
    df.drop("name_descr_genre_director_star", axis=1, inplace=True)

    for _, doc in df.iterrows():
        es_client.index(index=index_name, document=doc.to_json())

def ingest():
    index_name = "movies-database"
    df = read_data()
    es_client = configure_elasticsearch(index_name)
    process_and_index_data(df, es_client)


if __name__ == "__main__":
    ingest()

