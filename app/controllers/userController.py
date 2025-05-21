from app.models import User
from app import db

#Obtain all users
def get_all_users():
    return User.query.all()

#Obtain one user by id
def get_user_by_id(user_id):
    return User.query.get(user_id)

#Obtain one user by email
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()