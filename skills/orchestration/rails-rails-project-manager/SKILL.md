---
name: rails-project-manager
description: Project management skill that analyzes tasks, breaks them down into stages, coordinates other skills, and ensures proper workflow. Use when planning features, managing complex multi-step implementations, or need help organizing development tasks. Routes work to specialized skills (testing, security, components, etc.).
---

# Rails Project Manager

Orchestrates Rails development by analyzing requirements, breaking down tasks, and coordinating specialized skills.

## When to Use This Skill

- Planning new features or major refactorings
- Breaking down complex requirements into stages
- Coordinating multiple aspects (testing, security, UI, backend)
- Creating implementation plans
- Managing multi-step development workflows
- Code review and quality assurance
- Deciding which specialized skill to use for specific tasks

## Core Responsibilities

### 1. Requirements Analysis

**Analyze user request and determine:**
- What needs to be built
- Which components are involved (models, controllers, views, jobs, etc.)
- Which specialized skills are needed
- What order tasks should be completed
- What dependencies exist between tasks

### 2. Task Breakdown

**Create staged implementation plan:**

```markdown
## Stage 1: Database & Models
**Goal**: Set up data structure
**Skills needed**: rails-business-logic
**Tasks**:
- [ ] Create migration for users table
- [ ] Add User model with validations
- [ ] Write model tests

## Stage 2: Business Logic
**Goal**: Implement core operations
**Skills needed**: rails-business-logic, rails-testing
**Tasks**:
- [ ] Create Users::Create interaction
- [ ] Write interaction tests
- [ ] Handle edge cases

## Stage 3: UI Components
**Goal**: Build user interface
**Skills needed**: rails-viewcomponents
**Tasks**:
- [ ] Create UserFormComponent
- [ ] Add Turbo Frame for inline editing
- [ ] Write component tests
```

### 3. Skill Coordination

**Route tasks to appropriate specialists:**

- **Testing tasks** → `rails-testing`
- **UI/Components** → `rails-viewcomponents`
- **Security/Auth** → `rails-security`
- **Business logic** → `rails-business-logic`
- **Background jobs** → `rails-background-jobs`
- **Documentation** → `rails-technical-writer`
- **Inertia.js** → `rails-inertia`
- **Analysis/Metrics** → `rails-analyst`

### 4. Quality Assurance

**Ensure before completion:**
- ✓ All tests pass
- ✓ Code follows conventions
- ✓ Security best practices applied
- ✓ Documentation updated
- ✓ No linting errors
- ✓ Performance considerations addressed

## Planning Process

### Step 1: Understand the Request

Ask clarifying questions if needed:
- What is the user trying to achieve?
- Are there any constraints or requirements?
- What is the current state of the codebase?
- Are there any existing patterns to follow?

### Step 2: Identify Components

Determine what needs to be built:
- **Models**: New tables, associations, validations?
- **Interactions**: Business logic operations?
- **Controllers**: API endpoints or web routes?
- **Components**: UI elements, forms, displays?
- **Jobs**: Background processing needed?
- **Tests**: What test coverage is required?
- **Security**: Authorization, encryption needed?

### Step 3: Create Implementation Plan

Break into logical stages:
1. **Database/Models** (foundation)
2. **Business Logic** (core operations)
3. **API/Controllers** (interface)
4. **UI/Components** (presentation)
5. **Jobs** (async processing)
6. **Tests** (throughout, TDD)
7. **Documentation** (as you go)

### Step 4: Execute with Specialists

For each stage:
- Identify which specialist skill is needed
- Provide context and requirements
- Review output for quality
- Move to next stage

## Example: User Registration Feature

**Initial Request:**
> "I need to add user registration with email confirmation"

**Analysis:**
- Models: User model with email, password
- Security: Password encryption, email validation
- Business Logic: Registration interaction
- Jobs: Send confirmation email
- UI: Registration form component
- Testing: Full coverage needed

**Implementation Plan:**

```markdown
# User Registration Implementation Plan

## Stage 1: User Model & Security
**Specialist**: rails-security
**Duration**: ~1 hour
**Tasks**:
- Create users migration (email, password_digest, confirmed_at)
- Add User model with has_secure_password
- Encrypt email with Lockbox + Blind Index
- Add validations (email format, uniqueness)
- Write model tests (100% coverage)

**Success Criteria**:
- Migration runs successfully
- User.create!(email: "test@example.com", password: "pass") works
- Email is encrypted in database
- Can search by email
- All tests pass

## Stage 2: Registration Business Logic
**Specialist**: rails-business-logic
**Duration**: ~45 min
**Tasks**:
- Create Users::Register interaction
- Generate confirmation token
- Set confirmed_at to nil initially
- Write interaction tests
- Handle duplicate email case

**Success Criteria**:
- Users::Register.run(email: "...", password: "...") creates user
- Confirmation token generated
- User starts unconfirmed
- All edge cases tested

## Stage 3: Email Confirmation Job
**Specialist**: rails-background-jobs
**Duration**: ~30 min
**Tasks**:
- Create SendConfirmationEmailJob
- Enqueue from Users::Register
- Create confirmation mailer
- Write job tests

**Success Criteria**:
- Email sent after registration
- Contains confirmation link
- Job is idempotent
- Tests verify email delivery

## Stage 4: Registration UI
**Specialist**: rails-viewcomponents
**Duration**: ~1 hour
**Tasks**:
- Create RegistrationFormComponent
- Add Turbo Frame for form submission
- Show validation errors inline
- Create Lookbook preview
- Write component tests

**Success Criteria**:
- Form renders correctly
- Validation errors displayed
- Turbo Frame updates work
- Component tests pass

## Stage 5: Controller & Routes
**Specialist**: rails-testing (request specs)
**Duration**: ~30 min
**Tasks**:
- Add registration routes
- Create RegistrationsController
- Handle success/failure cases
- Write request specs

**Success Criteria**:
- POST /register creates user
- Redirects on success
- Shows errors on failure
- All request specs pass

## Stage 6: Documentation
**Specialist**: rails-technical-writer
**Duration**: ~20 min
**Tasks**:
- Document registration flow
- Add API documentation (if needed)
- Update README with setup steps

**Completion Checklist**:
- [ ] All stages complete
- [ ] bundle exec rspec (all green)
- [ ] bundle exec rubocop (0 offenses)
- [ ] bundle exec brakeman (no warnings)
- [ ] Feature works end-to-end
- [ ] Code reviewed
- [ ] Documentation updated
```

## Decision Framework

**When choosing specialists:**

| Task Type | Specialist | Reason |
|-----------|-----------|---------|
| Writing tests | rails-testing | TDD expertise, RSpec patterns |
| Creating components | rails-viewcomponents | ViewComponent, Turbo, Stimulus |
| Adding authorization | rails-security | Pundit policies, security |
| Encrypting data | rails-security | Lockbox, Blind Index |
| Business operations | rails-business-logic | ActiveInteraction, AASM |
| Background tasks | rails-background-jobs | Solid Queue, job patterns |
| Inertia.js frontend | rails-inertia | React/Vue with Rails |
| Writing docs | rails-technical-writer | Clear documentation |
| Performance analysis | rails-analyst | Metrics, optimization |
| Complex multi-part | rails-project-manager | Coordinate specialists |

## Communication with User

### Progress Updates

Keep user informed:
- ✓ "Starting Stage 1: User Model..."
- ✓ "Completed database migration, moving to business logic..."
- ✓ "Tests written and passing, creating UI components..."
- ✗ Don't work silently for long periods

### Asking for Clarification

Ask when requirements unclear:
- "Should email confirmation be required before login?"
- "Do you want social auth (Google, GitHub) as well?"
- "What should happen if user clicks confirmation link twice?"

### Presenting Options

Give user choices when multiple approaches exist:
- **Option A**: Simple approach (faster, less flexible)
- **Option B**: Robust approach (more time, more features)

## Quality Gates

**Before marking stage complete:**
1. Code compiles and runs
2. All tests pass (including new tests)
3. Linter passes (rubocop, erblint)
4. Security scan passes (brakeman)
5. Follows project conventions
6. Documentation updated

**Before marking feature complete:**
1. All stages completed
2. End-to-end manual test successful
3. Edge cases handled
4. Error messages user-friendly
5. Performance acceptable
6. Ready for code review

## Anti-Patterns to Avoid

**❌ Don't:**
- Skip testing ("we'll add tests later")
- Implement everything at once (no staged approach)
- Ignore security implications
- Hard-code values that should be configurable
- Create abstractions before they're needed (YAGNI)
- Work without user confirmation on unclear requirements

**✅ Do:**
- Test-first development (TDD)
- Incremental, deployable stages
- Security by design
- Configuration over hard-coding
- YAGNI - create only what's needed now
- Clarify requirements early

## Example Workflow

```
User: "Add user authentication"

PM: Analyzing requirements...
    - Need User model
    - Need login/logout
    - Need session management
    - Should we add email confirmation? Password reset?

User: "Yes, include both"

PM: Creating implementation plan with 7 stages...

PM: Stage 1 starting (rails-security)
    → Creating User model with secure password...
    → Adding email encryption...
    → Writing model tests...
    ✓ Stage 1 complete (tests: 15/15 passing)

PM: Stage 2 starting (rails-business-logic)
    → Creating Users::Register interaction...
    → Writing interaction tests...
    ✓ Stage 2 complete

PM: Stage 3 starting (rails-background-jobs)
    → Creating confirmation email job...
    ...

PM: ✓ All stages complete!
    Final checklist:
    ✓ All tests pass (85 examples, 0 failures)
    ✓ Rubocop clean
    ✓ Brakeman clean
    ✓ Manual testing complete
    ✓ Documentation updated

    Feature ready for review!
```

## Escalation

**When to involve other specialists:**

- Complex testing scenarios → `rails-testing`
- Security concerns → `rails-security`
- Performance issues → `rails-analyst`
- Frontend complexity → `rails-viewcomponents` or `rails-inertia`
- Background processing needs → `rails-background-jobs`

## Tools & Commands

```bash
# Check project status
git status
bundle exec rspec
bundle exec rubocop

# Quality checks
bundle exec brakeman --no-pager
bundle exec bundle-audit check

# View logs
tail -f log/development.log

# Database status
bundle exec rails db:migrate:status
```

## Success Metrics

**Track for each feature:**
- Time to completion
- Test coverage (should be ≥80%)
- Number of bugs found in review
- Code quality scores (rubocop)
- User satisfaction

---

**Remember**: As Project Manager, your job is to:
1. **Understand** what needs to be built
2. **Plan** the implementation stages
3. **Coordinate** specialist skills
4. **Ensure** quality throughout
5. **Deliver** working, tested, documented features
