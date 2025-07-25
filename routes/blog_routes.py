import os
from functools import wraps
from flask import request, jsonify, Blueprint
from services.blog_models import (
    insert_post, search_posts, get_all_posts,
    insert_category, get_categories,
    update_post, delete_post,
    update_category, delete_category
)

blog_bp = Blueprint('blog', __name__)

ADMIN_API_KEY = os.environ.get('ADMIN_API_KEY', 'changeme')

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('x-api-key')
        if not key or key != ADMIN_API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@blog_bp.route('/posts', methods=['POST'])
@require_api_key
def create_post():
    data = request.json
    ok, err = insert_post(data)
    if not ok:
        return jsonify({'error': err}), 400
    return jsonify({'message': 'Post creado'}), 201

@blog_bp.route('/posts', methods=['PUT'])
@require_api_key
def edit_post():
    data = request.json
    title = data.get('title')
    created_at = data.get('created_at')
    update_fields = data.get('update', {})
    if not title or not created_at or not update_fields:
        return jsonify({'error': 'Faltan datos'}), 400
    ok = update_post(title, created_at, update_fields)
    if not ok:
        return jsonify({'error': 'No se pudo actualizar'}), 404
    return jsonify({'message': 'Post actualizado'})

@blog_bp.route('/posts', methods=['DELETE'])
@require_api_key
def remove_post():
    data = request.json
    title = data.get('title')
    created_at = data.get('created_at')
    if not title or not created_at:
        return jsonify({'error': 'Faltan datos'}), 400
    ok = delete_post(title, created_at)
    if not ok:
        return jsonify({'error': 'No se pudo eliminar'}), 404
    return jsonify({'message': 'Post eliminado'})

@blog_bp.route('/categories', methods=['POST'])
@require_api_key
def create_category():
    data = request.json
    name = data.get('name')
    color = data.get('color', '#888')
    if not name:
        return jsonify({'error': 'Falta el nombre'}), 400
    ok = insert_category(name, color)
    if not ok:
        return jsonify({'error': 'Categoría ya existe'}), 400
    return jsonify({'message': 'Categoría creada'}), 201

@blog_bp.route('/categories', methods=['PUT'])
@require_api_key
def edit_category():
    data = request.json
    name = data.get('name')
    update_fields = data.get('update', {})
    if not name or not update_fields:
        return jsonify({'error': 'Faltan datos'}), 400
    ok = update_category(name, update_fields)
    if not ok:
        return jsonify({'error': 'No se pudo actualizar'}), 404
    return jsonify({'message': 'Categoría actualizada'})

@blog_bp.route('/categories', methods=['DELETE'])
@require_api_key
def remove_category():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Faltan datos'}), 400
    ok = delete_category(name)
    if not ok:
        return jsonify({'error': 'No se pudo eliminar'}), 404
    return jsonify({'message': 'Categoría eliminada'})

@blog_bp.route('/posts/search', methods=['POST'])
def search_blog_posts():
    data = request.json or {}
    q = data.get('q', '')
    categories = data.get('categories', [])
    posts = search_posts(q, categories)
    return jsonify(posts)

@blog_bp.route('/posts', methods=['GET'])
def list_posts():
    posts = get_all_posts()
    return jsonify(posts)

@blog_bp.route('/categories', methods=['GET'])
def list_categories():
    cats = get_categories()
    return jsonify(cats) 