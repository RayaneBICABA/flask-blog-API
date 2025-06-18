# Enhanced Flask Blog API Documentation

## Overview

This is an enhanced Flask-based REST API for a blog application with advanced features including role-based authorization, CORS support, rate limiting, and database migrations. The API provides comprehensive user and article management with proper security controls.

## New Features Added

### 🔐 **Enhanced Authorization System**
- Role-based access control (User/Admin)
- Resource ownership validation
- JWT token authentication with expiration
- Granular permission checks

### 🌐 **CORS Configuration**
- Cross-origin resource sharing enabled
- Configurable allowed origins
- Support for frontend applications

### ⚡ **Rate Limiting**
- Request rate limiting per endpoint
- Configurable limits (daily/hourly/minute)
- Protection against abuse and DDoS

### 🗄️ **Database Migrations**
- Alembic-based migration system
- Version control for database schema
- Rollback capabilities
- Management commands

## Base URL
```
http://localhost:5000
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Most endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
- **URL**: `/api/auth/register`
- **Method**: `POST`
- **Authentication**: None required
- **Rate Limit**: 5 per minute
- **Description**: Register a new user account

**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response**:
- **Success (201 Created)**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "profile_image_url": "default.png",
  "role": "user",
  "created_at": "2024-01-01T12:00:00Z",
  "is_active": true
}
```

#### 2. User Login
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Authentication**: None required
- **Rate Limit**: 5 per minute
- **Description**: Authenticate user and receive JWT token

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response**:
- **Success (200 OK)**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### User Management Endpoints

#### 3. Get All Users
- **URL**: `/api/users/`
- **Method**: `GET`
- **Authentication**: Admin required
- **Rate Limit**: 100 per hour
- **Description**: Retrieve all active users

**Response**:
- **Success (200 OK)**:
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "profile_image_url": "default.png",
    "role": "user",
    "created_at": "2024-01-01T12:00:00Z",
    "is_active": true
  }
]
```

#### 4. Get User by ID
- **URL**: `/api/users/{user_id}`
- **Method**: `GET`
- **Authentication**: Login required (owner or admin)
- **Rate Limit**: 100 per hour
- **Description**: Retrieve a specific user by ID

**Authorization**: Users can only access their own profile unless they are admin

#### 5. Update User
- **URL**: `/api/users/{user_id}`
- **Method**: `PUT`
- **Authentication**: Login required (owner or admin)
- **Rate Limit**: 100 per hour
- **Description**: Update user information

**Authorization**: Users can only update their own profile unless they are admin

#### 6. Delete User (Soft Delete)
- **URL**: `/api/users/{user_id}`
- **Method**: `DELETE`
- **Authentication**: Admin required
- **Rate Limit**: 100 per hour
- **Description**: Soft delete a user account

#### 7. Hard Delete User
- **URL**: `/api/users/{user_id}/hard-delete`
- **Method**: `DELETE`
- **Authentication**: Admin required
- **Rate Limit**: 100 per hour
- **Description**: Permanently delete a user account

#### 8. Update User Role
- **URL**: `/api/users/{user_id}/role`
- **Method**: `PUT`
- **Authentication**: Admin required
- **Rate Limit**: 100 per hour
- **Description**: Change user role

**Request Body**:
```json
{
  "role": "admin"
}
```

#### 9. Get Users by Role
- **URL**: `/api/users/role/{role}`
- **Method**: `GET`
- **Authentication**: Admin required
- **Rate Limit**: 100 per hour
- **Description**: Get all users with specific role

#### 10. Get Current User Profile
- **URL**: `/api/users/profile`
- **Method**: `GET`
- **Authentication**: Login required
- **Rate Limit**: 100 per hour
- **Description**: Get current user's profile

#### 11. Update Current User Profile
- **URL**: `/api/users/profile`
- **Method**: `PUT`
- **Authentication**: Login required
- **Rate Limit**: 100 per hour
- **Description**: Update current user's profile

### Article Management Endpoints

#### 12. Get All Articles
- **URL**: `/api/articles/`
- **Method**: `GET`
- **Authentication**: None required
- **Rate Limit**: 100 per hour
- **Description**: Retrieve all published articles (public)

**Response**:
- **Success (200 OK)**:
```json
[
  {
    "id": 1,
    "title": "Sample Article",
    "content": "This is the article content...",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z",
    "user_id": 1,
    "is_published": true
  }
]
```

#### 13. Get Article by ID
- **URL**: `/api/articles/{article_id}`
- **Method**: `GET`
- **Authentication**: None required (for published articles)
- **Rate Limit**: 100 per hour
- **Description**: Retrieve a specific article by ID

**Authorization**: Unpublished articles are only visible to owners and admins

#### 14. Create Article
- **URL**: `/api/articles/`
- **Method**: `POST`
- **Authentication**: Login required
- **Rate Limit**: 100 per hour
- **Description**: Create a new article

**Request Body**:
```json
{
  "title": "string",
  "content": "string",
  "is_published": true
}
```

#### 15. Update Article
- **URL**: `/api/articles/{article_id}`
- **Method**: `PUT`
- **Authentication**: Login required (owner or admin)
- **Rate Limit**: 100 per hour
- **Description**: Update an existing article

**Authorization**: Users can only update their own articles unless they are admin

#### 16. Delete Article
- **URL**: `/api/articles/{article_id}`
- **Method**: `DELETE`
- **Authentication**: Login required (owner or admin)
- **Rate Limit**: 100 per hour
- **Description**: Delete an article

**Authorization**: Users can only delete their own articles unless they are admin

#### 17. Get My Articles
- **URL**: `/api/articles/my-articles`
- **Method**: `GET`
- **Authentication**: Login required
- **Rate Limit**: 100 per hour
- **Description**: Get current user's articles

#### 18. Toggle Article Publish Status
- **URL**: `/api/articles/{article_id}/publish`
- **Method**: `PUT`
- **Authentication**: Login required (owner or admin)
- **Rate Limit**: 100 per hour
- **Description**: Publish or unpublish an article

**Request Body**:
```json
{
  "is_published": true
}
```

## Enhanced Data Models

### User Model
```python
{
  "id": "integer (primary key)",
  "username": "string (unique, required)",
  "email": "string (unique, required)",
  "password_hash": "string (required)",
  "profile_image_url": "string (default: 'default.png')",
  "role": "string (default: 'user', options: 'user', 'admin')",
  "created_at": "datetime (auto-generated)",
  "is_active": "boolean (default: true)"
}
```

### Article Model
```python
{
  "id": "integer (primary key)",
  "title": "string (required)",
  "content": "text (required)",
  "created_at": "datetime (auto-generated)",
  "updated_at": "datetime (auto-updated)",
  "user_id": "integer (foreign key to users.id, required)",
  "is_published": "boolean (default: true)"
}
```

## Authorization Rules

### Role-Based Access Control

#### User Role
- Can create, read, update, delete their own articles
- Can read their own profile
- Can update their own profile (except role)
- Cannot access other users' data
- Cannot access unpublished articles from other users

#### Admin Role
- Can perform all operations on all resources
- Can manage user roles
- Can view all articles (published and unpublished)
- Can delete users (soft and hard delete)
- Can access all user data

### Resource Ownership
- Users can only access resources they own
- Admins can access all resources
- Ownership is checked for each operation

## Rate Limiting

### Default Limits
- **Global**: 200 requests per day, 50 per hour
- **Authentication**: 5 requests per minute
- **API Endpoints**: 100 requests per hour

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## CORS Configuration

### Allowed Origins
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:8080`

### Allowed Methods
- GET, POST, PUT, DELETE, OPTIONS

### Allowed Headers
- Content-Type
- Authorization

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": ["Field is required", "Invalid email format"]
}
```

### 401 Unauthorized
```json
{
  "error": "Token is missing"
}
```
or
```json
{
  "error": "Token has expired"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied"
}
```
or
```json
{
  "error": "Admin privileges required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Database Migrations

### Migration Commands

#### Initialize Migrations
```bash
alembic init migrations
```

#### Create Migration
```bash
alembic revision --autogenerate -m "Add user role field"
```

#### Apply Migrations
```bash
alembic upgrade head
```

#### Rollback Migration
```bash
alembic downgrade -1
```

#### View Migration History
```bash
alembic history
```

### Management Commands

#### Initialize Database
```bash
python manage.py init-db
```

#### Create Admin User
```bash
python manage.py create-admin
```

#### Run Migrations
```bash
python manage.py migrate
```

#### Create Migration
```bash
python manage.py migrate-create
```

#### List Users
```bash
python manage.py list-users
```

## Security Features

### Password Security
- bcrypt hashing with salt
- Configurable password strength requirements
- Secure password storage

### JWT Security
- 24-hour token expiration
- Secure token generation
- Token validation on each request

### Input Validation
- Request data validation
- SQL injection protection via SQLAlchemy
- XSS protection

### Rate Limiting
- Per-endpoint rate limiting
- IP-based limiting
- Configurable limits

### CORS Protection
- Origin validation
- Method restriction
- Header validation

## Testing

### Manual Testing
Use the provided Postman collection for comprehensive testing.

### Automated Testing
```bash
# Run tests (when implemented)
python -m pytest tests/
```

## Deployment

### Environment Variables
```bash
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"
export DATABASE_URL="sqlite:///db/blogapi.db"
```

### Production Considerations
1. Use a production database (PostgreSQL, MySQL)
2. Set up proper logging
3. Configure HTTPS
4. Set up monitoring
5. Implement backup strategies
6. Use environment-specific configurations

## Monitoring and Logging

### Log Levels
- ERROR: Application errors
- WARNING: Potential issues
- INFO: General information
- DEBUG: Detailed debugging

### Health Check Endpoint
```bash
GET /health
```

## API Versioning

The API supports versioning through URL prefixes:
- Current version: `/api/`
- Future versions: `/api/v2/`, `/api/v3/`

## Support and Documentation

For additional support:
- Check the API documentation
- Review error logs
- Contact the development team

## Changelog

### Version 2.0.0
- Added role-based authorization
- Implemented CORS support
- Added rate limiting
- Added database migrations
- Enhanced security features
- Improved error handling
- Added management commands 