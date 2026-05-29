---
name: ralph-prompt-project
description: Generate Ralph-compatible prompts for entire projects from scratch. Creates comprehensive prompts with architecture phase, implementation phases, testing, and documentation. Use when building complete applications, libraries, CLI tools, or any greenfield project requiring end-to-end development.
---

# Ralph Prompt Generator: Complete Project

## Overview

Generates comprehensive prompts for building entire projects from scratch using the Ralph Wiggum technique. These prompts structure development into architectural phases (design, implementation, testing, documentation) with clear milestones and incremental completion.

**Best For:**
- Building complete REST APIs from scratch
- Creating CLI tools
- Developing libraries/packages
- Building web applications
- Creating automation tools
- Greenfield projects with clear requirements

**Real-World Success:**
- Geoffrey Huntley used Ralph to create the "cursed" programming language over 3 months
- Y Combinator hackathon: 6 repositories generated overnight
- $50k contract completed for $297 in API costs

**Ralph Philosophy**: These successes work because Ralph embraces that failures are deterministic and fixable. Each iteration learns from the previous. Don't fear failures—they're expected and provide data for improvement through prompt tuning, not tool changes.

## Quick Start

**Input Required:**
1. Project description (what to build)
2. Technical requirements (language, framework, features)
3. Success criteria (what makes it complete)
4. Final completion promise

**Generate prompt with:**
```
Generate a Ralph project prompt for:
Project: [Project description]
Tech stack: [Language, framework, tools]
Features: [List of required features]
Promise: [COMPLETION_PHRASE]
```

## Prompt Generation Workflow

### Step 1: Define Project Scope

**Project Definition Template:**
```markdown
PROJECT: [Project Name]
PURPOSE: [One sentence explaining what it does]
TECH STACK: [Languages, frameworks, tools]
TARGET USERS: [Who will use this]

CORE FEATURES:
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

NON-GOALS (Out of scope):
- [What this project will NOT do]
- [Explicit exclusions]

SUCCESS DEFINITION:
[Measurable, verifiable completion criteria]
```

### Step 2: Map Project Phases

Standard project phases:

| Phase | Name | Purpose | Typical % |
|-------|------|---------|-----------|
| 0 | Setup | Project scaffolding, dependencies | 5% |
| 1 | Architecture | Design patterns, structure | 10% |
| 2 | Core | Main functionality | 40% |
| 3 | Features | Additional features | 25% |
| 4 | Testing | Test coverage | 10% |
| 5 | Polish | Documentation, cleanup | 10% |

### Step 3: Define Milestones

Each phase needs concrete milestones:

**Good Milestones:**
- Verifiable by running commands
- Binary (complete or not)
- Independent of subjective judgment

**Examples:**
- "Project builds without errors" (verifiable)
- "All tests pass" (verifiable)
- "CLI help command works" (verifiable)

### Step 4: Structure the Prompt

Use this template:

```markdown
# Project: [Project Name]

## Vision
[2-3 sentences describing what this project is and why it exists]

## Technical Specifications
- **Language**: [e.g., TypeScript, Python, Go]
- **Framework**: [e.g., Express, FastAPI, none]
- **Database**: [e.g., PostgreSQL, SQLite, none]
- **Testing**: [e.g., Jest, pytest, go test]
- **Build**: [e.g., npm, poetry, go build]

## Core Features
1. [Feature 1]: [Brief description]
2. [Feature 2]: [Brief description]
3. [Feature 3]: [Brief description]
[...]

## Non-Goals
- [Explicit exclusion 1]
- [Explicit exclusion 2]

---

## Phase 0: Project Setup (Foundation)

### Objective
Initialize project structure with all dependencies and configuration.

### Tasks
1. Initialize project structure
2. Set up package management
3. Configure development tools (linting, formatting)
4. Create initial directory structure
5. Add basic configuration files

### Deliverables
- [ ] Project directory created
- [ ] Dependencies installed
- [ ] Linting configured and passing
- [ ] Basic structure in place
- [ ] README with setup instructions

### Verification
```bash
# Project builds
[build command]

# Lint passes
[lint command]

# Basic structure exists
ls -la [expected directories]
```

### Phase 0 Checkpoint
```
PHASE 0 COMPLETE:
- Project initialized: [path]
- Dependencies: Installed
- Lint: Passing
```
→ Continue to Phase 1

---

## Phase 1: Architecture & Design

### Objective
Establish core architecture, interfaces, and patterns.

### Tasks
1. Define main interfaces/types
2. Create directory structure following chosen pattern
3. Implement core utilities
4. Set up error handling patterns
5. Create configuration management

### Deliverables
- [ ] Core types/interfaces defined
- [ ] Directory structure matches architecture
- [ ] Utility functions implemented
- [ ] Error handling pattern established
- [ ] Configuration loading works

### Verification
```bash
# Types compile
[typecheck command]

# Config loads
[test config command]
```

### Phase 1 Checkpoint
```
PHASE 1 COMPLETE:
- Architecture: [pattern used]
- Types: Defined and compiling
- Config: Loading correctly
```
→ Continue to Phase 2

---

## Phase 2: Core Implementation

### Objective
Implement the primary functionality that defines this project.

### Tasks
[List core implementation tasks based on project type]

### Deliverables
- [ ] [Core deliverable 1]
- [ ] [Core deliverable 2]
- [ ] [Core deliverable 3]
- [ ] Core tests passing

### Verification
```bash
# Core functionality works
[verification command]

# Tests pass
[test command]
```

### Phase 2 Checkpoint
```
PHASE 2 COMPLETE:
- Core feature 1: Working
- Core feature 2: Working
- Tests: Passing
```
→ Continue to Phase 3

---

## Phase 3: Feature Implementation

### Objective
Add all required features beyond the core.

### Tasks
[List additional feature tasks]

### Deliverables
- [ ] [Feature deliverable 1]
- [ ] [Feature deliverable 2]
- [ ] All feature tests passing

### Verification
```bash
# Features work
[feature verification commands]

# All tests pass
[full test command]
```

### Phase 3 Checkpoint
```
PHASE 3 COMPLETE:
- Feature 1: Working
- Feature 2: Working
- All tests: Passing
```
→ Continue to Phase 4

---

## Phase 4: Testing & Quality

### Objective
Ensure comprehensive test coverage and code quality.

### Tasks
1. Write unit tests for all modules
2. Write integration tests
3. Add edge case tests
4. Ensure code coverage target met
5. Fix any linting issues

### Deliverables
- [ ] Unit test coverage ≥ [X]%
- [ ] Integration tests passing
- [ ] Edge cases covered
- [ ] All lint rules pass
- [ ] No TypeScript/type errors

### Verification
```bash
# Coverage report
[coverage command]

# All quality checks
[lint command] && [typecheck command] && [test command]
```

### Phase 4 Checkpoint
```
PHASE 4 COMPLETE:
- Coverage: [X]%
- All tests: Passing
- Quality: All checks green
```
→ Continue to Phase 5

---

## Phase 5: Documentation & Polish

### Objective
Complete documentation and final polish.

### Tasks
1. Write comprehensive README
2. Add inline documentation/comments for complex code
3. Create usage examples
4. Add CHANGELOG if applicable
5. Final code cleanup

### Deliverables
- [ ] README complete with all sections
- [ ] Usage examples documented
- [ ] Complex code has comments
- [ ] No TODO comments remaining
- [ ] Code formatted consistently

### Verification
```bash
# Check for TODOs
grep -r "TODO" src/

# Lint final
[lint command]

# Build final
[build command]
```

---

## Final Project Verification

### Complete Checklist
- [ ] Phase 0: Setup complete
- [ ] Phase 1: Architecture established
- [ ] Phase 2: Core functionality working
- [ ] Phase 3: All features implemented
- [ ] Phase 4: Tests passing, quality green
- [ ] Phase 5: Documentation complete

### Final Verification Commands
```bash
# Clean build
[clean and build command]

# All tests
[full test command]

# Lint
[lint command]

# Type check (if applicable)
[typecheck command]

# Manual smoke test
[manual verification steps]
```

## Completion
When ALL of the following are true:
- All 6 phases completed and verified
- All tests passing
- All quality checks green
- Documentation complete
- No TODO items remaining

Output: <promise>[COMPLETION_PHRASE]</promise>

## Progress Tracking
Update after each phase:
```
PROJECT PROGRESS:
Phase 0 (Setup): [COMPLETE/IN PROGRESS]
Phase 1 (Architecture): [COMPLETE/IN PROGRESS/NOT STARTED]
Phase 2 (Core): [COMPLETE/IN PROGRESS/NOT STARTED]
Phase 3 (Features): [COMPLETE/IN PROGRESS/NOT STARTED]
Phase 4 (Testing): [COMPLETE/IN PROGRESS/NOT STARTED]
Phase 5 (Documentation): [COMPLETE/IN PROGRESS/NOT STARTED]

Current Phase: [X]
Overall: [description of state]
```

## If Stuck
After multiple iterations on same issue:
1. Document the specific blocker
2. List what approaches have been tried
3. Identify the root cause if possible
4. Consider if feature should be descoped (but DO NOT skip without documenting)
5. Do NOT output false promise - continue or wait for max-iterations
```

## Example: REST API Project

**Input:**
- Project: Todo List REST API
- Tech: Node.js, Express, TypeScript, SQLite
- Features: CRUD todos, user auth, categories, due dates
- Promise: TODO_API_COMPLETE

**Generated Prompt:**

```markdown
# Project: Todo List REST API

## Vision
A RESTful API for managing todo items with user authentication, categories, and due date tracking. Built with TypeScript and Express for type safety and ease of development.

## Technical Specifications
- **Language**: TypeScript
- **Framework**: Express.js
- **Database**: SQLite with better-sqlite3
- **Testing**: Jest with supertest
- **Build**: npm with tsc

## Core Features
1. **User Authentication**: JWT-based auth with signup/login/logout
2. **Todo CRUD**: Create, read, update, delete todo items
3. **Categories**: Organize todos by category
4. **Due Dates**: Set and track due dates with overdue detection
5. **Filtering**: Filter todos by status, category, due date

## Non-Goals
- Frontend/UI (API only)
- Real-time updates (polling only)
- File attachments
- Collaboration/sharing

---

## Phase 0: Project Setup

### Tasks
1. `npm init` with TypeScript configuration
2. Install dependencies: express, better-sqlite3, jsonwebtoken, bcrypt
3. Install dev dependencies: typescript, jest, supertest, eslint
4. Configure tsconfig.json, eslint, jest
5. Create directory structure: src/{routes,controllers,models,middleware}

### Deliverables
- [ ] package.json with all dependencies
- [ ] tsconfig.json configured
- [ ] ESLint configured and passing
- [ ] Directory structure created
- [ ] `npm run build` works

### Verification
```bash
npm run build
npm run lint
ls src/
```

### Phase 0 Checkpoint
```
PHASE 0 COMPLETE: Project scaffolded, builds successfully
```

---

## Phase 1: Architecture

### Tasks
1. Define TypeScript interfaces: User, Todo, Category
2. Create database schema and initialization
3. Set up Express app structure with middleware
4. Implement error handling middleware
5. Create config management

### Deliverables
- [ ] Types in src/types/
- [ ] Database schema creates tables
- [ ] Express app configured with JSON parsing, CORS
- [ ] Error handler returns proper JSON errors
- [ ] Config loads from environment

### Verification
```bash
npm run build
npm test -- --grep "database"
```

---

## Phase 2: Core Implementation

### Tasks
1. Implement User model with password hashing
2. Create auth routes: POST /auth/signup, POST /auth/login
3. Implement JWT middleware for protected routes
4. Implement Todo model and CRUD
5. Create todo routes: GET, POST, PUT, DELETE /todos

### Deliverables
- [ ] Signup creates user, returns JWT
- [ ] Login validates, returns JWT
- [ ] Protected routes require valid JWT
- [ ] CRUD operations work for todos
- [ ] User can only access their own todos

### Verification
```bash
# Signup
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}' \
  http://localhost:3000/auth/signup

# Login and use token for todos
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}' \
  http://localhost:3000/auth/login | jq -r '.token')

curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/todos
```

---

## Phase 3: Features

### Tasks
1. Implement Category model and routes
2. Add category relationship to todos
3. Implement due date field with validation
4. Add overdue detection endpoint
5. Implement filtering (status, category, due date range)

### Deliverables
- [ ] Categories CRUD works
- [ ] Todos can be assigned to categories
- [ ] Due dates stored and validated
- [ ] GET /todos/overdue returns overdue items
- [ ] Filtering by query params works

---

## Phase 4: Testing

### Tasks
1. Unit tests for models
2. Integration tests for all routes
3. Auth flow tests
4. Edge case tests (invalid inputs, unauthorized access)

### Deliverables
- [ ] ≥80% code coverage
- [ ] All auth scenarios tested
- [ ] All CRUD scenarios tested
- [ ] Error cases tested

### Verification
```bash
npm test -- --coverage
```

---

## Phase 5: Documentation

### Tasks
1. README with API documentation
2. Setup instructions
3. Example requests for each endpoint
4. Environment variables documentation

### Deliverables
- [ ] README complete
- [ ] All endpoints documented
- [ ] Examples provided
- [ ] No TODOs remaining

---

## Final Verification
```bash
npm run lint
npm run build
npm test -- --coverage
npm start  # Manual smoke test
```

## Completion
When all phases verified and:
- All tests passing with ≥80% coverage
- All endpoints working
- Documentation complete

Output: <promise>TODO_API_COMPLETE</promise>
```

## Best Practices

### Project Scope
- Define clear boundaries (non-goals)
- Start smaller than you think necessary
- Add features incrementally

### Phase Management
- Complete phases in order
- Don't skip testing phase
- Document checkpoints

### Verification
- Include actual commands to run
- Make success criteria binary
- Automate where possible

### DO:
- Define clear project scope
- Use all 6 phases
- Include verification commands
- Set realistic feature scope
- Document progress at checkpoints

### DON'T:
- Skip architectural phase
- Rush to implementation
- Leave testing for "later"
- Scope creep mid-project
- Output promise before documentation

## Integration with Ralph Loop

```bash
/ralph-wiggum:ralph-loop "[paste generated prompt]" --completion-promise "YOUR_PROMISE" --max-iterations 100
```

**Recommended iterations by project size:**
- Small project (CLI tool, simple API): `--max-iterations 60-80`
- Medium project (Full API with auth): `--max-iterations 100-150`
- Large project (Multi-feature app): `--max-iterations 150-200`

**Tip:** For large projects, consider splitting into multiple Ralph sessions:
1. First session: Phases 0-2 (Setup through Core)
2. Second session: Phases 3-5 (Features through Polish)

---

For single-task prompts, see `ralph-prompt-single-task`.
For multi-task prompts, see `ralph-prompt-multi-task`.
For research/analysis prompts, see `ralph-prompt-research`.
