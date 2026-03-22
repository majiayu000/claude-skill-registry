---
name: datagrok-logging
description: Guide for logging errors, warnings, and info messages in Datagrok packages. Use when code needs error handling, user notifications, or server-side logging.
---

# Datagrok Logging & Notification API

Help the user choose and implement the correct logging/notification approach in Datagrok packages.

## Usage
```
/datagrok-logging
```

## User-Facing Notifications (Balloons)

Toast notifications shown to the user. Primary methods for communicating from package code.

```typescript
import * as grok from 'datagrok-api/grok';

// Green balloon — success or informational
grok.shell.info('Operation completed');

// Red balloon — error
grok.shell.error('Something went wrong');

// Yellow balloon — warning
grok.shell.warning('Check your settings');
```

All three accept `string | HTMLElement` and an optional `BalloonOptions`:

```typescript
interface BalloonOptions {
  oneTimeKey?: string;   // Show only once per key (prevents repeated identical messages)
  copyText?: string;     // Text copied to clipboard on click
  autoHide?: boolean;    // Auto-hide after timeout (default: true)
  timeout?: number;      // Timeout in seconds (default: 5)
}

grok.shell.error('Failed to connect', { timeout: 10 });
grok.shell.info('Copied!', { oneTimeKey: 'copy-hint', autoHide: true });
```

## Server-Side Logging (DG.Logger)

For audit trails, usage tracking, and debug logging recorded on the Datagrok server. These do NOT show UI notifications.

```typescript
import * as DG from 'datagrok-api/dg';

// Create a logger (optionally with default params attached to every entry)
const logger = DG.Logger.create({ params: { source: 'MyPackage' } });

// Log levels
logger.debug('Detailed diagnostic info', { step: 'init' });
logger.info('Normal operation', { action: 'loaded' });
logger.warning('Potential issue', { config: 'missing' });
logger.error('Something failed', { context: 'upload' }, stackTrace);
logger.audit('User did something', { item: 'report' });
logger.usage('Feature used', { feature: 'export' });
```

### PackageLogger

Automatically tags log entries with the package name:

```typescript
const logger = new DG.PackageLogger(_package);
logger.error('Connection failed');  // tagged with package name
```

### LOG_LEVEL enum

```typescript
DG.LOG_LEVEL.DEBUG   // 'debug'
DG.LOG_LEVEL.INFO    // 'info'
DG.LOG_LEVEL.WARNING // 'warning'
DG.LOG_LEVEL.ERROR   // 'error'
DG.LOG_LEVEL.AUDIT   // 'audit'
DG.LOG_LEVEL.USAGE   // 'usage'
```

## Progress Indicator with Logging

For long-running operations with status updates shown in the task bar:

```typescript
const pi = DG.TaskBarProgressIndicator.create('Processing...', { cancelable: true });
pi.update(50, 'Half done');
pi.log('Step 1 finished');   // Append to progress log
pi.close();
```

## Log Event Stream

Subscribe to all log events in real time:

```typescript
grok.events.onLog.subscribe((msg) => {
  console.log(`[${msg.level}] ${msg.message}`, msg.params);
});
```

## When to Use What

| Scenario | Method |
|----------|--------|
| Tell the user something succeeded | `grok.shell.info()` |
| Show a user-facing error | `grok.shell.error()` |
| Show a user-facing warning | `grok.shell.warning()` |
| Log for debugging (server-side) | `logger.debug()` / `logger.info()` |
| Record errors for diagnostics | `logger.error(message, params, stackTrace)` |
| Track feature usage | `logger.usage()` |
| Audit user actions | `logger.audit()` |
| Show progress for long ops | `DG.TaskBarProgressIndicator` |
| Internal dev logging (not recorded) | `console.log()` / `console.warn()` |

## Rules

- **Never use `console.log` for production logging** — use `DG.Logger` for server-side or `grok.shell.*` for user-facing.
- `console.warn` / `console.error` are acceptable for development diagnostics but won't be recorded on the server.
- Prefer `grok.shell.warning()` over `grok.shell.error()` for non-critical issues (e.g., missing optional config).
- Use `grok.shell.error()` for failures that block the user's workflow.
- Use `oneTimeKey` when a notification could fire repeatedly (e.g., in a loop or event handler).