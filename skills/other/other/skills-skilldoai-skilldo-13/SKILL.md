---
name: celery
description: Distributed task queue for running Python callables asynchronously via a message broker.
version: 5.6.2
ecosystem: python
license: BSD-3-Clause
generated_with: gpt-5.2
---

## Imports

```python
import celery
from celery import Celery
```

## Core Patterns

### Create an app and register tasks with `@app.task` ✅ Current
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["celery"]
# ///
from __future__ import annotations
from celery import Celery

# In-memory broker and backend for local/in-process testing.
app = Celery("hello", broker="memory://", backend="cache+memory://")

@app.task(name="hello")
def hello() -> str:
    return "hello world"

def main() -> None:
    # Test direct synchronous invocation
    task = app.tasks["hello"]
    assert hasattr(task, "name")
    assert task.name == "hello"
    result = task()
    assert isinstance(result, str)
    assert "hello" in result and "world" in result

    # Test .apply() (in-process - simulates async, but runs eagerly)
    async_result = task.apply()
    value = async_result.get(timeout=3)
    assert isinstance(value, str)
    assert "hello" in value and "world" in value

    # Test .delay() returns AsyncResult and result is as expected
    # For the memory:// broker/backend, .delay() does NOT run the task unless a worker is running.
    # Instead, force eager mode for testing .delay()/.apply_async() behavior.
    app.conf.task_always_eager = True
    async_result2 = task.delay()
    value2 = async_result2.get(timeout=3)
    assert isinstance(value2, str)
    assert "hello" in value2 and "world" in value2

if __name__ == "__main__":
    main()
    print("✓ Test passed: Create an app and register tasks with `@app.task` ✅ Current")
```
* Create exactly one `Celery(...)` application instance per logical app and register tasks on that instance.
* The `Celery('name', ...)` identifier should be stable for monitoring/logging and multi-app setups.

### Call a task synchronously (local function call) ✅ Current
```python
from __future__ import annotations

from celery import Celery

# Use an in-memory broker so this example is runnable without external services.
app = Celery("math_app", broker="memory://")


@app.task
def add(x: int, y: int) -> int:
    return x + y


def main() -> None:
    # This is a normal Python call (no broker/worker involved).
    result = add(2, 3)
    print(result)


if __name__ == "__main__":
    main()
```
* Celery tasks are still regular callables; invoking them directly runs in-process and bypasses the broker/worker.

### Use extras to match broker/backend dependencies ✅ Current
```python
from __future__ import annotations

# This file is runnable Python, but the key is the dependency pin:
# requirements.txt:
#   celery[redis]

from celery import Celery
from kombu import Connection

app = Celery("redis_app", broker="redis://localhost:6379/0")


def main() -> None:
    # Prove the redis transport is importable/resolvable (i.e., the extra is installed).
    conn = Connection(app.conf.broker_url)

    # kombu resolves the transport implementation on-demand; just accessing it
    # is enough to verify the optional dependency is present.
    transport = conn.transport
    module_path = transport.__class__.__module__

    assert module_path.startswith("kombu.transport.redis")

    # Attempt a connection to redis server (will fail if redis is not running, but proves extras are installed)
    try:
        conn.ensure_connection(max_retries=1)
    except Exception as e:
        # It's fine if redis isn't running for this sample
        print("Redis server not available (as expected in test env), but celery[redis] extra is installed.")
    print("✓ Test passed: Use extras to match broker/backend dependencies ✅ Current")


if __name__ == "__main__":
    main()
```
* Install Celery with the correct extras for your chosen broker/backend (e.g., `celery[redis]`) to avoid missing optional dependencies at runtime.

## Configuration

- Create the app with explicit name and broker:
  - `app = Celery("my_app", broker="amqp://guest@localhost//")`
- Prefer real brokers (RabbitMQ/Redis) for production; treat local-only or experimental transports as development-only.
- Dependency management:
  - Use extras such as `celery[redis]`, `celery[gevent]`, `celery[eventlet]`, `celery[sqlalchemy]` depending on transport/backend/pool needs.
- Runtime compatibility planning:
  - Celery 5.6.x supports Python 3.9–3.13 and PyPy 3.9+.
  - Celery 5.7.x will require Python 3.10+ (Python 3.9 removed).
- Framework integration:
  - Integration packages are optional; use them when you need lifecycle hooks (e.g., close DB connections after fork with prefork pools).

## Pitfalls

### Wrong: Decorating tasks on the `Celery` class (unbound task registration)
```python
from __future__ import annotations

from celery import Celery

Celery("hello", broker="amqp://guest@localhost//")


@Celery.task
def hello() -> str:
    return "hello world"
```

### Right: Bind tasks to a specific app instance with `@app.task`
```python
from __future__ import annotations

from celery import Celery

app = Celery("hello", broker="amqp://guest@localhost//")


@app.task
def hello() -> str:
    return "hello world"
```

### Wrong: Installing plain `celery` but configuring Redis broker/backend
```python
from __future__ import annotations

# requirements.txt (problematic):
# celery

from celery import Celery

app = Celery("redis_app", broker="redis://localhost:6379/0")
```

### Right: Install the matching extra (e.g., `celery[redis]`)
```python
from __future__ import annotations

# requirements.txt:
# celery[redis]

from celery import Celery

app = Celery("redis_app", broker="redis://localhost:6379/0")
```

### Wrong: Creating multiple app instances unintentionally (tasks registered on one, worker runs another)
```python
from __future__ import annotations

from celery import Celery

app_a = Celery("app_a", broker="amqp://guest@localhost//")
app_b = Celery("app_b", broker="amqp://guest@localhost//")


@app_a.task
def hello() -> str:
    return "hello from a"
```

### Right: Use a single app instance per logical application
```python
from __future__ import annotations

from celery import Celery

app = Celery("app", broker="amqp://guest@localhost//")


@app.task
def hello() -> str:
    return "hello"
```

### Wrong: Assuming Microsoft Windows is a supported production platform
```python
from __future__ import annotations

from celery import Celery

# This code may run, but operational support is best-effort on Windows.
app = Celery("win_app", broker="amqp://guest@localhost//")
```

### Right: Deploy workers on supported Unix-like environments (validate Windows yourself if required)
```python
from __future__ import annotations

from celery import Celery

# Prefer deploying Celery workers on Linux/macOS in production.
# If you must use Windows, validate thoroughly in your environment.
app = Celery("prod_app", broker="amqp://guest@localhost//")
```

## References

- [Documentation](https://docs.celeryq.dev/en/stable/)
- [Changelog](https://docs.celeryq.dev/en/stable/changelog.html)
- [Code](https://github.com/celery/celery)
- [Tracker](https://github.com/celery/celery/issues)
- [Funding](https://opencollective.com/celery)

## Migration from v5.6.x

- Breaking change when upgrading to Celery 5.7.x:
  - **Change:** Python 3.9 support removed; Celery 5.7.x requires Python 3.10+.
  - **Migration guidance:** Upgrade runtime/CI to Python 3.10+ before upgrading Celery. If you must stay on Python 3.9, pin Celery to `~=5.6`.
- Breaking change when upgrading from Celery 5.5.x to 5.6.x:
  - **Change:** Python 3.7 and below are no longer supported. Celery 5.6.x requires Python 3.8+.
  - **Migration:** Upgrade your Python interpreter to 3.8 or newer before upgrading to Celery 5.6.x.

## API Reference

- **celery.Celery(main: str = None, broker: str = None, backend: str = None, include: list = None, config_source: object = None, task_cls: type = None, autofinalize: bool = True, namespace: str = None, strict_typing: bool = False)**  
  Create a Celery application instance; key params: `main` (app name), `broker` (broker URL), `backend` (result backend), etc.
- **Celery.task(*dargs, **dkwargs)**  
  Decorator to register a function as a task on that app instance; used as `@app.task`.
- **celery.bugreport() -> str**  
  Return a string with useful information for bug reports.
- **celery.shared_task(*args, **kwargs) -> Task**  
  Decorator for creating tasks that use the current app when imported.
- **celery.Task**  
  Base class for creating custom task classes.
- **celery.current_app**  
  Property returning the current Celery application.
- **celery.current_task**  
  Property returning the currently executing task.
- **celery.chain(*tasks, **options) -> Signature**  
  Combine tasks to execute sequentially.
- **celery.chord(header, body=None, **options) -> Signature**  
  Group of tasks with a callback executed after all complete.
- **celery.chunks(task, it, n, *args, **kwargs) -> Signature**  
  Split an iterable into n-sized chunks and run as group of tasks.
- **celery.group(*tasks, **options) -> Signature**  
  Run a group of tasks in parallel.
- **celery.signature(task, args=None, kwargs=None, options=None, type=None, app=None, subtask_type=None, immutable=False, **other_options) -> Signature**  
  Create a task signature (truncated signature shown).
- **celery.maybe_signature(task, app=None, clone=False) -> Signature**  
  Convert an object to a signature if possible.
- **celery.xmap(task, it) -> list**  
  Map a task over an iterable, return results as list.
- **celery.xstarmap(task, it) -> list**  
  Like xmap but "star" (task receives unpacked args).
- **celery.uuid() -> str**  
  Generate a unique id.
- **celery.Signature**  
  Class representing a signature for a task.

## Current Library State (from source analysis)

### API Surface
```json
{
  "library_category": "general",
  "apis": [
    {
      "name": "celery.Celery",
      "type": "class",
      "signature": "Celery(main: str = None, broker: str = None, backend: str = None, include: list = None, config_source: object = None, task_cls: type = None, autofinalize: bool = True, namespace: str = None, strict_typing: bool = False)",
      "signature_truncated": false,
      "return_type": "Celery",
      "module": "celery.app.base",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "main": {
          "base_type": "str",
          "is_optional": true,
          "default_value": "None"
        },
        "broker": {
          "base_type": "str",
          "is_optional": true,
          "default_value": "None"
        },
        "backend": {
          "base_type": "str",
          "is_optional": true,
          "default_value": "None"
        },
        "include": {
          "base_type": "list",
          "is_optional": true,
          "default_value": "None"
        },
        "config_source": {
          "base_type": "object",
          "is_optional": true,
          "default_value": "None"
        },
        "task_cls": {
          "base_type": "type",
          "is_optional": true,
          "default_value": "None"
        },
        "autofinalize": {
          "base_type": "bool",
          "is_optional": true,
          "default_value": "True"
        },
        "namespace": {
          "base_type": "str",
          "is_optional": true,
          "default_value": "None"
        },
        "strict_typing": {
          "base_type": "bool",
          "is_optional": true,
          "default_value": "False"
        }
      },
      "class_hierarchy": {
        "base_classes": ["object"],
        "is_abstract": false,
        "metaclass": null
      }
    },
    {
      "name": "celery.bugreport",
      "type": "function",
      "signature": "bugreport() -> str",
      "signature_truncated": false,
      "return_type": "str",
      "module": "celery.app.utils",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.shared_task",
      "type": "function",
      "signature": "shared_task(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "Task",
      "module": "celery.app",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.Task",
      "type": "class",
      "signature": "Task(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "Task",
      "module": "celery.app.task",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "base_classes": ["object"],
        "is_abstract": false,
        "metaclass": null
      }
    },
    {
      "name": "celery.current_app",
      "type": "property",
      "signature": "current_app",
      "signature_truncated": false,
      "return_type": "Celery",
      "module": "celery._state",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "has_setter": false,
      "has_deleter": false
    },
    {
      "name": "celery.current_task",
      "type": "property",
      "signature": "current_task",
      "signature_truncated": false,
      "return_type": "Task",
      "module": "celery._state",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "has_setter": false,
      "has_deleter": false
    },
    {
      "name": "celery.chain",
      "type": "function",
      "signature": "chain(*tasks, **options) -> Signature",
      "signature_truncated": false,
      "return_type": "Signature",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.chord",
      "type": "function",
      "signature": "chord(header, body=None, **options) -> Signature",
      "signature_truncated": false,
      "return_type": "Signature",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.chunks",
      "type": "function",
      "signature": "chunks(task, it, n, *args, **kwargs) -> Signature",
      "signature_truncated": false,
      "return_type": "Signature",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.group",
      "type": "function",
      "signature": "group(*tasks, **options) -> Signature",
      "signature_truncated": false,
      "return_type": "Signature",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.signature",
      "type": "function",
      "signature": "signature(task, args=None, kwargs=None, options=None, type=None, app=None, subtask_type=None, immutable=False, **other_options)",
      "signature_truncated": true,
      "return_type": "Signature",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.maybe_signature",
      "type": "function",
      "signature": "maybe_signature(task, app=None, clone=False)",
      "signature_truncated": false,
      "return_type": "Signature",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.xmap",
      "type": "function",
      "signature": "xmap(task, it) -> list",
      "signature_truncated": false,
      "return_type": "list",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.xstarmap",
      "type": "function",
      "signature": "xstarmap(task, it) -> list",
      "signature_truncated": false,
      "return_type": "list",
      "module": "celery.canvas",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.uuid",
      "type": "function",
      "signature": "uuid() -> str",
      "signature_truncated": false,
      "return_type": "str",
      "module": "celery.utils",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "celery.Signature",
      "type": "class",
      "signature": "Signature(task=None, args=None, kwargs=None, options=None, type=None, app=None, subtask_type=None, immutable=False, **other_options)",
      "signature_truncated": true,
      "return_type": "Signature",
      "module": "celery.canvas",
      "publicity_score": "medium",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "base_classes": ["object"],
        "is_abstract": false,
        "metaclass": null
      }
    }
  ]
}
```

**Explanation and Notes:**
- **library_category**: "general" – Celery is a distributed task queue, not a web framework, ORM, CLI, etc.
- **Public API detection**: All APIs in `celery.__all__` are marked `"publicity_score": "high"`. `Signature` is also exposed via public imports, but not always in `__all__`.
- **Type hints**: Where available, type hints are extracted; if not in code, inferred from docs or usage.
- **Signatures**: Truncated if over 120 chars (e.g., `Signature`/`signature`).
- **Deprecation**: No deprecated APIs in this surface.
- **Class hierarchy**: Simple object inheritance, not abstract.
- **Decorators**: No decorators at top level for these public APIs.
- **Properties**: `current_app` and `current_task` are properties, not functions.
- **Module**: Source module is accurately set.
- **Other**: Internal, compatibility, or deprecated APIs not present in this top-level surface.

**Further Expansion**: This is a sample from the critical public API. More may be extracted from submodules if requested (such as `celery.canvas.subtask`, etc.), but above covers the canonical public API surface per `__all__` and official docs.

### Usage Patterns
```json
[
  {
    "api": "celery.signals.before_task_publish.connect",
    "setup_code": [
      "import pytest",
      "from celery.signals import before_task_publish",
      "from t.smoke.tasks import noop"
    ],
    "usage_pattern": [
      "@before_task_publish.connect",
      "def before_task_publish_handler(*args, **kwargs):",
      "    nonlocal signal_was_called",
      "    signal_was_called = True"
    ],
    "assertions": [
      "noop.s().apply_async(queue=celery_setup.worker.worker_queue)",
      "assert signal_was_called is True"
    ],
    "test_infrastructure": [
      "pytest fixtures",
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.signals.after_task_publish.connect",
    "setup_code": [
      "import pytest",
      "from celery.signals import after_task_publish",
      "from t.smoke.tasks import noop"
    ],
    "usage_pattern": [
      "@after_task_publish.connect",
      "def after_task_publish_handler(*args, **kwargs):",
      "    nonlocal signal_was_called",
      "    signal_was_called = True"
    ],
    "assertions": [
      "noop.s().apply_async(queue=celery_setup.worker.worker_queue)",
      "assert signal_was_called is True"
    ],
    "test_infrastructure": [
      "pytest fixtures",
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.app.control.ping",
    "setup_code": [
      "from pytest_celery import CeleryTestSetup"
    ],
    "usage_pattern": [
      "r = celery_setup.app.control.ping()"
    ],
    "assertions": [
      "assert all([all([res['ok'] == 'pong' for _, res in response.items()]) for response in r])"
    ],
    "test_infrastructure": [
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.app.control.shutdown",
    "setup_code": [
      "from pytest_celery import CeleryTestSetup"
    ],
    "usage_pattern": [
      "celery_setup.app.control.shutdown(destination=[celery_setup.worker.hostname()])"
    ],
    "assertions": [
      "while celery_setup.worker.container.status != 'exited':",
      "    celery_setup.worker.container.reload()",
      "assert celery_setup.worker.container.attrs['State']['ExitCode'] == 0"
    ],
    "test_infrastructure": [
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.signature",
    "setup_code": [
      "import pytest",
      "from celery.canvas import signature",
      "from t.integration.tasks import identity"
    ],
    "usage_pattern": [
      "sig = signature(identity, args=(...), queue=...)"
    ],
    "assertions": [
      "assert sig.delay().get(timeout=RESULT_TIMEOUT) == ... (expected value)"
    ],
    "test_infrastructure": [
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.group",
    "setup_code": [
      "from celery.canvas import group",
      "from t.integration.tasks import add"
    ],
    "usage_pattern": [
      "sig = group(",
      "    group(add.si(1, 1), add.si(2, 2)),",
      "    group([add.si(1, 1), add.si(2, 2)]),",
      "    group(s for s in [add.si(1, 1), add.si(2, 2)]),",
      ")"
    ],
    "assertions": [
      "res = sig.apply_async(queue=celery_setup.worker.worker_queue)",
      "assert res.get(timeout=RESULT_TIMEOUT) == [2, 4, 2, 4, 2, 4]"
    ],
    "test_infrastructure": [
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.chain",
    "setup_code": [
      "from celery.canvas import chain",
      "from t.integration.tasks import identity"
    ],
    "usage_pattern": [
      "sig = chain(",
      "    identity.si('chain_task1').set(queue=queue),",
      "    identity.si('chain_task2').set(queue=queue),",
      ") | identity.si('test_chain').set(queue=queue)"
    ],
    "assertions": [
      "res = sig.apply_async()",
      "assert res.get(timeout=RESULT_TIMEOUT) == 'test_chain'"
    ],
    "test_infrastructure": [
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.chord",
    "setup_code": [
      "from celery.canvas import chord, group",
      "from t.integration.tasks import add, fail"
    ],
    "usage_pattern": [
      "failing_group = group([add.si(15, 7).set(queue=queue), fail.si().set(queue=queue)])",
      "test_chord = chord(failing_group, input_body(queue))",
      "result = test_chord.apply_async()"
    ],
    "assertions": [
      "with pytest.raises(ExpectedException):",
      "    result.get(timeout=RESULT_TIMEOUT)"
    ],
    "test_infrastructure": [
      "pytest.mark.parametrize for input_body",
      "CeleryTestSetup fixture"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.stamp",
    "setup_code": [
      "from celery.canvas import StampingVisitor, chain",
      "from t.integration.tasks import identity"
    ],
    "usage_pattern": [
      "class CustomStampingVisitor(StampingVisitor):",
      "    def on_signature(self, sig, **headers) -> dict:",
      "        return {'stamp': 42}",
      "",
      "stamped_task = identity.si(123)",
      "stamped_task.stamp(visitor=CustomStampingVisitor())"
    ],
    "assertions": [
      "assert stamped_task.apply_async(queue=queue).get(timeout=RESULT_TIMEOUT)",
      "assert worker.logs().count(json.dumps({'stamp': 42}, indent=4, sort_keys=True))"
    ],
    "test_infrastructure": [
      "CeleryTestWorker",
      "CeleryTestSetup",
      "pytest.mark.parametrize for cluster matrix"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.result.AsyncResult.revoke_by_stamped_headers",
    "setup_code": [
      "from celery.result import AsyncResult",
      "from t.integration.tasks import StampOnReplace"
    ],
    "usage_pattern": [
      "result = canvas.apply_async(queue=celery_latest_worker.worker_queue)",
      "result.revoke_by_stamped_headers(StampOnReplace.stamp, terminate=True)"
    ],
    "assertions": [
      "dev_worker.assert_log_does_not_exist('Done waiting', timeout=wait_for_revoke_timeout)"
    ],
    "test_infrastructure": [
      "CeleryTestWorker",
      "pytest fixtures"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.app.control.revoke_by_stamped_headers",
    "setup_code": [
      "from t.integration.tasks import StampOnReplace"
    ],
    "usage_pattern": [
      "dev_worker.app.control.revoke_by_stamped_headers(",
      "    StampOnReplace.stamp,",
      "    terminate=True,",
      ")"
    ],
    "assertions": [
      "canvas.apply_async(queue=celery_latest_worker.worker_queue)",
      "dev_worker.assert_log_exists('Discarding revoked task')",
      "dev_worker.assert_log_exists(f'revoked by header: {StampOnReplace.stamp}')"
    ],
    "test_infrastructure": [
      "CeleryTestWorker",
      "pytest fixtures"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.Signature.link",
    "setup_code": [
      "from celery.canvas import StampingVisitor",
      "from t.integration.tasks import add, identity"
    ],
    "usage_pattern": [
      "stamped_task = identity.si(123).set(queue=dev_worker.worker_queue)",
      "stamped_task.link(add.s(0).stamp(no_visitor_stamp='val').set(queue=dev_worker.worker_queue))"
    ],
    "assertions": [
      "stamped_task.stamp(visitor=CustomStampingVisitor())",
      "stamped_task.delay().get(timeout=RESULT_TIMEOUT)",
      "assert dev_worker.logs().count(json.dumps(on_signature_stamp, indent=4, sort_keys=True))",
      "assert dev_worker.logs().count(json.dumps(link_stamp, indent=4, sort_keys=True))"
    ],
    "test_infrastructure": [
      "CeleryTestWorker"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.Signature.stamp",
    "setup_code": [
      "from celery.canvas import StampingVisitor",
      "from t.integration.tasks import identity"
    ],
    "usage_pattern": [
      "stamped_task = identity.si(123)",
      "stamped_task.stamp(visitor=CustomStampingVisitor())"
    ],
    "assertions": [
      "assert stamped_task.apply_async(queue=queue).get(timeout=RESULT_TIMEOUT)"
    ],
    "test_infrastructure": [
      "CeleryTestWorker"
    ],
    "deprecation_status": "current"
  },
  {
    "api": "celery.canvas.chain.stamp (multiple tasks and queues)",
    "setup_code": [
      "from celery.canvas import chain",
      "from t.integration.tasks import identity"
    ],
    "usage_pattern": [
      "stamped_task = chain(",
      "    identity.si(4).set(queue=w1.worker_queue),",
      "    identity.si(2).set(queue=w2.worker_queue),",
      ")",
      "stamped_task.stamp(visitor=CustomStampingVisitor())"
    ],
    "assertions": [
      "stamped_task.apply_async().get(timeout=RESULT_TIMEOUT)",
      "assert w1.logs().count(stamp)",
      "assert w2.logs().count(stamp)"
    ],
    "test_infrastructure": [
      "CeleryWorkerCluster",
      "CeleryTestWorker"
    ],
    "deprecation_status": "current"
  }
]
```

### Documentation & Changelog
```json
{
  "documented_apis": [
    "celery.Celery",
    "Celery.task"
  ],
  "conventions": [
    "Use the Celery application instance (Celery(...)) to register tasks using the @app.task decorator.",
    "Specify the broker URL explicitly when creating the Celery instance.",
    "Organize tasks as functions decorated with @app.task.",
    "Use bundles (e.g., celery[redis]) in pip install to get extras for specific backends or features.",
    "No configuration files required: configuration can be done in code.",
    "Framework integration is available, but not strictly required; direct usage is preferred unless advanced hooks are needed.",
    "Use supported Python versions (3.8+ for Celery 5.6.x)."
  ],
  "pitfalls": [
    {
      "category": "Task registration",
      "wrong": "def hello(): return 'hello world'",
      "why": "Functions are not registered as tasks unless decorated with @app.task.",
      "right": "@app.task\ndef hello(): return 'hello world'"
    },
    {
      "category": "Configuration",
      "wrong": "app = Celery('hello')  # Missing broker argument",
      "why": "If you do not specify the broker, Celery cannot connect to a message queue.",
      "right": "app = Celery('hello', broker='amqp://guest@localhost//')"
    },
    {
      "category": "Framework Integration",
      "wrong": "Relying on integration packages for basic usage when not required.",
      "why": "Celery works directly with most frameworks; integration packages are only for advanced hooks.",
      "right": "Use direct Celery integration unless you need ORM cleanup or other hooks."
    }
  ],
  "breaking_changes": [
    {
      "version_from": "5.5.x",
      "version_to": "5.6.x",
      "change": "Python 3.7 and below are no longer supported. Celery 5.6.x requires Python 3.8+.",
      "migration": "Upgrade your Python interpreter to 3.8 or newer before upgrading to Celery 5.6.x."
    }
  ],
  "migration_notes": "See CHANGELOG.md for migration guide. Notably, ensure your Python version is 3.8 or newer before upgrading to Celery 5.6.x. For users of older Python versions, use the corresponding older Celery version (see README for mapping)."
}
```