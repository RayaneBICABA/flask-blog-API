# 📰 Blog API - Flask RESTful

A minimalist RESTful blog API built with Flask. It allows multiple users to create accounts, publish articles, browse others' posts, search publications, and manage their profiles.

---

## 🚀 MVP - Core Features

- ✅ User account creation
- ✅ Authentication with JWT tokens
- ✅ Article publishing
- ✅ Public article reading
- ✅ Article search by title
- ✅ Author information display
- ✅ Username modification
- ✅ Profile picture updates

---

## 📁 Project Structure

```
flask-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── article.py
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

- **Python** 3.12+
- **Flask** 3.x
- **Flask-RESTful**
- **SQLAlchemy**
- **Flask-JWT-Extended**
- **SQLite** (via SQLAlchemy)
- **DBeaver** (optional DB management)

---

## 🧪 Installation and Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/flask-blog-api.git
cd flask-blog-api

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate    # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python run.py
```

The API runs by default on: 📍 `http://localhost:5000`

---

## 🔐 Authentication

The API uses JWT for securing routes.

- Routes `/register` and `/login` are public
- Other routes (article creation, profile editing) require an **access token**
- Send the token in the `Authorization: Bearer <token>` header

---

## 🧩 API Endpoints

### 🔑 Authentication

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and receive JWT token |

### 👤 User Management

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/user/me` | Get current user profile |
| PUT | `/api/user/update` | Update username or profile picture |

### 📝 Articles

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/articles` | Create a new article |
| GET | `/api/articles` | Get all articles |
| GET | `/api/articles?author=username` | Get articles filtered by author |
| GET | `/api/articles/<id>` | Get specific article by ID |

---

## 📚 Data Models

### 👤 User Model

```json
{
  "id": 1,
  "username": "coder123",
  "email": "coder@email.com",
  "profile_image_url": "https://example.com/profile.jpg",
  "password_hash": "hashed_password"
}
```

### 📝 Article Model

```json
{
  "id": 10,
  "title": "My First Article",
  "content": "Article content goes here...",
  "created_at": "2025-06-13T12:00:00",
  "user_id": 1
}
```

---

## 📋 API Request Examples

### Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Create an Article

```bash
curl -X POST http://localhost:5000/api/articles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My Article Title",
    "content": "This is the content of my article..."
  }'
```

### Get All Articles

```bash
curl -X GET http://localhost:5000/api/articles
```

---

## 🛠️ Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Database Migration

```bash
# Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## 🐛 Error Handling

The API returns consistent error responses:

```json
{
  "error": "Error message",
  "status_code": 400
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

---

## 🔒 Security Considerations

- Passwords are hashed using secure algorithms
- JWT tokens expire after a configurable time
- Input validation on all endpoints
- SQL injection protection via SQLAlchemy ORM

---

## 🎯 Future Enhancements

- [ ] Article comments system
- [ ] User follow/unfollow functionality
- [ ] Article categories and tags
- [ ] Image upload for articles
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Rate limiting
- [ ] API documentation with Swagger/OpenAPI

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Developed with ❤️ by [Your Name]

**Contact:** [your.email@example.com]

**GitHub:** [https://github.com/yourusername](https://github.com/yourusername)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Changelog

### v1.0.0 (2025-06-13)
- Initial release
- Basic CRUD operations for users and articles
- JWT authentication
- RESTful API design