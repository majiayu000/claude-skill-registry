---
name: writing-rules
description: 'Create markdown-based behavioral rules preventing unwanted actions.


  create hookify rule, behavioral rule, prevent behavior, block command


  Use when: preventing dangerous commands, blocking debug commits, enforcing conventions

  DO NOT use when: hook scope (abstract:hook-scope-guide), SDK hooks (abstract:hook-authoring), evaluating hooks (abstract:hooks-eval).'
category: hook-development
tags:
- hookify
- rules
- patterns
- validation
- safety
dependencies: []
estimated_tokens: 2500
complexity: beginner
provides:
  patterns:
  - rule-writing
  - pattern-matching
  - condition-building
  infrastructure:
  - rule-validation
usage_patterns:
- creating-rules
- pattern-matching
- behavioral-enforcement
---
## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Rule File Format](#rule-file-format)
- [Frontmatter Fields](#frontmatter-fields)
- [Event Types](#event-types)
- [Advanced Conditions](#advanced-conditions)
- [Operators](#operators)
- [Field Reference](#field-reference)
- [Pattern Writing](#pattern-writing)
- [Regex Basics](#regex-basics)
- [Examples](#examples)
- [Test Patterns](#test-patterns)
- [Example Rules](#example-rules)
- [Block Destructive Commands](#block-destructive-commands)
- [Warn About Debug Code](#warn-about-debug-code)
- [Require Tests](#require-tests)
- [Protect Production Files](#protect-production-files)
- [Management](#management)
- [Related Skills](#related-skills)
- [Best Practices](#best-practices)


# Hookify Rule Writing Guide


## When To Use

- Creating behavioral rules to prevent unwanted actions
- Defining persistent guardrails for Claude Code sessions

## When NOT To Use

- Complex multi-step workflows - use agents instead
- One-time operations that do not need persistent behavioral rules

## Overview

Hookify rules are markdown files with YAML frontmatter that define patterns to watch for and messages to show when those patterns match. Rules are stored in `.claude/hookify.{rule-name}.local.md` files.

## Quick Start

Create `.claude/hookify.dangerous-rm.local.md`:

```yaml
---
name: dangerous-rm
enabled: true
event: bash
pattern: rm\s+-rf
action: block
---

🛑 **Dangerous rm command detected!**

This command could delete important files.
```
**Verification:** Run the command with `--help` flag to verify availability.

The rule activates immediately - no restart needed!

## Rule File Format

### Frontmatter Fields

**name** (required): Unique identifier (kebab-case)
**enabled** (required): `true` or `false`
**event** (required): `bash`, `file`, `stop`, `prompt`, or `all`
**action** (optional): `warn` (default) or `block`
**pattern** (simple): Regex pattern to match

### Event Types

- **bash**: Bash tool commands
- **file**: Edit, Write, MultiEdit tools
- **stop**: When agent wants to stop
- **prompt**: User prompt submission
- **all**: All events

### Advanced Conditions

For multiple field checks:

```yaml
---
name: warn-env-edits
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$
  - field: new_text
    operator: contains
    pattern: API_KEY
---

🔐 **API key in .env file!**
Ensure file is in .gitignore.
```

### Operators

- `regex_match`: Pattern matching
- `contains`: Substring check
- `equals`: Exact match
- `not_contains`: Must NOT contain
- `starts_with`: Prefix check
- `ends_with`: Suffix check

### Field Reference

**bash events:** `command`
**file events:** `file_path`, `new_text`, `old_text`, `content`
**prompt events:** `user_prompt`
**stop events:** `transcript`

## Pattern Writing

### Regex Basics

- `\s` - whitespace
- `\d` - digit
- `\w` - word character
- `.` - any character (use `\.` for literal dot)
- `+` - one or more
- `*` - zero or more
- `|` - OR

### Examples

```
rm\s+-rf          → rm -rf
console\.log\(    → console.log(
chmod\s+777       → chmod 777
```

### Test Patterns

```bash
python3 -c "import re; print(re.search(r'pattern', 'text'))"
```

## Example Rules

### Block Destructive Commands

```yaml
---
name: block-destructive
enabled: true
event: bash
pattern: rm\s+-rf|dd\s+if=|mkfs
action: block
---

🛑 **Destructive operation blocked!**
Can cause data loss.
```

### Warn About Debug Code

```yaml
---
name: warn-debug
enabled: true
event: file
pattern: console\.log\(|debugger;
action: warn
---

🐛 **Debug code detected!**
Remove before committing.
```

### Require Tests

```yaml
---
name: require-tests
enabled: true
event: stop
action: warn
conditions:
  - field: transcript
    operator: not_contains
    pattern: pytest|npm test
---

⚠️ **Tests not run!**
Please verify changes.
```

### Protect Production Files

```yaml
---
name: protect-prod
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: /production/|\.prod\.
---

🚨 **Production file!**
Requires review.
```

## Management

**Enable/Disable:**
Edit `.local.md` file: `enabled: false`

**Delete:**
```bash
rm .claude/hookify.my-rule.local.md
```

**List:**
```bash
/hookify:list
```

## Related Skills

- **abstract:hook-scope-guide** - Hook placement decisions
- **abstract:hook-authoring** - SDK hook development
- **abstract:hooks-eval** - Hook evaluation

## Best Practices

1. Start with simple patterns
2. Test regex thoroughly
3. Use clear, helpful messages
4. Prefer warnings over blocks initially
5. Name rules descriptively
6. Document intent in messages
## Troubleshooting

### Common Issues

If a rule doesn't trigger, verify that the `event` type matches the tool being used (e.g., use `bash` for command line tools). Check that the regex `pattern` is valid and matches the target text by testing it with a short Python script. If you encounter permission errors when creating rule files in `.claude/`, ensure that the directory is writable by your user.
