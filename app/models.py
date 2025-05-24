from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    email=db.Column(db.String(120),nullable=False,unique=True)
    password_hash=db.Column(db.String(128),nullable=False)
    profile_image_url=db.Column(db.String(255),default="default.png")

    #Relation: One user have many posts
    articles = db.relationship('Article', backref='author', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"



class Article(db.Model):
    __tablename__ = 'articles'

    id= db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)


    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Article {self.title}>"