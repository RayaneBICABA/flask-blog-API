from app import db
from app.models import Article

#Obtain all articles
def get_all_articles():
    return Article.query.all()
