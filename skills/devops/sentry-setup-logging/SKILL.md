---
name: sentry-setup-logging
description: Setup Sentry Logging in any project. Use this when asked to add Sentry logs, enable structured logging, setup console log capture, or integrate logging with Sentry. Supports JavaScript, TypeScript, Python, Ruby, React, Next.js, and other frameworks.
---

# SOURCE: getsentry/sentry-for-claude
# PATH: skills/sentry-setup-logging/SKILL.md


# Setup Sentry Logging

This skill helps configure Sentry's structured logging feature across multiple platforms and frameworks.

## When to Use This Skill

Invoke this skill when:
- User asks to "setup Sentry logging" or "add Sentry logs"
- User wants to "capture console logs in Sentry"
- User requests "structured logging with Sentry"
- User mentions they want to send logs to Sentry
- User asks about `Sentry.logger` or `sentry_sdk.logger`
- User wants to integrate their existing logging library with Sentry

## Platform Detection

Before configuring, detect the project's platform:

### JavaScript/TypeScript Detection
Check for these files:
- `package.json` - Read to identify framework and Sentry SDK version
- Look for `@sentry/nextjs`, `@sentry/react`, `@sentry/node`, `@sentry/browser`, etc.
- Check if SDK version is 9.41.0+ (required for logging)

### Python Detection
Check for:
- `requirements.txt`, `pyproject.toml`, `setup.py`, or `Pipfile`
- Look for `sentry-sdk` version 2.35.0+ (required for logging)

### Ruby Detection
Check for:
- `Gemfile` or `*.gemspec`
- Look for `sentry-ruby` gem version 5.24.0+ (required for logging)

## Required Information

Ask the user:

```
I'll help you set up Sentry Logging. First, let me check your project setup.

After detecting the platform, I need to know:

1. **Logging approach** - Which setup do you prefer?
   - Console Integration: Automatically capture existing console.log/print statements
   - Structured Logging: Use Sentry.logger for new structured log calls
   - Both: Set up both approaches

2. **Log levels** (optional): Which levels should be captured?
   - Default: info, warn, error
   - All: trace, debug, info, warn, error, fatal
```

## Configuration by Platform

---

## JavaScript/TypeScript Platforms

### Minimum SDK Versions
- All JS platforms: `9.41.0+`
- Consola integration: `10.12.0+`

### Step 1: Verify SDK Version

```bash
grep -E '"@sentry/(nextjs|react|node|browser)"' package.json
```

If version is below 9.41.0, inform user to upgrade:
```bash
npm install @sentry/nextjs@latest  # or appropriate package
```

### Step 2: Enable Logging in Init

Find the Sentry.init() call and add `enableLogs: true`.

**Locate init files:**
- Next.js: `instrumentation-client.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`
- React: `src/index.tsx`, `src/main.tsx`, or dedicated sentry config file
- Node.js: Entry point file or dedicated sentry config
- Browser: Entry point or config file

**Modify init:**

```javascript
import * as Sentry from "@sentry/nextjs"; // or @sentry/react, @sentry/node, etc.

Sentry.init({
  dsn: "YOUR_DSN_HERE",

  // Enable structured logging
  enableLogs: true,

  // ... other existing config
});
```

### Step 3: Setup Console Integration (Optional)

If user wants console log capture, add the integration:

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  enableLogs: true,

  integrations: [
    Sentry.consoleLoggingIntegration({
      levels: ["log", "warn", "error"] // Customize as needed
    }),
  ],
});
```

**Available console levels:** `debug`, `info`, `warn`, `error`, `log`, `assert`, `trace`

### Step 4: Setup Log Filtering (Optional)

If user wants to filter logs before sending:

```javascript
Sentry.init({
  dsn: "YOUR_DSN_HERE",
  enableLogs: true,

  beforeSendLog: (log) => {
    // Drop info-level logs
    if (log.level === "info") {
      return null;
    }
    // Modify or pass through
    return log;
  },
});
```

### Structured Logging Examples (JavaScript)

Provide these examples to the user:

```javascript
// Basic logging with attributes
Sentry.logger.info("User logged in", {
  userId: "user_123",
  method: "oauth",
});

Sentry.logger.error("Payment failed", {
  orderId: "order_456",
  amount: 99.99,
  currency: "USD",
});

// Template literal formatting (creates searchable attributes)
Sentry.logger.info(
  Sentry.logger.fmt`User '${user.name}' purchased '${product.name}'`
);

// All available log levels
Sentry.logger.trace("Detailed trace info");
Sentry.logger.debug("Debug information");
Sentry.logger.info("Informational message");
Sentry.logger.warn("Warning message");
Sentry.logger.error("Error occurred");
Sentry.logger.fatal("Fatal error - application cannot continue");
```

### Third-Party Logger Integrations (JavaScript)

**Pino Integration:**
```javascript
import * as Sentry from "@sentry/node";
import pino from "pino";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  enableLogs: true,
  integrations: [Sentry.pinoIntegration()],
});

const logger = pino();
logger.info("This goes to Sentry");
```

**Winston Integration:**
```javascript
import * as Sentry from "@sentry/node";
import winston from "winston";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  enableLogs: true,
});

const sentryTransport = Sentry.createSentryWinstonTransport();
const logger = winston.createLogger({
  transports: [sentryTransport],
});
```

**Consola Integration (SDK 10.12.0+):**
```javascript
import * as Sentry from "@sentry/node";
import { consola } from "consola";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  enableLogs: true,
});

const sentryReporter = Sentry.createConsolaReporter({
  levels: ["error", "warn", "info"],
});
consola.addReporter(sentryReporter);
```

---

## Python Platform

### Minimum SDK Version
- `sentry-sdk` version `2.35.0+`

### Step 1: Verify SDK Version

```bash
pip show sentry-sdk | grep Version
```

If version is below 2.35.0:
```bash
pip install --upgrade sentry-sdk
```

### Step 2: Enable Logging in Init

Find `sentry_sdk.init()` and add `enable_logs=True`.

**Common locations:**
- Django: `settings.py`
- Flask: `app.py` or `__init__.py`
- FastAPI: `main.py`
- General: Entry point or dedicated config file

**Modify init:**

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",

    # Enable structured logging
    enable_logs=True,

    # ... other existing config
)
```

### Step 3: Setup Standard Library Logging Integration (Optional)

To capture Python's stdlib logging:

```python
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    enable_logs=True,
    integrations=[
        LoggingIntegration(
            sentry_logs_level=logging.WARNING  # Capture WARNING and above
        )
    ],
)
```

**Available levels:** `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR`, `logging.CRITICAL`

### Step 4: Setup Log Filtering (Optional)

```python
def before_send_log(log, hint):
    # Drop info-level logs
    if log["severity_text"] == "info":
        return None
    return log

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    enable_logs=True,
    before_send_log=before_send_log,
)
```

### Structured Logging Examples (Python)

```python
from sentry_sdk import logger as sentry_logger

# Basic logging with placeholder syntax
sentry_logger.info("User logged in: {user_id}", user_id="user_123")

sentry_logger.error(
    "Payment failed. Order: {order_id}. Amount: {amount}",
    order_id="order_456",
    amount=99.99
)

# Using attributes kwarg for additional context
sentry_logger.warning(
    "Rate limit approaching",
    attributes={
        "endpoint": "/api/users",
        "current_rate": 95,
        "limit": 100,
    }
)

# All available log levels
sentry_logger.trace("Detailed trace info")
sentry_logger.debug("Debug information")
sentry_logger.info("Informational message")
sentry_logger.warning("Warning message")
sentry_logger.error("Error occurred")
sentry_logger.fatal("Fatal error")
```

### Loguru Integration (Python)

```python
import sentry_sdk
from sentry_sdk.integrations.loguru import LoguruIntegration, LoggingLevels
from loguru import logger

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    enable_logs=True,
    integrations=[
        LoguruIntegration(
            sentry_logs_level=LoggingLevels.WARNING.value
        )
    ],
)

logger.warning("This goes to Sentry")
```

---

## Ruby Platform

### Minimum SDK Version
- `sentry-ruby` version `5.24.0+`

### Step 1: Verify SDK Version

```bash
bundle show sentry-ruby
# or
gem list sentry-ruby
```

If version is below 5.24.0:
```ruby
# In Gemfile
gem "sentry-ruby", ">= 5.24.0"
```
Then run `bundle update sentry-ruby`

### Step 2: Enable Logging in Init

Find `Sentry.init` block and add `config.enable_logs = true`.

**Common locations:**
- Rails: `config/initializers/sentry.rb`
- Sinatra/other: Entry point or config file

**Modify init:**

```ruby
Sentry.init do |config|
  config.dsn = "YOUR_DSN_HERE"

  # Enable structured logging
  config.enable_logs = true

  # ... other existing config
end
```

### Step 3: Setup Standard Logger Integration (Optional)

To capture Ruby's stdlib Logger:

```ruby
Sentry.init do |config|
  config.dsn = "YOUR_DSN_HERE"
  config.enable_logs = true
  config.enabled_patches = [:logger]
end
```

### Structured Logging Examples (Ruby)

```ruby
# Basic logging
Sentry.logger.info("User logged in")

# With named parameters (become searchable attributes)
Sentry.logger.debug("Cache miss for user %{user_id}", user_id: 123)

Sentry.logger.error(
  "Payment failed. Order: %{order_id}. Amount: %{amount}",
  order_id: "order_456",
  amount: 99.99
)

# All available log levels
Sentry.logger.trace("Detailed trace info")
Sentry.logger.debug("Debug information")
Sentry.logger.info("Informational message")
Sentry.logger.warning("Warning message")
Sentry.logger.error("Error occurred")
Sentry.logger.fatal("Fatal error")
```

---

## Framework-Specific Notes

### Next.js
- Enable logging in ALL init files: `instrumentation-client.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`
- Console integration works on both client and server
- Use `Sentry.logger` from `@sentry/nextjs`

### React (Browser)
- Enable logging in client init file only
- Console integration captures browser console calls
- Use `Sentry.logger` from `@sentry/react`

### Node.js
- Pino, Winston, and Consola integrations available
- Console integration captures server-side console calls
- Use `Sentry.logger` from `@sentry/node`

### Django
- Add logging config in `settings.py`
- LoggingIntegration captures Django's logging
- Extra fields in log records become Sentry attributes

### Flask
- Add logging config where you initialize the app
- Works with Flask's built-in logging

### Rails
- Add to `config/initializers/sentry.rb`
- Enable `:logger` patch for stdlib Logger capture

---

## Verification Steps

After setup, provide these verification instructions:

### JavaScript Verification
```javascript
// Add this temporarily to test
Sentry.logger.info("Sentry logging test", {
  test: true,
  timestamp: new Date().toISOString(),
});

console.log("Console capture test"); // If console integration enabled
```

### Python Verification
```python
from sentry_sdk import logger as sentry_logger

sentry_logger.info("Sentry logging test", test=True)

import logging
logging.warning("Standard logging test")  # If LoggingIntegration enabled
```

### Ruby Verification
```ruby
Sentry.logger.info("Sentry logging test")
```

Tell user to check their Sentry dashboard under **Logs** section to verify logs are arriving.

---

## Common Issues and Solutions

### Issue: Logs not appearing in Sentry
**Solutions:**
1. Verify SDK version meets minimum requirements
2. Ensure `enableLogs: true` (JS) or `enable_logs=True` (Python/Ruby) is set
3. Check DSN is correct
4. Verify you're looking at the Logs section (not Issues)
5. Check log level filtering isn't too restrictive

### Issue: Too many logs being sent
**Solutions:**
1. Use `beforeSendLog` / `before_send_log` to filter
2. Reduce log levels captured in console integration
3. Only enable logging where needed (e.g., just server-side)

### Issue: Console integration not capturing logs
**Solutions:**
1. Ensure integration is added to `integrations` array
2. Verify desired levels are included in `levels` array
3. Check for conflicts with other logging libraries

### Issue: SDK version too old
**Solutions:**
- JavaScript: `npm install @sentry/nextjs@latest`
- Python: `pip install --upgrade sentry-sdk`
- Ruby: `bundle update sentry-ruby`

---

## Summary Checklist

Provide this checklist after setup:

```markdown
## Sentry Logging Setup Complete

### Configuration Applied:
- [ ] SDK version verified (meets minimum requirements)
- [ ] `enableLogs` / `enable_logs` added to Sentry.init()
- [ ] Console integration added (if requested)
- [ ] Log filtering configured (if requested)
- [ ] Third-party logger integration added (if applicable)

### Sample Code Provided:
- [ ] Structured logging examples for your platform
- [ ] Verification test code

### Next Steps:
1. Run your application
2. Trigger some test logs
3. Check Sentry dashboard > Logs section
4. Adjust log levels and filtering as needed
```

---

## Quick Reference

| Platform | SDK Version | Enable Flag | Logger API |
|----------|-------------|-------------|------------|
| JavaScript | 9.41.0+ | `enableLogs: true` | `Sentry.logger.*` |
| Python | 2.35.0+ | `enable_logs=True` | `sentry_sdk.logger.*` |
| Ruby | 5.24.0+ | `config.enable_logs = true` | `Sentry.logger.*` |

| Log Level | JavaScript | Python | Ruby |
|-----------|------------|--------|------|
| Trace | `trace()` | `trace()` | `trace()` |
| Debug | `debug()` | `debug()` | `debug()` |
| Info | `info()` | `info()` | `info()` |
| Warning | `warn()` | `warning()` | `warning()` |
| Error | `error()` | `error()` | `error()` |
| Fatal | `fatal()` | `fatal()` | `fatal()` |
