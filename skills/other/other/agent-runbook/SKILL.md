---
name: agent-runbook
description: Create step-by-step executable runbooks for AI agents. Use when building automation scripts, setup guides, or multi-step workflows that agents can execute autonomously.
---

# Agent Runbook

## Core Principle

**Instructions as Code. Executable, repeatable, autonomous.**

A runbook is a step-by-step guide that an AI agent can execute without human intervention (except for explicit decision points). The agent reads it and does the work.

---

## When to Use

Use this skill when:
- Creating setup/installation guides for agents
- Automating multi-step workflows
- Building onboarding scripts
- Documenting repeatable processes
- Creating self-service automation

---

## Runbook Anatomy

Every runbook follows this structure:

```markdown
# [Title] - [Purpose]

**Last Updated:** [Date]
**Version:** [X.Y]

---

## 🤖 For AI Coding Agents

[Brief description of what this runbook does]

**Your goal:** [Clear statement of the end state]

---

## Step 0: Prerequisites Check

[Commands to verify environment is ready]

---

## Step 1-N: Execution Steps

[Each step with commands + decision points]

---

## Verification

[How to confirm success]

---

## Troubleshooting

[Common issues and solutions]
```

---

## Step 0: Gather Requirements

**Ask the user:**

"What type of runbook do you need?"
- **Setup/Installation** → Environment configuration, tool installation
- **Workflow/Process** → Multi-step business or dev process
- **Migration/Upgrade** → Moving from one state to another
- **Maintenance/Cleanup** → Periodic tasks, housekeeping

**Record:** `[RUNBOOK_TYPE]`

"What is the runbook's purpose? (one sentence)"
**Record:** `[PURPOSE]`

"What are the key decision points where the agent should ask the user?"
**Record:** `[DECISION_POINTS]`

---

## Step 1: Create File Structure

```bash
# Determine location
RUNBOOK_NAME="[snake_case_name]"

# Option A: Standalone runbook in project root
touch "${RUNBOOK_NAME}.md"

# Option B: Runbook as a skill (reusable)
mkdir -p .claude/skills/[category]/${RUNBOOK_NAME}
touch .claude/skills/[category]/${RUNBOOK_NAME}/SKILL.md
```

---

## Step 2: Write Header Section

```markdown
# [Title] - [Subtitle]

**Last Updated:** [Current Date]
**Version:** 1.0

---

## 🤖 For AI Coding Agents

This file contains **complete instructions** for [PURPOSE].
You (the AI agent) should execute these steps autonomously.

**Your goal:** [END_STATE - what success looks like]

---
```

**Key elements:**
- Clear title indicating what the runbook does
- Version for tracking changes
- Explicit statement that this is for agents
- Goal statement (the "done" criteria)

---

## Step 3: Write Prerequisites Check

```markdown
## Step 0: Prerequisites Check

Run these commands and record results:

\`\`\`bash
# Check [tool1]
[command] --version

# Check [tool2]  
[command] --version

# Check current state
[diagnostic command]
\`\`\`

**If [condition]:** [Tell user what to do]
**If [other condition]:** [Alternative path]
```

**Pattern:**
1. List all required tools/conditions
2. Provide check commands
3. Define what to do if checks fail
4. Never assume - always verify

---

## Step 4: Write Execution Steps

Each step follows this pattern:

```markdown
## Step N: [Action Title]

**Agent Instructions:** [Brief context for why this step exists]

### [Sub-action if needed]

\`\`\`bash
# Comments explaining what this does
[command]
[command]
\`\`\`

### Decision Point (if applicable)

**Ask the user:**

"[Question requiring user input]?"
- **Option A** → [What happens if chosen]
- **Option B** → [What happens if chosen]
- **Option C** → [What happens if chosen]

**Record answer:** `[VARIABLE_NAME]`

### Conditional Execution

**If [VARIABLE_NAME] = "Option A":**

\`\`\`bash
[commands for this path]
\`\`\`

**If [VARIABLE_NAME] = "Option B":**

\`\`\`bash
[commands for this path]
\`\`\`
```

**Best practices:**
- One logical action per step
- Commands in code blocks (executable)
- Decision points clearly marked with "Ask the user:"
- Variables in `[BRACKETS]` or backticks
- Conditional paths clearly labeled

---

## Step 5: Write Verification Section

```markdown
## Verification

**Run verification checks:**

\`\`\`bash
# 1. Check [first thing]
[command]

# 2. Check [second thing]
[command]

# 3. Check [third thing]
[command]
\`\`\`

**Success criteria:**

- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

**If all checks pass:** [Success message] 🎉
```

**Key elements:**
- Concrete verification commands
- Checklist with ✅ markers
- Clear success/failure criteria

---

## Step 6: Write Troubleshooting Section

```markdown
## Troubleshooting

### Issue: [Problem description]

**Solution:**

\`\`\`bash
[fix commands]
\`\`\`

### Issue: [Another problem]

**Solution:**

[Explanation and fix]
```

**Include:**
- Common failure modes
- Error messages users might see
- Copy-paste solutions
- Links to external docs if needed

---

## Step 7: Add Reference Section (Optional)

```markdown
## Reference

**Full Documentation:** [URL]

**Related Resources:**
- [Resource 1]
- [Resource 2]

**Available Options:**
- **Option A:** [Description]
- **Option B:** [Description]

---

## Support

**Issues?** [Where to report]
**Questions?** [Where to ask]
```

---

## Runbook Design Patterns

### Pattern 1: Detection → Ask → Execute

```markdown
### Automatic Detection

\`\`\`bash
# Detect current state
if [ -d ".git" ]; then
  echo "STATE=git-initialized"
else
  echo "STATE=no-git"
fi
\`\`\`

### Ask User to Confirm

**Present the user with a question:**

"We detected [STATE]. Is this correct?"
- **Yes** → Continue with detected settings
- **No, change to X** → Use alternative

**Record answer:** `[CONFIRMED_STATE]`

### Execute Based on State

**If [CONFIRMED_STATE] = "git-initialized":**
[commands]
```

### Pattern 2: Gather All → Execute All

```markdown
## Configuration (Answer All Questions First)

**Q1:** "What is your project name?"
**Record:** `[PROJECT_NAME]`

**Q2:** "Which framework?"
- React
- Vue
- Svelte

**Record:** `[FRAMEWORK]`

**Q3:** "Include testing?"
- Yes
- No

**Record:** `[INCLUDE_TESTS]`

---

## Execution (Now Run Everything)

\`\`\`bash
# Using recorded values
npx create-[FRAMEWORK]-app [PROJECT_NAME]

# If [INCLUDE_TESTS] = yes
npm install --save-dev jest
\`\`\`
```

### Pattern 3: Idempotent Steps

```markdown
## Step N: Install Package

\`\`\`bash
# Check if already installed
if ! command -v [tool] &>/dev/null; then
  echo "Installing [tool]..."
  [install command]
else
  echo "[tool] already installed, skipping"
fi
\`\`\`
```

---

## Quick Reference

```
Runbook Structure:
├── Header (title, version, goal)
├── Step 0: Prerequisites
├── Steps 1-N: Execution
│   ├── Commands (in code blocks)
│   ├── Decision Points ("Ask the user:")
│   └── Conditional Paths (If X = Y:)
├── Verification (success criteria)
├── Troubleshooting (common issues)
└── Reference (optional)

Key Markers:
  **Agent Instructions:**  → Context for the agent
  **Ask the user:**        → Decision point (pause for input)
  **Record:**              → Store user's answer
  **If [VAR] = "X":**      → Conditional execution
  ✅                       → Success criterion
  🎉                       → Completion celebration

Variables:
  [VARIABLE_NAME]          → User input placeholder
  `$VARIABLE`              → Shell variable
  [command]                → Placeholder for actual command
```

---

## Example: Mini Runbook

```markdown
# Database Setup - Local PostgreSQL

**Version:** 1.0

---

## 🤖 For AI Coding Agents

**Your goal:** Set up local PostgreSQL with a project database.

---

## Step 0: Prerequisites

\`\`\`bash
which psql || echo "PostgreSQL not installed"
\`\`\`

---

## Step 1: Get Configuration

**Ask the user:**

"What should the database be named?"
**Record:** `[DB_NAME]`

"Create a dedicated user? (recommended)"
- **Yes** → Create user with same name as DB
- **No** → Use default postgres user

**Record:** `[CREATE_USER]`

---

## Step 2: Create Database

\`\`\`bash
createdb [DB_NAME]
\`\`\`

**If [CREATE_USER] = Yes:**

\`\`\`bash
createuser [DB_NAME] --createdb
psql -c "ALTER USER [DB_NAME] WITH PASSWORD '[DB_NAME]123';"
\`\`\`

---

## Verification

\`\`\`bash
psql -d [DB_NAME] -c "SELECT 1;"
\`\`\`

**Success:** ✅ Query returns 1

---

## Troubleshooting

### Issue: `createdb: command not found`

\`\`\`bash
# macOS
brew install postgresql@15
brew services start postgresql@15
\`\`\`
```

---

## Validation Checklist

Before finalizing a runbook, verify:

- [ ] **Header** has title, version, and goal
- [ ] **Prerequisites** check all dependencies
- [ ] **Steps** are numbered and logical
- [ ] **Commands** are in code blocks
- [ ] **Decision points** use "Ask the user:" pattern
- [ ] **Variables** are clearly marked with `[BRACKETS]`
- [ ] **Conditionals** cover all paths
- [ ] **Verification** has concrete success criteria
- [ ] **Troubleshooting** covers common failures
- [ ] **Idempotent** - can run multiple times safely

---

## Anti-Patterns to Avoid

❌ **Vague instructions:** "Configure the database appropriately"
✅ **Specific commands:** "Run `createdb myapp_dev`"

❌ **Assumed knowledge:** "Set up Docker"
✅ **Explicit steps:** "Install Docker: `brew install docker`"

❌ **Missing decision points:** Silently picking defaults
✅ **Explicit choices:** "Ask the user: Which option?"

❌ **No verification:** "You're done!"
✅ **Concrete checks:** "Run `docker ps` - should show container running"

❌ **Monolithic steps:** One giant step with 50 commands
✅ **Atomic steps:** One logical action per step
