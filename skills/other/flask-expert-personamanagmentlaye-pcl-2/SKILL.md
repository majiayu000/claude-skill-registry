---
name: flask-expert
version: 1.0.0
description: Expert-level Flask web development, REST APIs, extensions, and production deployment
category: frameworks
tags: [flask, python, web-framework, rest-api, jinja2]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(flask:*, python:*)
---

# Flask Expert

Expert guidance for Flask web development, building REST APIs, using extensions, and production deployment.

## Core Concepts

### Flask Fundamentals
- Routing and views
- Request/response handling
- Templates with Jinja2
- Blueprints for modularity
- Application factory pattern
- Configuration management

### Flask Extensions
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (database migrations)
- Flask-Login (authentication)
- Flask-RESTful (REST APIs)
- Flask-JWT-Extended (JWT tokens)
- Flask-CORS (CORS handling)
- Flask-Limiter (rate limiting)

### Best Practices
- Application structure
- Error handling
- Testing
- Security
- Production deployment

## Basic Flask Application

```python
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Application factory
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

# Database setup
db = SQLAlchemy()
migrate = Migrate()

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.to_dict(),
            'created_at': self.created_at.isoformat()
        }
```

## REST API with Flask-RESTful

```python
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, User, Post

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Request parsers
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True)
post_parser.add_argument('content', type=str, required=True)

# Response marshalling
user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601')
}

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'author': fields.Nested(user_fields),
    'created_at': fields.DateTime(dt_format='iso8601')
}

# Resources
class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        """Get all users"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        users = User.query.paginate(page=page, per_page=per_page)
        return users.items

    def post(self):
        """Create new user"""
        args = user_parser.parse_args()

        if User.query.filter_by(email=args['email']).first():
            return {'message': 'Email already exists'}, 400

        user = User(email=args['email'])
        user.set_password(args['password'])

        db.session.add(user)
        db.session.commit()

        return user.to_dict(), 201

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        """Get user by ID"""
        user = User.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        """Delete user"""
        current_user_id = get_jwt_identity()

        if current_user_id != user_id:
            return {'message': 'Unauthorized'}, 403

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return '', 204

class PostListResource(Resource):
    @marshal_with(post_fields)
    def get(self):
        """Get all posts"""
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return posts

    @jwt_required()
    def post(self):
        """Create new post"""
        args = post_parser.parse_args()
        current_user_id = get_jwt_identity()

        post = Post(
            title=args['title'],
            content=args['content'],
            user_id=current_user_id
        )

        db.session.add(post)
        db.session.commit()

        return post.to_dict(), 201

# Register resources
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(PostListResource, '/posts')
```

## Authentication with JWT

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from .models import db, User

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    user = User(email=data['email'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)

    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)

    return jsonify(user.to_dict()), 200
```

## Error Handling

```python
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle HTTP exceptions"""
        return jsonify({
            'error': e.name,
            'message': e.description,
            'code': e.code
        }), e.code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        """Handle database integrity errors"""
        db.session.rollback()
        return jsonify({
            'error': 'Database error',
            'message': 'A database constraint was violated'
        }), 400

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unexpected exceptions"""
        app.logger.exception(e)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(e):
        """Handle 400 errors"""
        return jsonify({
            'error': 'Bad request',
            'message': 'The request was invalid'
        }), 400
```

## Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"
)

def create_app():
    app = Flask(__name__)
    limiter.init_app(app)

    @app.route('/api/search')
    @limiter.limit("10 per minute")
    def search():
        """Rate-limited search endpoint"""
        query = request.args.get('q')
        # Perform search
        return jsonify({'results': []})

    @app.route('/api/expensive')
    @limiter.limit("1 per minute")
    def expensive_operation():
        """Very rate-limited expensive operation"""
        # Expensive computation
        return jsonify({'status': 'completed'})

    return app
```

## Configuration

```python
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

## Testing

```python
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Create authenticated headers"""
    # Register user
    client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    # Login
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_register_user(client):
    """Test user registration"""
    response = client.post('/auth/register', json={
        'email': 'new@example.com',
        'password': 'password123'
    })

    assert response.status_code == 201
    assert response.json['email'] == 'new@example.com'

def test_login(client):
    """Test user login"""
    # Register first
    client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    # Login
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 200
    assert 'access_token' in response.json

def test_create_post(client, auth_headers):
    """Test creating a post"""
    response = client.post('/api/posts',
        json={
            'title': 'Test Post',
            'content': 'Test content'
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    assert response.json['title'] == 'Test Post'

def test_get_posts(client):
    """Test getting all posts"""
    response = client.get('/api/posts')

    assert response.status_code == 200
    assert isinstance(response.json, list)
```

## Production Deployment

```python
# wsgi.py
from app import create_app
import os

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run()
```

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

# With proper workers
gunicorn -w 4 \
  --worker-class gevent \
  --worker-connections 1000 \
  --timeout 30 \
  --keep-alive 5 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  wsgi:app
```

## Best Practices

- Use application factory pattern
- Organize code with blueprints
- Implement proper error handling
- Use environment variables for config
- Write comprehensive tests
- Use database migrations
- Implement authentication/authorization
- Add rate limiting
- Enable CORS properly
- Use connection pooling
- Log appropriately
- Monitor performance

## Anti-Patterns

❌ Global app instance
❌ No database migrations
❌ Hardcoded configuration
❌ Missing error handling
❌ No authentication
❌ Exposing sensitive data
❌ Not using blueprints

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Flask-RESTful: https://flask-restful.readthedocs.io/
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io/
- Miguel Grinberg's Flask Mega-Tutorial: https://blog.miguelgrinberg.com/
