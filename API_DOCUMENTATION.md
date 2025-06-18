# Flask Blog API Documentation

## Overview

This is a Flask-based REST API for a blog application with user authentication and article management. The API provides endpoints for user registration, authentication, user management, and article CRUD operations.

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
  "profile_image_url": "default.png"
}
```

- **Error (400 Bad Request)**:
```json
{
  "error": "Missing required fields"
}
```

#### 2. User Login
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Authentication**: None required
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

- **Error (401 Unauthorized)**:
```json
{
  "error": "User not found"
}
```
or
```json
{
  "error": "Incorrect password"
}
```

### User Management Endpoints

#### 3. Get All Users
- **URL**: `/api/users/`
- **Method**: `GET`
- **Authentication**: Admin required
- **Description**: Retrieve all users (admin only)

**Response**:
- **Success (200 OK)**:
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "profile_image_url": "default.png"
  }
]
```

#### 4. Get User by ID
- **URL**: `/api/users/{user_id}`
- **Method**: `GET`
- **Authentication**: Login required
- **Description**: Retrieve a specific user by ID

**Parameters**:
- `user_id` (integer, path parameter): User ID

**Response**:
- **Success (200 OK)**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "profile_image_url": "default.png"
}
```

- **Error (404 Not Found)**:
```json
{
  "error": "User not found"
}
```

#### 5. Update User
- **URL**: `/api/users/{user_id}`
- **Method**: `PUT`
- **Authentication**: Login required
- **Description**: Update user information

**Parameters**:
- `user_id` (integer, path parameter): User ID

**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "profile_image_url": "string"
}
```

**Response**:
- **Success (200 OK)**:
```json
{
  "id": 1,
  "username": "updated_username",
  "email": "updated@example.com",
  "profile_image_url": "new_image.png"
}
```

- **Error (404 Not Found)**:
```json
{
  "error": "User not found"
}
```

#### 6. Delete User
- **URL**: `/api/users/{user_id}`
- **Method**: `DELETE`
- **Authentication**: Admin required
- **Description**: Delete a user account

**Parameters**:
- `user_id` (integer, path parameter): User ID

**Response**:
- **Success (200 OK)**:
```json
{
  "message": "User deleted"
}
```

- **Error (404 Not Found)**:
```json
{
  "error": "User not found"
}
```

### Article Management Endpoints

#### 7. Get All Articles
- **URL**: `/api/articles/`
- **Method**: `GET`
- **Authentication**: None required
- **Description**: Retrieve all articles

**Response**:
- **Success (200 OK)**:
```json
[
  {
    "id": 1,
    "title": "Sample Article",
    "content": "This is the article content...",
    "created_at": "2024-01-01T12:00:00Z",
    "user_id": 1
  }
]
```

#### 8. Get Article by ID
- **URL**: `/api/articles/{article_id}`
- **Method**: `GET`
- **Authentication**: None required
- **Description**: Retrieve a specific article by ID

**Parameters**:
- `article_id` (integer, path parameter): Article ID

**Response**:
- **Success (200 OK)**:
```json
{
  "id": 1,
  "title": "Sample Article",
  "content": "This is the article content...",
  "created_at": "2024-01-01T12:00:00Z",
  "user_id": 1
}
```

- **Error (404 Not Found)**:
```json
{
  "error": "Article not found"
}
```

#### 9. Create Article
- **URL**: `/api/articles/`
- **Method**: `POST`
- **Authentication**: Login required
- **Description**: Create a new article

**Request Body**:
```json
{
  "title": "string",
  "content": "string"
}
```

**Response**:
- **Success (201 Created)**:
```json
{
  "id": 1,
  "title": "New Article",
  "content": "Article content...",
  "created_at": "2024-01-01T12:00:00Z",
  "user_id": 1
}
```

#### 10. Update Article
- **URL**: `/api/articles/{article_id}`
- **Method**: `PUT`
- **Authentication**: Login required
- **Description**: Update an existing article

**Parameters**:
- `article_id` (integer, path parameter): Article ID

**Request Body**:
```json
{
  "title": "string",
  "content": "string"
}
```

**Response**:
- **Success (200 OK)**:
```json
{
  "id": 1,
  "title": "Updated Article",
  "content": "Updated content...",
  "created_at": "2024-01-01T12:00:00Z",
  "user_id": 1
}
```

- **Error (404 Not Found)**:
```json
{
  "error": "Article Not Found"
}
```

#### 11. Delete Article
- **URL**: `/api/articles/{article_id}`
- **Method**: `DELETE`
- **Authentication**: Login required
- **Description**: Delete an article

**Parameters**:
- `article_id` (integer, path parameter): Article ID

**Response**:
- **Success (200 OK)**:
```json
{
  "message": "Article deleted"
}
```

- **Error (404 Not Found)**:
```json
{
  "error": "Article Not Found"
}
```

## Data Models

### User Model
```python
{
  "id": "integer (primary key)",
  "username": "string (unique, required)",
  "email": "string (unique, required)",
  "password_hash": "string (required)",
  "profile_image_url": "string (default: 'default.png')"
}
```

### Article Model
```python
{
  "id": "integer (primary key)",
  "title": "string (required)",
  "content": "text (required)",
  "created_at": "datetime (auto-generated)",
  "user_id": "integer (foreign key to users.id, required)"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Security Considerations

1. **Password Hashing**: Passwords are hashed using bcrypt
2. **JWT Authentication**: Tokens expire after 24 hours
3. **Input Validation**: All inputs should be validated (currently missing)
4. **SQL Injection**: Protected by SQLAlchemy ORM
5. **CORS**: Not configured (should be added for production)

## Known Issues and Recommendations

### Critical Issues Found:

1. **Missing Authentication Decorators**: The `login_required` and `admin_required` decorators are imported but not implemented
2. **Missing to_dict() Methods**: Models don't have `to_dict()` methods but are called in routes
3. **Route Registration**: Blueprints are not registered in the main app
4. **Missing Dependencies**: `bcrypt` and `PyJWT` are not in requirements.txt
5. **Typo in Code**: `db.commit()` should be `db.session.commit()` in article controller
6. **Inconsistent Error Handling**: Some endpoints return different error formats
7. **Missing Input Validation**: No validation for request data
8. **Security Issues**: No rate limiting, CORS, or proper error handling

### Recommendations:

1. **Implement Missing Decorators**: Create proper authentication decorators
2. **Add Model Serialization**: Implement `to_dict()` methods for models
3. **Register Blueprints**: Add blueprint registration in app factory
4. **Update Dependencies**: Add missing packages to requirements.txt
5. **Add Input Validation**: Implement request validation
6. **Improve Error Handling**: Standardize error responses
7. **Add Security Headers**: Implement CORS, rate limiting, and security headers
8. **Add Logging**: Implement proper logging for debugging
9. **Add Tests**: Create unit and integration tests
10. **Add Documentation**: Generate OpenAPI/Swagger documentation

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export SECRET_KEY="your-secret-key"
```

3. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## Postman Collection

A Postman collection with example requests can be generated using the OpenAPI specification below.

## OpenAPI 3.0 Specification

```yaml
openapi: 3.0.0
info:
  title: Flask Blog API
  version: 1.0.0
  description: A Flask-based REST API for blog management

servers:
  - url: http://localhost:5000
    description: Development server

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
        profile_image_url:
          type: string
      required:
        - username
        - email

    Article:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        content:
          type: string
        created_at:
          type: string
          format: date-time
        user_id:
          type: integer
      required:
        - title
        - content

paths:
  /api/auth/register:
    post:
      summary: Register a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                password:
                  type: string
              required:
                - username
                - email
                - password
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Bad request

  /api/auth/login:
    post:
      summary: Authenticate user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
              required:
                - email
                - password
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
        '401':
          description: Authentication failed

  /api/users:
    get:
      summary: Get all users
      security:
        - bearerAuth: []
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

  /api/users/{user_id}:
    get:
      summary: Get user by ID
      security:
        - bearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found

    put:
      summary: Update user
      security:
        - bearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                profile_image_url:
                  type: string
      responses:
        '200':
          description: User updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found

    delete:
      summary: Delete user
      security:
        - bearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User deleted successfully
        '404':
          description: User not found

  /api/articles:
    get:
      summary: Get all articles
      responses:
        '200':
          description: List of articles
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Article'

    post:
      summary: Create new article
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                content:
                  type: string
              required:
                - title
                - content
      responses:
        '201':
          description: Article created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Article'

  /api/articles/{article_id}:
    get:
      summary: Get article by ID
      parameters:
        - name: article_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Article details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Article'
        '404':
          description: Article not found

    put:
      summary: Update article
      security:
        - bearerAuth: []
      parameters:
        - name: article_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                content:
                  type: string
      responses:
        '200':
          description: Article updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Article'
        '404':
          description: Article not found

    delete:
      summary: Delete article
      security:
        - bearerAuth: []
      parameters:
        - name: article_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Article deleted successfully
        '404':
          description: Article not found
``` 