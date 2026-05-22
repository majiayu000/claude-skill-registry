---
name: Reverse Proxy Deployment
description: Deploy web applications behind Apache reverse proxy on rivsprod01 with relative URLs and proper path configuration
---

# Reverse Proxy Deployment

Guide for deploying web applications behind the Apache reverse proxy on rivsprod01 (dw.ramsden-international.com). Covers frontend relative URL patterns and Apache ProxyPass configuration.

## Instructions

When deploying a web application that will be accessed through the reverse proxy:

1. **Use Relative URLs**: Frontend code must use relative URLs (not absolute localhost URLs) to work behind the proxy
2. **Configure ProxyPass on rivsprod01**: Create Apache config in `/etc/apache2/proxy-conf.d/` with proper path stripping
3. **Order Matters**: More specific paths must come before general paths in Apache config
4. **Test Locally First**: Verify services are accessible from rivsprod01 before configuring proxy
5. **Use Trailing Slashes**: Both source and target URLs need trailing slashes for path stripping to work

## Examples

### Example 1: Deploy Web Application with API Backend

```
User: I have a web app with frontend on port 9273 and API on port 8765. Deploy it behind the proxy at /myapp/

Claude: I'll set up your application for reverse proxy deployment:

1. **Update Frontend URLs**: Change API calls to use relative URLs
   - Before: `fetch('http://localhost:8765/api/status')`
   - After: `fetch('api/status')`  // Relative to current path

2. **Create Apache Config**: SSH to rivsprod01 and create `/etc/apache2/proxy-conf.d/myapp.conf`
   - API path: `/myapp/api/` → backend on port 8765
   - Frontend path: `/myapp/` → frontend on port 9273
   - API location must come FIRST (more specific)

3. **Reload Apache**: `sudo systemctl reload apache2`

[Provides implementation using the ProxyPass Configuration pattern below]
```

### Example 2: Frontend Uses Absolute URLs

```
User: My frontend has `fetch('http://localhost:3000/api/data')` hardcoded. How do I make it work behind a proxy?

Claude: Absolute URLs won't work behind a reverse proxy. You need to update the frontend to use relative URLs:

**Options:**
1. **Best: Use relative URLs** - `fetch('api/data')` - works anywhere
2. **Alternative: Use base path** - Store base path in config, prepend to all API calls
3. **Hidden input method** - Store proxy path in HTML, read in JavaScript

For option 1 (recommended):
- Replace all `http://localhost:3000/api/` with `api/`
- The browser resolves relative to current page path
- If page is at `/myapp/`, API call goes to `/myapp/api/`

[Shows the Relative URL Pattern implementation below]
```

### Example 3: Multiple Services on Same Machine

```
User: I have 3 services running on ports 8001, 8002, 8003. Deploy all at /service1/, /service2/, /service3/

Claude: I'll configure all three services in a single Apache config file:

1. **Create single config file**: `/etc/apache2/proxy-conf.d/services.conf`
2. **Add ProxyPass for each**: More specific paths first (doesn't matter here since no overlap)
3. **Each service gets clean URLs**: Paths are stripped before forwarding
4. **Reload once**: All services go live together

[Provides implementation using the Multi-Service Configuration pattern below]
```

### Example 4: API Calls Return 404

```
User: My frontend loads but API calls return 404. Frontend is at /rabbit/, API should be at /rabbit/api/

Claude: The issue is likely ProxyPass configuration. Let me check:

1. **Verify services are reachable**: From rivsprod01, can you curl the backend directly?
   - `curl http://10.99.0.3:8765/status` should work

2. **Check ProxyPass order**: API location must come BEFORE frontend location
   - Wrong order: frontend `/rabbit/` catches `/rabbit/api/` requests
   - Right order: API `/rabbit/api/` catches first, then frontend `/rabbit/`

3. **Verify trailing slashes**: Both paths need trailing slashes for stripping
   - `ProxyPass /rabbit/api/ http://10.99.0.3:8765/`
   - Without trailing slash, path isn't stripped properly

[Shows debugging steps from Troubleshooting section below]
```

---

# Reference Implementation Details

The sections below contain proven working configurations from production deployments.

**Reference Files in This Folder**:
- `rabbit.conf` - Example Apache config from Invoice OCR deployment

## Relative URL Pattern

**Purpose**: Make frontend work behind any reverse proxy path without hardcoding URLs

### HTML Method (Recommended for Simple Cases)

```html
<!-- Hidden input stores the API base path -->
<input type="hidden" id="serverUrl" value="api">

<script>
function getServerUrl() {
    return document.getElementById('serverUrl').value.trim();
}

// Use in fetch calls
async function checkStatus() {
    const res = await fetch(`${getServerUrl()}/status`);
    const data = await res.json();
    // ...
}
</script>
```

**Key Points**:
- Value is `"api"` (relative) not `"http://localhost:8765"` (absolute)
- Browser resolves `api/status` relative to current page
- If page is at `https://example.com/rabbit/`, request goes to `https://example.com/rabbit/api/status`
- Proxy strips `/rabbit/` and forwards to backend

### JavaScript Config Method (For Complex Applications)

```javascript
// config.js
const CONFIG = {
    API_BASE: 'api',  // Relative to current path
    WS_BASE: 'ws'     // WebSocket endpoint if needed
};

// Use throughout app
fetch(`${CONFIG.API_BASE}/endpoint`)
```

**When to use**:
- Multiple API endpoints
- Different base paths for dev/staging/prod
- Need to change paths without editing HTML

## ProxyPass Configuration Pattern

**Purpose**: Configure Apache to forward requests from public path to internal service

### Basic Single-Service Configuration

**File**: `/etc/apache2/proxy-conf.d/myservice.conf`

```apache
# Single service on custom path
ProxyPass /myservice/ http://10.99.0.3:8080/
ProxyPassReverse /myservice/ http://10.99.0.3:8080/
```

**Key Points**:
- Simple ProxyPass directives (no `<Location>` blocks needed)
- Trailing slashes on both source and target strip the path prefix
- Request to `/myservice/page` becomes `/page` at backend
- `ProxyPassReverse` rewrites response headers (redirects, etc.)

### API + Frontend Configuration

**File**: `/etc/apache2/proxy-conf.d/service-with-api.conf`

```apache
# Backend API - Must come FIRST (more specific path)
ProxyPass /rabbit/api/ http://10.99.0.3:8765/
ProxyPassReverse /rabbit/api/ http://10.99.0.3:8765/

# Frontend - Comes SECOND (less specific path)
ProxyPass /rabbit/ http://10.99.0.3:9273/
ProxyPassReverse /rabbit/ http://10.99.0.3:9273/
```

**Key Points**:
- API location MUST be listed first (more specific)
- If frontend is listed first, it catches API requests → 404
- Both locations strip their prefix before forwarding
- Request flow:
  - `GET /rabbit/api/status` → matches first rule → `GET /status` to port 8765
  - `GET /rabbit/index.html` → matches second rule → `GET /index.html` to port 9273

### Large File Upload Configuration

```apache
# Service that handles file uploads (PDFs, images, etc.)
ProxyPass /uploads/ http://10.99.0.3:7000/
ProxyPassReverse /uploads/ http://10.99.0.3:7000/

# Important for large PDF uploads
<Location /uploads/>
    ProxyPass http://10.99.0.3:7000/
    ProxyPassReverse http://10.99.0.3:7000/

    # Allow 50MB uploads
    LimitRequestBody 52428800
</Location>
```

**When to use**:
- File upload services
- PDF/image processing
- Any endpoint that receives large request bodies

## Multi-Service Configuration Pattern

**Purpose**: Deploy multiple independent services in one config file

**File**: `/etc/apache2/proxy-conf.d/all-services.conf`

```apache
# Service 1: API Gateway
ProxyPass /api/ http://10.99.0.3:8001/
ProxyPassReverse /api/ http://10.99.0.3:8001/

# Service 2: Admin Dashboard
ProxyPass /admin/ http://10.99.0.3:8002/
ProxyPassReverse /admin/ http://10.99.0.3:8002/

# Service 3: Public Website
ProxyPass /site/ http://10.99.0.3:8003/
ProxyPassReverse /site/ http://10.99.0.3:8003/
```

**Key Points**:
- Each service is completely independent
- Order doesn't matter if paths don't overlap
- All go live together when Apache reloads
- Can comment out individual services to disable temporarily

## Deployment Workflow

**Standard deployment process for new service:**

### 1. Verify Local Service Accessibility

```bash
# From local machine where service runs
curl http://10.99.0.3:8765/status  # Test your port

# From rivsprod01 (SSH in)
ssh rivsprod01 "curl -s http://10.99.0.3:8765/status"
```

**Expected**: JSON response or HTML, not connection refused

### 2. Create Apache Configuration

```bash
# SSH to rivsprod01
ssh rivsprod01

# Create config file (as root or with sudo)
sudo nano /etc/apache2/proxy-conf.d/myservice.conf

# Add ProxyPass configuration (see patterns above)

# Verify syntax (optional, but recommended)
# apache2ctl configtest   # May not be available
# Just proceed to reload if command not found
```

### 3. Reload Apache

```bash
sudo systemctl reload apache2

# Verify Apache is still running
sudo systemctl status apache2
```

### 4. Test Public Access

```bash
# From any machine
curl https://dw.ramsden-international.com/myservice/

# Or open in browser
```

## Troubleshooting

### 404 Not Found - Service Works Locally

**Cause**: ProxyPass configuration issue

**Diagnostic Steps**:
1. Verify service is accessible from rivsprod01:
   ```bash
   ssh rivsprod01 "curl -s http://10.99.0.3:PORT/endpoint"
   ```

2. Check Apache config order:
   ```bash
   ssh rivsprod01 "cat /etc/apache2/proxy-conf.d/myservice.conf"
   ```
   - API paths must come before frontend paths
   - Verify trailing slashes on both source and target

3. Check Apache error logs:
   ```bash
   ssh rivsprod01 "sudo tail -50 /var/log/apache2/error.log | grep myservice"
   ```

**Solution**:
- Fix ProxyPass order (more specific first)
- Add missing trailing slashes
- Reload Apache: `sudo systemctl reload apache2`

### 404 on API Calls, Frontend Works

**Cause**: Frontend path is catching API requests

**Example of Wrong Configuration**:
```apache
# WRONG - Frontend catches everything
ProxyPass /app/ http://10.99.0.3:9000/
ProxyPass /app/api/ http://10.99.0.3:8000/
```

**Solution - Put API First**:
```apache
# CORRECT - API catches specific path first
ProxyPass /app/api/ http://10.99.0.3:8000/
ProxyPass /app/ http://10.99.0.3:9000/
```

### Connection Refused from rivsprod01

**Cause**: Service not listening on accessible IP

**Diagnostic**:
```bash
# On machine running service
netstat -tlnp | grep PORT
# or
ss -tlnp | grep PORT
```

**Look for**:
- `127.0.0.1:PORT` - Only listening on localhost (wrong)
- `10.99.0.3:PORT` - Listening on network IP (correct)
- `0.0.0.0:PORT` - Listening on all interfaces (also correct)

**Solution**: Configure service to bind to `0.0.0.0` or specific IP `10.99.0.3`

### Service Stops Working After Apache Reload

**Cause**: Configuration syntax error

**Diagnostic**:
```bash
ssh rivsprod01 "sudo systemctl status apache2"
```

**Solution**:
1. Check for typos in ProxyPass URLs
2. Verify no missing quotes or slashes
3. Look at error log: `sudo tail /var/log/apache2/error.log`
4. Fix config and reload again

### CORS Errors in Browser Console

**Cause**: Backend not configured for CORS, or wrong origin

**Solution (Backend)**: Enable CORS in your service

```python
# FastAPI example
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Note**: Proxy handles forwarding; backend sees requests from proxy IP, not client

## IP Addresses Reference

| Hostname | IP Address | Purpose |
|----------|-----------|---------|
| rivsprod01 | 10.99.0.2 | Reverse proxy server (Apache) |
| pogs (local) | 10.99.0.3 | Development machine running services |

**Service Configuration**:
- Services should bind to `10.99.0.3` or `0.0.0.0` to be accessible from rivsprod01
- Use `http://10.99.0.3:PORT` in ProxyPass target URLs
- Never use `localhost` or `127.0.0.1` in ProxyPass targets

## File Locations on rivsprod01

| Path | Purpose |
|------|---------|
| `/etc/apache2/proxy-conf.d/*.conf` | Proxy configurations (add yours here) |
| `/etc/apache2/sites-available/default-ssl.conf` | Main SSL site config (includes proxy-conf.d) |
| `/var/log/apache2/error.log` | Apache error log |
| `/var/log/apache2/access.log` | Access log (if needed) |

**Important**: Configs in `/etc/apache2/proxy-conf.d/` are automatically included by the SSL site configuration.

## Best Practices Summary

1. **Always use relative URLs** in frontend code for proxy compatibility
2. **Test service accessibility** from rivsprod01 before configuring proxy
3. **Put specific paths first** in Apache config (API before frontend)
4. **Use trailing slashes** on both ProxyPass source and target for path stripping
5. **Reload Apache** after config changes: `sudo systemctl reload apache2`
6. **Keep configs organized** - one file per application or related service group
7. **Document your paths** - add comments explaining what each ProxyPass does
8. **Test both frontend and API** after deployment to verify routing
