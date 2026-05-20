---
name: aim-parzival-team-builder
description: Design agent team structure for parallel work execution via Claude Code teams
context: fork
---

# Parzival Team Builder

**Purpose**: Analyze work to be parallelized, design the appropriate team structure (2-tier or 3-tier), and produce a team design document ready for execution via [DA] Dispatch Agent.

**Note**: This skill replaced the `session/team-prompt/` workflow (deprecated PLAN-017, 2026-03-10). Parzival designs teams here, then executes them via the agent-dispatch workflow. Parzival activates agents himself — the user does not run agents.

---

## Team Design Process

### Step 1: Preflight Analysis

1. Read the work to be parallelized (plan, spec, or user description)
2. Identify independent work units that can run concurrently
3. Check for file ownership conflicts between units
4. Determine tier selection:

| Scenario | Tier | Reasoning |
|----------|------|-----------|
| Single task | Subagent (no team) | Overhead not justified |
| 2-6 parallel tasks, single review | 2-Tier | Simple coordination |
| 3+ domains, multi-task per domain, domain-level review | 3-Tier | Complex coordination |

### Step 2: Team Composition

1. Assign agent roles from available BMAD agents (analyst, pm, architect, dev, sm, ux-designer)
2. Size teams: 3-5 teammates recommended, 5-6 tasks per teammate for productive sizing
3. **Assign agent identity**: Each agent MUST have a unique `AI_MEMORY_AGENT_ID`:
   - **Domain-named** (recommended): `dev-auth`, `dev-api`, `review-auth` — same agent always works on same domain
   - **Numbered** (for generic work): `dev-1`, `dev-2`, `review-1` — interchangeable agents
   - **Single-instance**: `pm`, `architect` — use role name directly
   - Same `AI_MEMORY_AGENT_ID` across sessions enables cross-session memory accumulation
   - Naming rules: domain-named agents always work the same domain/files across sessions; numbered agents are interchangeable for generic parallel work; single-instance agents use role name directly
4. Select models: Sonnet for implementation, Opus for complex architecture/review

### Step 3: File Ownership Map

1. Map every file that will be modified to exactly one agent
2. NO file ownership overlap between agents at any level
3. Cross-cutting concerns use interface contracts
4. Verify ownership map has zero conflicts before proceeding

### Step 4: Context Block Assembly

For each agent, prepare:
- ROLE: Agent type and assigned identity (AI_MEMORY_AGENT_ID)
- TASK: Specific work items with acceptance criteria
- FILES: Owned files (absolute paths)
- CONSTRAINTS: What NOT to touch
- DONE WHEN: Explicit completion criteria

### Step 5: Conflict Avoidance Strategy

Select from ranked strategies (highest effectiveness first):
1. **Git Worktree Isolation** — Each worker gets independent filesystem copy
2. **Exclusive File Ownership** — Enforced by Step 3 ownership map
3. **Directory Partitioning** — Workers own directories, not individual files
4. **Interface Contracts** — For workers producing compatible code
5. **Merge-on-Green** — Code merges to main only when all tests pass

**NEVER use file locking** — collapsed 20 agents to throughput of 2-3 in production testing.

**WSL2 note**: In-process mode recommended for WSL2 environments. tmux works best on macOS.

### Step 6: Pre-Delivery Review

Before handing to [DA] for execution, verify:
- [ ] All work units assigned to exactly one agent
- [ ] No file ownership conflicts
- [ ] Each agent has clear DONE WHEN criteria
- [ ] Each agent has a unique AI_MEMORY_AGENT_ID assigned
- [ ] Team size is 3-5 (split if larger)
- [ ] Conflict avoidance strategy selected and documented
- [ ] Context blocks are complete (no placeholders or TBDs)

---

## Anti-Patterns

- Never force 3-tier hierarchy when 2-tier suffices
- Never allow file ownership overlap between agents
- Never create teams without reading the codebase to verify boundaries
- Never skip the pre-delivery review
- Never let managers implement anything — they orchestrate workers only
- Never embed more than 4 worker prompts in a single manager context
- Never allow unbounded review loops — hard cap at 3 cycles, then escalate

---

## Output

The team design document feeds directly into [DA] Dispatch Agent for execution.
Parzival activates all agents himself via Claude Code teams — the user does not run agents.

**MANDATORY ROUTING**: After user approves the team design, Parzival MUST immediately
load and execute `{workflows_path}/cycles/agent-dispatch/workflow.md` starting at
step-02 (team creation) — the instruction preparation (step-01) is already complete
from the context blocks produced above. Execute step-02 once per agent in the team
design, spawning teammates in parallel where the design specifies parallel execution.
