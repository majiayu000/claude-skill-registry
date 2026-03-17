---
name: flaskapi
description: Flask API development including blueprints, extensions, and REST patterns. Activate for Flask apps, Python web APIs, and lightweight API development.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Flask API Skill

Provides comprehensive Flask API development capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Flask application development
- Blueprint organization
- Flask extensions
- REST API patterns
- Flask deployment

## Application Structure

\`\`\`
app/
├── __init__.py          # Application factory
├── config.py            # Configuration
├── extensions.py        # Flask extensions
├── models/
│   ├── __init__.py
│   └── agent.py
├── api/
│   ├── __init__.py
│   ├── agents.py        # Agents blueprint
│   └── tasks.py         # Tasks blueprint
├── services/
│   ├── __init__.py
│   └── agent_service.py
└── utils/
    └── validators.py
\`\`\`

## Application Factory

\`\`\`python
# app/__init__.py
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, cors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints
    from app.api.agents import agents_bp
    from app.api.tasks import tasks_bp

    app.register_blueprint(agents_bp, url_prefix='/api/v1/agents')
    app.register_blueprint(tasks_bp, url_prefix='/api/v1/tasks')

    # Register error handlers
    register_error_handlers(app)

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'golden-armada'}

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
\`\`\`

## Configuration

\`\`\`python
# app/config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
\`\`\`

## Extensions

\`\`\`python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
\`\`\`

## Models

\`\`\`python
# app/models/agent.py
from app.extensions import db
from datetime import datetime
import uuid

class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='idle')
    config = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = db.relationship('Task', backref='agent', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'config': self.config,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
\`\`\`

## Blueprints (API Routes)

\`\`\`python
# app/api/agents.py
from flask import Blueprint, request, jsonify
from app.models.agent import Agent
from app.extensions import db
from app.utils.validators import validate_agent_input

agents_bp = Blueprint('agents', __name__)

@agents_bp.route('/', methods=['GET'])
def list_agents():
    """List all agents with optional filtering."""
    agent_type = request.args.get('type')
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Agent.query

    if agent_type:
        query = query.filter(Agent.type == agent_type)
    if status:
        query = query.filter(Agent.status == status)

    pagination = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'agents': [agent.to_dict() for agent in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@agents_bp.route('/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get a specific agent by ID."""
    agent = Agent.query.get_or_404(agent_id)
    return jsonify(agent.to_dict())

@agents_bp.route('/', methods=['POST'])
def create_agent():
    """Create a new agent."""
    data = request.get_json()

    errors = validate_agent_input(data)
    if errors:
        return jsonify({'errors': errors}), 400

    agent = Agent(
        name=data['name'],
        type=data['type'],
        config=data.get('config', {})
    )

    db.session.add(agent)
    db.session.commit()

    return jsonify(agent.to_dict()), 201

@agents_bp.route('/<agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Update an existing agent."""
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()

    if 'name' in data:
        agent.name = data['name']
    if 'config' in data:
        agent.config = data['config']
    if 'status' in data:
        agent.status = data['status']

    db.session.commit()
    return jsonify(agent.to_dict())

@agents_bp.route('/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent."""
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return '', 204
\`\`\`

## JWT Authentication

\`\`\`python
# app/api/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token})

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())
\`\`\`

## Request Validation

\`\`\`python
# app/utils/validators.py
def validate_agent_input(data):
    errors = []

    if not data.get('name'):
        errors.append('Name is required')
    elif len(data['name']) > 100:
        errors.append('Name must be less than 100 characters')

    valid_types = ['claude', 'gpt', 'gemini', 'ollama']
    if not data.get('type'):
        errors.append('Type is required')
    elif data['type'] not in valid_types:
        errors.append(f'Type must be one of: {", ".join(valid_types)}')

    return errors
\`\`\`

## CLI Commands

\`\`\`python
# app/cli.py
import click
from flask.cli import with_appcontext
from app.extensions import db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Seed the database with sample data."""
    from app.models.agent import Agent
    agents = [
        Agent(name='Claude Agent', type='claude'),
        Agent(name='GPT Agent', type='gpt'),
    ]
    db.session.add_all(agents)
    db.session.commit()
    click.echo('Seeded the database.')
\`\`\`

## Run Commands

\`\`\`bash
# Development
flask run --debug

# Production (Gunicorn)
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"

# Database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
\`\`\`
