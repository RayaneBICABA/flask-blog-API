from app import db
from app.models import Article

#Obtain all articles
def get_all_articles():
    return Article.query.all()

#Obtain one article by id
def get_article_by_id(article_id):
    return Article.query.get(article_id)

#Create new article
def create_article(title, content, user_id, is_published=True):
    new_article = Article(
        title=title, 
        content=content, 
        user_id=user_id,
        is_published=is_published
    )
    db.session.add(new_article)
    db.session.commit()
    return new_article

#Update existing article
def update_article(article_id, title=None, content=None, is_published=None):
    article = get_article_by_id(article_id)
    if not article:
        return None, "Article not found"
    if title:
        article.title = title
    if content:
        article.content = content
    if is_published is not None:
        article.is_published = is_published

    db.session.commit()
    return article, None

#Delete article
def delete_article(article_id):
    article = get_article_by_id(article_id)
    if not article:
        return False
    
    db.session.delete(article)
    db.session.commit()
    return True

# Get published articles only
def get_published_articles():
    return Article.query.filter_by(is_published=True).all()

# Get articles by user
def get_articles_by_user(user_id):
    return Article.query.filter_by(user_id=user_id).all()

# Get published articles by user
def get_published_articles_by_user(user_id):
    return Article.query.filter_by(user_id=user_id, is_published=True).all()
