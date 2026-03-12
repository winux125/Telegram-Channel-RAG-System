import json
from qdrant_client import QdrantClient 
from qdrant_client.http.models import Distance, VectorParams  

client = QdrantClient(url="http://localhost:6333")



def create_collection(client,collection_name,size):
    client.create_collection(
        collection_name = collection_name,
        vectors_config = VectorParams(size=size,distance = Distance.COSINE)
    )





def read_json():
    with open('result.json','r') as fl:
        s = json.loads(fl.read())
    messages = []
    for message in s.get("messages"):
        if type(message.get("text")) is str:

            messages.append({"content": message.get("text"), "metadata":{
                "message_id": message.get("id"),
                "date": message.get("date")
            }})
        else: 
            ms = ""
            for text in message.get("text"):
                if type(text) is str:
                        ms = ms +" "+text
                if type(text) is dict:
                    ms = ms  + " " + text["text"]
                print(text)

            messages.append({"content": ms, "metadata":{
                "message_id": message.get("id"),
                "date": message.get("date")

            }})
    return messages
