---
name: production-observability
# prettier-ignore
description: Use when adding logging, error monitoring, metrics, Sentry, debugging production issues, or improving observability
version: 1.0.0
---

<objective>
Make systems transparent. When something happens, you should see it. When something breaks, you should know why. Observability is the foundation of reliable production systems.
</objective>

<when-to-use>
Auto-triggers when:
- Writing code that runs in production
- Discussing error handling or monitoring
- Investigating production issues
- Planning new features that affect users
- Reviewing code for production readiness
</when-to-use>

<core-principles>

## Structured Logging

Log with context that helps debug issues. Use structured JSON logging with consistent
fields across the application.

<logging-pattern>
import { logger } from '@/lib/logger';

// Include relevant context in every log logger.info( { userId, action:
'subscription_created', subscriptionType, paymentMethod, amount, }, 'User subscribed
successfully' );

logger.error( { error, userId, operation: 'process_payment', paymentProvider: 'stripe',
attemptCount, }, 'Payment processing failed' );

logger.warn( { userId, resourceType: 'api_request', endpoint: '/api/data', responseTime:
2500, threshold: 1000, }, 'Slow API response detected' ); </logging-pattern>

<logging-pattern>
// Create child loggers for request context
const requestLogger = logger.child({
  requestId,
  userEmail,
  endpoint: req.url,
});

requestLogger.info('Processing request'); // All subsequent logs include requestId +
userEmail automatically requestLogger.debug({ queryParams }, 'Executing database
query'); requestLogger.info({ duration }, 'Request completed'); </logging-pattern>

<logging-pattern>
// Log at appropriate levels
logger.debug({ sql, params }, 'Database query'); // Development debugging
logger.info({ userId, action }, 'User action completed'); // Normal operations
logger.warn({ retryCount, error }, 'Retrying operation'); // Attention needed
logger.error({ error, context }, 'Operation failed'); // Immediate attention
</logging-pattern>

## Error Monitoring

Capture exceptions with rich context that enables debugging. Use Sentry or similar tools
to track errors in production.

<error-monitoring-pattern>
import * as Sentry from '@sentry/nextjs';

try { await criticalOperation(); } catch (error) { logger.error({ error, userId,
operation }, 'Critical operation failed');

Sentry.captureException(error, { tags: { operation: 'payment_processing', provider:
'stripe', }, extra: { userId, subscriptionId, attemptCount, paymentMethod, }, level:
'error', });

throw error; // Let error bubble to boundary } </error-monitoring-pattern>

<error-monitoring-pattern>
// Add breadcrumbs for debugging context
Sentry.addBreadcrumb({
  category: 'auth',
  message: 'User authentication started',
  level: 'info',
  data: { provider: 'google', userEmail },
});

// Later when error occurs, breadcrumbs show the sequence </error-monitoring-pattern>

<error-monitoring-pattern>
// Set user context for all errors
Sentry.setUser({
  id: user.id,
  email: user.email,
  username: user.name,
});

// All subsequent errors include user context automatically </error-monitoring-pattern>

## Performance Monitoring

Track operation timing to catch performance degradation early.

<performance-monitoring-pattern>
import * as Sentry from '@sentry/nextjs';

// Trace important operations const result = await Sentry.startSpan( { op:
'http.client', name: `${method} ${url}`, }, async (span) => {
span.setAttribute('http.method', method); span.setAttribute('http.url', url);
span.setAttribute('user.id', userId);

    const response = await fetch(url, options);

    span.setAttribute('http.status_code', response.status);
    span.setStatus({ code: 1, message: 'Success' });

    return response;

} ); </performance-monitoring-pattern>

<performance-monitoring-pattern>
// Track database query performance
logger.info(
  {
    operation: 'database_query',
    table: 'users',
    queryType: 'select',
    duration: queryDuration,
    rowCount: results.length,
  },
  'Database query completed'
);

if (queryDuration > 1000) { logger.warn( { query: sanitizedQuery, duration:
queryDuration, threshold: 1000, }, 'Slow query detected' ); }
</performance-monitoring-pattern>

## Health Checks

Expose endpoints that verify system health and dependencies.

<health-check-pattern>
// Health check endpoint
export async function GET() {
  const checks = await Promise.allSettled([
    checkDatabase(),
    checkRedis(),
    checkExternalAPI(),
  ]);

const results = { status: checks.every(c => c.status === 'fulfilled') ? 'healthy' :
'degraded', timestamp: new Date().toISOString(), checks: { database: checks[0].status
=== 'fulfilled' ? 'ok' : 'failed', redis: checks[1].status === 'fulfilled' ? 'ok' :
'failed', externalAPI: checks[2].status === 'fulfilled' ? 'ok' : 'failed', }, };

logger.info({ health: results }, 'Health check completed');

return Response.json(results, { status: results.status === 'healthy' ? 200 : 503, }); }
</health-check-pattern>

## Metrics and Monitoring

Track key business and system metrics that indicate application health.

<metrics-pattern>
import * as Sentry from '@sentry/nextjs';

// Track business metrics Sentry.metrics.increment('user.signup', 1, { tags: { source:
'google_oauth', plan: 'free' }, });

Sentry.metrics.distribution('api.response_time', responseTime, { tags: { endpoint:
'/api/chat', method: 'POST' }, unit: 'millisecond', });

Sentry.metrics.gauge('active_connections', connectionCount, { tags: { service:
'websocket' }, }); </metrics-pattern>

## Error Boundaries

Let errors bubble to boundaries where they can be handled appropriately. Don't silently
catch and hide errors.

<error-boundary-pattern>
// API route error boundary
export async function POST(request: Request) {
  try {
    const data = await request.json();
    const result = await processData(data);
    return Response.json({ success: true, result });
  } catch (error) {
    logger.error({ error, endpoint: '/api/process' }, 'API request failed');

    Sentry.captureException(error, {
      tags: { endpoint: '/api/process' },
    });

    if (error instanceof ValidationError) {
      return Response.json(
        { error: error.message },
        { status: 400 }
      );
    }

    if (error instanceof NotFoundError) {
      return Response.json(
        { error: error.message },
        { status: 404 }
      );
    }

    return Response.json(
      { error: 'Internal server error' },
      { status: 500 }
    );

} } </error-boundary-pattern>

## Correlation IDs

Track requests across service boundaries using correlation IDs.

<correlation-pattern>
// Generate correlation ID for request
const correlationId = generateId();

const requestLogger = logger.child({ correlationId });

// Pass correlation ID to downstream services const response = await
fetch(upstreamService, { headers: { 'X-Correlation-ID': correlationId, }, });

// All logs include correlationId, making distributed tracing possible
requestLogger.info({ service: 'upstream' }, 'Called upstream service');
</correlation-pattern>

</core-principles>

<what-to-monitor>

Monitor these signals to catch production issues early:

Error rates - Track 4xx and 5xx errors. Sudden spikes indicate problems.

Response times - P50, P95, P99 latencies. Degradation affects user experience.

Resource usage - CPU, memory, disk, network. Exhaustion causes failures.

External dependencies - API availability, database connections, third-party services.

Business metrics - User signups, purchases, key user actions. Drops indicate broken
flows.

</what-to-monitor>

<production-readiness-checklist>

Before deploying code to production, verify:

Structured logging covers critical paths - Can you debug issues from logs alone?

Errors are captured to Sentry - Will you know when things break?

Performance is tracked - Can you identify slow operations?

Health checks are implemented - Can monitoring detect degraded state?

Correlation IDs flow through requests - Can you trace requests across services?

Alerts are configured - Will someone be notified when thresholds are exceeded?

</production-readiness-checklist>

<debugging-production-issues>

When investigating production problems:

Start with error tracking - Check Sentry for exceptions and error patterns.

Review structured logs - Filter by user, request, or correlation ID to trace execution.

Check metrics - Look for anomalies in response times, error rates, resource usage.

Verify external dependencies - Confirm third-party services are operational.

Reproduce locally - Use production logs to recreate the scenario.

Add instrumentation - If debugging is difficult, add more logging and redeploy.

</debugging-production-issues>

<observability-culture>

Treat observability as a core feature, not an afterthought:

Log before releasing - Instrumentation is harder to add after deployment.

Monitor what matters - Focus on user-impacting metrics, not vanity numbers.

Make logs searchable - Use consistent field names and structured data.

Review errors regularly - Sentry notifications should trigger investigation.

Celebrate transparency - Visible problems get fixed. Hidden problems accumulate.

</observability-culture>
