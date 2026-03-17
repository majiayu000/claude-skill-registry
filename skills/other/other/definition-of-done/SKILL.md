---
name: definition-of-done
description: Verify all Definition of Done criteria before marking a feature complete
disable-model-invocation: true
argument-hint: [feature name]
---

# Definition of Done Verification

Verify completion criteria for: $ARGUMENTS

## Checklist

A feature is ONLY complete when ALL of the following pass:

### 1. Backend Compilation
```bash
./mvnw compile
```
- [ ] Compiles without errors

### 2. Frontend Compilation
```bash
cd /home/reuben/Documents/workspace/past-care-spring-frontend && ng build --configuration=production
```
- [ ] Builds without errors

### 3. Backend Tests
```bash
./mvnw test
```
- [ ] All tests pass

### 4. Frontend Unit Tests
```bash
cd /home/reuben/Documents/workspace/past-care-spring-frontend && ng test --watch=false --browsers=ChromeHeadless
```
- [ ] All tests pass

### 5. E2E Tests
```bash
cd /home/reuben/Documents/workspace/past-care-spring-frontend && npx playwright test
```
- [ ] All tests pass

### 6. Documentation Updated
- [ ] README.md updated (if new feature)
- [ ] USER_GUIDE.md updated (if user-facing)
- [ ] API endpoints documented (if applicable)
- [ ] Last Updated date changed

## Documentation Files

| File | Location |
|------|----------|
| Backend README | `/home/reuben/Documents/workspace/pastcare-spring/README.md` |
| Frontend README | `/home/reuben/Documents/workspace/past-care-spring-frontend/README.md` |
| Backend User Guide | `/home/reuben/Documents/workspace/pastcare-spring/USER_GUIDE.md` |
| Frontend User Guide | `/home/reuben/Documents/workspace/past-care-spring-frontend/USER_GUIDE.md` |

## Additional Checks

### Security
- [ ] Tenant isolation verified (if service methods added)
- [ ] @Transactional on all tenant-scoped queries
- [ ] Custom @Query includes church filter
- [ ] No hardcoded secrets

### Code Quality
- [ ] No TODO comments left unresolved
- [ ] Error handling implemented
- [ ] Percentage calculations capped at 100%

### Permissions (if applicable)
- [ ] Permission added to `Permission.java`
- [ ] Permission added to `Role.java`
- [ ] Permission added to frontend `permission.enum.ts`
- [ ] Controller annotated with `@RequirePermission`

## Port Cleanup (if server was started)
```bash
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
```
Only run if you started the backend server during this task.

## Result

**DO NOT mark task complete until ALL checks pass.**

Report any failures with specific error messages.
