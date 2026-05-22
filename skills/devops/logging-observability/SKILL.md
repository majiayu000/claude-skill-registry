---
name: logging-observability
description: Structured JSON logging with correlation IDs, request context propagation across async boundaries, performance timing decorators, and worker metrics collection.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: observability
  time: 4h
  source: drift-masterguide
---

# Logging & Observability

Structured logging with correlation IDs and context propagation.

## When to Use This Skill

- Need request tracing across distributed services
- Want structured JSON logs for aggregation
- Require performance timing for operations
- Building background workers with metrics

## Core Concepts

Effective observability requires:

1. **Correlation IDs** - Track requests across services
2. **Structured logging** - JSON format for machine parsing
3. **Context propagation** - Carry metadata through async calls
4. **Performance timing** - Measure operation durations

## Implementation

### Python

```python
import contextvars
import uuid
import json
import logging
import time
import functools
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Callable, TypeVar
from contextlib import contextmanager

# Context variable for request-scoped logging
_logging_context: contextvars.ContextVar["LoggingContext"] = contextvars.ContextVar(
    "logging_context", default=None
)


@dataclass
class LoggingContext:
    """Request-scoped logging context."""
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    request_path: Optional[str] = None
    request_method: Optional[str] = None
    service_name: str = "api"
    environment: str = "development"
    extra: Dict[str, Any] = field(default_factory=dict)
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "user_id": self.user_id,
            "request_path": self.request_path,
            "request_method": self.request_method,
            "service_name": self.service_name,
            "environment": self.environment,
            **self.extra,
        }
    
    def with_extra(self, **kwargs) -> "LoggingContext":
        return LoggingContext(
            correlation_id=self.correlation_id,
            user_id=self.user_id,
            request_path=self.request_path,
            request_method=self.request_method,
            service_name=self.service_name,
            environment=self.environment,
            extra={**self.extra, **kwargs},
            start_time=self.start_time,
        )


def get_logging_context() -> Optional[LoggingContext]:
    return _logging_context.get()


def set_logging_context(context: LoggingContext) -> contextvars.Token:
    return _logging_context.set(context)


def reset_logging_context(token: contextvars.Token) -> None:
    _logging_context.reset(token)


class StructuredJsonFormatter(logging.Formatter):
    """JSON log formatter with context injection."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        context = get_logging_context()
        if context:
            log_entry.update(context.to_dict())
        
        if record.exc_info:
            import traceback
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info),
            }
        
        # Add extra fields
        skip_keys = {
            "name", "msg", "args", "created", "filename", "funcName",
            "levelname", "levelno", "lineno", "module", "msecs",
            "pathname", "process", "processName", "relativeCreated",
            "stack_info", "exc_info", "exc_text", "thread", "threadName", "message",
        }
        for key, value in record.__dict__.items():
            if key not in skip_keys:
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str)


def configure_logging(
    level: str = "INFO",
    service_name: str = "api",
    environment: str = "development",
) -> None:
    """Configure structured logging."""
    formatter = StructuredJsonFormatter()
    
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    set_logging_context(LoggingContext(
        service_name=service_name,
        environment=environment,
    ))


class ContextLogger:
    """Logger wrapper that includes context automatically."""
    
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
    
    def _log(self, level: int, message: str, exc_info: bool = False, **kwargs: Any) -> None:
        context = get_logging_context()
        extra = {}
        if context:
            extra.update(context.to_dict())
        extra.update(kwargs)
        self._logger.log(level, message, exc_info=exc_info, extra=extra)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, exc_info: bool = False, **kwargs: Any) -> None:
        self._log(logging.ERROR, message, exc_info=exc_info, **kwargs)
    
    def exception(self, message: str, **kwargs: Any) -> None:
        self._log(logging.ERROR, message, exc_info=True, **kwargs)


def get_logger(name: str) -> ContextLogger:
    return ContextLogger(name)


# Performance timing decorator
F = TypeVar("F", bound=Callable[..., Any])

def timed(
    operation_name: str = None,
    log_args: bool = False,
    threshold_ms: float = None,
) -> Callable[[F], F]:
    """Decorator to log function execution time."""
    def decorator(func: F) -> F:
        name = operation_name or func.__name__
        logger = get_logger(func.__module__)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000
                
                if threshold_ms is None or duration_ms >= threshold_ms:
                    log_kwargs = {"operation": name, "duration_ms": round(duration_ms, 2)}
                    if log_args:
                        log_kwargs["args"] = str(args)[:200]
                    logger.info(f"{name} completed", **log_kwargs)
                
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000
                logger.error(f"{name} failed", operation=name, duration_ms=round(duration_ms, 2), exc_info=True)
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000
                
                if threshold_ms is None or duration_ms >= threshold_ms:
                    logger.info(f"{name} completed", operation=name, duration_ms=round(duration_ms, 2))
                
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000
                logger.error(f"{name} failed", operation=name, duration_ms=round(duration_ms, 2), exc_info=True)
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


@contextmanager
def worker_job_context(worker_name: str, job_id: str, user_id: str = None):
    """Context manager for worker job execution."""
    context = LoggingContext(
        correlation_id=job_id,
        user_id=user_id,
        service_name=worker_name,
        extra={"job_id": job_id},
    )
    token = set_logging_context(context)
    logger = get_logger(worker_name)
    
    start_time = time.perf_counter()
    
    try:
        logger.info("Job started", job_id=job_id)
        yield
        
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info("Job completed", job_id=job_id, duration_ms=round(duration_ms, 2))
    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.exception("Job failed", job_id=job_id, duration_ms=round(duration_ms, 2))
        raise
    finally:
        reset_logging_context(token)
```

### TypeScript

```typescript
import { AsyncLocalStorage } from 'async_hooks';
import { randomUUID } from 'crypto';

interface LoggingContext {
  correlationId: string;
  userId?: string;
  requestPath?: string;
  requestMethod?: string;
  serviceName: string;
  environment: string;
  extra: Record<string, unknown>;
  startTime: Date;
}

const asyncLocalStorage = new AsyncLocalStorage<LoggingContext>();

function createContext(overrides: Partial<LoggingContext> = {}): LoggingContext {
  return {
    correlationId: randomUUID(),
    serviceName: 'api',
    environment: process.env.NODE_ENV || 'development',
    extra: {},
    startTime: new Date(),
    ...overrides,
  };
}

function getContext(): LoggingContext | undefined {
  return asyncLocalStorage.getStore();
}

function runWithContext<T>(context: LoggingContext, fn: () => T): T {
  return asyncLocalStorage.run(context, fn);
}

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  correlationId?: string;
  userId?: string;
  serviceName?: string;
  [key: string]: unknown;
}

class ContextLogger {
  constructor(private name: string) {}

  private log(level: string, message: string, extra: Record<string, unknown> = {}): void {
    const context = getContext();
    
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      logger: this.name,
      message,
      ...extra,
    };

    if (context) {
      entry.correlationId = context.correlationId;
      entry.userId = context.userId;
      entry.serviceName = context.serviceName;
      entry.requestPath = context.requestPath;
      Object.assign(entry, context.extra);
    }

    console.log(JSON.stringify(entry));
  }

  debug(message: string, extra?: Record<string, unknown>): void {
    this.log('DEBUG', message, extra);
  }

  info(message: string, extra?: Record<string, unknown>): void {
    this.log('INFO', message, extra);
  }

  warn(message: string, extra?: Record<string, unknown>): void {
    this.log('WARN', message, extra);
  }

  error(message: string, error?: Error, extra?: Record<string, unknown>): void {
    const errorInfo = error ? {
      errorType: error.name,
      errorMessage: error.message,
      stack: error.stack,
    } : {};
    this.log('ERROR', message, { ...errorInfo, ...extra });
  }
}

function getLogger(name: string): ContextLogger {
  return new ContextLogger(name);
}

// Performance timing decorator
function timed(operationName?: string, options: { threshold?: number } = {}) {
  return function <T extends (...args: any[]) => any>(
    target: any,
    propertyKey: string,
    descriptor: TypedPropertyDescriptor<T>
  ): TypedPropertyDescriptor<T> {
    const originalMethod = descriptor.value!;
    const name = operationName || propertyKey;
    const logger = getLogger(target.constructor.name);

    descriptor.value = async function (...args: any[]) {
      const start = performance.now();
      try {
        const result = await originalMethod.apply(this, args);
        const durationMs = performance.now() - start;
        
        if (!options.threshold || durationMs >= options.threshold) {
          logger.info(`${name} completed`, { operation: name, durationMs: Math.round(durationMs * 100) / 100 });
        }
        
        return result;
      } catch (error) {
        const durationMs = performance.now() - start;
        logger.error(`${name} failed`, error as Error, { operation: name, durationMs: Math.round(durationMs * 100) / 100 });
        throw error;
      }
    } as T;

    return descriptor;
  };
}

// Express middleware
function loggingMiddleware(serviceName: string) {
  return (req: any, res: any, next: any) => {
    const correlationId = req.headers['x-correlation-id'] || randomUUID();
    
    const context = createContext({
      correlationId,
      userId: req.user?.id,
      requestPath: req.path,
      requestMethod: req.method,
      serviceName,
    });

    runWithContext(context, () => {
      const logger = getLogger('http');
      const start = performance.now();

      logger.info('Request started', {
        queryParams: req.query,
        clientIp: req.ip,
      });

      res.on('finish', () => {
        const durationMs = performance.now() - start;
        logger.info('Request completed', {
          statusCode: res.statusCode,
          durationMs: Math.round(durationMs * 100) / 100,
        });
      });

      res.setHeader('X-Correlation-ID', correlationId);
      next();
    });
  };
}

export {
  LoggingContext,
  createContext,
  getContext,
  runWithContext,
  getLogger,
  timed,
  loggingMiddleware,
};
```

## Usage Examples

### API Routes with Context

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        
        context = LoggingContext(
            correlation_id=correlation_id,
            request_path=request.url.path,
            request_method=request.method,
        )
        token = set_logging_context(context)
        
        try:
            logger.info("Request started")
            start = time.perf_counter()
            
            response = await call_next(request)
            
            duration_ms = (time.perf_counter() - start) * 1000
            logger.info("Request completed", status_code=response.status_code, duration_ms=round(duration_ms, 2))
            
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        finally:
            reset_logging_context(token)

app.add_middleware(LoggingMiddleware)

@app.post("/generate")
@timed("generate_asset")
async def generate_asset(request: GenerateRequest):
    logger.info("Starting generation", asset_type=request.asset_type)
    # All logs include correlation_id automatically
    return {"job_id": job.id}
```

### Background Workers

```python
def process_job(job_id: str, user_id: str):
    with worker_job_context("generation_worker", job_id, user_id):
        logger.info("Processing generation job")
        # All logs include job_id and user_id
        result = generate_image(...)
        logger.info("Image generated", size_bytes=len(result))
```

### Timed Operations

```python
@timed("database_query", threshold_ms=100)
async def fetch_user(user_id: str):
    # Only logs if query takes > 100ms
    return await db.users.find_one({"id": user_id})
```

## Best Practices

1. Always use correlation IDs for distributed tracing
2. Use JSON format for log aggregation tools
3. Propagate context through async boundaries with contextvars
4. Set thresholds to only log slow operations
5. Never log passwords, tokens, or PII
6. Use DEBUG for development, INFO for production

## Common Mistakes

- Missing correlation IDs (can't trace requests)
- Unstructured log messages (hard to parse)
- Logging sensitive data (security risk)
- No context propagation (lose trace in async code)
- Logging everything (noise and cost)

## Related Patterns

- anomaly-detection - Uses logs to detect issues
- health-checks - Logs health status
- error-sanitization - Safe error logging
