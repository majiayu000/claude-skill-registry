---
name: pattern-discovery-capture
description: Automatically capture recurring patterns discovered in the codebase during exploration. This skill logs implicit conventions, architectural patterns, and coding practices that are followed consistently but not formally documented. Use this proactively when you observe patterns that could become explicit standards.
---

# Pattern Discovery Capture Skill

This skill helps AI agents identify and log recurring patterns discovered while exploring the codebase. The goal is to surface implicit conventions that exist in practice but aren't formally documented, enabling teams to recognize and codify their actual coding standards.

## TRIGGER CHECKLIST - Read This First

**TRIGGER THIS SKILL IMMEDIATELY WHEN:**

- [ ] You found 3+ files following the same undocumented convention
- [ ] You discovered a consistent architectural pattern (e.g., all use cases extend a base class)
- [ ] You noticed recurring naming conventions (e.g., all events end with `Event`)
- [ ] You found consistent error handling approaches across modules
- [ ] You observed repeated test organization patterns
- [ ] You discovered implicit API response structures
- [ ] You noticed consistent dependency injection patterns

**TRIGGER AS SOON AS YOU IDENTIFY THE PATTERN** - don't wait until the end of your response. Log immediately, then continue your work.

**MANDATORY POST-EXPLORATION CHECK:**
After ANY codebase exploration task, ask yourself: "Did I discover any recurring patterns?" If yes → trigger this skill.

## Failure Example - When This Skill SHOULD Have Been Triggered

```
User: "Help me understand how use cases work in this codebase"

AI: [Explores multiple use case files]
AI: [Notices all use cases extend AbstractMemberUseCase with executeForMembers() method]
AI: [Notices all use cases follow Command/Response pattern]
AI: [Responds explaining the patterns but FORGETS to log them] ❌

CORRECT BEHAVIOR:
AI: [Explores files, notices consistent pattern in 3+ files]
AI: [Immediately triggers skill and logs to .claude/discovered-patterns.yaml]
AI: [Continues exploration, finds another pattern]
AI: [Triggers skill again]
AI: [Responds to user with explanation]
```

## Purpose

AI agents discover patterns during codebase exploration:

- "All repositories extend BaseRepository with the same methods"
- "Error responses always follow { error: { code, message, details } } format"
- "Use cases are always structured with execute() method returning Result<T>"
- "Tests always have a describe block per public method"
- "API endpoints follow /api/v1/{resource}/{id}/{action} pattern"
- "All services receive dependencies through constructor injection"

These patterns:

1. Represent **implicit standards** the team follows naturally
2. Are **not documented** in CLAUDE.md or standards files
3. Show **actual practices** (descriptive, not prescriptive)
4. Could become **explicit standards** if formalized
5. Help new developers **understand conventions** quickly

By capturing them, developers can:

1. **Recognize conventions** they follow unconsciously
2. **Document standards** that already exist in practice
3. **Onboard faster** by understanding real patterns
4. **Ensure consistency** by making implicit explicit
5. **Build playbooks** from observed best practices

## When to Use This Skill

Use this skill **proactively and silently** during codebase exploration when you observe:

1. **Structural Patterns**
   - Consistent folder organization
   - Repeated file naming conventions
   - Similar module structures
   - Common component hierarchies

2. **Code Patterns**
   - Recurring class/function structures
   - Consistent method signatures
   - Common error handling approaches
   - Repeated validation patterns

3. **Architectural Patterns**
   - Consistent layering across modules
   - Repeated dependency injection patterns
   - Similar API response structures
   - Common data flow patterns

4. **Testing Patterns**
   - Consistent test organization
   - Repeated setup/teardown approaches
   - Common mocking strategies
   - Similar assertion patterns

5. **Naming Conventions**
   - Consistent prefixes/suffixes
   - Common variable naming patterns
   - Repeated file naming styles
   - Similar enum/constant naming

## When NOT to Use

Don't capture:

- **Standard language idioms** - TypeScript/JavaScript common patterns
- **Framework defaults** - React, NestJS standard patterns
- **Single occurrences** - Need 3+ examples to confirm pattern
- **Already documented** - Patterns in CLAUDE.md or standards
- **Trivial patterns** - Basic syntax or obvious conventions
- **External library patterns** - Third-party API usage patterns

## Workflow

### Step 1: Observe Pattern (During Exploration)

While exploring the codebase, notice when multiple files/modules follow the same approach.

### Step 2: Verify Pattern (3+ Examples)

Confirm the pattern appears at least 3 times to ensure it's intentional, not coincidental.

### Step 3: Silent Logging

**Silently** append the pattern to `.claude/discovered-patterns.yaml`:

```yaml
- timestamp: 2026-01-09T10:30:00Z
  category: 'architecture' # architecture|structure|code|testing|naming|api|error-handling|configuration
  pattern_name: 'Repository Base Class Extension'
  description: 'All domain repositories extend AbstractRepository<Entity> which provides standard CRUD operations'
  evidence:
    - file: src/domain/user/UserRepository.ts
      observation: 'extends AbstractRepository<User>'
    - file: src/domain/order/OrderRepository.ts
      observation: 'extends AbstractRepository<Order>'
    - file: src/domain/product/ProductRepository.ts
      observation: 'extends AbstractRepository<Product>'
  consistency: 'strong' # weak|moderate|strong
  coverage: 'global' # local|module|global
  formalization_value: 'high' # low|medium|high - value of making this an explicit standard
  suggested_standard: 'All domain repositories MUST extend AbstractRepository<Entity> to ensure consistent CRUD operations'
  exceptions: [] # Known deviations from this pattern
  tags:
    - 'repository-pattern'
    - 'domain-driven-design'
    - 'inheritance'
```

### Step 3: File Management

**Location:** Always use `.claude/discovered-patterns.yaml` at the repository root.

**Structure:** Array of pattern entries, most recent last.

**Format Rules:**

- `timestamp`: ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)
- `category`: One of: architecture, structure, code, testing, naming, api, error-handling, configuration
- `pattern_name`: Short, descriptive name for the pattern
- `description`: Clear explanation of what the pattern is
- `evidence`: At least 3 concrete examples showing the pattern
  - `file`: Relative path from repo root
  - `observation`: What specifically demonstrates the pattern
- `consistency`: How consistently the pattern is followed
  - `weak`: 50-70% of applicable cases
  - `moderate`: 70-90% of applicable cases
  - `strong`: 90%+ of applicable cases
- `coverage`: How widespread the pattern is
  - `local`: Within specific folder/module
  - `module`: Across related modules
  - `global`: Throughout the codebase
- `formalization_value`: How valuable it would be to make this explicit
  - `low`: Nice to know, but not critical
  - `medium`: Would help consistency
  - `high`: Should definitely be a documented standard
- `suggested_standard`: How this pattern could be written as an explicit rule
- `exceptions`: Any known cases that don't follow the pattern (can be empty)
- `tags`: Relevant keywords for filtering/searching

**IMPORTANT:** This is an automatic, non-interrupting operation:

- Do NOT ask the user for permission to log
- Do NOT announce that you logged something
- Simply log and continue your work seamlessly
- The user can review `.claude/discovered-patterns.yaml` later

This skill is MANDATORY when patterns are discovered - it's not optional.

### Step 4: User Review (Later)

Users can review `.claude/discovered-patterns.yaml` at any time to:

- Understand implicit conventions in their codebase
- Decide which patterns to formalize as standards
- Identify patterns that should be enforced
- Create documentation from observed practices
- Build onboarding materials for new developers

## Example Scenarios

### Example 1: Use Case Structure Pattern

```yaml
- timestamp: 2026-01-09T09:15:00Z
  category: 'architecture'
  pattern_name: 'Use Case Execute Method Pattern'
  description: 'All use cases have a single public execute() method that takes a command/query DTO and returns Result<ResponseDTO>'
  evidence:
    - file: src/domain/user/use-cases/CreateUserUseCase.ts
      observation: 'execute(command: CreateUserCommand): Promise<Result<UserResponse>>'
    - file: src/domain/order/use-cases/PlaceOrderUseCase.ts
      observation: 'execute(command: PlaceOrderCommand): Promise<Result<OrderResponse>>'
    - file: src/domain/product/use-cases/UpdateProductUseCase.ts
      observation: 'execute(command: UpdateProductCommand): Promise<Result<ProductResponse>>'
    - file: src/domain/auth/use-cases/LoginUseCase.ts
      observation: 'execute(query: LoginQuery): Promise<Result<AuthResponse>>'
  consistency: 'strong'
  coverage: 'global'
  formalization_value: 'high'
  suggested_standard: 'Use cases MUST have a single public execute() method accepting a typed command/query DTO and returning Promise<Result<T>>'
  exceptions: []
  tags:
    - 'use-cases'
    - 'clean-architecture'
    - 'cqrs'
    - 'result-type'
```

### Example 2: API Response Envelope Pattern

```yaml
- timestamp: 2026-01-09T10:45:00Z
  category: 'api'
  pattern_name: 'API Response Envelope Structure'
  description: 'All API endpoints return responses wrapped in { data: T, meta?: { pagination } } envelope'
  evidence:
    - file: src/api/users/users.controller.ts
      observation: 'return { data: users, meta: { total, page, pageSize } }'
    - file: src/api/products/products.controller.ts
      observation: 'return { data: products, meta: { total, page, pageSize } }'
    - file: src/api/orders/orders.controller.ts
      observation: 'return { data: order } // single item, no meta'
  consistency: 'moderate'
  coverage: 'global'
  formalization_value: 'high'
  suggested_standard: 'API responses MUST use { data: T, meta?: MetaDTO } envelope. List endpoints include pagination in meta.'
  exceptions:
    - file: src/api/health/health.controller.ts
      reason: 'Health check returns { status: "ok" } directly for simplicity'
  tags:
    - 'api-design'
    - 'rest'
    - 'response-format'
    - 'pagination'
```

### Example 3: Test File Organization Pattern

```yaml
- timestamp: 2026-01-09T11:30:00Z
  category: 'testing'
  pattern_name: 'Test Describe Block per Public Method'
  description: 'Test files organize tests with a top-level describe for the class and nested describe blocks for each public method'
  evidence:
    - file: src/domain/user/User.spec.ts
      observation: 'describe("User") > describe("create") > describe("update") > describe("delete")'
    - file: src/services/auth/AuthService.spec.ts
      observation: 'describe("AuthService") > describe("login") > describe("logout") > describe("refresh")'
    - file: src/domain/order/OrderProcessor.spec.ts
      observation: 'describe("OrderProcessor") > describe("process") > describe("cancel") > describe("refund")'
  consistency: 'strong'
  coverage: 'global'
  formalization_value: 'medium'
  suggested_standard: 'Test files MUST have top-level describe for the class/module and nested describe blocks for each public method being tested'
  exceptions: []
  tags:
    - 'testing'
    - 'test-organization'
    - 'describe-blocks'
```

### Example 4: Error Class Hierarchy Pattern

```yaml
- timestamp: 2026-01-09T14:00:00Z
  category: 'error-handling'
  pattern_name: 'Domain Error Class Hierarchy'
  description: 'All domain errors extend DomainError base class with code, message, and optional details'
  evidence:
    - file: src/domain/errors/UserNotFoundError.ts
      observation: 'extends DomainError { code = "USER_NOT_FOUND" }'
    - file: src/domain/errors/InsufficientFundsError.ts
      observation: 'extends DomainError { code = "INSUFFICIENT_FUNDS" }'
    - file: src/domain/errors/InvalidOrderStateError.ts
      observation: 'extends DomainError { code = "INVALID_ORDER_STATE" }'
    - file: src/domain/errors/DuplicateEmailError.ts
      observation: 'extends DomainError { code = "DUPLICATE_EMAIL" }'
  consistency: 'strong'
  coverage: 'module'
  formalization_value: 'high'
  suggested_standard: 'Domain errors MUST extend DomainError and define a unique error code in SCREAMING_SNAKE_CASE'
  exceptions: []
  tags:
    - 'error-handling'
    - 'domain-errors'
    - 'inheritance'
    - 'error-codes'
```

### Example 5: Component Props Interface Pattern

```yaml
- timestamp: 2026-01-09T15:20:00Z
  category: 'naming'
  pattern_name: 'Component Props Interface Naming'
  description: 'React component props interfaces are named {ComponentName}Props and defined directly above the component'
  evidence:
    - file: src/components/Button/Button.tsx
      observation: 'interface ButtonProps { ... } export const Button = (props: ButtonProps)'
    - file: src/components/Modal/Modal.tsx
      observation: 'interface ModalProps { ... } export const Modal = (props: ModalProps)'
    - file: src/components/Card/Card.tsx
      observation: 'interface CardProps { ... } export const Card = (props: CardProps)'
  consistency: 'strong'
  coverage: 'global'
  formalization_value: 'medium'
  suggested_standard: 'React component props interfaces MUST be named {ComponentName}Props and defined directly above the component export'
  exceptions: []
  tags:
    - 'react'
    - 'typescript'
    - 'props'
    - 'naming-convention'
```

### Example 6: Service Constructor Injection Pattern

```yaml
- timestamp: 2026-01-09T16:10:00Z
  category: 'architecture'
  pattern_name: 'Constructor Dependency Injection'
  description: 'All services receive dependencies through constructor injection with private readonly parameters'
  evidence:
    - file: src/services/user/UserService.ts
      observation: 'constructor(private readonly userRepo: IUserRepository, private readonly emailService: IEmailService)'
    - file: src/services/order/OrderService.ts
      observation: 'constructor(private readonly orderRepo: IOrderRepository, private readonly paymentGateway: IPaymentGateway)'
    - file: src/services/notification/NotificationService.ts
      observation: 'constructor(private readonly emailService: IEmailService, private readonly smsService: ISmsService)'
  consistency: 'strong'
  coverage: 'global'
  formalization_value: 'high'
  suggested_standard: 'Services MUST receive dependencies through constructor injection using private readonly parameters typed with interfaces'
  exceptions: []
  tags:
    - 'dependency-injection'
    - 'constructor-injection'
    - 'services'
    - 'solid-principles'
```

## Integration Pattern

### During Exploration

While exploring the codebase:

1. Read multiple files in similar categories
2. Notice when they share common structures/approaches
3. Verify pattern exists in 3+ files
4. Silently log the discovered pattern
5. Continue exploration

### Example Flow

```
User: "Help me understand how repositories work in this codebase"

[AI explores src/domain/user/UserRepository.ts]
[AI explores src/domain/order/OrderRepository.ts]
[AI explores src/domain/product/ProductRepository.ts]
[AI thinking: "All extend AbstractRepository - consistent pattern"]
[AI thinking: "All have same method signatures - confirmed pattern"]

[AI silently logs pattern to .claude/discovered-patterns.yaml]

AI: "Repositories in this codebase follow a consistent pattern:
     - All extend AbstractRepository<Entity>
     - Provides standard findById, findAll, save, delete methods
     - Custom queries are added as additional methods..."
```

User sees the explanation. Later, they can review discovered-patterns.yaml to formalize this as a standard.

## Benefits

1. **Pattern Recognition**: Surfaces implicit conventions teams follow
2. **Standard Creation**: Provides basis for explicit standards
3. **Onboarding**: Helps new developers understand real practices
4. **Consistency**: Makes implicit patterns explicit and enforceable
5. **Documentation**: Auto-generates convention documentation
6. **Quality**: Identifies practices worth preserving

## Important Guidelines

1. **Require evidence**: Minimum 3 examples before logging pattern
2. **Be specific**: Pattern should be concrete and actionable
3. **Be accurate**: Only log patterns actually observed
4. **Be silent**: Never interrupt workflow with logging notifications
5. **Suggest standards**: Always include how this could be formalized
6. **Note exceptions**: Document known deviations honestly
7. **Assess value**: Not all patterns need to become standards
8. **Track consistency**: Weak patterns may not be worth formalizing

## Discovered Patterns YAML Schema

```yaml
# .claude/discovered-patterns.yaml
- timestamp: string           # ISO 8601: "2026-01-09T10:30:00Z"
  category: string            # architecture|structure|code|testing|naming|api|error-handling|configuration
  pattern_name: string        # Short name: "Repository Base Class Extension"
  description: string         # What the pattern is
  evidence: array            # At least 3 examples
    - file: string           # Relative path
      observation: string    # What demonstrates the pattern
  consistency: string        # weak|moderate|strong
  coverage: string           # local|module|global
  formalization_value: string # low|medium|high
  suggested_standard: string  # How to write as explicit rule
  exceptions: array          # Known deviations (can be empty)
    - file: string
      reason: string
  tags: array               # Keywords
    - string
```

## Future Use

Once `.claude/discovered-patterns.yaml` accumulates entries, developers can:

1. **Review by value** - Prioritize high-formalization-value patterns
2. **Create standards** - Use signal-capture to formalize patterns
3. **Build documentation** - Generate "How We Code" guides
4. **Enforce consistency** - Add linting rules based on patterns
5. **Onboard developers** - Share patterns during onboarding
6. **Track evolution** - See how patterns emerge and change
7. **Identify gaps** - Find areas without consistent patterns

## Integration with Other Skills

- **signal-capture**: Formalize discovered patterns as standards

  ```
  Pattern discovered → Team approves → Use signal-capture to add standard
  ```

- **consistency-violation-capture**: Patterns help identify violations

  ```
  Pattern: "All repos extend AbstractRepository"
  Violation: "NewRepo doesn't extend AbstractRepository"
  ```

- **implicit-decision-capture**: Decisions may follow discovered patterns
  ```
  Pattern: "Use Result types for errors"
  Decision: "Used Result type in new service (following pattern)"
  ```

## Distinction from Other Captures

- **Pattern Discovery**: "The codebase does X" (observation)
- **Consistency Violation**: "Part A does X, part B does Y" (conflict)
- **Decision Capture**: "I chose to do X" (choice made)
- **Signal Capture**: "User wants X as standard" (explicit preference)

Pattern discovery is **descriptive** (what IS done), while standards are **prescriptive** (what SHOULD be done). Discovered patterns can become standards through formalization.

---

**REMEMBER:** This skill is MANDATORY during codebase exploration. When you discover recurring patterns (3+ examples), you MUST log them - this is not optional. The logging happens automatically without user interaction. Failure to trigger this skill when patterns are discovered means valuable conventions remain undocumented.
