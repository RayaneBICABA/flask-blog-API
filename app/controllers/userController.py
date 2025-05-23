from app.models import User
from app import db

#Obtain all users
def get_all_users():
    return User.query.all()
