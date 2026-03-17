---
name: oauth-login
description: Complete OAuth login flow and store tokens for verification. Use when browser verification requires authenticated sessions.
argument-hint: <provider>
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion, WebFetch, mcp__playwright__*
---

Complete an OAuth login flow for browser verification. Opens a browser to the OAuth
consent page, waits for callback, and stores tokens in the project's `.env` file.

## Supported Providers

| Provider | OAuth 2.0 Endpoint | Scopes |
|----------|-------------------|--------|
| google | accounts.google.com | openid, email, profile |
| github | github.com/login/oauth | read:user, user:email |

## Usage

```
/oauth-login google
/oauth-login github
```

## Prerequisites

1. **OAuth App Credentials Required**

   Before running this command, the user must have created an OAuth application
   with the provider and have the client ID and secret ready.

   **Google:**
   - Go to https://console.cloud.google.com/apis/credentials
   - Create OAuth 2.0 Client ID (Web application)
   - Add authorized redirect URI: `http://localhost:3847/oauth/callback`

   **GitHub:**
   - Go to https://github.com/settings/developers
   - Create new OAuth App
   - Set callback URL: `http://localhost:3847/oauth/callback`

2. **Browser MCP Available**

   Playwright MCP or similar browser tool must be available for automated flow.

## Workflow

Copy this checklist and track progress:

```
OAuth Login Progress:
- [ ] Step 1: Check provider argument
- [ ] Step 2: Check for existing credentials
- [ ] Step 3: Collect OAuth app credentials
- [ ] Step 4: Generate state parameter
- [ ] Step 5: Build authorization URL
- [ ] Step 6: Start callback server
- [ ] Step 7: Open browser to auth URL
- [ ] Step 8: Wait for callback
- [ ] Step 9: Exchange code for tokens
- [ ] Step 10: Store tokens in .env
- [ ] Step 11: Verify token validity
- [ ] Step 12: Report success
```

### Step 1: Check Provider Argument

If `$1` is not provided or not recognized:

```
OAUTH LOGIN
===========

Usage: /oauth-login <provider>

Supported providers:
  google - Google OAuth 2.0
  github - GitHub OAuth

Example: /oauth-login google
```

### Step 2: Check for Existing Credentials

Read `.env` file and check for existing OAuth tokens:

```bash
grep -E "^OAUTH_(GOOGLE|GITHUB)_" .env 2>/dev/null || true
```

If tokens exist for this provider, ask:

```
Question: "OAuth tokens for {provider} already exist. What would you like to do?"
Header: "Existing tokens"
Options:
  - Label: "Refresh tokens"
    Description: "Re-authenticate and get new tokens"
  - Label: "Keep existing"
    Description: "Exit without changes"
```

### Step 3: Get Client Credentials

Use AskUserQuestion to collect OAuth app credentials:

```
Question: "Enter your {Provider} OAuth Client ID:"
Header: "Client ID"
```

Then:

```
Question: "Enter your {Provider} OAuth Client Secret:"
Header: "Client Secret"
```

### Step 4: Store Client Credentials

Add to `.env`:

```
OAUTH_{PROVIDER}_CLIENT_ID=<client_id>
OAUTH_{PROVIDER}_CLIENT_SECRET=<client_secret>
```

### Step 5: Start Local Callback Server

Create a temporary callback server to receive the OAuth code.

**EXECUTE this entire block** via the Bash tool (the JavaScript is written to a file, then executed):

```bash
# Create callback server script
cat > /tmp/oauth-callback-server.js << 'EOF'
const http = require('http');
const url = require('url');
const fs = require('fs');

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);

  if (parsedUrl.pathname === '/oauth/callback') {
    const code = parsedUrl.query.code;
    const error = parsedUrl.query.error;

    if (code) {
      fs.writeFileSync('/tmp/oauth-code.txt', code);
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end('<html><body><h1>✓ Authorization successful!</h1><p>You can close this window and return to Claude Code.</p></body></html>');
    } else {
      fs.writeFileSync('/tmp/oauth-error.txt', error || 'unknown');
      res.writeHead(400, {'Content-Type': 'text/html'});
      res.end('<html><body><h1>✗ Authorization failed</h1><p>Error: ' + (error || 'unknown') + '</p></body></html>');
    }

    setTimeout(() => server.close(), 1000);
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(3847, () => {
  console.log('OAuth callback server listening on http://localhost:3847');
});
EOF

# Start callback server as BACKGROUND PROCESS
node /tmp/oauth-callback-server.js &
CALLBACK_PID=$!
echo "Callback server started (PID: $CALLBACK_PID, background process)"

# Verify the server started successfully
sleep 1
curl -sf http://localhost:3847/ -o /dev/null 2>&1 || echo "WARNING: Callback server may not have started"
```

**Verify server is listening** before proceeding. If the server failed to start
(port in use, Node.js error), check the error output and try an alternate port
(3848, 3849) before continuing.

### Step 6: Build Authorization URL

**Google:**
```
https://accounts.google.com/o/oauth2/v2/auth?
  client_id={CLIENT_ID}&
  redirect_uri=http://localhost:3847/oauth/callback&
  response_type=code&
  scope=openid%20email%20profile&
  access_type=offline&
  prompt=consent
```

**GitHub:**
```
https://github.com/login/oauth/authorize?
  client_id={CLIENT_ID}&
  redirect_uri=http://localhost:3847/oauth/callback&
  scope=read:user%20user:email
```

### Step 7: Open Browser for Consent

Use Playwright MCP to open the authorization URL:

```
mcp__playwright__browser_navigate with url={auth_url}
```

Display to user:

```
OAUTH AUTHORIZATION
===================

Opening browser for {Provider} authorization...

Please complete the login in the browser window.
This command will wait for you to complete authorization.

If the browser doesn't open, visit this URL:
{auth_url}
```

### Step 8: Wait for Callback

Poll for the callback result:

```bash
# Wait up to 120 seconds for callback
for i in $(seq 1 120); do
  if [ -f /tmp/oauth-code.txt ]; then
    CODE=$(cat /tmp/oauth-code.txt)
    rm /tmp/oauth-code.txt
    break
  fi
  if [ -f /tmp/oauth-error.txt ]; then
    ERROR=$(cat /tmp/oauth-error.txt)
    rm /tmp/oauth-error.txt
    echo "OAuth error: $ERROR"
    exit 1
  fi
  sleep 1
done
```

### Step 9: Exchange Code for Tokens

**Google token exchange:**
```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "code=$CODE" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:3847/oauth/callback" \
  -d "grant_type=authorization_code"
```

**GitHub token exchange:**
```bash
curl -s -X POST https://github.com/login/oauth/access_token \
  -H "Accept: application/json" \
  -d "code=$CODE" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET"
```

Parse response for:
- `access_token`
- `refresh_token` (Google only)
- `expires_in`

After obtaining the token, verify it is valid by making a lightweight test API call (e.g., fetch the user profile endpoint). If the test call fails, report the token as invalid and retry the OAuth flow.

**Google verification:**
```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" https://www.googleapis.com/oauth2/v2/userinfo
```

**GitHub verification:**
```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" https://api.github.com/user
```

If the response indicates an error (HTTP 401 or invalid token), report: "Token verification failed — token appears invalid" and restart the OAuth flow from Step 5.

### Step 10: Store Tokens

Calculate expiry timestamp and store in `.env`:

```bash
EXPIRY=$(date -v+${EXPIRES_IN}S +%s 2>/dev/null || date -d "+${EXPIRES_IN} seconds" +%s)
```

Add/update in `.env`:

```
OAUTH_{PROVIDER}_ACCESS_TOKEN={access_token}
OAUTH_{PROVIDER}_REFRESH_TOKEN={refresh_token}
OAUTH_{PROVIDER}_TOKEN_EXPIRY={expiry_timestamp}
```

### Step 11: Update verification-config.json

Update `.claude/verification-config.json` to use OAuth:

```json
{
  "auth": {
    "strategy": "oauth",
    "provider": "{provider}",
    "tokenVar": "OAUTH_{PROVIDER}_ACCESS_TOKEN",
    "refreshTokenVar": "OAUTH_{PROVIDER}_REFRESH_TOKEN",
    "expiryVar": "OAUTH_{PROVIDER}_TOKEN_EXPIRY"
  }
}
```

### Step 12: Cleanup and Report

```bash
# Kill callback server if still running
kill $CALLBACK_PID 2>/dev/null || true
rm -f /tmp/oauth-callback-server.js /tmp/oauth-code.txt /tmp/oauth-error.txt
```

```
OAUTH LOGIN COMPLETE
====================

Provider: {Provider}
Access Token: Stored in .env as OAUTH_{PROVIDER}_ACCESS_TOKEN
Refresh Token: {Stored | Not provided (GitHub)}
Token Expiry: {date/time}

verification-config.json updated with OAuth settings.

The access token will be automatically refreshed before verification runs
if it's within 5 minutes of expiry.
```

## Token Refresh

This command also handles token refresh when called with `--refresh`:

```
/oauth-login google --refresh
```

**Refresh flow:**
1. Read `OAUTH_{PROVIDER}_REFRESH_TOKEN` from `.env`
2. If expiry is >5 min away, skip refresh
3. Otherwise, call refresh endpoint:

**Google refresh:**
```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "grant_type=refresh_token"
```

4. Update `OAUTH_{PROVIDER}_ACCESS_TOKEN` and `OAUTH_{PROVIDER}_TOKEN_EXPIRY` in `.env`

**Note:** GitHub tokens don't expire unless revoked, so no refresh needed.

## Error Handling

| Error | Action |
|-------|--------|
| Callback server port in use | Try port 3848, 3849, etc. |
| User cancels consent | Show error, suggest retry |
| Token exchange fails | Show API error, suggest checking credentials |
| Browser MCP unavailable | Provide manual URL, ask user to paste code |

## When Login Cannot Complete

**If user is still in browser after 120s timeout:**
- Do NOT close the browser or kill the callback server
- Report: "OAuth callback timeout reached (120s)"
- Ask user:
  - "Extend timeout by 60s" — Continue waiting
  - "Paste authorization code manually" — Fallback to manual entry
  - "Cancel and retry later" — Clean up and exit

**If browser MCP is completely unavailable:**
- Display the full authorization URL for manual copy
- Provide instructions: "Open this URL in your browser, then paste the authorization code when prompted"
- Wait for manual code entry
- Proceed with token exchange using manually provided code

**If OAuth app credentials are invalid:**
- Report the specific error from the provider (invalid_client, unauthorized, etc.)
- Suggest: "Verify client ID and secret match your OAuth app settings"
- Provide link to OAuth app settings page for the provider
- Exit cleanly without partial state

**If callback server cannot start on any port:**
- Report: "Unable to start callback server on ports 3847-3849"
- Suggest: "Check for processes using these ports: lsof -i :3847"
- Exit cleanly

## Security Notes

- Client secrets are stored in `.env` which should be in `.gitignore`
- Tokens are project-local, not shared across projects
- Refresh tokens are long-lived and should be treated as secrets
- The callback server only runs during authorization flow
