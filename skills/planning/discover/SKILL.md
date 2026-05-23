---
name: discover
description: Discovery-first development workflow. Use BEFORE creating worktrees for any non-trivial feature. Explores requirements through questions, proposes approaches, validates design incrementally, and generates implementation plans with verification commands.
---

# Discovery Skill

Turn ideas into validated designs and executable plans through structured dialogue.

## When to Use

**Always use /discover before worktree creation when:**

- Adding new features or functionality
- Refactoring significant code
- Any task touching 3+ files
- Requirements are unclear or have multiple valid approaches

**Skip discovery for:**

- Single-file bug fixes
- Typo corrections
- Simple configuration changes
- Tasks where the user provides explicit, detailed instructions

## Overview

The discovery process has three phases:

```
Phase 1: Understand     → Ask questions, explore codebase
Phase 2: Design         → Propose approaches, validate design
Phase 3: Plan           → Write executable implementation plan
```

**Key principles:**

- One question at a time (never overwhelm)
- Multiple choice when possible (easier to answer)
- Validate design in sections (200-300 words each)
- YAGNI ruthlessly (remove unnecessary complexity)
- Evidence before claims (verification commands for every task)

---

## Phase 1: Understand

### Step 1: Explore Context First

Before asking any questions, explore the codebase to understand:

- Existing patterns that relate to this feature
- Files that will likely need changes
- Similar implementations for reference

```
Use Task tool with subagent_type=Explore to search:
- Related files and patterns
- Existing similar features
- Architecture and conventions
```

### Step 2: Ask Clarifying Questions

Use `AskUserQuestion` tool to ask ONE question at a time.

**Question design principles:**

- Multiple choice preferred (2-4 options)
- Lead with your recommendation (add "(Recommended)" to label)
- Include "Other" option implicitly (tool adds it)
- Keep questions focused and specific

**Example questions:**

```javascript
// Good: Specific, multiple choice, has recommendation
AskUserQuestion({
  questions: [{
    question: "Should webhooks support retry on failure?",
    header: "Retry behavior",
    options: [
      { label: "Yes, with exponential backoff (Recommended)", description: "Retries 3 times with 1s, 5s, 30s delays" },
      { label: "Yes, with fixed interval", description: "Retries 3 times with 30s delay each" },
      { label: "No retries", description: "Single delivery attempt, failures logged only" }
    ],
    multiSelect: false
  }]
})

// Bad: Too many questions at once
AskUserQuestion({
  questions: [
    { question: "Retry behavior?", ... },
    { question: "Payload format?", ... },
    { question: "Authentication?", ... },  // Too many!
    { question: "Rate limiting?", ... }
  ]
})
```

**Question topics to cover:**

1. Core requirements (what must it do?)
2. Scope boundaries (what should it NOT do?)
3. Integration points (what does it connect to?)
4. Success criteria (how do we know it's done?)

### Step 3: Identify When You Have Enough

Stop asking when you can confidently:

- Describe the feature in one paragraph
- List all files that need changes
- Explain why this approach over alternatives

---

## Phase 2: Design

### Step 4: Propose Approaches

Present 2-3 different approaches with trade-offs:

```markdown
## Approach Options

### Option A: Event-driven webhooks (Recommended)

**How it works:** Events emit to a queue, webhook service consumes and delivers.

**Pros:**

- Decoupled from main flow
- Easy to add retry logic
- Scalable

**Cons:**

- More infrastructure (queue)
- Eventual consistency

**I recommend this because:** It matches our existing event patterns and
keeps webhook delivery from blocking core operations.

### Option B: Synchronous webhooks

**How it works:** Direct HTTP call during event handling.

**Pros:**

- Simpler, no queue needed
- Immediate feedback

**Cons:**

- Blocks event processing
- No built-in retry
- Harder to scale
```

Ask user to confirm approach:

```javascript
AskUserQuestion({
  questions: [
    {
      question: 'Which approach should we use?',
      header: 'Approach',
      options: [
        {
          label: 'Option A: Event-driven (Recommended)',
          description: 'Queue-based delivery with retry support',
        },
        { label: 'Option B: Synchronous', description: 'Direct HTTP calls, simpler but blocking' },
      ],
      multiSelect: false,
    },
  ],
});
```

### Step 5: Present Design in Sections

After approach is selected, present the detailed design in **200-300 word sections**.

After each section, ask: "Does this section look right?"

**Sections to cover:**

1. Data model (schemas, tables)
2. API surface (endpoints, payloads)
3. Core logic (algorithms, flows)
4. Error handling (failure modes, recovery)
5. Testing approach (what to test, how)

```javascript
// After presenting a section
AskUserQuestion({
  questions: [
    {
      question: 'Does this data model design look right?',
      header: 'Data model',
      options: [
        { label: 'Yes, proceed', description: 'Move to the next section' },
        { label: 'Needs adjustment', description: 'I have feedback on this section' },
      ],
      multiSelect: false,
    },
  ],
});
```

---

## Phase 3: Plan

### Step 6: Write Implementation Plan

Create a plan document at:

```
docs/plans/YYYY-MM-DD-<feature-name>.md
```

**Plan structure:**

````markdown
# [Feature Name] Implementation Plan

**Goal:** One sentence describing what this builds
**Architecture:** 2-3 sentences about the approach
**Key decisions:**

- Decision 1 and why
- Decision 2 and why

---

## Tasks

### Task 1: [Component Name]

**Independent:** Yes/No (if No, list dependencies)
**Estimated scope:** Small (1-2 files) / Medium (3-5 files) / Large (6+ files)

**Files:**

- Create: `exact/path/to/new-file.ts`
- Modify: `exact/path/to/existing.ts` (lines 45-67)
- Test: `exact/path/to/test-file.test.ts`

**Steps:**

1. Write failing test for [specific behavior]
   ```typescript
   // Exact test code
   ```
````

2. Run: `pnpm test path/to/test` → Expect: FAIL with "[specific error]"
3. Implement [specific functionality]
   ```typescript
   // Key implementation code (not everything, but enough to guide)
   ```
4. Run: `pnpm test path/to/test` → Expect: PASS
5. Commit: `git commit -m "feat: add [component]"`

**Verification:** `pnpm test path/to/test --grep "specific test"`
**Acceptance criteria:**

- [ ] Test exists and passes
- [ ] [Specific behavior] works correctly
- [ ] No TypeScript errors

---

### Task 2: ...

---

## Dependency Graph

```
Task 1 (independent) ──┐
                       ├──► Task 3 ──► Task 4
Task 2 (independent) ──┘
```

**Parallelizable:** Tasks 1, 2
**Sequential:** Task 3 (after 1,2), Task 4 (after 3)

---

## Verification Summary

| Task | Verification Command                             | Expected Output |
| ---- | ------------------------------------------------ | --------------- |
| 1    | `pnpm test packages/core --grep WebhookConfig`   | All tests pass  |
| 2    | `pnpm test packages/core --grep WebhookDelivery` | All tests pass  |
| 3    | `pnpm build`                                     | Exit code 0     |
| 4    | `pnpm test:e2e --grep webhook`                   | E2E tests pass  |

````

### Step 7: Handoff to Worktree

After plan is written, offer to create worktree:

```javascript
AskUserQuestion({
  questions: [{
    question: "Plan saved to docs/plans/2026-02-01-webhook-support.md. Ready to create worktree?",
    header: "Create worktree",
    options: [
      { label: "Yes, create worktree now (Recommended)", description: "Creates isolated worktree with plan already loaded" },
      { label: "No, I'll review the plan first", description: "You can create worktree later with /worktree-manager" },
      { label: "Make changes to the plan", description: "Edit the plan before proceeding" }
    ],
    multiSelect: false
  }]
})
````

If user says yes, invoke worktree creation:

```bash
# Using Skill tool
Skill(skill: 'claude-worktree-manager', args: 'create <feature-name> --plan docs/plans/YYYY-MM-DD-<feature-name>.md')
```

---

## Example Session

```
User: /discover add webhook support for integrations

Agent: [Explores codebase - finds existing integration patterns, event system]

Agent: [AskUserQuestion]
"What events should trigger webhook delivery?"
□ Integration lifecycle (connected, disconnected) (Recommended)
□ Agent actions (tool calls, completions)
□ All events (comprehensive but noisy)

User: "Integration lifecycle"

Agent: [AskUserQuestion]
"Should webhooks support retry on failure?"
□ Yes, with exponential backoff (Recommended)
□ No retries
...

[After enough questions]

Agent: "Based on our discussion, here are two approaches..."
[Presents options, user picks one]

Agent: "Let me walk through the design. First, the data model..."
[Presents 250 words on data model]
"Does this look right?"

User: "Yes, proceed"

Agent: [Continues through all sections]

Agent: "Writing implementation plan..."
[Writes docs/plans/2026-02-01-webhook-support.md]

Agent: [AskUserQuestion]
"Plan complete. Ready to create worktree?"
□ Yes, create worktree now

User: "Yes"

Agent: [Creates worktree with plan]
"Worktree created at ~/claude-worktrees/orient/webhook-support-1234567890
The worktree agent will read the plan at docs/plans/2026-02-01-webhook-support.md
and execute tasks with verification."
```

---

## Integration with Other Skills

**After discovery:**

- `claude-worktree-manager` - Creates isolated worktree with plan
- `worktree-operations` - Guides development in worktree

**Plan execution (in worktree):**

- Worktree agent reads plan
- Executes tasks with two-stage review
- Mandatory verification before completion claims
- Batch checkpoints for human feedback

---

## Custom Agents for Specialized Tasks

For certain task types, recommend specialized agents in `.claude/agents/` instead of general worktrees:

| Task Type          | Recommended Agent      | When to Use                                               |
| ------------------ | ---------------------- | --------------------------------------------------------- |
| Code review        | `/agent code-reviewer` | PR reviews, pattern enforcement, code audits              |
| Writing tests      | `/agent test-writer`   | Adding tests, improving coverage, debugging test failures |
| Database changes   | `/agent migration`     | Schema changes, new tables, column modifications          |
| OAuth integrations | `/agent integration`   | Adding new services (Linear, Notion, GitHub, etc.)        |
| Documentation      | `/agent docs`          | README updates, skill creation, API docs                  |

**When to recommend agents vs worktrees:**

- **Use agents** for focused, single-purpose tasks that match an agent's specialty
- **Use worktrees** for larger features that span multiple concerns

**Example recommendations in discovery:**

```javascript
// If user wants to add tests
"For adding tests, I recommend using `/agent test-writer` which is
specialized for writing and running tests with Vitest patterns."

// If user wants schema changes
"Database migrations require extra care. I recommend `/agent migration`
which uses Opus model and has safety checks for destructive operations."

// If user wants a larger feature with multiple concerns
"This feature involves schema changes, new API endpoints, and tests.
Let's create a full implementation plan and use a worktree."
```

---

## Anti-Patterns

**Don't:**

- Ask multiple questions at once
- Skip codebase exploration
- Present design all at once (validate in sections)
- Write vague tasks ("implement webhook handling")
- Omit verification commands
- Assume requirements (ask if unclear)

**Do:**

- One question at a time
- Explore before asking
- Validate design incrementally
- Write specific, executable tasks
- Include exact verification commands
- Ask until confident
