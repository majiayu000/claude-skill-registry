---
name: mastering-hooks
description: Master Claude Context Hooks (CCH), the Rust-based runtime for controlling Claude Code behavior through hooks.yaml configuration. Use when asked to "install CCH", "create hooks", "debug hooks", "hook not firing", "configure context injection", "validate hooks.yaml", "PreToolUse", "PostToolUse", or "block dangerous commands". Covers installation, rule creation, troubleshooting, and optimization.
metadata:
  version: "1.1.0"
  author: CCH Team
  api_version: "1.1.0"
---

# mastering-hooks

## Contents

- [Overview](#overview)
- [Decision Tree](#decision-tree)
- [Capabilities](#capabilities)
- [When NOT to Use](#when-not-to-use)
- [References](#references)

## Overview

Claude Context Hooks (CCH) is a **deterministic runtime engine** that intercepts Claude Code events and executes configured actions.

```
User Prompt --> Claude Code --> CCH Binary --> [Match Rules] --> Execute Actions
                    |                              |
                    v                              v
              PreToolUse                    inject/run/block
              PostToolUse                   context/validation
              PermissionRequest
```

**System components**:
- **CCH Binary** (Rust): Fast, deterministic hook execution at runtime
- **hooks.yaml**: Declarative configuration defining rules, matchers, and actions
- **This Skill**: Intelligent assistant for setup, debugging, and optimization

## Decision Tree

```
What do you need?
|
+-- New to CCH? --> [1. Install & Initialize]
|
+-- Have hooks.yaml but hooks not working? --> [4. Troubleshoot]
|
+-- Need to add new behavior? --> [2. Create Rules]
|
+-- Want to understand existing config? --> [3. Explain Configuration]
|
+-- Performance or complexity issues? --> [5. Optimize]
```

## Capabilities

### 1. Install & Initialize CCH

**Use when**: Setting up CCH for the first time in a project or user-wide.

**Checklist**:
1. Verify CCH binary is installed: `cch --version --json`
2. Initialize configuration: `cch init` (creates `.claude/hooks.yaml`)
3. Register with Claude Code: `cch install --project` or `cch install --user`
4. Validate configuration: `cch validate`
5. Verify installation: Check `.claude/settings.json` for hook entries

**Expected output** from `cch --version --json`:
```json
{"version": "1.1.0", "api_version": "1.1.0", "git_sha": "abc1234"}
```

**Reference**: [cli-commands.md](references/cli-commands.md)

---

### 2. Create Hook Rules

**Use when**: Adding new behaviors like context injection, command validation, or workflow automation.

**Checklist**:
1. Identify the event type (PreToolUse, PostToolUse, etc.)
2. Define matchers (tools, extensions, directories, patterns)
3. Choose action type (inject, run, block, require_fields)
4. Write the rule in hooks.yaml
5. Validate: `cch validate`
6. Test with: `cch debug <event> --tool <tool_name>`

**Rule anatomy**:
```yaml
hooks:
  - name: rule-name           # kebab-case identifier
    event: PreToolUse         # When to trigger
    match:
      tools: [Write, Edit]    # What to match
      extensions: [.py]       # Optional: file filters
    action:
      type: inject            # What to do
      source: file            # file | inline | command
      path: .claude/context/python-standards.md
```

**Reference**: [hooks-yaml-schema.md](references/hooks-yaml-schema.md) | [rule-patterns.md](references/rule-patterns.md)

---

### 3. Explain Configuration

**Use when**: Understanding what existing hooks do, why they exist, or how they interact.

**Checklist**:
1. Run `cch explain rule <rule-name>` for specific rule analysis
2. Run `cch explain config` for full configuration overview
3. Check rule precedence (first match wins within same event)
4. Identify potential conflicts or overlaps

**Example output** from `cch explain rule python-standards`:
```
Rule: python-standards
Event: PreToolUse
Triggers when: Write or Edit tool used on .py files
Action: Injects content from .claude/context/python-standards.md
```

**Reference**: [cli-commands.md](references/cli-commands.md)

---

### 4. Troubleshoot Hook Issues

**Use when**: Hooks not firing, unexpected behavior, or error messages.

**Diagnostic checklist**:
1. **Validate config**: `cch validate` - catches YAML/schema errors
2. **Check registration**: `cat .claude/settings.json | grep hooks`
3. **Enable debug logging**: `cch debug PreToolUse --tool Write --verbose`
4. **Check logs**: `cch logs --tail 20`
5. **Verify file paths**: Ensure all `path:` references exist

**Common issues**:

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Hook never fires | Event/matcher mismatch | Use `cch debug` to trace matching |
| "file not found" | Invalid path in action | Check relative paths from project root |
| Context not injected | Script returns invalid JSON | Validate script output format |
| Permission denied | Script not executable | `chmod +x script.sh` |

**Reference**: [troubleshooting-guide.md](references/troubleshooting-guide.md)

---

### 5. Optimize Configuration

**Use when**: Too many rules, slow execution, or complex maintenance.

**Optimization checklist**:
1. Consolidate overlapping rules with broader matchers
2. Use `enabled_when` for conditional rules instead of duplicates
3. Move shared context to reusable markdown files
4. Order rules by frequency (most common first)
5. Use `block` early to short-circuit unnecessary processing

**Reference**: [rule-patterns.md](references/rule-patterns.md)

---

## When NOT to Use This Skill

- **Simple Claude Code configuration**: Use `settings.json` directly for basic permissions
- **One-time context injection**: Just paste into your prompt
- **Non-Claude Code tools**: CCH only works with Claude Code CLI
- **Dynamic runtime decisions**: CCH is deterministic; use MCP servers for complex logic

---

## References

| Document | Purpose |
|----------|---------|
| [quick-reference.md](references/quick-reference.md) | Events, matchers, actions, file locations |
| [hooks-yaml-schema.md](references/hooks-yaml-schema.md) | Complete YAML configuration reference |
| [cli-commands.md](references/cli-commands.md) | All CLI commands with examples |
| [rule-patterns.md](references/rule-patterns.md) | Common patterns and recipes |
| [troubleshooting-guide.md](references/troubleshooting-guide.md) | Diagnostic procedures |

---

## Example: Complete hooks.yaml

```yaml
# .claude/hooks.yaml
version: "1"

hooks:
  # Inject Python standards before writing Python files
  - name: python-standards
    event: PreToolUse
    match:
      tools: [Write, Edit]
      extensions: [.py]
    action:
      type: inject
      source: file
      path: .claude/context/python-standards.md

  # Block dangerous git commands
  - name: block-force-push
    event: PreToolUse
    match:
      tools: [Bash]
      command_match: "git push.*--force"
    action:
      type: block
      reason: "Force push requires explicit approval."

  # Run security check before committing
  - name: pre-commit-security
    event: PreToolUse
    match:
      tools: [Bash]
      command_match: "git commit"
    action:
      type: run
      command: .claude/validators/check-secrets.sh
      timeout: 30
```
