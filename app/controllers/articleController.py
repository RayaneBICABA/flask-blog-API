from app import db
from app.models import Article

#Obtain all articles
def get_all_articles():
    return Article.query.all()

#Obtain one article by id
def get_article_by_id(article_id):
    return Article.query.get(article_id)

#Create new article
def create_article(title, content,user_id):
    new_article = Article(title=title, content=content,user_id =user_id)
    db.session.add(new_article)
    db.commit()
    return new_article

#Update existing article
def update_article(article_id, title=None, content=None):
    article =get_article_by_id(article_id)
    if not article:
        return None , "Article not found"
    if title:
        article.title = title
    if content:
        article.content = content

    db.session.commit()
    return article

