---
name: api-error-handling
description: Implement comprehensive API error handling with standardized error responses, logging, monitoring, and user-friendly messages. Use when building resilient APIs, debugging issues, or improving error reporting.
---

# API Error Handling

## Overview

Build robust error handling systems with standardized error responses, detailed logging, error categorization, and user-friendly error messages.

## When to Use

- Handling API errors consistently
- Debugging production issues
- Implementing error recovery strategies
- Monitoring error rates
- Providing meaningful error messages to clients
- Tracking error patterns

## Instructions

### 1. **Standardized Error Response Format**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input validation failed",
    "statusCode": 422,
    "requestId": "req_abc123xyz789",
    "timestamp": "2025-01-15T10:30:00Z",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "INVALID_EMAIL"
      },
      {
        "field": "age",
        "message": "Must be at least 18",
        "code": "VALUE_OUT_OF_RANGE"
      }
    ],
    "path": "/api/users",
    "method": "POST",
    "traceId": "trace_001"
  }
}
```

### 2. **Node.js Error Handling**

```javascript
const express = require('express');
const app = express();

// Error codes and mappings
const ERROR_CODES = {
  VALIDATION_ERROR: { status: 422, message: 'Validation failed' },
  NOT_FOUND: { status: 404, message: 'Resource not found' },
  UNAUTHORIZED: { status: 401, message: 'Authentication required' },
  FORBIDDEN: { status: 403, message: 'Access denied' },
  CONFLICT: { status: 409, message: 'Resource conflict' },
  RATE_LIMITED: { status: 429, message: 'Too many requests' },
  INTERNAL_ERROR: { status: 500, message: 'Internal server error' },
  SERVICE_UNAVAILABLE: { status: 503, message: 'Service unavailable' }
};

// Custom error class
class ApiError extends Error {
  constructor(code, message, statusCode = null, details = null) {
    super(message);
    this.code = code;
    this.statusCode = statusCode || ERROR_CODES[code]?.status || 500;
    this.details = details;
    this.timestamp = new Date().toISOString();
  }
}

// Global error handler middleware
app.use((err, req, res, next) => {
  const requestId = req.id || `req_${Date.now()}`;
  const traceId = req.traceId;

  // Log error
  logError(err, {
    requestId,
    traceId,
    method: req.method,
    path: req.path,
    query: req.query,
    userId: req.user?.id
  });

  // Handle different error types
  if (err instanceof ApiError) {
    return res.status(err.statusCode).json(formatErrorResponse(err, requestId, traceId));
  }

  if (err instanceof SyntaxError && 'body' in err) {
    const apiError = new ApiError('VALIDATION_ERROR', 'Invalid JSON', 400);
    return res.status(400).json(formatErrorResponse(apiError, requestId, traceId));
  }

  if (err.name === 'ValidationError') {
    const details = Object.keys(err.errors).map(field => ({
      field,
      message: err.errors[field].message,
      code: 'VALIDATION_FAILED'
    }));
    const apiError = new ApiError('VALIDATION_ERROR', 'Validation failed', 422, details);
    return res.status(422).json(formatErrorResponse(apiError, requestId, traceId));
  }

  if (err.name === 'CastError') {
    const apiError = new ApiError('NOT_FOUND', 'Invalid resource ID', 404);
    return res.status(404).json(formatErrorResponse(apiError, requestId, traceId));
  }

  // Unknown error
  const internalError = new ApiError('INTERNAL_ERROR', 'An unexpected error occurred', 500);
  res.status(500).json(formatErrorResponse(internalError, requestId, traceId));
});

// Error response formatter
function formatErrorResponse(error, requestId, traceId) {
  return {
    error: {
      code: error.code,
      message: error.message,
      statusCode: error.statusCode,
      requestId,
      timestamp: error.timestamp,
      ...(error.details && { details: error.details }),
      traceId
    }
  };
}

// Error logger
function logError(error, context) {
  const logData = {
    timestamp: new Date().toISOString(),
    errorCode: error.code,
    errorMessage: error.message,
    statusCode: error.statusCode,
    stack: error.stack,
    context
  };

  // Log to different levels based on severity
  if (error.statusCode >= 500) {
    console.error('[ERROR]', JSON.stringify(logData));
    // Send to error tracking service (Sentry, etc)
    trackError(logData);
  } else if (error.statusCode >= 400) {
    console.warn('[WARN]', JSON.stringify(logData));
  }
}

// Route with error handling
app.post('/api/users', async (req, res, next) => {
  try {
    const { email, firstName, lastName } = req.body;

    // Validation
    if (!email || !firstName || !lastName) {
      throw new ApiError(
        'VALIDATION_ERROR',
        'Missing required fields',
        422,
        [
          !email && { field: 'email', message: 'Email is required' },
          !firstName && { field: 'firstName', message: 'First name is required' },
          !lastName && { field: 'lastName', message: 'Last name is required' }
        ].filter(Boolean)
      );
    }

    // Check for conflicts
    const existing = await User.findOne({ email });
    if (existing) {
      throw new ApiError('CONFLICT', 'Email already exists', 409);
    }

    const user = await User.create({ email, firstName, lastName });
    res.status(201).json({ data: user });
  } catch (error) {
    next(error);
  }
});

// Async route wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/api/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    throw new ApiError('NOT_FOUND', 'User not found', 404);
  }

  res.json({ data: user });
}));

// Handle unhandled rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  trackError({ type: 'unhandledRejection', reason });
});
```

### 3. **Python Error Handling (Flask)**

```python
from flask import Flask, jsonify, request
from datetime import datetime
import logging
import traceback
from functools import wraps

app = Flask(__name__)
logger = logging.getLogger(__name__)

class APIError(Exception):
    def __init__(self, code, message, status_code=500, details=None):
        super().__init__()
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        self.timestamp = datetime.utcnow().isoformat()

ERROR_CODES = {
    'VALIDATION_ERROR': 422,
    'NOT_FOUND': 404,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'CONFLICT': 409,
    'INTERNAL_ERROR': 500
}

def format_error(error, request_id, trace_id):
    return {
        'error': {
            'code': error.code,
            'message': error.message,
            'statusCode': error.status_code,
            'requestId': request_id,
            'timestamp': error.timestamp,
            'traceId': trace_id,
            'details': error.details if error.details else None
        }
    }

@app.errorhandler(APIError)
def handle_api_error(error):
    request_id = request.headers.get('X-Request-ID', f'req_{int(datetime.utcnow().timestamp())}')
    trace_id = request.headers.get('X-Trace-ID')

    log_error(error, {
        'request_id': request_id,
        'trace_id': trace_id,
        'method': request.method,
        'path': request.path
    })

    response = jsonify(format_error(error, request_id, trace_id))
    return response, error.status_code

@app.errorhandler(400)
def handle_bad_request(error):
    request_id = f'req_{int(datetime.utcnow().timestamp())}'
    api_error = APIError('VALIDATION_ERROR', 'Invalid request', 400)
    return jsonify(format_error(api_error, request_id, None)), 400

@app.errorhandler(404)
def handle_not_found(error):
    request_id = f'req_{int(datetime.utcnow().timestamp())}'
    api_error = APIError('NOT_FOUND', 'Resource not found', 404)
    return jsonify(format_error(api_error, request_id, None)), 404

@app.errorhandler(500)
def handle_internal_error(error):
    request_id = f'req_{int(datetime.utcnow().timestamp())}'
    logger.error(f'Internal error: {error}', exc_info=True)
    api_error = APIError('INTERNAL_ERROR', 'Internal server error', 500)
    return jsonify(format_error(api_error, request_id, None)), 500

def log_error(error, context):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'code': error.code,
        'message': error.message,
        'status': error.status_code,
        'context': context
    }

    if error.status_code >= 500:
        logger.error(log_entry)
    elif error.status_code >= 400:
        logger.warning(log_entry)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        raise APIError('VALIDATION_ERROR', 'Request body required', 400)

    errors = []
    if not data.get('email'):
        errors.append({'field': 'email', 'message': 'Email is required'})
    if not data.get('firstName'):
        errors.append({'field': 'firstName', 'message': 'First name is required'})

    if errors:
        raise APIError('VALIDATION_ERROR', 'Validation failed', 422, errors)

    try:
        user = User.create(**data)
        return jsonify({'data': user.to_dict()}), 201
    except IntegrityError:
        raise APIError('CONFLICT', 'Email already exists', 409)

@app.route('/api/users/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIError('NOT_FOUND', 'User not found', 404)
    return jsonify({'data': user.to_dict()})
```

### 4. **Error Recovery Strategies**

```javascript
// Circuit breaker pattern
class CircuitBreaker {
  constructor(failureThreshold = 5, timeout = 60000) {
    this.failureCount = 0;
    this.failureThreshold = failureThreshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new ApiError('SERVICE_UNAVAILABLE', 'Circuit breaker is open', 503);
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}

// Retry with exponential backoff
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;

      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### 5. **Error Monitoring**

```javascript
// Sentry integration
const Sentry = require('@sentry/node');

Sentry.init({ dsn: process.env.SENTRY_DSN });

function trackError(errorData) {
  Sentry.captureException(new Error(errorData.errorMessage), {
    tags: {
      code: errorData.errorCode,
      status: errorData.statusCode
    },
    extra: errorData.context
  });
}

// Error rate monitoring
const errorMetrics = {
  total: 0,
  byCode: {},
  byStatus: {}
};

function recordError(error) {
  errorMetrics.total++;
  errorMetrics.byCode[error.code] = (errorMetrics.byCode[error.code] || 0) + 1;
  errorMetrics.byStatus[error.statusCode] = (errorMetrics.byStatus[error.statusCode] || 0) + 1;
}

app.get('/metrics/errors', (req, res) => {
  res.json(errorMetrics);
});
```

## Best Practices

### ✅ DO
- Use consistent error response format
- Include request ID for tracing
- Log with appropriate severity levels
- Provide actionable error messages
- Include error details for debugging
- Use standard HTTP status codes
- Implement error recovery strategies
- Monitor error rates
- Distinguish user vs server errors
- Handle all error types

### ❌ DON'T
- Expose stack traces to clients
- Return 200 for errors
- Ignore errors silently
- Log sensitive data
- Use vague error messages
- Mix error handling with business logic
- Retry all errors indefinitely
- Expose internal implementation details
- Return different formats for errors
