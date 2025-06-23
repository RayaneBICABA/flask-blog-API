![Ryko Logo](logo/RykoLogo.png)

# Flask Blog API

A robust and secure RESTful API built with Flask for managing users and blog articles. This API supports user authentication, role-based authorization, article CRUD operations, and advanced features like rate limiting, CORS, and database migrations.

---

## Features

- User registration and JWT-based authentication
- Role-based access control (User/Admin)
- User profile management
- Article creation, reading, updating, and deletion
- Rate limiting to prevent abuse
- CORS support for frontend integration
- Database migrations with Alembic
- Secure password hashing with bcrypt
- Comprehensive error handling and validation

---

## Tech Stack

- Python 3.8+
- Flask 3.x
- Flask-RESTful
- SQLAlchemy ORM
- Flask-JWT-Extended
- Alembic for migrations
- SQLite (default, configurable to other DBs)
- bcrypt for password hashing

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip
- Git (optional)

### Steps

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd flask-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file or export variables:
   ```bash
   export SECRET_KEY="your-secret-key"
   export JWT_SECRET_KEY="your-jwt-secret-key"
   export FLASK_ENV="development"
   export DATABASE_URL="sqlite:///db/blogapi.db"
   export LOG_LEVEL="INFO"
   ```

5. Initialize the database and create an admin user:
   ```bash
   python manage.py init-db
   python manage.py create-admin
   ```

6. Run the application:
   ```bash
   python run.py
   ```

The API will be available at: `http://localhost:5000`

---

## Usage and API Overview

### Authentication

- Use JWT tokens for securing endpoints.
- Public endpoints: `/api/auth/register`, `/api/auth/login`
- Protected endpoints require `Authorization: Bearer <token>` header.

### Main API Endpoints

| Resource       | Endpoint                  | Method | Auth Required | Description                      |
|----------------|---------------------------|--------|---------------|--------------------------------|
| Authentication | `/api/auth/register`       | POST   | No            | Register a new user             |
| Authentication | `/api/auth/login`          | POST   | No            | Login and receive JWT token     |
| Users          | `/api/users/`              | GET    | Admin         | Get all users                  |
| Users          | `/api/users/{user_id}`     | GET    | Owner/Admin   | Get user by ID                 |
| Users          | `/api/users/{user_id}`     | PUT    | Owner/Admin   | Update user info               |
| Users          | `/api/users/{user_id}`     | DELETE | Admin         | Soft delete user               |
| Articles       | `/api/articles/`           | GET    | No            | Get all published articles     |
| Articles       | `/api/articles/{article_id}`| GET   | No            | Get article by ID              |
| Articles       | `/api/articles/`           | POST   | User          | Create a new article           |
| Articles       | `/api/articles/{article_id}`| PUT   | Owner/Admin   | Update an article              |
| Articles       | `/api/articles/{article_id}`| DELETE| Owner/Admin   | Delete an article              |

For full API details, refer to the [API Documentation](API_DOCUMENTATION.md) and [Enhanced API Documentation](ENHANCED_API_DOCUMENTATION.md).

---

## Security

- Passwords hashed securely with bcrypt.
- JWT tokens expire after 24 hours.
- Role-based access control with user and admin roles.
- Rate limiting to prevent abuse.
- CORS configured for allowed origins and methods.
- Input validation and SQL injection protection via SQLAlchemy.

---

## Data Models

### User Model

| Field             | Type     | Description                          |
|-------------------|----------|----------------------------------|
| id                | Integer  | Primary key                       |
| username          | String   | Unique username                   |
| email             | String   | Unique email                     |
| password_hash     | String   | Hashed password                  |
| profile_image_url | String   | URL or path to profile image     |
| role              | String   | User role (user/admin)            |
| created_at        | DateTime | Account creation timestamp       |
| is_active         | Boolean  | Active status                    |

### Article Model

| Field        | Type     | Description                          |
|--------------|----------|----------------------------------|
| id           | Integer  | Primary key                       |
| title        | String   | Article title                    |
| content      | Text     | Article content                  |
| created_at   | DateTime | Creation timestamp               |
| updated_at   | DateTime | Last update timestamp            |
| user_id      | Integer  | Foreign key to User              |
| is_published | Boolean  | Publication status               |

---

## Error Handling

Common error responses include:

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or token invalid
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

Error responses follow this format:

```json
{
  "error": "Error message"
}
```

---

## Testing

- Use the provided Postman collection (`POSTMAN_COLLECTION.json`) for API testing.
- Run automated tests (when implemented) with:
  ```bash
  python -m pytest tests/
  ```

---

## Deployment

### Production Environment Variables

```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export JWT_SECRET_KEY=your-production-jwt-secret
export DATABASE_URL=postgresql://user:password@localhost/dbname
export LOG_LEVEL=WARNING
```

### Running with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Systemd Service Example (Linux)

```ini
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
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

Engineered with 💙 by Ryko – BICABA P. Jean-Louis Rayane

- Email: rayanebicaba.dev@gmail.com
- GitHub: [https://github.com/yourusername](https://github.com/RayaneBICABA)

---

## Additional Documentation

- [API Documentation](API_DOCUMENTATION.md)
- [Enhanced API Documentation](ENHANCED_API_DOCUMENTATION.md)
- [Postman Collection](POSTMAN_COLLECTION.json)
- [OpenAPI Specification](openapi.yaml)
