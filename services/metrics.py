from pymongo import MongoClient
from datetime import datetime
import os
from user_agents import parse as parse_ua

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["prompt_db"]
collection = db["visit_metrics"]

def save_visit(request, path):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent_str = request.headers.get('User-Agent', '')
    user_agent = parse_ua(user_agent_str)
    lang = request.headers.get('Accept-Language', '').split(',')[0]
    referrer = request.headers.get('Referer', '')
    doc = {
        "timestamp": datetime.utcnow(),
        "ip": ip,
        "user_agent": user_agent_str,
        "os": user_agent.os.family,
        "browser": user_agent.browser.family,
        "is_mobile": user_agent.is_mobile,
        "is_bot": user_agent.is_bot,
        "lang": lang,
        "referrer": referrer,
        "path": path
    }
    collection.insert_one(doc)

# Nueva función para limitar prompts por IP

def count_prompt_requests(ip, since_dt):
    from pymongo import MongoClient
    import os
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
    client = MongoClient(MONGO_URI)
    db = client["prompt_db"]
    collection = db["metrics"]
    return collection.count_documents({
        "ip": ip,
        "route": "/prompt",
        "method": "POST",
        "timestamp": {"$gte": since_dt}
    }) 