---
name: "Monitoring & Logging"
description: "Implement CloudWatch monitoring, error tracking with Sentry, structured logging, and alert configuration. Apply when setting up monitoring, tracking errors, debugging production issues, or configuring dashboards."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# Monitoring & Logging

Systematic monitoring, logging, and alerting for production applications.

## Overview

This Skill enforces:
- Structured logging (JSON format)
- CloudWatch integration
- Error tracking with Sentry
- Distributed tracing
- Alert configuration
- Dashboard setup
- Log aggregation
- Metrics collection

Apply when setting up monitoring, tracking errors, or debugging production issues.

## Structured Logging

### JSON Logging Format

```ts
// ✅ GOOD: Structured logs with context
const logger = {
  info: (message: string, context?: Record<string, any>) => {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      level: 'info',
      message,
      requestId: context?.requestId,
      userId: context?.userId,
      duration: context?.duration,
      ...context
    }));
  },
  error: (message: string, error?: Error, context?: Record<string, any>) => {
    console.error(JSON.stringify({
      timestamp: new Date().toISOString(),
      level: 'error',
      message,
      errorName: error?.name,
      errorMessage: error?.message,
      errorStack: error?.stack,
      requestId: context?.requestId,
      ...context
    }));
  },
  warn: (message: string, context?: Record<string, any>) => {
    console.warn(JSON.stringify({
      timestamp: new Date().toISOString(),
      level: 'warn',
      message,
      requestId: context?.requestId,
      ...context
    }));
  }
};

// Usage
logger.info('User created', { userId: user.id, email: user.email });
logger.error('Database connection failed', error, { 
  host: 'db.example.com',
  port: 5432 
});
```

### Middleware for Request Logging

```ts
// middleware/logging.ts
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const requestId = crypto.randomUUID();
  const start = Date.now();

  const response = NextResponse.next();
  response.headers.set('x-request-id', requestId);

  // Log after response
  const duration = Date.now() - start;
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level: 'info',
    message: 'HTTP Request',
    requestId,
    method: request.method,
    path: request.nextUrl.pathname,
    status: response.status,
    duration,
    userAgent: request.headers.get('user-agent')
  }));

  return response;
}
```

## CloudWatch Integration

### AWS SDK Logging

```ts
// lib/cloudwatch.ts
import { CloudWatchLogsClient, PutLogEventsCommand } from '@aws-sdk/client-cloudwatch-logs';

const client = new CloudWatchLogsClient({ region: 'us-east-1' });

export async function logToCloudWatch(
  logGroup: string,
  logStream: string,
  message: string
) {
  const command = new PutLogEventsCommand({
    logGroupName: logGroup,
    logStreamName: logStream,
    logEvents: [
      {
        message: JSON.stringify({
          timestamp: new Date().toISOString(),
          message
        }),
        timestamp: Date.now()
      }
    ]
  });

  try {
    await client.send(command);
  } catch (error) {
    console.error('Failed to log to CloudWatch:', error);
  }
}
```

### Log Agent Setup

```bash
# Install CloudWatch Logs agent
sudo apt install awslogs -y

# Configure /etc/awslogs/awslogs.conf
[/var/log/nodejs/app.log]
log_group_name = /aws/nodejs/myapp
log_stream_name = {instance_id}
file = /var/log/nodejs/app.log
datetime_format = %Y-%m-%d %H:%M:%S

# Restart agent
sudo systemctl restart awslogsd
```

## Structured Logging in Code

```ts
// lib/logger.ts
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { 
    service: 'myapp',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ 
      filename: 'logs/error.log', 
      level: 'error' 
    }),
    new winston.transports.File({ 
      filename: 'logs/combined.log' 
    })
  ]
});

export default logger;

// Usage
logger.info('User logged in', { userId: user.id });
logger.error('Database error', { error: err.message });
```

## Error Tracking with Sentry

### Setup Sentry

```bash
npm install @sentry/nextjs
```

### Configure

```ts
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,  // 10% of transactions
  beforeSend(event) {
    // Filter out certain errors
    if (event.exception) {
      const error = event.exception.values?.[0];
      if (error?.value?.includes('ResizeObserver')) {
        return null;  // Don't send
      }
    }
    return event;
  }
});
```

### Capture Errors

```ts
// Manual error capture
try {
  riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    tags: {
      section: 'user-profile'
    },
    contexts: {
      user: {
        userId: user.id,
        email: user.email
      }
    }
  });
}

// Automatic error capture
Sentry.withScope((scope) => {
  scope.setContext('user', { userId: user.id });
  Sentry.captureMessage('User action completed');
});
```

## Metrics Collection

### Custom Metrics

```ts
// lib/metrics.ts
import { CloudWatchClient, PutMetricDataCommand } from '@aws-sdk/client-cloudwatch';

const client = new CloudWatchClient({ region: 'us-east-1' });

export async function putMetric(
  metricName: string,
  value: number,
  unit: 'Count' | 'Seconds' | 'Milliseconds' = 'Count'
) {
  const command = new PutMetricDataCommand({
    Namespace: 'MyApp',
    MetricData: [
      {
        MetricName: metricName,
        Value: value,
        Unit: unit,
        Timestamp: new Date()
      }
    ]
  });

  try {
    await client.send(command);
  } catch (error) {
    console.error('Failed to put metric:', error);
  }
}

// Usage
await putMetric('UserCreated', 1, 'Count');
await putMetric('DatabaseQueryTime', 45, 'Milliseconds');
```

## Alert Configuration

### CloudWatch Alarms

```ts
// lib/alarms.ts
import { CloudWatchClient, PutMetricAlarmCommand } from '@aws-sdk/client-cloudwatch';

const client = new CloudWatchClient({ region: 'us-east-1' });

export async function createErrorCountAlarm() {
  const command = new PutMetricAlarmCommand({
    AlarmName: 'ApplicationErrors',
    MetricName: 'Errors',
    Namespace: 'MyApp',
    Statistic: 'Sum',
    Period: 300,  // 5 minutes
    EvaluationPeriods: 1,
    Threshold: 10,  // Alert if > 10 errors
    ComparisonOperator: 'GreaterThanThreshold',
    AlarmActions: [
      'arn:aws:sns:us-east-1:123456789012:AlertTopic'
    ]
  });

  await client.send(command);
}

// ✅ GOOD: Multiple metrics
PutMetricAlarmCommand({
  AlarmName: 'HighErrorRate',
  Metrics: [
    {
      Id: 'error_rate',
      Expression: '(errors / requests) * 100',
      ReturnData: true
    },
    {
      Id: 'errors',
      MetricStat: {
        Metric: { MetricName: 'Errors', Namespace: 'MyApp' },
        Stat: 'Sum',
        Period: 300
      }
    },
    {
      Id: 'requests',
      MetricStat: {
        Metric: { MetricName: 'Requests', Namespace: 'MyApp' },
        Stat: 'Sum',
        Period: 300
      }
    }
  ],
  Threshold: 5,  // Alert if error rate > 5%
  ComparisonOperator: 'GreaterThanThreshold'
});
```

## Dashboards

### CloudWatch Dashboard

```ts
// lib/dashboard.ts
import { CloudWatchClient, PutDashboardCommand } from '@aws-sdk/client-cloudwatch';

const client = new CloudWatchClient({ region: 'us-east-1' });

export async function createDashboard() {
  const command = new PutDashboardCommand({
    DashboardName: 'MyAppDashboard',
    DashboardBody: JSON.stringify({
      widgets: [
        {
          type: 'metric',
          properties: {
            metrics: [
              ['MyApp', 'Requests', { stat: 'Sum' }],
              ['MyApp', 'Errors', { stat: 'Sum' }],
              ['MyApp', 'Latency', { stat: 'Average' }]
            ],
            period: 300,
            stat: 'Average',
            region: 'us-east-1',
            title: 'Application Metrics'
          }
        },
        {
          type: 'log',
          properties: {
            query: 'fields @timestamp, @message | filter @message like /ERROR/',
            region: 'us-east-1',
            title: 'Recent Errors'
          }
        }
      ]
    })
  });

  await client.send(command);
}
```

## Distributed Tracing

### OpenTelemetry

```ts
// lib/tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { AWSXRayIdGenerator } from '@opentelemetry/id-generator-aws-xray';
import { AWSXRayPropagator } from '@opentelemetry/aws-xray-propagator';

const sdk = new NodeSDK({
  idGenerator: new AWSXRayIdGenerator(),
  instrumentations: [getNodeAutoInstrumentations()],
  traceExporter: new AWSXRayExporter({})
});

sdk.start();

process.on('SIGTERM', () => {
  sdk
    .shutdown()
    .then(() => process.exit(0))
    .catch((err) => {
      console.error('Error shutting down tracing:', err);
      process.exit(1);
    });
});

export default sdk;
```

## Log Retention

### Set Retention Policy

```ts
import { CloudWatchLogsClient, PutRetentionPolicyCommand } from '@aws-sdk/client-cloudwatch-logs';

const client = new CloudWatchLogsClient({ region: 'us-east-1' });

export async function setLogRetention(logGroup: string, days: number) {
  const command = new PutRetentionPolicyCommand({
    logGroupName: logGroup,
    retentionInDays: days
  });

  await client.send(command);
}

// Usage: Keep logs for 30 days
await setLogRetention('/aws/nodejs/myapp', 30);
```

## Anti-Patterns

```ts
// ❌ BAD: No structured logging
console.log('User created');
console.error('Something went wrong');

// ✅ GOOD: Structured with context
logger.info('User created', { userId: user.id, email: user.email });
logger.error('Database failed', error, { host: 'db.example.com' });

// ❌ BAD: No error tracking
try {
  riskyOperation();
} catch (error) {
  console.error(error);  // Lost!
}

// ✅ GOOD: Error tracking
try {
  riskyOperation();
} catch (error) {
  Sentry.captureException(error);
}

// ❌ BAD: No correlation IDs
// Impossible to trace requests

// ✅ GOOD: Correlation IDs
const requestId = crypto.randomUUID();
logger.info('Request started', { requestId });
```

## Verification Before Production

- [ ] Structured logging implemented
- [ ] CloudWatch integrated
- [ ] Sentry configured for error tracking
- [ ] Alarms set up for critical metrics
- [ ] Dashboard created
- [ ] Log retention policy set
- [ ] Request correlation IDs used
- [ ] Sensitive data filtered from logs
- [ ] Metrics collected for key operations
- [ ] Alert channels configured (email, Slack)

## Integration with Project Standards

Enforces observability:
- Quick error detection
- Production debugging capability
- Performance monitoring
- SLA compliance

## Resources

- CloudWatch Docs: https://docs.aws.amazon.com/cloudwatch
- Sentry: https://sentry.io
- OpenTelemetry: https://opentelemetry.io
- Winston Logger: https://github.com/winstonjs/winston
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
