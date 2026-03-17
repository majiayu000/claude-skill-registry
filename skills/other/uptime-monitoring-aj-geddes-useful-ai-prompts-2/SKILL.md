---
name: uptime-monitoring
description: Implement uptime monitoring and status page systems for tracking service availability. Use when monitoring application uptime, creating status pages, or implementing health checks.
---

# Uptime Monitoring

## Overview

Set up comprehensive uptime monitoring with health checks, status pages, and incident tracking to ensure visibility into service availability.

## When to Use

- Service availability tracking
- Health check implementation
- Status page creation
- Incident management
- SLA monitoring

## Instructions

### 1. **Health Check Endpoints**

```javascript
// Node.js health check
const express = require('express');
const app = express();

app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

app.get('/health/deep', async (req, res) => {
  const health = {
    status: 'ok',
    checks: {
      database: 'unknown',
      cache: 'unknown',
      externalApi: 'unknown'
    }
  };

  try {
    const dbResult = await db.query('SELECT 1');
    health.checks.database = dbResult ? 'ok' : 'error';
  } catch {
    health.checks.database = 'error';
    health.status = 'degraded';
  }

  try {
    const cacheResult = await redis.ping();
    health.checks.cache = cacheResult === 'PONG' ? 'ok' : 'error';
  } catch {
    health.checks.cache = 'error';
  }

  try {
    const response = await fetch('https://api.example.com/health');
    health.checks.externalApi = response.ok ? 'ok' : 'error';
  } catch {
    health.checks.externalApi = 'error';
  }

  const statusCode = health.status === 'ok' ? 200 : 503;
  res.status(statusCode).json(health);
});

app.get('/readiness', async (req, res) => {
  try {
    const dbCheck = await db.query('SELECT 1');
    const cacheCheck = await redis.ping();

    if (dbCheck && cacheCheck === 'PONG') {
      res.json({ ready: true });
    } else {
      res.status(503).json({ ready: false });
    }
  } catch {
    res.status(503).json({ ready: false });
  }
});

app.get('/liveness', (req, res) => {
  res.json({ alive: true });
});
```

### 2. **Python Health Checks**

```python
from flask import Flask, jsonify
import time

app = Flask(__name__)
startup_time = time.time()

def get_uptime():
    return int(time.time() - startup_time)

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'uptime_seconds': get_uptime()
    }), 200

@app.route('/health/deep')
def health_deep():
    health_status = {
        'status': 'ok',
        'checks': {
            'database': 'unknown',
            'cache': 'unknown'
        }
    }

    try:
        db.session.execute('SELECT 1')
        health_status['checks']['database'] = 'ok'
    except:
        health_status['checks']['database'] = 'error'
        health_status['status'] = 'degraded'

    try:
        cache.get('_health')
        health_status['checks']['cache'] = 'ok'
    except:
        health_status['checks']['cache'] = 'error'

    status_code = 200 if health_status['status'] == 'ok' else 503
    return jsonify(health_status), status_code

@app.route('/readiness')
def readiness():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'ready': True}), 200
    except:
        return jsonify({'ready': False}), 503
```

### 3. **Uptime Monitor with Heartbeat**

```javascript
// heartbeat.js
const axios = require('axios');

class UptimeMonitor {
  constructor(config = {}) {
    this.checkInterval = config.checkInterval || 60000;
    this.timeout = config.timeout || 5000;
    this.endpoints = config.endpoints || [];
  }

  async checkEndpoint(endpoint) {
    const startTime = Date.now();

    try {
      const response = await axios.get(endpoint.url, {
        timeout: this.timeout,
        validateStatus: (s) => s >= 200 && s < 300
      });

      const check = {
        endpoint: endpoint.name,
        status: 'up',
        responseTime: Date.now() - startTime,
        timestamp: new Date()
      };

      await this.saveCheck(check);
      return check;
    } catch (error) {
      const check = {
        endpoint: endpoint.name,
        status: 'down',
        responseTime: Date.now() - startTime,
        timestamp: new Date(),
        error: error.message
      };

      await this.saveCheck(check);
      return check;
    }
  }

  async saveCheck(check) {
    try {
      await db.query(
        'INSERT INTO uptime_checks (endpoint, status, response_time, timestamp) VALUES (?, ?, ?, ?)',
        [check.endpoint, check.status, check.responseTime, check.timestamp]
      );
    } catch (error) {
      console.error('Failed to save check:', error);
    }
  }

  async runChecks() {
    return Promise.all(
      this.endpoints.map(e => this.checkEndpoint(e))
    );
  }

  start() {
    this.runChecks();
    this.interval = setInterval(() => this.runChecks(), this.checkInterval);
  }

  stop() {
    if (this.interval) clearInterval(this.interval);
  }

  async getStats(endpoint, hours = 24) {
    const [stats] = await db.query(`
      SELECT
        COUNT(*) as total_checks,
        SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) as uptime_checks,
        AVG(response_time) as avg_response_time
      FROM uptime_checks
      WHERE endpoint = ? AND timestamp > DATE_SUB(NOW(), INTERVAL ? HOUR)
    `, [endpoint, hours]);
    return stats[0];
  }
}

module.exports = UptimeMonitor;
```

### 4. **Public Status Page API**

```javascript
// status-page-api.js
const express = require('express');
const router = express.Router();

router.get('/api/status', async (req, res) => {
  try {
    const endpoints = await db.query(`
      SELECT DISTINCT endpoint FROM uptime_checks
    `);

    const status = {
      page: { name: 'My Service Status', updated_at: new Date().toISOString() },
      components: []
    };

    for (const { endpoint } of endpoints) {
      const [lastCheck] = await db.query(`
        SELECT status FROM uptime_checks
        WHERE endpoint = ? ORDER BY timestamp DESC LIMIT 1
      `, [endpoint]);

      status.components.push({
        id: endpoint,
        name: endpoint,
        status: lastCheck?.status === 'up' ? 'operational' : 'major_outage'
      });
    }

    const allUp = status.components.every(c => c.status === 'operational');
    status.status = {
      overall: allUp ? 'all_operational' : 'major_outage'
    };

    res.json(status);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch status' });
  }
});

router.get('/api/status/uptime/:endpoint', async (req, res) => {
  try {
    const stats = await db.query(`
      SELECT
        DATE(timestamp) as date,
        COUNT(*) as total,
        SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) as uptime
      FROM uptime_checks
      WHERE endpoint = ? AND timestamp > DATE_SUB(NOW(), INTERVAL 30 DAY)
      GROUP BY DATE(timestamp)
      ORDER BY date DESC
    `, [req.params.endpoint]);

    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch statistics' });
  }
});

module.exports = router;
```

### 5. **Kubernetes Health Probes**

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: api-service
        image: api-service:latest

        startupProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 0
          periodSeconds: 10
          failureThreshold: 30

        readinessProbe:
          httpGet:
            path: /readiness
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3

        livenessProbe:
          httpGet:
            path: /liveness
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
```

## Best Practices

### ✅ DO
- Implement comprehensive health checks
- Check all critical dependencies
- Use appropriate timeout values
- Track response times
- Store check history
- Monitor uptime trends
- Alert on status changes
- Use standard HTTP status codes

### ❌ DON'T
- Check only application process
- Ignore external dependencies
- Set timeouts too low
- Alert on every failure
- Use health checks for load balancing
- Expose sensitive information

## SLA Compliance Calculation

```javascript
function calculateSLA(upChecks, totalChecks) {
  const uptime = (upChecks / totalChecks) * 100;
  return {
    uptime_percentage: uptime.toFixed(4),
    meets_99_9: uptime >= 99.9,
    meets_99_99: uptime >= 99.99
  };
}
```
