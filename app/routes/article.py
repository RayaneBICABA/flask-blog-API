from flask import Blueprint, jsonify, request, g
from app.controllers.articleController import (
    get_all_articles, get_article_by_id, create_article, update_article, delete_article
)
from app.controllers.userController import get_user_by_id
from app.utils.auth import login_required, admin_required, check_resource_ownership

article_bp = Blueprint('article', __name__, url_prefix='/api/articles')

# Get all articles
@article_bp.route('/', methods=['GET'])
def get_articles():
    """Get all published articles (public)"""
    articles = get_all_articles()
    # Filter to only show published articles for non-authenticated users
    if not hasattr(g, 'user'):
        articles = [article for article in articles if article.is_published]
    return jsonify([article.to_dict() for article in articles])

# Get an article by id
@article_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get article by ID (public for published articles)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404
    
    # Check if user can access unpublished articles
    if not article.is_published and (not hasattr(g, 'user') or 
        not check_resource_ownership(article.user_id, g.user)):
        return jsonify({"error": "Article not found"}), 404
    
    return jsonify(article.to_dict())

# Create an article
@article_bp.route('/', methods=['POST'])
@login_required
def create_new_article():
    """Create a new article (authenticated users only)"""
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    is_published = data.get('is_published', True)
    
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    user_id = g.user.id
    article = create_article(title, content, user_id, is_published)
    return jsonify(article.to_dict()), 201

# Update an article
@article_bp.route('/<int:article_id>', methods=['PUT'])
@login_required
def update_an_article(article_id):
    """Update article (owner or admin only)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # Check if user can update this article
    if not check_resource_ownership(article.user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    is_published = data.get('is_published')
    
    article, error = update_article(article_id, title, content, is_published)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(article.to_dict())

# Delete an article
@article_bp.route('/<int:article_id>', methods=['DELETE'])
@login_required
def delete_an_article(article_id):
    """Delete article (owner or admin only)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # Check if user can delete this article
    if not check_resource_ownership(article.user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    deleted = delete_article(article_id)
    if not deleted:
        return jsonify({'error': 'Article Not Found'}), 404
    return jsonify({'message': 'Article deleted'}), 200

# Get user's articles
@article_bp.route('/my-articles', methods=['GET'])
@login_required
def get_my_articles():
    """Get current user's articles"""
    articles = get_all_articles()
    user_articles = [article for article in articles if article.user_id == g.user.id]
    return jsonify([article.to_dict() for article in user_articles])

# Publish/Unpublish article
@article_bp.route('/<int:article_id>/publish', methods=['PUT'])
@login_required
def toggle_article_publish(article_id):
    """Toggle article publish status (owner or admin only)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # Check if user can modify this article
    if not check_resource_ownership(article.user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    is_published = data.get('is_published', not article.is_published)
    
    article, error = update_article(article_id, is_published=is_published)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(article.to_dict())