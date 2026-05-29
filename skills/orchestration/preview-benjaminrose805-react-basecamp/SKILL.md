---
name: preview
description: Display execution plan preview before running commands, allowing user confirmation or modification.
---

# Preview Skill

Display execution plan preview before running commands, allowing user confirmation or modification.

## Mode Check

**CRITICAL:** Check mode before displaying preview.

```typescript
if (mode === "basic") {
  // Skip preview entirely
  // Execute command immediately
  return;
}
// Continue with preview display
```

## When Used

| Command      | Preview Content                             |
| ------------ | ------------------------------------------- |
| `/start`     | Worktree path, branch name, next steps      |
| `/plan`      | Mode (define/reconcile), phases, sub-agents |
| `/implement` | Spec reference, stages, agents, TDD phases  |
| `/ship`      | Commit, PR, CI, CodeRabbit stages           |

**NOT used by:** `/guide` (informational), `/mode` (immediate switch)

## Preview Data Structure

```typescript
interface ExecutionPreview {
  // Command context
  command: string; // Original command (e.g., "/implement login form")
  detected: string; // What was detected (e.g., "Frontend component")
  scope: string; // Scope description (e.g., "Login form UI")

  // Routing info
  route: {
    type: "agent" | "workflow";
    name: string; // Agent or workflow name
    reason: string; // Why this route was chosen
  };

  // Execution plan
  stages: Stage[];

  // Metadata
  tools: string[]; // MCP servers/CLI tools that will be used
  flags?: string[]; // Any flags that modify behavior
}

interface Stage {
  number: number;
  name: string; // e.g., "RESEARCH", "BUILD", "VERIFY"
  agent?: string; // Agent handling this stage
  subAgents: SubAgentPlan[];
  status: "pending" | "conditional"; // conditional = depends on prior stage
}

interface SubAgentPlan {
  name: string; // e.g., "ui-researcher"
  model: "Opus" | "Sonnet" | "Haiku";
  tasks: string[]; // Planned tasks
  parallel?: boolean; // True if runs in parallel with siblings
}
```

---

## Display Formats

### /start Preview

```text
┌─────────────────────────────────────────────────────────────────┐
│  /start user-authentication                                     │
├─────────────────────────────────────────────────────────────────┤
│  Creating new workspace for: user-authentication                │
│                                                                 │
│  ACTIONS                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 1. CREATE WORKTREE                                          ││
│  │    Path: ../project-user-authentication                     ││
│  │    Branch: feature/user-authentication                      ││
│  │                                                             ││
│  │ 2. NEXT STEPS                                               ││
│  │    → Restart session in new worktree                        ││
│  │    → Run /plan to begin designing                           ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  [Enter] Run  [e] Edit name  [Esc] Cancel                       │
└─────────────────────────────────────────────────────────────────┘
```

### /plan Preview (Define Mode)

```text
┌─────────────────────────────────────────────────────────────────┐
│  /plan user-authentication                                      │
├─────────────────────────────────────────────────────────────────┤
│  Mode: Define                                                   │
│  Feature: User authentication with email/password               │
│                                                                 │
│  PHASES                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 1. RESEARCH         domain-researcher      Opus             ││
│  │    □ Search existing auth patterns                          ││
│  │    □ Check for conflicts                                    ││
│  │    □ Identify integration points                            ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 2. WRITE            domain-writer          Sonnet           ││
│  │    □ Create requirements.md (EARS format)                   ││
│  │    □ Create design.md (architecture)                        ││
│  │    □ Create tasks.md (phased work items)                    ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 3. VALIDATE         quality-validator      Haiku            ││
│  │    □ Verify EARS compliance                                 ││
│  │    □ Check acceptance criteria                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Output: specs/user-authentication/                             │
│                                                                 │
│  [Enter] Run  [e] Edit  [?] Details  [Esc] Cancel               │
└─────────────────────────────────────────────────────────────────┘
```

### /plan Preview (Reconcile Mode)

```text
┌─────────────────────────────────────────────────────────────────┐
│  /plan (reconcile PR #42)                                       │
├─────────────────────────────────────────────────────────────────┤
│  Mode: Reconcile                                                │
│  PR: #42 - Add user authentication                              │
│  CodeRabbit comments: 3                                         │
│                                                                 │
│  ISSUES TO ADDRESS                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 1. [Security] Use bcrypt, not SHA256                        ││
│  │ 2. [Performance] Add index on email column                  ││
│  │ 3. [Style] Use early returns in validatePassword()          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  PHASES                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 1. ANALYZE          domain-researcher      Opus             ││
│  │    □ Review each CodeRabbit comment                         ││
│  │    □ Identify affected files                                ││
│  │    □ Assess fix complexity                                  ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 2. PLAN             domain-writer          Sonnet           ││
│  │    □ Create fix plan with tasks                             ││
│  │    □ Prioritize by severity                                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  [Enter] Run  [e] Edit  [?] Details  [Esc] Cancel               │
└─────────────────────────────────────────────────────────────────┘
```

### /implement Preview

```text
┌─────────────────────────────────────────────────────────────────┐
│  /implement user-authentication                                 │
├─────────────────────────────────────────────────────────────────┤
│  Spec: specs/user-authentication/ (approved)                    │
│  Tasks: 12 across 4 phases                                      │
│  TDD: Enabled (red → green → refactor)                          │
│                                                                 │
│  STAGE 1: DATABASE SCHEMA                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Agent: code-agent                                           ││
│  │                                                             ││
│  │ 1. RESEARCH         code-researcher        Opus             ││
│  │    □ Find existing DB patterns                              ││
│  │ 2. TDD-RED          code-writer            Sonnet           ││
│  │    □ Write failing tests                                    ││
│  │ 3. TDD-GREEN        code-writer            Sonnet           ││
│  │    □ Implement to pass tests                                ││
│  │ 4. VALIDATE         code-validator         Haiku            ││
│  │    □ Verify tests pass                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  STAGE 2: AUTH API                                              │
│  └─ [Same pattern with code-agent]                              │
│                                                                 │
│  STAGE 3: UI COMPONENTS                                         │
│  └─ [Same pattern with ui-agent]                                │
│                                                                 │
│  STAGE 4: FINAL VERIFICATION                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Agent: check-agent (parallel)              Haiku            ││
│  │    ⊕ build-checker                                          ││
│  │    ⊕ type-checker                                           ││
│  │    ⊕ lint-checker                                           ││
│  │    ⊕ test-runner                                            ││
│  │    ⊕ security-scanner                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Tools: cclsp, context7, next-devtools                          │
│                                                                 │
│  [Enter] Run  [e] Edit  [?] Details  [Esc] Cancel               │
└─────────────────────────────────────────────────────────────────┘
```

### /ship Preview

```text
┌─────────────────────────────────────────────────────────────────┐
│  /ship                                                          │
├─────────────────────────────────────────────────────────────────┤
│  Feature: user-authentication                                   │
│  Branch: feature/user-authentication                            │
│  Changes: 8 files, +342 -12                                     │
│                                                                 │
│  STAGES                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 1. COMMIT                                                   ││
│  │    Agent: git-agent                                         ││
│  │    ├─ change-analyzer (Sonnet) - Generate message           ││
│  │    └─ git-executor (Haiku) - Create commit                  ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 2. CREATE PR                                                ││
│  │    Agent: git-agent                                         ││
│  │    ├─ pr-analyzer (Sonnet) - Generate description           ││
│  │    └─ git-executor (Haiku) - Create PR via gh CLI           ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 3. WAIT FOR CI                                              ││
│  │    □ Monitor GitHub Actions                                 ││
│  │    □ Report pass/fail                                       ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 4. WAIT FOR CODERABBIT                                      ││
│  │    □ Monitor CodeRabbit review                              ││
│  │    □ Report comments or approval                            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  [Enter] Run  [e] Edit  [Esc] Cancel                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## User Interactions

### Keyboard Controls

| Key     | Action  | Description                            |
| ------- | ------- | -------------------------------------- |
| `Enter` | Run     | Execute the plan as shown              |
| `e`     | Edit    | Modify scope or options                |
| `?`     | Details | Show expanded details (tools, context) |
| `Esc`   | Cancel  | Abort without executing                |

### Edit Mode

When user presses `e`:

```text
┌─────────────────────────────────────────────────────────────────┐
│  Edit Execution Plan                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Scope: login form                                              │
│  ─────────────────                                              │
│  Current: "Login form UI"                                       │
│  New scope: _                                                   │
│                                                                 │
│  Options:                                                       │
│  ─────────                                                      │
│  [ ] Skip research phase                                        │
│  [ ] Skip validation phase                                      │
│  [x] Include accessibility audit                                │
│                                                                 │
│  [Enter] Apply  [Esc] Cancel                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Details View

When user presses `?`:

```text
┌─────────────────────────────────────────────────────────────────┐
│  Execution Details                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MCP Servers:                                                   │
│  ─────────────                                                  │
│  • cclsp - TypeScript LSP for code navigation                   │
│  • shadcn - Component registry lookup                           │
│  • playwright - E2E and accessibility testing                   │
│  • context7 - Library documentation lookup                      │
│                                                                 │
│  CLI Tools:                                                     │
│  ──────────                                                     │
│  • pnpm test - Run Vitest tests                                 │
│  • pnpm typecheck - TypeScript checking                         │
│  • pnpm lint - ESLint checking                                  │
│                                                                 │
│  Spec Reference:                                                │
│  ───────────────                                                │
│  • specs/login-form/design.md                                   │
│                                                                 │
│  Estimated Context Usage:                                       │
│  ─────────────────────────                                      │
│  • Research: ~15% (Opus)                                        │
│  • Build: ~50% (Sonnet)                                         │
│  • Validate: ~10% (Haiku)                                       │
│                                                                 │
│  [Any key] Back                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Automation Flag

### Skip Preview with --yes

```bash
/implement --yes    # Execute immediately without preview
/ship --yes         # Ship without confirmation
/start auth --yes   # Create worktree without preview
```

When `--yes` flag is present:

1. Skip preview display
2. Use default options
3. Execute immediately
4. Still show progress during execution

### When to Use --yes

| Scenario             | Recommended |
| -------------------- | ----------- |
| CI/CD automation     | Yes         |
| Scripted workflows   | Yes         |
| Repetitive tasks     | Yes         |
| New/unfamiliar tasks | No          |
| Complex features     | No          |
| Production changes   | No          |

---

## Preview Generation

### Algorithm

```typescript
async function generatePreview(
  command: string,
  args: string
): Promise<ExecutionPreview> {
  // 1. Parse command
  const { type, target, flags } = parseCommand(command, args);

  // 2. Route command
  const routing = await route(type, target);

  // 3. Build preview based on route type
  if (routing.type === "agent") {
    return buildAgentPreview(routing.agent, target);
  } else {
    return buildWorkflowPreview(routing.workflow, target);
  }
}

function buildAgentPreview(agent: Agent, target: string): ExecutionPreview {
  return {
    command: `/${agent.command} ${target}`,
    detected: agent.detectType(target),
    scope: target,
    route: {
      type: "agent",
      name: agent.name,
      reason: agent.routingReason,
    },
    stages: agent.phases.map((phase) => ({
      number: phase.order,
      name: phase.name,
      agent: agent.name,
      subAgents: [
        {
          name: phase.subAgent,
          model: phase.model,
          tasks: phase.defaultTasks,
        },
      ],
      status: "pending",
    })),
    tools: agent.tools,
  };
}
```

---

## Error Handling

| Scenario                | Handling                                   |
| ----------------------- | ------------------------------------------ |
| Routing fails           | Show error, suggest alternatives           |
| Spec not found          | Show warning, proceed with keyword routing |
| Invalid edit input      | Show validation error, re-prompt           |
| User cancels            | Exit gracefully, no execution              |
| Preview generation fail | Fall back to simple text description       |

---

## Output

### Preview Accepted

```markdown
## Preview: ACCEPTED

Executing plan as shown...
(Switches to progress display)
```

### Preview Edited

```markdown
## Preview: MODIFIED

Changes:

- Scope: "login form" → "login form with 2FA"
- Skipped: research phase

Executing modified plan...
```

### Preview Cancelled

```markdown
## Preview: CANCELLED

No changes made.
```
