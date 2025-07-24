from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["prompt_db"]
collection = db["prompt_cache"]

def get_cached_prompt(prompt_text, lang):
    doc = collection.find_one({"prompt_text": prompt_text, "lang": lang})
    return doc["bito_json"] if doc else None

def save_prompt_cache(prompt_text, lang, bito_json):
    collection.insert_one({
        "prompt_text": prompt_text,  # prompt normalizado
        "lang": lang,
        "bito_json": bito_json,
        "created_at": datetime.utcnow()
    }) 