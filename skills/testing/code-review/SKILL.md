---
name: code-review
description: Review, analyze, and inspect code for Photo Map MVP project following
  Spring Boot, Angular 18, and shared project conventions. Check security, performance,
  naming, testing, and MVP scope compliance. U
---

---
name: code-review
description: Review, analyze, and inspect code for Photo Map MVP project following Spring Boot, Angular 18, and shared project conventions. Check security, performance, naming, testing, and MVP scope compliance. Use when reviewing pull requests, conducting code audits, analyzing code quality, inspecting Java or TypeScript files, or ensuring quality before commits. File types: .java, .ts, .html, .xml, .properties, .css, .scss
allowed-tools: Read, Grep, Glob
---

# Code Review - Photo Map MVP

**Note:** This is a READ-ONLY Skill (allowed-tools: Read, Grep, Glob only).

## Review Philosophy

**MVP-First Mindset:**
- ✅ Simple, working solution over complex, perfect solution
- ✅ Security-first (user scoping, input validation, JWT)
- ✅ Code readability (self-documenting, English names)
- ❌ NO over-engineering
- ❌ NO features beyond MVP requirements

**Read-Only Workflow:**
Use Read, Grep, Glob to analyze code. Provide findings as comments. Never edit code directly.

---

## When to Review

**Decision Tree:**

| Scenario | Action |
|----------|--------|
| Pre-commit review | Check Security + Architecture + Tests |
| Pull Request review | Full review with `references/` checklists |
| Bug investigation | Focus on Security + Performance |
| Refactoring audit | Check Architecture + Anti-patterns |

---

## Review Workflows

### Backend Review (Spring Boot + Java 17)

**Priority Check Order:**
1. **Security (CRITICAL!)** → `references/security-patterns.md`
   - User scoping on ALL photo queries
   - JWT validation working
   - Input validation present
   - No entities exposed to API

2. **Architecture** → `references/backend-checklist.md`
   - Controllers → Services → Repositories
   - DTOs used for all API responses
   - `@Transactional` on service methods

3. **Testing** → `references/backend-checklist.md`
   - Service logic tested (>70% coverage)
   - Custom queries tested
   - Security configuration tested

**Quick Scan:**
- Grep for `findById\(` without `userId` parameter → Security issue!
- Grep for `return new Photo\(` in Controller → Entity exposure!
- Grep for business logic in `@RestController` → Architecture violation!

**Examples:** Check `examples/user-scoping.java` for bad vs good patterns.

---

### Frontend Review (Angular 18 + TypeScript)

**Priority Check Order:**
1. **Architecture (CRITICAL!)** → `references/frontend-checklist.md`
   - NO `@NgModule` anywhere (standalone only!)
   - `inject()` function used (not constructor)
   - BehaviorSubject kept private

2. **State Management** → `references/frontend-checklist.md`
   - Signals for component-local state
   - BehaviorSubject for shared state (services)
   - Async pipe over manual subscriptions

3. **Testing** → `references/frontend-checklist.md`
   - Component logic tested
   - Service methods tested (HTTP mocked)
   - Guards tested

**Quick Scan:**
- Grep for `@NgModule` → Angular 18 violation!
- Grep for `constructor.*inject\(` → Should use inject() function!
- Grep for `public.*BehaviorSubject` → Exposed state management!

**Examples:**
- `examples/standalone-patterns.ts` - NgModule vs Standalone
- `examples/state-management.ts` - BehaviorSubject patterns

---

### Security Review

**Critical Checks:**
- **User Scoping:** ALL photo queries include `userId` filtering
- **JWT Validation:** Token signature & expiration checked
- **Input Validation:** `@Valid` on DTOs, file upload validation
- **No Data Leaks:** Entities never exposed, DTOs only

**Detailed Patterns:** `references/security-patterns.md`

**Examples:** `examples/user-scoping.java` for complete patterns

---

### Performance Review

**Backend Checks:**
- Database indexes on `user_id`, frequently queried columns
- `@Transactional(readOnly = true)` on queries
- `FetchType.LAZY` for relationships
- ❌ NO premature optimization (Redis, queues)

**Frontend Checks:**
- Lazy loading images in gallery
- Async pipe (automatic subscription cleanup)
- TrackBy for *ngFor lists
- ❌ NO premature optimization (Virtual Scroll, Service Workers)

**Detailed Patterns:** `references/performance-review.md`

---

## Common Anti-Patterns

**Quick Scan List:**

**Backend:**
- ❌ Business logic in Controller
- ❌ Exposing entities to API
- ❌ No user scoping on queries
- ❌ No `@Transactional` on service methods

**Frontend:**
- ❌ `@NgModule` usage (Angular 18!)
- ❌ Constructor injection instead of `inject()`
- ❌ Exposed BehaviorSubject (public)
- ❌ Nested subscriptions (use `switchMap`)

**Complete List:** `examples/common-anti-patterns.md`

---

## Git Commit Review

**Check:**
- ✅ Conventional Commits format: `type(scope): description`
- ✅ Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- ✅ NO promotional messages ("Generated with Claude Code")
- ✅ Clear, focused commits (single change)
- ✅ Imperative mood ("add" not "added")

**Detailed Standards:** `references/git-standards.md`

---

## Quick Reference

### Reference Lookup

| Need | Check |
|------|-------|
| Backend security, architecture, testing | `references/backend-checklist.md` |
| Frontend standalone, DI, state, testing | `references/frontend-checklist.md` |
| User scoping, JWT, input validation | `references/security-patterns.md` |
| Performance checks (backend + frontend) | `references/performance-review.md` |
| Conventional Commits, PR review | `references/git-standards.md` |

### Example Lookup

| Need | Check |
|------|-------|
| User scoping patterns (bad vs good) | `examples/user-scoping.java` |
| Standalone components (NgModule vs Standalone) | `examples/standalone-patterns.ts` |
| BehaviorSubject patterns (private vs public) | `examples/state-management.ts` |
| Common mistakes quick scan | `examples/common-anti-patterns.md` |

---

## Review Checklist Summary

**Before Approval:**

**Security:**
- [ ] User scoping on all photo queries
- [ ] JWT validation working
- [ ] Input validation present
- [ ] No entities exposed to API

**Architecture:**
- [ ] Backend: Controllers → Services → Repositories
- [ ] Frontend: Standalone components, inject(), BehaviorSubject pattern
- [ ] NO NgModules in Angular code
- [ ] DTOs used for all API responses

**Testing:**
- [ ] Service logic tested (>70% coverage)
- [ ] Component logic tested
- [ ] Custom queries tested
- [ ] Guards tested

**Code Quality:**
- [ ] English naming conventions
- [ ] Self-documenting code
- [ ] Minimal comments
- [ ] No over-engineering

**MVP Scope:**
- [ ] Only features from `.ai/prd.md`
- [ ] No premature optimization
- [ ] Simple solutions

**For detailed checklists:** Check `references/backend-checklist.md` and `references/frontend-checklist.md`

---

## Related Documentation

**Project Context:**
- `.ai/prd.md` - MVP scope and requirements
- `.ai/tech-stack.md` - Technology specifications
- `.ai/api-plan.md` - Backend API specification
- `.ai/ui-plan.md` - Frontend architecture

**Skill Resources:**
- `references/` - Detailed review checklists (loaded on demand)
- `examples/` - Code examples (bad vs good patterns)
