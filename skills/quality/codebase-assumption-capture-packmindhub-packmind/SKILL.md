---
name: codebase-assumption-capture
description: Capture wrong assumptions you made about the codebase. TRIGGER when reality differs from expectation (e.g., "assumed Jest but it's Vitest", "assumed AbstractUseCase exists but found AbstractMemberUseCase", "assumed REST but it's GraphQL"). Log silently to .claude/assumption-corrections.yaml to identify CLAUDE.md documentation gaps. Key distinction - assumptions are corrected by reality, decisions are choices between valid options.
---

# Codebase Assumption Capture Skill

This skill helps AI agents track assumptions they made about the codebase that turned out to be incorrect. The goal is to identify documentation gaps and create better onboarding context for future AI agent sessions.

## TRIGGER CHECKLIST - Read This First

**TRIGGER THIS SKILL IMMEDIATELY WHEN:**

### Pre-Work Assumptions (before you start coding)

- [ ] You assumed a framework/library was used but found a different one (e.g., assumed Jest, found Vitest)
- [ ] You assumed an architectural pattern but discovered a different one (e.g., assumed MVC, found hexagonal)
- [ ] You assumed a file/folder was the entry point but it wasn't
- [ ] You assumed a naming convention but found the opposite
- [ ] You found something non-obvious that CLAUDE.md should mention

### During Implementation (when starting to code)

- [ ] You started implementing with a wrong assumption and had to change approach
- [ ] You assumed you'd find a pattern/template to follow but it doesn't exist
- [ ] You assumed certain helpers/utils existed but they don't (or they work differently)
- [ ] You assumed the testing setup works a certain way but it doesn't
- [ ] You thought a base class/interface existed but had to create it yourself
- [ ] You assumed DI/IoC container works a certain way but discovered it's different

### Post-Implementation Realizations

- [ ] You had to backtrack after discovering your initial assumption was wrong
- [ ] Tests failed because your assumption about dependencies was wrong
- [ ] Build/lint failed because of an undocumented rule you didn't know about

**TRIGGER THE MOMENT YOU REALIZE YOU WERE WRONG** - don't wait. Log immediately, then continue with the corrected understanding.

**MANDATORY SELF-CHECK:**
Whenever you realize "I assumed X, but it's actually Y" → trigger this skill.

**KEY DISTINCTION FROM implicit-decision-capture:**

- **Assumption**: "I thought/expected X" → Reality proved me wrong → Log as assumption
- **Decision**: "I chose X over Y" → Both were valid options → Log as decision
- If you **had no choice** because reality was different from expectation → that's an assumption
- If you **made a choice** between valid alternatives → that's a decision

## Failure Examples - When This Skill SHOULD Have Been Triggered

### Failure Example 1: During Exploration (Classic)

```
User: "Add a new API endpoint"

AI: [Thinks: "Based on Express in dependencies, I'll create a REST endpoint"]
AI: [Explores src/api/ and finds GraphQL resolvers]
AI: [Thinks: "Oh, it's GraphQL, not REST"]
AI: [Implements GraphQL resolver but FORGETS to log the wrong assumption] ❌

CORRECT BEHAVIOR:
AI: [Realizes assumption was wrong]
AI: [Immediately triggers skill and logs to .claude/assumption-corrections.yaml]
AI: [Continues with corrected approach]
AI: [Responds to user]
```

### Failure Example 2: During Implementation (Common!)

```
User: "Add a new UseCase to edit a standard"

AI: [Thinks: "UseCases probably follow a base class pattern like in most clean architecture codebases"]
AI: [Creates EditStandardUseCase extending a presumed AbstractUseCase]
AI: [Finds that AbstractUseCase doesn't exist - it's AbstractMemberUseCase with different requirements]
AI: [Adapts the code but FORGETS to log the wrong assumption] ❌

CORRECT BEHAVIOR:
AI: [Discovers base class is different than expected]
AI: [Triggers skill: "Assumed generic AbstractUseCase exists, but found AbstractMemberUseCase with member-scoping"]
AI: [Adjusts implementation to use correct base class]
AI: [Responds to user with correct implementation]
```

### Failure Example 3: Build/Test Failure Reveals Assumption

```
User: "Add unit tests for this service"

AI: [Thinks: "I'll use Jest mocking patterns like jest.mock()"]
AI: [Writes tests with Jest patterns]
AI: [Tests fail because project uses Vitest with different mocking API]
AI: [Fixes tests but FORGETS to log the assumption] ❌

CORRECT BEHAVIOR:
AI: [Test failure reveals testing framework assumption was wrong]
AI: [Triggers skill: "Assumed Jest testing framework, but project uses Vitest"]
AI: [Rewrites tests with Vitest patterns]
AI: [Responds with working tests]
```

### Failure Example 4: Helper/Util Assumption

```
User: "Add date formatting to the response"

AI: [Thinks: "There's probably a date formatting util in this codebase"]
AI: [Searches for formatDate or date utils]
AI: [Finds nothing - project uses raw Intl.DateTimeFormat everywhere]
AI: [Implements without util but FORGETS to log the assumption] ❌

CORRECT BEHAVIOR:
AI: [Realizes expected utility doesn't exist]
AI: [Triggers skill: "Assumed centralized date formatting utility exists, but found raw Intl.DateTimeFormat used directly"]
AI: [Suggests adding documentation about date handling approach OR follows existing pattern]
AI: [Responds to user]
```

## Purpose

AI agents make assumptions when starting work on a codebase:

- "I assumed this was a REST API, but it uses GraphQL"
- "I assumed tests used Jest, but they use Vitest"
- "I assumed auth was JWT-based, but it's session-based"
- "I assumed the ORM was Prisma, but it's TypeORM"
- "I assumed this followed MVC, but it's hexagonal architecture"
- "I assumed this file was the entry point, but it wasn't"

These incorrect assumptions:

1. **Waste time** when the AI goes down the wrong path
2. **Reveal documentation gaps** that hurt onboarding
3. **Show what's non-obvious** about the codebase
4. **Help improve CLAUDE.md** with better context
5. **Identify confusing patterns** that should be clarified

By capturing them, developers can:

1. **Improve documentation** in CLAUDE.md and README
2. **Add clarifying comments** to confusing areas
3. **Understand onboarding friction** for new developers
4. **Rename or restructure** confusing code
5. **Provide better context** for future AI sessions

## When to Use This Skill

Use this skill **proactively and silently** when you (the AI agent):

1. **Discover You Were Wrong**
   - Initially assumed X, but exploration revealed Y
   - Started implementing with wrong assumption
   - Had to backtrack after discovering truth
   - Realized a pattern wasn't what it seemed

2. **Find Unexpected Architecture**
   - Framework or library different than expected
   - Architectural pattern different than assumed
   - File structure doesn't match conventions
   - Naming suggests something it isn't

3. **Encounter Misleading Names/Structures**
   - File named X but does Y
   - Folder structure implies wrong organization
   - Variable/function name suggests wrong behavior
   - Module appears to be something it isn't

4. **Realize Context Was Missing**
   - Important information not in CLAUDE.md
   - Key architectural decision not documented
   - Non-obvious pattern not explained
   - Custom conventions not described

## When NOT to Use

Don't capture:

- **Correct assumptions** - Only log when you were WRONG
- **Trivial misunderstandings** - Minor things that don't impact work
- **User error** - When user gave misleading instructions
- **Obvious exploration** - Normal discovery process without assumption
- **External confusion** - Third-party library confusion

## Workflow

### Step 1: Realize Assumption Was Wrong

During exploration or implementation, notice when your initial assumption about the codebase was incorrect.

### Step 2: Silent Logging

**Silently** append the assumption to `.claude/assumption-corrections.yaml`:

```yaml
- timestamp: 2026-01-09T10:30:00Z
  category: 'architecture' # architecture|framework|testing|patterns|naming|structure|configuration|dependencies
  assumption: 'Assumed the API uses REST with Express based on package.json having express dependency'
  reality: 'API uses GraphQL with Apollo Server - Express is only used as middleware host'
  discovery_point: 'Found schema.graphql and resolvers folder while exploring src/'
  impact: 'high' # low|medium|high - how much time/effort was wasted
  misleading_signals:
    - 'Express listed in dependencies'
    - 'src/api folder exists (but contains GraphQL resolvers)'
  documentation_gap: 'CLAUDE.md should mention GraphQL architecture upfront'
  files_explored:
    - src/api/
    - src/schema.graphql
    - package.json
  tags:
    - 'graphql'
    - 'api-architecture'
    - 'express'
```

### Step 3: File Management

**Location:** Always use `.claude/assumption-corrections.yaml` at the repository root.

**Structure:** Array of assumption entries, most recent last.

**Format Rules:**

- `timestamp`: ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)
- `category`: One of: architecture, framework, testing, patterns, naming, structure, configuration, dependencies
- `assumption`: What you initially assumed and why
- `reality`: What turned out to be true
- `discovery_point`: How/when you discovered the truth
- `impact`: How much this incorrect assumption affected your work
  - `low`: Quick correction, minimal wasted effort
  - `medium`: Some backtracking needed, moderate confusion
  - `high`: Significant time wasted, major reorientation needed
- `misleading_signals`: What led you to the wrong assumption (list)
- `documentation_gap`: What should be documented to prevent this
- `files_explored`: Files that helped reveal the truth
- `tags`: Relevant keywords for filtering/searching

**IMPORTANT:** This is an automatic, non-interrupting operation:

- Do NOT ask the user for permission to log
- Do NOT announce that you logged something
- Simply log and continue your work seamlessly
- The user can review `.claude/assumption-corrections.yaml` later

This skill is MANDATORY when you realize an assumption was wrong - it's not optional.

### Step 4: User Review (Later)

Users can review `.claude/assumption-corrections.yaml` at any time to:

- Understand what's confusing about their codebase
- Improve CLAUDE.md with better context
- Identify misleading names or structures to refactor
- See common onboarding friction points
- Enhance documentation for humans too

## Example Scenarios

### Example 1: Framework Assumption

```yaml
- timestamp: 2026-01-09T09:15:00Z
  category: 'framework'
  assumption: 'Assumed this is a Next.js app based on pages/ folder structure'
  reality: 'This is a custom React app with file-based routing implemented manually'
  discovery_point: 'Found custom router implementation in src/lib/router.ts with no next.config.js'
  impact: 'medium'
  misleading_signals:
    - 'pages/ folder at root (Next.js convention)'
    - 'React listed in dependencies'
    - 'File naming follows Next.js patterns'
  documentation_gap: 'README or CLAUDE.md should clarify this is NOT Next.js despite similar structure'
  files_explored:
    - pages/
    - package.json
    - src/lib/router.ts
  tags:
    - 'react'
    - 'routing'
    - 'framework'
```

### Example 2: Testing Framework Assumption

```yaml
- timestamp: 2026-01-09T10:45:00Z
  category: 'testing'
  assumption: 'Assumed tests use Jest based on .spec.ts file naming convention'
  reality: 'Tests use Vitest - similar API but different configuration and runner'
  discovery_point: 'Found vitest.config.ts and vitest in devDependencies, no jest.config.js'
  impact: 'low'
  misleading_signals:
    - '.spec.ts files (common in both Jest and Vitest)'
    - 'describe/it/expect syntax (identical in both)'
  documentation_gap: 'CLAUDE.md testing section should specify Vitest, not assume Jest knowledge transfers'
  files_explored:
    - vitest.config.ts
    - package.json
    - src/**/*.spec.ts
  tags:
    - 'testing'
    - 'vitest'
    - 'jest'
```

### Example 3: Authentication Assumption

```yaml
- timestamp: 2026-01-09T11:30:00Z
  category: 'architecture'
  assumption: 'Assumed JWT-based authentication based on jsonwebtoken dependency'
  reality: 'Primary auth is session-based with cookies - JWT only used for email verification tokens'
  discovery_point: 'Found session middleware in src/middleware/auth.ts and cookie-session dependency'
  impact: 'high'
  misleading_signals:
    - 'jsonwebtoken in dependencies'
    - 'src/utils/jwt.ts exists'
    - 'Token mentioned in auth-related files'
  documentation_gap: 'CLAUDE.md should explicitly state session-based auth and clarify JWT is only for specific flows'
  files_explored:
    - src/middleware/auth.ts
    - src/utils/jwt.ts
    - package.json
  tags:
    - 'authentication'
    - 'jwt'
    - 'sessions'
    - 'security'
```

### Example 4: ORM Assumption

```yaml
- timestamp: 2026-01-09T14:00:00Z
  category: 'dependencies'
  assumption: 'Assumed Prisma ORM based on prisma/ folder in root'
  reality: 'Uses TypeORM - prisma folder contains unrelated data migration scripts'
  discovery_point: 'Found TypeORM entities in src/domain/ and ormconfig.ts at root'
  impact: 'medium'
  misleading_signals:
    - 'prisma/ folder at root'
    - 'Some files mention "schema" (Prisma terminology)'
  documentation_gap: 'Rename prisma/ folder to avoid confusion, add ORM section to CLAUDE.md'
  files_explored:
    - prisma/
    - src/domain/
    - ormconfig.ts
    - package.json
  tags:
    - 'orm'
    - 'typeorm'
    - 'prisma'
    - 'database'
```

### Example 5: File Purpose Assumption

```yaml
- timestamp: 2026-01-09T15:20:00Z
  category: 'naming'
  assumption: 'Assumed src/services/ contains business logic services'
  reality: 'src/services/ contains infrastructure services (email, cache, etc.) - business logic is in src/domain/use-cases/'
  discovery_point: 'Explored services folder and found only infrastructure concerns'
  impact: 'low'
  misleading_signals:
    - 'services/ folder name (often contains business logic)'
    - 'Similar naming to other projects'
  documentation_gap: 'CLAUDE.md architecture section should explain the folder structure and where business logic lives'
  files_explored:
    - src/services/
    - src/domain/use-cases/
  tags:
    - 'folder-structure'
    - 'architecture'
    - 'naming'
```

### Example 6: Entry Point Assumption

```yaml
- timestamp: 2026-01-09T16:10:00Z
  category: 'structure'
  assumption: 'Assumed src/index.ts is the application entry point'
  reality: 'Entry point is src/main.ts - index.ts is just barrel exports for the library'
  discovery_point: 'package.json main field points to dist/main.js, found bootstrap logic in main.ts'
  impact: 'low'
  misleading_signals:
    - 'src/index.ts exists (common entry point name)'
    - 'index.ts has exports at top level'
  documentation_gap: 'CLAUDE.md should specify main.ts as entry point for application startup'
  files_explored:
    - src/index.ts
    - src/main.ts
    - package.json
  tags:
    - 'entry-point'
    - 'project-structure'
    - 'bootstrap'
```

## Integration Pattern

### During Exploration

While exploring a new codebase:

1. Make initial assumptions based on conventions
2. Verify assumptions through exploration
3. When wrong, silently log the correction
4. Continue with corrected understanding

### During Implementation

While implementing features:

1. Proceed based on current understanding
2. If implementation reveals wrong assumption, pause
3. Log the incorrect assumption silently
4. Adjust approach and continue

### Example Flow

```
User: "Add a new API endpoint for user preferences"

[AI thinking: "Based on Express in dependencies, I'll create a REST endpoint"]
[AI explores src/api/ - finds GraphQL resolvers]
[AI thinking: "Wrong assumption - this is GraphQL, not REST"]

[AI silently logs assumption correction to .claude/assumption-corrections.yaml]

AI: "I see the API uses GraphQL with Apollo Server. I'll add a new
     resolver for user preferences rather than a REST endpoint."
```

User sees smooth adaptation. Later, they can review assumption-corrections.yaml to improve docs.

## Benefits

1. **Documentation Improvement**: Reveals what's missing from CLAUDE.md
2. **Onboarding Insights**: Shows what confuses newcomers (human or AI)
3. **Naming Feedback**: Identifies misleading names that should change
4. **Structure Clarity**: Highlights non-obvious organization
5. **Pattern Recognition**: Reveals which conventions cause confusion
6. **Continuous Improvement**: Each session improves context for the next

## Important Guidelines

1. **Be honest**: Only log genuinely wrong assumptions
2. **Be specific**: Document exactly what misled you
3. **Be constructive**: Always suggest documentation improvement
4. **Be silent**: Never interrupt workflow with logging notifications
5. **Be reflective**: Think about why the assumption seemed reasonable
6. **Identify signals**: List what led to the wrong conclusion
7. **Suggest fixes**: Propose concrete documentation additions
8. **Track impact**: Higher impact = higher priority for fixing

## Assumption Corrections YAML Schema

```yaml
# .claude/assumption-corrections.yaml
- timestamp: string          # ISO 8601: "2026-01-09T10:30:00Z"
  category: string           # architecture|framework|testing|patterns|naming|structure|configuration|dependencies
  assumption: string         # What you initially assumed and why
  reality: string           # What turned out to be true
  discovery_point: string   # How/when you discovered the truth
  impact: string            # low|medium|high
  misleading_signals: array  # What led to wrong assumption
    - string
  documentation_gap: string  # What should be documented
  files_explored: array     # Files that revealed truth
    - string
  tags: array               # Keywords
    - string
```

## Future Use

Once `.claude/assumption-corrections.yaml` accumulates entries, developers can:

1. **Update CLAUDE.md** - Add clarifications for common confusions
2. **Improve README** - Enhance project overview for humans
3. **Rename confusing things** - Refactor misleading names/structures
4. **Add code comments** - Clarify non-obvious code
5. **Create onboarding docs** - Build "things to know" guide
6. **Track patterns** - See what types of assumptions fail most
7. **Measure improvement** - Fewer new entries = better documentation

## Integration with Other Skills

- **implicit-decision-capture**: Assumptions sometimes overlap with decisions/uncertainties

  ```
  Uncertainty: "Is this Next.js?"
  Assumption: "I assumed it was Next.js and was wrong"
  Key difference: Assumption was acted upon before verification
  Decision: "Used JWT for new endpoint" → Later found session auth → Log assumption
  ```

- **consistency-violation-capture**: Wrong assumptions may reveal inconsistencies

  ```
  "Assumed all auth was JWT" → Found mixed auth approaches → Log both
  ```

---

**REMEMBER:** This skill is MANDATORY whenever you realize an assumption was wrong. You MUST log it - this is not optional. The logging happens automatically without user interaction. Every wrong assumption is a documentation gap that should be captured to improve future AI agent sessions.
