# 📊 Error Analytics Skill

---
name: error-analytics
description: Analyze error patterns, identify root causes, and provide systematic solutions
---

## 🎯 Purpose

วิเคราะห์ error patterns, หา root causes, และเสนอ systematic solutions เพื่อลด recurring errors

## 📋 When to Use

- เจอ errors ซ้ำๆ
- ต้องการเข้าใจ error patterns
- Reduce error rate
- Improve error handling
- Debug production issues

## 🔧 Analysis Dimensions

### 1. Error Classification
| Category | Examples |
|----------|----------|
| **Syntax** | SyntaxError, TSError |
| **Runtime** | TypeError, ReferenceError |
| **Logic** | Wrong output, infinite loops |
| **Network** | Timeout, CORS, 404/500 |
| **Resource** | Memory, disk, connection |

### 2. Error Frequency
```
High Frequency (daily)     → Fix immediately
Medium Frequency (weekly)  → Plan fix
Low Frequency (monthly)    → Monitor
```

### 3. Error Impact
```
Critical (app crash)       → Highest priority
Major (feature broken)     → High priority
Minor (cosmetic issue)     → Low priority
```

## 📊 Error Pattern Analysis

### Common Patterns

#### Null Reference Errors
```javascript
// Pattern: Accessing property of null/undefined
TypeError: Cannot read property 'x' of undefined

// Analysis: Missing null checks
// Occurrences: 45 times in last week
// Location: UserProfile.tsx, OrderPage.tsx

// Solution: Add optional chaining
const value = obj?.property ?? default;
```

#### Async/Await Errors
```javascript
// Pattern: Unhandled promise rejection
UnhandledPromiseRejection: ...

// Analysis: Missing try-catch or .catch()
// Occurrences: 23 times

// Solution: Wrap in try-catch
try {
  await asyncOperation();
} catch (error) {
  handleError(error);
}
```

#### API Errors
```javascript
// Pattern: Network failures
Error: Network request failed

// Analysis: 
// - 30% timeout (> 30s response)
// - 50% server errors (500)
// - 20% client errors (400)

// Solutions:
// - Add retry logic
// - Implement circuit breaker
// - Add request timeout
```

## 📝 Analysis Process

```
1. COLLECT error data
   - Error messages
   - Stack traces
   - Frequency
   - Timestamps

2. CATEGORIZE errors
   - By type
   - By location
   - By severity

3. IDENTIFY patterns
   - Common root causes
   - Related errors
   - Trigger conditions

4. ANALYZE root cause
   - Why does it happen?
   - What triggers it?
   - Who does it affect?

5. PROPOSE solutions
   - Quick fixes
   - Long-term solutions
   - Prevention strategies

6. TRACK results
   - Error rate before/after
   - Recurrence
   - Side effects
```

## 📋 Error Analysis Report Template

```markdown
## 📊 Error Analysis Report

### Period: {date range}
### Total Errors: {count}

---

### 🔴 Critical Errors

#### Error: {error message}
- **Occurrences**: {count}
- **Files affected**: {list}
- **Root cause**: {analysis}
- **Solution**: {proposed fix}
- **Priority**: Critical

---

### 📈 Error Trends

| Error Type | Last Week | This Week | Trend |
|------------|-----------|-----------|-------|
| TypeError | 45 | 12 | ⬇️ -73% |
| NetworkError | 30 | 35 | ⬆️ +17% |
| SyntaxError | 5 | 0 | ⬇️ -100% |

### 🎯 Top Recommendations

1. Add global error boundary
2. Implement retry logic for API calls
3. Add input validation on forms
```

## 🔧 Error Monitoring Setup

### Sentry
```javascript
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: 'your-dsn',
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});

// Capture errors
Sentry.captureException(error);
```

### Custom Error Tracking
```javascript
class ErrorTracker {
  private errors: ErrorLog[] = [];

  log(error: Error, context: object) {
    this.errors.push({
      message: error.message,
      stack: error.stack,
      context,
      timestamp: new Date(),
    });
    this.analyze();
  }

  analyze() {
    const grouped = groupBy(this.errors, 'message');
    const frequent = Object.entries(grouped)
      .filter(([, errors]) => errors.length > 5)
      .map(([message, errors]) => ({
        message,
        count: errors.length,
        lastOccurred: errors[errors.length - 1].timestamp,
      }));
    return frequent;
  }
}
```

## 📊 Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Error Rate | Errors per 1000 requests | < 1% |
| MTTR | Mean time to resolve | < 4 hours |
| Recurrence | Same error repeating | 0% |
| Coverage | Errors with handling | 100% |

## ✅ Error Prevention Checklist

- [ ] Input validation on all forms
- [ ] Null checks on data access
- [ ] Error boundaries in React
- [ ] Try-catch on async operations
- [ ] Timeout on network requests
- [ ] Logging for debugging
- [ ] User-friendly error messages
- [ ] Fallback UI for errors

## 🔗 Related Skills

- `debugging` - Debug specific errors
- `auto-debug` - Auto-fix errors
- `logging` - Error logging
- `testing` - Prevent errors
