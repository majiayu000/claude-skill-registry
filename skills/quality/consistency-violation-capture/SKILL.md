---
name: consistency-violation-capture
description: Capture codebase inconsistencies discovered during exploration OR implementation. TRIGGER when you find conflicting patterns while looking for code to follow (e.g., "some UseCases extend AbstractMemberUseCase, others don't") or different approaches to the same concern across modules (naming, error handling, validation placement). Log silently to .claude/consistency-violations.yaml so teams can standardize later.
---

# Consistency Violation Capture Skill

This skill helps AI agents identify and log inconsistencies discovered while exploring or working in the codebase. The goal is to create a transparent log of places where the codebase lacks consistency, enabling teams to standardize approaches over time.

## TRIGGER CHECKLIST - Read This First

**TRIGGER THIS SKILL IMMEDIATELY WHEN:**

### During Exploration

- [ ] You explored code across 2+ modules/packages and found different approaches to the same concern
- [ ] You noticed naming conventions differ between files (e.g., `IFoo` vs `Foo` for interfaces)
- [ ] You found different error handling patterns (exceptions vs Result types)
- [ ] You discovered mixed async patterns (Promises vs async/await)
- [ ] You saw inconsistent API response structures
- [ ] You found varying test organization approaches
- [ ] You noticed different folder structures for similar modules

### During Implementation (e.g., "Add a UseCase", "Create a new endpoint")

- [ ] You looked for similar implementations to follow as a template and found **conflicting patterns**
- [ ] You tried to extend/inherit from a base class but found that similar code doesn't follow this pattern
- [ ] You discovered that event emission/handling varies (some use cases emit events, others don't)
- [ ] You found that validation is placed differently (controller vs use case vs domain entity)
- [ ] You noticed dependency injection patterns vary (constructor vs method injection)
- [ ] You found mixed approaches to repository methods (findById vs getById, returning null vs throwing)

**TRIGGER AS SOON AS YOU NOTICE** - don't wait until the end of your response. Log immediately, then continue your work.

**MANDATORY CHECKS:**

- **Post-Exploration:** After ANY codebase exploration task, ask yourself: "Did I find any inconsistencies?" If yes → trigger this skill.
- **Pre-Implementation:** Before implementing, when looking for patterns to follow: "Are there conflicting approaches?" If yes → trigger this skill.
- **During Implementation:** While coding: "Does my approach match what I see elsewhere?" If not → investigate and potentially trigger this skill.

## Failure Examples - When This Skill SHOULD Have Been Triggered

### Failure Example 1: During Exploration

```
User: "Analyze event tracking in the standards package"

AI: [Explores packages/standards and packages/llm]
AI: [Finds that standards package emits events but LLM package doesn't]
AI: [Finds that some use cases extend AbstractMemberUseCase, others don't]
AI: [Responds with analysis but FORGETS to trigger this skill] ❌

CORRECT BEHAVIOR:
AI: [Notices inconsistency] → [Immediately triggers skill and logs to .claude/consistency-violations.yaml]
AI: [Continues exploration]
AI: [Notices another inconsistency] → [Immediately triggers skill again]
AI: [Responds to user with analysis]
```

### Failure Example 2: During Implementation (Common!)

```
User: "Add a new UseCase to edit a standard"

AI: [Explores existing UseCases to find a pattern to follow]
AI: [Finds EditStandardNameUseCase extends AbstractMemberUseCase]
AI: [Finds CreateStandardUseCase does NOT extend AbstractMemberUseCase]
AI: [Picks one pattern and implements but FORGETS to log the inconsistency] ❌

CORRECT BEHAVIOR:
AI: [Discovers conflicting patterns while looking for template]
AI: [Immediately triggers skill: "UseCase inheritance varies - some extend AbstractMemberUseCase, some don't"]
AI: [Continues with implementation, following one pattern]
AI: [Responds to user with the implementation]
```

### Failure Example 3: During Code Review/Understanding

```
User: "Help me understand how validation works in this codebase"

AI: [Explores API controllers - finds validation in controllers]
AI: [Explores domain layer - finds validation in entities]
AI: [Explores use cases - finds validation there too]
AI: [Explains validation but FORGETS to log the inconsistency] ❌

CORRECT BEHAVIOR:
AI: [Notices validation is scattered across layers]
AI: [Triggers skill: "Validation placement inconsistent - found in controllers, use cases, and entities"]
AI: [Responds to user with explanation AND the team can later review the logged inconsistency]
```

## Purpose

AI agents often discover inconsistencies during exploration:

- "Module A uses async/await, Module B uses Promises for the same pattern"
- "Some files prefix interfaces with 'I', others don't"
- "Error handling uses exceptions in services but Result types in domain"
- "Some tests use factories, others create inline test data"
- "Date formatting differs between components"
- "API responses have inconsistent structures across endpoints"

These inconsistencies:

1. Make the codebase **harder to understand** for new developers
2. Create **cognitive load** when switching between areas
3. Indicate **missing standards** that should be documented
4. Can lead to **bugs** when developers follow the wrong pattern
5. Represent **technical debt** that accumulates over time

By capturing them, developers can:

1. **Prioritize standardization** efforts based on impact
2. **Create new standards** to prevent future inconsistencies
3. **Plan refactoring** sessions to unify approaches
4. **Document decisions** about which pattern to prefer
5. **Track progress** toward codebase consistency

## When to Use This Skill

Use this skill **proactively and silently** during any codebase exploration or coding work when you notice:

1. **Naming Inconsistencies**
   - Interface naming (IFoo vs Foo)
   - File naming conventions (kebab-case vs camelCase)
   - Variable naming patterns (userID vs userId)
   - Test file naming (.spec.ts vs .test.ts)

2. **Pattern Inconsistencies**
   - Different error handling approaches
   - Mixed async patterns (Promises vs async/await)
   - Varying component structures
   - Inconsistent API response formats

3. **Structural Inconsistencies**
   - Different folder organizations for similar modules
   - Inconsistent layering (some use repository, some don't)
   - Mixed import styles (relative vs absolute)
   - Varying test organization

4. **Style Inconsistencies**
   - Mixed formatting within similar code
   - Inconsistent comment styles
   - Different logging approaches
   - Varying configuration patterns

5. **Architectural Inconsistencies**
   - Some modules follow hexagonal, others don't
   - Inconsistent dependency injection usage
   - Mixed state management approaches
   - Varying validation placement

## When NOT to Use

Don't capture:

- **Intentional differences** - Some variation is by design (e.g., different domains)
- **Legacy code in migration** - Already planned for standardization
- **External dependencies** - Third-party code styles
- **Single occurrences** - Need at least 2 conflicting examples
- **Trivial variations** - Minor differences that don't impact understanding

## Workflow

### Step 1: Discover Inconsistency (During Work)

While exploring or coding, notice when different parts of the codebase handle similar concerns differently.

### Step 2: Silent Logging

**Silently** append the inconsistency to `.claude/consistency-violations.yaml`:

```yaml
- timestamp: 2026-01-09T10:30:00Z
  category: 'naming' # naming|patterns|structure|style|architecture|testing|error-handling|api
  description: 'Interface naming convention is inconsistent across packages'
  examples:
    - file: src/domain/user/IUserRepository.ts
      pattern: 'Prefix interfaces with I'
      context: 'Domain layer uses I prefix'
    - file: src/services/auth/AuthService.ts
      pattern: 'No prefix on interfaces'
      context: 'Service layer interfaces have no prefix'
  impact: 'medium' # low|medium|high
  scope: 'global' # local|module|global
  recommendation: 'Standardize on I prefix for interfaces as documented in CLAUDE.md'
  related_standard: 'typescript-code-standards' # optional: existing standard this violates
  tags:
    - 'typescript'
    - 'interfaces'
    - 'naming-conventions'
```

### Step 3: File Management

**Location:** Always use `.claude/consistency-violations.yaml` at the repository root.

**Structure:** Array of violation entries, most recent last.

**Format Rules:**

- `timestamp`: ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)
- `category`: One of: naming, patterns, structure, style, architecture, testing, error-handling, api
- `description`: Clear summary of what is inconsistent
- `examples`: At least 2 concrete examples showing the conflict
  - `file`: Relative path from repo root
  - `pattern`: What pattern this file follows
  - `context`: Brief explanation
- `impact`: How much this affects development
  - `low`: Minor inconvenience
  - `medium`: Causes confusion, occasional bugs
  - `high`: Significant confusion, frequent issues
- `scope`: How widespread the inconsistency is
  - `local`: Within a single module
  - `module`: Across a few related modules
  - `global`: Throughout the codebase
- `recommendation`: Suggested approach to standardize (which pattern to prefer)
- `related_standard`: If there's an existing standard being violated (optional)
- `tags`: Relevant keywords for filtering/searching

**IMPORTANT:** This is an automatic, non-interrupting operation:

- Do NOT ask the user for permission to log
- Do NOT announce that you logged something
- Simply log and continue your work seamlessly
- The user can review `.claude/consistency-violations.yaml` later

This skill is MANDATORY when inconsistencies are found - it's not optional.

### Step 4: User Review (Later)

Users can review `.claude/consistency-violations.yaml` at any time to:

- Understand where the codebase lacks consistency
- Prioritize which inconsistencies to address first
- Create new standards to prevent future occurrences
- Plan refactoring sessions
- Make decisions about which pattern to adopt

## Example Scenarios

### Example 1: Error Handling Inconsistency

```yaml
- timestamp: 2026-01-09T09:15:00Z
  category: 'error-handling'
  description: 'Error handling approach differs between service and domain layers'
  examples:
    - file: src/services/payment/PaymentService.ts
      pattern: 'Throws exceptions for error cases'
      context: 'Service layer uses try/catch with thrown errors'
    - file: src/domain/order/OrderProcessor.ts
      pattern: 'Returns Result<T, Error> type'
      context: 'Domain layer uses functional error handling'
  impact: 'high'
  scope: 'global'
  recommendation: 'Standardize on Result types for domain, exceptions for infrastructure boundaries'
  related_standard: null
  tags:
    - 'error-handling'
    - 'domain-driven-design'
    - 'functional-programming'
```

### Example 2: Test Organization Inconsistency

```yaml
- timestamp: 2026-01-09T10:45:00Z
  category: 'testing'
  description: 'Test data creation approach varies across test files'
  examples:
    - file: src/domain/user/__tests__/User.spec.ts
      pattern: 'Uses factory functions from __fixtures__'
      context: 'Creates test users with createTestUser()'
    - file: src/services/auth/__tests__/AuthService.spec.ts
      pattern: 'Inline object literals'
      context: 'Defines test data directly in each test'
    - file: src/api/users/__tests__/UsersController.spec.ts
      pattern: 'Uses builder pattern'
      context: 'Creates test data with UserBuilder.create().withEmail().build()'
  impact: 'medium'
  scope: 'global'
  recommendation: 'Adopt factory functions pattern consistently as it balances readability and reusability'
  related_standard: 'testing-good-practices'
  tags:
    - 'testing'
    - 'test-data'
    - 'fixtures'
    - 'consistency'
```

### Example 3: API Response Structure Inconsistency

```yaml
- timestamp: 2026-01-09T11:30:00Z
  category: 'api'
  description: 'API response envelope structure varies between endpoints'
  examples:
    - file: src/api/users/users.controller.ts
      pattern: '{ data: T, meta: { total, page } }'
      context: 'User endpoints wrap response in data with pagination meta'
    - file: src/api/products/products.controller.ts
      pattern: '{ items: T[], pagination: { ... } }'
      context: 'Product endpoints use items array with separate pagination object'
    - file: src/api/orders/orders.controller.ts
      pattern: 'Returns array directly'
      context: 'Order endpoints return raw arrays without envelope'
  impact: 'high'
  scope: 'global'
  recommendation: 'Standardize on { data, meta } envelope for all list endpoints'
  related_standard: null
  tags:
    - 'api'
    - 'rest'
    - 'response-format'
    - 'pagination'
```

### Example 4: Import Style Inconsistency

```yaml
- timestamp: 2026-01-09T14:00:00Z
  category: 'structure'
  description: 'Import path styles vary across the codebase'
  examples:
    - file: src/features/dashboard/Dashboard.tsx
      pattern: 'Absolute imports with @/ alias'
      context: 'Uses @/components/Button'
    - file: src/features/settings/Settings.tsx
      pattern: 'Relative imports'
      context: 'Uses ../../components/Button'
    - file: src/features/auth/Login.tsx
      pattern: 'Mixed styles'
      context: 'Some imports absolute, some relative in same file'
  impact: 'low'
  scope: 'global'
  recommendation: 'Use absolute imports with @ alias for cross-feature imports, relative for same-folder'
  related_standard: null
  tags:
    - 'imports'
    - 'project-structure'
    - 'typescript'
```

### Example 5: Naming Convention Inconsistency

```yaml
- timestamp: 2026-01-09T15:20:00Z
  category: 'naming'
  description: 'Repository method naming varies across domain modules'
  examples:
    - file: src/domain/user/UserRepository.ts
      pattern: 'find* prefix (findById, findByEmail)'
      context: 'User repository uses find prefix'
    - file: src/domain/order/OrderRepository.ts
      pattern: 'get* prefix (getById, getByUserId)'
      context: 'Order repository uses get prefix'
    - file: src/domain/product/ProductRepository.ts
      pattern: 'Mixed (findById, getByCategory)'
      context: 'Product repository mixes both styles'
  impact: 'medium'
  scope: 'global'
  recommendation: 'Standardize on find* prefix for queries that may return null, get* for queries that throw'
  related_standard: null
  tags:
    - 'naming'
    - 'repository-pattern'
    - 'domain-driven-design'
```

### Example 6: Configuration Loading Inconsistency

```yaml
- timestamp: 2026-01-09T16:10:00Z
  category: 'patterns'
  description: 'Configuration loading approach differs between modules'
  examples:
    - file: src/services/database/DatabaseService.ts
      pattern: 'Reads from process.env directly'
      context: 'Accesses process.env.DATABASE_URL inline'
    - file: src/services/email/EmailService.ts
      pattern: 'Uses ConfigService injection'
      context: 'Receives config through constructor DI'
    - file: src/services/cache/CacheService.ts
      pattern: 'Loads from config file'
      context: 'Reads from config/cache.json at startup'
  impact: 'medium'
  scope: 'global'
  recommendation: 'Use ConfigService injection consistently for testability and centralized config management'
  related_standard: null
  tags:
    - 'configuration'
    - 'dependency-injection'
    - 'environment-variables'
```

## Integration Pattern

### During Exploration

While exploring the codebase:

1. Read files to understand patterns
2. Notice when similar concerns are handled differently
3. Silently log inconsistencies with concrete examples
4. Continue exploration without interruption

### During Implementation

While implementing features:

1. Follow existing patterns in the area you're working
2. Notice when your approach differs from other areas
3. Log the inconsistency if it represents a real conflict
4. Continue implementation without blocking

### Example Flow

```
User: "Help me understand how error handling works in this codebase"

[AI explores src/services/ - sees thrown exceptions]
[AI explores src/domain/ - sees Result types]
[AI thinking: "Inconsistency - two different error handling patterns"]

[AI silently logs to .claude/consistency-violations.yaml]

AI: "I found two error handling approaches in the codebase:
     - Service layer uses thrown exceptions
     - Domain layer uses Result<T, E> types

     This creates inconsistency when domain errors need to propagate..."
```

User sees the analysis. Later, they can review consistency-violations.yaml to understand the full picture.

## Benefits

1. **Visibility**: Teams see where their codebase lacks consistency
2. **Prioritization**: Impact and scope help decide what to fix first
3. **Standard Creation**: Violations often reveal need for new standards
4. **Technical Debt Tracking**: Quantifies inconsistency as technical debt
5. **Onboarding**: New developers understand why things vary
6. **Refactoring Planning**: Provides concrete targets for cleanup sprints

## Important Guidelines

1. **Be specific**: Include concrete file examples, not vague claims
2. **Be balanced**: Include at least 2 conflicting examples
3. **Be constructive**: Always suggest which pattern to prefer
4. **Be silent**: Never interrupt workflow with logging notifications
5. **Be practical**: Focus on inconsistencies that actually impact work
6. **Consider scope**: Global issues are usually higher priority
7. **Link standards**: Reference existing standards if being violated
8. **Assess impact**: High-impact issues deserve earlier attention

## Consistency Violations YAML Schema

```yaml
# .claude/consistency-violations.yaml
- timestamp: string       # ISO 8601: "2026-01-09T10:30:00Z"
  category: string        # naming|patterns|structure|style|architecture|testing|error-handling|api
  description: string     # Clear summary of the inconsistency
  examples: array         # At least 2 examples showing conflict
    - file: string       # Relative path: "src/api/users.ts"
      pattern: string    # What pattern this file follows
      context: string    # Brief explanation
  impact: string         # low|medium|high
  scope: string          # local|module|global
  recommendation: string # Suggested standardization approach
  related_standard: string | null  # Existing standard being violated (optional)
  tags: array           # Keywords
    - string            # "naming", "error-handling", etc.
```

## Future Use

Once `.claude/consistency-violations.yaml` accumulates entries, developers can:

1. **Review by impact** - Fix high-impact inconsistencies first
2. **Review by scope** - Global issues affect more developers
3. **Create standards** - Use signal-capture to formalize chosen patterns
4. **Plan refactoring** - Group related violations into refactoring tasks
5. **Track progress** - Remove violations as they get standardized
6. **Measure tech debt** - Count/weight violations as debt metric
7. **Onboard developers** - Show where to expect variation

## Integration with Other Skills

- **signal-capture**: When team decides which pattern to standardize

  ```
  Consistency violation identified → Team picks preferred pattern → Use signal-capture to add standard
  ```

- **implicit-decision-capture**: When making a choice in inconsistent area
  ```
  AI must pick one pattern → Log implicit-decision-capture for the choice made
  Inconsistency causes uncertainty → Log the decision with the question field
  ```

---

**REMEMBER:** This skill is MANDATORY during codebase exploration. When you find inconsistencies, you MUST log them - this is not optional. The logging happens automatically without user interaction. Failure to trigger this skill when inconsistencies are discovered is a missed opportunity for improving codebase quality.
