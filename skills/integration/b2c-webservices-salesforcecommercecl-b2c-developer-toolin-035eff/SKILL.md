---
name: b2c-webservices
description: Guide for implementing web service integrations in Salesforce B2C Commerce
---

# Web Services Skill

This skill guides you through implementing web service integrations in B2C Commerce using the Service Framework.

## Overview

The Service Framework provides a structured way to call external services with:

| Feature | Description |
|---------|-------------|
| **Configuration** | Service settings managed in Business Manager |
| **Rate Limiting** | Automatic throttling to protect external systems |
| **Circuit Breaker** | Automatic failure handling to prevent cascade failures |
| **Logging** | Communication logging with sensitive data filtering |
| **Mocking** | Test services without external calls |

## Service Types

| Type | Use Case | Protocol |
|------|----------|----------|
| `HTTP` | REST APIs, webhooks | HTTP/HTTPS |
| `HTTPForm` | Form submissions | HTTP/HTTPS with form encoding |
| `FTP` | File transfers (deprecated) | FTP |
| `SFTP` | Secure file transfers | SFTP |
| `SOAP` | SOAP web services | HTTP/HTTPS with SOAP |
| `GENERIC` | Custom protocols | Any |

## Service Framework Components

### Business Manager Configuration

Services are configured in **Administration > Operations > Services**:

1. **Service Configuration** - General settings (enabled, logging, callbacks)
2. **Service Profile** - Rate limiting and circuit breaker settings
3. **Service Credential** - URL and authentication credentials

### Script Components

| Component | Purpose |
|-----------|---------|
| `LocalServiceRegistry` | Creates service instances |
| `ServiceCallback` | Defines request/response handling |
| `Service` | Base service with common methods |
| `Result` | Response object with status and data |

## Basic Pattern

```javascript
'use strict';

var LocalServiceRegistry = require('dw/svc/LocalServiceRegistry');

var myService = LocalServiceRegistry.createService('my.service.id', {
    /**
     * Configure the request before it is sent
     * @param {dw.svc.HTTPService} svc - The service instance
     * @param {Object} params - Parameters passed to service.call()
     * @returns {string} Request body
     */
    createRequest: function (svc, params) {
        svc.setRequestMethod('POST');
        svc.addHeader('Content-Type', 'application/json');
        return JSON.stringify(params);
    },

    /**
     * Parse the response after a successful call
     * @param {dw.svc.HTTPService} svc - The service instance
     * @param {dw.net.HTTPClient} client - The HTTP client with response
     * @returns {Object} Parsed response
     */
    parseResponse: function (svc, client) {
        return JSON.parse(client.text);
    },

    /**
     * Filter sensitive data from logs (required for production)
     * @param {string} msg - The message to filter
     * @returns {string} Filtered message
     */
    filterLogMessage: function (msg) {
        return msg.replace(/("api_key"\s*:\s*")[^"]+"/g, '$1***"');
    }
});

// Call the service
var result = myService.call({ key: 'value' });

if (result.ok) {
    var data = result.object;
} else {
    var error = result.errorMessage;
}
```

## Service Callbacks

| Callback | Required | Description |
|----------|----------|-------------|
| `createRequest` | Yes* | Configure request, return body |
| `parseResponse` | Yes* | Parse response, return result object |
| `execute` | No | Custom execution logic (replaces default) |
| `initServiceClient` | No | Create/configure underlying client |
| `mockCall` | No | Return mock response (execute phase only) |
| `mockFull` | No | Return mock response (entire call) |
| `filterLogMessage` | Recommended | Filter sensitive data from logs |
| `getRequestLogMessage` | No | Custom request log message |
| `getResponseLogMessage` | No | Custom response log message |

*Required unless `execute` is implemented

## Result Object

The `call()` method returns a `dw.svc.Result`:

| Property | Type | Description |
|----------|------|-------------|
| `ok` | Boolean | True if successful |
| `status` | String | "OK", "ERROR", or "SERVICE_UNAVAILABLE" |
| `object` | Object | Response from `parseResponse` |
| `error` | Number | Error code (e.g., HTTP status) |
| `errorMessage` | String | Error description |
| `unavailableReason` | String | Why service is unavailable |
| `mockResult` | Boolean | True if from mock callback |

### Unavailable Reasons

| Reason | Description |
|--------|-------------|
| `TIMEOUT` | Call timed out |
| `RATE_LIMITED` | Rate limit exceeded |
| `CIRCUIT_BROKEN` | Circuit breaker open |
| `DISABLED` | Service disabled |
| `CONFIG_PROBLEM` | Configuration error |

## Error Handling

```javascript
var result = myService.call(params);

if (result.ok) {
    return result.object;
}

// Handle different error types
switch (result.status) {
    case 'SERVICE_UNAVAILABLE':
        switch (result.unavailableReason) {
            case 'RATE_LIMITED':
                // Retry later
                break;
            case 'CIRCUIT_BROKEN':
                // Service is down, use fallback
                break;
            case 'TIMEOUT':
                // Request timed out
                break;
        }
        break;
    case 'ERROR':
        // Check HTTP status code
        if (result.error === 401) {
            // Authentication error
        } else if (result.error === 404) {
            // Resource not found
        }
        break;
}

throw new Error('Service error: ' + result.errorMessage);
```

## Log Filtering

Production environments require log filtering to prevent sensitive data exposure:

```javascript
var myService = LocalServiceRegistry.createService('my.service', {
    createRequest: function (svc, params) {
        // ... configure request
    },

    parseResponse: function (svc, client) {
        return JSON.parse(client.text);
    },

    /**
     * Filter sensitive data from all log messages
     */
    filterLogMessage: function (msg) {
        // Filter API keys
        msg = msg.replace(/api_key=[^&]+/g, 'api_key=***');
        // Filter authorization headers
        msg = msg.replace(/Authorization:\s*[^\r\n]+/gi, 'Authorization: ***');
        // Filter passwords in JSON
        msg = msg.replace(/("password"\s*:\s*")[^"]+"/g, '$1***"');
        return msg;
    },

    /**
     * Custom request log message (optional)
     */
    getRequestLogMessage: function (request) {
        // Return custom message or null for default
        return 'Request: ' + request.substring(0, 100) + '...';
    },

    /**
     * Custom response log message (optional)
     */
    getResponseLogMessage: function (response) {
        // Return custom message or null for default
        return 'Response received';
    }
});
```

## Mocking Services

Use mock callbacks for testing without external calls:

```javascript
var myService = LocalServiceRegistry.createService('my.service', {
    createRequest: function (svc, params) {
        svc.setRequestMethod('GET');
        svc.addParam('id', params.id);
        return null;
    },

    parseResponse: function (svc, client) {
        return JSON.parse(client.text);
    },

    /**
     * Mock the execute phase only (createRequest and parseResponse still run)
     */
    mockCall: function (svc, request) {
        return {
            statusCode: 200,
            text: JSON.stringify({ id: 1, name: 'Mock Data' })
        };
    },

    /**
     * Or mock the entire call (replaces all phases)
     */
    mockFull: function (svc, params) {
        return { id: params.id, name: 'Full Mock Data' };
    }
});

// Force mock mode
myService.setMock();
var result = myService.call({ id: 123 });
```

## Service Configuration in Business Manager

### Creating a Service

1. Go to **Administration > Operations > Services**
2. Click **New** under Service Configurations
3. Fill in:
   - **Service ID**: Unique identifier (e.g., `my.api.service`)
   - **Service Type**: HTTP, FTP, SOAP, etc.
   - **Enabled**: Check to enable
   - **Profile**: Select or create a profile
   - **Credential**: Select or create credentials
   - **Communication Log**: Enable for debugging

### Service Profile Settings

| Setting | Description |
|---------|-------------|
| **Timeout** | Maximum wait time in milliseconds |
| **Rate Limit** | Maximum calls per time unit |
| **Circuit Breaker Enabled** | Enable automatic failure handling |
| **Max Circuit Breaker Calls** | Calls before circuit opens |
| **Circuit Breaker Interval** | Time window for tracking failures |

### Service Credential Settings

| Setting | Description |
|---------|-------------|
| **ID** | Credential identifier |
| **URL** | Base URL for the service |
| **User** | Username for authentication |
| **Password** | Password for authentication |

## Detailed References

- [HTTP Services](references/HTTP-SERVICES.md) - REST API integrations
- [FTP/SFTP Services](references/FTP-SERVICES.md) - File transfer operations
- [SOAP Services](references/SOAP-SERVICES.md) - SOAP web service integrations
- [Services XML](references/SERVICES-XML.md) - Import/export service configurations

## Script API Classes

| Class | Description |
|-------|-------------|
| `dw.svc.LocalServiceRegistry` | Create service instances |
| `dw.svc.Service` | Base service class |
| `dw.svc.HTTPService` | HTTP service methods |
| `dw.svc.FTPService` | FTP/SFTP service methods |
| `dw.svc.SOAPService` | SOAP service methods |
| `dw.svc.Result` | Service call result |
| `dw.svc.ServiceConfig` | Service configuration |
| `dw.svc.ServiceProfile` | Rate limit/circuit breaker config |
| `dw.svc.ServiceCredential` | Authentication credentials |
| `dw.net.HTTPClient` | Underlying HTTP client |
| `dw.net.FTPClient` | Underlying FTP client |
| `dw.net.SFTPClient` | Underlying SFTP client |
