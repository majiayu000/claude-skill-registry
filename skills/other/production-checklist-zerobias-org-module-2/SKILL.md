---
name: production-checklist
description: Production readiness checklist before module release
---

# Production Readiness Checklist

## 🚨 MANDATORY - Must Pass Before Module Release

### 1. Security Requirements
- [ ] **NO plaintext credentials** in code, comments, or logs
- [ ] **NO sensitive data** in error messages
- [ ] **NO API keys** hardcoded anywhere
- [ ] **NO passwords** visible in any form
- [ ] **NO PII** in logs or test fixtures
- [ ] All credentials from ConnectionProfile only

### 2. Error Handling
- [ ] All errors use core error types
- [ ] Error messages are helpful but don't leak sensitive info
- [ ] Only log error messages when wrapping into core errors
- [ ] No stack traces exposed to users
- [ ] Proper HTTP status mapping to core errors

### 3. Code Quality
- [ ] Build passes with exit code 0
- [ ] All tests pass (unit and integration)
- [ ] No lint errors or warnings
- [ ] No TypeScript errors
- [ ] No use of `!` (non-null assertion)
- [ ] All mappers use `const output: Type` pattern

### 4. Documentation
- [ ] USERGUIDE.md complete with:
  - [ ] How to obtain credentials
  - [ ] Connection profile structure
  - [ ] Required permissions
  - [ ] Troubleshooting section
- [ ] README.md only if special requirements
- [ ] All operations documented in API spec
- [ ] Examples work correctly

### 5. API Specification
- [ ] All 12 critical rules followed
- [ ] No root-level servers or security
- [ ] All properties camelCase
- [ ] Pagination using standard patterns
- [ ] All operations from original request implemented

### 6. Implementation
- [ ] ConnectionState.yml if needed (tokens, sessions)
- [ ] All mappers validate required fields
- [ ] PagedResults uses manual assignment
- [ ] No environment variables used
- [ ] Proper type imports from core packages

### 7. Testing
- [ ] Integration tests prepared (may fail without creds)
- [ ] Unit tests with sanitized fixtures
- [ ] No skipped tests
- [ ] No `.only()` in tests
- [ ] Test data sanitized (no PII)
- [ ] Read-only operations tested on production when possible

### 8. Examples
- [ ] Connection example works
- [ ] At least one operation example works
- [ ] Examples use realistic data
- [ ] Examples don't contain real credentials

## 🟡 WARNINGS - Should Be Fixed

### Performance
- [ ] Reasonable timeout values
- [ ] No unnecessary API calls
- [ ] Efficient pagination handling

### Maintenance
- [ ] Clear code structure
- [ ] Consistent naming
- [ ] No commented-out code
- [ ] No console.log statements

## 🟢 NICE TO HAVE

### Developer Experience
- [ ] Helpful error messages
- [ ] Clear function names
- [ ] Logical file organization
- [ ] Consistent patterns

## Validation Commands

Run these before marking complete:

```bash
# Security check
grep -r "password\|secret\|key\|token" src/ --exclude="*.ts"

# Build validation
npm run clean
npm run build

# Test validation
npm run test
npm run test:integration

# Lint check
npm run lint

# Check for console.log
grep -r "console.log" src/

# Check for non-null assertions
grep -r "!" src/ | grep -v "!=" | grep -v "!=="

# Check for skipped tests
grep -r ".skip\|.only" test/
```

## Sign-off Criteria

✅ Module is ready when:
1. All mandatory items checked
2. Build and tests pass
3. Documentation complete
4. Examples work
5. No security issues
6. No breaking changes to existing operations

## Important Reminders

- **Never write to production** during testing unless explicitly required
- **Never log sensitive data** even in development
- **Always validate inputs** before using them
- **Always use core error types** never generic Error
- **Always follow the rules** even if external API doesn't

## Logging Policy

**What to log**:
- Error messages when wrapping to core errors

**What NOT to log**:
- Request/response bodies
- Headers with auth info
- Any credentials
- User data
- Debug information
- Performance metrics

**No logging for**:
- Health checks
- Metrics
- Debug mode
- Observability

The module should be silent except for errors.
