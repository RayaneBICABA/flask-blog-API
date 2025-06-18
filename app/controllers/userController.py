from app.models import User
from app.utils.passwordHash import hash_password
from app import db

#Obtain all users
def get_all_users():
    return User.query.filter_by(is_active=True).all()

#Obtain one user by id
def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id, is_active=True).first()

#Obtain one user by email
def get_user_by_email(email):
    return User.query.filter_by(email=email, is_active=True).first()

#Create a new user
def create_user(username,email,password,profile_image_url="default.png", role="user"):
    password_hash = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        profile_image_url = profile_image_url,
        role = role
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user

#Update an existing user
def update_user(user_id,username=None,email=None,profile_image_url=None, role=None):
    user = User.query.get(user_id)
    if not user:
        return None
    if username:
        user.username = username
    if email:
        user.email = email
    if profile_image_url:
        user.profile_image_url = profile_image_url
    if role:
        user.role = role

    db.session.commit()
    return user


#Delete an existing user (soft delete)
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    user.is_active = False
    db.session.commit()
    return True

# Hard delete user (admin only)
def hard_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

# Create admin user
def create_admin_user(username, email, password, profile_image_url="default.png"):
    return create_user(username, email, password, profile_image_url, role="admin")

# Get users by role
def get_users_by_role(role):
    return User.query.filter_by(role=role, is_active=True).all()

# Update user role
def update_user_role(user_id, new_role):
    user = User.query.get(user_id)
    if not user:
        return None
    user.role = new_role
    db.session.commit()
    return user