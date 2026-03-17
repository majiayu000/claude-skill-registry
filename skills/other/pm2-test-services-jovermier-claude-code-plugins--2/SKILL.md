---
name: pm2-test-services
description: Activate when managing PM2 services for Playwright test reports, trace viewers, or other test artifacts. Includes starting/stopping services, generating dynamic workspace URLs (Coder/VS Code), and viewing service logs.
updated: 2025-01-13
---

# PM2 Test Services Skill

This skill manages PM2 services for serving Playwright test reports, trace viewers, and other test artifacts in development environments.

## When This Skill Activates

Claude automatically uses this skill when you:

- Need to serve Playwright HTML reports via PM2
- Want to run a trace viewer for failed tests
- Are managing multiple test-related services
- Need dynamic URLs for workspace environments (Coder, VS Code, Codespaces)
- Want to view or manage PM2 service logs
- Are troubleshooting test report access issues

## Why PM2 for Test Services?

PM2 provides:
- **Persistent services** - Reports stay available after tests complete
- **Easy management** - Start, stop, restart with simple commands
- **Log management** - Built-in log viewing and rotation
- **Process monitoring** - Automatic restart on failure
- **Multi-service** - Run report server, trace viewer, and more simultaneously

## PM2 Service Configuration

**Example PM2 Ecosystem File:**

```javascript
// pm2.test.config.js
module.exports = {
  apps: [
    {
      name: 'playwright-report-server',
      script: 'npx',
      args: 'playwright show-report',
      cwd: './playwright-report',
      env: {
        PORT: 9323,
        HOST: '0.0.0.0',
      },
    },
    {
      name: 'playwright-trace-viewer',
      script: 'npx',
      args: 'playwright show-trace',
      cwd: './test-results',
      env: {
        PORT: 9324,
        HOST: '0.0.0.0',
      },
    },
  ],
};
```

## Common PM2 Commands

### Starting Services

```bash
# Start all services from ecosystem file
pm2 start pm2.test.config.js

# Start specific app
pm2 start playwright-report-server

# Start with custom name
pm2 start npx --name "test-report" -- show-report
```

### Managing Services

```bash
# List all services
pm2 status

# Stop all services
pm2 stop all

# Stop specific service
pm2 stop playwright-report-server

# Restart service
pm2 restart playwright-report-server

# Delete service
pm2 delete playwright-report-server

# Delete all services
pm2 delete all
```

### Viewing Logs

```bash
# View all logs (streaming)
pm2 logs

# View specific service logs
pm2 logs playwright-report-server

# View last N lines without streaming
pm2 logs playwright-report-server --nostream --lines 50

# View logs with timestamp
pm2 logs --timestamp

# Clear all logs
pm2 flush
```

## Dynamic Workspace URLs

For cloud development environments (Coder, VS Code, Codespaces), you need to generate URLs dynamically based on workspace info.

### URL Pattern Templates

| Environment | URL Pattern |
|-------------|-------------|
| **Coder** | `https://playwright-ui--{workspace}--{owner}.{coder-domain}/` |
| **VS Code** | Forwarded port: `localhost:9323` |
| **Codespaces** | `https://{port}-{workspace}.{github-username}.github.dev/` |

### Generating Coder URLs

```bash
# Get Coder environment info
export CODER_WORKSPACE=$(basename $PWD)
export CODER_OWNER=$(whoami)
export CODER_DOMAIN=${CODER_DOMAIN:-"coder.example.com"}

# Generate service URLs
REPORT_URL="https://playwright-ui--${CODER_WORKSPACE}--${CODER_OWNER}.${CODER_DOMAIN}/"
TRACE_URL="https://playwright-trace--${CODER_WORKSPACE}--${CODER_OWNER}.${CODER_DOMAIN}/"

echo "Report Server: $REPORT_URL"
echo "Trace Viewer: $TRACE_URL"
```

### Package.json Scripts

```json
{
  "scripts": {
    "test:pm2:start": "pm2 start pm2.test.config.js",
    "test:pm2:stop": "pm2 delete all",
    "test:pm2:restart": "pm2 restart all",
    "test:pm2:status": "pm2 status",
    "test:pm2:logs": "pm2 logs --nostream --lines 50",
    "playwright:url": "node scripts/show-test-urls.js"
  }
}
```

### URL Generation Script

```javascript
// scripts/show-test-urls.js
const { execSync } = require('child_process');

// Try to detect environment
const env = process.env.CODESPACE_NAME ? 'codespaces' :
            process.env.CODER_WORKSPACE ? 'coder' : 'local';

let reportUrl, traceUrl;

switch (env) {
  case 'coder':
    const workspace = process.env.CODER_WORKSPACE;
    const owner = process.env.CODER_OWNER || process.env.USER;
    const domain = process.env.CODER_DOMAIN || 'coder.example.com';
    reportUrl = `https://playwright-ui--${workspace}--${owner}.${domain}/`;
    traceUrl = `https://playwright-trace--${workspace}--${owner}.${domain}/`;
    break;

  case 'codespaces':
    const codespace = process.env.CODESPACE_NAME;
    reportUrl = `https://9323-${codespace}.preview.app.github.dev/`;
    traceUrl = `https://9324-${codespace}.preview.app.github.dev/`;
    break;

  case 'local':
  default:
    reportUrl = 'http://localhost:9323';
    traceUrl = 'http://localhost:9324';
    break;
}

console.log(`Environment: ${env}`);
console.log(`Report Server: ${reportUrl}`);
console.log(`Trace Viewer: ${traceUrl}`);

// Optional: Open in browser
if (process.platform === 'darwin') {
  execSync(`open ${reportUrl}`);
} else if (process.platform === 'linux') {
  execSync(`xdg-open ${reportUrl}`);
}
```

## Complete Test Workflow

### 1. Run Tests with PM2 Services

```bash
# Start PM2 services before tests
pnpm test:pm2:start

# Run Playwright tests
pnpm test:e2e

# Get service URLs
pnpm playwright:url

# Open report in browser
```

### 2. View Traces for Failed Tests

```bash
# Ensure trace viewer is running
pm2 start playwright-trace-viewer

# Get trace viewer URL
pnpm playwright:url

# Navigate to URL and open trace files from test-results/
```

### 3. Clean Up

```bash
# Stop all test services
pnpm test:pm2:stop

# Clear logs
pm2 flush
```

## Service Health Monitoring

### Check Service Status

```bash
# Detailed status for all services
pm2 status

# Detailed info for specific service
pm2 show playwright-report-server

# Monitor in real-time
pm2 monit
```

### Auto-Restart on Failure

PM2 automatically restarts failed services. Configure restart behavior:

```javascript
{
  name: 'playwright-report-server',
  script: 'npx',
  args: 'playwright show-report',
  watch: false,
  autorestart: true,
  max_restarts: 3,
  min_uptime: '10s',
}
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :9323
lsof -i :9324

# Kill the process
kill -9 $(lsof -t -i :9323)

# Or use PM2 to stop the service
pm2 stop playwright-report-server
```

### Service Won't Start

```bash
# Check PM2 logs
pm2 logs playwright-report-server --nostream

# Check if report directory exists
ls -la playwright-report/

# Verify port is available
netstat -an | grep 9323
```

### URL Not Accessible

```bash
# Verify service is running
pm2 status

# Check service is listening on all interfaces
netstat -an | grep 9323

# For Coder environments, verify environment variables
echo $CODER_WORKSPACE
echo $CODER_OWNER
echo $CODER_DOMAIN

# Test local access
curl http://localhost:9323
```

### PM2 Not Persisting Services

```bash
# Save current process list
pm2 save

# Setup startup script (runs on system boot)
pm2 startup
# Follow the instructions output by the command
```

## Alternative: Simple HTTP Server

If you don't need PM2's process management, use a simple HTTP server:

```bash
# Using Python
cd playwright-report && python3 -m http.server 9323

# Using Node.js http-server
npx http-server playwright-report -p 9323

# Using serve
npx serve playwright-report -l 9323
```

## Quick Reference

| Task | Command |
|------|---------|
| Start all services | `pm2 start pm2.test.config.js` |
| Stop all services | `pm2 delete all` |
| View status | `pm2 status` |
| View logs | `pm2 logs --nostream` |
| Get URLs | `pnpm playwright:url` |
| Restart service | `pm2 restart playwright-report-server` |
| Show service info | `pm2 show playwright-report-server` |
| Monitor real-time | `pm2 monit` |

---

**Remember**: PM2 is ideal for persistent test services in development. Use dynamic URL generation for cloud workspaces, and always clean up services when done to free ports.
