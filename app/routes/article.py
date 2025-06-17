from flask import Blueprint, jsonify, request, g
from app.controllers.articleController import (
    get_all_articles, get_article_by_id, create_article, update_article, delete_article
)
from app.controllers.userController import get_user_by_id
from app.routes.auth import login_required

article_bp = Blueprint('article', __name__, url_prefix='/api/articles')

# Get all articles
@article_bp.route('/', methods=['GET'])
def get_articles():
    articles = get_all_articles()
    return jsonify([article.to_dict() for article in articles])

#Get an artcile by id
@article_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404
    return jsonify(article.to_dict())

# Create an article
@article_bp.route('/', methods=['POST'])
@login_required
def create_new_artcile():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = g.user.id  # Assuming you have a login decorator that sets
    article = create_article(title, content, user_id)
    return jsonify(article.to_dict()), 201

# Update an article
@article_bp.route('/<int:article_id>', methods = ['PUT'])
@login_required
def update_an_article(article_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    article = update_article(article_id,title,content)
    if not article:
        return jsonify({'error':'Article Not Found'}), 404
    return jsonify(article.to_dict())

# Delete an article
@article_bp.route('/<int:artcile_id>', methods=['DELETE'])
@login_required
def delete_an_article(article_id):
    deleted = delete_an_article(article_id)
    if not deleted:
        return jsonify({'error':'Article Not Found'}), 404
    return jsonify({'message': 'Article deleted'}), 200