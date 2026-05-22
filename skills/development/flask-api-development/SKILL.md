---
name: flask-api-development
description: Develop lightweight Flask APIs with routing, blueprints, database integration, authentication, and request/response handling. Use when building RESTful APIs, microservices, or lightweight web services with Flask.
---

# Flask API Development

## Overview

Create efficient Flask APIs with blueprints for modular organization, SQLAlchemy for ORM, JWT authentication, comprehensive error handling, and proper request validation following REST principles.

## When to Use

- Building RESTful APIs with Flask
- Creating microservices with minimal overhead
- Implementing lightweight authentication systems
- Designing API endpoints with proper validation
- Integrating with relational databases
- Building request/response handling systems

## Instructions

### 1. **Flask Application Setup**

```python
# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret')
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Request ID middleware
@app.before_request
def assign_request_id():
    import uuid
    request.request_id = str(uuid.uuid4())

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': str(error),
        'request_id': request.request_id
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'Resource does not exist',
        'request_id': request.request_id
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'error': 'Internal Server Error',
        'request_id': request.request_id
    }), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('ENV') != 'production')
```

### 2. **Database Models with SQLAlchemy**

```python
# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user', index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'content': self.content,
            'published': self.published,
            'author_id': str(self.user_id),
            'created_at': self.created_at.isoformat()
        }
```

### 3. **Authentication and JWT**

```python
# auth.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from models import User, db

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user
    return None

def login_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.query.get(identity)
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if request.current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# routes/auth.py
from flask import Blueprint, request, jsonify
from auth import authenticate_user, login_required
from models import User, db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400

    user = authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    user = User(email=data['email'], first_name=data.get('first_name'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'user': user.to_dict()}), 201

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({'user': request.current_user.to_dict()}), 200
```

### 4. **Blueprints for Modular API Design**

```python
# routes/users.py
from flask import Blueprint, request, jsonify
from auth import login_required, admin_required
from models import User, db
from sqlalchemy import or_

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('', methods=['GET'])
@login_required
def list_users():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    search = request.args.get('q', '', type=str)

    query = User.query
    if search:
        query = query.filter(or_(
            User.email.ilike(f'%{search}%'),
            User.first_name.ilike(f'%{search}%')
        ))

    paginated = query.paginate(page=page, per_page=limit)
    return jsonify({
        'data': [user.to_dict() for user in paginated.items],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200

@users_bp.route('/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200

@users_bp.route('/<user_id>', methods=['PATCH'])
@login_required
def update_user(user_id):
    if str(request.current_user.id) != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']

    db.session.commit()
    return jsonify({'user': user.to_dict()}), 200

@users_bp.route('/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return '', 204
```

### 5. **Request Validation**

```python
# validators.py
from flask import request, jsonify
from functools import wraps

def validate_json(*required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Request body must be JSON'}), 400

            data = request.get_json()
            missing = [field for field in required_fields if field not in data]

            if missing:
                return jsonify({
                    'error': 'Missing required fields',
                    'missing_fields': missing
                }), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Usage
@users_bp.route('', methods=['POST'])
@validate_json('email', 'password', 'first_name')
def create_user():
    data = request.get_json()
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    # ... rest of logic
```

### 6. **Application Factory and Configuration**

```python
# config.py
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# factory.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

def create_app(config_name='development'):
    app = Flask(__name__)

    if config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    db = SQLAlchemy(app)
    jwt = JWTManager(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.users import users_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    return app
```

## Best Practices

### ✅ DO
- Use blueprints for modular organization
- Implement proper authentication with JWT
- Validate all user input
- Use SQLAlchemy ORM for database operations
- Implement comprehensive error handling
- Use pagination for collection endpoints
- Log errors and important events
- Return appropriate HTTP status codes
- Implement CORS properly
- Use environment variables for configuration

### ❌ DON'T
- Store secrets in code
- Use global variables for shared state
- Ignore database transactions
- Trust user input without validation
- Return stack traces in production
- Use mutable default arguments
- Forget to handle database connection errors
- Implement authentication in route handlers

## Complete Example

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid'}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'email': u.email} for u in users]), 200

if __name__ == '__main__':
    app.run()
```
