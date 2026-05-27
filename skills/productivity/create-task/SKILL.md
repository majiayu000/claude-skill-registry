---
name: create-task
description: This skill should be used when the user asks to 'create a task from', 'add issue for', 'track work on', or provides conversational task descriptions like 'I need to fix the blog bug' or 'remind me to update the docs'. Converts natural language task descriptions into structured beads with automatic categorization, priority inference, and optional blocking relationships.
---

# Task Creation Skill

Converts conversational task descriptions into structured work items (beads) with automatic categorization, priority assignment, and dependency tracking.

## When to Use

Activate this skill when users ask to:
- Create or add a new task or issue
- Track work that needs to be done
- Convert conversational descriptions into structured work items
- Document something to remember or do later
- Set up tasks with blocking relationships
- Categorize and prioritize work

## Required Information

Gather from conversation:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| **Title** | String | "Fix blog pagination bug" | Clear, specific task name |
| **Description** | String | "The blog archive page shows 404 on pages 2+ after deployment" | Detailed context and acceptance criteria |

## Optional Information

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| **Tags** | Array | ["bug", "urgent", "frontend"] | For categorization and filtering |
| **Blocking** | Array | ["task-id-123"] | Task IDs this blocks (dependent tasks) |
| **BlockedBy** | Array | ["task-id-456"] | Task IDs that block this one |
| **Priority** | Number | 1-5 | 1=critical, 5=low (inferred if not provided) |

## Auto-Categorization Rules

The system automatically determines task type and priority from natural language patterns:

### Task Type Detection

| Pattern | Type | Emoji |
|---------|------|-------|
| "fix", "resolve", "patch", "bug" | bug | 🐛 |
| "add", "create", "implement", "build" | feature | ✨ |
| "improve", "enhance", "optimize", "refactor" | enhancement | 🔧 |
| "update", "upgrade", "bump", "patch version" | chore | ⚙️ |
| "document", "write", "add docs", "update README" | documentation | 📝 |
| "investigate", "research", "explore", "investigate" | research | 🔍 |

### Priority Inference

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| "critical", "urgent", "blocking", "ASAP", "now" | 1 (P0) | Immediate action needed |
| "important", "high", "soon", "before release" | 2 (P1) | Next cycle priority |
| "normal", "should", "eventually" | 3 (P2) | Standard priority |
| "nice-to-have", "consider", "backlog" | 4 (P3) | Lower priority |
| "someday", "maybe", "if time" | 5 (P4) | Lowest priority |

## Generation Process

### Step 1: Gather Task Information

Collect through conversation:

1. "What needs to be done?" (Title)
2. "Can you describe more details?" (Description)
3. "Any context on why or when?" (Optional tags/priority hints)

If user provides conversational description like "The blog is broken on mobile", extract and clarify:
- Title: "Fix mobile layout on blog pages"
- Description: Expanded context about the issue

### Step 2: Auto-Detect Category and Priority

Parse the description and title for keywords:
- Identify task type from verb patterns
- Infer priority from urgency keywords
- Extract dependencies if mentioned

### Step 3: Invoke Task Agent

Run the TypeScript agent to create the task:

```bash
bun run packages/agents/src/cli/agent-cli.ts task-create \
  --title "{{title}}" \
  --description "{{description}}" \
  --type {{type}} \
  --priority {{priority}} \
  --tags "{{tags}}" \
  --blocking "{{blocking}}" \
  --blocked-by "{{blocked_by}}"
```

The agent will:
1. Parse natural language input
2. Create a structured bead in `.beads/issues.jsonl`
3. Assign a unique task ID
4. Set up blocking relationships if provided
5. Return task details and confirmation

**Example output:**
```
--- Task Agent ---

Creating task from description...

[SUCCESS] Task created

Task ID: PROJ-123
Title: Fix blog pagination bug
Type: bug (🐛)
Priority: P1 (High)
Status: pending

Description:
The blog archive page shows 404 on pages 2+ after deployment.
Root cause appears to be missing pagination handler in router.

URL: [task details URL]
```

### Step 4: Display and Confirm

Show the user:
- Generated task ID
- Auto-detected category and priority
- Full description as it was stored
- Any blocking relationships
- Next steps for the task (assignment, workflow)

## Task Type Definitions

### Bug (🐛)
Something is broken or not working as expected.
- **Markers:** "fix", "broken", "bug", "error", "issue", "not working"
- **Default Priority:** P1 or P2 depending on urgency keywords

### Feature (✨)
New functionality to add.
- **Markers:** "add", "create", "implement", "build", "new"
- **Default Priority:** P2 or P3 (features are typically planned)

### Enhancement (🔧)
Improving existing functionality.
- **Markers:** "improve", "enhance", "optimize", "refactor", "speed up", "better"
- **Default Priority:** P2 or P3

### Chore (⚙️)
Maintenance, dependency updates, configuration changes.
- **Markers:** "update", "upgrade", "bump", "version", "dependencies"
- **Default Priority:** P3 (non-blocking)

### Documentation (📝)
Writing or updating documentation.
- **Markers:** "document", "write docs", "add README", "update guide"
- **Default Priority:** P3 (can document in parallel)

### Research (🔍)
Investigation or evaluation needed.
- **Markers:** "investigate", "research", "explore", "evaluate", "compare"
- **Default Priority:** P3 or P4 (time-bounded research)

## Dependency Management

### Setting Up Blocking Relationships

If a task depends on another or blocks others, express as:

**User:** "I need to refactor the API before we can optimize the cache layer"

**Response:** Extract two tasks:
- Task A: "Refactor the API" → Type: enhancement, Priority: P1
- Task B: "Optimize cache layer" → Type: enhancement, Priority: P2
- Set: Task B is blocked by Task A

```bash
bun run packages/agents/src/cli/agent-cli.ts task-create \
  --title "Optimize cache layer" \
  --description "..." \
  --type enhancement \
  --blocked-by "{{task-a-id}}"
```

### Querying Blockers

After creating tasks, show dependencies:
```
Task PROJ-124 (Optimize cache) is blocked by:
  └─ PROJ-123 (Refactor API) - pending

Cannot start until PROJ-123 is completed.
```

## Writing Task Descriptions

### Do:
- Be specific about what needs to happen
- Include context: why, where, what problem it solves
- Add acceptance criteria if applicable ("The page should load in < 1s")
- Mention any related tasks or tickets
- Include error messages or reproduction steps for bugs

### Avoid:
- Generic descriptions like "fix stuff"
- Assumptions about implementation details (let the executor decide)
- Combining multiple unrelated tasks in one item
- Vague impact statements ("make it better")

## Example Interactions

### Example 1: Simple Bug Report

**User:** "The checkout button on the homepage is broken"

**Response:**
1. Clarify: "Can you describe what's broken? Is it not clickable, hidden, or showing an error?"
2. Gather details about browser, reproduction steps
3. Create task:
   ```
   Task ID: PROJ-201
   Title: Fix checkout button functionality on homepage
   Type: bug (🐛)
   Priority: P1 (Critical - affects conversions)
   ```

### Example 2: Feature Request with Dependencies

**User:** "I want to add an analytics dashboard, but first we need to set up event tracking"

**Response:**
1. Create two tasks:
   ```
   Task ID: PROJ-301
   Title: Implement event tracking infrastructure
   Type: feature (✨)
   Priority: P1

   Task ID: PROJ-302
   Title: Build analytics dashboard
   Type: feature (✨)
   Priority: P2
   Blocked By: PROJ-301
   ```
2. Show the dependency chain
3. Explain that PROJ-302 cannot start until PROJ-301 is completed

### Example 3: Enhancement with Optimization Context

**User:** "We should optimize the blog query performance, it's getting slow with more posts"

**Response:**
1. Gather: "How slow? Do you have metrics? Which queries are slow?"
2. Create task:
   ```
   Task ID: PROJ-401
   Title: Optimize blog query performance
   Type: enhancement (🔧)
   Priority: P2

   Description:
   Blog queries are getting slower as post count increases.
   Goal: Sub-100ms response time for archive pages.
   Consider indexing strategy, caching layer, and query optimization.
   ```

## File Locations

| Purpose | Path |
|---------|------|
| Task tracking | `.beads/issues.jsonl` |
| Task agent | `packages/agents/src/task/task-agent.ts` |
| CLI handler | `packages/agents/src/cli/agent-cli.ts` |
| Type definitions | `packages/agents/src/types/index.ts` |

## Task Lifecycle

Tasks created with this skill start in `pending` status:

```
pending → in_progress → completed
            ↓
        (if issues)
          resolved
```

Use beads commands to manage lifecycle:
```bash
bd update <task-id> --status in_progress
bd update <task-id> --status completed
bd close <task-id>
```

## Common Patterns

### Multi-step Breakdown

If user describes complex work, offer to break into subtasks:

**User:** "Redesign the checkout flow"

**Suggest:**
- Task 1: "Design checkout wireframes"
- Task 2: "Implement checkout form component"
- Task 3: "Integrate payment processing"
- Task 4: "Add order confirmation page"

Set dependencies so they work in sequence.

### Adding Context from Errors

For bug reports, include error messages and logs in description:

```
Task: Fix authentication redirect loop

Description:
Users report infinite redirect when accessing /dashboard after login.

Error log:
  [ERROR] /auth/callback → /dashboard → /login → /auth/callback

Environment: Production
Affected users: ~15% of login attempts
First reported: 2026-01-24
```

## Voice Learning

Record feedback on task creation for improvement:

```
Location: .cody/project/library/style-docs/task-style.json

Track:
- Effective task titles (what works)
- Common categorization errors (what to fix)
- Useful description patterns (what to encourage)
```

## Integration with Workflows

After task creation, users can:

1. **Assign** - `bd update <task-id> --owner <name>`
2. **Add labels** - `bd label add <task-id> bug frontend`
3. **Link dependencies** - `bd dep add <task-a> --blocks <task-b>`
4. **Start working** - `bd update <task-id> --status in_progress`
