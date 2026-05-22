---
name: Debugging Tools and Techniques
description: Comprehensive debugging strategies, tools, and techniques for efficiently identifying and fixing bugs across different environments.
---

# Debugging Tools and Techniques

## Overview

Debugging Tools and Techniques provide systematic approaches to finding and fixing bugs efficiently. Good debugging skills separate senior developers from juniors.

**Core Principle**: "Debugging is a science, not an art. Use tools, form hypotheses, test systematically."

---

## 1. Debugging Mindset

```markdown
## The Scientific Method for Debugging

1. **Observe**: What is the actual behavior?
2. **Hypothesize**: What could cause this?
3. **Test**: How can I verify my hypothesis?
4. **Analyze**: Was my hypothesis correct?
5. **Repeat**: If not, form new hypothesis

### Example
**Bug**: User login fails with 500 error

1. **Observe**: Server returns 500, logs show "Cannot read property 'id' of undefined"
2. **Hypothesize**: User object is null/undefined
3. **Test**: Add console.log before accessing user.id
4. **Analyze**: User is undefined when email doesn't exist
5. **Fix**: Add null check before accessing user.id
```

---

## 2. Browser DevTools

### Console Debugging
```javascript
// Basic logging
console.log('User:', user);

// Structured logging
console.table([
  { name: 'Alice', age: 30 },
  { name: 'Bob', age: 25 }
]);

// Grouping
console.group('User Login');
console.log('Email:', email);
console.log('Password length:', password.length);
console.groupEnd();

// Timing
console.time('API Call');
await fetchUser();
console.timeEnd('API Call');

// Conditional logging
console.assert(user !== null, 'User should not be null');

// Stack trace
console.trace('How did we get here?');
```

### Breakpoints
```javascript
// Debugger statement
function processPayment(amount) {
  debugger;  // Execution pauses here
  
  if (amount > 1000) {
    // Complex logic
  }
}

// Conditional breakpoint (in DevTools)
// Right-click line number → Add conditional breakpoint
// Condition: amount > 1000
```

### Network Tab
```markdown
## Network Debugging Checklist

- [ ] Check request URL (correct endpoint?)
- [ ] Check request method (GET/POST/PUT/DELETE)
- [ ] Check request headers (auth token present?)
- [ ] Check request payload (correct data?)
- [ ] Check response status (200/400/500?)
- [ ] Check response body (expected data?)
- [ ] Check timing (slow requests?)
- [ ] Check CORS errors
```

---

## 3. VS Code Debugging

### Launch Configuration
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Node.js",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build - tsconfig.json",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "env": {
        "NODE_ENV": "development"
      }
    },
    {
      "name": "Debug Jest Tests",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["--runInBand", "--no-cache"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    },
    {
      "name": "Attach to Process",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "restart": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

### Debugging Features
```typescript
// Logpoints (log without modifying code)
// Right-click line number → Add Logpoint
// Message: User ID: {user.id}, Email: {user.email}

// Watch expressions
// Add to Watch panel:
// - user.id
// - user.permissions.includes('admin')
// - Object.keys(user)

// Call stack inspection
// See how you got to current line

// Variable inspection
// Hover over variables to see values
```

---

## 4. Node.js Debugging

### Built-in Debugger
```bash
# Start with inspector
node --inspect src/index.js

# Start and break immediately
node --inspect-brk src/index.js

# Custom port
node --inspect=9230 src/index.js
```

### Chrome DevTools
```bash
# Start Node with inspector
node --inspect src/index.js

# Open Chrome
# Navigate to: chrome://inspect
# Click "inspect" under your process
```

### Debug Logging
```typescript
import debug from 'debug';

const log = debug('app:server');
const dbLog = debug('app:database');

log('Server starting on port %d', 3000);
dbLog('Connecting to database');

// Run with:
// DEBUG=app:* node src/index.js
// DEBUG=app:database node src/index.js
```

---

## 5. React Debugging

### React DevTools
```jsx
// Install React DevTools browser extension

// Component inspection
// - View props
// - View state
// - View hooks
// - View component tree

// Profiler
// - Record performance
// - Identify slow renders
// - Find unnecessary re-renders
```

### Common React Bugs
```jsx
// Bug: Infinite re-render
function BadComponent() {
  const [count, setCount] = useState(0);
  
  // ❌ This causes infinite loop
  setCount(count + 1);
  
  return <div>{count}</div>;
}

// Fix: Use useEffect
function GoodComponent() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    setCount(count + 1);
  }, []);  // Empty deps = run once
  
  return <div>{count}</div>;
}

// Bug: Stale closure
function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      // ❌ count is always 0 (stale closure)
      setCount(count + 1);
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  // ✅ Fix: Use functional update
  useEffect(() => {
    const interval = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
}
```

---

## 6. Database Debugging

### PostgreSQL
```sql
-- Enable query logging
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();

-- Explain query plan
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Active queries
SELECT pid, query, state, query_start
FROM pg_stat_activity
WHERE state = 'active';
```

### Prisma Debugging
```typescript
// Enable query logging
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

// Custom logging
const prisma = new PrismaClient({
  log: [
    {
      emit: 'event',
      level: 'query',
    },
  ],
});

prisma.$on('query', (e) => {
  console.log('Query: ' + e.query);
  console.log('Duration: ' + e.duration + 'ms');
});
```

---

## 7. API Debugging

### cURL
```bash
# Basic request
curl https://api.example.com/users

# With headers
curl -H "Authorization: Bearer token123" \
     https://api.example.com/users

# POST with JSON
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com"}' \
     https://api.example.com/users

# Verbose output
curl -v https://api.example.com/users

# Save response
curl https://api.example.com/users > response.json
```

### Postman/Insomnia
```markdown
## API Debugging Workflow

1. **Create Collection**: Organize related requests
2. **Environment Variables**: Store API URL, tokens
3. **Pre-request Scripts**: Generate auth tokens
4. **Tests**: Validate responses
5. **Mock Server**: Test without backend
```

### HTTP Debugging Proxy
```bash
# Charles Proxy / Fiddler
# - Intercept all HTTP traffic
# - Modify requests/responses
# - Simulate slow network
# - Breakpoint on requests
```

---

## 8. Production Debugging

### Logging Best Practices
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'user-service' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Structured logging
logger.info('User login', {
  userId: user.id,
  email: user.email,
  ip: req.ip,
  timestamp: new Date(),
});

// Error logging with context
try {
  await processPayment(order);
} catch (error) {
  logger.error('Payment failed', {
    error: error.message,
    stack: error.stack,
    orderId: order.id,
    userId: order.userId,
    amount: order.total,
  });
  throw error;
}
```

### Error Tracking (Sentry)
```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
});

// Capture exception with context
try {
  await processOrder(order);
} catch (error) {
  Sentry.captureException(error, {
    tags: {
      orderId: order.id,
      userId: order.userId,
    },
    extra: {
      orderData: order,
    },
  });
}

// Breadcrumbs
Sentry.addBreadcrumb({
  category: 'order',
  message: 'Order validation started',
  level: 'info',
});
```

---

## 9. Performance Debugging

### Chrome Performance Tab
```markdown
## Performance Profiling

1. Open DevTools → Performance tab
2. Click Record
3. Perform slow action
4. Stop recording
5. Analyze:
   - Long tasks (> 50ms)
   - Layout thrashing
   - Excessive re-renders
   - Memory leaks
```

### Node.js Profiling
```bash
# CPU profiling
node --prof src/index.js

# Generate report
node --prof-process isolate-0x*.log > profile.txt

# Memory profiling
node --inspect src/index.js
# Open Chrome DevTools
# Take heap snapshot
# Compare snapshots to find leaks
```

### Lighthouse
```bash
# Install
npm install -g lighthouse

# Run audit
lighthouse https://example.com --view

# CI integration
lighthouse https://example.com --output=json --output-path=./report.json
```

---

## 10. Debugging Checklist

```markdown
# Debugging Checklist

## Before You Start
- [ ] Can you reproduce the bug consistently?
- [ ] What changed recently?
- [ ] Check error logs
- [ ] Check monitoring dashboards

## Investigation
- [ ] Read error message carefully
- [ ] Check stack trace
- [ ] Add logging around problem area
- [ ] Use debugger to step through code
- [ ] Check network requests
- [ ] Check database queries
- [ ] Verify environment variables
- [ ] Test in different environment

## Hypothesis Testing
- [ ] Form hypothesis about cause
- [ ] Design test to verify
- [ ] Run test
- [ ] Analyze results
- [ ] Repeat if needed

## After Fix
- [ ] Add test to prevent regression
- [ ] Update documentation
- [ ] Share learnings with team
- [ ] Consider monitoring/alerting
```

---

## 11. Common Debugging Scenarios

### Scenario 1: "It works on my machine"
```markdown
**Symptoms**: Works locally, fails in production

**Checklist**:
- [ ] Environment variables different?
- [ ] Node version different?
- [ ] Database data different?
- [ ] Network/firewall issues?
- [ ] Timezone differences?
- [ ] Case-sensitive file systems?
```

### Scenario 2: Intermittent Failures
```markdown
**Symptoms**: Bug appears randomly

**Checklist**:
- [ ] Race condition?
- [ ] Timing-dependent?
- [ ] Load-dependent?
- [ ] External service flakiness?
- [ ] Memory leak causing OOM?
```

### Scenario 3: Performance Degradation
```markdown
**Symptoms**: App getting slower over time

**Checklist**:
- [ ] Memory leak?
- [ ] Database query performance?
- [ ] Cache not working?
- [ ] Too many connections?
- [ ] Disk space full?
```

---

## 12. Debugging Tools Checklist

- [ ] **Browser DevTools**: Proficient with Console, Network, Debugger?
- [ ] **VS Code Debugger**: Launch configs set up?
- [ ] **Logging**: Structured logging implemented?
- [ ] **Error Tracking**: Sentry/similar configured?
- [ ] **API Testing**: Postman/Insomnia collections?
- [ ] **Database Tools**: Query debugging enabled?
- [ ] **Performance Tools**: Profiling tools available?
- [ ] **Production Access**: Can debug production safely?
- [ ] **Documentation**: Common issues documented?
- [ ] **Team Knowledge**: Debugging practices shared?

---

## Related Skills
- `45-developer-experience/dev-environment-setup`
- `45-developer-experience/hot-reload-fast-feedback`
- `40-system-resilience/observability`
