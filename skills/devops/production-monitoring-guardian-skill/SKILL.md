---
name: production-monitoring-guardian
description: Prevents production blind spots by establishing comprehensive monitoring, alerting, and observability. Use when deploying to production, experiencing unexplained downtime, debugging performance issues, or setting up incident response. Covers error tracking (Sentry), uptime monitoring (UptimeRobot), performance monitoring (APM), log aggregation, alerting strategies, and dashboard design.
---

# Production Monitoring Guardian

**Mission:** Ensure you know what's happening in production BEFORE your users do. Establish proactive monitoring that catches issues early, enables fast debugging, and prevents revenue loss.

## Activation Triggers

- Deploying to production for the first time
- "How do I know if my app is down?"
- Performance degradation reports
- Unexplained errors or downtime
- Capacity planning needs
- Incident response preparation
- SLA/uptime requirements
- Customer reports issues before you

## The Four Pillars of Observability

1. **Metrics** - What's happening? (CPU, memory, request rate, error rate)
2. **Logs** - Why is it happening? (Error messages, stack traces, context)
3. **Traces** - Where is it happening? (Request flow through system)
4. **Alerts** - When should I act? (Thresholds, escalation policies)

## Scan Methodology

### 1. Initial Context Gathering

**Ask if not provided:**
- "Is your application in production?"
- "What's your current monitoring setup?" (none, partial, comprehensive)
- "What's your uptime requirement?" (99%, 99.9%, 99.99%)
- "How do you currently know if something breaks?"
- "What's your incident response process?"

### 2. Monitoring Maturity Assessment

**Level 0: Blind** 🔴 **CRITICAL RISK**
- No monitoring
- Users report outages
- No error tracking
- No performance visibility
- **Risk**: Revenue loss, customer churn, reputation damage

**Level 1: Basic** 🟡 **HIGH RISK**
- Simple uptime checks (ping endpoints)
- Basic server metrics (CPU, memory)
- Manual log checking
- **Risk**: Delayed incident response, no root cause analysis

**Level 2: Operational** 🟢 **ACCEPTABLE**
- Error tracking (Sentry)
- Uptime monitoring (UptimeRobot)
- Log aggregation
- Basic alerting
- **Risk**: Minimal, can operate safely

**Level 3: Advanced** ⭐ **OPTIMAL**
- Full observability (metrics + logs + traces)
- Proactive alerting
- Performance monitoring (APM)
- Auto-scaling based on metrics
- Dashboards for all stakeholders
- **Risk**: Very low, enterprise-grade

**PDFLab Current State**: Level 0-1 (Production deployed, monitoring incomplete)

### 3. Critical Monitoring Components

#### 🔴 CRITICAL: Error Tracking (Sentry)

**Why Essential:**
- Catches errors before users report them
- Provides stack traces and context
- Tracks error frequency and impact
- Enables quick debugging

**Setup for PDFLab:**

```bash
# Install Sentry
cd backend
npm install @sentry/node @sentry/profiling-node

cd ..
npm install @sentry/nextjs
```

**Backend Integration (Express.js):**
```typescript
// backend/src/server.ts
import * as Sentry from '@sentry/node'
import { ProfilingIntegration } from '@sentry/profiling-node'

// Initialize Sentry FIRST (before any other imports)
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || 'development',
  integrations: [
    new ProfilingIntegration(),
    new Sentry.Integrations.Http({ tracing: true }),
    new Sentry.Integrations.Express({ app })
  ],
  tracesSampleRate: 0.1, // 10% of transactions
  profilesSampleRate: 0.1,

  // Filter sensitive data
  beforeSend(event) {
    // Remove passwords from error data
    if (event.request) {
      delete event.request.cookies
      if (event.request.data?.password) {
        event.request.data.password = '[REDACTED]'
      }
    }
    return event
  }
})

// Sentry request handler (BEFORE routes)
app.use(Sentry.Handlers.requestHandler())
app.use(Sentry.Handlers.tracingHandler())

// ... your routes ...

// Sentry error handler (AFTER routes, BEFORE other error handlers)
app.use(Sentry.Handlers.errorHandler())

// Custom error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // Sentry already captured error
  console.error('Unhandled error:', err)

  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong',
    sentry_id: res.sentry // Error ID for support tickets
  })
})
```

**Frontend Integration (Next.js):**
```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,

  // Filter PII
  beforeSend(event, hint) {
    // Don't send auth tokens
    if (event.request?.headers) {
      delete event.request.headers.authorization
    }
    return event
  }
})

// Usage in components:
try {
  await pdflabAPI.uploadBatch(files, operation, options)
} catch (error) {
  Sentry.captureException(error, {
    tags: {
      feature: 'batch_upload',
      operation: operation
    },
    extra: {
      file_count: files.length,
      total_size: files.reduce((sum, f) => sum + f.size, 0)
    }
  })
  throw error
}
```

**Environment Variables:**
```bash
# .env (backend)
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# .env.local (frontend)
NEXT_PUBLIC_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
```

**Verification:**
```typescript
// Test Sentry integration
app.get('/debug-sentry', (req, res) => {
  throw new Error('Test Sentry error tracking')
})

// Visit http://localhost:3006/debug-sentry
// Check Sentry dashboard for error
```

#### 🔴 CRITICAL: Uptime Monitoring (UptimeRobot)

**Why Essential:**
- Detects when site is down
- Monitors from external location (not your server)
- Alerts via SMS/email/Slack
- Tracks uptime percentage for SLAs

**Setup (5 minutes, FREE):**

1. **Create UptimeRobot Account**
   - Go to https://uptimerobot.com
   - Free tier: 50 monitors, 5-minute intervals

2. **Add HTTP Monitor**
   ```
   Monitor Type: HTTP(s)
   Friendly Name: PDFLab Production
   URL: https://pdflab.pro
   Monitoring Interval: 5 minutes (free tier)

   Advanced:
   - Check for keyword: "PDFLab" (ensures page loads correctly)
   - Timeout: 30 seconds
   ```

3. **Add Health Check Endpoint Monitor**
   ```
   Monitor Type: HTTP(s)
   Friendly Name: PDFLab API Health
   URL: https://pdflab.pro/health
   Monitoring Interval: 5 minutes
   Expected Status: 200

   POST-Value (for detailed check):
   Check for JSON: "status":"healthy"
   ```

4. **Configure Alerts**
   ```
   Email: your@email.com
   SMS: +1-xxx-xxx-xxxx (optional, paid)
   Slack: webhook URL (recommended)

   Alert When:
   - Down (site unreachable)
   - Up (site back online)
   - Slow response (>5s)
   ```

5. **Test Alerts**
   ```bash
   # Stop backend to trigger alert
   docker stop pdflab-backend

   # Wait 5-10 minutes for UptimeRobot to detect
   # Verify you receive alert

   # Restart backend
   docker start pdflab-backend

   # Verify "Up" alert
   ```

**Advanced Health Checks:**
```typescript
// backend/src/server.ts
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks: {
      database: 'unknown',
      redis: 'unknown',
      cloudconvert: 'unknown'
    }
  }

  try {
    // Check database
    await sequelize.authenticate()
    health.checks.database = 'healthy'
  } catch {
    health.checks.database = 'unhealthy'
    health.status = 'degraded'
  }

  try {
    // Check Redis
    await redisClient.ping()
    health.checks.redis = 'healthy'
  } catch {
    health.checks.redis = 'unhealthy'
    health.status = 'degraded'
  }

  const statusCode = health.status === 'healthy' ? 200 : 503
  res.status(statusCode).json(health)
})
```

#### 🟡 HIGH: Log Aggregation

**Why Important:**
- Centralized log viewing
- Search across all servers
- Correlate logs with errors
- Compliance/audit requirements

**Simple Pattern (File-based):**
```typescript
// backend/src/utils/logger.ts
import winston from 'winston'

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    // Console (for Docker logs)
    new winston.transports.Console({
      format: winston.format.simple()
    }),

    // File (for persistence)
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: 'logs/combined.log'
    })
  ]
})

export default logger

// Usage:
logger.info('Batch processing started', {
  batch_id: batchId,
  user_id: userId,
  file_count: files.length
})

logger.error('Conversion failed', {
  batch_id: batchId,
  error: error.message,
  stack: error.stack
})
```

**Structured Logging Pattern:**
```typescript
// Always log with context
logger.info('Event description', {
  // Standard fields
  user_id: req.user?.id,
  request_id: req.id,
  ip_address: req.ip,

  // Event-specific fields
  batch_id: batchId,
  operation: 'batch_upload',
  file_count: 5,

  // Metrics
  duration_ms: Date.now() - startTime,
  success: true
})
```

**Log Levels:**
- `error` - Something failed, needs attention
- `warn` - Something suspicious, might need attention
- `info` - Normal operation, important events
- `http` - HTTP request/response (verbose)
- `debug` - Detailed debugging info (development only)

#### 🟡 HIGH: Performance Monitoring (APM)

**Why Important:**
- Identify slow endpoints
- Database query optimization
- Memory leak detection
- Capacity planning

**Simple APM (Built-in Node.js):**
```typescript
// backend/src/middleware/performance.middleware.ts
export const performanceMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const start = Date.now()

  // Capture response finish
  res.on('finish', () => {
    const duration = Date.now() - start

    // Log slow requests
    if (duration > 1000) {
      logger.warn('Slow request', {
        method: req.method,
        url: req.url,
        duration_ms: duration,
        status: res.statusCode
      })
    }

    // Track metrics
    metrics.histogram('http.request.duration', duration, {
      method: req.method,
      route: req.route?.path,
      status: res.statusCode
    })
  })

  next()
}

app.use(performanceMiddleware)
```

**Database Query Monitoring:**
```typescript
// backend/src/config/database.ts
export const sequelize = new Sequelize({
  // ... other config ...

  logging: (sql, timing) => {
    if (timing && timing > 100) {
      logger.warn('Slow query', {
        sql,
        duration_ms: timing
      })
    }
  },

  benchmark: true // Enable timing
})
```

#### 🟠 MEDIUM: Application Metrics

**Key Metrics to Track:**

```typescript
// backend/src/utils/metrics.ts
class Metrics {
  private metrics = new Map<string, number>()

  increment(name: string, tags: Record<string, string> = {}) {
    const key = `${name}:${JSON.stringify(tags)}`
    this.metrics.set(key, (this.metrics.get(key) || 0) + 1)
  }

  gauge(name: string, value: number, tags: Record<string, string> = {}) {
    const key = `${name}:${JSON.stringify(tags)}`
    this.metrics.set(key, value)
  }

  // Export for monitoring systems
  getAll() {
    return Object.fromEntries(this.metrics)
  }
}

export const metrics = new Metrics()

// Usage throughout application:

// Conversion job started
metrics.increment('conversion.job.started', {
  type: 'pdf_to_pptx',
  user_plan: user.plan
})

// Conversion job completed
metrics.increment('conversion.job.completed', {
  type: 'pdf_to_pptx'
})

// Conversion job failed
metrics.increment('conversion.job.failed', {
  type: 'pdf_to_pptx',
  error_type: 'cloudconvert_timeout'
})

// Active users
metrics.gauge('users.active', await getActiveUserCount())

// Queue depth
metrics.gauge('queue.depth', await conversionQueue.count())
```

**Metrics Endpoint:**
```typescript
// Expose metrics for Prometheus/monitoring
app.get('/metrics', (req, res) => {
  res.json({
    timestamp: new Date().toISOString(),
    metrics: metrics.getAll(),
    system: {
      memory: process.memoryUsage(),
      uptime: process.uptime(),
      cpu: process.cpuUsage()
    }
  })
})
```

### 4. Alerting Strategy

**Alert Fatigue Prevention:**
- Don't alert on everything
- Use severity levels (P1=critical, P2=high, P3=medium, P4=low)
- Escalate if not acknowledged
- Group related alerts

**Critical Alerts (Wake up at 3am):**
- Site down (5+ minute outage)
- Database unreachable
- Error rate >10%
- Payment processing failed
- Disk usage >90%

**High Priority Alerts (Check within 1 hour):**
- Error rate >5%
- Slow response times (P95 >5s)
- Queue backing up (>100 jobs pending)
- CloudConvert API errors

**Medium Priority Alerts (Check during business hours):**
- Warning logs increasing
- Memory usage trending up
- Unusual traffic patterns

**Alert Channels:**
```
Critical (P1):
  → SMS to on-call engineer
  → Slack #incidents channel
  → PagerDuty escalation

High (P2):
  → Slack #alerts channel
  → Email to team

Medium (P3):
  → Slack #monitoring channel
  → Daily digest email
```

### 5. Dashboard Design

**Essential Dashboards:**

**1. Service Health Dashboard (Operations)**
```
┌─────────────────────────────────────┐
│  PDFLab Production Status           │
├─────────────────────────────────────┤
│  Uptime (24h):      99.95% ✅       │
│  Error Rate (1h):   0.2%   ✅       │
│  Avg Response:      245ms  ✅       │
│  Active Users:      127             │
│  Conversion Queue:  3 jobs          │
│                                     │
│  Component Status:                  │
│  • Frontend:        ✅ Healthy      │
│  • Backend API:     ✅ Healthy      │
│  • Database:        ✅ Healthy      │
│  • Redis:           ✅ Healthy      │
│  • CloudConvert:    ⚠️  Slow (3s)   │
└─────────────────────────────────────┘
```

**2. Business Metrics Dashboard (Executives)**
```
┌─────────────────────────────────────┐
│  PDFLab Business Metrics            │
├─────────────────────────────────────┤
│  Today:                             │
│  • Conversions:     342  (+12%)     │
│  • New Users:       23   (+5%)      │
│  • Revenue:         $156 (+8%)      │
│                                     │
│  This Month:                        │
│  • MRR:             $1,247          │
│  • Active Users:    892             │
│  • Churn Rate:      3.2%            │
│                                     │
│  Popular Features:                  │
│  1. PDF → PPTX      45%             │
│  2. PDF → DOCX      32%             │
│  3. PDF Compress    18%             │
└─────────────────────────────────────┘
```

**3. Performance Dashboard (Developers)**
```
┌─────────────────────────────────────┐
│  API Performance                    │
├─────────────────────────────────────┤
│  Request Duration (P95):            │
│  /api/upload        423ms  ⚠️       │
│  /api/status        87ms   ✅       │
│  /api/download      1.2s   ❌       │
│                                     │
│  Database Queries (P95):            │
│  Users.findByPk     12ms   ✅       │
│  Jobs.findAll       156ms  ⚠️       │
│                                     │
│  Memory Usage:                      │
│  Heap Used:         324MB  ✅       │
│  Heap Total:        512MB           │
│  RSS:               478MB  ✅       │
└─────────────────────────────────────┘
```

### 6. Incident Response Playbook

**When Alert Fires:**

1. **Acknowledge** (1 minute)
   - Click "Acknowledge" in PagerDuty/Slack
   - Prevents escalation

2. **Assess** (5 minutes)
   - Check Sentry for recent errors
   - Check UptimeRobot for uptime status
   - Check server metrics (CPU, memory, disk)
   - Check logs for patterns

3. **Mitigate** (15 minutes)
   - If site down: restart services
   - If database down: check connections, restart MySQL
   - If queue backed up: add workers or pause intake
   - If CloudConvert down: show maintenance message

4. **Communicate** (ongoing)
   - Update status page
   - Notify affected users
   - Internal Slack updates

5. **Resolve** (variable)
   - Fix root cause
   - Verify fix in production
   - Monitor for recurrence

6. **Post-Mortem** (24 hours later)
   - Document what happened
   - Identify root cause
   - Create prevention tasks
   - Share learnings

## Production Monitoring Checklist

### Essential (Deploy with these)
- [ ] Sentry error tracking configured
- [ ] UptimeRobot monitoring pdflab.pro
- [ ] Health check endpoint (`/health`)
- [ ] Structured logging with Winston
- [ ] Alert for site down (email/SMS)

### Important (Add within first month)
- [ ] Performance monitoring (slow requests logged)
- [ ] Database query monitoring
- [ ] Business metrics tracking
- [ ] Dashboard for operations team
- [ ] Incident response playbook documented

### Advanced (Add as you scale)
- [ ] Distributed tracing (Sentry Traces)
- [ ] Custom metrics (conversion rates, revenue)
- [ ] Auto-scaling based on metrics
- [ ] Anomaly detection (ML-based alerting)
- [ ] Real user monitoring (RUM)

## Quick Setup (30 minutes)

```bash
# 1. Sentry (10 min)
npm install @sentry/node @sentry/nextjs
# Add initialization code (see above)
# Test with /debug-sentry endpoint

# 2. UptimeRobot (5 min)
# Sign up at https://uptimerobot.com
# Add pdflab.pro monitor
# Configure email alerts

# 3. Health Check (5 min)
# Add /health endpoint (see above)
# Test: curl https://pdflab.pro/health

# 4. Logging (10 min)
npm install winston
# Add structured logging (see above)
# Verify logs: tail -f logs/combined.log
```

## Key Principles

1. **Monitor user-facing metrics** - Uptime, error rate, performance
2. **Alert on symptoms, not causes** - "Site down" not "CPU high"
3. **Make alerts actionable** - Include fix suggestions
4. **Prevent alert fatigue** - Only critical alerts wake people up
5. **Document incident response** - Playbooks save time
6. **Review metrics regularly** - Weekly ops review
7. **Continuous improvement** - Add monitoring as you learn

## Monitoring ROI

**Cost:**
- Sentry: $0-26/month (free tier sufficient for PDFLab)
- UptimeRobot: $0-7/month (free tier sufficient)
- Time: 2-4 hours initial setup
- **Total: ~$0-50/month**

**Benefits:**
- Detect outages in 5 minutes (vs 5 hours from user reports)
- Reduce MTTR from hours to minutes
- Prevent revenue loss from undetected issues
- Build customer trust with transparent status
- **ROI: 10-100x** (one prevented outage pays for years of monitoring)

## When to Escalate

- Distributed tracing needs (microservices)
- Custom monitoring dashboards
- SLA/SLO definition
- On-call rotation setup
- Runbook automation
- Chaos engineering
