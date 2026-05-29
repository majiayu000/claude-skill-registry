---
description: Brainstorm a feature idea, then generate PRDs for Ralph autonomous execution.
---

# /idea - From Brainstorm to PRD

You are helping the user go from a rough idea to executable PRDs for Ralph.

**CRITICAL: This command does NOT write code. It produces documentation files only.**

## When to Use

| Workflow | Best For |
|----------|----------|
| **`/idea`** | Structured brainstorming with guided questions - Claude leads |
| **Plan mode → save to `docs/ideas/`** | Free-form exploration - you lead the thinking |
| **`/prd "description"`** | Quick PRD, no docs artifact needed |

**Both `/idea` and plan mode can produce `docs/ideas/*.md` files.** The difference is who drives the conversation:
- `/idea` asks you structured questions (scope, UX, edge cases, etc.)
- Plan mode lets you explore freely with Claude's help

Use `/idea` when you want the structured checklist. Use plan mode when you prefer to think through it your way.

## User Input

```text
$ARGUMENTS
```

## Workflow

### Step 1: Start Brainstorming

If `$ARGUMENTS` is empty, ask: "What feature or idea would you like to brainstorm?"

If `$ARGUMENTS` has content, acknowledge it and proceed.

Say: "Let's brainstorm this idea. I'll help you think it through, then we'll create documentation for Ralph to execute."

### Step 2: Explore and Ask Questions

Help the user flesh out the idea through conversation:

1. **Understand the goal** - What problem does this solve? Who benefits?
2. **Explore the codebase** - Use Glob/Grep/Read to understand what exists and what patterns to follow
3. **Ask clarifying questions** about:

**Scope & UX:**
- What's in scope vs out of scope?
- What does the user see/do? (ask for mockup if UI)
- What are the edge cases?

**Security (IMPORTANT - ask if feature involves):**
- Authentication: Who can access this? Login required?
- Passwords: How stored? (must be hashed, never plain text)
- User input: What validation needed? (SQL injection, XSS, command injection)
- Sensitive data: What should NEVER be in API responses?
- Rate limiting: Should this be rate limited? (login attempts, API calls)

**Scale (IMPORTANT - ask if feature involves lists/data):**
- How many items expected? (10s, 1000s, millions?)
- Pagination needed? What's the max per page?
- Caching needed? How fresh must data be?
- Database indexes: What will be queried/sorted frequently?

**Migration/Refactoring (IMPORTANT - ask if moving or restructuring code):**
- Source paths: Where does the code currently live?
- Destination paths: Where should it end up? (be explicit, not vague)
- Phases: What's the logical order? (move files → update imports → verify)
- Verification: What commands prove each phase worked?

### Step 3: Summarize Before Writing

When you have enough information, summarize what you've learned:

Say: "Here's what I understand about the feature:

**Problem:** [summary]
**Solution:** [summary]
**Key decisions:** [list]

Ready to write this to `docs/ideas/{feature-name}.md`? Say **'yes'** or tell me what to adjust."

**STOP and wait for user confirmation before writing any files.**

### Step 4: Write the Idea File

Once the user confirms, write the idea file:

1. Create the directory if needed:
   ```bash
   mkdir -p docs/ideas
   ```

2. Write to `docs/ideas/{feature-name}.md` with this structure:
   ```markdown
   # {Feature Name}

   ## Problem
   What problem does this solve?

   ## Solution
   High-level description of the solution.

   ## User Stories
   - As a [user], I want to [action] so that [benefit]
   - ...

   ## Scope
   ### In Scope
   - ...

   ### Out of Scope
   - ...

   ## Architecture
   ### Directory Structure
   - Where new files should go (be specific: `src/components/forms/`, not just `src/`)

   ### Patterns to Follow
   - Existing components/utilities to reuse
   - Naming conventions

   ### Do NOT Create
   - List things that already exist (avoid duplication)

   ## Security Requirements
   - **Authentication**: Who can access? Login required?
   - **Password handling**: Must be hashed with bcrypt (cost 10+), never in responses
   - **Input validation**: What must be validated/sanitized?
   - **Rate limiting**: What should be rate limited?
   - **Sensitive data**: What must NEVER appear in logs/responses?

   ## Scale Requirements
   - **Expected volume**: How many users/items/requests?
   - **Pagination**: Max items per page (recommend 100)
   - **Caching**: What can be cached? For how long?
   - **Database**: What indexes are needed?

   ## Migration Mapping (if moving/restructuring code)
   For refactoring or migration tasks, explicitly map source to destination:

   | Source | Destination |
   |--------|-------------|
   | `~/Sites/old-project/src/` | `apps/new-location/src/` |
   | `~/Sites/old-project/tests/` | `apps/new-location/tests/` |

   ## Phases & Verification
   Break complex work into phases with explicit verification commands:

   ### Phase 1: [Name]
   **What:** Description of what this phase accomplishes
   **Exit Criteria:**
   ```bash
   # These commands must pass before phase is complete
   test -d apps/new-location/src
   cd apps/new-location && uv run pytest -x
   cd apps/new-location && npm run build
   ```

   ### Phase 2: [Name]
   **What:** Description
   **Exit Criteria:**
   ```bash
   # Verification commands for phase 2
   docker-compose config | grep -q 'service-name:'
   curl -s http://localhost:8000/health | jq -e '.status == "ok"'
   ```

   ## UI Mockup (if applicable)
   ```
   ┌─────────────────────────────────┐
   │  [ASCII mockup of the UI]       │
   └─────────────────────────────────┘
   ```

   ## Open Questions
   - Any unresolved decisions
   ```

3. Say: "I've written the idea to `docs/ideas/{feature-name}.md`.

   Review it and let me know:
   - **'approved'** - Ready to generate PRD
   - **'edit [changes]'** - Tell me what to change"

**STOP and wait for user response. Do not proceed until they say 'approved' or 'done'.**

### Step 5: Generate PRD

**Only proceed here after user explicitly approves the idea file.**

Say: "Now I'll generate the PRD from your idea file."

**Use the Skill tool** to invoke `/prd` with the idea file path:
```
Skill: prd
Args: docs/ideas/{feature-name}.md
```

This hands off to `/prd` which handles:
- Reading the idea file
- Splitting into stories
- Writing `.ralph/prd.json`
- All PRD schema details (testing, testSteps, MCP tools, etc.)

**DO NOT duplicate the PRD schema or guidelines here - /prd is the single source of truth.**

---

## Error Handling

- If user provides no arguments, ask what they want to brainstorm
- If user abandons mid-flow, the idea file is still saved for later
- If /prd fails, check the idea file has enough detail

---

## Guidelines

### Idea File Quality

A good idea file has:
- **Clear problem statement** - What's broken or missing?
- **Specific solution** - Not vague ("improve UX") but concrete ("add inline validation")
- **Scope boundaries** - What's explicitly out of scope?
- **Architecture hints** - Where do files go? What patterns to follow?
- **Verification commands** - How do we know it worked? (executable commands, not prose)

### Migration/Refactoring Ideas

For ideas that involve moving or restructuring code, MUST include:

1. **Explicit path mapping** - Source → Destination for every directory
   ```
   ❌ "Move GOPA to apps folder"
   ✅ "~/Sites/gopa/src/gopa/ → apps/gopa/src/gopa/"
   ```

2. **Phase-based verification** - Each phase has exit criteria with commands
   ```
   ❌ "Verify everything still works"
   ✅ "cd apps/gopa && uv run pytest -x && uv run python -c 'from gopa.server import mcp'"
   ```

3. **Order of operations** - What must happen before what?
   - Move files → Update imports → Update configs → Verify

### ASCII Art for UI

If the feature involves UI, include ASCII mockups in the idea file:

```
┌─────────────────────────────────────┐
│  Dashboard                    [⚙️]  │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────┐  ┌─────────┐          │
│  │ Card 1  │  │ Card 2  │          │
│  │  $1,234 │  │  89%    │          │
│  └─────────┘  └─────────┘          │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Recent Activity              │   │
│  │ • Item 1                     │   │
│  │ • Item 2                     │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

Ralph will read these from the idea file via `story.contextFiles`.
