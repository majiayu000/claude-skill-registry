---
name: b2c-logging
description: Guide for implementing logging in Salesforce B2C Commerce scripts
---

# Logging Skill

This skill guides you through implementing logging in B2C Commerce using the Logger and Log classes.

## Overview

B2C Commerce provides a logging framework with:

| Feature | Description |
|---------|-------------|
| **Log Levels** | debug, info, warn, error, fatal |
| **Categories** | Organize logs by functional area |
| **Custom Files** | Write to dedicated log files |
| **NDC** | Nested Diagnostic Context for tracing |
| **BM Configuration** | Enable/disable levels per category |

## Log Levels

| Level | Method | Description | Default State |
|-------|--------|-------------|---------------|
| `debug` | `debug()` | Detailed debugging information | Disabled (never on production) |
| `info` | `info()` | General information | Disabled by default |
| `warn` | `warn()` | Warning conditions | Always enabled |
| `error` | `error()` | Error conditions | Always enabled |
| `fatal` | `fatal()` | Critical failures | Always enabled, can send email |

## Basic Logging

### Using Logger (Static Methods)

The `Logger` class provides static methods for quick logging:

```javascript
var Logger = require('dw/system/Logger');

// Simple messages
Logger.debug('Debug message');
Logger.info('Info message');
Logger.warn('Warning message');
Logger.error('Error message');

// Messages with parameters (Java MessageFormat syntax)
Logger.info('Processing order {0} for customer {1}', orderNo, customerEmail);
Logger.error('Failed to process {0}: {1}', productId, errorMessage);
```

### Using Log (Instance Methods)

The `Log` class provides instance-based logging with categories:

```javascript
var Logger = require('dw/system/Logger');

// Get logger for a category
var log = Logger.getLogger('checkout');

log.debug('Cart contents: {0}', JSON.stringify(cart));
log.info('Checkout started for basket {0}', basketId);
log.warn('Inventory low for product {0}', productId);
log.error('Payment failed: {0}', errorMessage);
log.fatal('Critical checkout failure: {0}', errorMessage);
```

## Categories

Categories help organize and filter log messages:

```javascript
var Logger = require('dw/system/Logger');

// Different categories for different areas
var checkoutLog = Logger.getLogger('checkout');
var paymentLog = Logger.getLogger('payment');
var inventoryLog = Logger.getLogger('inventory');
var integrationLog = Logger.getLogger('integration');

// Use appropriate logger
checkoutLog.info('Order {0} submitted', orderNo);
paymentLog.info('Payment authorized: {0}', transactionId);
inventoryLog.warn('Stock level below threshold for {0}', productId);
integrationLog.error('API call failed: {0}', serviceName);
```

Categories are configured in Business Manager under **Administration > Operations > Custom Log Settings**.

## Custom Named Log Files

Write to dedicated log files instead of the standard custom log files:

```javascript
var Logger = require('dw/system/Logger');

// Get logger with custom file prefix
var orderExportLog = Logger.getLogger('orderexport', 'export');
var feedLog = Logger.getLogger('productfeed', 'feed');

// Messages go to custom-orderexport-*.log
orderExportLog.info('Exporting order {0}', orderNo);

// Messages go to custom-productfeed-*.log
feedLog.info('Processing product {0}', productId);
```

### File Name Rules

The `fileNamePrefix` parameter must follow these rules:

| Rule | Requirement |
|------|-------------|
| Length | 3-25 characters |
| Characters | a-z, A-Z, 0-9, `-`, `_` |
| Start/End | Must start and end with alphanumeric |
| Not allowed | Cannot start or end with `-` or `_` |

### File Naming Pattern

Custom log files follow this pattern:
```
custom-<prefix>-<hostname>-appserver-<date>.log
```

Example: `custom-orderexport-blade0-1-appserver-20240115.log`

### Quota

Maximum 200 different log file names per day per appserver.

## Checking Log Level Status

Check if a log level is enabled before expensive operations:

```javascript
var Logger = require('dw/system/Logger');
var log = Logger.getLogger('myCategory');

// Check before expensive string building
if (log.isDebugEnabled()) {
    log.debug('Full cart contents: {0}', JSON.stringify(cart));
}

// Check before expensive calculations
if (log.isInfoEnabled()) {
    var stats = calculateDetailedStats(); // expensive
    log.info('Statistics: {0}', JSON.stringify(stats));
}

// Available checks
log.isDebugEnabled();  // true if debug logging enabled
log.isInfoEnabled();   // true if info logging enabled
log.isWarnEnabled();   // true if warn logging enabled
log.isErrorEnabled();  // true if error logging enabled
```

### Static Level Checks

```javascript
var Logger = require('dw/system/Logger');

if (Logger.isDebugEnabled()) {
    Logger.debug('Debug message');
}
```

## Message Formatting

Messages support Java MessageFormat syntax:

```javascript
var Logger = require('dw/system/Logger');
var log = Logger.getLogger('order');

// Positional parameters
log.info('Order {0} has {1} items totaling {2}', orderNo, itemCount, total);

// Same parameter multiple times
log.info('Product {0}: {0} is out of stock', productId);

// Complex objects (use JSON.stringify for objects)
log.debug('Request: {0}', JSON.stringify(requestData));
```

## Nested Diagnostic Context (NDC)

NDC helps trace related log messages across a request:

```javascript
var Logger = require('dw/system/Logger');
var Log = require('dw/system/Log');

var log = Logger.getLogger('checkout');
var ndc = Log.getNDC();

function processOrder(orderId) {
    // Push context onto the stack
    ndc.push('Order:' + orderId);

    try {
        log.info('Starting order processing');
        processPayment();
        processShipping();
        log.info('Order processing complete');
    } finally {
        // Always pop context when leaving scope
        ndc.pop();
    }
}

function processPayment() {
    ndc.push('Payment');
    try {
        log.info('Processing payment'); // NDC shows: Order:123 Payment
    } finally {
        ndc.pop();
    }
}
```

### NDC Methods

| Method | Description |
|--------|-------------|
| `push(message)` | Add context to the stack |
| `pop()` | Remove and return top context |
| `peek()` | View top context without removing |
| `remove()` | Clear entire context |

## Best Practices

### 1. Use Categories

```javascript
// Good: Organized by functional area
var log = Logger.getLogger('payment.processor');
var log = Logger.getLogger('inventory.sync');
var log = Logger.getLogger('order.export');

// Avoid: No category
Logger.info('Something happened');
```

### 2. Check Level Before Expensive Operations

```javascript
// Good: Check before building expensive string
if (log.isDebugEnabled()) {
    log.debug('Full response: {0}', JSON.stringify(largeObject));
}

// Avoid: Always building expensive strings
log.debug('Full response: {0}', JSON.stringify(largeObject));
```

### 3. Include Context in Messages

```javascript
// Good: Includes relevant context
log.error('Payment failed for order {0}, customer {1}: {2}',
    orderNo, customerId, errorMessage);

// Avoid: Missing context
log.error('Payment failed');
```

### 4. Use Appropriate Levels

```javascript
// debug: Detailed technical information
log.debug('SQL query: {0}', query);
log.debug('API request body: {0}', JSON.stringify(body));

// info: Notable events
log.info('Order {0} placed successfully', orderNo);
log.info('Customer {0} logged in', customerId);

// warn: Potential issues
log.warn('Inventory low for product {0}: {1} remaining', productId, qty);
log.warn('Slow API response: {0}ms', responseTime);

// error: Failures that need attention
log.error('Payment declined for order {0}: {1}', orderNo, reason);
log.error('Failed to connect to service {0}: {1}', serviceName, error);

// fatal: Critical system failures
log.fatal('Database connection lost');
log.fatal('Critical configuration missing: {0}', configKey);
```

### 5. Use Custom Log Files for Integration

```javascript
// Dedicated files for each integration
var erpLog = Logger.getLogger('erp-sync', 'erp');
var omsLog = Logger.getLogger('oms-export', 'oms');
var crmLog = Logger.getLogger('crm-sync', 'crm');
```

### 6. Don't Log Sensitive Data

```javascript
// Good: Mask sensitive data
log.info('Payment processed for card ending in {0}', cardNumber.slice(-4));

// Avoid: Logging sensitive data
log.info('Payment processed for card {0}', cardNumber);
```

## Business Manager Configuration

Configure custom logging in **Administration > Operations > Custom Log Settings**:

| Setting | Description |
|---------|-------------|
| **Log to File** | Enable file logging for each level |
| **Receive Email** | Email addresses for fatal notifications |
| **Root Category** | Default settings for all categories |
| **Custom Categories** | Override settings per category |

### Configuring Categories

1. Go to **Custom Log Settings**
2. Click **Add Category**
3. Enter category name (e.g., `checkout`, `payment`)
4. Set log levels to enable

## Log Output Format

Log entries follow this format:
```
[timestamp] [level] [category] message
```

Example:
```
[2024-01-15 10:30:45.123 GMT] [INFO] [checkout] Order ORD123 placed successfully
```

## Detailed Reference

- [Log Files](references/LOG-FILES.md) - Log file types, locations, and retention

## Script API Classes

| Class | Description |
|-------|-------------|
| `dw.system.Logger` | Static logging methods and logger factory |
| `dw.system.Log` | Logger instance with category support |
| `dw.system.LogNDC` | Nested Diagnostic Context for tracing |
