---
name: structured-logging-lite
description: Logging system design guide covering centralized architecture, field standards, and distributed tracing. Use when designing log systems, establishing standards, or debugging production issues.
---
# Structured Logging System Design

## Core Principles

- **Logs are data** — Every log is a queryable, structured data point
- **Single source of truth** — One logging configuration, used everywhere
- **Context is king** — Every log must be traceable to its source
- **Human + Machine readable** — Structured for parsing, clear for debugging
- **No secrets** — Never log passwords, tokens, or PII without masking

---

## System Architecture

### The Golden Rule

> **Configure once, use everywhere. Never instantiate loggers directly in business code.**

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Service A│  │ Service B│  │ Service C│  │ Handler D│        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       └─────────────┴──────┬──────┴─────────────┘               │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              LOGGING INFRASTRUCTURE                      │   │
│  │    Logger Factory | Context Provider | Formatters        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ▼                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Console  │  │   File   │  │ Log Agg. │  │  Alerts  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
src/
├── lib/logging/              # Centralized logging infrastructure
│   ├── index.ts              # Public API exports
│   ├── logger.ts             # Core logger implementation
│   ├── context.ts            # Request context management
│   ├── config.ts             # Configuration
│   └── types.ts              # Type definitions
├── modules/
│   ├── users/user.service.ts # import { logger } from '@/lib/logging'
│   └── orders/order.service.ts
└── main.ts                   # Initialize logging once at startup
```

### Anti-Patterns vs Correct Patterns

```typescript
// ❌ BAD: Creating loggers everywhere
class UserService {
  private logger = new Logger({ service: 'user' });  // Duplicated config
}

// ❌ BAD: Direct console in production
console.log('User created:', userId);  // No structure, no context

// ✅ GOOD: Import from central location
import { logger, getContextLogger } from '@/lib/logging';

class UserService {
  async createUser(data: CreateUserInput) {
    const log = getContextLogger();  // Gets context automatically
    log.info('Creating user', { email: data.email });
  }
}
```

---

## Log Record Schema

### Tier 1: Essential Fields (Always Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `timestamp` | ISO 8601 | When event occurred | `2025-12-16T10:30:00.123Z` |
| `level` | string | Log severity | `INFO`, `WARN`, `ERROR` |
| `message` | string | Human-readable description | `User login successful` |
| `service` | string | Service/application name | `user-auth` |

### Tier 2: Tracing Fields (Distributed Systems)

| Field | Type | Description |
|-------|------|-------------|
| `trace_id` | string | Request chain identifier (32 hex) |
| `span_id` | string | Current operation ID (16 hex) |
| `request_id` | string | HTTP request identifier |

### Tier 3: Context Fields (Debugging)

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | string | User identifier (hashed if needed) |
| `method` | string | Function/method name |
| `duration_ms` | number | Operation duration |
| `error_code` | string | Application error code |
| `error_message` | string | Error description |

### Tier 4: Environment Fields (Operations)

| Field | Type | Description |
|-------|------|-------------|
| `env` | string | Deployment environment |
| `version` | string | Service version |
| `host` | string | Server hostname |
| `region` | string | Cloud region |

### Example Log Entry

```json
{
  "timestamp": "2025-12-16T10:30:00.123Z",
  "level": "INFO",
  "message": "Order created",
  "service": "order-service",
  "trace_id": "7b2e4f1a9c3d8e5b6a1f2c3d4e5f6a7b",
  "span_id": "1a2b3c4d5e6f7890",
  "request_id": "req_abc123",
  "user_id": "usr_456",
  "duration_ms": 145
}
```

---

## Log Levels

| Level | When to Use | Production | Alert |
|-------|-------------|------------|-------|
| `DEBUG` | Development diagnostics | Off | No |
| `INFO` | Normal business operations | On | No |
| `WARN` | Unexpected but recoverable | On | Optional |
| `ERROR` | Failures requiring attention | On | Yes |
| `FATAL` | Application cannot continue | On | Immediate |

### Level Selection Guide

```
DEBUG → Variable states, cache misses, detailed flow
INFO  → Business milestones: "User registered", "Order shipped"
WARN  → Degraded service: "DB slow, retrying", "Rate limit at 80%"
ERROR → Failures: "Payment failed", "Query timeout after 3 retries"
FATAL → Unrecoverable: "DB connection lost", "Out of memory"
```

---

## Centralized Configuration

```typescript
// lib/logging/config.ts
export interface LoggingConfig {
  service: string;
  environment: 'development' | 'staging' | 'production';
  level: 'debug' | 'info' | 'warn' | 'error' | 'fatal';
  format: 'json' | 'pretty';
  redactPaths?: string[];  // ['password', 'token', 'secret']
}

// lib/logging/index.ts
let initialized = false;
let globalLogger: Logger;

export function initializeLogging(config: LoggingConfig): void {
  if (initialized) return;
  globalLogger = createLogger(config);
  initialized = true;
}

export function getLogger(): Logger {
  if (!initialized) throw new Error('Call initializeLogging() at startup');
  return globalLogger;
}
```

---

## Library Selection

| Language | Library | Why |
|----------|---------|-----|
| Node.js | **Pino** | Fastest, native JSON |
| Node.js | Winston | Most popular, flexible |
| Python | **structlog** | Best structured logging |
| Go | **zerolog** | Zero allocation |
| Java | Logback + SLF4J | Industry standard |
| Rust | tracing | Async-aware |
| C#/.NET | Serilog | Structured logging pioneer |

---

## TypeScript Implementation

A complete, copy-paste ready logging setup:

```typescript
// lib/logging/types.ts
export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  service: string;
  trace_id?: string;
  request_id?: string;
  [key: string]: unknown;
}

export interface LoggingConfig {
  service: string;
  level: LogLevel;
  pretty?: boolean;
}
```

```typescript
// lib/logging/logger.ts
import { LogEntry, LogLevel, LoggingConfig } from './types';

const LEVELS: Record<LogLevel, number> = { debug: 0, info: 1, warn: 2, error: 3 };

class Logger {
  private config: LoggingConfig;
  private context: Record<string, unknown> = {};

  constructor(config: LoggingConfig) {
    this.config = config;
  }

  private shouldLog(level: LogLevel): boolean {
    return LEVELS[level] >= LEVELS[this.config.level];
  }

  private write(level: LogLevel, message: string, data?: Record<string, unknown>) {
    if (!this.shouldLog(level)) return;

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      service: this.config.service,
      ...this.context,
      ...data,
    };

    const output = this.config.pretty
      ? `[${entry.timestamp}] ${level.toUpperCase()} ${message} ${JSON.stringify(data || {})}`
      : JSON.stringify(entry);

    console.log(output);
  }

  debug(message: string, data?: Record<string, unknown>) { this.write('debug', message, data); }
  info(message: string, data?: Record<string, unknown>) { this.write('info', message, data); }
  warn(message: string, data?: Record<string, unknown>) { this.write('warn', message, data); }
  error(message: string, data?: Record<string, unknown>) { this.write('error', message, data); }

  child(context: Record<string, unknown>): Logger {
    const child = new Logger(this.config);
    child.context = { ...this.context, ...context };
    return child;
  }
}

export { Logger };
```

```typescript
// lib/logging/index.ts
import { Logger } from './logger';
import { LoggingConfig } from './types';

let instance: Logger | null = null;

export function initLogging(config: LoggingConfig): void {
  instance = new Logger(config);
}

export function getLogger(): Logger {
  if (!instance) throw new Error('Call initLogging() first');
  return instance;
}

// Usage:
// initLogging({ service: 'my-app', level: 'info', pretty: process.env.NODE_ENV === 'development' });
// const log = getLogger();
// log.info('Server started', { port: 3000 });
```

---

## Best Practices

### DO ✅

```typescript
// Structured, queryable data
log.info('Order created', {
  order_id: 'ord_123',
  user_id: 'usr_456',
  total_amount: 99.99,
  items_count: 3
});

// Include correlation IDs
log.info('Processing payment', { trace_id, span_id, order_id });

// Log at boundaries
log.info('API request received', { method: 'POST', path: '/orders' });
log.info('API response sent', { status: 201, duration_ms: 145 });
```

### DON'T ❌

```typescript
// String concatenation (not queryable)
log.info(`User ${userId} created order ${orderId}`);

// Logging sensitive data
log.info('Login', { password: '...', credit_card: '...' });

// Wrong log levels
log.error('Cache miss');  // Should be DEBUG
log.debug('Payment failed'); // Should be ERROR

// Missing context
log.error('Something went wrong'); // What? Where? Why?
```

---

## Sensitive Data Handling

### Never Log
- Passwords, API keys, tokens, secrets
- Full credit card numbers, SSN
- Private keys

### Always Mask

| Data Type | Pattern | Example |
|-----------|---------|---------|
| Email | Partial | `j***n@example.com` |
| Phone | Last 4 | `****1234` |
| Credit Card | Last 4 | `****4242` |
| IP Address | Partial | `192.168.***.***` |

```typescript
export const mask = {
  email: (e: string) => `${e[0]}***${e.split('@')[0].slice(-1)}@${e.split('@')[1]}`,
  phone: (p: string) => `****${p.slice(-4)}`,
  card: (c: string) => `****${c.slice(-4)}`,
};
```

---

## Field Naming Conventions

```yaml
# Identifiers
user_id, order_id, product_id, session_id, request_id

# Tracing
trace_id, span_id, parent_span_id

# Time
timestamp, duration_ms, started_at, ended_at

# Status
status, outcome, error_code, error_message

# HTTP
http_method, http_path, http_status

# Database
db_system, db_name, db_operation

# Environment
env, version, host, region, instance_id
```

---

## Checklist

```markdown
## Architecture
- [ ] Centralized logging module (lib/logging/)
- [ ] Single configuration source
- [ ] No direct logger instantiation in business code

## Schema
- [ ] Tier 1 fields (timestamp, level, message, service)
- [ ] Tier 2 tracing (trace_id, span_id, request_id)
- [ ] Field naming convention documented
- [ ] Sensitive data masking rules

## Standards
- [ ] Log levels used correctly
- [ ] All logs are structured JSON
- [ ] No sensitive data in logs
- [ ] Consistent field names across services
- [ ] No console.log in production

## Operations
- [ ] Log aggregation configured
- [ ] Alerts for ERROR/FATAL levels
- [ ] Retention policy defined
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    STRUCTURED LOG ENTRY                     │
├─────────────────────────────────────────────────────────────┤
│  Tier 1 (Required)                                          │
│  ├── timestamp    → ISO 8601 format                         │
│  ├── level        → DEBUG|INFO|WARN|ERROR|FATAL             │
│  ├── message      → Human readable description              │
│  └── service      → Service name                            │
├─────────────────────────────────────────────────────────────┤
│  Tier 2 (Tracing)                                           │
│  ├── trace_id     → Request chain ID                        │
│  ├── span_id      → Current operation ID                    │
│  └── request_id   → HTTP request ID                         │
├─────────────────────────────────────────────────────────────┤
│  Tier 3 (Context)                                           │
│  ├── user_id      → Who triggered this                      │
│  ├── method       → Function/method name                    │
│  ├── duration_ms  → How long it took                        │
│  └── error_*      → Error details (if applicable)           │
├─────────────────────────────────────────────────────────────┤
│  Tier 4 (Environment)                                       │
│  ├── env          → production|staging|dev                  │
│  ├── version      → Service version                         │
│  └── host/region  → Where it's running                      │
└─────────────────────────────────────────────────────────────┘
```
