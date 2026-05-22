---
name: reviewing-casbin
description: Review Go code using Casbin authorization for security issues, model correctness, policy design, and common anti-patterns. Use when reviewing PRs with Casbin code or auditing authorization implementations.
version: 1.0.0
---

# Casbin Authorization Code Review

## Purpose

Review Go code using Casbin for authorization to identify security vulnerabilities, model configuration errors, and common anti-patterns. Ensures RBAC/ABAC implementations follow best practices.

## When NOT to Use

- Initial Casbin setup (use `implementing-casbin` skill instead)
- Learning Casbin basics (refer to documentation)
- Non-Go Casbin implementations

---

## Review Workflow

### Step 1: Identify Casbin Files

```bash
# Find all files using Casbin
grep -r "casbin" --include="*.go" -l

# Find enforcement points
grep -r "Enforce\|AddPolicy\|NewEnforcer" --include="*.go" -l

# Find model files
find . -name "*.conf" | xargs grep -l "request_definition"
```

### Step 2: Run Automated Checks

```bash
# Find ignored errors (CRITICAL)
grep -rn "NewEnforcer.*_\|Enforce.*_" --include="*.go"

# Find unsafe type assertions (CRITICAL)
grep -rn "\.Value.*\)\.\(string\|int\)" --include="*.go" | grep -v ", ok"

# Find hardcoded policies (MEDIUM)
grep -rn "AddPolicy\|AddRoleForUser" --include="*.go" | grep -v "_test.go"
```

### Step 3: Review Critical Areas

Review each area in priority order (see Critical Review Areas below).

### Step 4: Generate Report

Use the Review Output Template to document findings.

---

## Critical Review Areas

### 1. Model File Errors (CRITICAL)

**Check for missing role definition in RBAC models:**

```ini
# FAIL: Missing role definition
[request_definition]
r = sub, obj, act
[policy_definition]
p = sub, obj, act
# Missing: [role_definition] g = _, _
[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj  # g() undefined!

# PASS: Complete RBAC model
[role_definition]
g = _, _
[matchers]
m = g(r.sub, p.sub) && keyMatch2(r.obj, p.obj) && r.act == p.act
```

**Check for wrong matcher function:**

| Pattern Type | Use Function |
|--------------|--------------|
| `/users/:id` | `keyMatch2` |
| `/users/{id}` | `keyMatch3` |
| `/users/*` | `keyMatch` |

### 2. Enforcer Initialization (CRITICAL)

```go
// FAIL: Ignoring errors
e, _ := casbin.NewEnforcer(modelPath, adapter)

// FAIL: Hardcoded paths
e, _ := casbin.NewEnforcer("/app/model.conf", adapter)

// FAIL: Missing auto-save
e, _ := casbin.NewEnforcer(modelPath, adapter)
// No EnableAutoSave(true)

// PASS: Proper initialization
e, err := casbin.NewEnforcer(cfg.ModelPath, adapter)
if err != nil {
    return nil, fmt.Errorf("create enforcer: %w", err)
}
e.EnableAutoSave(true)
```

### 3. Middleware Security (CRITICAL)

```go
// FAIL: Unsafe type assertion (panic risk)
user := r.Context().Value("userID").(string)

// FAIL: No authentication check before authorization
func Authorize(e *casbin.Enforcer) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            user := r.Context().Value("userID").(string)
            // Proceeds without checking if user is authenticated

// PASS: Safe context extraction
user, ok := r.Context().Value("userID").(string)
if !ok || user == "" {
    http.Error(w, "Unauthorized", http.StatusUnauthorized)
    return
}
```

### 4. Error Handling in Enforce (HIGH)

```go
// FAIL: Ignoring enforce errors
ok, _ := e.Enforce(user, obj, act)

// FAIL: Wrong HTTP status code
if !allowed {
    http.Error(w, "Unauthorized", http.StatusUnauthorized)  // Wrong!
}

// PASS: Proper error handling and status codes
allowed, err := e.Enforce(user, obj, act)
if err != nil {
    http.Error(w, "Authorization error", http.StatusInternalServerError)
    return
}
if !allowed {
    http.Error(w, "Forbidden", http.StatusForbidden)  // 403, not 401
    return
}
```

**Status Code Guide:**
- `401 Unauthorized`: User not authenticated (who are you?)
- `403 Forbidden`: User authenticated but not permitted (you can't do this)

### 5. Policy Thread Safety (HIGH)

```go
// FAIL: Concurrent policy modification
go func() { e.AddPolicy("alice", "/api", "GET") }()
go func() { e.RemovePolicy("bob", "/api", "GET") }()

// PASS: Use SyncedEnforcer
e, _ := casbin.NewSyncedEnforcer(model, adapter)

// PASS: Or single-writer pattern with mutex
```

### 6. Missing Authorization Checks (HIGH)

Look for:
- Endpoints without authorization middleware
- Inconsistent middleware application
- Missing resource-level authorization
- Admin endpoints without extra protection

### 7. Hardcoded Policies (MEDIUM)

```go
// FAIL: Policies in code (not maintainable)
e.AddPolicy("admin", "/api/users/*", "GET")
e.AddRoleForUser("alice", "admin")

// PASS: Policies in database via admin interface
// Code only initializes enforcer, policies managed externally
```

### 8. Performance Issues (MEDIUM)

```go
// FAIL: Enforce in loop (N+1 problem)
for _, item := range items {
    if allowed, _ := e.Enforce(user, item.Path, "read"); allowed {
        result = append(result, item)
    }
}

// PASS: Batch enforcement
requests := make([][]interface{}, len(items))
for i, item := range items {
    requests[i] = []interface{}{user, item.Path, "read"}
}
results, _ := e.BatchEnforce(requests)
```

### 9. ABAC Nil Safety (MEDIUM)

```go
// FAIL: Nil resource causes panic in ABAC
e.Enforce(user, resource, "read")

// PASS: Validate before enforce
if resource == nil {
    return false, errors.New("resource cannot be nil")
}
allowed, err := e.Enforce(user, resource, "read")
```

### 10. Test Coverage (LOW)

Check for:
- Unit tests for policy rules
- Middleware integration tests
- Table-driven permission scenario tests
- Edge case coverage (empty user, nil resource)

---

## Review Output Template

```markdown
## Casbin Authorization Review: [File/PR]

### Summary
[1-2 sentence overview]

### Critical Issues
- [ ] [Issue] - [file:line]

### High Priority
- [ ] [Issue] - [file:line]

### Medium Priority
- [ ] [Issue] - [file:line]

### Security Checklist
- [ ] All endpoints have authorization middleware
- [ ] Authentication verified before authorization
- [ ] 401 vs 403 used correctly
- [ ] No hardcoded policies in production code
- [ ] SyncedEnforcer used for concurrent access

### Model Checklist
- [ ] Model file syntax correct
- [ ] Role definition present for RBAC
- [ ] Correct matcher function for path patterns
- [ ] Policy effect appropriate (allow/deny)

### Code Quality Checklist
- [ ] All Enforce errors handled
- [ ] Context extraction uses safe type assertion
- [ ] Batch enforcement for loops
- [ ] Tests cover policy scenarios

### Passed Checks
- [x] [What's correct]
```

---

## Quick Commands

```bash
# Full review scan
grep -rn "casbin\|Enforce\|AddPolicy" --include="*.go"

# Find security issues
grep -rn "Enforce.*_\|\.Value.*\)\.\(string" --include="*.go"

# Check model files
find . -name "*.conf" -exec cat {} \;

# Find missing tests
grep -rL "Enforce" --include="*_test.go" $(grep -rl "Enforce" --include="*.go" | grep -v _test.go)
```

---

## Integration with Other Skills

- **implementing-casbin**: Reference for correct patterns
- **error-handling-audit**: Go error handling review
- **quality-check**: General code quality checks
- **go-code-reviewer**: Comprehensive Go review

---

## References

- [Casbin Documentation](https://casbin.org/docs/en/overview)
- [GORM Adapter](https://github.com/casbin/gorm-adapter)
- See `implementing-casbin` skill for implementation guidance
