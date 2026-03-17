---
name: fullstory-logging
version: v2
description: Comprehensive guide for implementing Fullstory's Logging API (log method) for web applications. Teaches proper log level usage, message formatting, and capturing application logs in session replay. Includes detailed good/bad examples for error tracking, debugging, and operational monitoring to help developers add contextual log messages to Fullstory sessions.
related_skills:
  - fullstory-observe-callbacks
  - fullstory-analytics-events
  - fullstory-async-methods
---

# Fullstory Logging API

## Overview

Fullstory's Logging API allows developers to send log messages directly to Fullstory sessions without logging to the browser's developer console. These logs appear in the session replay, providing valuable context for debugging user issues, tracking application state, and understanding user workflows.

Key use cases:

- **Error Context**: Log errors with stack traces viewable in replay
- **Application State**: Record important state changes
- **Debugging**: Add contextual information during development
- **Audit Trail**: Log significant user actions
- **Support Context**: Add logs that support teams can see in sessions

## Core Concepts

### Log Levels

| Level     | Use For                | Console Equivalent |
| --------- | ---------------------- | ------------------ |
| `'log'`   | General information    | `console.log()`    |
| `'info'`  | Informational messages | `console.info()`   |
| `'warn'`  | Warning conditions     | `console.warn()`   |
| `'error'` | Error conditions       | `console.error()`  |
| `'debug'` | Debug information      | `console.debug()`  |

### Key Behaviors

| Behavior                   | Description                                        |
| -------------------------- | -------------------------------------------------- |
| **Not in browser console** | Logs only appear in Fullstory, not browser console |
| **Session context**        | Logs viewable in session replay timeline           |
| **Timestamp**              | Automatically timestamped by Fullstory             |
| **Searchable**             | Can search sessions by log content                 |

### When to Use FS Logging vs Console

| Use FS Logging                       | Use Console                        |
| ------------------------------------ | ---------------------------------- |
| Production errors you want in replay | Development-only debugging         |
| State changes for support context    | Verbose tracing during development |
| User action audit trails             | Performance timing logs            |
| Integration errors                   | Internal debugging                 |

---

## API Reference

### Basic Syntax

```javascript
FS('log', {
  level: string, // Optional: Log level (default: 'log')
  msg: string, // Required: Message to log
})
```

### Async Version

```javascript
await FS('logAsync', {
  level: string,
  msg: string,
})
```

### Parameters

| Parameter | Type   | Required | Default | Description                                        |
| --------- | ------ | -------- | ------- | -------------------------------------------------- |
| `level`   | string | No       | `'log'` | Log level: 'log', 'info', 'warn', 'error', 'debug' |
| `msg`     | string | **Yes**  | -       | Message to log (string only)                       |

### Rate Limits

- Standard API rate limits apply
- Excessive logging may be throttled

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: Error Logging with Context

```javascript
// GOOD: Log errors with context for session replay
function logError(error, context = {}) {
  // Create detailed error message
  const errorDetails = [
    `Error: ${error.message}`,
    `Type: ${error.name}`,
    `Context: ${JSON.stringify(context)}`,
    error.stack ? `Stack:\n${error.stack}` : '',
  ]
    .filter(Boolean)
    .join('\n')

  // Send to Fullstory
  FS('log', {
    level: 'error',
    msg: errorDetails,
  })

  // Also send to your error tracking service
  // Sentry, Bugsnag, etc.
}

// Usage
try {
  await processPayment(paymentData)
} catch (error) {
  logError(error, {
    action: 'processPayment',
    paymentMethod: paymentData.method,
    amount: paymentData.amount,
  })
  showErrorToUser('Payment failed. Please try again.')
}
```

**Why this is good:**

- ✅ Includes error type, message, and stack trace
- ✅ Adds business context (action, payment details)
- ✅ Uses appropriate 'error' level
- ✅ Formatted for readability in replay

### Example 2: API Response Logging

```javascript
// GOOD: Log API responses for debugging
async function fetchWithLogging(url, options = {}) {
  const startTime = Date.now()

  FS('log', {
    level: 'info',
    msg: `API Request: ${options.method || 'GET'} ${url}`,
  })

  try {
    const response = await fetch(url, options)
    const duration = Date.now() - startTime

    if (!response.ok) {
      FS('log', {
        level: 'warn',
        msg: `API Error: ${response.status} ${response.statusText} - ${url} (${duration}ms)`,
      })
    } else {
      FS('log', {
        level: 'log',
        msg: `API Success: ${response.status} - ${url} (${duration}ms)`,
      })
    }

    return response
  } catch (error) {
    const duration = Date.now() - startTime

    FS('log', {
      level: 'error',
      msg: `API Failed: ${error.message} - ${url} (${duration}ms)`,
    })

    throw error
  }
}

// Usage
const response = await fetchWithLogging('/api/users/123')
```

**Why this is good:**

- ✅ Logs request start, success, and failures
- ✅ Includes timing information
- ✅ Appropriate log levels (info, warn, error)
- ✅ URL and status for debugging

### Example 3: User Action Audit Trail

```javascript
// GOOD: Create audit trail of important user actions
class AuditLogger {
  static log(action, details = {}) {
    const message = [
      `Action: ${action}`,
      `Time: ${new Date().toISOString()}`,
      `Details: ${JSON.stringify(details)}`,
    ].join(' | ')

    FS('log', {
      level: 'info',
      msg: message,
    })
  }

  static logNavigation(from, to) {
    this.log('Navigation', {from, to})
  }

  static logFormSubmit(formName, success) {
    this.log('Form Submit', {
      formName,
      success,
      timestamp: Date.now(),
    })
  }

  static logFeatureUsed(featureName, context = {}) {
    this.log('Feature Used', {featureName, ...context})
  }

  static logSettingChanged(setting, oldValue, newValue) {
    this.log('Setting Changed', {
      setting,
      oldValue: String(oldValue),
      newValue: String(newValue),
    })
  }
}

// Usage
AuditLogger.logNavigation('/dashboard', '/settings')
AuditLogger.logFormSubmit('contact-form', true)
AuditLogger.logFeatureUsed('export', {format: 'csv', rows: 500})
AuditLogger.logSettingChanged('notifications', true, false)
```

**Why this is good:**

- ✅ Consistent log format
- ✅ Rich context for each action
- ✅ Easy to search in Fullstory
- ✅ Reusable across application

### Example 4: State Change Logging

```javascript
// GOOD: Log important state changes for debugging
function createLoggingStore(initialState, storeName) {
  let state = initialState

  return {
    getState() {
      return state
    },

    setState(updates, actionName = 'unknown') {
      const prevState = {...state}
      state = {...state, ...updates}

      // Log the state change
      FS('log', {
        level: 'log',
        msg: `[${storeName}] ${actionName}: ${JSON.stringify({
          changes: Object.keys(updates),
          newValues: updates,
        })}`,
      })

      return state
    },
  }
}

// Usage
const cartStore = createLoggingStore({items: [], total: 0}, 'CartStore')

cartStore.setState(
  {
    items: [...cartStore.getState().items, newItem],
    total: cartStore.getState().total + newItem.price,
  },
  'addItem',
)
// Logs: [CartStore] addItem: {"changes":["items","total"],"newValues":{...}}
```

**Why this is good:**

- ✅ Tracks state changes with context
- ✅ Includes action name for debugging
- ✅ Shows what changed
- ✅ Store name for multi-store apps

### Example 5: Integration Error Logging

```javascript
// GOOD: Log third-party integration errors
class IntegrationLogger {
  constructor(integrationName) {
    this.integrationName = integrationName
  }

  logConnectionAttempt() {
    FS('log', {
      level: 'info',
      msg: `[${this.integrationName}] Attempting connection...`,
    })
  }

  logConnected() {
    FS('log', {
      level: 'info',
      msg: `[${this.integrationName}] Connected successfully`,
    })
  }

  logDisconnected(reason) {
    FS('log', {
      level: 'warn',
      msg: `[${this.integrationName}] Disconnected: ${reason}`,
    })
  }

  logError(operation, error) {
    FS('log', {
      level: 'error',
      msg: `[${this.integrationName}] ${operation} failed: ${error.message}`,
    })
  }

  logTimeout(operation, timeoutMs) {
    FS('log', {
      level: 'warn',
      msg: `[${this.integrationName}] ${operation} timed out after ${timeoutMs}ms`,
    })
  }
}

// Usage
const stripeLogger = new IntegrationLogger('Stripe')

async function initializeStripe() {
  stripeLogger.logConnectionAttempt()

  try {
    await stripe.init()
    stripeLogger.logConnected()
  } catch (error) {
    stripeLogger.logError('initialization', error)
    throw error
  }
}
```

**Why this is good:**

- ✅ Clear integration name prefix
- ✅ Tracks full lifecycle
- ✅ Appropriate log levels
- ✅ Reusable for multiple integrations

### Example 6: Debug Mode Logging

```javascript
// GOOD: Conditional verbose logging for debugging
class DebugLogger {
  static isDebugMode() {
    return (
      localStorage.getItem('fs_debug') === 'true' ||
      new URLSearchParams(window.location.search).has('debug')
    )
  }

  static debug(message, data = null) {
    if (this.isDebugMode()) {
      const fullMessage = data
        ? `[DEBUG] ${message}\nData: ${JSON.stringify(data, null, 2)}`
        : `[DEBUG] ${message}`

      FS('log', {
        level: 'debug',
        msg: fullMessage,
      })

      // Also log to console in debug mode
      console.debug(message, data)
    }
  }

  static trace(functionName, args) {
    if (this.isDebugMode()) {
      FS('log', {
        level: 'debug',
        msg: `[TRACE] ${functionName}(${args.map((a) => JSON.stringify(a)).join(', ')})`,
      })
    }
  }

  static measure(label, fn) {
    if (!this.isDebugMode()) {
      return fn()
    }

    const start = performance.now()
    const result = fn()
    const duration = performance.now() - start

    FS('log', {
      level: 'debug',
      msg: `[PERF] ${label}: ${duration.toFixed(2)}ms`,
    })

    return result
  }
}

// Usage
DebugLogger.debug('Processing checkout', {cartId, itemCount})
DebugLogger.trace('calculateTotal', [items, taxRate, discount])
const total = DebugLogger.measure('calculateTotal', () => calculateTotal(items))
```

**Why this is good:**

- ✅ Conditional logging (only when needed)
- ✅ Rich debug information
- ✅ Performance measurement option
- ✅ Easy to enable via localStorage or URL

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Logging Sensitive Data

```javascript
// BAD: Logging sensitive/PII data
FS('log', {
  level: 'info',
  msg: `User login: email=${user.email}, password=${user.password}`, // BAD: Password!
})

FS('log', {
  level: 'info',
  msg: `Payment: card=${user.creditCard}`, // BAD: Credit card!
})
```

**Why this is bad:**

- ❌ Logs PII (email exposed unnecessarily)
- ❌ Logs secrets (password!)
- ❌ Logs PCI data (credit card!)
- ❌ Security and compliance violation

**CORRECTED VERSION:**

```javascript
// GOOD: Sanitize sensitive data
FS('log', {
  level: 'info',
  msg: `User login: userId=${user.id}, method=password`,
})

FS('log', {
  level: 'info',
  msg: `Payment: cardLast4=${user.creditCard.slice(-4)}, type=${user.cardType}`,
})
```

### Example 2: Excessive Logging

```javascript
// BAD: Logging too much
document.addEventListener('mousemove', (e) => {
  FS('log', {
    level: 'debug',
    msg: `Mouse: ${e.clientX}, ${e.clientY}`,
  }) // BAD: Fires hundreds of times per second!
})

for (let i = 0; i < 10000; i++) {
  FS('log', {
    level: 'log',
    msg: `Processing item ${i}`,
  }) // BAD: 10,000 log calls!
}
```

**Why this is bad:**

- ❌ Will hit rate limits
- ❌ Drowns out useful logs
- ❌ Performance impact
- ❌ Makes sessions hard to analyze

**CORRECTED VERSION:**

```javascript
// GOOD: Log significant events only
FS('log', {
  level: 'info',
  msg: `Processing started: 10000 items`,
})

// ... process items ...

FS('log', {
  level: 'info',
  msg: `Processing complete: 10000 items in ${duration}ms`,
})
```

### Example 3: Non-String Messages

```javascript
// BAD: Passing objects instead of strings
FS('log', {
  level: 'error',
  msg: {error: 'Something failed', code: 500}, // BAD: Object!
})

FS('log', {
  level: 'log',
  msg: ['item1', 'item2', 'item3'], // BAD: Array!
})
```

**Why this is bad:**

- ❌ msg must be a string
- ❌ Objects/arrays won't display properly
- ❌ May cause errors or [object Object]

**CORRECTED VERSION:**

```javascript
// GOOD: Stringify objects
FS('log', {
  level: 'error',
  msg: JSON.stringify({error: 'Something failed', code: 500}),
})

FS('log', {
  level: 'log',
  msg: `Items: ${['item1', 'item2', 'item3'].join(', ')}`,
})
```

### Example 4: Missing Error Details

```javascript
// BAD: Vague error logging
try {
  await doSomething()
} catch (error) {
  FS('log', {
    level: 'error',
    msg: 'An error occurred', // BAD: No useful information!
  })
}
```

**Why this is bad:**

- ❌ No information about what failed
- ❌ No error message or stack
- ❌ Impossible to debug

**CORRECTED VERSION:**

```javascript
// GOOD: Detailed error logging
try {
  await doSomething()
} catch (error) {
  FS('log', {
    level: 'error',
    msg: `doSomething failed: ${error.message}\nStack: ${error.stack}`,
  })
}
```

### Example 5: Wrong Log Levels

```javascript
// BAD: Misusing log levels
FS('log', {
  level: 'error',
  msg: 'User clicked button', // BAD: Not an error!
})

FS('log', {
  level: 'debug',
  msg: 'Database connection failed!', // BAD: This is an error!
})
```

**Why this is bad:**

- ❌ Error level for normal events
- ❌ Debug level for critical errors
- ❌ Makes triage difficult
- ❌ Misleading in session analysis

**CORRECTED VERSION:**

```javascript
// GOOD: Appropriate log levels
FS('log', {
  level: 'info',
  msg: 'User clicked button: submit-form',
})

FS('log', {
  level: 'error',
  msg: 'Database connection failed: timeout after 30s',
})
```

### Example 6: Logging Instead of Events

```javascript
// BAD: Using logs for analytics instead of events
FS('log', {
  level: 'info',
  msg: 'Purchase completed: $99.99, order_id: ORD-123',
})
// Missing: FS('trackEvent', ...) for proper analytics!
```

**Why this is bad:**

- ❌ Logs aren't searchable like events
- ❌ Can't segment by purchase amount
- ❌ Doesn't appear in event analytics
- ❌ Misuse of logging API

**CORRECTED VERSION:**

```javascript
// GOOD: Use events for analytics, logs for debugging
FS('trackEvent', {
  name: 'Order Completed',
  properties: {
    orderId: 'ORD-123',
    revenue: 99.99,
  },
})

// Log additional debugging context if needed
FS('log', {
  level: 'info',
  msg: 'Order ORD-123 processed successfully',
})
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Centralized Logger

```javascript
// Centralized logging utility
const AppLogger = {
  _formatMessage(prefix, message, data) {
    let formatted = `[${prefix}] ${message}`
    if (data) {
      formatted += `\nData: ${JSON.stringify(data)}`
    }
    return formatted
  },

  log(message, data) {
    if (typeof FS !== 'undefined') {
      FS('log', {level: 'log', msg: this._formatMessage('LOG', message, data)})
    }
  },

  info(message, data) {
    if (typeof FS !== 'undefined') {
      FS('log', {level: 'info', msg: this._formatMessage('INFO', message, data)})
    }
  },

  warn(message, data) {
    if (typeof FS !== 'undefined') {
      FS('log', {level: 'warn', msg: this._formatMessage('WARN', message, data)})
    }
  },

  error(message, error, data) {
    if (typeof FS !== 'undefined') {
      let errorMsg = this._formatMessage('ERROR', message, data)
      if (error) {
        errorMsg += `\nError: ${error.message}\nStack: ${error.stack}`
      }
      FS('log', {level: 'error', msg: errorMsg})
    }
  },

  debug(message, data) {
    if (typeof FS !== 'undefined' && this._isDebugEnabled()) {
      FS('log', {level: 'debug', msg: this._formatMessage('DEBUG', message, data)})
    }
  },

  _isDebugEnabled() {
    return localStorage.getItem('fs_debug') === 'true'
  },
}

// Usage
AppLogger.info('Page loaded', {path: window.location.pathname})
AppLogger.warn('Slow API response', {endpoint: '/api/data', duration: 5000})
AppLogger.error('Checkout failed', error, {cartId: '123'})
```

### Pattern 2: Scoped Logger Factory

```javascript
// Create loggers scoped to modules/components
function createScopedLogger(scope) {
  return {
    log(message, data) {
      FS('log', {
        level: 'log',
        msg: `[${scope}] ${message}${data ? ` | ${JSON.stringify(data)}` : ''}`,
      })
    },
    info(message, data) {
      FS('log', {
        level: 'info',
        msg: `[${scope}] ${message}${data ? ` | ${JSON.stringify(data)}` : ''}`,
      })
    },
    warn(message, data) {
      FS('log', {
        level: 'warn',
        msg: `[${scope}] ${message}${data ? ` | ${JSON.stringify(data)}` : ''}`,
      })
    },
    error(message, error) {
      FS('log', {
        level: 'error',
        msg: `[${scope}] ${message}${error ? ` | ${error.message}` : ''}`,
      })
    },
  }
}

// Usage in different modules
const authLogger = createScopedLogger('Auth')
authLogger.info('Login attempt', {method: 'password'})

const paymentLogger = createScopedLogger('Payment')
paymentLogger.error('Payment failed', new Error('Insufficient funds'))
```

### Pattern 3: Request/Response Logger Middleware

```javascript
// Fetch wrapper with automatic logging
function createLoggingFetch() {
  const originalFetch = window.fetch

  return async function loggingFetch(url, options = {}) {
    const requestId = Math.random().toString(36).substr(2, 9)
    const method = options.method || 'GET'
    const startTime = Date.now()

    FS('log', {
      level: 'info',
      msg: `[HTTP:${requestId}] → ${method} ${url}`,
    })

    try {
      const response = await originalFetch(url, options)
      const duration = Date.now() - startTime

      const level = response.ok ? 'info' : 'warn'
      FS('log', {
        level,
        msg: `[HTTP:${requestId}] ← ${response.status} ${method} ${url} (${duration}ms)`,
      })

      return response
    } catch (error) {
      const duration = Date.now() - startTime
      FS('log', {
        level: 'error',
        msg: `[HTTP:${requestId}] ✕ ${method} ${url} - ${error.message} (${duration}ms)`,
      })
      throw error
    }
  }
}

// Apply globally
window.fetch = createLoggingFetch()
```

---

## TROUBLESHOOTING

### Logs Not Appearing in Session

**Symptom**: FS('log') called but logs not in session replay

**Common Causes**:

1. ❌ Fullstory not initialized
2. ❌ Session not being recorded
3. ❌ Page excluded from capture
4. ❌ FS blocked by ad blocker

**Solutions**:

- ✅ Verify FS is defined before logging
- ✅ Check Fullstory is recording
- ✅ Verify page isn't excluded
- ✅ Check browser network tab for FS requests

### Log Messages Truncated

**Symptom**: Long messages appear cut off

**Common Causes**:

1. ❌ Message too long
2. ❌ JSON stringification issues

**Solutions**:

- ✅ Keep messages concise
- ✅ Summarize large data structures
- ✅ Log key fields only

---

## KEY TAKEAWAYS FOR AGENT

When helping developers with Logging API:

1. **Always emphasize**:
   - msg must be a string
   - Never log sensitive data (passwords, PII, credit cards)
   - Use appropriate log levels
   - Logs are for context, not analytics

2. **Common mistakes to watch for**:
   - Logging sensitive information
   - Excessive logging (loops, mousemove)
   - Objects instead of strings
   - Wrong log levels
   - Using logs instead of events

3. **Questions to ask developers**:
   - What are you trying to debug?
   - Does this contain any sensitive data?
   - How frequently will this log?
   - Should this be an event instead?

4. **Best practices to recommend**:
   - Sanitize data before logging
   - Use consistent formatting
   - Include context (IDs, state)
   - Use events for analytics, logs for debugging

---

## REFERENCE LINKS

- **Logging**: https://developer.fullstory.com/browser/fullcapture/logging/
- **Help Center - Console Logs**: https://help.fullstory.com/hc/en-us/articles/360020623154

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's Logging API correctly for web applications._
