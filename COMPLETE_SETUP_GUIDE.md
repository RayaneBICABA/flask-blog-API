# Complete Setup Guide - Enhanced Flask Blog API

This guide provides step-by-step instructions to set up and run the enhanced Flask Blog API with all new features.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### 1. Clone and Setup
```bash
# Clone the repository (if using git)
git clone <your-repo-url>
cd flask-api

# Or if you're starting fresh, create the directory structure
mkdir flask-api
cd flask-api
```

### 2. Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Create .env file
cat > .env << EOF
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
FLASK_ENV=development
DATABASE_URL=sqlite:///db/blogapi.db
LOG_LEVEL=INFO
EOF
```

### 5. Database Setup
```bash
# Initialize database
python manage.py init-db

# Create admin user
python manage.py create-admin
```

### 6. Run the Application
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 🔧 Advanced Setup

### Database Migrations
```bash
# Initialize Alembic (if not already done)
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Create Multiple Users
```bash
# Create regular user
python manage.py create-user

# Create admin user
python manage.py create-admin
```

### Management Commands
```bash
# List all users
python manage.py list-users

# Reset database (WARNING: deletes all data)
python manage.py reset-db

# Show migration history
python manage.py migrate-history
```

## 🧪 Testing the API

### 1. Test Authentication
```bash
# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. Test Protected Endpoints
```bash
# Get user profile (replace YOUR_TOKEN with actual token)
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create article
curl -X POST http://localhost:5000/api/articles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "My First Article",
    "content": "This is the content of my article.",
    "is_published": true
  }'
```

### 3. Test Admin Features
```bash
# Login as admin (replace with admin credentials)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'

# Get all users (admin only)
curl -X GET http://localhost:5000/api/users/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

## 📊 API Features

### Authentication & Authorization
- ✅ JWT-based authentication
- ✅ Role-based access control (User/Admin)
- ✅ Resource ownership validation
- ✅ Token expiration (24 hours)

### Security Features
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection protection

### Database Features
- ✅ SQLAlchemy ORM
- ✅ Database migrations with Alembic
- ✅ Soft delete for users
- ✅ Relationship management

### API Endpoints
- ✅ User registration and login
- ✅ User management (CRUD)
- ✅ Article management (CRUD)
- ✅ Role management
- ✅ Profile management

## 🔒 Security Configuration

### Rate Limiting
- Global: 200 requests per day, 50 per hour
- Authentication: 5 requests per minute
- API endpoints: 100 requests per hour

### CORS Settings
- Allowed origins: localhost:3000, localhost:8080
- Allowed methods: GET, POST, PUT, DELETE, OPTIONS
- Allowed headers: Content-Type, Authorization

### Password Requirements
- Minimum length: 6 characters
- Hashing: bcrypt with salt

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    profile_image_url VARCHAR(255) DEFAULT 'default.png',
    role VARCHAR(20) DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Articles Table
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT TRUE,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🚀 Production Deployment

### 1. Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export JWT_SECRET_KEY=your-production-jwt-secret
export DATABASE_URL=postgresql://user:password@localhost/dbname
export LOG_LEVEL=WARNING
```

### 2. Install Production Dependencies
```bash
pip install gunicorn
```

### 3. Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 4. Using Systemd (Linux)
```bash
# Create service file
sudo nano /etc/systemd/system/flask-api.service

[Unit]
Description=Flask Blog API
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/flask-api
Environment=PATH=/path/to/flask-api/venv/bin
ExecStart=/path/to/flask-api/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable flask-api
sudo systemctl start flask-api
```

## 🧪 Testing

### Unit Tests
```bash
# Install pytest
pip install pytest

# Run tests
python -m pytest tests/
```

### API Testing with Postman
1. Import the provided Postman collection
2. Set up environment variables
3. Run the authentication flow
4. Test all endpoints

### Load Testing
```bash
# Install locust
pip install locust

# Run load test
locust -f load_test.py
```

## 📝 Logging

### Log Levels
- ERROR: Application errors
- WARNING: Potential issues
- INFO: General information
- DEBUG: Detailed debugging

### Log Configuration
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Check database file exists
ls -la db/

# Recreate database
python manage.py reset-db
```

#### 2. Import Errors
```bash
# Check virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Migration Issues
```bash
# Check migration status
alembic current

# Reset migrations
alembic downgrade base
alembic upgrade head
```

#### 4. CORS Issues
```bash
# Check CORS configuration in app/__init__.py
# Ensure frontend origin is in CORS_ORIGINS
```

#### 5. Rate Limiting Issues
```bash
# Check rate limit headers in response
# Adjust limits in config.py if needed
```

### Debug Mode
```bash
# Enable debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run with debug
python run.py
```

## 📚 Additional Resources

### Documentation
- [API Documentation](API_DOCUMENTATION.md)
- [Enhanced API Documentation](ENHANCED_API_DOCUMENTATION.md)
- [Step-by-Step Rebuild Guide](STEP_BY_STEP_REBUILD_GUIDE.md)

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [JWT Documentation](https://pyjwt.readthedocs.io/)

### Support
- Check logs in `app.log`
- Review error responses
- Test with Postman collection
- Verify environment variables

## 🎯 Next Steps

### Immediate Actions
1. ✅ Set up the API
2. ✅ Test all endpoints
3. ✅ Create admin user
4. ✅ Configure production environment

### Future Enhancements
1. Add email verification
2. Implement password reset
3. Add file upload for images
4. Implement search functionality
5. Add pagination
6. Set up monitoring and alerting
7. Add comprehensive test suite
8. Implement API versioning

### Monitoring
1. Set up application monitoring
2. Configure error tracking
3. Set up performance monitoring
4. Implement health checks
5. Configure backup strategies

The API is now ready for production use with enterprise-level features and security! 