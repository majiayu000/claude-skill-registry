---
name: ralph-prompt-multi-task
description: Generate Ralph-compatible prompts for multiple related tasks. Creates phased prompts with sequential milestones, cumulative progress tracking, and phase-based completion promises. Use when creating prompts for CRUD implementations, multi-step features, staged migrations, or any work requiring multiple distinct but related tasks.
---

# Ralph Prompt Generator: Multi-Task

## Overview

Generates structured prompts for multiple related tasks that need to be completed in sequence or parallel. Uses phase-based organization with milestone tracking, cumulative success criteria, and clear progression through tasks.

**Best For:**
- CRUD operation implementations (Create, Read, Update, Delete)
- Multi-step feature development
- Database migrations with multiple stages
- API endpoint suites
- Test suite creation for multiple modules
- Multi-file refactoring projects

**Ralph Philosophy**: This generator embraces the principle that failures are deterministic and fixable. Each phase iteration learns from previous attempts. Don't fear failures—they're expected and provide data for improvement through prompt tuning.

## Quick Start

**Input Required:**
1. List of tasks to complete
2. Task dependencies (which tasks depend on others)
3. Success criteria for each task
4. Final completion promise

**Generate prompt with:**
```
Generate a Ralph multi-task prompt for:
Tasks:
1. [Task 1]
2. [Task 2]
3. [Task 3]
Dependencies: [Task 2 depends on Task 1, etc.]
Final promise: [COMPLETION_PHRASE]
```

## Prompt Generation Workflow

### Step 1: Map the Tasks

Create a task inventory:

| Task # | Task Name | Dependencies | Verification | Est. Complexity |
|--------|-----------|--------------|--------------|-----------------|
| 1 | [Name] | None | [How to verify] | Low/Med/High |
| 2 | [Name] | Task 1 | [How to verify] | Low/Med/High |
| 3 | [Name] | Task 1 | [How to verify] | Low/Med/High |
| 4 | [Name] | Tasks 2, 3 | [How to verify] | Low/Med/High |

### Step 2: Define Phases

Group tasks into logical phases:

**Phase Structure:**
- **Phase 1: Foundation** - Independent setup tasks, no dependencies
- **Phase 2: Core Implementation** - Main functionality, depends on Phase 1
- **Phase 3: Enhancement** - Additional features, depends on Phase 2
- **Phase 4: Validation** - Testing, cleanup, verification

### Step 3: Create Phase Milestones

Each phase needs:
- Clear entry criteria (what must be done to start)
- Specific tasks within the phase
- Exit criteria (what proves phase is complete)
- Phase milestone marker

### Step 4: Structure the Prompt

Use this template:

```markdown
# Multi-Task: [Overall Objective]

## Overview
[1-2 sentences describing the overall goal and scope]

## Task Inventory
| # | Task | Phase | Dependencies | Verification |
|---|------|-------|--------------|--------------|
| 1 | [Task 1] | 1 | None | [Verification] |
| 2 | [Task 2] | 2 | Task 1 | [Verification] |
| 3 | [Task 3] | 2 | Task 1 | [Verification] |
| 4 | [Task 4] | 3 | Tasks 2, 3 | [Verification] |

## Phase 1: [Phase Name] (Foundation)

### Objective
[What this phase accomplishes]

### Tasks
1. **[Task 1 Name]**
   - Requirements: [Specific requirements]
   - Files: [Files to create/modify]
   - Verification: [How to verify]

### Phase 1 Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] Tests pass: `[test command]`

### Phase 1 Checkpoint
When Phase 1 criteria met, document:
```
PHASE 1 COMPLETE:
- [Task 1]: Done - [evidence]
- Tests: [pass/fail status]
```
Continue to Phase 2.

---

## Phase 2: [Phase Name] (Core)

### Objective
[What this phase accomplishes]

### Prerequisites
- Phase 1 complete
- [Any specific requirements]

### Tasks
2. **[Task 2 Name]**
   - Requirements: [Specific requirements]
   - Files: [Files to create/modify]
   - Verification: [How to verify]

3. **[Task 3 Name]**
   - Requirements: [Specific requirements]
   - Files: [Files to create/modify]
   - Verification: [How to verify]

### Phase 2 Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] Tests pass: `[test command]`

### Phase 2 Checkpoint
When Phase 2 criteria met, document:
```
PHASE 2 COMPLETE:
- [Task 2]: Done - [evidence]
- [Task 3]: Done - [evidence]
- Tests: [pass/fail status]
```
Continue to Phase 3.

---

## Phase 3: [Phase Name] (Enhancement/Validation)

### Objective
[What this phase accomplishes]

### Prerequisites
- Phases 1-2 complete
- [Any specific requirements]

### Tasks
4. **[Task 4 Name]**
   - Requirements: [Specific requirements]
   - Files: [Files to create/modify]
   - Verification: [How to verify]

### Phase 3 Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] All tests pass: `[test command]`

---

## Final Verification

Run complete verification:
```bash
# All tests
[full test command]

# Integration check
[integration verification]

# Lint/Type check
[lint command]
```

## Completion Checklist
- [ ] Phase 1: All tasks complete and verified
- [ ] Phase 2: All tasks complete and verified
- [ ] Phase 3: All tasks complete and verified
- [ ] All tests passing
- [ ] No regressions
- [ ] [Any additional requirements]

## Completion
When ALL phases complete and all checklist items verified:

Output: <promise>[COMPLETION_PHRASE]</promise>

## Progress Tracking
As you work, track progress in this format:
```
PROGRESS:
Phase 1: [COMPLETE/IN PROGRESS] - [X/Y tasks]
Phase 2: [COMPLETE/IN PROGRESS/NOT STARTED] - [X/Y tasks]
Phase 3: [COMPLETE/IN PROGRESS/NOT STARTED] - [X/Y tasks]
Overall: [X/Y tasks complete]
```

## If Stuck
- Document which phase/task is blocking
- List what's been tried
- Identify the specific blocker
- Do NOT skip tasks or output false promise
```

## Example Prompts

### Example 1: CRUD API Implementation

**Input:**
- Tasks: Create, Read (single), Read (list), Update, Delete for Products
- Dependencies: Create first, then others can be parallel
- Promise: CRUD_API_COMPLETE

**Generated Prompt:**

```markdown
# Multi-Task: Product CRUD API Implementation

## Overview
Implement complete CRUD operations for Products resource with RESTful endpoints, validation, and comprehensive tests.

## Task Inventory
| # | Task | Phase | Dependencies | Verification |
|---|------|-------|--------------|--------------|
| 1 | Product model/schema | 1 | None | Model exists, validates |
| 2 | POST /products (Create) | 2 | Task 1 | Returns 201, creates record |
| 3 | GET /products/:id (Read) | 2 | Task 1 | Returns 200, correct data |
| 4 | GET /products (List) | 2 | Task 1 | Returns array, pagination |
| 5 | PUT /products/:id (Update) | 3 | Tasks 2,3 | Returns 200, updates record |
| 6 | DELETE /products/:id | 3 | Tasks 2,3 | Returns 204, removes record |
| 7 | Integration tests | 4 | Tasks 2-6 | All scenarios pass |

## Phase 1: Foundation

### Objective
Create Product model with validation and database schema.

### Tasks
1. **Product Model**
   - Requirements:
     - Fields: id, name, description, price, category, createdAt, updatedAt
     - Validation: name required, price > 0, category from enum
   - Files: `src/models/product.ts`, `src/schemas/product.ts`
   - Verification: Model compiles, validation tests pass

### Phase 1 Success Criteria
- [ ] Product model created with all fields
- [ ] Validation rules implemented
- [ ] Database migration/schema created
- [ ] Model tests pass: `npm test -- --grep "Product model"`

### Phase 1 Checkpoint
```
PHASE 1 COMPLETE:
- Product model: Done - all fields, validation working
- Tests: All model tests passing
```

---

## Phase 2: Core CRUD Operations

### Objective
Implement Create, Read (single), and Read (list) endpoints.

### Prerequisites
- Phase 1 complete (Product model exists)

### Tasks
2. **POST /products (Create)**
   - Requirements:
     - Accept JSON body with product data
     - Validate input using schema
     - Return 201 with created product
     - Return 400 for validation errors
   - Files: `src/routes/products.ts`, `src/controllers/products.ts`
   - Verification: `curl -X POST -H "Content-Type: application/json" -d '{"name":"Test","price":9.99,"category":"electronics"}' localhost:3000/products`

3. **GET /products/:id (Read Single)**
   - Requirements:
     - Return 200 with product data
     - Return 404 if not found
   - Files: `src/routes/products.ts`, `src/controllers/products.ts`
   - Verification: `curl localhost:3000/products/1`

4. **GET /products (List)**
   - Requirements:
     - Return array of products
     - Support pagination: page, limit query params
     - Return metadata: total, page, limit, totalPages
   - Files: `src/routes/products.ts`, `src/controllers/products.ts`
   - Verification: `curl "localhost:3000/products?page=1&limit=10"`

### Phase 2 Success Criteria
- [ ] POST /products creates product, returns 201
- [ ] POST /products returns 400 for invalid data
- [ ] GET /products/:id returns product
- [ ] GET /products/:id returns 404 for missing
- [ ] GET /products returns paginated list
- [ ] All endpoint tests pass: `npm test -- --grep "products"`

### Phase 2 Checkpoint
```
PHASE 2 COMPLETE:
- POST /products: Done - creates products, validates input
- GET /products/:id: Done - returns product or 404
- GET /products: Done - paginated list working
- Tests: All passing
```

---

## Phase 3: Update and Delete Operations

### Objective
Complete CRUD with Update and Delete endpoints.

### Prerequisites
- Phase 2 complete (Create and Read working)

### Tasks
5. **PUT /products/:id (Update)**
   - Requirements:
     - Accept JSON body with update data
     - Partial updates allowed
     - Return 200 with updated product
     - Return 404 if not found
     - Return 400 for validation errors
   - Verification: `curl -X PUT -H "Content-Type: application/json" -d '{"price":19.99}' localhost:3000/products/1`

6. **DELETE /products/:id**
   - Requirements:
     - Return 204 on success (no content)
     - Return 404 if not found
     - Actually remove record from database
   - Verification: `curl -X DELETE localhost:3000/products/1`

### Phase 3 Success Criteria
- [ ] PUT /products/:id updates product
- [ ] PUT returns 404 for missing, 400 for invalid
- [ ] DELETE /products/:id removes product
- [ ] DELETE returns 404 for missing
- [ ] All endpoint tests pass

### Phase 3 Checkpoint
```
PHASE 3 COMPLETE:
- PUT /products/:id: Done - updates work
- DELETE /products/:id: Done - deletes work
- Tests: All passing
```

---

## Phase 4: Integration & Validation

### Objective
Complete test coverage and integration verification.

### Tasks
7. **Integration Tests**
   - Requirements:
     - Full CRUD flow test (create, read, update, delete)
     - Error handling tests (400, 404 scenarios)
     - Pagination tests
     - Edge cases (empty database, special characters)
   - Files: `tests/integration/products.test.ts`

### Phase 4 Success Criteria
- [ ] Integration tests cover full CRUD flow
- [ ] Error scenarios tested
- [ ] All tests passing: `npm test`
- [ ] No TypeScript errors: `npm run typecheck`

---

## Final Verification

```bash
# All tests
npm test

# Type check
npm run typecheck

# Manual CRUD flow test
curl -X POST -H "Content-Type: application/json" -d '{"name":"Test Product","price":29.99,"category":"electronics"}' localhost:3000/products
curl localhost:3000/products
curl localhost:3000/products/1
curl -X PUT -H "Content-Type: application/json" -d '{"price":39.99}' localhost:3000/products/1
curl -X DELETE localhost:3000/products/1
```

## Completion Checklist
- [ ] Phase 1: Product model complete
- [ ] Phase 2: Create, Read single, Read list working
- [ ] Phase 3: Update, Delete working
- [ ] Phase 4: Integration tests complete
- [ ] All tests passing
- [ ] Manual verification successful

## Completion
When ALL phases complete and all checklist items verified:

Output: <promise>CRUD_API_COMPLETE</promise>

## Progress Tracking
```
PROGRESS:
Phase 1: [status] - 1/1 tasks
Phase 2: [status] - 3/3 tasks
Phase 3: [status] - 2/2 tasks
Phase 4: [status] - 1/1 tasks
Overall: X/7 tasks complete
```

## If Stuck
- Document which phase/task is blocking
- Note specific error messages
- List approaches tried
- Do NOT skip tasks or output false promise
```

### Example 2: CI/CD Pipeline Setup

**Input:**
- Tasks: Lint, Test, Build, Deploy staging, Deploy prod
- Dependencies: Sequential progression
- Promise: PIPELINE_COMPLETE

**Generated Prompt:**

```markdown
# Multi-Task: CI/CD Pipeline Implementation

## Overview
Set up complete CI/CD pipeline with linting, testing, building, and staged deployments using GitHub Actions.

## Task Inventory
| # | Task | Phase | Dependencies | Verification |
|---|------|-------|--------------|--------------|
| 1 | Workflow file structure | 1 | None | File exists |
| 2 | Lint job | 2 | Task 1 | Workflow runs lint |
| 3 | Test job | 2 | Task 2 | Tests run in CI |
| 4 | Build job | 3 | Task 3 | Build artifacts created |
| 5 | Deploy staging | 4 | Task 4 | Staging deployment works |
| 6 | Deploy production | 4 | Task 5 | Prod deployment works |

## Phase 1: Workflow Foundation

### Tasks
1. **Workflow File Structure**
   - Create `.github/workflows/ci.yml`
   - Define triggers (push to main, PRs)
   - Set up job structure

### Phase 1 Success Criteria
- [ ] Workflow file exists and is valid YAML
- [ ] Triggers defined for push and PR

---

## Phase 2: Quality Gates

### Tasks
2. **Lint Job**
   - Run linter on all source files
   - Fail pipeline if lint errors

3. **Test Job**
   - Depends on lint passing
   - Run full test suite
   - Upload coverage report

### Phase 2 Success Criteria
- [ ] Lint job runs and catches errors
- [ ] Test job runs full suite
- [ ] Pipeline fails if tests fail

---

## Phase 3: Build

### Tasks
4. **Build Job**
   - Depends on tests passing
   - Create production build
   - Upload build artifacts

### Phase 3 Success Criteria
- [ ] Build creates production artifacts
- [ ] Artifacts uploaded and accessible

---

## Phase 4: Deployments

### Tasks
5. **Deploy Staging**
   - Automatic on main branch
   - Deploy to staging environment

6. **Deploy Production**
   - Manual approval required
   - Deploy to production

### Phase 4 Success Criteria
- [ ] Staging auto-deploys on main
- [ ] Production requires manual trigger
- [ ] Both environments update correctly

---

## Completion
When all phases verified:

Output: <promise>PIPELINE_COMPLETE</promise>
```

## Best Practices

### Task Organization
- Group related tasks into phases
- Clear dependencies between phases
- Independent tasks within phases can be parallel

### Phase Design
- Each phase has clear entry/exit criteria
- Document checkpoint at each phase boundary
- Phase names should reflect purpose (Foundation, Core, Enhancement, Validation)

### Progress Tracking
- Update progress marker after each task
- Document evidence at checkpoints
- Don't skip phases even if tasks seem simple

### DO:
- Create clear phase boundaries
- Define dependencies explicitly
- Include verification for each task
- Track progress systematically
- Checkpoint after each phase

### DON'T:
- Skip phases or tasks
- Leave dependencies unclear
- Forget phase checkpoints
- Output promise before all phases complete

## Integration with Ralph Loop

```bash
/ralph-wiggum:ralph-loop "[paste generated prompt]" --completion-promise "YOUR_PROMISE" --max-iterations 50
```

**Recommended iterations by complexity:**
- 4-5 tasks: `--max-iterations 35-45`
- 6-8 tasks: `--max-iterations 50-70`
- 9+ tasks: `--max-iterations 80-100`

---

For single-task prompts, see `ralph-prompt-single-task`.
For project-level prompts, see `ralph-prompt-project`.
For research/analysis prompts, see `ralph-prompt-research`.
