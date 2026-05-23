---
description: Software Architect technical refinement and DoR/DoD for [PROJECT_NAME]
globs: []
alwaysApply: false
---

# Architect Refinement Skill

> Project: [PROJECT_NAME]
> Generated: [DATE]
> Purpose: Guide for technical refinement of user stories

## When to Use

This skill guides you when doing technical refinement for:
- New stories in `/create-spec`
- Added stories in `/add-story`
- Quick tasks in `/add-todo`
- Bug stories in `/add-bug`

## Quick Reference

### Technical Refinement Process

1. **Understand Requirements**: Read fachliche story (Feature, Acceptance Criteria)
2. **Analyze Architecture**: What patterns apply?
3. **Determine WAS**: Which components to create/modify
4. **Determine WIE**: Architecture guidance and constraints
5. **Determine WO**: Which files to touch
6. **Define DoD**: Completion criteria
7. **Mark DoR**: All checkboxes [x] when ready

### Story is READY when

- [ ] Fachliche requirements clear
- [ ] Acceptance criteria specific and testable
- [ ] Technical approach defined (WAS/WIE/WO)
- [ ] Dependencies identified
- [ ] Story appropriately sized (max 5 files, 400 LOC)
- [ ] All betroffene Layer identified (Frontend/Backend/Database)
- [ ] Integration points documented (if Full-stack)

---

## Detailed Guidance

### WAS (What to Build)

**Components/Features to create or modify - NO CODE**

Examples:
- "User registration service"
- "Profile edit form component"
- "Email validation middleware"
- "User database migration"

**Anti-patterns:**
```
❌ "Add function validateEmail()"  // Too specific
✅ "Email validation logic"

❌ "Create UserController with create(), update() methods"  // Implementation details
✅ "User API endpoints"
```

### WIE (How/Architecture Guidance)

**Patterns and constraints - NO IMPLEMENTATION**

Examples:
- "Use Service Object pattern"
- "Follow existing UserController pattern"
- "No direct DB calls from controllers"
- "Requires rate limiting"
- "Use caching for performance"

**Anti-patterns:**
```
❌ "def create_user(params)..."  // Code implementation
✅ "Use Service Object pattern for business logic"

❌ "Add try-catch in line 45"  // Too specific
✅ "Implement error handling with custom exceptions"
```

### WO (Where/Files)

**File paths to create or modify - NO CONTENT**

Examples:
- "app/services/users/register.rb"
- "src/app/components/user-profile/"
- "db/migrate/[timestamp]_add_email_to_users.rb"

**Guidelines:**
- List all files that will be touched
- Include new files to create
- Include existing files to modify
- Be specific with paths

### Domain Reference (v3.0)

**NEW in v3.0:** Stories can reference domain areas

```markdown
**Domain:** user-registration
```

This tells the main agent:
- Which business process this affects
- Which domain doc to keep updated
- Business context to consider

### Layer Analysis

**Identify all affected layers:**

| Layer | Components | What Changes |
|-------|------------|--------------|
| Frontend | ProfileForm, Avatar component | New edit form, image upload |
| Backend | UserService, ProfileController | Update endpoint, validation |
| Database | users table | Add avatar_url column |
| DevOps | - | No changes |

**Integration Type:**
- Backend-only
- Frontend-only
- Full-stack

**Critical Integration Points (if Full-stack):**
- Backend API Response → Frontend Component
- Database Schema → Backend Query
- Frontend Form → Backend Validation

### DoD (Definition of Done)

**Start all items unchecked [ ]**

Standard DoD items:
```markdown
#### Implementierung
- [ ] Code implemented and follows style guide
- [ ] Architecture patterns followed (WIE section)
- [ ] Security/performance requirements met

#### Qualitätssicherung
- [ ] All acceptance criteria satisfied
- [ ] Unit tests written and passing
- [ ] Integration tests written (if applicable)
- [ ] Linter passes

#### Dokumentation
- [ ] Code is self-documenting or has comments
- [ ] No debug code left in
```

Add story-specific items based on requirements.

### Completion Check Commands

**Provide bash commands to verify story completion:**

```bash
# File existence
test -f src/app/components/profile/edit.component.ts && echo "Component OK"

# Content verification
grep -q "export class ProfileEditComponent" src/app/components/profile/edit.component.ts && echo "Class OK"

# Tests pass
npm test -- profile.component.spec.ts

# Linter
npm run lint
```

All commands must exit with code 0 for story to be DONE.

---

## Architecture Patterns Reference

### Common Patterns by Layer

**Frontend:**
- Smart vs Dumb Components
- Container/Presenter
- State Management (Context, Store, Signals)
- Form Validation

**Backend:**
- Service Objects
- Repository Pattern
- Controller → Service → Repository
- Result/Either Pattern

**API:**
- RESTful endpoints
- Request/Response DTOs
- Error handling
- Pagination

**Database:**
- Migration for schema changes
- Validations in model
- Scopes for queries
- Associations

### Security Checklist

- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Authentication required?
- [ ] Authorization rules defined?

### Performance Checklist

- [ ] N+1 queries avoided
- [ ] Large datasets paginated
- [ ] Caching considered
- [ ] Eager loading for associations
- [ ] Indexes on foreign keys

---

## Story Sizing Guidelines

### Maximum Limits
- **Files:** Max 5 files per story
- **LOC:** Max 400 lines of code
- **Complexity:** Max S (Small, 1-3 SP)
- **Concerns:** Single concern per story

### When to Split

Split story if:
- More than 5 files affected
- Multiple unrelated changes
- Can be done independently
- Different developers could work on parts

---

## Dependencies Analysis

### Types of Dependencies

**Hard Dependency (Sequential):**
```
Story A → Story B
Example: "User model" before "User registration"
```

**Soft Dependency (Optional):**
```
Story A ⇢ Story B (better if A done first)
Example: "Basic search" before "Advanced filters"
```

**No Dependency (Parallel):**
```
Story A ∥ Story B
Example: "Profile edit" and "Avatar upload" can be parallel
```

### How to Document

```markdown
**Abhängigkeiten:** STORY-001, STORY-003
```

Or if none:
```markdown
**Abhängigkeiten:** None
```

---

## v3.0 Changes

### What's Different

**REMOVED in v3.0:**
- ❌ No "WER" (Agent) field
- ❌ No "Relevante Skills" section
- ❌ No skill-index.md lookup

**ADDED in v3.0:**
- ✅ Optional "Domain" field
- ✅ Skills auto-load via globs during implementation

**Why:**
- Main agent implements directly (no delegation)
- Skills activate based on files edited
- Simpler story template
- Domain tracking for business docs

### Story Template Fields (v3.0)

```markdown
**Type**: Backend | Frontend | Full-Stack | DevOps
**Domain:** [optional - e.g., user-registration]
**Abhängigkeiten:** [Story IDs or None]

### Technical Details

**WAS:** Components to create/modify
**WIE:** Architecture patterns and constraints
**WO:** File paths
**Domain:** [Optional domain area]
**Geschätzte Komplexität:** XS/S/M
```

---

## Project-Specific Standards

### Architecture Standards
<!-- From agent-os/product/architecture-decision.md or architecture/platform-architecture.md -->
[ARCHITECTURE_PATTERNS]

### Project Structure
<!-- From agent-os/product/architecture-structure.md -->
[PROJECT_STRUCTURE]

### Naming Conventions
[NAMING_CONVENTIONS]

---

## Quality Standards Reference

For full DoD criteria see: `agent-os/team/dod.md`
For full DoR criteria see: `agent-os/team/dor.md`
