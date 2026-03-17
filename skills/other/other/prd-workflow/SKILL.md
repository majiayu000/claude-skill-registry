---
name: prd-workflow
description: |
  PRD-driven development workflow for feature implementation.
  Auto-activates on "PRD", "產品需求", "功能文檔", "規格書", "feature spec" keywords.
  Ensures all features have proper documentation before and after implementation.
allowed-tools: [Read, Write, Edit, Grep]
---

# PRD Workflow Skill

## Purpose
Document-driven development: **PRD → Plan → Implement → Update PRD**.

Prevents:
- ❌ Undocumented features
- ❌ Scope creep
- ❌ Lost context after months
- ❌ Inconsistent implementation

---

## Auto-Activation

Triggers on:
- ✅ "PRD", "產品需求文檔"
- ✅ "功能規格", "feature spec"
- ✅ "需求文檔", "requirements document"

---

## PRD-Driven Workflow

```
1. 收到需求
   ↓
2. 寫/更新 PRD (BEFORE coding)
   ↓
3. Review PRD → Get approval
   ↓
4. Enter Plan Mode → Design implementation
   ↓
5. Implement with TDD
   ↓
6. Update PRD (mark as implemented)
   ↓
7. Update CHANGELOG
```

---

## PRD Template

### Location
```
docs/features/PRD_<feature_name>.md
```

### Template Structure

````markdown
# PRD: <Feature Name>

**Status**: 🟡 Planning / 🟢 Implemented / 🔴 Blocked
**Priority**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)
**Owner**: <Team/Person>
**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD

---

## 1. Background & Motivation

### Problem Statement
What problem are we solving?

### User Impact
Who benefits? How?

### Business Value
Why now? What's the ROI?

---

## 2. User Stories

### Primary User Story
```
As a [user type],
I want to [action],
So that [benefit].
```

### Additional Stories
- As a ...
- As a ...

---

## 3. Functional Requirements

### Must Have (P0)
- [ ] Requirement 1
- [ ] Requirement 2

### Should Have (P1)
- [ ] Requirement 3

### Nice to Have (P2)
- [ ] Requirement 4

---

## 4. API Design

### Endpoint(s)

**POST /api/v1/<resource>**

Request:
```json
{
  "field1": "value",
  "field2": 123
}
```

Response:
```json
{
  "id": 1,
  "field1": "value",
  "created_at": "2025-12-25T00:00:00Z"
}
```

Error Cases:
- 400: Invalid input
- 401: Unauthorized
- 404: Resource not found

---

## 5. Data Model

```python
class <Model>(Base):
    __tablename__ = "<table>"

    id: int
    field1: str
    field2: int
    created_at: datetime
```

---

## 6. Acceptance Criteria

### Functional
- [ ] User can do X
- [ ] System validates Y
- [ ] Error message shows when Z

### Technical
- [ ] API endpoint implemented
- [ ] Database migration created
- [ ] Integration tests pass (≥3 tests)
- [ ] Error handling complete

### Quality
- [ ] Code follows project patterns
- [ ] Documentation updated
- [ ] No hardcoded values

---

## 7. Testing Strategy

### Integration Tests
```python
# tests/integration/test_<feature>_api.py

test_<feature>_create_success()
test_<feature>_create_validation_error()
test_<feature>_create_unauthorized()
test_<feature>_get_success()
test_<feature>_update_success()
test_<feature>_delete_success()
```

### Test Data
- Sample inputs
- Expected outputs
- Edge cases

---

## 8. Implementation Plan

### Phase 1: Database & Models
- [ ] Create migration
- [ ] Define models
- [ ] Test with sample data

### Phase 2: API Implementation
- [ ] Write integration tests (RED)
- [ ] Implement endpoints (GREEN)
- [ ] Add error handling
- [ ] Refactor (REFACTOR)

### Phase 3: Verification
- [ ] Manual testing in console.html
- [ ] All tests pass
- [ ] Code review

---

## 9. Dependencies

### Depends On
- Feature X must be completed first
- Database schema Y must exist

### Blocks
- Feature Z is waiting for this

---

## 10. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Database performance | Medium | High | Add indexes |
| Complex validation | Low | Medium | Use Pydantic |

---

## 11. Out of Scope

**Explicitly NOT included** (to prevent scope creep):
- Feature X (defer to v2)
- Complex Y (too much complexity)

---

## 12. Implementation Log

### 2025-12-25: Initial implementation
- Created database model
- Implemented CRUD API
- Added 6 integration tests
- Status: ✅ Completed

### Issues Encountered
- Issue 1: [description] → Solution: [solution]

---

## 13. Future Enhancements

**v2 Considerations**:
- Enhancement 1
- Enhancement 2
````

---

## Workflow: New Feature

### Step 1: Create PRD (Before Coding!)

```bash
# Create PRD file
touch docs/features/PRD_client_search.md

# Use template above
# Fill in sections 1-9
# Get user approval
```

**CRITICAL**: Do NOT start coding until PRD is approved!

### Step 2: Enter Plan Mode

```bash
# In Claude Code, enter Plan Mode
/plan

# Or trigger with keywords
"Let's plan how to implement client search based on the PRD"
```

**In Plan Mode**:
1. Read PRD
2. Design implementation strategy
3. Identify files to change
4. Sequence the work
5. Write to plan.md
6. Exit plan mode

### Step 3: Implement with TDD

**Follow tdd-workflow**:
```
1. RED: Write tests (from acceptance criteria)
2. GREEN: Implement (from API design)
3. REFACTOR: Clean up
```

### Step 4: Update PRD

```markdown
## 12. Implementation Log

### 2025-12-25: Completed
- ✅ All acceptance criteria met
- ✅ 5 integration tests passing
- ✅ Deployed to staging

Files changed:
- app/api/clients.py
- app/schemas/client.py
- tests/integration/test_clients_api.py
```

### Step 5: Update CHANGELOG

```markdown
## [Unreleased]

### Added
- Client search API (PRD_client_search.md)
  - Search by name, email, code
  - Paginated results
  - Case-insensitive matching
```

---

## Workflow: Update Existing Feature

### Step 1: Find Existing PRD

```bash
# Find PRD
find docs/features/ -name "PRD_*.md" | grep -i "client"
```

### Step 2: Update PRD

```markdown
## Amendment: 2025-12-25

### New Requirement
- Add sorting to search results

### Acceptance Criteria
- [ ] Can sort by name (asc/desc)
- [ ] Can sort by created_at (asc/desc)

### Implementation
- Modified: GET /api/v1/clients/search?q={query}&sort={field}&order={asc|desc}
```

### Step 3: Implement Changes

Follow TDD workflow with updated requirements.

### Step 4: Update Implementation Log

```markdown
### 2025-12-25: Added sorting
- Added sort parameter
- Updated tests
- Status: ✅ Completed
```

---

## PRD Organization

### Directory Structure

```
docs/
├── features/
│   ├── PRD_client_search.md
│   ├── PRD_session_transcripts.md
│   ├── PRD_realtime_suggestions.md
│   └── PRD_report_generation.md
├── architecture/
│   └── system_design.md
└── api/
    └── api_overview.md
```

### Naming Convention

```
PRD_<feature_name>.md

Examples:
✅ PRD_client_search.md
✅ PRD_session_transcripts.md
✅ PRD_realtime_expert_suggestions.md

❌ client.md (not descriptive)
❌ feature1.md (not clear)
```

---

## PRD Status Tracking

### Status Indicators

```markdown
**Status**: 🟡 Planning
**Status**: 🔵 In Development
**Status**: 🟢 Implemented
**Status**: 🔴 Blocked
**Status**: ⚫ Cancelled
```

### Priority Levels

```
P0: Critical (must have, blocks other work)
P1: High (important, significant value)
P2: Medium (nice to have)
P3: Low (future consideration)
```

---

## Integration with TDD Workflow

```
PRD defines "WHAT"
  ↓
Acceptance Criteria → Integration Tests (RED)
  ↓
API Design → Implementation (GREEN)
  ↓
Quality Requirements → Refactor
  ↓
Implementation Log → Update PRD
```

**Key Point**: PRD acceptance criteria become test cases!

```python
# From PRD:
- [ ] User can search by client name
- [ ] Search is case-insensitive
- [ ] Results are paginated

# Becomes tests:
def test_search_by_name():
def test_search_case_insensitive():
def test_search_pagination():
```

---

## Real Example: Client Search Feature

### Before (No PRD)

```
User: "加一個搜尋功能"
Agent: (直接實作，猜測需求)
Result: ❌ 功能不符預期，重做 3 次
```

### After (With PRD)

````markdown
# PRD: Client Search

**Status**: 🟢 Implemented
**Priority**: P1
**Created**: 2025-12-20

## 1. Background
Counselors need to quickly find clients from a large list.

## 2. User Story
As a counselor,
I want to search for clients by name/email/code,
So that I can quickly find the client I need.

## 3. Functional Requirements

Must Have:
- [x] Search by client name (partial match)
- [x] Search by email (partial match)
- [x] Search by client code (exact match)
- [x] Case-insensitive
- [x] Paginated results (10 per page)

## 4. API Design

GET /api/v1/clients/search?q={query}&page={page}

Response:
```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "pages": 5
}
```

## 6. Acceptance Criteria
- [x] Returns matching clients
- [x] Pagination works
- [x] Case doesn't matter
- [x] Empty query returns error

## 12. Implementation Log

### 2025-12-25: Completed
- Implemented search endpoint
- Added 5 integration tests
- All tests passing ✅
````

**Result**: ✅ 一次做對，需求清楚，測試完整

---

## PRD Review Checklist

**Before starting implementation**:

### Completeness
- [ ] Problem clearly stated?
- [ ] User stories defined?
- [ ] Acceptance criteria specific?
- [ ] API design complete?
- [ ] Test strategy defined?

### Clarity
- [ ] Can another developer implement from this PRD?
- [ ] Are there ambiguous requirements?
- [ ] Are edge cases covered?

### Feasibility
- [ ] Dependencies identified?
- [ ] Risks assessed?
- [ ] Scope reasonable?

---

## Benefits

### For Developers
- ✅ Clear requirements (no guessing)
- ✅ Test cases pre-defined
- ✅ Implementation roadmap ready

### For Product Owners
- ✅ Documented decisions
- ✅ Trackable progress
- ✅ Easy to review/approve

### For Future You
- ✅ Context preserved (6 months later, still understand)
- ✅ Change history tracked
- ✅ Easy to extend feature

---

## Common Mistakes

### ❌ Writing PRD After Implementation

```
"我已經做完了，現在寫 PRD..."
```

**Problem**: PRD 變成事後補文檔，失去價值

### ❌ Too Much Detail

```
100 頁的 PRD，包含每個變數的名字...
```

**Problem**: 沒人會讀，浪費時間

### ❌ Too Little Detail

```
"加一個搜尋功能"（整個 PRD 只有這一句）
```

**Problem**: 跟沒有 PRD 一樣

### ✅ Right Balance

```
2-4 頁 PRD:
- Problem + User Story (1 段)
- Requirements (5-10 items)
- API Design (具體格式)
- Acceptance Criteria (測試清單)
```

---

## Quick Start

**Minimal PRD** (for small features):

```markdown
# PRD: <Feature>

**Problem**: <1 sentence>

**User Story**: As a ..., I want ..., so that ...

**Requirements**:
- [ ] Must do X
- [ ] Must validate Y
- [ ] Must handle error Z

**API**:
POST /api/v1/resource
Request: { "field": "value" }
Response: { "id": 1, "field": "value" }

**Tests**:
- test_create_success
- test_create_validation_error
- test_create_unauthorized

**Acceptance**:
- [ ] API works
- [ ] Tests pass
- [ ] Error handling complete
```

**Time**: 10-15 minutes to write, saves 2+ hours of rework!

---

## Related Skills

- **requirements-clarification**: Clarify before writing PRD
- **tdd-workflow**: Implement PRD with TDD
- **api-development**: Follow API design from PRD

---

**Skill Version**: v1.0
**Last Updated**: 2025-12-25
**Project**: career_ios_backend
**Philosophy**: "If it's not documented, it doesn't exist"
