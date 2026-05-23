---
name: hookify
description: Create dynamic hook rules from natural language descriptions. Generates .claude/hookify.*.local.md files that warn or block operations matching patterns. Triggers on "hookify", "create hook rule", "warn me when", "block when", "don't let me".
---

# Hookify — Dynamic Hook Rules

Create hook rules from natural language without editing hooks.json.

## Step 1: Understand Intent

Parse the user's description to determine:
- **Event type**: bash (commands), file (edits/writes), stop (session end), prompt (user input)
- **Action**: warn (show message, allow) or block (deny operation)
- **Pattern**: regex to match against the relevant field
- **Field**: what to match (command, file_path, new_text, user_prompt, etc.)

Examples:
- "Warn me when I use rm -rf" → event: bash, action: warn, pattern: `rm\s+-rf`
- "Don't let me edit .env files" → event: file, action: block, field: file_path, pattern: `\.env$`
- "Block console.log in TypeScript" → event: file, action: warn, field: new_text, conditions on file_path AND new_text
- "Don't stop without running tests" → event: stop, action: block, field: transcript, operator: not_contains, pattern: `pytest|npm test`

## Step 2: Generate Rule File

Create `.claude/hookify.<short-name>.local.md`:

```markdown
---
name: <descriptive-kebab-case-name>
enabled: true
event: <bash|file|stop|prompt>
action: <warn|block>
pattern: <regex>  # for single-condition rules
---

<Warning/block message in markdown. Be helpful — explain WHY and suggest alternatives.>
```

For multi-condition rules:

```markdown
---
name: <name>
enabled: true
event: <event>
action: <action>
conditions:
  - field: <field>
    operator: <regex_match|contains|not_contains|equals|starts_with|ends_with>
    pattern: <value>
  - field: <field>
    operator: <operator>
    pattern: <value>
---

<Message>
```

## Step 3: Confirm

Show the user:
1. The generated file path and content
2. What it will catch (with example triggers)
3. What it will NOT catch (edge cases)

## Step 4: Test Suggestion

Suggest a way to test the rule immediately:
- For bash rules: "Try running `<command that triggers>`"
- For file rules: "Try editing a file matching the pattern"
- For stop rules: "The rule will trigger next time the session ends"

## Rule Naming Convention

- `hookify.block-rm-rf.local.md` — block dangerous rm
- `hookify.warn-console-log.local.md` — warn about debug code
- `hookify.require-tests.local.md` — require tests before stopping
- `hookify.warn-env-edit.local.md` — warn about .env edits

## Management Commands

If user asks to list/manage rules:
- **List**: `ls .claude/hookify.*.md` and show name + event + action + enabled for each
- **Disable**: set `enabled: false` in frontmatter
- **Delete**: remove the file
- **Enable**: set `enabled: true` in frontmatter

## Notes

- Rules take effect immediately — no restart needed
- `.local.md` files are gitignored by convention
- To share rules with the team, drop the `.local` suffix
- Keep regex patterns simple — complex patterns are hard to maintain
- Prefer `warn` over `block` for most cases
- All conditions in a rule must match (AND logic)
- No external dependencies — stdlib Python only
