---
name: error-patterns
description: Error handling patterns and logging standards. Use when error patterns guidance is required.
---
# Error Handling Strategy Implementation

## Fail-Fast Pattern Enforcement

### Early Exit Implementation

Apply fail-fast principles at system boundaries:

Input validation failures:
- Reject invalid input immediately with descriptive errors
- Validate all external data before processing
- Check preconditions before performing operations
- Return specific error types for different failure modes

Invariant violations:
- Assert program invariants at critical points
- Fail immediately when business rules are violated
- Check state consistency before state transitions
- Implement defensive checks at module boundaries

### Error Context Preservation

Maintain error context throughout call chains:
- Wrap errors with context using language-specific patterns
- Include relevant state information in error messages
- Preserve original error messages and stack traces
- Implement error chaining for comprehensive debugging

Error context standards:
- Log input parameters that caused failures
- Capture system state at error occurrence
- Include user context for application errors
- Document retry attempts and recovery actions

## Structured Logging Implementation

### Logging Format Standards

Implement consistent structured logging:
- Use JSON or key-value structured format
- Include timestamp, severity level, and message
- Add correlation IDs for request tracing
- Structure context data as key-value pairs

Log level usage guidelines:
- ERROR: System failures requiring intervention
- WARN: Recoverable errors or degraded functionality
- INFO: Significant business events and state changes
- DEBUG: Detailed execution information for troubleshooting

### Log Content Standards

Essential log entry components:
- Timestamp in ISO 8601 format with timezone
- Structured severity/level field
- Correlation/request ID for distributed tracing
- Service/component name identification
- Message with sufficient detail for debugging

Contextual data inclusion:
- User identifiers when applicable
- Operation names and parameters
- Performance metrics (duration, resource usage)
- Error details with stack traces for errors

## Error Recovery Patterns

### Retry Logic Implementation

Apply exponential backoff for transient failures:
- Start with initial delay (e.g., 100ms)
- Double delay with each retry attempt
- Implement jitter to avoid thundering herd
- Set maximum retry limits and timeout bounds

Retry condition validation:
- Retry only on transient errors (timeouts, network issues)
- Avoid retrying on client errors (4xx HTTP status)
- Implement idempotency for retried operations
- Use circuit breakers for persistent failures

### Circuit Breaker Pattern

Implement circuit breaker for external dependencies:
- Track failure rates for external service calls
- Open circuit when failure threshold exceeded
- Implement timeout for open state duration
- Use half-open state for recovery testing

Circuit breaker configuration:
- Set appropriate failure rate thresholds (e.g., 50%)
- Configure minimum request count before tripping
- Implement timeout for open state (e.g., 60 seconds)
- Add monitoring for circuit state changes

## Error Monitoring and Alerting

### Error Classification System

Categorize errors for effective triage:
- Critical: System outages, data corruption, security breaches
- High: Degraded functionality, major feature failures
- Medium: Non-critical errors with workarounds
- Low: Cosmetic issues or minor UX problems

Error metadata standards:
- Include error type and category in structured logs
- Add business impact assessment
- Capture affected user counts when applicable
- Document resolution steps and time to resolution

### Monitoring Integration

Implement comprehensive error monitoring:
- Aggregate errors from all services and components
- Set up alerting for critical error patterns
- Create dashboards for error trend analysis
- Integrate with incident management systems

Alert configuration guidelines:
- Alert on critical errors immediately
- Set thresholds for error rate increases
- Monitor new error types and patterns
- Implement escalation procedures for persistent issues

# Language-Specific Error Patterns

## Go Error Handling Patterns

### Go-Specific Error Conventions

Apply Go error handling best practices:
- Use explicit error returns, not exceptions
- Implement error wrapping with `fmt.Errorf("%w", err)`
- Create custom error types with proper interfaces
- Use sentinel errors for expected failure conditions

Error interface implementation:
```go
type ValidationError struct {
    Field   string
    Message string
    Cause   error
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}
```

## Python Error Handling Patterns

### Python Exception Handling

Apply Python exception best practices:
- Use specific exception types, not bare `except:`
- Implement custom exception classes for domain errors
- Use context managers for resource management
- Apply exception chaining with `raise ... from err`

Logging integration patterns:
```python
import logging

logger = logging.getLogger(__name__)

try:
    process_data(data)
except ValidationError as e:
    logger.error("Validation failed", extra={
        "error_type": "validation",
        "field": e.field,
        "input_data": data
    })
    raise
```

## JavaScript Error Handling Patterns

### JavaScript Exception Strategies

Apply JavaScript error handling patterns:
- Use try-catch blocks for synchronous operations
- Implement Promise rejection handling with `.catch()`
- Use async/await with proper error propagation
- Create custom error classes extending `Error`

Error handling in asynchronous code:
```javascript
async function processRequest(request) {
    try {
        const data = await validateInput(request);
        const result = await processData(data);
        return result;
    } catch (error) {
        logger.error("Request processing failed", {
            requestId: request.id,
            error: error.message,
            stack: error.stack
        });
        throw error;
    }
}
```

# Error Prevention Strategies

## Defensive Programming Implementation

### Input Validation Standards

Validate all external inputs systematically:
- Check for null/undefined values
- Validate data types and formats
- Enforce business rule constraints
- Sanitize inputs to prevent injection attacks

Validation pattern implementation:
- Implement validation schemas for complex inputs
- Use validation libraries for common patterns
- Apply validation at API boundaries
- Provide clear validation error messages

### State Management Validation

Implement robust state management:
- Validate state transitions
- Check for illegal state combinations
- Implement invariants checking
- Use state machines for complex workflows

State validation techniques:
- Add assertions for critical invariants
- Implement state consistency checks
- Use type systems to prevent invalid states
- Document allowed state transitions

## Testing Error Conditions

### Error Path Testing

Comprehensive error condition testing:
- Test all error branches and edge cases
- Verify error messages are informative
- Test error recovery mechanisms
- Validate error propagation patterns

Error testing strategies:
- Use mocking to simulate error conditions
- Test with invalid inputs and boundary conditions
- Verify retry logic and circuit breaker behavior
- Test monitoring and alerting integration
