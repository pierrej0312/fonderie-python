import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
with MongoClient(os.getenv("MONGO_URI")) as client:
    clients = client["fonderie"]["clients"]
    cafe = clients.find_one({"type": "café"})
    print(cafe["nom"], cafe["ville"])