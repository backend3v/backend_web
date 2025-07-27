from pymongo import MongoClient
from datetime import datetime
import os
from dateutil.parser import parse as parse_date

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["prompt_db"]
posts_col = db["blog_posts"]
categories_col = db["blog_categories"]

def insert_category(name: str, color: str):
    if categories_col.find_one({"name": name}):
        return False
    categories_col.insert_one({"name": name, "color": color})
    return True

def get_categories():
    return list(categories_col.find({}, {"_id": 0}))

def validate_category(name: str):
    return categories_col.find_one({"name": name}) is not None

def insert_post(post: dict):
    # post debe tener: html, title, category, description, image
    if not validate_category(post.get("category", "")):
        return False, "Categoría no existe"
    post["created_at"] = datetime.utcnow()
    posts_col.insert_one(post)
    return True, None

def get_all_posts():
    return list(posts_col.find({}, {"_id": 0}))

def search_posts(q: str = "", categories: list = None):
    filtro = {}
    if q:
        filtro["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]
    if categories:
        filtro["category"] = {"$in": categories}
    return list(posts_col.find(filtro, {"_id": 0}))

def get_posts_by_category(categories: list):
    return list(posts_col.find({"category": {"$in": categories}}, {"_id": 0}))

def get_post_by_title_or_description(q: str):
    filtro = {"$or": [
        {"title": {"$regex": q, "$options": "i"}},
        {"description": {"$regex": q, "$options": "i"}}
    ]}
    return list(posts_col.find(filtro, {"_id": 0}))

def update_post(title: str, update_fields: dict):

    result = posts_col.update_one(
        {"title": title},
        {"$set": update_fields}
    )
    return result.modified_count > 0

def delete_post(title: str, created_at: str):
    result = posts_col.delete_one({"title": title, "created_at": created_at})
    return result.deleted_count > 0

def update_category(name: str, update_fields: dict):
    result = categories_col.update_one({"name": name}, {"$set": update_fields})
    return result.modified_count > 0

def delete_category(name: str):
    result = categories_col.delete_one({"name": name})
    return result.deleted_count > 0 