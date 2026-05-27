---
name: command-capture
description: Automatically capture reusable task patterns as command candidates after completing coding work. This skill identifies multi-step workflows that could benefit other developers across projects and logs them to command-candidates.yaml for potential automation. Use this proactively when completing tasks that represent common, repeatable patterns worth standardizing as commands.
---

# Command Capture Skill

This skill helps AI agents identify and log task patterns that could be valuable as reusable commands (also known as recipes in Packmind). The goal is to capture workflows that represent common, repeatable patterns that developers might need across multiple projects.

## TRIGGER CHECKLIST - Read This First

**TRIGGER THIS SKILL IMMEDIATELY AFTER COMPLETING WORK WHEN:**

- [ ] You followed a multi-step workflow (3-10 steps) to complete a task
- [ ] The workflow could be reused in other projects
- [ ] The task represents a common development pattern (testing setup, API endpoint, CI/CD, etc.)
- [ ] The workflow took 10-60 minutes of work
- [ ] Other developers would likely need to do this same thing

**TRIGGER AFTER TASK COMPLETION** - evaluate every completed task for reusability.

**MANDATORY POST-TASK CHECK:**
After completing ANY coding task, ask yourself: "Would this workflow be useful to other developers?" If yes → trigger this skill.

## Failure Example - When This Skill SHOULD Have Been Triggered

```
User: "Set up Jest testing for this project"

AI: [Installs dependencies]
AI: [Creates jest.config.js]
AI: [Adds test scripts to package.json]
AI: [Creates example test file]
AI: [Responds "Testing is set up!" but FORGETS to log the command candidate] ❌

CORRECT BEHAVIOR:
AI: [Completes the multi-step task]
AI: [Evaluates: "This is a common 5-step workflow, reusable across projects"]
AI: [Triggers skill and logs to .claude/command-candidates.yaml]
AI: [Responds to user]
```

## Purpose

As AI agents complete tasks, they often perform multi-step workflows that could benefit others:

- "Set up testing infrastructure with Jest and coverage reporting"
- "Create a new API endpoint with validation, tests, and documentation"
- "Add authentication middleware to an Express application"
- "Configure CI/CD pipeline with linting and tests"
- "Implement CRUD operations for a new entity"
- "Implement a release workflow with version bumping and changelog management"
- "Add a new rendering system for an AI agent with full integration across packages"
- "Create a new UI page with routing, components, and state management"
- "Write TypeORM migrations following project patterns with logging and rollback"
- "Add a new use case in hexagonal architecture with ports and adapters"

These workflows:

1. Follow a **repeatable pattern** with clear steps
2. Are **not too complex** to be automated or templated
3. Could be **reused by other developers** in different contexts
4. Would be used **once or multiple times per month** across projects
5. Provide **consistent value** when applied correctly

By capturing them as command candidates, developers can:

1. **Build a library** of reusable task patterns
2. **Standardize workflows** across teams and projects
3. **Speed up common tasks** with pre-defined templates
4. **Share knowledge** about effective implementation approaches
5. **Reduce cognitive load** for repetitive tasks

## When to Use This Skill

Use this skill **proactively and silently** after completing tasks when the work you performed:

1. **Represents a Common Pattern**
   - Setting up testing frameworks
   - Creating CRUD operations
   - Adding authentication/authorization
   - Configuring build tools or CI/CD
   - Implementing common architectural patterns
   - Release and deployment workflows
   - Multi-package system integrations
   - UI page implementations with routing and state
   - Database migration patterns

2. **Has Clear, Repeatable Steps**
   - The workflow has 3-10 distinct steps
   - Each step is well-defined and actionable
   - The order of steps matters for success
   - Similar tasks would follow similar steps

3. **Could Benefit Other Developers**
   - Not project-specific or one-off code
   - Applicable to different codebases
   - Solves a common problem
   - Follows best practices

4. **Has Appropriate Complexity**
   - Not too trivial (e.g., "add a file")
   - Not too complex (e.g., "redesign entire architecture")
   - Sweet spot: 10-30 minutes of work
   - Multiple related operations that form a cohesive task

5. **Would Be Used Regularly**
   - Developers might need this once or more per month
   - Common enough to justify automation
   - Standard enough to have consistent approach

## When NOT to Use

Don't capture:

- **One-off tasks** - Specific to this project only, unlikely to recur
- **Trivial operations** - Single-step tasks (e.g., "rename a variable")
- **Highly complex workflows** - Tasks requiring deep architectural decisions
- **Project-specific implementation** - Code that only makes sense in this context
- **User-defined custom logic** - Business rules specific to this application
- **Obvious standard operations** - "Write a function" or "Fix a bug" (too vague)

## Workflow

### Step 1: Complete Your Task

Implement the feature/fix as requested by the user.

### Step 2: Evaluate Reusability (Silent)

After completing the task, mentally review:

- Did I follow a multi-step workflow?
- Would this pattern be useful in other projects?
- Is this complex enough to be worth capturing?
- Would developers use this regularly?
- Can I summarize this in a clear name and description?

### Step 3: Silent Logging

**Silently** append command candidates to `.claude/command-candidates.yaml`:

```yaml
- name: 'setup-jest-testing'
  description: 'Configure Jest testing framework with TypeScript support, coverage reporting, and example test structure'
  category: 'testing' # setup|testing|api|database|deployment|architecture|security|performance|documentation|refactoring|ui|process
  frequency: 'monthly' # weekly|monthly|quarterly
  complexity: 'medium' # simple|medium|complex
  timestamp: '2026-01-09T10:30:00Z'
  context: 'Added Jest configuration while setting up testing for user service'
  applicability: 'cross-project' # project-specific|cross-project|universal
  tags:
    - 'jest'
    - 'testing'
    - 'typescript'
    - 'configuration'
```

### Step 4: File Management

**Location:** Always use `.claude/command-candidates.yaml` at the repository root.

**Structure:** Array of command candidate entries, most recent last.

**Format Rules:**

- `name`: Kebab-case identifier for the command (e.g., "setup-jest-testing", "create-api-endpoint")
- `description`: One or two sentences summarizing what the command does and the value it provides
- `category`: One of: setup, testing, api, database, deployment, architecture, security, performance, documentation, refactoring, ui, process
- `frequency`: How often developers might use this
  - `weekly`: Very common tasks (multiple times per week)
  - `monthly`: Regular tasks (once or more per month)
  - `quarterly`: Less frequent but still valuable
- `complexity`: Scope and difficulty of the task
  - `simple`: 3-5 steps, 10-15 minutes
  - `medium`: 5-8 steps, 15-30 minutes
  - `complex`: 8-10 steps, 30-60 minutes
- `timestamp`: ISO 8601 format when captured (YYYY-MM-DDTHH:mm:ssZ)
- `context`: Brief note about when/why this was captured
- `applicability`: How widely applicable this command is
  - `project-specific`: Mainly useful for this project
  - `cross-project`: Useful across multiple projects in same domain
  - `universal`: Useful across any project/domain
- `tags`: Relevant keywords for filtering/searching

**IMPORTANT:** This is an automatic, non-interrupting operation:

- Do NOT ask the user for permission to log
- Do NOT announce that you logged something
- Simply log and continue your work seamlessly
- The user can review `.claude/command-candidates.yaml` later

This skill is MANDATORY for reusable workflows - it's not optional.

### Step 5: User Review (Later)

Users can review `.claude/command-candidates.yaml` at any time to:

- Understand what reusable patterns were identified
- Prioritize which commands to formalize
- Create full command/recipe implementations
- Build a command library for their organization
- Identify common workflows that need standardization

## Example Scenarios

### Example 1: Testing Setup

**Task Completed:** "Set up Jest testing framework with TypeScript"

**Evaluation:**

- Multi-step process (install deps, configure jest.config.js, add test scripts, create example test)
- Very common across TypeScript projects
- Clear, repeatable steps
- Would be used regularly

**Logged Entry:**

```yaml
- name: 'setup-jest-typescript'
  description: 'Install and configure Jest testing framework for TypeScript projects with coverage reporting, test scripts, and example test structure'
  category: 'testing'
  frequency: 'monthly'
  complexity: 'medium'
  timestamp: '2026-01-09T09:15:00Z'
  context: 'Set up testing infrastructure for new microservice'
  applicability: 'universal'
  tags:
    - 'jest'
    - 'typescript'
    - 'testing'
    - 'configuration'
    - 'setup'
```

### Example 2: API Endpoint Creation

**Task Completed:** "Create new REST API endpoint for user management with validation"

**Evaluation:**

- Standard pattern (route → controller → service → tests)
- Common task for API development
- Well-defined steps
- Cross-project applicability

**Logged Entry:**

```yaml
- name: 'create-rest-endpoint'
  description: 'Create a new REST API endpoint with request validation, error handling, service layer implementation, and comprehensive tests'
  category: 'api'
  frequency: 'weekly'
  complexity: 'medium'
  timestamp: '2026-01-09T10:45:00Z'
  context: 'Added CRUD endpoints for user resource in Express API'
  applicability: 'cross-project'
  tags:
    - 'rest-api'
    - 'express'
    - 'validation'
    - 'testing'
    - 'crud'
```

### Example 3: Database Migration

**Task Completed:** "Add new database table with TypeORM migration"

**Evaluation:**

- Repeatable workflow (create entity, generate migration, test up/down, update schema)
- Common in projects using TypeORM
- Clear steps that must be followed in order
- Regular occurrence

**Logged Entry:**

```yaml
- name: 'create-typeorm-migration'
  description: 'Create a new TypeORM migration with entity definition, up/down methods, and testing to safely modify database schema'
  category: 'database'
  frequency: 'monthly'
  complexity: 'medium'
  timestamp: '2026-01-09T11:30:00Z'
  context: 'Added user_preferences table with migration'
  applicability: 'cross-project'
  tags:
    - 'typeorm'
    - 'database'
    - 'migration'
    - 'schema'
```

### Example 4: CI/CD Pipeline

**Task Completed:** "Set up GitHub Actions workflow with linting, tests, and build"

**Evaluation:**

- Standard DevOps pattern
- Applicable to many projects
- Multiple configuration steps
- Highly valuable for consistency

**Logged Entry:**

```yaml
- name: 'setup-github-actions-ci'
  description: 'Configure GitHub Actions CI pipeline with linting, testing, building, and coverage reporting for Node.js projects'
  category: 'deployment'
  frequency: 'monthly'
  complexity: 'medium'
  timestamp: '2026-01-09T14:00:00Z'
  context: 'Added CI pipeline for new repository'
  applicability: 'universal'
  tags:
    - 'ci-cd'
    - 'github-actions'
    - 'automation'
    - 'devops'
    - 'nodejs'
```

### Example 5: Authentication Middleware

**Task Completed:** "Implement JWT authentication middleware for Express"

**Evaluation:**

- Common security pattern
- Well-established steps
- Reusable across Express APIs
- Important enough to standardize

**Logged Entry:**

```yaml
- name: 'add-jwt-auth-middleware'
  description: 'Implement JWT authentication middleware for Express applications with token validation, error handling, and protected route examples'
  category: 'security'
  frequency: 'monthly'
  complexity: 'medium'
  timestamp: '2026-01-09T15:20:00Z'
  context: 'Added authentication to API endpoints'
  applicability: 'cross-project'
  tags:
    - 'authentication'
    - 'jwt'
    - 'express'
    - 'middleware'
    - 'security'
```

### Example 6: Component Library Setup

**Task Completed:** "Create reusable React component with Storybook documentation"

**Evaluation:**

- Standard component development workflow
- Follows best practices
- Repeatable for each new component
- Valuable for design systems

**Logged Entry:**

```yaml
- name: 'create-react-component-with-storybook'
  description: 'Create a reusable React component with TypeScript, props interface, unit tests, and Storybook documentation'
  category: 'architecture'
  frequency: 'weekly'
  complexity: 'simple'
  timestamp: '2026-01-09T16:10:00Z'
  context: 'Built Button component for design system'
  applicability: 'cross-project'
  tags:
    - 'react'
    - 'components'
    - 'storybook'
    - 'typescript'
    - 'design-system'
```

### Example 7: Release Process Workflow

**Task Completed:** "Create release workflow with version bumping, changelog updates, and git tagging"

**Evaluation:**

- Multi-step process (verify git status, update versions, update changelog, create tags, push)
- Common across projects that follow semantic versioning
- Clear, ordered steps that must be executed correctly
- Prevents manual errors in release process

**Logged Entry:**

```yaml
- name: 'release-workflow'
  description: 'Implement a release workflow with automatic version bumping in package.json, changelog updates with ISO 8601 dates, git tag creation, and preparation for next development cycle'
  category: 'process'
  frequency: 'monthly'
  complexity: 'medium'
  timestamp: '2026-01-09T17:00:00Z'
  context: 'Automated release process for semantic versioning'
  applicability: 'universal'
  tags:
    - 'release'
    - 'versioning'
    - 'changelog'
    - 'git'
    - 'automation'
```

### Example 8: Complex System Integration

**Task Completed:** "Add new AI agent rendering system with deployer, type mappings, frontend config, tests"

**Evaluation:**

- Complex integration across multiple packages in monorepo
- Touches types, backend deployer, frontend UI, documentation
- Repeatable pattern when adding new AI agent integrations
- Valuable for maintaining consistency in system extensions

**Logged Entry:**

```yaml
- name: 'add-ai-agent-rendering-system'
  description: 'Implement a new AI agent rendering pipeline including deployer class, type definitions, registry registration, frontend UI integration, documentation, and comprehensive unit/integration tests'
  category: 'architecture'
  frequency: 'quarterly'
  complexity: 'complex'
  timestamp: '2026-01-09T17:30:00Z'
  context: 'Added Continue.dev support to Packmind rendering system'
  applicability: 'project-specific'
  tags:
    - 'monorepo'
    - 'integration'
    - 'ai-agents'
    - 'deployer'
    - 'full-stack'
```

### Example 9: UI Page Implementation

**Task Completed:** "Create new settings page with routing, form components, validation, and API integration"

**Evaluation:**

- Standard frontend workflow (route setup, component creation, state management, API calls)
- Common when building admin panels or dashboard pages
- Well-defined pattern in React/Angular/Vue applications
- Includes testing and error handling

**Logged Entry:**

```yaml
- name: 'create-ui-settings-page'
  description: 'Implement a new UI page with routing configuration, form components, client-side validation, API integration, loading states, error handling, and tests'
  category: 'ui'
  frequency: 'weekly'
  complexity: 'medium'
  timestamp: '2026-01-09T18:00:00Z'
  context: 'Created user preferences settings page'
  applicability: 'cross-project'
  tags:
    - 'react'
    - 'routing'
    - 'forms'
    - 'validation'
    - 'frontend'
```

### Example 10: Architectural Pattern Implementation

**Task Completed:** "Add new use case in hexagonal architecture with ports, adapters, and domain logic"

**Evaluation:**

- Architectural pattern with clear structure (domain → ports → adapters → infrastructure)
- Common in projects following clean architecture / hexagonal architecture
- Multiple files and layers involved
- Establishes consistent structure for new features

**Logged Entry:**

```yaml
- name: 'add-hexagonal-use-case'
  description: 'Implement a new use case following hexagonal architecture with domain logic, port interfaces, adapter implementations, dependency injection, and comprehensive tests for each layer'
  category: 'architecture'
  frequency: 'monthly'
  complexity: 'complex'
  timestamp: '2026-01-09T18:30:00Z'
  context: 'Added user notification use case with ports and adapters'
  applicability: 'cross-project'
  tags:
    - 'hexagonal-architecture'
    - 'clean-architecture'
    - 'use-case'
    - 'ports-adapters'
    - 'domain-driven-design'
```

## Integration Pattern

### During Task Completion

After implementing a feature:

1. Complete the implementation
2. Reflect on the workflow you followed
3. Evaluate if it meets the criteria for a command candidate
4. Silently log to command-candidates.yaml if applicable
5. Continue to next task or respond to user

### Example Flow

```
User: "Set up testing for the new service"

[AI implements Jest with config, example tests, coverage setup]

[AI thinking: "This is a repeatable pattern - Jest setup is common"]
[AI thinking: "5-7 clear steps, would be useful across projects"]
[AI thinking: "Medium complexity, done monthly across teams"]

[AI silently logs command candidate to .claude/command-candidates.yaml]

AI: "I've set up Jest testing with TypeScript support, coverage reporting,
     and example test structure. You can run tests with 'npm test'."
```

User sees the implementation. Later, they can review `.claude/command-candidates.yaml` to see what reusable patterns emerged.

## Benefits

1. **Knowledge Capture**: Documents valuable workflows as they emerge naturally
2. **Pattern Library**: Builds a collection of proven, reusable task patterns
3. **Team Efficiency**: Enables quick reuse of common workflows
4. **Standardization**: Promotes consistent approaches across projects
5. **Onboarding**: New team members see examples of standard workflows
6. **Continuous Improvement**: Identifies which tasks are worth automating

## Important Guidelines

1. **Be selective**: Only capture truly reusable patterns, not one-off tasks
2. **Be clear**: Name and description should immediately convey value
3. **Be honest**: Only log patterns you actually followed, not theoretical ones
4. **Be silent**: Never interrupt workflow with logging notifications
5. **Be practical**: Focus on tasks that would genuinely save time if templated
6. **Consider frequency**: If a task is done less than quarterly, it may not be worth capturing
7. **Assess complexity**: Too simple (1-2 steps) or too complex (requires deep thinking) aren't good candidates

## Command Candidates YAML Schema

```yaml
# .claude/command-candidates.yaml
- name: string              # Kebab-case: "setup-jest-testing"
  description: string       # 1-2 sentences: "Configure Jest with TypeScript..."
  category: string          # setup|testing|api|database|deployment|architecture|security|performance|documentation|refactoring|ui|process
  frequency: string         # weekly|monthly|quarterly
  complexity: string        # simple|medium|complex
  timestamp: string         # ISO 8601: "2026-01-09T10:30:00Z"
  context: string          # Brief note: "Added testing to user service"
  applicability: string    # project-specific|cross-project|universal
  tags: array             # Keywords
    - string              # "jest", "typescript", etc.
```

## Future Use

Once `.claude/command-candidates.yaml` accumulates entries, developers can:

1. **Review by frequency** - Prioritize weekly/monthly tasks for automation
2. **Review by applicability** - Universal commands are highest value
3. **Review by complexity** - Medium complexity often has best ROI
4. **Create full commands** - Develop detailed recipes from candidates
5. **Build command library** - Standardize workflows across organization
6. **Share with community** - Contribute valuable patterns to Packmind
7. **Identify training gaps** - See what workflows need better documentation

## Integration with Other Skills

- **implicit-decision-capture**: Command candidates may reference specific technical decisions

  ```
  Command involves choosing patterns → decisions.yaml has the technical rationale
  Repeated uncertainties → Opportunity for a command to standardize the approach
  ```

- **signal-capture**: Commands represent formalized workflows based on standards
  ```
  Standards define "how" → Commands automate the "what"
  ```

## Distinguishing Commands from Other Captures

- **Decision (implicit-decision-capture)**: "I chose compound components pattern" - A technical choice or uncertainty
- **Signal (signal-capture)**: "Prefix interfaces with I" - A coding standard
- **Command (command-capture)**: "Set up Jest testing framework" - A reusable workflow

All four work together:

- Signals define standards
- Decisions apply standards to specific contexts
- Uncertainties reveal gaps in guidance
- Commands automate common workflows that follow standards and apply decisions

---

**REMEMBER:** This skill is MANDATORY after completing multi-step coding tasks. Evaluate every completed task for reusability. If the workflow could benefit other developers, you MUST log it - this is not optional. The logging happens automatically without user interaction. Building a library of reusable workflows is a key goal of this skill.
