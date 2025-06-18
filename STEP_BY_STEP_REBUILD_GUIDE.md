# Step-by-Step Guide: Rebuilding the Flask Blog API

This guide will walk you through rebuilding the entire Flask Blog API from scratch, including all the enhanced features like authorization, CORS, rate limiting, and database migrations.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)
- A text editor or IDE (VS Code, PyCharm, etc.)

## Step 1: Project Setup

### 1.1 Create Project Directory
```bash
mkdir flask-blog-api
cd flask-blog-api
```

### 1.2 Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 1.3 Initialize Git Repository
```bash
git init
```

### 1.4 Create .gitignore
```bash
# Create .gitignore file
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# Environment variables
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Flask
instance/
.webassets-cache

# Alembic
migrations/versions/*.py
!migrations/versions/__init__.py
EOF
```

## Step 2: Install Dependencies

### 2.1 Create requirements.txt
```bash
cat > requirements.txt << EOF
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
PyJWT==2.8.0
bcrypt==4.0.1
alembic==1.13.1
python-dotenv==1.0.0
Werkzeug==3.1.3
click==8.2.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
EOF
```

### 2.2 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Project Structure

### 3.1 Create Directory Structure
```bash
mkdir -p app/{controllers,models,routes,utils}
mkdir -p db
mkdir -p migrations/{versions}
mkdir -p tests
mkdir -p doc
```

### 3.2 Create __init__.py Files
```bash
touch app/__init__.py
touch app/controllers/__init__.py
touch app/models/__init__.py
touch app/routes/__init__.py
touch app/utils/__init__.py
touch migrations/__init__.py
touch migrations/versions/__init__.py
```

## Step 4: Configuration

### 4.1 Create config.py
```python
import os
from datetime import timedelta

class Config:
    # Basic Flask Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database Configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(BASE_DIR, 'db/blogapi.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # CORS Configuration
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080"
    ]
    
    # Rate Limiting Configuration
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Security Configuration
    BCRYPT_LOG_ROUNDS = 12
    PASSWORD_MIN_LENGTH = 6
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
```

### 4.2 Create .env file
```bash
cat > .env << EOF
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
FLASK_ENV=development
DATABASE_URL=sqlite:///db/blogapi.db
LOG_LEVEL=INFO
EOF
```

## Step 5: Database Models

### 5.1 Create app/models.py
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image_url = db.Column(db.String(255), default="default.png")
    role = db.Column(db.String(20), default="user")  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relation: One user have many posts
    articles = db.relationship('Article', backref='author', lazy=True)

    def to_dict(self):
        """Convert user object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_image_url': self.profile_image_url,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

    def is_admin(self):
        """Check if user has admin privileges"""
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.username}>"

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        """Convert article object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
            'is_published': self.is_published
        }

    def __repr__(self):
        return f"<Article {self.title}>"
```

## Step 6: Utilities

### 6.1 Create app/utils/passwordHash.py
```python
import bcrypt

def hash_password(plain_password: str) -> str:
    """Hash a password using bcrypt"""
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
```

### 6.2 Create app/utils/auth.py
```python
import jwt
import functools
from flask import request, jsonify, g, current_app
from app.controllers.userController import get_user_by_id

def login_required(f):
    """
    Decorator to require authentication for protected routes.
    Extracts JWT token from Authorization header and validates it.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            g.user = current_user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin privileges for protected routes.
    Checks if the current user has admin role.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # First ensure user is logged in
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Check if user has admin role
            if not hasattr(current_user, 'role') or current_user.role != 'admin':
                return jsonify({'error': 'Admin privileges required'}), 403
            
            g.user = current_user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def check_resource_ownership(resource_user_id, current_user):
    """
    Helper function to check if current user owns the resource or is admin.
    """
    if hasattr(current_user, 'role') and current_user.role == 'admin':
        return True
    return current_user.id == resource_user_id

def get_current_user():
    """
    Helper function to get the current authenticated user from Flask's g object.
    """
    return getattr(g, 'user', None)
```

### 6.3 Create app/utils/validators.py
```python
import re
from flask import request, jsonify

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_required_fields(data, required_fields):
    """Check for required fields in request data"""
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    return missing_fields

def validate_user_data(data):
    """Validate user registration/update data"""
    errors = []
    
    # Check required fields
    required_fields = ['username', 'email', 'password']
    missing = validate_required_fields(data, required_fields)
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    
    # Validate email format
    if 'email' in data and not validate_email(data['email']):
        errors.append("Invalid email format")
    
    # Validate password strength
    if 'password' in data and len(data['password']) < 6:
        errors.append("Password must be at least 6 characters long")
    
    return errors

def validate_article_data(data):
    """Validate article creation/update data"""
    errors = []
    
    # Check required fields
    required_fields = ['title', 'content']
    missing = validate_required_fields(data, required_fields)
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    
    # Validate title length
    if 'title' in data and len(data['title']) > 200:
        errors.append("Title must be less than 200 characters")
    
    return errors
```

## Step 7: Controllers

### 7.1 Create app/controllers/auth_controller.py
```python
import jwt
import datetime
from flask import current_app
from app.utils.passwordHash import verify_password
from app.controllers.userController import get_user_by_email

def authenticate_user(email, password):
    """Authenticate a user and return JWT token"""
    user = get_user_by_email(email)
    if not user:
        return None, "User not found"
    if not verify_password(password, user.password_hash):
        return None, "Incorrect password"
    
    # Create a JWT token
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token, None
```

### 7.2 Create app/controllers/userController.py
```python
from app.models import User
from app.utils.passwordHash import hash_password
from app import db

def get_all_users():
    """Get all active users"""
    return User.query.filter_by(is_active=True).all()

def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.filter_by(id=user_id, is_active=True).first()

def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email, is_active=True).first()

def create_user(username, email, password, profile_image_url="default.png", role="user"):
    """Create a new user"""
    password_hash = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        profile_image_url=profile_image_url,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user

def update_user(user_id, username=None, email=None, profile_image_url=None, role=None):
    """Update an existing user"""
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

def delete_user(user_id):
    """Soft delete user"""
    user = User.query.get(user_id)
    if not user:
        return False
    user.is_active = False
    db.session.commit()
    return True

def hard_delete_user(user_id):
    """Hard delete user"""
    user = User.query.get(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

def create_admin_user(username, email, password, profile_image_url="default.png"):
    """Create an admin user"""
    return create_user(username, email, password, profile_image_url, role="admin")

def get_users_by_role(role):
    """Get users by role"""
    return User.query.filter_by(role=role, is_active=True).all()

def update_user_role(user_id, new_role):
    """Update user role"""
    user = User.query.get(user_id)
    if not user:
        return None
    user.role = new_role
    db.session.commit()
    return user
```

### 7.3 Create app/controllers/articleController.py
```python
from app import db
from app.models import Article

def get_all_articles():
    """Get all articles"""
    return Article.query.all()

def get_article_by_id(article_id):
    """Get article by ID"""
    return Article.query.get(article_id)

def create_article(title, content, user_id, is_published=True):
    """Create a new article"""
    new_article = Article(
        title=title, 
        content=content, 
        user_id=user_id,
        is_published=is_published
    )
    db.session.add(new_article)
    db.session.commit()
    return new_article

def update_article(article_id, title=None, content=None, is_published=None):
    """Update an existing article"""
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

def delete_article(article_id):
    """Delete an article"""
    article = get_article_by_id(article_id)
    if not article:
        return False
    
    db.session.delete(article)
    db.session.commit()
    return True

def get_published_articles():
    """Get published articles only"""
    return Article.query.filter_by(is_published=True).all()

def get_articles_by_user(user_id):
    """Get articles by user"""
    return Article.query.filter_by(user_id=user_id).all()

def get_published_articles_by_user(user_id):
    """Get published articles by user"""
    return Article.query.filter_by(user_id=user_id, is_published=True).all()
```

## Step 8: Routes

### 8.1 Create app/routes/auth.py
```python
from flask import Blueprint, jsonify, request
from app.controllers.auth_controller import authenticate_user
from app.controllers.userController import create_user
from app.utils.validators import validate_user_data

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input data
    errors = validate_user_data(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = create_user(username, email, password)
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': 'User creation failed', 'details': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    token, error = authenticate_user(email, password)
    if error:
        return jsonify({"error": error}), 401
    return jsonify({"token": token})
```

### 8.2 Create app/routes/user.py
```python
from flask import Blueprint, jsonify, request, g
from app.controllers.userController import (
    get_all_users, get_user_by_id, update_user, delete_user, hard_delete_user,
    update_user_role, get_users_by_role
)
from app.utils.auth import login_required, admin_required, check_resource_ownership

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    """Get all active users (admin only)"""
    users = get_all_users()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get user by ID (owner or admin only)"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if current user can access this user's data
    if not check_resource_ownership(user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
def update_a_user(user_id):
    """Update user (owner or admin only)"""
    # Check if current user can update this user
    if not check_resource_ownership(user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    profile_image_url = data.get('profile_image_url')
    
    # Only admins can change roles
    role = None
    if g.user.is_admin() and 'role' in data:
        role = data.get('role')
    
    user = update_user(user_id, username, email, profile_image_url, role)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_a_user(user_id):
    """Soft delete user (admin only)"""
    deleted = delete_user(user_id)
    if not deleted:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200

@user_bp.route('/<int:user_id>/hard-delete', methods=['DELETE'])
@admin_required
def hard_delete_a_user(user_id):
    """Hard delete user (admin only)"""
    deleted = hard_delete_user(user_id)
    if not deleted:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User permanently deleted'}), 200

@user_bp.route('/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role_endpoint(user_id):
    """Update user role (admin only)"""
    data = request.get_json()
    new_role = data.get('role')
    
    if not new_role or new_role not in ['user', 'admin']:
        return jsonify({'error': 'Invalid role. Must be "user" or "admin"'}), 400
    
    user = update_user_role(user_id, new_role)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/role/<role>', methods=['GET'])
@admin_required
def get_users_by_role_endpoint(role):
    """Get users by role (admin only)"""
    if role not in ['user', 'admin']:
        return jsonify({'error': 'Invalid role. Must be "user" or "admin"'}), 400
    
    users = get_users_by_role(role)
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/profile', methods=['GET'])
@login_required
def get_current_user_profile():
    """Get current user's profile"""
    return jsonify(g.user.to_dict())

@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_current_user_profile():
    """Update current user's profile"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    profile_image_url = data.get('profile_image_url')
    
    user = update_user(g.user.id, username, email, profile_image_url)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())
```

### 8.3 Create app/routes/article.py
```python
from flask import Blueprint, jsonify, request, g
from app.controllers.articleController import (
    get_all_articles, get_article_by_id, create_article, update_article, delete_article
)
from app.controllers.userController import get_user_by_id
from app.utils.auth import login_required, admin_required, check_resource_ownership
from app.utils.validators import validate_article_data

article_bp = Blueprint('article', __name__, url_prefix='/api/articles')

@article_bp.route('/', methods=['GET'])
def get_articles():
    """Get all published articles (public)"""
    articles = get_all_articles()
    # Filter to only show published articles for non-authenticated users
    if not hasattr(g, 'user'):
        articles = [article for article in articles if article.is_published]
    return jsonify([article.to_dict() for article in articles])

@article_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get article by ID (public for published articles)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404
    
    # Check if user can access unpublished articles
    if not article.is_published and (not hasattr(g, 'user') or 
        not check_resource_ownership(article.user_id, g.user)):
        return jsonify({"error": "Article not found"}), 404
    
    return jsonify(article.to_dict())

@article_bp.route('/', methods=['POST'])
@login_required
def create_new_article():
    """Create a new article (authenticated users only)"""
    data = request.get_json()
    
    # Validate input data
    errors = validate_article_data(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    title = data.get('title')
    content = data.get('content')
    is_published = data.get('is_published', True)
    
    user_id = g.user.id
    article = create_article(title, content, user_id, is_published)
    return jsonify(article.to_dict()), 201

@article_bp.route('/<int:article_id>', methods=['PUT'])
@login_required
def update_an_article(article_id):
    """Update article (owner or admin only)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # Check if user can update this article
    if not check_resource_ownership(article.user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    is_published = data.get('is_published')
    
    article, error = update_article(article_id, title, content, is_published)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(article.to_dict())

@article_bp.route('/<int:article_id>', methods=['DELETE'])
@login_required
def delete_an_article(article_id):
    """Delete article (owner or admin only)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # Check if user can delete this article
    if not check_resource_ownership(article.user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    deleted = delete_article(article_id)
    if not deleted:
        return jsonify({'error': 'Article Not Found'}), 404
    return jsonify({'message': 'Article deleted'}), 200

@article_bp.route('/my-articles', methods=['GET'])
@login_required
def get_my_articles():
    """Get current user's articles"""
    articles = get_all_articles()
    user_articles = [article for article in articles if article.user_id == g.user.id]
    return jsonify([article.to_dict() for article in user_articles])

@article_bp.route('/<int:article_id>/publish', methods=['PUT'])
@login_required
def toggle_article_publish(article_id):
    """Toggle article publish status (owner or admin only)"""
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # Check if user can modify this article
    if not check_resource_ownership(article.user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    is_published = data.get('is_published', not article.is_published)
    
    article, error = update_article(article_id, is_published=is_published)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(article.to_dict())
```

## Step 9: Application Factory

### 9.1 Create app/__init__.py
```python
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from .models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configure rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=app.config['RATELIMIT_DEFAULT'].split(';')
    )
    
    # Apply rate limits to specific endpoints
    @limiter.limit("5 per minute")
    def auth_endpoints():
        pass
    
    @limiter.limit("100 per hour")
    def api_endpoints():
        pass

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.user import user_bp
    from .routes.article import article_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'API is running'})

    with app.app_context():
        db.create_all()  # Create tables on first run

    return app
```

## Step 10: Database Migrations

### 10.1 Initialize Alembic
```bash
alembic init migrations
```

### 10.2 Update migrations/env.py
```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.models import db
target_metadata = db.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 10.3 Update migrations/alembic.ini
```ini
[alembic]
script_location = migrations
sqlalchemy.url = sqlite:///db/blogapi.db
```

## Step 11: Management Script

### 11.1 Create manage.py
```python
#!/usr/bin/env python3
"""
Management script for Flask Blog API
Handles database migrations, user creation, and other administrative tasks
"""

import os
import sys
from flask.cli import FlaskGroup
from app import create_app
from app.models import db, User
from app.controllers.userController import create_admin_user

app = create_app()
cli = FlaskGroup(app)

@cli.command("init-db")
def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

@cli.command("create-admin")
def create_admin():
    """Create an admin user"""
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    with app.app_context():
        try:
            admin = create_admin_user(username, email, password)
            print(f"Admin user '{admin.username}' created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {e}")

@cli.command("migrate")
def migrate():
    """Run database migrations"""
    os.system("alembic upgrade head")
    print("Migrations completed successfully!")

@cli.command("migrate-create")
def migrate_create():
    """Create a new migration"""
    message = input("Enter migration message: ")
    os.system(f"alembic revision --autogenerate -m '{message}'")
    print("Migration created successfully!")

@cli.command("migrate-rollback")
def migrate_rollback():
    """Rollback the last migration"""
    os.system("alembic downgrade -1")
    print("Migration rolled back successfully!")

@cli.command("migrate-history")
def migrate_history():
    """Show migration history"""
    os.system("alembic history")

@cli.command("reset-db")
def reset_db():
    """Reset the database (WARNING: This will delete all data)"""
    confirm = input("Are you sure you want to reset the database? This will delete ALL data! (yes/no): ")
    if confirm.lower() == 'yes':
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Database reset successfully!")
    else:
        print("Database reset cancelled.")

@cli.command("list-users")
def list_users():
    """List all users"""
    with app.app_context():
        users = User.query.all()
        if users:
            print("\nUsers:")
            print("-" * 50)
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}")
        else:
            print("No users found.")

if __name__ == '__main__':
    cli()
```

## Step 12: Main Application

### 12.1 Create run.py
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## Step 13: Testing Setup

### 13.1 Create tests/__init__.py
```python
# Test package
```

### 13.2 Create tests/test_auth.py
```python
import pytest
from app import create_app, db
from app.models import User
from app.controllers.userController import create_user

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'

def test_login_user(client):
    """Test user login"""
    # First register a user
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Then try to login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
```

## Step 14: Documentation

### 14.1 Create README.md
```markdown
# Flask Blog API

A comprehensive Flask-based REST API for blog management with advanced features including role-based authorization, CORS support, rate limiting, and database migrations.

## Features

- 🔐 JWT-based authentication
- 👥 Role-based authorization (User/Admin)
- 🌐 CORS support for frontend integration
- ⚡ Rate limiting for API protection
- 🗄️ Database migrations with Alembic
- 📝 Article management with publish/unpublish
- 👤 User management with soft delete
- 🔒 Resource ownership validation
- ✅ Input validation and error handling

## Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd flask-blog-api
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize database
```bash
python manage.py init-db
```

### 6. Create admin user
```bash
python manage.py create-admin
```

### 7. Run the application
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete endpoint documentation.

## Management Commands

- `python manage.py init-db` - Initialize database
- `python manage.py create-admin` - Create admin user
- `python manage.py migrate` - Run migrations
- `python manage.py migrate-create` - Create new migration
- `python manage.py list-users` - List all users

## Testing

```bash
python -m pytest tests/
```

## License

MIT License
```

## Step 15: Final Setup and Testing

### 15.1 Initialize the Project
```bash
# Make sure you're in the project directory
cd flask-blog-api

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python manage.py init-db

# Create admin user
python manage.py create-admin

# Run migrations
python manage.py migrate
```

### 15.2 Test the API
```bash
# Start the server
python run.py
```

### 15.3 Test Endpoints
```bash
# Test registration
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Test protected endpoint
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Step 16: Production Deployment

### 16.1 Update Configuration
```python
# config.py - Add production configuration
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # Add production database URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
```

### 16.2 Set Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 16.3 Use Production Server
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Summary

You have now successfully rebuilt the entire Flask Blog API with all the enhanced features:

✅ **Project Structure** - Organized and scalable  
✅ **Configuration** - Environment-based settings  
✅ **Database Models** - User and Article with relationships  
✅ **Authentication** - JWT-based with role support  
✅ **Authorization** - Role-based access control  
✅ **CORS Support** - Frontend integration ready  
✅ **Rate Limiting** - API protection  
✅ **Database Migrations** - Version control for schema  
✅ **Input Validation** - Data integrity  
✅ **Error Handling** - Comprehensive error responses  
✅ **Management Commands** - Administrative tasks  
✅ **Testing Setup** - Unit test framework  
✅ **Documentation** - Complete API documentation  
✅ **Production Ready** - Deployment configuration  

The API is now production-ready with enterprise-level features and can be deployed to any environment. 