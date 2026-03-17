---
name: "structlog"
description: "Structured logging for Python applications with context support and powerful processors"
when_to_use: "When you need structured logging with context, JSON output, or enhanced logging capabilities for Python applications"
---

# Structlog Skill

## Quick Start

```python
import structlog

# Basic usage
log = structlog.get_logger()
log.info("hello, %s!", "world", key="value", more_than_strings=[1, 2, 3])
```

## Common Patterns

### Basic Configuration

```python
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False
)
```

### JSON Logging

```python
import structlog

# Configure for JSON output
structlog.configure(
    processors=[structlog.processors.JSONRenderer()]
)

log = structlog.get_logger()
log.info("Processing request", request_id="req-123", user_id=456)
# Output: {"event": "Processing request", "request_id": "req-123", "user_id": 456}
```

### Standard Library Integration

```python
import logging
import structlog

# Configure standard logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO
)

# Configure structlog to use standard library
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.render_to_log_kwargs,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

### Context Binding

```python
import structlog

log = structlog.get_logger()

# Bind context that persists across log calls
request_log = log.bind(request_id="req-789", user="alice")
request_log.info("Processing started")
request_log.info("Database query executed", query="SELECT * FROM users")
request_log.info("Processing completed")

# Output includes request_id and user in all log entries
```

### Custom Processors

```python
import time

def add_custom_context(logger, log_method, event_dict):
    """Add custom context to every log entry"""
    event_dict["custom_field"] = "custom_value"
    event_dict["timestamp"] = time.time()
    return event_dict

structlog.configure(
    processors=[
        add_custom_context,
        structlog.processors.JSONRenderer()
    ]
)
```

### Exception Handling

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
)

log = structlog.get_logger()

try:
    1 / 0
except ZeroDivisionError:
    log.exception("Division error occurred")
```

### Testing with Structlog

```python
import pytest
import structlog
from structlog.testing import LogCapture

@pytest.fixture
def log_output():
    return LogCapture()

@pytest.fixture(autouse=True)
def configure_structlog(log_output):
    structlog.configure(
        processors=[log_output]
    )

def test_logging(log_output):
    log = structlog.get_logger()
    log.info("test message", key="value")

    assert len(log_output.entries) == 1
    assert log_output.entries[0]["event"] == "test message"
    assert log_output.entries[0]["key"] == "value"
```

### Performance-Optimized Configuration

```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

### Advanced Console Output

```python
import logging.config
import structlog

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
pre_chain = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.ExtraAdder(),
    timestamper,
]

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processors": [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=False),
            ],
            "foreign_pre_chain": pre_chain,
        },
        "colored": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processors": [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            "foreign_pre_chain": pre_chain,
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "app.log",
            "formatter": "plain",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
        }
    }
})
```

## Key Features

- **Structured Logging**: Log events as dictionaries with context
- **Multiple Output Formats**: Console, JSON, logfmt, and custom renderers
- **Context Binding**: Persistent context across log calls
- **Standard Library Integration**: Works seamlessly with Python's logging module
- **Performance**: Optimized for high-throughput applications
- **Testing Support**: Built-in testing utilities
- **Exception Handling**: Enhanced exception formatting and rendering
- **Custom Processors**: Flexible pipeline for log processing

## Best Practices

1. **Configure Once**: Set up structlog configuration at application startup
2. **Use Context**: Bind relevant context (request_id, user_id) early in request handling
3. **Choose Right Renderer**: Use ConsoleRenderer for development, JSONRenderer for production
4. **Test Logging**: Use LogCapture for unit testing logging behavior
5. **Performance**: Cache loggers and use efficient processors for production
