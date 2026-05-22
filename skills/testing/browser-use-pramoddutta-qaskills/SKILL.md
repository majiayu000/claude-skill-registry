---
name: Browser-Use Automation
description: CLI tool for persistent browser automation with multi-session support, featuring Chromium/Real/Remote browser modes, cookie management, JavaScript execution, and long-running automation workflows.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [browser-automation, persistent-sessions, multi-session, cookie-management, chromium, cli, javascript-execution]
testingTypes: [e2e, integration, performance]
frameworks: []
languages: [javascript, typescript, python]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Browser-Use Automation Skill

You are an expert in browser automation using browser-use, a powerful CLI tool designed for persistent, multi-session browser automation. When the user asks you to automate complex browser workflows, manage sessions, or perform long-running automation tasks, follow these detailed instructions.

## Core Principles

1. **Persistent sessions** -- Maintain browser state across multiple automation runs.
2. **Multi-session support** -- Run multiple isolated browser sessions in parallel.
3. **Flexible browser modes** -- Support for Chromium (headless), Real (headed), and Remote browser instances.
4. **Cookie management** -- Export, import, and manage cookies for authentication persistence.
5. **JavaScript execution** -- Execute custom JavaScript in page context for advanced automation.

## Installation

```bash
# Install via npm
npm install -g browser-use

# Or use with npx
npx browser-use --version

# Install with Python
pip install browser-use

# Verify installation
browser-use --help
```

## Browser Modes

### Chromium Mode (Default Headless)

```bash
# Launch Chromium in headless mode
browser-use start --mode chromium --headless

# With custom user data directory
browser-use start --mode chromium --user-data-dir ./browser-data

# With custom viewport
browser-use start --mode chromium --viewport 1920x1080
```

### Real Browser Mode (Headed)

```bash
# Launch visible Chrome browser
browser-use start --mode real --browser chrome

# Launch Firefox
browser-use start --mode real --browser firefox

# Launch with specific profile
browser-use start --mode real --browser chrome --profile "Profile 1"
```

### Remote Browser Mode

```bash
# Connect to remote Chrome DevTools Protocol
browser-use start --mode remote --cdp-url ws://localhost:9222

# Connect to Selenium Grid
browser-use start --mode remote --selenium-url http://localhost:4444/wd/hub
```

## Session Management

### Creating and Managing Sessions

```bash
# Create named session
browser-use session create --name "user-session-1" --persist

# List all sessions
browser-use session list

# Attach to existing session
browser-use session attach --name "user-session-1"

# Delete session
browser-use session delete --name "user-session-1"

# Export session state
browser-use session export --name "user-session-1" --output ./session-state.json

# Import session state
browser-use session import --input ./session-state.json --name "restored-session"
```

**Session List Output:**
```json
{
  "sessions": [
    {
      "name": "user-session-1",
      "id": "abc123",
      "created": "2024-02-12T10:00:00Z",
      "lastActive": "2024-02-12T10:30:00Z",
      "persistent": true,
      "tabs": 3
    },
    {
      "name": "test-session-2",
      "id": "def456",
      "created": "2024-02-12T11:00:00Z",
      "lastActive": "2024-02-12T11:15:00Z",
      "persistent": false,
      "tabs": 1
    }
  ]
}
```

### Multi-Session Parallel Execution

```bash
# Run multiple sessions in parallel
browser-use parallel --sessions "session-1,session-2,session-3" \
  --command "navigate --url https://example.com"

# Run different commands per session
browser-use parallel \
  --session session-1 --command "navigate --url https://site1.com" \
  --session session-2 --command "navigate --url https://site2.com" \
  --session session-3 --command "navigate --url https://site3.com"
```

## Cookie Management

### Export and Import Cookies

```bash
# Export cookies from session
browser-use cookies export --session "user-session-1" --output cookies.json

# Export specific domain cookies
browser-use cookies export --session "user-session-1" --domain "example.com" --output example-cookies.json

# Import cookies into session
browser-use cookies import --session "user-session-1" --input cookies.json

# Import cookies for specific domain
browser-use cookies import --session "user-session-1" --input auth-cookies.json --domain "app.example.com"

# Clear all cookies
browser-use cookies clear --session "user-session-1"

# Clear cookies for specific domain
browser-use cookies clear --session "user-session-1" --domain "example.com"
```

**Cookie Export Format:**
```json
{
  "cookies": [
    {
      "name": "session_token",
      "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "domain": ".example.com",
      "path": "/",
      "expires": 1707753600,
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax"
    },
    {
      "name": "user_preferences",
      "value": "theme=dark&lang=en",
      "domain": "app.example.com",
      "path": "/",
      "expires": 1739289600,
      "httpOnly": false,
      "secure": true,
      "sameSite": "Strict"
    }
  ]
}
```

### Cookie-Based Authentication Persistence

```bash
#!/bin/bash
# auth-persist.sh - Login once, reuse session

SESSION_NAME="authenticated-user"

# Check if session exists
if browser-use session list | grep -q "$SESSION_NAME"; then
  echo "Using existing authenticated session"
  browser-use session attach --name "$SESSION_NAME"
else
  echo "Creating new authenticated session"
  browser-use session create --name "$SESSION_NAME" --persist

  # Perform login
  browser-use navigate --url "https://app.example.com/login"
  browser-use type --selector "#email" --text "user@example.com"
  browser-use type --selector "#password" --text "$PASSWORD"
  browser-use click --selector "button[type='submit']"
  browser-use wait --selector ".dashboard" --timeout 10000

  # Export cookies for backup
  browser-use cookies export --session "$SESSION_NAME" --output auth-cookies.json
  echo "Session authenticated and cookies saved"
fi

# Now use authenticated session
browser-use navigate --url "https://app.example.com/dashboard"
```

## JavaScript Execution

### Execute JavaScript in Page Context

```bash
# Execute simple JavaScript
browser-use execute --script "return document.title"

# Execute with arguments
browser-use execute --script "return arguments[0] + arguments[1]" --args "[5, 10]"

# Execute and save result
browser-use execute --script "return document.querySelectorAll('.item').length" --output item-count.json

# Execute script from file
browser-use execute --script-file ./custom-script.js
```

**Example Script File (custom-script.js):**
```javascript
// Extract all product data from page
const products = Array.from(document.querySelectorAll('.product-card')).map(card => {
  return {
    name: card.querySelector('.product-name')?.textContent.trim(),
    price: card.querySelector('.product-price')?.textContent.trim(),
    image: card.querySelector('.product-image')?.src,
    rating: card.querySelector('.rating')?.getAttribute('data-rating'),
    available: !card.querySelector('.out-of-stock')
  };
});

return { products, total: products.length };
```

```bash
# Execute the script
browser-use execute --script-file ./extract-products.js --output products.json
```

### Advanced JavaScript Patterns

```bash
# Wait for dynamic content with custom condition
browser-use execute --script "
  return new Promise(resolve => {
    const check = () => {
      if (document.querySelectorAll('.loaded-item').length >= 10) {
        resolve(true);
      } else {
        setTimeout(check, 100);
      }
    };
    check();
  });
"

# Manipulate page elements
browser-use execute --script "
  document.querySelectorAll('.annoying-popup').forEach(el => el.remove());
  document.body.style.backgroundColor = '#f0f0f0';
  return 'Page modified';
"

# Trigger events
browser-use execute --script "
  const event = new Event('custom-event');
  document.dispatchEvent(event);
  return 'Event triggered';
"
```

## Navigation and Page Interaction

### Advanced Navigation

```bash
# Navigate with custom headers
browser-use navigate --url "https://api.example.com" \
  --headers '{"Authorization": "Bearer token123", "X-Custom": "value"}'

# Navigate with POST data
browser-use navigate --url "https://example.com/search" \
  --method POST \
  --data '{"query": "automation", "filters": ["category:tools"]}'

# Navigate with referer
browser-use navigate --url "https://example.com/protected" \
  --referer "https://example.com/home"

# Navigate and wait for specific event
browser-use navigate --url "https://example.com" \
  --wait-for-event "load"
```

### Page Interaction Commands

```bash
# Scroll to element
browser-use scroll --selector ".footer" --behavior smooth

# Scroll by pixels
browser-use scroll --delta "0,500"

# Scroll to top/bottom
browser-use scroll --position top
browser-use scroll --position bottom

# Hover over element
browser-use hover --selector ".dropdown-trigger"

# Focus element
browser-use focus --selector "input#search"

# Select dropdown option
browser-use select --selector "select#country" --value "US"

# Upload file
browser-use upload --selector "input[type='file']" --file ./document.pdf

# Download file
browser-use download --url "https://example.com/file.pdf" --output ./downloaded.pdf
```

## Tab Management

### Multi-Tab Operations

```bash
# Open new tab
browser-use tab new --url "https://example.com"

# List all tabs
browser-use tab list

# Switch to tab by index
browser-use tab switch --index 0

# Switch to tab by URL pattern
browser-use tab switch --url-pattern "example.com"

# Close tab
browser-use tab close --index 1

# Close all tabs except current
browser-use tab close --others

# Duplicate tab
browser-use tab duplicate --index 0
```

**Tab List Output:**
```json
{
  "tabs": [
    {
      "index": 0,
      "url": "https://example.com",
      "title": "Example Domain",
      "active": true
    },
    {
      "index": 1,
      "url": "https://google.com",
      "title": "Google",
      "active": false
    }
  ],
  "total": 2
}
```

## Network Monitoring and Interception

### Monitor Network Requests

```bash
# Start network monitoring
browser-use network start --filter "*.json"

# Navigate and capture requests
browser-use navigate --url "https://api.example.com"

# Get network log
browser-use network log --output network-requests.json

# Stop monitoring
browser-use network stop
```

**Network Log Format:**
```json
{
  "requests": [
    {
      "url": "https://api.example.com/users",
      "method": "GET",
      "status": 200,
      "responseTime": 234,
      "size": 1024,
      "timestamp": "2024-02-12T10:30:00Z"
    }
  ]
}
```

### Request Interception

```bash
# Intercept and modify requests
browser-use intercept --pattern "*/api/*" \
  --modify-headers '{"X-Custom-Header": "value"}' \
  --modify-response-status 200

# Block specific requests
browser-use intercept --pattern "*.jpg" --block

# Mock API responses
browser-use intercept --pattern "*/api/users" \
  --mock-response ./mock-users.json
```

## TypeScript/JavaScript Integration

```typescript
import { BrowserUse } from 'browser-use';

interface BrowserUseConfig {
  mode: 'chromium' | 'real' | 'remote';
  headless?: boolean;
  viewport?: { width: number; height: number };
  userDataDir?: string;
}

class BrowserAutomation {
  private browser: BrowserUse;
  private sessionName: string;

  constructor(sessionName: string, config: BrowserUseConfig = { mode: 'chromium' }) {
    this.sessionName = sessionName;
    this.browser = new BrowserUse(config);
  }

  async start(): Promise<void> {
    await this.browser.session.create({
      name: this.sessionName,
      persist: true,
    });
  }

  async navigate(url: string, options?: { waitUntil?: string }): Promise<void> {
    await this.browser.navigate({ url, ...options });
  }

  async executeScript<T>(script: string | Function, args: any[] = []): Promise<T> {
    const scriptStr = typeof script === 'function' ? script.toString() : script;
    const result = await this.browser.execute({
      script: scriptStr,
      args,
    });
    return result.value as T;
  }

  async saveAuthCookies(filepath: string): Promise<void> {
    await this.browser.cookies.export({
      session: this.sessionName,
      output: filepath,
    });
  }

  async loadAuthCookies(filepath: string): Promise<void> {
    await this.browser.cookies.import({
      session: this.sessionName,
      input: filepath,
    });
  }

  async cleanup(): Promise<void> {
    await this.browser.session.delete({ name: this.sessionName });
  }
}

// Usage example
async function automateWorkflow() {
  const automation = new BrowserAutomation('my-workflow-session');

  try {
    await automation.start();

    // Check if we have saved auth cookies
    const cookiesExist = await fs.promises.access('./auth-cookies.json')
      .then(() => true)
      .catch(() => false);

    if (cookiesExist) {
      // Restore authenticated session
      await automation.loadAuthCookies('./auth-cookies.json');
      await automation.navigate('https://app.example.com/dashboard');
    } else {
      // Perform fresh login
      await automation.navigate('https://app.example.com/login');
      // ... login steps ...
      await automation.saveAuthCookies('./auth-cookies.json');
    }

    // Execute custom JavaScript
    const itemCount = await automation.executeScript<number>(() => {
      return document.querySelectorAll('.item').length;
    });

    console.log(`Found ${itemCount} items on page`);

  } finally {
    await automation.cleanup();
  }
}
```

## Python Integration

```python
import json
from browser_use import BrowserUse

class BrowserAutomation:
    def __init__(self, session_name: str, mode: str = "chromium", headless: bool = True):
        self.session_name = session_name
        self.browser = BrowserUse(mode=mode, headless=headless)

    def start(self):
        self.browser.session.create(name=self.session_name, persist=True)

    def navigate(self, url: str, wait_until: str = "load"):
        self.browser.navigate(url=url, wait_until=wait_until)

    def execute_script(self, script: str, *args):
        return self.browser.execute(script=script, args=list(args))

    def save_cookies(self, filepath: str):
        self.browser.cookies.export(session=self.session_name, output=filepath)

    def load_cookies(self, filepath: str):
        self.browser.cookies.import_(session=self.session_name, input=filepath)

    def cleanup(self):
        self.browser.session.delete(name=self.session_name)

# Usage
def main():
    automation = BrowserAutomation("my-session")

    try:
        automation.start()

        # Try to restore session
        try:
            automation.load_cookies("auth-cookies.json")
            automation.navigate("https://app.example.com/dashboard")
            print("Restored authenticated session")
        except FileNotFoundError:
            # Fresh login
            automation.navigate("https://app.example.com/login")
            # ... perform login ...
            automation.save_cookies("auth-cookies.json")
            print("New session authenticated")

        # Extract data with JavaScript
        data = automation.execute_script("""
            return Array.from(document.querySelectorAll('.data-item')).map(el => ({
                id: el.dataset.id,
                text: el.textContent.trim()
            }));
        """)

        print(f"Extracted {len(data)} items")

    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()
```

## Advanced Patterns

### Long-Running Monitoring

```bash
#!/bin/bash
# monitor-site.sh - Continuous site monitoring

SESSION="monitor-session"
INTERVAL=300  # 5 minutes

browser-use session create --name "$SESSION" --persist
browser-use navigate --url "https://status.example.com"

while true; do
  # Execute monitoring script
  STATUS=$(browser-use execute --script "
    const statusEl = document.querySelector('.status-indicator');
    return {
      status: statusEl.textContent,
      color: getComputedStyle(statusEl).backgroundColor,
      timestamp: new Date().toISOString()
    };
  ")

  echo "$(date): $STATUS" >> monitor.log

  # Check for failures
  if echo "$STATUS" | grep -q "down"; then
    browser-use snapshot --output "failure-$(date +%s).png"
    # Send alert
    curl -X POST https://alerts.example.com/notify -d "$STATUS"
  fi

  sleep $INTERVAL
  browser-use execute --script "location.reload()"
done
```

### Parallel Session Processing

```typescript
async function processMultipleAccounts(accounts: Array<{ email: string; password: string }>) {
  const sessions = await Promise.all(
    accounts.map(async (account, index) => {
      const sessionName = `account-${index}`;
      const browser = new BrowserAutomation(sessionName);

      await browser.start();
      await browser.navigate('https://app.example.com/login');

      // Login for each account
      await browser.executeScript((email: string, password: string) => {
        (document.querySelector('#email') as HTMLInputElement).value = email;
        (document.querySelector('#password') as HTMLInputElement).value = password;
        (document.querySelector('button[type="submit"]') as HTMLButtonElement).click();
      }, account.email, account.password);

      // Wait for dashboard
      await new Promise(resolve => setTimeout(resolve, 3000));

      // Save session
      await browser.saveAuthCookies(`./cookies-${index}.json`);

      return browser;
    })
  );

  return sessions;
}
```

## Best Practices

1. **Use persistent sessions** for workflows requiring authentication state.
2. **Export cookies regularly** to recover from session failures.
3. **Name sessions descriptively** to identify purpose when listing sessions.
4. **Clean up sessions** after completion to avoid resource leaks.
5. **Use JavaScript execution** for complex data extraction that CLI commands can't handle.
6. **Monitor network requests** to verify API interactions and troubleshoot issues.
7. **Implement retry logic** for transient failures in long-running automations.
8. **Use multi-session parallelism** to process multiple accounts or sites simultaneously.
9. **Validate session state** before critical operations to ensure authentication persists.
10. **Document session requirements** for each automation workflow.

## Anti-Patterns to Avoid

1. **Not cleaning up sessions** -- Leads to resource exhaustion.
2. **Hardcoding credentials** -- Use environment variables or secure vaults.
3. **Ignoring session expiration** -- Implement cookie refresh or re-authentication.
4. **Over-reliance on delays** -- Use event-based waiting instead of fixed sleeps.
5. **Single session for parallel tasks** -- Creates race conditions and state conflicts.
6. **Not backing up cookies** -- Session loss requires re-authentication.
7. **Ignoring network errors** -- Implement proper error handling and retries.
8. **Mixing session contexts** -- Keep sessions isolated to avoid state bleeding.
9. **Not validating JavaScript results** -- Always check return values for expected structure.
10. **Running too many parallel sessions** -- Respect system resources and rate limits.

## Debugging and Troubleshooting

### Enable Debug Mode

```bash
# Verbose logging
browser-use --debug navigate --url "https://example.com"

# Save console output
browser-use --console-output ./console.log navigate --url "https://example.com"

# Take screenshot on error
browser-use --screenshot-on-error ./errors/ navigate --url "https://example.com"

# Show DevTools
browser-use start --mode real --devtools
```

### Session Recovery

```bash
# Check session health
browser-use session health --name "my-session"

# Recover corrupted session
browser-use session recover --name "my-session" --backup ./session-backup.json

# Force delete stuck session
browser-use session delete --name "my-session" --force
```

## Integration with CI/CD

```yaml
# .github/workflows/browser-automation.yml
name: Browser Automation Tests

on: [push, pull_request]

jobs:
  automation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install browser-use
        run: npm install -g browser-use

      - name: Run automation tests
        env:
          APP_PASSWORD: ${{ secrets.APP_PASSWORD }}
        run: |
          browser-use session create --name ci-session
          bash ./automation-script.sh
          browser-use session delete --name ci-session

      - name: Upload artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: failure-screenshots
          path: ./screenshots/
```

This skill enables powerful, persistent browser automation with session management, making it ideal for long-running workflows, authenticated applications, and complex multi-step automations that AI agents need to orchestrate.
