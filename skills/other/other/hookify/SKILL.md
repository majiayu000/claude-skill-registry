---
name: hookify
description: Guide for creating hookify rules to prevent unwanted behaviors. Use when creating, editing, or understanding hookify rule files.
argument-hint: help | list | configure | <behavior description>
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Task, TodoWrite, Skill
---

# Hookify - Hook Management

Manage hookify rules that prevent unwanted Claude behaviors in the Wythm project.

## Usage

- `/hookify help` - Show documentation on how hookify works
- `/hookify list` - List all configured rules
- `/hookify configure` - Enable/disable rules interactively
- `/hookify <behavior>` - Create rule for specific behavior
- `/hookify` - Analyze conversation to find behaviors to prevent

Parse $ARGUMENTS to determine which sub-command to run.

## Reference

For complete rule writing guide, syntax, examples, and testing instructions, see [references/rule-guide.md](references/rule-guide.md).

---

## Sub-command: help

**Show comprehensive hookify documentation.**

Read and present the content from [references/rule-guide.md](references/rule-guide.md).

Explain:
1. How hookify works (hook events, rule loading)
2. Configuration file format (frontmatter + message)
3. Pattern syntax (Python regex)
4. Available commands
5. Example rules

**Key points to cover:**
- Rule files location: `.claude/hooks/hookify/rules/*.local.md`
- Events: bash, file, stop, prompt, all
- Actions: warn (default), block
- Changes take effect immediately

---

## Sub-command: list

**List all configured hookify rules.**

Steps:
1. Glob for `.claude/hooks/hookify/rules/*.local.md`
2. Read each file, extract frontmatter (name, enabled, event, pattern)
3. Present as table:

| Name | Enabled | Event | Pattern | File |
|------|---------|-------|---------|------|

4. Show totals (X enabled, Y disabled)
5. Add footer with edit/disable instructions

If no rules found, suggest `/hookify <behavior>` to create first rule.

---

## Sub-command: configure

**Enable/disable rules interactively.**

Steps:
1. Glob for `.claude/hooks/hookify/rules/*.local.md`
2. Read each file, get name and enabled state
3. Use AskUserQuestion with multiSelect to let user pick rules to toggle
4. For each selected: toggle `enabled: true` <-> `enabled: false` using Edit tool
5. Confirm changes

---

## Sub-command: create (default when $ARGUMENTS is not a sub-command)

**Create hook rules from behavior description or conversation analysis.**

### If $ARGUMENTS contains behavior description:
- Parse the specific instruction
- Still scan recent conversation for examples

### If $ARGUMENTS is empty:
- Launch conversation-analyzer agent to find problematic behaviors
- Agent scans user prompts for frustration signals

### Creation steps:
1. Gather behaviors (from args or agent)
2. Present findings with AskUserQuestion:
   - Which behaviors to hookify? (multiSelect)
   - Warn or block? (for each selected)
3. Generate rule files in `.claude/hooks/hookify/rules/{name}.local.md`
4. Confirm creation, remind no restart needed

### Rule file format:
```markdown
---
name: {kebab-case-name}
enabled: true
event: {bash|file|stop|prompt|all}
conditions:
  - field: {command|new_text|file_path|user_prompt}
    operator: {regex_match|contains|equals|starts_with|ends_with|not_contains}
    pattern: '{regex pattern}'
action: {warn|block}
---

{Message to show Claude when rule triggers}
```

---

## Quick Reference

**Events:**
- bash: Bash tool commands
- file: Edit/Write tools
- stop: When agent wants to stop
- prompt: User prompt submission
- all: All events

**Regex tips:**
- `rm\s+-rf` - rm -rf
- `console\.log\(` - console.log()
- `\.env$` - .env files
- `chmod\s+777` - chmod 777

**File location:** `.claude/hooks/hookify/rules/*.local.md`

**No restart needed** - rules apply immediately!
