---
name: flask
description: |
  Build Python web apps with Flask using application factory pattern, Blueprints, and Flask-SQLAlchemy. Prevents 9 documented errors including stream_with_context teardown issues, async/gevent conflicts, and CSRF cache problems.

  Use when: creating Flask projects, organizing blueprints, or troubleshooting circular imports, context errors, registration, streaming, or authentication.
user-invocable: true
---

# Flask Skill

Production-tested patterns for Flask with the application factory pattern, Blueprints, and Flask-SQLAlchemy.

**Latest Versions** (verified January 2026):
- Flask: 3.1.2
- Flask-SQLAlchemy: 3.1.1
- Flask-Login: 0.6.3
- Flask-WTF: 1.2.2
- Werkzeug: 3.1.5
- **Python**: 3.9+ required (3.8 dropped in Flask 3.1.0)

---

## Quick Start

### Project Setup with uv

```bash
# Create project
uv init my-flask-app
cd my-flask-app

# Add dependencies
uv add flask flask-sqlalchemy flask-login flask-wtf python-dotenv

# Run development server
uv run flask --app app run --debug
```

### Minimal Working Example

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    app.run(debug=True)
```

Run: `uv run flask --app app run --debug`

---

## Known Issues Prevention

This skill prevents **9** documented issues:

### Issue #1: stream_with_context Teardown Regression (Flask 3.1.2)
**Error**: `KeyError` in teardown functions when using `stream_with_context`
**Source**: [GitHub Issue #5804](https://github.com/pallets/flask/issues/5804)
**Why It Happens**: Flask 3.1.2 introduced a regression where `stream_with_context` triggers `teardown_request()` calls multiple times before response generation completes. If teardown callbacks use `g.pop(key)` without a default, they fail on the second call.

**Prevention**:
```python
# WRONG - fails on second teardown call
@app.teardown_request
def _teardown_request(_):
    g.pop("hello")  # KeyError on second call

# RIGHT - idempotent teardown
@app.teardown_request
def _teardown_request(_):
    g.pop("hello", None)  # Provide default value
```

**Status**: Will be fixed in Flask 3.2.0 as side effect of PR #5812. Until then, ensure all teardown callbacks are idempotent.

---

### Issue #2: Async Views with Gevent Incompatibility
**Error**: `RuntimeError` when handling concurrent async requests with gevent
**Source**: [GitHub Issue #5881](https://github.com/pallets/flask/issues/5881)
**Why It Happens**: Asgiref fails when gevent monkey-patching is active. Asyncio expects a single event loop per OS thread, but gevent's monkey-patching makes `threading.Thread` create greenlets instead of real threads, causing both loops to run on the same physical thread and block each other.

**Prevention**: Choose either async (with asyncio/uvloop) OR gevent, not both. If you must use both:

```python
import asyncio
import gevent.monkey
import gevent.selectors
from flask import Flask

gevent.monkey.patch_all()
loop = asyncio.EventLoop(gevent.selectors.DefaultSelector())
gevent.spawn(loop.run_forever)

class GeventFlask(Flask):
    def async_to_sync(self, func):
        def run(*args, **kwargs):
            coro = func(*args, **kwargs)
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            return future.result()
        return run

app = GeventFlask(__name__)
```

**Note**: This "defeats the whole purpose of both" (maintainer comment). Individual async requests work, but concurrent requests fail without this workaround.

---

### Issue #3: Test Client Session Not Updated on Redirect
**Error**: Session state incorrect after `follow_redirects=True` in tests
**Source**: [GitHub Issue #5786](https://github.com/pallets/flask/issues/5786)
**Why It Happens**: In Flask < 3.1.2, the test client's session wasn't correctly updated after following redirects.

**Prevention**:
```python
# If using Flask >= 3.1.2, follow_redirects works correctly
def test_login_redirect(client):
    response = client.post('/login',
        data={'email': 'test@example.com', 'password': 'pass'},
        follow_redirects=True)
    assert 'user_id' in session  # Works in 3.1.2+

# For Flask < 3.1.2, make separate requests
response = client.post('/login', data={...})
assert response.status_code == 302
response = client.get(response.location)  # Explicit redirect follow
```

**Status**: Fixed in Flask 3.1.2. Upgrade to latest version.

---

### Issue #4: Application Context Lost in Threads (Community-sourced)
**Error**: `RuntimeError: Working outside of application context` in background threads
**Source**: [Sentry.io Guide](https://sentry.io/answers/working-outside-of-application-context/)
**Why It Happens**: When passing `current_app` to a new thread, you must unwrap the proxy object using `_get_current_object()` and push app context in the thread.

**Prevention**:
```python
from flask import current_app
import threading

# WRONG - current_app is a proxy, loses context in thread
def background_task():
    app_name = current_app.name  # Fails!

@app.route('/start')
def start_task():
    thread = threading.Thread(target=background_task)
    thread.start()

# RIGHT - unwrap proxy and push context
def background_task(app):
    with app.app_context():
        app_name = app.name  # Works!

@app.route('/start')
def start_task():
    app = current_app._get_current_object()
    thread = threading.Thread(target=background_task, args=(app,))
    thread.start()
```

**Verified**: Common pattern in production applications, documented in official Flask docs.

---

### Issue #5: Flask-Login Session Protection Unexpected Logouts (Community-sourced)
**Error**: Users logged out unexpectedly when IP address changes
**Source**: [Flask-Login Docs](https://flask-login.readthedocs.io/)
**Why It Happens**: Flask-Login's "strong" session protection mode deletes the entire session if session identifiers (like IP address) change. This affects users on mobile networks or VPNs.

**Prevention**:
```python
# app/extensions.py
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = "basic"  # Default, less strict
# login_manager.session_protection = "strong"  # Strict, may logout on IP change
# login_manager.session_protection = None  # Disabled (not recommended)
```

**Note**: By default, Flask-Login allows concurrent sessions (same user on multiple browsers). To prevent this, implement custom session tracking.

**Verified**: Official Flask-Login documentation, multiple 2024 blog posts.

---

### Issue #6: CSRF Protection Cache Interference (Community-sourced)
**Error**: Form submissions fail with "CSRF token missing/invalid" on cached pages
**Source**: [Flask-WTF Docs](https://flask-wtf.readthedocs.io/en/latest/csrf/)
**Why It Happens**: If webserver cache policy caches pages longer than `WTF_CSRF_TIME_LIMIT`, browsers serve cached pages with expired CSRF tokens.

**Prevention**:
```python
# Option 1: Align cache duration with token lifetime
WTF_CSRF_TIME_LIMIT = None  # Never expire (less secure)

# Option 2: Exclude forms from cache
@app.after_request
def add_cache_headers(response):
    if request.method == 'GET' and 'form' in request.endpoint:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

# Option 3: Configure webserver to not cache POST targets
# In Nginx: add "proxy_cache_bypass $cookie_session" for form routes
```

**Verified**: Official Flask-WTF documentation warning, security best practices guides from 2024.

---

### Issue #7: Per-Request max_content_length Override (New Feature)
**Feature**: Flask 3.1.0 added ability to customize `Request.max_content_length` per-request
**Source**: [Flask 3.1.0 Release Notes](https://github.com/pallets/flask/releases/tag/3.1.0)

**Usage**:
```python
from flask import Flask, request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB default

@app.route('/upload', methods=['POST'])
def upload():
    # Override for this specific route
    request.max_content_length = 100 * 1024 * 1024  # 100MB for uploads
    file = request.files['file']
    # ...
```

**Note**: Also added `MAX_FORM_MEMORY_SIZE` and `MAX_FORM_PARTS` config options in 3.1.0. See [security documentation](https://flask.palletsprojects.com/en/stable/security/).

---

### Issue #8: SECRET_KEY Rotation (New Feature)
**Feature**: Flask 3.1.0 added `SECRET_KEY_FALLBACKS` for key rotation
**Source**: [Flask 3.1.0 Release Notes](https://github.com/pallets/flask/releases/tag/3.1.0)

**Usage**:
```python
# config.py
class Config:
    SECRET_KEY = "new-secret-key-2024"
    SECRET_KEY_FALLBACKS = [
        "old-secret-key-2023",
        "older-secret-key-2022"
    ]
```

**Note**: Extensions need explicit support for this feature. Flask-Login and Flask-WTF may need updates to use fallback keys.

---

### Issue #9: Werkzeug 3.1+ Dependency Conflict
**Error**: `flask==2.2.4 incompatible with werkzeug==3.1.3`
**Source**: [Flask 3.1.0 Release Notes](https://github.com/pallets/flask/releases/tag/3.1.0) | [GitHub Issue #5652](https://github.com/pallets/flask/issues/5652)
**Why It Happens**: Flask 3.1.0 updated minimum dependency versions: Werkzeug >= 3.1, ItsDangerous >= 2.2, Blinker >= 1.9. Projects pinned to older versions will have conflicts.

**Prevention**:
```bash
# Update all Pallets projects together
pip install flask>=3.1.0 werkzeug>=3.1.0 itsdangerous>=2.2.0 blinker>=1.9.0

# Or with uv
uv add "flask>=3.1.0" "werkzeug>=3.1.0" "itsdangerous>=2.2.0" "blinker>=1.9.0"
```

---

## Project Structure (Application Factory)

For maintainable applications, use the factory pattern with blueprints:

```
my-flask-app/
├── pyproject.toml
├── config.py                # Configuration classes
├── run.py                   # Entry point
│
├── app/
│   ├── __init__.py          # Application factory (create_app)
│   ├── extensions.py        # Flask extensions (db, login_manager)
│   ├── models.py            # SQLAlchemy models
│   │
│   ├── main/                # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── auth/                # Auth blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── main/
│   │   └── auth/
│   │
│   └── static/
│       ├── css/
│       └── js/
│
└── tests/
    ├── conftest.py
    └── test_main.py
```

---

## Core Patterns

### Application Factory

```python
# app/__init__.py
from flask import Flask
from app.extensions import db, login_manager
from config import Config


def create_app(config_class=Config):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
```

**Key Benefits**:
- Multiple app instances with different configs (testing)
- Avoids circular imports
- Extensions initialized once, bound to app later

### Extensions Module

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
```

**Why separate file?**: Prevents circular imports - models can import `db` without importing `app`.

### Configuration

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
```

### Entry Point

```python
# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

Run: `flask --app run run --debug`

---

## Blueprints

### Creating a Blueprint

```python
# app/main/__init__.py
from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main import routes  # Import routes after bp is created!
```

```python
# app/main/routes.py
from flask import render_template, jsonify
from app.main import bp


@bp.route("/")
def index():
    return render_template("main/index.html")


@bp.route("/api/health")
def health():
    return jsonify({"status": "ok"})
```

### Blueprint with Templates

```python
# app/auth/__init__.py
from flask import Blueprint

bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",  # Blueprint-specific templates
    static_folder="static",       # Blueprint-specific static files
)

from app.auth import routes
```

---

## Database Models

```python
# app/models.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """User model for authentication."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

---

## Authentication with Flask-Login

### Auth Forms

```python
# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match")
    ])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")
```

### Auth Routes

```python
# app/auth/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.extensions import db
from app.models import User


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Logged in successfully!", "success")
            return redirect(next_page or url_for("main.index"))
        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
```

### Protecting Routes

```python
from flask_login import login_required, current_user

@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html", user=current_user)
```

---

## API Routes (JSON)

For REST APIs without templates:

```python
# app/api/__init__.py
from flask import Blueprint

bp = Blueprint("api", __name__)

from app.api import routes
```

```python
# app/api/routes.py
from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import bp
from app.extensions import db
from app.models import User


@bp.route("/users", methods=["GET"])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "email": u.email}
        for u in users
    ])


@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201
```

Register with prefix:
```python
app.register_blueprint(api_bp, url_prefix="/api/v1")
```

---

## Critical Rules

### Always Do

1. **Use application factory pattern** - Enables testing, avoids globals
2. **Put extensions in separate file** - Prevents circular imports
3. **Import routes at bottom of blueprint `__init__.py`** - After `bp` is created
4. **Use `current_app` not `app`** - Inside request context
5. **Use `with app.app_context()`** - When accessing db outside requests

### Never Do

1. **Never import `app` in models** - Causes circular imports
2. **Never access `db` before app context** - RuntimeError
3. **Never store secrets in code** - Use environment variables
4. **Never use `app.run()` in production** - Use Gunicorn
5. **Never skip CSRF protection** - Keep Flask-WTF enabled

---

## Common Errors & Fixes

### Circular Import Error

**Error**: `ImportError: cannot import name 'X' from partially initialized module`

**Cause**: Models importing app, app importing models

**Fix**: Use extensions.py pattern:
```python
# WRONG - circular import
# app/__init__.py
from app.models import User  # models.py imports db from here!

# RIGHT - deferred import
# app/__init__.py
def create_app():
    # ... setup ...
    from app.models import User  # Import inside factory
```

### Working Outside Application Context

**Error**: `RuntimeError: Working outside of application context`

**Cause**: Accessing `current_app`, `g`, or `db` outside request

**Fix**:
```python
# WRONG
from app import create_app
app = create_app()
users = User.query.all()  # No context!

# RIGHT
from app import create_app
app = create_app()
with app.app_context():
    users = User.query.all()  # Has context
```

### Blueprint Not Found

**Error**: `werkzeug.routing.BuildError: Could not build url for endpoint`

**Cause**: Using wrong blueprint prefix in `url_for()`

**Fix**:
```python
# WRONG
url_for("login")

# RIGHT - include blueprint name
url_for("auth.login")
```

### CSRF Token Missing

**Error**: `Bad Request: The CSRF token is missing`

**Cause**: Form submission without CSRF token

**Fix**: Include token in templates:
```html
<form method="post">
    {{ form.hidden_tag() }}  <!-- Adds CSRF token -->
    <!-- form fields -->
</form>
```

---

## Testing

```python
# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
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
```

```python
# tests/test_main.py
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register(client):
    response = client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "testpass123",
        "confirm": "testpass123",
    }, follow_redirects=True)
    assert response.status_code == 200
```

Run: `uv run pytest`

---

## Deployment

### Development
```bash
flask --app run run --debug
```

### Production with Gunicorn
```bash
uv add gunicorn
uv run gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```

### Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

### Environment Variables (.env)
```
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
FLASK_ENV=production
```

---

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Application Factory Pattern](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)

---

**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Added 9 known issues (stream_with_context regression, async/gevent conflicts, test client sessions, threading context, Flask-Login session protection, CSRF cache, new 3.1.0 features, Werkzeug dependencies)
**Maintainer**: Jezweb | jeremy@jezweb.net
