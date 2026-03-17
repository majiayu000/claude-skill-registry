---
name: flask
description: A WSGI web framework for building HTTP applications with routing, request/response handling, templates, and modular blueprints.
version: 3.1.3
ecosystem: python
license: BSD-3-Clause
generated_with: gpt-5.2
---

## Imports

```python
import flask
from flask import (
    Flask,
    Blueprint,
    request,
    render_template,
    jsonify,
    redirect,
    url_for,
    abort,
    send_file,
    stream_with_context,
)
from flask import AppContext, Request
```

## Core Patterns

### Application + Routes + Responses ✅ Current
```python
from __future__ import annotations

from typing import Any

from flask import Flask, abort, jsonify, redirect, request, url_for

app = Flask(__name__)


@app.get("/")
def index() -> str:
    return "OK"


@app.post("/echo")
def echo() -> tuple[dict[str, Any], int]:
    data = request.get_json(silent=True) or {}
    if "message" not in data:
        abort(400, description="Missing 'message'")
    return jsonify(received=data["message"]), 200


@app.post("/submit")
def submit() -> "flask.wrappers.Response":
    # Flask 3.1.3: redirect() defaults to 302 unless code is provided.
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Prefer: `flask --app app run --debug`
    app.run(debug=True)
```
* Use `Flask` to create an app, decorators to add routes, `request` for input, and `jsonify` / `redirect` / `abort` for common responses.
* Note: `redirect(...)` default status is 302 in Flask 3.1.3.

### Blueprints for Modular Routing ✅ Current
```python
from __future__ import annotations

from flask import Blueprint, Flask, jsonify, url_for

app = Flask(__name__)

api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/health")
def health() -> tuple[dict[str, str], int]:
    return jsonify(status="ok"), 200


@api.get("/links")
def links() -> dict[str, str]:
    # Prefer blueprint-relative endpoint references within the same blueprint.
    return {"health": url_for(".health", _external=False)}


app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
```
* Use `Blueprint` to group routes and register them with `Flask.register_blueprint`.
* Use `url_for(".endpoint")` to reference endpoints within the same blueprint without hard-coding the blueprint name.

### Templates + Namespacing ✅ Current
```python
from __future__ import annotations

from flask import Blueprint, Flask, render_template

app = Flask(__name__)

# Blueprint templates are resolved relative to the app's template folder by default
admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.get("/")
def dashboard() -> str:
    # Recommended: organize templates in app's templates/ folder as admin/index.html
    # This avoids collisions with other templates
    return render_template("admin/index.html")


app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True)
```
* Use `render_template` for Jinja templates.
* Namespace blueprint templates (e.g., `templates/admin/...`) to avoid collisions with app templates or other blueprints.
* By default, blueprints share the app's template folder; organize files in subdirectories for clarity.

### Streaming Responses with Request Context ✅ Current
```python
from __future__ import annotations

from collections.abc import Iterator

from flask import Flask, stream_with_context

app = Flask(__name__)


@app.get("/stream")
def stream() -> Iterator[bytes]:
    @stream_with_context
    def generate() -> Iterator[bytes]:
        yield b"line 1\n"
        yield b"line 2\n"

    return generate()


if __name__ == "__main__":
    app.run(debug=True)
```
* Use `stream_with_context` so generators can access request context during streaming.

### Files and Resources (app / blueprint) ✅ Current
```python
from __future__ import annotations

from pathlib import Path

from flask import Blueprint, Flask, send_file

app = Flask(__name__)
bp = Blueprint("assets", __name__, url_prefix="/assets")


@app.get("/app-resource")
def app_resource() -> str:
    # Reads from the application's root_path (package/module location).
    with app.open_resource("pyproject.toml", mode="r") as f:
        return f.readline().strip()


@bp.get("/bp-resource")
def bp_resource() -> str:
    # Reads relative to the blueprint's root_path.
    with bp.open_resource("README.md", mode="r") as f:
        return f.readline().strip()


@app.get("/download")
def download() -> "flask.wrappers.Response":
    path = Path(__file__).resolve()
    return send_file(path, as_attachment=True, download_name=path.name)


app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
```
* Use `Flask.open_resource` / `Blueprint.open_resource` to read packaged resources.
* Use `send_file` to return a file response (downloads, static artifacts, etc.).

### Flash Messages ✅ Current
```python
from __future__ import annotations

from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "your-secret-key"


@app.post("/submit")
def submit() -> "flask.wrappers.Response":
    # Flash a message to be displayed on the next request
    flash("Form submitted successfully!")
    flash("Warning: check your input", "warning")
    return redirect(url_for("index"))


@app.get("/")
def index() -> str:
    # Retrieve flashed messages with categories
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True)
```
* Use `flash()` to store messages in the session for display on the next request.
* Use `get_flashed_messages(with_categories=True)` to retrieve messages with their categories.

### Session Management ✅ Current
```python
from __future__ import annotations

from flask import Flask, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your-secret-key"


@app.post("/login")
def login() -> "flask.wrappers.Response":
    session["user_id"] = 123
    session["username"] = "alice"
    # Make session persist beyond browser closure
    session.permanent = True
    return redirect(url_for("index"))


@app.get("/profile")
def profile() -> str:
    user_id = session.get("user_id")
    if user_id is None:
        return "Not logged in", 401
    return f"User ID: {user_id}"


@app.post("/logout")
def logout() -> "flask.wrappers.Response":
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
```
* Use `session` to store user data across requests (stored in signed cookies by default).
* Set `session.permanent = True` to make the session persist beyond browser closure.
* Use `session.clear()` to remove all session data.

## Configuration

- Prefer running the dev server via CLI:
  - `flask --app app run --debug`
- If calling `Flask.run()` in code, guard with:
  - `if __name__ == "__main__": app.run(debug=True)`
- Common security / deployment-related configuration (Flask 3.1+ conventions):
  - `SECRET_KEY`: primary secret for session signing.
  - `SECRET_KEY_FALLBACKS`: rotate secrets (extensions must support it).
  - `SESSION_COOKIE_PARTITIONED`: enable CHIPS cookie attribute when needed.
  - `TRUSTED_HOSTS`: enable host validation; accessible via `Request.trusted_hosts`.
- Request limits:
  - `MAX_CONTENT_LENGTH`: enforce max request size.
  - `MAX_FORM_MEMORY_SIZE`: limit form data memory usage.
  - `MAX_FORM_PARTS`: limit number of form parts.
- `.env` support:
  - `flask.load_dotenv()` can load environment variables from a dotenv file (commonly used by the CLI workflow).

## Pitfalls

### Wrong: Running the dev server at import time (breaks CLI discovery / production imports)
```python
from flask import Flask

app = Flask(__name__)

# Wrong: executed on import.
app.run(debug=True)
```

### Right: Guard `run()` with a main block (or prefer `flask run`)
```python
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
```

### Wrong: Using the built-in dev server in production
```python
from flask import Flask

app = Flask(__name__)

# Wrong: the built-in server is not for production.
app.run(host="0.0.0.0", port=80)
```

### Right: Use the CLI for development; use a production WSGI server for deployment
```python
from flask import Flask

app = Flask(__name__)

# Development:
#   $ flask --app app run --debug
# Production:
#   Run behind a production WSGI server (see Flask deploying docs).
```

### Wrong: Assuming a blueprint 404 handler catches unknown URLs outside its routes
```python
from flask import Blueprint

bp = Blueprint("bp", __name__)

@bp.errorhandler(404)
def not_found(e):  # noqa: ANN001
    return "Not found", 404

# Wrong expectation: this will handle /does-not-exist even if it never matched bp routes.
```

### Right: Register 404/405 handlers at the app level (optionally scope by path)
```python
from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.errorhandler(404)
@app.errorhandler(405)
def handle_api_errors(ex):  # noqa: ANN001
    if request.path.startswith("/api/"):
        return jsonify(error=str(ex)), ex.code
    return ex
```

### Wrong: Blueprint static files without `url_prefix` (shadowed by app `/static`)
```python
from flask import Blueprint, Flask

app = Flask(__name__)
admin = Blueprint("admin", __name__, static_folder="static")

app.register_blueprint(admin)

# Wrong expectation: /static/... will serve admin's static files.
```

### Right: Give the blueprint a `url_prefix` so its static route is reachable
```python
from flask import Blueprint, Flask

app = Flask(__name__)
admin = Blueprint("admin", __name__, static_folder="static", url_prefix="/admin")

app.register_blueprint(admin)

# Blueprint static is served under /admin/static/...
```

### Wrong: Template path collisions between app and blueprint templates
```python
from flask import Blueprint, Flask, render_template

app = Flask(__name__)
admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.get("/")
def index() -> str:
    # Wrong: can resolve to app's templates/index.html instead of the blueprint's.
    return render_template("index.html")

app.register_blueprint(admin)
```

### Right: Namespace blueprint templates under a subfolder and reference it explicitly
```python
from flask import Blueprint, Flask, render_template

app = Flask(__name__)
admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.get("/")
def index() -> str:
    return render_template("admin/index.html")

app.register_blueprint(admin)
```

### Wrong: Assuming session access operations are read-only
```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "key"

@app.get("/")
def index() -> str:
    # Wrong: checking membership marks session as accessed, may trigger save/Vary header
    if "user_id" in session:
        return "Logged in"
    return "Not logged in"
```

### Right: Be aware that session operations mark it as accessed
```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "key"

@app.get("/")
def index() -> str:
    # Right: understand that 'in' and 'len' mark session as accessed
    # This may set Vary: Cookie header and trigger session refresh
    if "user_id" in session:
        return "Logged in"
    return "Not logged in"
```

## References

- [Donate](https://palletsprojects.com/donate)
- [Documentation](https://flask.palletsprojects.com/)
- [Changes](https://flask.palletsprojects.com/page/changes/)
- [Source](https://github.com/pallets/flask/)
- [Chat](https://discord.gg/pallets)

## Migration from v3.0.x

- Python support:
  - 🗑️ Removed: Python 3.8 support dropped in 3.1.0.
  - Action: upgrade runtime to Python 3.9+.
- Version attribute:
  - ⚠️ Hard Deprecation: `flask.__version__` deprecated in 3.1.0 (will be removed in 3.2.0).
    - Deprecated since: 3.1.0
    - Still works: True (with deprecation warning)
    - Modern alternative: `importlib.metadata.version("flask")`
    - Migration guidance:
      ```python
      from importlib.metadata import version

      print(version("flask"))
      ```
- Dependency updates:
  - Minimum Werkzeug version: 3.1+
  - Minimum ItsDangerous version: 2.2+
  - Minimum Blinker version: 1.9+
  - Action: update dependencies to meet minimum versions.
- `SERVER_NAME` behavior change:
  - ⚠️ Breaking: `SERVER_NAME` no longer restricts requests to only that domain.
  - Migration guidance: use `TRUSTED_HOSTS` config for host validation.
- Environment file precedence:
  - ⚠️ Breaking: `-e path` CLI option now takes precedence over default `.env` and `.flaskenv` files.
  - Migration guidance: if relying on default files to override explicit `-e path`, restructure configuration. Use `load_defaults=False` with `load_dotenv()` if needed.
- Session access behavior:
  - ⚠️ Behavioral change: operations like `in` and `len` on session now mark it as accessed.
  - Migration guidance: be aware that checking session membership may trigger session save and set `Vary: Cookie` header.

## API Reference

- **Flask(import_name)** - Create the WSGI application; `import_name` usually `__name__`.
- **Blueprint(name, import_name, url_prefix=..., template_folder=..., static_folder=...)** - Modular group of routes, templates, and static files.
- **Flask.run(host=None, port=None, debug=None, ...)** - Run the built-in dev server (development only; prefer `flask run`).
- **Flask.register_blueprint(blueprint, url_prefix=None, ...)** - Attach blueprint routes and handlers to the app.
- **Flask.open_resource(resource, mode="rb")** - Open a resource file relative to the app's `root_path`.
- **Flask.open_instance_resource(resource, mode="rb")** - Open a resource file relative to the instance folder.
- **Blueprint.open_resource(resource, mode="rb")** - Open a resource file relative to the blueprint's `root_path`.
- **Blueprint.route(rule, **options)** - Decorator to register a view function on a blueprint (use `.get`, `.post` variants when available).
- **Blueprint.register_blueprint(child, url_prefix=None, ...)** - Nest a blueprint under another blueprint.
- **Blueprint.errorhandler(code_or_exception)** - Register an error handler scoped to errors raised from within that blueprint's views.
- **Blueprint.root_path** - Filesystem path used as base for blueprint resources.
- **render_template(template_name, **context)** - Render a Jinja template to a response body.
- **render_template_string(source, **context)** - Render a Jinja template from a string.
- **stream_template(template_name, **context)** - Render a Jinja template as a stream.
- **stream_template_string(source, **context)** - Render a Jinja template from a string as a stream.
- **abort(code, description=None)** - Raise an HTTP exception (e.g., 400, 404, 403).
- **url_for(endpoint, **values)** - Build a URL for an endpoint; use `url_for(".name")` within a blueprint.
- **redirect(location, code=302)** - Return a redirect response (default 302 in Flask 3.1.3).
- **jsonify(*args, **kwargs)** - Create a JSON response with correct mimetype.
- **flask.json.dumps(obj, **kwargs)** - Serialize data as JSON string.
- **flask.json.dump(obj, fp, **kwargs)** - Serialize data as JSON and write to file.
- **flask.json.loads(s, **kwargs)** - Deserialize JSON string to Python object.
- **flask.json.load(fp, **kwargs)** - Deserialize JSON from file to Python object.
- **request** - Request proxy for accessing headers, args, JSON, form data, etc.
- **session** - Session proxy for accessing session data stored in signed cookies.
- **g** - Application context global object for storing data during a request.
- **current_app** - Proxy to the current Flask application.
- **stream_with_context(generator_or_function)** - Ensure a generator runs with the current request context.
- **send_file(path_or_file, mimetype=None, as_attachment=False, download_name=None, ...)** - Send a file-like object or path as a response.
- **send_from_directory(directory, path, **kwargs)** - Send a file from a directory (safely validates path).
- **flash(message, category="message")** - Store a message in the session for display on the next request.
- **get_flashed_messages(with_categories=False, category_filter=())** - Retrieve flashed messages from the session.
- **make_response(*args)** - Convert return values to Response objects.
- **after_this_request(f)** - Register a function to run after the current request.
- **copy_current_request_context(f)** - Copy the current request context to a function.
- **has_app_context()** - Check if an application context is active.
- **has_request_context()** - Check if a request context is active.
- **load_dotenv(path=None, **kwargs)** - Load environment variables from a dotenv file (commonly used with CLI).
- **get_template_attribute(template_name, attribute)** - Load a macro or variable from a template.
- **AppContext** - Application context object.
- **Request** - Request class; includes attributes like `max_content_length` and `trusted_hosts`.
- **Request.max_content_length** - Maximum request body size for the current request (if configured).
- **Request.trusted_hosts** - Host validation configuration for the current request.
- **Response** - Response class for creating custom responses.
- **Config** - Configuration dictionary subclass with from_file, from_object methods.
- **flask.__version__** - ⚠️ Deprecated in 3.1.0 (removed in 3.2.0); use `importlib.metadata.version("flask")` instead.

### Signals
- **template_rendered** - Signal sent when a template is rendered.
- **before_render_template** - Signal sent before template rendering.
- **request_started** - Signal sent when request processing starts.
- **request_finished** - Signal sent when request processing finishes.
- **request_tearing_down** - Signal sent when request context is torn down.
- **got_request_exception** - Signal sent when an exception occurs during request processing.
- **appcontext_pushed** - Signal sent when application context is pushed.
- **appcontext_popped** - Signal sent when application context is popped.
- **appcontext_tearing_down** - Signal sent when application context is torn down.
- **message_flashed** - Signal sent when a message is flashed.