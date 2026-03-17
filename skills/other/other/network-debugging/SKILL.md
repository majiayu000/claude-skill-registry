---
name: network-debugging
description: Debug network issues using browser tools and network analysis. Diagnose connection problems, latency, and data transmission issues.
---

# Network Debugging

## Overview

Network debugging identifies connectivity issues, latency problems, and data transmission errors that impact application performance.

## When to Use

- Slow loading times
- Failed requests
- Intermittent connectivity
- CORS errors
- SSL/TLS issues
- API communication problems

## Instructions

### 1. **Browser Network Tools**

```yaml
Chrome DevTools Network Tab:

Columns:
  - Name: Request file/endpoint
  - Status: HTTP status code
  - Type: Resource type (xhr, fetch, etc)
  - Initiator: What triggered request
  - Size: Resource size / transferred size
  - Time: Total time to complete
  - Waterfall: Timeline visualization

Timeline Breakdown:
  - Queueing: Waiting in queue
  - DNS: Domain name resolution
  - Initial connection: TCP handshake
  - SSL: SSL/TLS negotiation
  - Request sent: Time to send request
  - Waiting (TTFB): Time to first byte
  - Content Download: Receiving response

---

Network Conditions:

Throttling Presets:
  - Fast 3G: 1.6 Mbps down, 750 Kbps up
  - Slow 3G: 400 Kbps down, 400 Kbps up
  - Offline: No network connection

Custom Settings:
  - Simulate real network speeds
  - Test mobile performance
  - Identify bottlenecks
  - Verify error handling

---

Request Analysis:

Headers:
  - Request headers (what browser sent)
  - Response headers (server response)
  - Cookies (session data)
  - Authorization (tokens)

Preview:
  - JSON formatted view
  - Response data inspection
  - Parse errors highlighted

Response:
  - Full response body
  - Raw vs formatted view
  - File download option

Timing:
  - Detailed timing breakdown
  - Identify slow components
  - DNS lookup time
  - Connection establishment
```

### 2. **Common Network Issues**

```yaml
Issue: CORS Error

Error: "No 'Access-Control-Allow-Origin' header"

Solution:
  1. Check server CORS headers
  2. Verify allowed origins
  3. Check request method (GET, POST, etc)
  4. Add preflight handling
  5. Test with curl first

Server Configuration (Node.js):
  app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
  });

---

Issue: Slow DNS Resolution

Symptoms: Long DNS lookup time (>100ms)

Solutions:
  1. Use faster DNS (8.8.8.8, 1.1.1.1)
  2. Pre-connect to domain: <link rel="preconnect" href="https://api.example.com">
  3. DNS prefetch: <link rel="dns-prefetch" href="https://cdn.example.com">
  4. Check DNS provider
  5. Implement DNS caching

---

Issue: SSL Certificate Error

Error: "SSL_ERROR_RX_RECORD_TOO_LONG"

Debug:
  curl -v https://example.com
  openssl s_client -connect example.com:443
  Check certificate validity
  Check certificate chain
  Verify hostname matches

Solutions:
  1. Renew certificate
  2. Fix certificate chain
  3. Verify hostname
  4. Check server configuration

---

Issue: Timeout Errors

Symptoms: Requests hang, then fail after timeout

Analysis:
  1. Increase timeout in DevTools
  2. Check server response
  3. Verify network connectivity
  4. Check firewall rules
  5. Review server logs

---

Issue: Failed Requests (5xx errors)

Diagnosis:
  1. Check server logs
  2. Verify request data
  3. Check server resources
  4. Review recent changes
  5. Check database connectivity

Response:
  1. Implement retry logic
  2. Fallback mechanism
  3. Error notifications
  4. Graceful degradation
```

### 3. **Debugging Tools & Techniques**

```yaml
Tools:

curl:
  curl -v https://api.example.com
  curl -H "Authorization: Bearer token" https://api.example.com
  curl -X POST -d '{"key": "value"}' https://api.example.com

Postman:
  - GUI for request testing
  - Collection of requests
  - Environment variables
  - Pre/post request scripts
  - Mock servers

Network Inspector:
  - Browser DevTools Network tab
  - Real request/response viewing
  - Request filtering
  - Timing analysis

Traffic Analysis:
  - Charles Proxy (HTTP/HTTPS)
  - Fiddler
  - Wireshark (packet level)
  - tcpdump

---

Analysis Steps:

1. Reproduce Issue
  - Clear cache
  - Disable plugins
  - Disable extensions
  - Try incognito mode

2. Capture Traffic
  - Open Network tab
  - Clear current requests
  - Perform action
  - Observe requests

3. Analyze Requests
  - Check status codes
  - Review headers
  - Inspect payload
  - Check response time

4. Identify Pattern
  - Failed request pattern
  - Timing correlation
  - Specific conditions
  - Data size impact

5. Test Fix
  - Make change
  - Clear cache
  - Reproduce
  - Verify fix
```

### 4. **Checklist**

```yaml
Network Debugging Checklist:

Connection:
  [ ] Internet connectivity verified
  [ ] Firewall allows connection
  [ ] VPN not blocking
  [ ] Proxy configured if needed
  [ ] DNS resolving correctly

Request:
  [ ] Correct URL
  [ ] Correct HTTP method
  [ ] Required headers present
  [ ] Authorization correct
  [ ] Request body valid

Response:
  [ ] Status code expected
  [ ] Response headers correct
  [ ] Content-Type appropriate
  [ ] Response body valid
  [ ] No parsing errors

Performance:
  [ ] DNS lookup <50ms
  [ ] Connection <100ms
  [ ] TTFB <500ms
  [ ] Download reasonable
  [ ] Total time acceptable

Monitoring:
  [ ] Error logging enabled
  [ ] Network metrics tracked
  [ ] Alerts configured
  [ ] Baseline established
```

## Key Points

- Use Network tab for request analysis
- Check status codes and headers first
- Simulate network conditions for testing
- Test CORS with curl before debugging
- Monitor DNS and TLS times
- Implement retry logic for reliability
- Use appropriate timeouts
- Log requests for debugging
- Test on slow networks
- Verify error handling
