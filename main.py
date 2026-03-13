import json
from qdrant_client import QdrantClient 
from qdrant_client.http.models import Distance, VectorParams  
from qdrant_client.models import PointStruct
import uuid
from sentence_transformers import SentenceTransformer
import torch
from openai import OpenAI
import os
import sys
from dotenv import load_dotenv
load_dotenv()


API_KEY_LLM = os.getenv("API_KEY_LLM")
BASE_URL_LLM = os.getenv("BASE_URL_LLM")
MODEL_LLM = "z-ai/glm-4.5-air:free"

clientllm = OpenAI(
  base_url=BASE_URL_LLM,
  api_key=API_KEY_LLM,
)

EMBEDDING_MODEL = "BAAI/bge-m3"
device = "cuda" if torch.cuda.is_available() else "cpu" 


model = SentenceTransformer(EMBEDDING_MODEL, device = device)
client = QdrantClient(url="http://localhost:6333")
collection_name = "durov_telegram_channel"

def get_embeddings(text):
    return model.encode(text)

def create_collection(client,collection_name,size):
    client.create_collection(
        collection_name = collection_name,
        vectors_config = VectorParams(size=size,distance = Distance.COSINE)
    )


def add_point(client, collection_name, text, payload):
    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=str(uuid.uuid4().hex),
                vector=get_embeddings(text).tolist(),
                payload=payload
            )
        ]
    )


def read_json(client,collection_name):
    if os.path.exists("result.json"):
        with open('result.json','r') as fl:
            s = json.loads(fl.read())
    else:
        print("="*60 + "\nAdd result.json\n" + "="*60)
        sys.exit(0)
        return 
    messages = []
    for message in s.get("messages"):
        if type(message.get("text")) is str:

            # messages.append({"content": message.get("text"), "metadata":{
            #     "message_id": message.get("id"),
            #     "date": message.get("date")
            # }})
            payload = {"metadata":{
                "content": message.get("text"),
                "message_id": message.get("id"),
                "date": message.get("date"),
            }}
            add_point(client, collection_name, message.get("text"), payload)
        else: 
            ms = ""
            for text in message.get("text"):
                if type(text) is str:
                        ms = ms +" "+text
                if type(text) is dict:
                    ms = ms  + " " + text["text"]

            # messages.append({"content": ms, "metadata":{
            #     "message_id": message.get("id"),
            #     "date": message.get("date")

            # }})
            add_point(client,collection_name,ms,{"metadata":{
                "content": ms,
                "message_id": message.get("id"),
                "date": message.get("date")
            }})



def search(client, collection_name, query, top_k=5):
    results = client.query_points(
        collection_name=collection_name,
        query=get_embeddings(query).tolist(),
        limit=top_k,
        with_payload=True
    )
    # print(results.points[0].payload)

    return results.points


def generate_answer(query, context_chunks):
    context = "\n\n".join([r.payload["metadata"]["content"] for r in context_chunks])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    # → отправить prompt в LLM
    response = clientllm.chat.completions.create(
    model=MODEL_LLM,
    messages=[
            {
                "role": "user",
                "content": prompt
            }
            ],
    )
    response = response.choices[0].message

    return response


def rag(query):
    results = search(client, collection_name, query)
    answer = generate_answer(query, results)
    return answer

def main():
    if not client.collection_exists(collection_name):
        size = len(get_embeddings("test"))
        create_collection(client, collection_name, size)
        read_json(client, collection_name)
    print(search(client,collection_name,"telegram is the most downloaded"))

main()