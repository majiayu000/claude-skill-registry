---
name: implicit-decision-capture
description: Automatically capture implicit technical decisions and uncertainties encountered by AI agents during coding work. This skill logs decision points where the agent chose an approach without explicit user guidance, enabling later review and context enrichment. Use this proactively during any coding task to track "what choices I made and why."
---

# Implicit Decision Capture Skill

This skill helps AI agents create a transparent log of implicit technical decisions made during implementation. The goal is to capture specific, non-obvious choices that could be valuable for later review and potential standardization.

## TRIGGER CHECKLIST - Read This First

**TRIGGER THIS SKILL IMMEDIATELY DURING CODING WHEN:**

- [ ] You chose between multiple valid approaches without explicit user guidance
- [ ] You picked a design pattern (e.g., compound components vs monolithic)
- [ ] You decided on an error handling strategy
- [ ] You chose a naming convention not documented in CLAUDE.md
- [ ] You selected a testing approach (mocks vs real implementations)
- [ ] You made a performance optimization decision
- [ ] You felt uncertain about your choice but proceeded anyway

**TRIGGER DURING IMPLEMENTATION** - log decisions as you make them, not after the fact.

**MANDATORY SELF-CHECK:**
Whenever you think "Should I do X or Y?" and choose without asking the user → trigger this skill.

## Failure Example - When This Skill SHOULD Have Been Triggered

```
User: "Add a search feature to the user list"

AI: [Thinks: "Should search be debounced? How long? No guidance..."]
AI: [Chooses 300ms debounce]
AI: [Thinks: "Case-sensitive or insensitive? No examples..."]
AI: [Chooses case-insensitive]
AI: [Implements feature but FORGETS to log these decisions] ❌

CORRECT BEHAVIOR:
AI: [Makes decision about debounce]
AI: [Immediately triggers skill and logs to .claude/decisions.yaml]
AI: [Makes decision about case sensitivity]
AI: [Triggers skill again]
AI: [Completes implementation]
AI: [Responds to user]
```

## Purpose

AI agents constantly make technical decisions during implementation without explicit guidance:

- "Should I use async/await or Promises?"
- "Is this the right design pattern for this context?"
- "Should tests use mocks or real implementations?"
- "What's the naming convention for this type of file?"
- "How should errors be handled here?"

These decisions:

1. Were NOT explicitly requested by the user
2. Were NOT documented in CLAUDE.md or standards
3. Reflect specific architectural/design choices
4. Could become patterns worth standardizing

By capturing them, developers can:

1. **Review what assumptions were made** during implementation
2. **Validate AI decisions** and provide feedback
3. **Identify candidates for standards** that should be formalized
4. **Understand the rationale** behind implementation choices
5. **Improve future AI agent performance** with better context

## When to Use This Skill

Use this skill **proactively and silently** during any coding work when you (the AI agent):

1. **Make a design decision** without explicit guidance
   - Choose between multiple valid approaches
   - Pick a pattern or architecture
   - Decide on naming conventions
   - Select a library or tool

2. **Encounter ambiguity** in requirements
   - User's instructions could be interpreted multiple ways
   - Best practices are unclear for this context
   - No existing examples to follow

3. **Apply implicit knowledge** from general training
   - Use "common practices" that may not match this codebase
   - Make assumptions about code style
   - Infer patterns from limited examples

4. **Feel uncertain** about your choice
   - Low confidence in the approach
   - Multiple alternatives seem equally valid
   - Unusual or edge case scenario

5. **Choose implementation strategies**
   - Error handling approach
   - Validation logic placement
   - Caching strategies
   - Performance optimizations

6. **Decide on code organization**
   - File/folder structure decisions
   - Naming conventions not documented
   - Import/export patterns

## When NOT to Use

Don't capture:

- **Trivial syntax choices** (const vs let, quote style)
- **Standard language/framework conventions** (React hooks basics, TypeScript standard patterns)
- **User-specified requirements** (user explicitly asked for this approach)
- **Documented patterns** (already in CLAUDE.md or .packmind/standards)
- **Generic best practices** ("write clean code" - too vague)
- **Obvious only-choice decisions** (using the only available library)

## Workflow

### Step 1: Silent Capture (During Work)

When you make a decision during coding, **silently** append it to `.claude/decisions.yaml` without interrupting the user or your workflow:

```yaml
- timestamp: 2026-01-09T10:30:00Z
  file: src/components/UserProfile.tsx
  context: 'Implementing user profile component'
  category: 'architecture' # architecture|patterns|naming|testing|error-handling|performance|security|styling|dependencies
  question: 'Should the component fetch its own data or receive it via props?' # Optional: the uncertainty you had
  decision: 'Use compound component pattern with Profile.Header, Profile.Content, Profile.Actions'
  reasoning: 'Provides composition flexibility while maintaining encapsulation. Follows Chakra UI pattern seen in codebase.'
  alternatives:
    - 'Single monolithic component with section props'
    - 'Separate independent components'
  impact: 'module' # local|module|global
  confidence: 'medium' # low|medium|high
  source: 'pattern-matching' # ai-agent|inference|pattern-matching
  tags:
    - 'react'
    - 'component-architecture'
    - 'compound-components'
```

### Step 2: File Management

**Location:** Always use `.claude/decisions.yaml` at the repository root.

**Structure:** Array of decision entries, most recent last.

**Format Rules:**

- `timestamp`: ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)
- `file`: Relative path from repo root where decision was applied
- `context`: Brief description of what you were implementing
- `category`: One of: architecture, patterns, naming, testing, error-handling, performance, security, styling, dependencies
- `question`: (Optional) The question/uncertainty you had before deciding
- `decision`: The technical decision made (verb-first, imperative like "Use X pattern", "Structure Y as Z")
- `reasoning`: Why you chose this approach (reference similar patterns if found)
- `alternatives`: List of other valid options you considered
- `impact`: Scope of the decision
  - `local`: Affects only this file/component
  - `module`: Could affect this package/folder
  - `global`: Could be project-wide pattern
- `confidence`: low (uncertain, needs review) | medium (reasonable choice) | high (confident but worth documenting)
- `source`: How you arrived at this decision
  - `ai-agent`: Based on your general AI knowledge
  - `inference`: Inferred from codebase patterns
  - `pattern-matching`: Following similar code you found
- `tags`: Relevant keywords for filtering/searching

**IMPORTANT:** This is an automatic, non-interrupting operation:

- Do NOT ask the user for permission to log
- Do NOT announce that you logged something
- Simply log and continue your work seamlessly
- The user can review `.claude/decisions.yaml` later

This skill is MANDATORY during coding work - it's not optional.

### Step 3: User Review (Later)

Users can review `.claude/decisions.yaml` at any time to:

- Understand what decisions were made and why
- Identify patterns in uncertainties
- Create explicit guidelines in CLAUDE.md
- Add standards to Packmind
- Validate or question specific decisions

## Example Scenarios

### Example 1: Component Architecture

```yaml
- timestamp: 2026-01-09T09:15:00Z
  file: src/features/dashboard/Dashboard.tsx
  context: 'Creating dashboard feature with multiple widgets'
  category: 'architecture'
  question: 'Should the dashboard component handle data fetching or just presentation?'
  decision: 'Use container/presenter pattern with DashboardContainer fetching data and Dashboard handling presentation'
  reasoning: 'Separates data fetching concerns from UI logic. Saw this pattern in features/analytics folder.'
  alternatives:
    - 'All-in-one component with hooks'
    - 'Use React Query in presentational component'
  impact: 'module'
  confidence: 'high'
  source: 'inference'
  tags:
    - 'react'
    - 'container-presenter'
    - 'separation-of-concerns'
```

### Example 2: Testing Approach

```yaml
- timestamp: 2026-01-09T14:22:00Z
  file: src/services/auth.spec.ts
  context: 'Writing unit tests for authentication service'
  category: 'testing'
  question: 'Should I mock the database or use an in-memory test database?'
  decision: 'Use mocks for the database layer'
  reasoning: 'Tests run faster with mocks and other test files in the codebase use this approach'
  alternatives:
    - 'Use in-memory SQLite for integration testing'
    - 'Use test containers with real database'
  impact: 'module'
  confidence: 'medium'
  source: 'pattern-matching'
  tags:
    - 'testing'
    - 'mocking'
    - 'database'
```

### Example 3: Error Handling Strategy

```yaml
- timestamp: 2026-01-09T10:45:00Z
  file: src/services/payment/PaymentService.ts
  context: 'Implementing payment processing service'
  category: 'error-handling'
  question: 'Should API errors throw exceptions or return Result<T, Error> types?'
  decision: 'Use Result<T, E> type instead of throwing exceptions for expected errors (insufficient funds, invalid card)'
  reasoning: 'Makes error handling explicit and type-safe. Allows callers to handle errors functionally without try-catch.'
  alternatives:
    - 'Throw custom exception classes'
    - 'Return null with separate error channel'
  impact: 'global'
  confidence: 'medium'
  source: 'ai-agent'
  tags:
    - 'error-handling'
    - 'functional-programming'
    - 'type-safety'
```

### Example 4: Naming Convention

```yaml
- timestamp: 2026-01-09T16:10:00Z
  file: src/hooks/useUserData.ts
  context: 'Creating custom React hook for user data'
  category: 'naming'
  question: 'Should custom hooks be in /hooks or co-located with components?'
  decision: 'Place reusable hooks in /src/hooks/ directory'
  reasoning: 'Found other custom hooks in this directory'
  alternatives:
    - 'Co-locate with the component that uses it'
    - 'Create /src/lib/hooks for reusable hooks'
  impact: 'global'
  confidence: 'high'
  source: 'pattern-matching'
  tags:
    - 'react'
    - 'hooks'
    - 'project-structure'
```

### Example 5: Performance Optimization

```yaml
- timestamp: 2026-01-09T15:20:00Z
  file: src/components/DataTable.tsx
  context: 'Implementing large data table with pagination'
  category: 'performance'
  decision: 'Use React.memo with custom comparison function on table rows instead of virtualizing'
  reasoning: 'Table has max 50 rows per page, virtualization overhead not worth it. Memo prevents unnecessary row re-renders on pagination.'
  alternatives:
    - 'Virtual scrolling with react-window'
    - 'No optimization (let React handle it)'
  impact: 'local'
  confidence: 'high'
  source: 'ai-agent'
  tags:
    - 'performance'
    - 'react'
    - 'memoization'
```

### Example 6: Dependency Choice

```yaml
- timestamp: 2026-01-09T16:55:00Z
  file: src/utils/date.ts
  context: 'Adding date formatting utility'
  category: 'dependencies'
  question: 'Should I use date-fns, dayjs, or native Intl for date formatting?'
  decision: 'Use date-fns because it was already in package.json'
  reasoning: 'Avoiding adding new dependencies, date-fns already installed and tree-shakeable'
  alternatives:
    - 'Use dayjs (smaller bundle size)'
    - 'Use native Intl.DateTimeFormat (no dependencies)'
  impact: 'global'
  confidence: 'high'
  source: 'inference'
  tags:
    - 'dependencies'
    - 'date-formatting'
    - 'bundle-size'
```

## Integration Pattern

### During Normal Work

When implementing a feature:

1. Write code as normal
2. When you make a decision without explicit guidance, silently append to decisions.yaml
3. Continue working without interruption
4. Multiple decisions can be logged during a single task

### Example Flow

```
User: "Add a search feature to the user list"

[AI Agent thinking: "Should search be debounced? How long? No guidance provided..."]
[AI Agent silently logs to decisions.yaml with question + decision]
[AI Agent implements with 300ms debounce]

[AI Agent thinking: "Should search be case-sensitive? No examples to follow..."]
[AI Agent silently logs to decisions.yaml]
[AI Agent implements case-insensitive search]

AI Agent: "I've added the search feature with debounced input (300ms) and case-insensitive matching."
```

User sees the implementation but can later review decisions.yaml to see what decisions were made and why.

## Benefits

1. **Transparency**: Developers see the AI's decision-making process
2. **Pattern Discovery**: Reveals emerging patterns that should be standardized
3. **Context Improvement**: Identify gaps in project guidelines
4. **Quality Assurance**: Enables review of AI decisions before they become habits
5. **Standard Creation**: Provides source material for formalizing practices
6. **Trust Building**: Users understand what assumptions were made
7. **Continuous Improvement**: Feedback loop for improving AI coding decisions

## Important Guidelines

1. **Be specific**: Decisions should be concrete and actionable, not vague
2. **Be honest**: Log real decisions you made, not imagined ones
3. **Be selective**: Only log meaningful decisions, not trivial choices
4. **Be silent**: Never interrupt workflow with logging notifications
5. **Be contextual**: Include enough information to understand the situation later
6. **Reference patterns**: When you followed existing code, mention it
7. **Consider impact**: Tag global decisions for higher-priority review
8. **Track confidence**: Low-confidence decisions need review more urgently
9. **Source attribution**: Distinguish between your AI knowledge vs codebase patterns

## Decisions YAML Schema

```yaml
# .claude/decisions.yaml
- timestamp: string      # ISO 8601: "2026-01-09T10:30:00Z"
  file: string           # Relative path: "src/api/users.ts"
  context: string        # Brief: "Adding user authentication"
  category: string       # architecture|patterns|naming|testing|error-handling|performance|security|styling|dependencies
  question: string       # Optional: "Should validation be in middleware or controller?"
  decision: string       # Imperative: "Use factory pattern for object creation"
  reasoning: string      # Why: "Encapsulates creation logic, saw pattern in auth module"
  alternatives: array    # Other options considered
    - string
  impact: string         # local|module|global
  confidence: string     # low|medium|high
  source: string         # ai-agent|inference|pattern-matching
  tags: array            # Keywords for filtering
    - string
```

## Future Use

Once `.claude/decisions.yaml` accumulates entries, developers can:

1. **Review by impact** - Check global decisions first
2. **Review by confidence** - Validate low-confidence choices
3. **Identify patterns** - Group by category to see trends
4. **Create standards** - Use signal-capture to formalize good patterns
5. **Provide feedback** - Add clarifications to CLAUDE.md
6. **Audit consistency** - Ensure similar problems have similar solutions
7. **Onboard new AI contexts** - Show examples of past decisions

## Integration with Other Skills

- **signal-capture**: When user reviews decisions and wants to formalize a pattern

  ```
  User: "I like this compound component pattern, let's make it our standard"
  → Use signal-capture to add to standards
  ```

- **Standard creation**: Decisions file provides source material for new standards

---

**REMEMBER:** This skill is MANDATORY during ALL coding work. When you make technical decisions without explicit user guidance, you MUST log them - this is not optional. The logging happens automatically without user interaction. Every undocumented decision is an opportunity to improve project guidelines and maintain transparency.
