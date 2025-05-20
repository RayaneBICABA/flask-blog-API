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

#Create a new user
def create_user(username,email,password_hash,profile_image_url="default.img"):
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        profile_image_url = profile_image_url
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user