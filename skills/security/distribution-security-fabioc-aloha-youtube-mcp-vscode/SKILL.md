---
name: "distribution-security"
description: "Defense-in-depth, PII protection, secrets scanning, and secure packaging for distributed software"
metadata:
  inheritance: inheritable
---

# Distribution Security

> Multi-layer security for software that ships to users — secrets scanning, permission minimization, and secure UI patterns.

**Scope**: Inheritable skill. Covers defense-in-depth architecture, PII protection, secrets scanning, permission minimization, CSP patterns, and secure WebView communication.

## Defense-in-Depth Architecture

### 4-Layer Security Model

Every distributed application needs four independent security layers:

| Layer | Function | Failure Mode |
|-------|----------|-------------|
| 1. **Authentication** | Verify identity (OAuth, MSAL, API keys) | Unauthorized access |
| 2. **Authorization** | Role-based access control (RBAC) | Privilege escalation |
| 3. **Secrets Scanning** | Detect leaked credentials in source | Data breach |
| 4. **Audit Logging** | Record all security-relevant events | Undetected compromise |

**Rule**: Each layer must work independently. A failure in Layer 1 should not cascade — Layer 2 still blocks unauthorized actions, Layer 3 still catches leaked keys, Layer 4 still records the attempt.

## PII Protection

### 3-Layer Exclusion Model

For projects that package and distribute source files:

| Layer | Implementation | Catches |
|-------|---------------|---------|
| 1. **`.gitignore`** | Exclude from version control | Personal config, local data |
| 2. **`.vscodeignore`** / build exclusions | Exclude from package | Dev-only files, test data |
| 3. **Build pipeline scan** | Regex validation gate | Anything layers 1-2 missed |

### Personal Data Rules

| Location | Allowed? | Alternative |
|----------|---------|------------|
| Source code headers | No | Use team/org name |
| `package.json` author | Org name only | `"author": "Team Name"` |
| README credits | Generic unless opted in | "Created by the team" |
| Error messages | No PII ever | Use error codes |
| Telemetry | No PII without consent | Anonymized identifiers |

**Rationale**: Users installing software see `package.json` and source headers. Personal names create trust concerns and privacy issues.

## Secrets Scanning

### Detection Patterns

| Pattern | Regex | Severity |
|---------|-------|----------|
| API keys | `/[A-Za-z0-9_\-]{32,}/` | High |
| Connection strings | `/Server=.*;[P]assword=.*/i` | Critical |
| JWT tokens | `/eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+/` | Critical |
| Private keys | `/-----BEGIN.*PRIVATE KEY-----/` | Critical |
| Azure keys | `/[A-Za-z0-9+/]{86}==/` | High |

### False Positive Reduction

Naive regex scanning floods developers with noise. Filter these contexts:

| Context | Example | Action |
|---------|---------|--------|
| Import statements | `import { KEY_LENGTH } from...` | Skip |
| Comments explaining patterns | `// API keys look like: abc123...` | Skip |
| Env variable definitions | `const API_KEY = process.env.KEY` | Skip (value is reference) |
| Test fixtures with dummy data | `const testKey = "test-key-1234"` | Skip if in test folder |
| Actual hardcoded secrets | `const key = "sk-live-abc123..."` | ALERT |

**Rule**: Only alert on literal string values that match secret patterns outside of comments, imports, and environment variable references.

### Priority Matrix for Findings

When security audits surface findings, triage with this matrix:

| Priority | Criteria | SLA |
|----------|---------|-----|
| **P0** | Active secret exposure, data breach | Immediate (hours) |
| **P1** | Vulnerability in auth/authz layer | 24 hours |
| **P2** | Missing security control (no CSP, etc.) | Sprint |
| **P3** | Best practice gap (logging format, etc.) | Backlog |

## Permission Minimization

### The Less-Is-More Principle

Request ONLY the permissions your software actually uses:

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| Request `Mail.Send` for reading contacts | Users fear email spam | Request `Contacts.Read` only |
| Request admin scopes "for future use" | Over-privileged from day one | Request when feature ships |
| Broad `*` scopes | No granular control | Request specific sub-scopes |

**Rule**: Users evaluate trust based on the scariest permission requested. One unnecessary permission can tank adoption.

### Permission Audit Checklist

For every capability that requires a permission:

1. Is this the **minimum** scope that enables the feature?
2. Can this be a **delegated** permission (user context) instead of application?
3. Can this be requested **just-in-time** instead of at install?
4. Does the permission description match what users **expect**?
5. Can we **function without** this permission (graceful degradation)?

## Content Security Policy (CSP)

### Secure UI Patterns

For WebViews, panels, and embedded web content:

| Anti-pattern | Problem | Secure Alternative |
|-------------|---------|-------------------|
| `onclick="handler()"` | Inline scripts violate CSP | `data-cmd` attribute + delegated listener |
| `eval()` | Code injection vector | Pre-compiled templates |
| `innerHTML = userInput` | XSS vulnerability | `textContent` or sanitized HTML |
| `<script src="cdn">` | External dependency risk | Bundle locally |

### Data-Cmd Pattern

Replace inline event handlers with data attributes:

```html
<!-- Anti-pattern: inline handler (blocked by CSP) -->
<button onclick="doThing()">Click</button>

<!-- Secure: data-cmd + delegated listener -->
<button data-cmd="do-thing">Click</button>

<script>
  document.addEventListener('click', (e) => {
    const cmd = e.target.closest('[data-cmd]')?.dataset.cmd;
    if (cmd) handleCommand(cmd);
  });
</script>
```

## WebView Security

### Communication Pattern

WebViews run in sandboxed iframes. Communication must use message passing:

| Direction | Method | Example |
|-----------|--------|---------|
| Extension → WebView | `webview.postMessage(data)` | Send state updates |
| WebView → Extension | `vscode.postMessage(data)` | Report user actions |
| WebView → External URL | **BLOCKED** | `window.open()` silently fails |
| WebView → Local files | Via extension only | Request through message |

**Critical**: `window.open()` silently fails in WebViews. Links that need to open externally must send a message to the extension, which calls `vscode.env.openExternal()`.

### Message Validation

Always validate messages on both sides:

```typescript
// Extension side - validate WebView messages
panel.webview.onDidReceiveMessage((msg) => {
  if (!msg.type || typeof msg.type !== 'string') return;
  switch (msg.type) {
    case 'save': handleSave(msg.data); break;
    case 'navigate': handleNavigate(msg.url); break;
    // Ignore unknown message types
  }
});
```

## Kill Switch Pattern

### Multi-Layer Protection for Destructive Operations

For operations that could cause irreversible damage:

| Layer | Implementation | Purpose |
|-------|---------------|---------|
| 1. **Marker file** | Presence of protection file blocks operation | Static guard |
| 2. **Confirmation dialog** | "Are you sure?" prompt | User intent validation |
| 3. **Typed confirmation** | User must type exact phrase | Prevent accidental clicks |
| 4. **Cooldown timer** | Wait N seconds before enabling action | Prevent impulse actions |
| 5. **Audit log** | Record who triggered what and when | Post-incident analysis |

**Rule**: The confirmation dialog ("I Understand" button) must STILL block the destructive action even if earlier layers fail. Each layer is independent.

## Security Testing

### Test Priority Order

When adding test coverage to security-critical code:

| Tier | Coverage Target | What to Test |
|------|----------------|-------------|
| 1. Auth/AuthZ | 80%+ first | Token validation, role checks, permission gates |
| 2. Input validation | 80%+ next | Sanitization, bounds, injection prevention |
| 3. Secrets handling | Full coverage | No secrets in logs, proper encryption |
| 4. UI/cosmetic | After security | Layout, theming, preferences |

**Rule**: Achieve 80%+ coverage on Tier 1 before touching Tier 4. In a resource-constrained sprint, security tests win over UI tests every time.

## SFI Compliance (Azure/Microsoft)

### Audit Scope

Security audits must scan the full subscription, not just infrastructure-as-code:

| Method | Covers | Misses |
|--------|--------|--------|
| IaC scanning (Bicep/Terraform) | Declared resources | Manually created resources |
| `az resource list --subscription X` | All resources | Config drift within resources |
| Azure Policy + Defender | Compliance posture | Application-level vulns |

**Rule**: Always combine IaC scanning with live subscription scanning. Manual portal clicks create resources that IaC scans will never find.
