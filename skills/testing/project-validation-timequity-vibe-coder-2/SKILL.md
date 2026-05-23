---
name: project-validation
description: |
  Validates project after initialization. Checks static files, endpoints, CSS, health.
  Use when: after rust-project-init, before TDD loop.
  Triggers: "validate project", "check project", "verify init".
---

# Project Validation Skill

Validates that a project is correctly initialized and ready for development.

## When to Use

- After `Task[rust-project-init]` completes
- Before starting TDD loop in /ship
- When something doesn't work and you need to diagnose

## Validation Checks

### 1. Build Check
```bash
cargo build 2>&1 | tail -10
# Expected: "Finished" message, no errors
```

### 2. Health Endpoint
```bash
cargo run &
APP_PID=$!
sleep 3
curl -sf http://127.0.0.1:3000/health
# Expected: "ok" or 200 status
kill $APP_PID 2>/dev/null
```

### 3. Static Files (fullstack only)
```bash
curl -sI http://127.0.0.1:3000/static/styles.css | head -1
# Expected: HTTP/1.1 200 OK
```

### 4. Index Page
```bash
curl -s http://127.0.0.1:3000/ | grep -q "<html"
# Expected: exit code 0
```

### 5. HTMX Endpoints
```bash
# Parse templates for expected endpoints
grep -rh "hx-get\|hx-post\|hx-delete" templates/ 2>/dev/null | \
  grep -oE '"[^"]*"' | tr -d '"' | sort -u

# Each should return non-404
```

### 6. CSS Animation Safety
```bash
# Check for problematic opacity patterns
grep -n "opacity.*0" static/styles.css
grep -n "animation-fill-mode" static/styles.css
# Warn if opacity:0 without animation-fill-mode: both
```

### 7. Dependencies
```bash
# Check required features
grep "tower-http" Cargo.toml | grep -q "fs"
# Required for fullstack
```

## Script Usage

```bash
python3 scripts/validate_project.py --path /path/to/project
```

**Output:**
```
## Project Validation: /path/to/project

[PASS] Build succeeds
[PASS] Health endpoint responds
[PASS] Static files served
[PASS] Index returns HTML
[WARN] Endpoint /tags not implemented (expected by templates)
[PASS] CSS animations safe

Result: 5/6 checks passed, 1 warning

Issues to fix:
- Add handler for GET /tags
```

## Integration

Called automatically in:
- `rust-project-init.md` → Post-Init Validation section
- `ship.md` → Phase 2.5: Project Validation
