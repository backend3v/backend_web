import json
import subprocess
import concurrent.futures
from flask import request, jsonify
from services.bitoService import BitoService
from services.prompt_cache_mongo import get_cached_prompt, save_prompt_cache
from services.metrics import save_visit
from services.prompt_normalizer import normalize_prompt

def register_prompt_routes(app, getResponse):
    @app.route('/prompt', methods=['POST'])
    def prompt():
        save_visit(request, request.path)
        data = request.json
        prompt_text = data.get('prompt')
        lang = data.get('lang')
        if not prompt_text:
            return json.dumps({"error": "Missing prompt text"}), 400
        try:
            BS = BitoService(lang)
            normalized_prompt = normalize_prompt(prompt_text)
            cached = get_cached_prompt(normalized_prompt, lang)
            if cached:
                bito_result = cached
            else:
                bito_result = BS.setConsult(normalized_prompt)
                save_prompt_cache(normalized_prompt, lang, bito_result)
            return getResponse(bito_result)
        except subprocess.CalledProcessError as e:
            return getResponse(data={"error": str(e), "output": e.output}, error=True)

    @app.route('/test_prompt', methods=['POST'])
    def test_prompt():
        save_visit(request, request.path)
        data = request.json
        prompt_text = data.get('prompt')
        lang = data.get('lang')
        if not prompt_text:
            return json.dumps({"error": "Missing prompt text"}), 400
        try:
            BS = BitoService(lang)
            normalized_prompt = normalize_prompt(prompt_text)
            cached = get_cached_prompt(normalized_prompt, lang)
            if cached:
                bito_result = cached
            else:
                bito_result = BS.getConsult()
                save_prompt_cache(normalized_prompt, lang, bito_result)
            return getResponse(bito_result)
        except Exception as e:
            return getResponse(data={"error": str(e)}, error=True)

    @app.route('/prompt-history', methods=['GET'])
    def prompt_history():
        save_visit(request, request.path)
        from services.prompt_cache_mongo import collection
        docs = collection.find({}, {"prompt_text": 1, "lang": 1, "created_at": 1, "bito_json.topic": 1}).sort("created_at", -1)
        history = []
        for doc in docs:
            history.append({
                "prompt_text": doc.get("prompt_text"),  # prompt normalizado
                "lang": doc.get("lang"),
                "created_at": doc.get("created_at"),
                "topic": doc.get("bito_json", {}).get("topic") if isinstance(doc.get("bito_json"), dict) else None
            })
        return jsonify(history)

    @app.route('/metrics', methods=['GET'])
    def metrics():
        from services.metrics import collection as metrics_collection
        docs = metrics_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(100)
        metrics_list = []
        for doc in docs:
            metrics_list.append(doc)
        return jsonify(metrics_list) 