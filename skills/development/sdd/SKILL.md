---
name: sdd (Spec Driven Development)
description: This skill outlines how to follow the spec driven development workflow. The workflow is non-negotiable and must be followed for sdd or Spec Driven Development. Use this for writing, refining and reviewing specs, specifications, designs, tasks, test and implementations.
version: 0.1.13
---

# Spec Driven Development (SDD)

## Practical Guidelines

### Project Structure and Paths

All SDD artifacts live in the `.sdd/` folder at the repository root. Use these exact paths:

| Variable | Path |
|----------|------|
| `SDD_FOLDER` | `.sdd/` |
| `SDD_INDEX` | `.sdd/index.md` |
| `SDD_PROJECT_FOLDER` | `.sdd/[FEATURE]/` |
| `SDD_SPECIFICATION_DOCUMENT` | `.sdd/[FEATURE]/specification.md` |
| `SDD_DESIGN_DOCUMENT` | `.sdd/[FEATURE]/design.md` |
| `SDD_PROJECT_GUIDELINES` | `.sdd/project-guidelines.md` |

Where `[FEATURE]` is the kebab-case name of the feature (e.g., `user-authentication`, `shopping-cart`).

### Templates

- `SDD_TEMPLATE_INDEX` located in `templates/index.template.md` used for feature index
- `SDD_TEMPLATE_SPECIFICATION` located in `templates/specification.template.md` used for initial requirements gathering
- `SDD_TEMPLATE_DESIGN` located in `templates/design.template.md` used for design documents
- `SDD_TEMPLATE_PROJECT_GUIDELINES` located in `templates/project-guidelines.template.md` used for project-specific conventions

### Project Guidelines

The `SDD_PROJECT_GUIDELINES` file (`.sdd/project-guidelines.md`) contains project-specific conventions that agents MUST follow in all phases. This file can:

1. **Reference existing documentation** - List paths to docs, READMEs, or other files containing conventions
2. **Define inline guidelines** - Specify conventions directly in the file

You MUST read this file during exploration and apply these conventions to architectural decisions.

### Domain Skills

After exploring the codebase and understanding the task, identify which domain skills apply:

- **distributed-systems**: Multiple services, network coordination, eventual consistency
- **low-level-systems**: Memory management, performance-critical, OS interfaces
- **security**: Auth, untrusted input, sensitive data, compliance
- **infrastructure**: Cloud resources, IaC, networking, disaster recovery
- **devops-sre**: CI/CD, deployment, observability, SLOs
- **data-engineering**: Pipelines, ETL, schema evolution, data quality
- **api-design**: Public/internal APIs, versioning, contracts

Load relevant skills and apply their mindset and practices throughout specification, design, and review phases.

### Requirement Traceability

Requirements use fully-qualified IDs in the format `[feature-name:REQ-ID]` where:
- `feature-name` is the kebab-case folder name (e.g., `user-authentication`)
- `REQ-ID` is the requirement ID from the specification (e.g., `FR-001`, `NFR-002`)

This format MUST be used consistently in:

**Code comments:**
```python
# Implements [user-authentication:FR-003] - Password must be hashed before storage
def hash_password(password: str) -> str:
```

**Test documentation:**
```python
def test_password_hashing():
    """Verifies [user-authentication:FR-003] - Password hashing"""
```

**Design documents** - Always use fully-qualified IDs when referencing requirements.

This enables grep-based traceability: `grep -r "\[user-authentication:FR-003\]"` finds all code and tests implementing a requirement.

### Test Scenario Traceability

Test scenarios use fully-qualified IDs in the format `[feature-name:SCENARIO-ID]` where:
- `feature-name` is the kebab-case folder name (e.g., `user-authentication`)
- `SCENARIO-ID` is the scenario ID from the design:
  - Component scenarios: `ComponentName/TS-XX` (e.g., `AuthService/TS-01`)
  - Integration scenarios: `ITS-XX` (e.g., `ITS-01`)
  - E2E scenarios: `E2E-XX` (e.g., `E2E-01`)

This format MUST be used in **test code only** (not implementation code), via documentation comments or docstrings as appropriate for the language:

**Test documentation:**
```python
def test_valid_credentials_return_session():
    """Verifies [user-authentication:AuthService/TS-01] - Valid credentials return session token

    Given: A registered user with valid credentials
    When: User submits correct username and password
    Then: A valid session token is returned
    """
```

**Design documents** - The Test Scenario Validation section must map every scenario to tasks.

This enables grep-based traceability: `grep -r "\[user-authentication:AuthService/TS-01\]" tests/` finds all tests verifying a scenario.

## Processes

You **MUST** explore the code base using tools like Read, Glob etc before doing **ANY** of the below.
You **MUST** understand project guidelines starting with the file [SDD_PROJECT_GUIDELINES]

### Creating

Do this when a user asks to create a specification or design

You MUST create the required document in the relevant feature specific folder in the `.sdd/` folder at the root of the project

**Maintain the index:**
1. If `.sdd/index.md` doesn't exist, create it from `templates/index.template.md`
2. Add a row for the new feature (newest entries at top, ordered by date)
3. Update the status as the feature progresses through Draft → Approved → Implemented

**Examples**

**If** the user asks to create a **specification** for user authentication **then** copy `templates/specification.template.md` to `.sdd/user-authentication/specification.md` if it doesn't already exist.

**If** the user asks to create a **design** for user authentication **then** copy `templates/design.template.md` to `.sdd/user-authentication/design.md` if it doesn't already exist.

### Specifying

Your **GOAL** is to complete all parts of the specification template for the feature.

**Scope:** A single specification should represent approximately 1 day of implementation work. If the feature is larger, break it into multiple specifications. During the discovery interview, sense check the scope and suggest splitting if necessary.

**CRITICAL: Template structure is sacred.**
- Do NOT add sections that aren't in the template
- Do NOT remove sections from the template
- Do NOT rename sections
- If a section doesn't apply, write "N/A" or "None" with brief justification
- Follow the template structure EXACTLY as defined in [SDD_TEMPLATE_SPECIFICATION]

#### Process

**Phase 1: Discovery Interview**

Interview the user about their idea or brief. Keep asking questions until you can unambiguously fill out every section of the template. Don't ask about template sections directly - ask about their problem, users, and goals.

- What problem are they solving? Why does it matter?
- Who experiences this problem? How do they cope today?
- What does success look like? How will they know it's working?
- What are the boundaries? What's explicitly not included?
- What could go wrong? What are the edge cases?

**Probe vague answers relentlessly** - Don't accept "fast", "secure", or "user-friendly" without measurable criteria. Keep questioning until requirements are specific and testable.

**NFRs are optional** - Only include non-functional requirements when there are genuine, measurable quality constraints (e.g., specific latency targets, compliance requirements). Most features don't need them.

**Phase 2: Write the Specification**

Once you have enough information to fill out every section unambiguously, write the complete specification in one pass. Do not ask further questions during this phase.

You **MUST** complete [SDD_SPECIFICATION_DOCUMENT] **FULLY** for the feature

### Designing

Your **GOAL** is to complete all parts of the design template for the feature.

**Purpose:** The design document is a complete handover document. Anyone on the team should be able to pick it up and carry out the implementation without needing to ask clarifying questions.

**Level of detail:** Include enough detail to enable handover to another team member, but not so much that you replicate the implementation in the document. Describe *what* and *why*, not *how* at the code level.

**CRITICAL: Template structure is sacred.**
- Do NOT add sections that aren't in the template
- Do NOT remove sections from the template
- Do NOT rename sections
- If a section doesn't apply, write "N/A" or "None" with brief justification
- Follow the template structure EXACTLY as defined in [SDD_TEMPLATE_DESIGN]

#### Process

**Phase 1: Research**

Read and understand before designing:
- Read the specification thoroughly
- **Extract and list ALL functional and non-functional requirements by ID** - create a working checklist
- Explore the existing codebase for patterns, conventions, and integration points
- Read project guidelines if they exist

**Phase 2: Design**

Once you understand the requirements and codebase:

1. **Requirements Enumeration Checkpoint** (MANDATORY before writing components)
   - Create a checklist of every FR and NFR from the specification
   - For each requirement, identify which component(s) will address it
   - If a requirement cannot be mapped to a component, you must either:
     a. Add a new component to address it
     b. Document it in Feasibility Review with justification why it cannot be addressed
   - **Do NOT proceed until every requirement has a component assignment**

2. **Write the design document**
   - Work through components systematically
   - As you define each component, verify its Requirements References are complete
   - Cross-check against your requirements checklist as you go
   - Do NOT proceed to Task Breakdown until all requirements are mapped to components

3. **Complete Requirements Validation section BEFORE finalizing**
   - This is a mandatory checkpoint, not optional documentation
   - Every requirement must appear with at least one task reference
   - If any requirement is missing task coverage, add tasks to cover it
   - **A design with unmapped requirements is incomplete and must not be submitted**

You **MUST** identify components required to implement the feature in the specification

#### Component Identification

For each component, document:
- **Modified**: Current behavior, what changes, dependencies, test scenarios (Given/When/Then)
- **Added**: Single responsibility, consumers, location, requirements satisfied, test scenarios (Given/When/Then)
- **Used**: Existing components required as-is for implementation (document what it provides and why it's needed)

Keep components focused (single responsibility, minimal coupling, explicit dependencies). Define public interfaces and error handling. Avoid over-engineering for future needs.

#### API Design (When Needed)

**Design documents describe contracts, not code.**
API designs should:
- Describe operations conceptually (what they do, inputs, outputs, errors)
- Define data shapes and validation rules in prose or simple schemas
- Specify error conditions and expected behaviors
- Document constraints and invariants
- Show Interfaces

API designs should NOT include:
- Code of function implementations
- Language-specific syntax (unless illustrating a non-functional requirement)
- Internal implementation logic

**Exception:** Include code samples ONLY when they illustrate specific non-functional requirements:
- Serialization formats (JSON structure, protocol buffers)
- Concurrency patterns (mutex usage, async boundaries)
- Performance-critical algorithms (when the algorithm IS the requirement)
- Protocol specifics (wire format, handshake sequences)

**Example - GOOD (conceptual):**
> The `addToCart` operation accepts a product identifier and quantity. It validates the product exists and quantity is positive. On success, returns the updated cart. On failure, returns an error indicating whether the product was not found or quantity was invalid.

**Example - BAD (implementation leakage):**
```python
def add_to_cart(product_id: str, quantity: int) -> Cart:
    product = self.product_repo.get(product_id)
    if not product:
        raise ProductNotFoundError(product_id)
    ...
```

#### Test Scenarios

**Tests must verify user scenarios, not implementation details.**

GOOD tests (scenario-driven):
- "User can add item to cart and see updated total"
- "User receives error when submitting invalid email"
- "API returns 404 when product doesn't exist"

BAD tests (avoid these):
- Testing enum value equals itself
- Testing functions with low complexity or trivial implementations (e.g., simple getters, pass-through functions)
- "Concurrency tests" that don't actually run concurrent requests
- Mocking everything so the test only verifies mock setup
- Testing that a function was called (instead of its effect)

**If you can't realistically test an NFR, don't write a fake test.**
- Concurrency: Only test if you can run actual concurrent requests against separated client/server
- Performance: Only test if you have proper benchmarking infrastructure
- Security: Only test what you can actually verify (e.g., input validation, auth checks)

For NFRs that can't be tested in CI, document them as "Manual Verification Required" with instructions.

**Scenario ID Format:**
- Component scenarios: `ComponentName/TS-XX` (e.g., `CartService/TS-01`, `UserAuth/TS-02`)
- Integration scenarios: `ITS-XX` (e.g., `ITS-01`, `ITS-02`)
- E2E scenarios: `E2E-XX` (e.g., `E2E-01`, `E2E-02`)

**Scenario Structure:**
Each scenario uses Given/When/Then format:
- **Given**: Initial state or preconditions
- **When**: Action performed
- **Then**: Expected outcome


#### Instrumentation (optional)

Only needed if NFRs require observability. Skip for typical features.

#### Task Breakdown

- Group into logical phases ordered by dependencies
- Each task must have clear completion criteria
- Each task must specify which requirements it fulfills using `[feature:REQ-ID]` format
- Each task must reference which test scenarios (TS-IDs, ITS-IDs, E2E-IDs) it implements
- Testing happens WITH implementation, not after
- Every requirement must map to tasks (and vice versa)

#### Write the design

**Fill the design template**
- You will be given the path to the new design file
- Reference the **sdd** skill for the standard design template structure [SDD_TEMPLATE_DESIGN]
- Follow the template structure exactly
- Ensure every section is complete and detailed
- Link requirements to components to tasks for full traceability
- Always save the document once you've finished designing. **Never** skip this step

**Ensure requirement coverage**
- Every functional requirement must map to one or more components
- Every non-functional requirement must map to implementation decisions
- Every requirement must map to one or more tasks
- Use the Requirements Validation section to verify complete coverage
- No requirement should be left unaddressed in the design
- If a requirement cannot be addressed, document it in Feasibility Review

#### Design Quality Standards

A complete design document must have:
- ✅ **Link to specification** via the Linked Specification field
- ✅ **Architecture overview** explaining current context and proposed changes
- ✅ **All requirements traced** to components via Requirements References
- ✅ **All components defined** with clear descriptions and locations
- ✅ **Component test scenarios** using Given/When/Then format with unique IDs (ComponentName/TS-XX)
- ✅ **Integration test scenarios** covering multi-component interactions (ITS-XX)
- ✅ **E2E test scenarios** covering complete user workflows (E2E-XX)
- ✅ **Risks identified** with mitigation strategies
- ✅ **Tasks organized** into logical phases with dependencies
- ✅ **Tasks reference test scenarios** they implement (TS-IDs, ITS-IDs, E2E-IDs)
- ✅ **Requirements validation** showing every requirement maps to tasks
- ✅ **No TBDs or ambiguities** in the final design
- ✅ **Instrumentation defined** if NFRs require observability
- ✅ **Standard structure** following [SDD_TEMPLATE_DESIGN] exactly
- ✅ **Project guidelines compliance** if SDD_PROJECT_GUIDELINES exists

### Refining

When asked to refine a specification or design:
1. Read existing documents and linked specification thoroughly
2. Identify gaps, inconsistencies, or new requirements
3. Explore codebase for changed context or new patterns
4. Ask stakeholder about changed priorities or constraints
5. Update documents while maintaining template structure
6. Verify all requirements still map to components and tasks

### Implementing

**CRITICAL:** You must read the design document, specification, and project guidelines before starting any implementation.

#### Before Writing Any Code

Read the design, specification, existing code, and documentation thoroughly. If anything is unclear or ambiguous, ask before guessing.

#### When implementing a feature:

1. **Read and understand the design**
   - Read the design document and linked specification
   - Understand all tasks and which phase you are implementing
   - Identify prerequisites or dependencies

2. **Read project guidelines**
   - Check for `.sdd/project-guidelines.md` (SDD_PROJECT_GUIDELINES)
   - Read all referenced documentation files
   - Note error handling, logging, naming, and testing conventions
   - **CRITICAL** These conventions MUST inform your implementation decisions

3. **Set up the feature branch**
   - Create a feature branch for the current phase
   - Use a descriptive branch name (e.g., `feature/auth-phase-1`)

4. **Implement task by task**
   - Work through tasks in order as specified in the design
   - For each task:
     a. Write tests first (TDD when appropriate)
     b. Implement the code to pass tests
     c. Run linters and formatters
     d. Run the full test suite
     e. Commit the completed task with a clear message
     f. Update the task status in the design document
   - Do NOT skip ahead or batch multiple tasks into one commit

5. **Validate continuously** - Build, lint, and test after each task. Fix issues immediately.

6. **Track progress** - Mark tasks complete in design document. Document deviations and issues.

7. **Complete the phase** - All tasks done, tests passing, code linted. Wait for merge before next phase.

#### Dead Code

- Any dead code introduced in intermediate phases **MUST** be tracked in the design document with a `DC-XX` identifier
- Dead code **MUST** include a comment referencing its identifier (e.g., `// DC-01`)
- All dead code **MUST** be used by the end of the final phase

#### Stubs

- Any stub implementations **MUST** be tracked in the design document with a `ST-XX` identifier
- Stubs **MUST** include a comment referencing their identifier (e.g., `// ST-01`)
- All stubs **MUST** be implemented or removed by the end of the final phase

### Reviewing

The user can ask to review a specification, design or implementation. Follow the process below and produce a report for the user at the end.

**CRITICAL**: You MUST use the Task tool to create a subagent for the review.

#### Common Review Steps

1. Read specification, design, and project guidelines (if exists)
2. Load relevant domain skills based on the feature (e.g., security, api-design, distributed-systems) and apply their review criteria
3. Verify requirements traceability and coverage
4. Check for edge cases and architectural fit
5. Validate against project conventions (error handling, logging, naming, testing)

#### Specification Review

**Focus areas:**
- Verify achievability and dependencies
- Ensure requirements are testable and measurable (not implementation details)
- Check for conflicts with existing functionality
- Validate scope is appropriate for single iteration

**Abstraction level check:**

GOOD (stays at specification level):
- "Users must be able to search products by name"
- "Search results must return within 500ms for 95th percentile"

BAD (contains implementation details):
- "Use Elasticsearch for product search"
- "Create a ProductSearchService class"

**Red flags:**
- Implementation details masquerading as requirements
- Vague/untestable requirements
- Unrealistic performance expectations
- Dependencies on unavailable services
- Requirements that assume non-existent functionality

#### Design Review

**Focus areas:**
- All requirements traced to components and tasks
- No implementation leakage (describe contracts conceptually, not code)
- Tests included WITH tasks, not deferred to later phases
- Architectural decisions fit existing codebase patterns
- Project guidelines compliance (if SDD_PROJECT_GUIDELINES exists)
- Test Scenario Validation section is complete (no orphan scenarios)
- Instrumentation section present if NFRs require observability

**Task-level test verification:**
- Each task must have a "Test Scenarios:" field referencing specific scenario IDs (TS-XX, ITS-XX, E2E-XX)
- No separate "add tests" tasks or testing phases
- All component, integration, and E2E test scenarios must be assigned to tasks
- Test Scenario Validation section maps every scenario to at least one task

**Example of GOOD task structure:**
```
**Task 1: Implement CartService.addItem()**
- Status: Backlog
- Requirements: [shopping-cart:FR-001], [shopping-cart:FR-002]
- Test Scenarios: [shopping-cart:CartService/TS-01], [shopping-cart:ITS-01]
- Details:
  fn addItem(productId: string, quantity: int) -> Cart
    throws: ProductNotFound, InvalidQuantity
```

**Example of BAD task structure:**
```
Phase 1: Implement CartService
Phase 2: Add unit tests for CartService  ← VIOLATION
```

**Red flags:**
- Requirements not traced to components/tasks
- Code samples in API design sections
- Separate "add tests" phases
- TBDs or ambiguities
- Architectural decisions conflicting with existing patterns
- Missing risk assessment
- Test scenarios missing Given/When/Then structure

#### Implementation Review

**Diff analysis:**
- Run `git diff main...HEAD` to understand scope
- Verify all design tasks are represented
- Check for changes that don't correspond to any task

**Design validation:**
- Verify implementation matches design tasks
- Check that APIs and interfaces match design contracts
- Flag any undocumented deviations
- If design was altered, verify workarounds are documented

**Traceability verification:**
- Code comments reference requirements using `[feature-name:FR-XXX]` or `[feature-name:NFR-XXX]` format
- Test documentation (comments/docstrings) reference scenarios using `[feature-name:ComponentName/TS-XX]`, `[feature-name:ITS-XX]`, or `[feature-name:E2E-XX]` format
- Run `grep -r "\[feature-name:" src/ tests/` to verify coverage
- Verify all scenarios from design have corresponding test implementations

**Check for stubs:**
- Search for: `skip`, `todo`, `pending`, `@pytest.mark.skip`, `pass` in test functions, placeholder assertions
- **Intermediate phases**: Stubs acceptable only if tracked in design document
- **Final phase**: No stubs allowed

**Check for dead code:**
- Unused imports, variables, or functions
- Commented-out code
- **Intermediate phases**: Dead code acceptable only if tracked in design document
- **Final phase**: No dead code allowed

**Quality gates:**
- Run all tests (unit, integration, e2e)
- Run linters and formatters
- Build/compile the project
- Verify code follows documented practices
- Verify instrumentation from design is implemented (metrics emitted, logs present, traces configured)

**Red flags:**
- Implementation doesn't match design
- Requirements removed without justification
- New code without tests
- Untracked stubs or dead code (in final phase)
- Failing tests or linting errors
- Undocumented deviations from design
- Test scenarios not referenced in test implementations
- Orphan scenarios (defined but never assigned to tasks)
- Security vulnerabilities
- Missing requirement traceability in code comments
- Missing scenario references in test documentation
- Instrumentation defined in design but not implemented

#### Quality Standards (All Reviews)

A thorough review must verify:
- ✅ Requirements coverage complete
- ✅ Tests adequate and passing (scenario-driven, avoid trivial tests)
- ✅ All test scenarios use Given/When/Then format with unique IDs
- ✅ Integration test scenarios cover component interactions
- ✅ E2E test scenarios cover complete user workflows
- ✅ No TBDs or ambiguities
- ✅ Project guidelines followed
- ✅ Risks identified with mitigations
- ✅ All stubs and dead code tracked (intermediate) or resolved (final)
- ✅ Code and tests use fully-qualified requirement IDs `[feature:REQ-ID]`
- ✅ Tests use fully-qualified scenario IDs `[feature:ComponentName/TS-XX]`, `[feature:ITS-XX]`, `[feature:E2E-XX]`
- ✅ All scenarios mapped to tasks (no orphans)

#### Review Severity Levels

All review findings MUST be categorized by severity. Reports must list findings grouped by severity, with P0 issues first.

**P0 - Blocking (must fix before approval):**
- Missing tests for new code
- Failing tests
- Untracked stubs in final phase
- Security vulnerabilities
- Requirements not covered by implementation
- New code without corresponding test scenarios

**P1 - High (should fix before approval):**
- Missing requirement traceability in code comments
- Missing scenario references in test documentation
- Undocumented deviations from design
- Orphan test scenarios (defined but not implemented)
- Dead code in final phase

**P2 - Medium (fix recommended):**
- Test scenarios missing Given/When/Then structure
- Minor architectural inconsistencies
- Missing risk mitigations

**P3 - Low (nice to have):**
- Style inconsistencies not caught by linter
- Documentation improvements
- Minor naming convention deviations

**Report format:**
Reviews MUST present findings in severity order:
```
## P0 - Blocking
- [Finding description and location]

## P1 - High
- [Finding description and location]

## P2 - Medium
- [Finding description and location]

## P3 - Low
- [Finding description and location]
```

A review with any P0 findings MUST recommend rejection until resolved.
