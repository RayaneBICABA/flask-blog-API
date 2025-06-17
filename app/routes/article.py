from flask import Blueprint, jsonify, request, g
from app.controllers.articleController import (
    get_all_articles, get_article_by_id, create_article, update_article, delete_article
)
from app.controllers.userController import get_user_by_id
from app.utils.auth import login_required

article_bp = Blueprint('article', __name__, url_prefix='/api/articles')

# Get all articles
@article_bp.route('/', methods=['GET'])
def get_articles():
    articles = get_all_articles()
    return jsonify([article.to_dict() for article in articles])