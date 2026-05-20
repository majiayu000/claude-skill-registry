---
name: deploy
description: Build, deploy, and test NiFi E2E environment (Docker containers)
user-invocable: true
allowed-tools: Bash, Read, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__find, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__browser_wait_for
---

# NiFi E2E Deployment Skill

Manages the Docker-based NiFi + Keycloak test environment for E2E testing.

## Parameters

Optional argument selects the workflow:
- `/deploy` or `/deploy status` — Show container status
- `/deploy start` — First-time start (build NAR + start containers)
- `/deploy redeploy` — Redeploy after code changes (rebuild NAR + restart NiFi only)
- `/deploy test` — Run E2E Playwright tests (containers must be running)
- `/deploy test <file>` — Run specific E2E test file
- `/deploy stop` — Stop all containers
- `/deploy full` — Full CI workflow: stop → build → start → test → stop
- `/deploy troubleshoot` — Diagnose common issues

## Workflow

### Step 1: Determine Action

Parse the argument to determine which workflow to execute. Default (no args) = show status.

### Step 2: Execute Action

#### status (default)
```bash
./integration-testing/src/main/docker/check-status.sh --quiet
```

#### start
```bash
./integration-testing/src/main/docker/run-and-deploy.sh
```
Builds NAR, copies to `target/nifi-deploy/`, starts Keycloak + NiFi.
NiFi takes ~60-80s to become healthy. URLs after start:
- NiFi: https://localhost:9095/nifi (testUser / drowssap)
- Keycloak: https://localhost:9085 (admin / admin)

**After containers are healthy, run the [NiFi Browser Login](#nifi-browser-login) procedure, then display the [Sandbox Credentials](#sandbox-credentials).**

#### redeploy
```bash
./integration-testing/src/main/docker/redeploy-nifi.sh
```
Rebuilds NAR, copies to deploy dir, runs `docker compose restart nifi`.
Wait ~60-80s for NiFi to become healthy.
Verify: `./integration-testing/src/main/docker/check-status.sh`

**After NiFi is healthy, run the [NiFi Browser Login](#nifi-browser-login) procedure, then display the [Sandbox Credentials](#sandbox-credentials).**

#### test [file]
```bash
cd e-2-e-playwright && npm run playwright:test [-- tests/<file>.spec.js]
```
Containers MUST be running. Use `/deploy start` first if needed.

#### stop
```bash
cd integration-testing/src/main/docker && docker compose down -v
```

#### full
```bash
cd integration-testing/src/main/docker && docker compose down -v
cd <project-root>
./mvnw clean install
./mvnw verify -Pintegration-tests -pl e-2-e-playwright -am
```
IMPORTANT: Maven manages its own container lifecycle. Do NOT have manually-started containers running.

#### troubleshoot
Check for common issues in order:
1. `docker ps` — Are containers running? Any orphaned containers on ports 7777/9095/9443?
2. `docker compose -f integration-testing/src/main/docker/docker-compose.yml ps` — Container states
3. Port conflicts: `lsof -i :7777 -i :9095 -i :9443 2>/dev/null`
4. NiFi logs: `docker logs docker-nifi-1 --tail 50`
5. NAR loaded: `docker logs docker-nifi-1 2>&1 | grep -i cuioss`

## NiFi Browser Login

After every **start** or **redeploy**, open Chrome and log in to NiFi.

**Prerequisites:** The user must have accepted the self-signed certificate for `https://localhost:9095` in Chrome beforehand. If the browser shows a certificate error page, ask the user to manually accept the certificate (Advanced → Proceed) and then retry.

**CRITICAL — Chrome extension false negatives:**
The `tabs_context_mcp` call frequently returns "Browser extension is not connected" even when the extension IS connected and working. This is a transient MCP initialization issue, NOT an actual disconnection. You MUST retry up to **5 times** before concluding the extension is truly disconnected. NEVER tell the user the extension is disconnected based on failed calls alone — just keep retrying silently. In practice, the extension is almost always connected; failures resolve after 1-5 retries.

**Login steps:**

1. Call `tabs_context_mcp` with `createIfEmpty: true`. If it returns "not connected", retry up to 5 times (no delay needed between retries). Only after 5 consecutive failures should you ask the user to check the extension.
2. Create a new tab with `tabs_create_mcp`
3. Navigate to `https://localhost:9095/nifi/` — this redirects to NiFi's own login page (`#/login`)
4. Take a screenshot to see the current page state
5. Click the Username input field and type `testUser`
6. Click the Password input field and type `drowssap`
7. Click the "Log in" button
8. Wait until the URL contains `#/process-groups/` and the page title is "NiFi Flow" to verify a successful login
9. Report login success to the user

**Notes:**
- This is NiFi's built-in login form — **not** Keycloak. The login page URL is `https://localhost:9095/nifi/#/login`.
- If the URL already contains `#/process-groups/` after navigation, the user is already logged in — skip the login steps.
- If NiFi is still starting and the page doesn't load, wait a few seconds and retry navigation.
- Use `computer` tool with coordinate-based clicks for the login form — `find` and `read_page` can be unreliable inside NiFi's Angular UI.

## Critical Rules

- Maven E2E (`./mvnw verify -Pintegration-tests`) automatically stops existing containers before starting fresh ones (via fixed `deploy-and-start.sh`)
- After `./mvnw clean install`, the NAR in `target/nifi-deploy/` is stale — must run `/deploy redeploy` to update running containers
- NiFi loads NARs only at startup — code changes require container restart, not just file copy
- The `target/nifi-deploy/` directory is volume-mounted into the NiFi container

## Key Paths

| Path | Purpose |
|------|---------|
| `target/nifi-deploy/` | NAR deployment dir (Docker volume mount) |
| `integration-testing/src/main/docker/docker-compose.yml` | Docker Compose config |
| `integration-testing/src/main/docker/*.sh` | Local deployment scripts |
| `e-2-e-playwright/scripts/*.sh` | Maven-phase scripts |
| `e-2-e-playwright/target/test-results/` | Test artifacts |

## Sandbox Credentials

After a successful **start** or **redeploy** (and browser login), display these credentials to the user so they can use the Token Fetch form in the Endpunkt-Tester tab:

```
Sandbox Keycloak Credentials (for Token Fetch)
───────────────────────────────────────────────
Realm:         oauth_integration_tests
Client-ID:     test_client
Client-Secret: yTKslWLtf4giJcWCaoVJ20H8sy6STexM

ROPC (password grant):
  Username:    testUser
  Password:    drowssap

Token Endpoint (auto-discovered via issuer):
  https://keycloak:8443/realms/oauth_integration_tests/protocol/openid-connect/token

Other realm (for cross-issuer testing):
  Realm:         other_realm
  Client-ID:     other_client
  Client-Secret: otherClientSecretValue123456789
  Username:      otherUser / drowssap
```

**Note:** The issuer dropdown in the Endpunkt-Tester auto-populates from the processor's Controller Service config. The token endpoint is resolved via OIDC discovery when clicking "Ermitteln".

## NiFi Custom UI Browser Verification

The Custom UI runs inside an iframe. To access it manually:
1. Navigate to `https://localhost:9095/nifi/`
2. Double-click process group to enter it
3. Right-click processor → look for "Advanced" menu item
4. If not visible: click "Configure" → click Custom UI icon (top-right of dialog, red sticky-note icon)
5. Custom UI loads in iframe with `?id={processorId}` query parameter
