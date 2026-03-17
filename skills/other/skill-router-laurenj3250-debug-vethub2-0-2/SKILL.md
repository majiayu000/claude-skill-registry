---
name: skill-router
description: Analyzes tasks to find the optimal workflow of skills, presents the recommended sequence with rationale, and lets user approve/modify before execution. Use when starting any complex task, wanting help finding the right tools, or needing a structured approach.
---

# Skill Router

Analyze tasks and recommend optimal skill workflows.

## How It Works

1. **Analyze the task** - Understand what user is trying to accomplish
2. **Match to workflow pattern** - Find best skill sequence for the task type
3. **Present with rationale** - Explain why each skill and in what order
4. **Let user modify** - Accept, modify, or skip to specific step
5. **Execute sequentially** - Run skills in order, passing context between them

## Workflow Pattern Library

### Design & UI

| Task Type | Workflow | When to Use |
|-----------|----------|-------------|
| **Design from reference** | `ai-multimodal` → `brainstorming` → `writing-plans` → `aesthetic` → `frontend-design` → `code-review` | User has a screenshot/reference they want to build from |
| **Build UI from scratch** | `brainstorming` → `writing-plans` → `frontend-design` → `code-review` | Building new UI without reference |
| **Improve existing UI** | `chrome-devtools` (screenshot) → `ai-multimodal` → `aesthetic` → `frontend-design` | Enhancing current design |
| **Design system work** | `aesthetic` → `frontend-development` → `code-review` | Component libraries, tokens, themes |

### Development

| Task Type | Workflow | When to Use |
|-----------|----------|-------------|
| **New feature** | `brainstorming` → `writing-plans` → `executing-plans` → `code-review` | Adding significant functionality |
| **API development** | `brainstorming` → `backend-development` → `code-review` | Building APIs, services |
| **Research & build** | `docs-seeker` → `brainstorming` → `writing-plans` → `executing-plans` | Need to learn before implementing |
| **Quick implementation** | `writing-plans` → `executing-plans` | Clear requirements, just need to build |

### Debugging & Quality

| Task Type | Workflow | When to Use |
|-----------|----------|-------------|
| **Bug fixing** | `systematic-debugging` → `code-review` | Finding and fixing bugs |
| **Flaky tests** | `systematic-debugging` → `condition-based-waiting` → `code-review` | Tests pass sometimes, fail others |
| **Performance issues** | `chrome-devtools` → `systematic-debugging` → `code-review` | Slow app, need profiling |
| **Security review** | `code-review` → `defense-in-depth` | Checking for vulnerabilities |

### Content & Documentation

| Task Type | Workflow | When to Use |
|-----------|----------|-------------|
| **Content creation** | `content-research-writer` | Writing articles, docs with research |
| **LLM prompts** | `prompt-engineering` | Writing prompts for AI systems |
| **Technical docs** | `docs-seeker` → `content-research-writer` | Documentation with research |

### Infrastructure

| Task Type | Workflow | When to Use |
|-----------|----------|-------------|
| **Deploy app** | `devops` | Cloudflare, Docker, GCP deployment |
| **Database work** | `databases` | MongoDB, PostgreSQL operations |
| **MCP server** | `mcp-builder` → `code-review` | Building MCP integrations |
| **MCP tools** | `mcp-management` | Discovering/using existing MCP tools |

## Task Recognition Signals

Look for these keywords to identify task type:

| Keywords | Task Type |
|----------|-----------|
| "screenshot", "like this", "reference", "inspiration", "similar to" | Design from reference |
| "UI", "component", "page", "interface", "design" | Build UI |
| "bug", "error", "broken", "not working", "fix" | Bug fixing |
| "flaky", "sometimes fails", "intermittent" | Flaky tests |
| "slow", "performance", "optimize", "speed" | Performance issues |
| "feature", "add", "implement", "build" | New feature |
| "API", "endpoint", "backend", "server" | API development |
| "how to", "docs", "documentation", "learn" | Research & build |
| "write", "article", "content", "blog" | Content creation |
| "prompt", "LLM", "Claude", "GPT" | LLM prompts |
| "deploy", "hosting", "production" | Deploy app |
| "database", "query", "migration" | Database work |
| "MCP", "tool", "integration" | MCP work |

## Presenting the Workflow

Use `AskUserQuestion` to present the recommended workflow:

```markdown
**Recommended Workflow for:** [task description]

1. **[skill-name]** - [what it does for this task]
2. **[skill-name]** - [what it does for this task]
3. **[skill-name]** - [what it does for this task]

**Why this order:** [brief rationale]
```

**Question format:**
- header: "Workflow"
- multiSelect: false
- options:
  - "Accept workflow" - Run all steps in sequence
  - "Modify workflow" - Let me adjust the steps
  - "Skip to step" - Jump to a specific skill
  - "Just show skills" - Show individual options instead

## Workflow Execution

When user accepts:
1. **Run Mandatory Quality Gate first** - Think through data flow, async, race conditions
2. Invoke first skill
3. After completion, pass relevant context to next skill
4. Continue through workflow
5. **Self-roast before claiming done** - Actively try to break your own code
6. Offer to run `code-review` at end if not included

When user wants to modify:
1. Present all skills in workflow as multiSelect list
2. Let them remove/reorder
3. Ask if they want to add any other skills
4. Execute modified workflow

## Context Passing

Maintain a workflow context that includes:
- Original task description
- Outputs/decisions from each completed skill
- Any user feedback during execution

Pass this context when invoking each skill so they build on previous work.

## Rules

- **Always present workflow first** - Never auto-execute without approval
- **Explain the rationale** - Help user understand why this sequence
- **Allow modification** - User knows their needs best
- **Pass context forward** - Each skill should know what came before
- **Offer code-review** - Suggest at end of any coding workflow
- **Handle unknowns** - If task doesn't match patterns, ask clarifying questions first
- **⚠️ MANDATORY: Run Quality Gate** - Before ANY code, think through data/async/race conditions
- **⚠️ MANDATORY: Self-Roast** - Before claiming done, actively try to break your code
- **No half-assed work** - If you find issues, fix them. Don't ship with known problems.

## Google-Engineer Production Checklist (MANDATORY)

**Every implementation MUST include solutions for ALL of these:**

| Concern | Required Solution |
|---------|-------------------|
| **DRY Violations** | Centralized config modules for any value used in 2+ places |
| **Error Handling** | Error boundaries (React), try-catch with proper logging, graceful degradation |
| **Loading States** | Skeleton loaders that match content structure (NOT spinners) |
| **User Feedback** | Toast/notification for ALL mutations (success AND failure) |
| **Optimistic Updates** | TanStack Query pattern with snapshot/rollback for instant UX |
| **Mobile UX** | Min 44px touch targets, responsive grids, thumb-zone placement |
| **Type Safety** | Strict TypeScript, Zod validation at boundaries, no `any` |
| **Testing** | E2E tests for critical paths, unit tests for business logic |
| **Accessibility** | ARIA labels, keyboard navigation, color contrast |
| **Performance** | Lazy loading, code splitting, memoization where needed |

**Defensive Programming Patterns:**
- Validate inputs at system boundaries (API routes, form submissions)
- Never trust client data on the server
- Use TypeScript strict mode
- Prefer immutable updates
- Handle null/undefined explicitly
- Log errors with context (not just the error message)

---

## Mandatory Quality Gate (ALL TASKS)

**⚠️ THIS IS NOT OPTIONAL - APPLIES TO EVERY TASK, EVERY FIX, EVERY FEATURE**

**BEFORE writing ANY code, ask yourself:**

1. **Understand the data flow**
   - Where does the data come from?
   - What updates the data?
   - What depends on fresh data?

2. **Check async/await ordering**
   - Does this code depend on data that's fetched asynchronously?
   - Am I updating UI state BEFORE or AFTER the data is ready?
   - Will the user see stale data flash before the update?

3. **Race condition checklist**
   - Can the user trigger this action multiple times rapidly?
   - What happens if async operation A completes after operation B started?
   - Is there shared state that could be corrupted?

4. **State timing questions**
   - When I call `setState`, what data will the next render see?
   - Am I reading from state that was JUST updated (it won't be fresh yet)?
   - Should I `await` something before showing UI?

**Red flags that indicate duct tape:**
- "It works but might flash wrong data briefly" → NOT DONE
- "The data updates on the next render" → FIX THE ORDERING
- "User just needs to refresh" → BUILD IT PROPERLY
- "Works if you don't click too fast" → HANDLE THE RACE CONDITION
- Setting state then immediately reading from array that state updates → AWAIT FIRST

**Proper pattern for UI that depends on fresh data:**
```typescript
// WRONG - duct tape
doAsyncThing();
setShowModal(true); // Modal sees stale data

// RIGHT - proper
await doAsyncThing();
setShowModal(true); // Modal sees fresh data
```

---

## Self-Roast Protocol (MANDATORY BEFORE "DONE")

**After implementing ANY change, BEFORE claiming it's done:**

1. **Actively try to break it** - Don't just test the happy path
   - What if user clicks twice rapidly?
   - What if the network is slow?
   - What if data is missing/null?
   - What if user does things out of order?

2. **Question your assumptions**
   - "Will this always be true?" (probably not)
   - "What if this state is stale?"
   - "What happens on first load vs subsequent loads?"

3. **Roast your own code**
   - Look at what you wrote and ask: "What's wrong with this?"
   - If you can't find anything wrong, you're not looking hard enough
   - Pretend a senior dev is reviewing - what would they critique?

4. **Check these specific things:**
   - [ ] Async operations complete before dependent code runs
   - [ ] State updates are awaited before UI reads from them
   - [ ] Error cases are handled (not just logged)
   - [ ] Loading states exist where needed
   - [ ] User can't break it with rapid clicks
   - [ ] Works on first load, not just after refresh

**If you find issues during self-roast → FIX THEM FIRST**

Don't tell the user "it works" and then list caveats. Fix the caveats.

---

## Build It Right Protocol

**BEFORE starting any feature implementation:**

1. **Define "done"** - Write a brief spec listing all user-facing touchpoints:
   - What can users CREATE?
   - What can users READ/VIEW?
   - What can users UPDATE?
   - What can users DELETE?
   - What can users CONFIGURE?

2. **Ask clarifying questions** - If any part is ambiguous, ask BEFORE coding:
   - "Should users be able to view X later?"
   - "How should users configure this?"
   - "What happens when Y occurs?"

3. **Get approval on the spec** - Present the full scope and confirm before implementing

**DURING implementation:**

4. **No duct tape** - If you find yourself saying:
   - "You can run this SQL command to..." → Build the UI instead
   - "We can add that later..." → Add it now or explicitly descope it
   - "For now, just..." → Either do it properly or don't do it

5. **Complete the loop** - Every feature needs:
   - The core functionality
   - A way to view/access it
   - A way to configure it (if applicable)
   - Error handling for edge cases

**AFTER implementation:**

6. **Verify completeness** - Answer these before marking done:
   - "What can a user do now that they couldn't before?"
   - "Walk me through the complete user flow"
   - "Is there any manual step required?" (if yes, not done)

7. **Never claim "done" if:**
   - Tests are failing
   - Implementation is partial
   - Any workarounds are required
   - Configuration requires raw SQL/CLI commands

## Fallback: Individual Skill Selection

If user prefers to pick individual skills or task doesn't match patterns:

### Skill Categories

**Development & Coding**
- `frontend-design` - Production-grade UI with high design quality
- `frontend-development` - React/TypeScript patterns, performance
- `backend-development` - APIs, databases, auth, microservices
- `code-review` - Security, quality, best practices
- `systematic-debugging` - Root cause analysis and fixes

**Planning & Thinking**
- `brainstorming` - Refine ideas through collaborative questioning
- `writing-plans` - Design implementation strategies
- `executing-plans` - Execute plans in controlled batches

**Design & Media**
- `aesthetic` - Beautiful interfaces, design principles
- `canvas-design` - Posters, art, static visual designs
- `ai-multimodal` - Analyze/generate audio, video, images, PDFs
- `chrome-devtools` - Browser automation, screenshots

**Testing & Quality**
- `webapp-testing` - End-to-end testing
- `condition-based-waiting` - Fix flaky tests
- `defense-in-depth` - Multi-layer validation

**Documentation & Research**
- `docs-seeker` - Find technical docs
- `prompt-engineering` - Write LLM prompts
- `content-research-writer` - Research and write with citations

**Infrastructure & Tools**
- `mcp-builder` - Create MCP servers
- `mcp-management` - Discover/execute MCP tools
- `devops` - Cloudflare, Docker, GCP
- `databases` - MongoDB, PostgreSQL
