---
name: command-creator
model: fast
description: |
  WHAT: Create Claude Code slash commands - reusable markdown workflows invoked with /command-name.
  
  WHEN: User wants to create, make, or add a slash command. User wants to automate a repetitive workflow or document a consistent process for reuse.
  
  KEYWORDS: "create a command", "make a slash command", "add a command", "new command", "/command", "automate this workflow", "make this repeatable"
---

# Command Creator

Slash commands are markdown files in `.claude/commands/` (project) or `~/.claude/commands/` (global) that expand into prompts when invoked.

## Command Structure

```markdown
---
description: Brief description for /help (required)
argument-hint: <required> or [optional] (if takes arguments)
---

# Command Title

[Instructions for agent to execute autonomously]
```


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install command-creator
```


---

## Creation Workflow

### Step 1: Determine Location

1. Check if in git repo: `git rev-parse --is-inside-work-tree`
2. Default: Git repo → `.claude/commands/`, No git → `~/.claude/commands/`
3. Override if user explicitly says "global" or "project"

Report chosen location before proceeding.

### Step 2: Identify Pattern

Load [references/patterns.md](references/patterns.md) and present options:

| Pattern | Structure | Use When |
|---------|-----------|----------|
| Workflow Automation | Analyze → Act → Report | Multi-step with clear sequence |
| Iterative Fixing | Run → Parse → Fix → Repeat | Fix issues until passing |
| Agent Delegation | Context → Delegate → Iterate | Complex tasks, user review |
| Simple Execution | Parse → Execute → Return | Wrapper for existing tools |

Ask: "Which pattern is closest to what you want?"

### Step 3: Gather Information

**A. Name and Purpose**
- "What should the command be called?" (kebab-case: `my-command`)
- "What does it do?" (for description field)

**B. Arguments**
- "Does it take arguments? Required or optional?"
- Required: `<placeholder>`, Optional: `[placeholder]`

**C. Workflow Steps**
- "What specific steps should it follow?"
- "What tools or commands should it use?"

**D. Constraints**
- "Any specific tools to use or avoid?"
- "Any files to read for context?"

### Step 4: Generate Command

Load [references/best-practices.md](references/best-practices.md) for:
- Template structure
- Writing style (imperative form)
- Quality checklist

Key principles:
- Use imperative form: "Run X", not "You should run X"
- Be explicit: "Run `make lint`", not "Check for errors"
- Include expected outcomes
- Define error handling
- State success criteria

### Step 5: Create File

```bash
mkdir -p [directory-path]
```

Write the command file. Report:
- File location
- What the command does
- How to use: `/command-name [args]`

### Step 6: Test (Optional)

Suggest: "Test with `/command-name [args]`"

Iterate based on feedback.

---

## Writing Guidelines

**Imperative form (verb-first)**:
- ✅ "Run git status"
- ❌ "You should run git status"

**Specific, not vague**:
- ✅ "Run `make lint` to check for errors"
- ❌ "Check for errors"

**Include outcomes**:
- ✅ "Run `git status` - should show modified files"
- ❌ "Run git status"

**Realistic examples**:
- ✅ `git commit -m "Add OAuth2 authentication"`
- ❌ `git commit -m "foo bar"`

---

## Command Patterns Quick Reference

### Workflow Automation
```markdown
1. Check for .PLAN.md
2. Analyze git status/diff
3. Perform actions
4. Report results
```

### Iterative Fixing
```markdown
1. Run make all-ci (max 10 iterations)
2. Parse errors by category
3. Apply targeted fixes
4. Repeat until success or stuck
```

### Agent Delegation
```markdown
1. Present context
2. Invoke subagent with Task tool
3. Iterate with user feedback
4. Save output after approval
```

See [references/examples.md](references/examples.md) for full command examples.

---

## Quality Checklist

Before finalizing:

- [ ] Name is kebab-case (`my-command`, not `my_command`)
- [ ] Description is action-oriented
- [ ] Steps are numbered and specific
- [ ] Tool usage explicitly specified
- [ ] Error handling defined
- [ ] Success criteria stated
- [ ] Uses imperative form

---

## NEVER

- Use underscores in command names (use hyphens)
- Write vague instructions ("fix errors")
- Skip error handling
- Use second person ("You should...")
- Create commands without testing
- Leave success criteria undefined
