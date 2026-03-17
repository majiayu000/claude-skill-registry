---
name: structlog-logging-specialist
description: Configure and use Structlog for structured logging in HuleEdu services. Guides correlation context propagation, async-safe logging, and integration with error handling. Integrates with Context7 for latest Structlog documentation.
---

# Structlog Logging Specialist

Compact skill for implementing structured logging with Structlog in HuleEdu services.

## When to Use

Activate when the user:
- Needs to configure Structlog for a new or existing service
- Wants to propagate correlation IDs through logs
- Asks about async-safe context variables
- Needs to integrate logging with error handling
- Wants to understand production vs development logging
- Mentions Structlog, structured logging, correlation context, or log context
- Needs to bind context variables to logs

## Core Capabilities

- **Structlog Configuration**: Production (JSON) vs Development (colored console) setup
- **Correlation Propagation**: HTTP request → logs, Kafka events → logs, cross-service tracing
- **Context Variables**: Async-safe context binding with `bind_contextvars`
- **Logger Creation**: Service-specific logger instances
- **Event Logging**: Structured logging for Kafka event processing
- **Error Integration**: Automatic correlation context in error handlers
- **JSON Output**: Production-ready JSON logs for Loki aggregation
- **Context7 Integration**: Fetch latest Structlog documentation

## Quick Workflow

1. Configure Structlog at service startup with environment-specific settings
2. Create logger instances for modules/components
3. Bind correlation context at request/event boundaries
4. Log with structured key-value pairs
5. Clear context when done (async boundaries)
6. Verify JSON output in production logs

## Configuration Pattern

```python
from huleedu_service_libs.logging_utils import configure_service_logging

# In app.py or main startup
configure_service_logging(
    service_name="spellchecker_service",
    environment=settings.ENVIRONMENT,  # "production" or "development"
    log_level=settings.LOG_LEVEL,      # "INFO", "DEBUG", etc.
)
```

## Logger Usage Pattern

```python
from huleedu_service_libs.logging_utils import create_service_logger

# Create logger for module
logger = create_service_logger("spellchecker_service.event_processor")

# Log with context
logger.info(
    "Processing event",
    correlation_id=str(correlation_id),
    event_id=str(event_id),
    essay_id=essay_id,
)
```

## Context Binding Pattern

```python
from structlog.contextvars import bind_contextvars, clear_contextvars

# Bind context at request/event boundary
bind_contextvars(
    correlation_id=str(envelope.correlation_id),
    event_id=str(envelope.event_id),
    event_type=envelope.event_type,
)

# All logs now include bound context automatically
logger.info("Processing started")  # Includes correlation_id, event_id, event_type

# Clear when done
clear_contextvars()
```

## Reference Documentation

- **Detailed Configuration & Patterns**: See `reference.md` in this directory
- **Real-World Logging Examples**: See `examples.md` in this directory
- **Logging Library**: `/libs/huleedu_service_libs/src/huleedu_service_libs/logging_utils.py`
- **Correlation Utilities**: `/libs/huleedu_service_libs/src/huleedu_service_libs/error_handling/correlation.py`
