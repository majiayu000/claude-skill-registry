---
name: error-tracking
description: Implement error tracking with Sentry for automatic exception monitoring, release tracking, and performance issues. Use when setting up error monitoring, tracking bugs in production, or analyzing application stability.
---

# Error Tracking

## Overview

Set up comprehensive error tracking with Sentry to automatically capture, report, and analyze exceptions, performance issues, and application stability.

## When to Use

- Production error monitoring
- Automatic exception capture
- Release tracking
- Performance issue detection
- User impact analysis

## Instructions

### 1. **Sentry Setup**

```bash
npm install -g @sentry/cli
npm install @sentry/node @sentry/tracing
sentry init -d
```

### 2. **Node.js Sentry Integration**

```javascript
// sentry.js
const Sentry = require("@sentry/node");
const Tracing = require("@sentry/tracing");

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || 'development',
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
  release: process.env.APP_VERSION || '1.0.0',
  integrations: [
    new Sentry.Integrations.Http({ tracing: true }),
    new Tracing.Integrations.Express({
      app: true,
      request: true,
      transaction: true
    })
  ],
  ignoreErrors: [
    'Network request failed',
    'TimeoutError'
  ]
});

module.exports = Sentry;
```

### 3. **Express Middleware Integration**

```javascript
// app.js
const express = require('express');
const Sentry = require('./sentry');

const app = express();

app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

app.get('/api/users/:id', (req, res) => {
  const transaction = Sentry.startTransaction({
    name: 'get_user',
    op: 'http.server'
  });

  try {
    const userId = req.params.id;

    Sentry.captureMessage('Fetching user', {
      level: 'info',
      tags: { userId: userId }
    });

    const user = db.query(`SELECT * FROM users WHERE id = ${userId}`);

    if (!user) {
      Sentry.captureException(new Error('User not found'), {
        level: 'warning',
        contexts: { request: { userId } }
      });
      return res.status(404).json({ error: 'User not found' });
    }

    transaction.setTag('user.id', user.id);
    res.json(user);
  } catch (error) {
    Sentry.captureException(error, {
      level: 'error',
      tags: { endpoint: 'get_user', userId: req.params.id }
    });
    res.status(500).json({ error: 'Internal server error' });
  } finally {
    transaction.finish();
  }
});

app.use(Sentry.Handlers.errorHandler());

app.listen(3000);
```

### 4. **Python Sentry Integration**

```python
# sentry_config.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
import os

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration(), sentry_logging],
    environment=os.environ.get('ENVIRONMENT', 'development'),
    release=os.environ.get('APP_VERSION', '1.0.0'),
    traces_sample_rate=0.1 if os.environ.get('ENVIRONMENT') == 'production' else 1.0,
    attach_stacktrace=True
)

# Flask integration
from flask import Flask
import sentry_sdk

app = Flask(__name__)

@app.route('/api/orders/<order_id>')
def get_order(order_id):
    try:
        sentry_sdk.set_user({'id': request.user.id})
        sentry_sdk.capture_message(f'Fetching order {order_id}', level='info')

        order = db.query(f'SELECT * FROM orders WHERE id = {order_id}')

        if not order:
            sentry_sdk.capture_exception(ValueError('Order not found'))
            return {'error': 'Order not found'}, 404

        return {'order': order}

    except Exception as e:
        sentry_sdk.capture_exception(e, {
            'tags': { 'endpoint': 'get_order', 'order_id': order_id }
        })
        return {'error': 'Internal server error'}, 500
```

### 5. **Source Maps and Release Management**

```javascript
// webpack.config.js
const SentryCliPlugin = require('@sentry/webpack-plugin');

module.exports = {
  plugins: [
    new SentryCliPlugin({
      include: './dist',
      urlPrefix: 'https://example.com/',
      release: process.env.APP_VERSION || '1.0.0',
      org: process.env.SENTRY_ORG,
      project: process.env.SENTRY_PROJECT,
      authToken: process.env.SENTRY_AUTH_TOKEN
    })
  ]
};
```

### 6. **CI/CD Release Creation**

```bash
#!/bin/bash
VERSION=$(cat package.json | grep version | head -1 | awk -F: '{ print $2 }' | sed 's/[",]//g')

# Create release
sentry-cli releases -o my-org -p my-project create $VERSION

# Upload source maps
sentry-cli releases -o my-org -p my-project files $VERSION upload-sourcemaps ./dist

# Finalize release
sentry-cli releases -o my-org -p my-project finalize $VERSION

# Deploy
sentry-cli releases -o my-org -p my-project deploys $VERSION new -e production
```

### 7. **Custom Error Context**

```javascript
// custom-error-context.js
const Sentry = require('@sentry/node');

Sentry.configureScope(scope => {
  scope.setUser({
    id: userId,
    email: userEmail,
    subscription: 'pro'
  });

  scope.setTag('feature_flag', 'new-ui');
  scope.setTag('database', 'postgres-v12');

  scope.setContext('character', {
    name: 'Mighty Fighter',
    level: 19
  });

  scope.addBreadcrumb({
    category: 'ui.click',
    message: 'User clicked signup button',
    level: 'info'
  });

  scope.addBreadcrumb({
    category: 'database',
    message: 'Query executed',
    level: 'debug',
    data: {
      query: 'SELECT * FROM users',
      duration: 125
    }
  });
});

// Before sending
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  beforeSend(event, hint) {
    if (event.request) {
      delete event.request.cookies;
      delete event.request.headers['authorization'];
    }
    return event;
  }
});
```

### 8. **Performance Monitoring**

```javascript
// performance.js
const Sentry = require('@sentry/node');

const transaction = Sentry.startTransaction({
  name: 'process_order',
  op: 'task',
  data: { orderId: '12345' }
});

const dbSpan = transaction.startChild({
  op: 'db',
  description: 'Save order to database'
});
saveOrderToDb(order);
dbSpan.finish();

const paymentSpan = transaction.startChild({
  op: 'http.client',
  description: 'Process payment'
});
processPayment(order);
paymentSpan.finish();

transaction.setStatus('ok');
transaction.finish();
```

## Best Practices

### ✅ DO
- Set up source maps for production
- Configure appropriate sample rates
- Track releases and deployments
- Filter sensitive information
- Add meaningful context to errors
- Use breadcrumbs for debugging
- Set user information
- Review error patterns regularly

### ❌ DON'T
- Send 100% of errors in production
- Include passwords in context
- Ignore configuration for environment
- Skip source map uploads
- Log personally identifiable information
- Use without proper filtering
- Disable tracking in production

## Key Commands

```bash
sentry-cli releases create $VERSION
sentry-cli releases files upload-sourcemaps $VERSION ./dist
sentry-cli releases deploys $VERSION new -e production
sentry-cli releases finalize $VERSION
sentry-cli releases info $VERSION
```
