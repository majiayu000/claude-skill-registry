---
name: swarm
description: "Autonomous multi-agent workflow system for complex coding tasks. Use when the user requests non-trivial changes that would benefit from autonomous execution with built-in review gates. Ideal for refactoring modules, adding major features, migrating codebases, adding comprehensive test coverage, or any multi-step development task that can run autonomously. NOT for simple fixes, typos, or single-file changes."
---

# Swarm: Autonomous Multi-Agent Workflows

Execute complex coding tasks autonomously using multiple agents working from a coordinated plan.

## How It Works

1. **Interview** — Gather requirements and context from user
2. **Plan** — Create structured markdown plan with checkboxes and review gates
3. **Execute** — Spawn autonomous agents to work on the plan
4. **Complete** — Agents signal completion with `.done` files

## Workflow

### Step 1: Interview the User

When this skill is invoked, gather the information needed to create an effective plan:

**Required information:**
- **Goal**: What does "done" look like? (Be specific and measurable)
- **Context**: What files/directories are involved? Key constraints?
- **Test strategy**: What commands verify success? (e.g., `npm test`, `pytest`)
- **Plan location**: Where should the plan file be created?

**Interview questions:**

```
I'll help you set up an autonomous workflow for this task.

To create an effective plan, I need to understand:

1. What's the specific goal? What does "done" look like?
2. What files or directories are involved?
3. What tests or verification commands should agents run?
4. Where should I create the plan file? (e.g., PLAN.md, AUTH_REFACTOR.md)
```

Ask follow-up questions as needed to clarify scope, constraints, or success criteria.

### Step 2: Create the Plan

Use the template at `assets/PLAN_TEMPLATE.md` as a starting point. Customize it based on the user's requirements.

**Plan structure:**
- `## Goal` — One sentence defining completion criteria
- `## Context` — Codebase structure, key files, constraints
- `## Plan` — Phases with checkboxes for each step
- `## Agent Roles` — Review gates (Reviewer, Simplifier, Tester, Gatekeeper)
- `## Rules` — Behavioral constraints for agents
- `## Log` — Communication space for agents across iterations

**Critical components:**

1. **Checkboxes** — Every step must be checkable. Avoid prose.

2. **Review Gates** — Force perspective shifts at intervals:
   - **Reviewer (every 5th iteration)**: Fresh eyes on progress vs goal
   - **Simplifier (before final phase)**: Identify overengineering
   - **Tester (before final phase)**: Write and run tests
   - **Gatekeeper (before .done)**: Mandatory checklist before completion

3. **Gatekeeper Checklist** — Must include:
   - Commands to run with output (`npm test`, `git diff --stat`)
   - Explicit yes/no questions with evidence
   - GO/NO-GO decision with reasoning

4. **Log Section** — Agents append work here. Format:
   ```markdown
   ### Iteration N — YYYY-MM-DD HH:MM
   **Role:** [Worker / Reviewer / Simplifier / Tester / Gatekeeper]
   **What I did:** ...
   **Current state:** ...
   **Next agent should:** ...
   ```

**Write the plan file:**

```markdown
I've created the plan at [FILENAME]. Here's the structure:
- [Summarize the phases]
- [Note key review gates]
- [Highlight gatekeeper checklist]

The agents will work through this autonomously. Ready to start?
```

### Step 3: Execute with Autonomous Agents

Once the plan is written and user approves, run the swarm script.

**Execution mechanism:** The `swarm.sh` script spawns headless agent processes in a loop. By default, it uses Codex CLI in full-auto mode (`codex exec --full-auto`). You can use `--claude` to switch to Claude CLI. Each iteration runs the agent with the iteration number and plan file path. The plan file serves as shared state between iterations. Agents signal completion by creating a `.done` file.

**Running the swarm:**

Use the Bash tool with `run_in_background: true` to start the swarm:

```
Bash(run_in_background=true):
./path/to/swarm.sh .context/PLAN.md
```

This returns a `task_id`. Tell the user the swarm is starting, then use `TaskOutput` to wait for completion:

```
TaskOutput(task_id=<id>, block=true, timeout=600000)
```

This blocks until the swarm finishes (up to 10 minutes) without burning tokens on polling. The swarm typically completes in 2-10 iterations.

**Important:** The swarm script uses `--full-auto` for Codex (or `--dangerously-skip-permissions` for Claude) for headless agents. This is required for agents to edit files autonomously.

**Tell the user:**
```
Starting the swarm. Agents will work autonomously on the plan.

You can monitor progress by watching the plan file:
  tail -f .context/PLAN.md

The swarm will:
- Execute steps and check them off
- Log progress after each iteration
- Run review gates at intervals
- Complete the Gatekeeper checklist before finishing
- Create .done when all criteria are met

I'll let you know when it's complete.
```

**Available flags:**
- `--codex`: Use Codex CLI in full-auto mode (default)
- `--claude`: Use Claude CLI instead of Codex
- `--verbose` / `-v`: Show timing and log section after each iteration
- `--dry-run` / `-n`: Preview what would run without executing
- `--help` / `-h`: Show usage information

### Step 4: Report Completion

**When TaskOutput returns:**

1. Check if `.done` file exists (success) or max iterations reached (needs intervention)
2. Read the last ~30 lines of the plan file to see the final Log entry
3. Report to user:

**On success:**
```
The swarm has completed!

Summary:
- [Number] iterations executed
- Gatekeeper verification: [Passed]

Final checks from agents:
- Tests: [status from log]
- Changes: [git diff summary from log]

The code is ready for your review. Check [PLAN_FILE] for the full execution log.
```

**On max iterations (no .done file):**
```
The swarm reached max iterations without completing.

Last status from agents:
[Summary from final log entry]

Would you like me to:
1. Resume the swarm for more iterations
2. Review the plan and identify blockers
3. Take over and complete manually
```

**On NO-GO decision:**
```
The agents completed but identified issues:
[List issues from Gatekeeper log]

Would you like me to:
1. Spawn another iteration to address these
2. Review and fix the issues manually
3. Adjust the plan and restart
```

## Plan Quality Guidelines

### Good Plans Have:

✅ **Specific goal**: "Convert auth/ to async/await, tests pass, >80% coverage"
❌ **Vague goal**: "Improve the auth system"

✅ **Discrete checkboxes**: "- [ ] Convert tokens.js to async/await"
❌ **Prose paragraphs**: "The agent should convert files to async/await..."

✅ **Mandatory review gates**: Reviewer every 5th iteration, Gatekeeper before .done
❌ **No review**: Just implementation steps, agents tunnel-vision

✅ **Explicit Gatekeeper checks**: "Run `npm test` and paste output"
❌ **Fuzzy completion**: "When it works, mark it done"

✅ **Log section**: Agents append progress, communicate across iterations
❌ **No log**: Agents have no memory, repeat work

### Example Plan

See `assets/PLAN_TEMPLATE.md` for a complete template.

## When to Use This Skill

**Use for:**
- Refactoring modules or subsystems
- Adding authentication/authorization
- Migrating from X to Y (callbacks→async, REST→GraphQL)
- Adding comprehensive test coverage
- Multi-file feature implementations
- Codebase modernization tasks

**Don't use for:**
- Single-file changes
- Typo fixes
- Simple CRUD additions
- Exploratory "understand the codebase" tasks
- Tasks that need frequent user input

## Tips

**Start with clear goals.** The more specific the Goal section, the better agents can self-correct.

**Trust the review gates.** They prevent tunnel vision. Don't skip them to save iterations.

**Gatekeeper is critical.** Agents are optimistic and will complete early. Gatekeeper forces verification.

**Watch the Log.** If agents repeat the same work 3+ times, the plan needs clarification.

**Git commits as checkpoints.** Add to Rules: "Commit after each phase." Creates restore points.

## Resources

### assets/PLAN_TEMPLATE.md
Template for creating autonomous workflow plans. Copy and customize based on user requirements.

### assets/swarm.sh
Bash script that runs the iteration loop. Usage:
```bash
./swarm.sh [OPTIONS] PLAN_FILE.md
```

Options:
- `--codex`: Use Codex CLI in full-auto mode (default)
- `--claude`: Use Claude CLI instead of Codex
- `-n, --dry-run`: Show what would happen without running agents
- `-v, --verbose`: Print timing and log section after each iteration
- `-h, --help`: Show help message

Set `MAX_ITERATIONS` env var to override default (20).

### assets/test_swarm.sh
Test script for swarm.sh. Run to verify the script works:
```bash
./test_swarm.sh
```
