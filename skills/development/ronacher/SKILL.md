---
name: ronacher-pragmatic-design
description: Write Python code in the style of Armin Ronacher, creator of Flask and Jinja2. Emphasizes pragmatic minimalism, explicit over implicit, and composable design. Use when building frameworks, libraries, or applications that need to be extensible and maintainable.
---

# Armin Ronacher Style Guide

## Overview

Armin Ronacher created Flask, Jinja2, Click, Werkzeug, and many other foundational Python libraries. His approach: pragmatic minimalism, explicit behavior, and composable design. Flask's success proves that "micro" can be mighty.

## Core Philosophy

> "Explicit is better than implicit."

> "Simple things should be simple, complex things should be possible."

> "We're all consenting adults here."

Ronacher believes in **trusting developers** with power and flexibility, while providing sensible defaults and clear documentation.

## Design Principles

1. **Explicit Over Implicit**: Never do magic behind the scenes. Make behavior visible.

2. **Composable Over Monolithic**: Small, focused components that work together.

3. **Configuration Over Convention**: Don't hide configuration in naming conventions.

4. **Extension Points**: Design for extensibility from day one.

## When Writing Code

### Always

- Use explicit imports, never implicit `*` imports
- Make dependencies obvious and injectable
- Provide hooks for customization
- Document extension points clearly
- Use context locals sparingly and explicitly
- Prefer composition over inheritance

### Never

- Modify global state silently
- Use metaclass magic without clear benefit
- Hide functionality in `__init__.py` imports
- Create deep inheritance hierarchies
- Make assumptions about the user's environment

### Prefer

- Factory functions over global instances
- Dependency injection over singletons
- Decorators for cross-cutting concerns
- Context managers for resource management
- Plain functions over classes when state isn't needed

## Code Patterns

### The Application Factory Pattern

```python
# BAD: Global application state
from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Impossible to test, configure differently, or run multiple instances

# GOOD: Application factory (Flask pattern)
def create_app(config=None):
    app = Flask(__name__)
    
    # Default configuration
    app.config.from_object('myapp.default_config')
    
    # Override with instance config
    app.config.from_pyfile('config.py', silent=True)
    
    # Override with passed config
    if config:
        app.config.update(config)
    
    # Register blueprints
    from myapp.views import main_bp
    app.register_blueprint(main_bp)
    
    # Initialize extensions
    db.init_app(app)
    
    return app


# Testing is now easy
def test_something():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
```

### Explicit Extension Pattern

```python
# Flask extension pattern: explicit initialization

class Database:
    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        # Store config, set up teardown, etc.
        app.config.setdefault('DATABASE_URI', 'sqlite:///:memory:')
        app.teardown_appcontext(self._teardown)
        
        # Store self on app for retrieval
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['database'] = self
    
    def _teardown(self, exception):
        # Clean up resources
        pass
    
    def get_connection(self):
        # Get connection for current app context
        return self._get_connection_for_app(current_app._get_current_object())


# Usage:
db = Database()

def create_app():
    app = Flask(__name__)
    db.init_app(app)  # Explicit initialization
    return app
```

### Decorator-Based Configuration

```python
# Click-style command decoration

import click

@click.command()
@click.option('--name', default='World', help='Name to greet')
@click.option('--count', default=1, type=int, help='Number of greetings')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose mode')
def hello(name, count, verbose):
    """Simple program that greets NAME for COUNT times."""
    for _ in range(count):
        if verbose:
            click.echo(f'Verbose: About to greet {name}')
        click.echo(f'Hello, {name}!')


# Benefits:
# - Self-documenting
# - Type conversion built-in
# - Help text from decorators
# - Testable without subprocess
```

### Context-Local Pattern (Use Sparingly)

```python
from werkzeug.local import LocalStack, LocalProxy

# Context stack for request-like objects
_request_ctx_stack = LocalStack()

def get_current_request():
    ctx = _request_ctx_stack.top
    if ctx is None:
        raise RuntimeError('No request context')
    return ctx.request

# Proxy that always points to current request
current_request = LocalProxy(get_current_request)


class RequestContext:
    def __init__(self, app, request):
        self.app = app
        self.request = request
    
    def push(self):
        _request_ctx_stack.push(self)
    
    def pop(self):
        _request_ctx_stack.pop()
    
    def __enter__(self):
        self.push()
        return self
    
    def __exit__(self, *args):
        self.pop()


# Explicit context management
with RequestContext(app, request):
    # current_request is now available
    print(current_request.method)
```

### Composable Middleware/Decorators

```python
# Composable decorators for routes

from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if role not in current_user.roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator


def cached(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            key = f'{f.__name__}:{args}:{kwargs}'
            result = cache.get(key)
            if result is None:
                result = f(*args, **kwargs)
                cache.set(key, result, timeout=timeout)
            return result
        return decorated
    return decorator


# Compose them explicitly
@app.route('/admin/users')
@require_auth
@require_role('admin')
@cached(timeout=60)
def admin_users():
    return get_all_users()
```

### Jinja2-Style Template Inheritance

```python
# Explicit template inheritance
# base.html
"""
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
"""

# child.html
"""
{% extends "base.html" %}

{% block title %}My Page{% endblock %}

{% block content %}
<h1>Hello, World!</h1>
{% endblock %}
"""

# Benefits:
# - Explicit extension declaration
# - Clear block boundaries
# - No magic filename conventions
```

## Mental Model

Ronacher designs systems by asking:

1. **What's the minimal core?** Start with the smallest useful thing.
2. **Where are the extension points?** Design for customization from the start.
3. **Is behavior explicit?** Can a reader understand what's happening?
4. **Are components composable?** Can pieces be used independently?

## The Flask Philosophy

- **One way to do configuration**: Use `app.config`
- **One way to register routes**: Use decorators or `add_url_rule`
- **One way to handle requests**: The WSGI interface
- **Many ways to extend**: Blueprints, extensions, middleware

This isn't limiting—it's clarifying.

