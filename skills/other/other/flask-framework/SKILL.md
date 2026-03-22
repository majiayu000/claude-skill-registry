---
name: flask-framework
description: "Master Flask microframework for building Python web applications, REST APIs, and microservices with blueprints and extensions. Use for: developing lightweight web applications, creating REST APIs, building microservices architecture, implementing modular applications with blueprints, integrating Flask extensions, handling authentication and sessions, deploying Flask apps, and creating scalable backend services."
---

# Flask Framework

Build lightweight, flexible Python web applications and microservices with Flask's minimalist approach.

## Overview

Flask is a Python microframework that provides essential web development tools without imposing rigid structure. Its "micro" nature means it's lightweight and extensible, making it ideal for microservices, REST APIs, and applications where you want full control over architecture. Flask's simplicity and flexibility have made it one of the most popular Python web frameworks.

## When to Use Flask

| Scenario | Reason | Key Feature |
|----------|--------|-------------|
| Microservices | Lightweight and fast startup | Minimal footprint |
| REST APIs | Clean routing and JSON handling | Flask-RESTful extension |
| Prototypes | Quick development | Simple syntax |
| Small to medium apps | No unnecessary overhead | Choose your own tools |
| Learning web development | Easy to understand | Minimal magic |
| Custom architecture | Full control | No enforced structure |
| Serverless functions | Fast cold starts | Small package size |

## Core Concepts

### Basic Application

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    return jsonify({'id': user_id, 'name': 'John'})

if __name__ == '__main__':
    app.run(debug=True)
```

### Routing

```python
# HTTP methods
@app.route('/post', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'POST':
        return jsonify({'message': 'Created'}), 201
    return jsonify({'posts': []})

# URL parameters
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

# Multiple types
@app.route('/post/<int:post_id>')
@app.route('/post/<string:slug>')
def show_post(post_id=None, slug=None):
    if post_id:
        return f'Post ID: {post_id}'
    return f'Post Slug: {slug}'
```

## Request Handling

```python
from flask import request, jsonify

@app.route('/api/data', methods=['POST'])
def handle_data():
    # JSON data
    data = request.get_json()
    
    # Form data
    name = request.form.get('name')
    
    # Query parameters
    page = request.args.get('page', 1, type=int)
    
    # Headers
    auth_token = request.headers.get('Authorization')
    
    # Files
    file = request.files.get('upload')
    if file:
        file.save(f'uploads/{file.filename}')
    
    return jsonify({'status': 'success'})
```

## Blueprints (Modular Applications)

```python
# auth/routes.py
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Authentication logic
    return jsonify({'token': 'abc123'})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out'})

# app.py
from flask import Flask
from auth.routes import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
```

### Nested Blueprints

```python
# api/v1/users.py
from flask import Blueprint

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def list_users():
    return jsonify({'users': []})

# api/v1/__init__.py
from flask import Blueprint
from .users import users_bp

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v1.register_blueprint(users_bp, url_prefix='/users')

# app.py
app.register_blueprint(api_v1)
```

## Flask Extensions

### Flask-SQLAlchemy (Database ORM)

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

# Create tables
with app.app_context():
    db.create_all()

# Usage
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
```

### Flask-JWT-Extended (Authentication)

```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Verify credentials
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)
```

### Flask-CORS

```python
from flask_cors import CORS

# Enable CORS for all routes
CORS(app)

# Or specific routes
CORS(app, resources={r"/api/*": {"origins": "https://example.com"}})
```

### Flask-Migrate (Database Migrations)

```python
from flask_migrate import Migrate

migrate = Migrate(app, db)

# Commands:
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade
```

## Error Handling

```python
from flask import jsonify

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Custom exceptions
class ValidationError(Exception):
    pass

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({'error': str(error)}), 400
```

## Application Factory Pattern

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    db.init_app(app)
    
    from .auth import auth_bp
    from .api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    
    return app

# run.py
from app import create_app

app = create_app('production')

if __name__ == '__main__':
    app.run()
```

## Configuration

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
```

## Testing

```python
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_user(client):
    response = client.post('/users', json={'username': 'test', 'email': 'test@example.com'})
    assert response.status_code == 201
    assert response.json['username'] == 'test'
```

## Deployment

### Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

## Using the Reference Files

### When to Read Each Reference

**`/references/blueprints-architecture.md`** — Read when structuring large Flask applications, implementing modular design, or organizing microservices.

**`/references/extensions-guide.md`** — Read when integrating Flask extensions, choosing the right tools, or extending Flask functionality.

**`/references/api-development.md`** — Read when building REST APIs, implementing authentication, or creating API documentation.
