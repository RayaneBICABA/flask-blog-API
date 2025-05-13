from app import db
from app.models import Article

#Obtain all articles
def get_all_articles():
    return Article.query.all()

#Obtain one article by id
def get_article_by_id(article_id):
    return Article.query.get(article_id)
