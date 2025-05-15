import jwt
import datetime
from flask import current_app
from app.utils.passwordHash import verify_password
from app.controllers.userController import get_user_by_email

#Authenticate a user
def authenticate_user(email,password):
    user = get_user_by_email(email)
    if not user:
        return None,"User not found"
    if not verify_password(password,user.password_hash):
        return None, "Incorrect password"
    
    # Create a JWT token
    payload ={
        'user_id':user.id,
        'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'],algorithm='HS256')
    return token,None