---
name: raccoon-audit
description: Rummage through code with curious precision, inspecting every corner for security risks and cleaning up what doesn't belong. Use when auditing security, finding secrets, removing dead code, or sanitizing before deployment.
---

# Raccoon Audit 🦝

The raccoon is curious. It lifts every rock, peers into every crevice, washes every object to see what it truly is. Nothing escapes those clever paws. What looks clean on the surface reveals its secrets under inspection. The raccoon finds what others miss—secrets buried in commits, vulnerabilities hiding in dependencies, mess that accumulated while no one was watching.

## When to Activate

- User asks to "audit security" or "check for secrets"
- User says "clean this up" or "sanitize before deploy"
- User calls `/raccoon-audit` or mentions raccoon/cleanup
- Before deploying to production (security sweep)
- When inheriting a codebase (unknown risks)
- After security incidents (post-mortem audit)
- Removing unused code, dependencies, or features
- Preparing for open source release (scrubbing internals)

**Pair with:** `spider-weave` for auth security, `beaver-build` for testing security fixes

---

## The Audit

```
RUMMAGE → INSPECT → SANITIZE → PURGE → VERIFY
    ↓         ↓          ↓         ↓         ↓
Search   Examine   Cleanse   Remove   Confirm
Everything  Closely   Contaminated Dead     Clean
```

### Phase 1: RUMMAGE

*Little paws lift the rocks, curious eyes peer underneath...*

Systematic search for things that don't belong:

**Secret Detection:**
```bash
# Search for common secret patterns
grep -r "api_key\|apikey\|api-key" . --include="*.{js,ts,py,json,yaml,yml,env,md}" 2>/dev/null | head -20
grep -r "password\|passwd\|pwd" . --include="*.{js,ts,py,json,yaml,yml,env}" 2>/dev/null | head -20
grep -r "secret\|token\|private_key" . --include="*.{js,ts,py,json,yaml,yml,env}" 2>/dev/null | head -20
grep -r "AKIA[0-9A-Z]{16}" . 2>/dev/null  # AWS access keys
grep -r "ghp_[a-zA-Z0-9]{36}" . 2>/dev/null  # GitHub personal tokens
```

**Common Hiding Spots:**
- `.env` files (should be in `.gitignore`)
- `config.json` with hardcoded values
- Test fixtures with real credentials
- Documentation examples that look too real
- Commented-out code containing keys
- Git history (check `git log -p` for deleted secrets)

**Bare Error Detection (Signpost Compliance):**

Grove requires all errors to use Signpost codes. Search for violations:

```bash
# Find bare throw error() without throwGroveError
grep -r "throw error(" --include="*.ts" --include="*.js" | grep -v "throwGroveError\|node_modules\|\.test\."

# Find ad-hoc JSON error responses without buildErrorJson
grep -r "json.*error.*status" --include="*.ts" | grep -v "buildErrorJson\|node_modules"

# Find console.error without logGroveError
grep -r "console\.error" --include="*.ts" --include="*.svelte" | grep -v "logGroveError\|node_modules"

# Find bare alert() where toast should be used
grep -r "alert(" --include="*.svelte" --include="*.ts" | grep -v "node_modules"
```

**Signpost Compliance Checklist:**
- [ ] No bare `throw error()` — use `throwGroveError()` or `buildErrorJson()`
- [ ] No `console.error` without `logGroveError()` companion
- [ ] No ad-hoc JSON error shapes — all use `buildErrorJson()`
- [ ] No `alert()` — use `toast` from `@autumnsgrove/groveengine/ui`
- [ ] `adminMessage` never exposed to client responses

**Dependency Check:**
```bash
# Check for known vulnerabilities
npm audit
pip audit  # if using Python
```

**Output:** Inventory of potential secrets, vulnerabilities, and suspicious patterns found

---

### Phase 2: INSPECT

*The raccoon washes the object, turning it over in careful paws...*

Examine findings to separate real risks from false positives:

**Secret Validation:**
For each potential secret found:
1. **Is it a real secret?** — Test if the key/token works
2. **Is it active?** — Check creation date, last used
3. **What's the blast radius?** — What can this access?
4. **How exposed?** — Public repo, internal, just local?

**Vulnerability Assessment:**
```
┌──────────────────────────────────────────────────────────────┐
│                  RISK EVALUATION MATRIX                      │
├──────────────────────────────────────────────────────────────┤
│  CRITICAL  │  Active secrets in public repos                │
│            │  SQL injection vulnerabilities                 │
│            │  Remote code execution paths                   │
├────────────┼────────────────────────────────────────────────┤
│  HIGH      │  Dependencies with known CVEs                  │
│            │  Weak cryptography (MD5, SHA1)                 │
│            │  Missing authentication on admin endpoints     │
├────────────┼────────────────────────────────────────────────┤
│  MEDIUM    │  Information disclosure in error messages      │
│            │  Missing rate limiting                         │
│            │  Verbose logging of sensitive data             │
├────────────┼────────────────────────────────────────────────┤
│  LOW       │  Outdated dependencies (no known CVEs)         │
│            │  Unused code/dependencies                      │
│            │  Comments containing internal details          │
└────────────┴────────────────────────────────────────────────┘
```

**Code Smell Inspection:**
- Functions that bypass security checks
- Debug flags left enabled
- Hardcoded URLs that should be configurable
- TODO comments about security issues
- Disabled tests (especially security-related ones)

**Output:** Prioritized list of confirmed issues with severity ratings

---

### Phase 3: SANITIZE

*Contaminated objects get scrubbed until they gleam...*

Clean up the mess without breaking functionality:

**Secret Rotation (if exposed):**
```bash
# 1. Revoke the exposed secret immediately
curl -X DELETE https://api.service.com/keys/EXPOSED_KEY_ID \
  -H "Authorization: Bearer ADMIN_TOKEN"

# 2. Generate new secret
NEW_KEY=$(curl -X POST https://api.service.com/keys \
  -H "Authorization: Bearer ADMIN_TOKEN" | jq -r '.key')

# 3. Update configuration (environment variables, not code!)
echo "SERVICE_API_KEY=$NEW_KEY" >> .env.local
```

**Code Sanitization:**
```typescript
// BEFORE: Secret in code
const API_KEY = 'sk-live-abc123xyz789';

// AFTER: Environment variable
const API_KEY = process.env.SERVICE_API_KEY;
if (!API_KEY) {
  throw new Error('SERVICE_API_KEY environment variable required');
}
```

**Security Hardening:**
```typescript
// Add input validation
function sanitizeInput(input: string): string {
  return input.replace(/[<>\"']/g, '');
}

// Add rate limiting
const rateLimiter = new Map<string, number[]>();

// Remove debug endpoints
// DELETE: app.get('/debug/users', ...)
```

**Dependency Updates:**
```bash
# Update vulnerable packages
npm update package-name
# or
pip install --upgrade package-name

# Verify fix
npm audit  # Should show 0 vulnerabilities
```

**Output:** Clean code with secrets externalized, vulnerabilities patched

---

### Phase 4: PURGE

*What doesn't belong gets carried away, never to return...*

Remove the harmful remnants:

**Git History Cleaning (if secrets were committed):**
```bash
# Use BFG Repo-Cleaner or git-filter-branch
# WARNING: This rewrites history - coordinate with team!

# BFG approach (recommended):
bfg --delete-files '.*env' --replace-text secrets.txt my-repo.git

# Or specific file cleanup:
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secret-file' \
  --prune-empty --tag-name-filter cat -- --all
```

**Dead Code Removal:**
```bash
# Find unused exports
npx ts-prune  # TypeScript

# Find unused dependencies
npx depcheck

# Remove with confidence after tests pass
git rm src/old-feature/
npm uninstall unused-package
```

**Environment Cleanup:**
- Remove old API keys from services
- Delete test accounts created with real credentials
- Clear CI/CD cache if it contains secrets
- Rotate database credentials if exposed

**Documentation Updates:**
- Remove internal URLs from public docs
- Scrub employee names/IDs from examples
- Update architecture diagrams (remove sensitive details)

**Output:** Clean repository, fresh credentials, purged history

---

### Phase 5: VERIFY

*The raccoon washes its paws, inspecting them one last time...*

Confirm everything is clean and stays clean:

**Automated Verification:**
```bash
# Re-run secret scan - should find nothing
grep -r "sk-live\|sk-test" . --include="*.{js,ts,json}" 2>/dev/null

# Security tests pass
npm run test:security

# No new vulnerabilities
npm audit --audit-level=moderate
```

**Manual Checks:**
- [ ] Application starts without hardcoded secrets
- [ ] All environment variables documented (not their values!)
- [ ] Test suite passes
- [ ] No sensitive data in logs
- [ ] Error messages don't reveal internals

**Preventive Measures:**
```bash
# Install pre-commit hooks
npm install --save-dev husky
npx husky add .husky/pre-commit "npm run lint && npm run security-check"

# Add to CI/CD pipeline
# .github/workflows/security.yml
- name: Security Scan
  run: |
    npm audit --audit-level=moderate
    npx secretlint "**/*"
```

**Verification Report:**
```markdown
## 🦝 RACCOON AUDIT COMPLETE

### Secrets Found & Fixed
| Location | Severity | Action Taken |
|----------|----------|--------------|
| config.ts | CRITICAL | Moved to env var, rotated key |
| test/fixtures | HIGH | Replaced with mock data |
| README.md | MEDIUM | Removed internal URL |

### Dependencies
- 3 vulnerabilities patched
- 2 unused packages removed
- All packages up to date

### Verification
- [x] No secrets in current codebase
- [x] Git history cleaned (force push required)
- [x] Pre-commit hooks installed
- [x] All tests passing
```

**Output:** Clean bill of health with preventive measures in place

---

## Raccoon Rules

### Curiosity
Inspect everything. The raccoon doesn't assume— it verifies. That "harmless" test file might contain production credentials.

### Thoroughness
Wash every object. Half-cleaned secrets are still exposed secrets. Don't stop at the surface.

### Safety
Handle contaminated items carefully. When rotating secrets, ensure zero-downtime transitions. Don't break production while fixing security.

### Communication
Use investigative metaphors:
- "Lifting the rocks..." (searching thoroughly)
- "Washing the object..." (examining closely)
- "Scrubbing clean..." (sanitizing)
- "Carrying away..." (purging)

---

## Anti-Patterns

**The raccoon does NOT:**
- Leave secrets in code with "TODO: remove this" comments
- Skip git history when secrets were committed
- Break production while rotating credentials
- Assume "it's just a test key" means it's safe
- Forget to update documentation after cleanup
- Trust that "someone else handled it"

---

## Example Audit

**User:** "Audit the codebase before open sourcing"

**Raccoon flow:**

1. 🦝 **RUMMAGE** — "Found 3 API keys in config files, internal URLs in README, employee emails in test data, 12 TODO comments with internal ticket numbers"

2. 🦝 **INSPECT** — "One API key is active production key (CRITICAL). Others are test keys but still shouldn't be public. Internal URLs expose infrastructure."

3. 🦝 **SANITIZE** — "Move keys to env vars, replace URLs with example.com, scrub employee data, rewrite TODOs generically"

4. 🦝 **PURGE** — "Use BFG to clean git history of secrets, remove 2 unused dependencies, delete old deployment scripts"

5. 🦝 **VERIFY** — "Re-scan shows no secrets, all tests pass, pre-commit hooks installed to prevent future secrets"

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| Secret committed to git | Rotate immediately, clean history, force push |
| Vulnerability in dependency | Update to patched version, test, deploy |
| Hardcoded credentials | Move to environment variables, rotate keys |
| Dead code detected | Remove if tests pass, document if uncertain |
| Debug code in production | Remove endpoints, check logs for exposure |
| Preparing for open source | Full audit: secrets, internals, history, docs |

---

## Integration with Other Skills

**Before Audit:**
- `bloodhound-scout` — Understand codebase structure first

**During Audit:**
- `spider-weave` — If auth/security system needs review
- `beaver-build` — If writing security regression tests

**After Audit:**
- `panther-strike` — If fixing specific security issues rapidly
- `grove-documentation` — Update security runbooks

---

*Nothing stays hidden from paws that know how to look.* 🦝
