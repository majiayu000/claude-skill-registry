---
name: mastering-hooks
description: Master RuleZ, the high-performance AI policy engine for development workflows. Use when asked to "install rulez", "create hooks", "debug hooks", "hook not firing", "configure context injection", "validate hooks.yaml", "PreToolUse", "PostToolUse", "block dangerous commands", "multi-platform hooks", "Gemini CLI hooks", "Copilot hooks", "OpenCode hooks", "dual-fire events", or "cross-platform rules". Covers installation, rule creation, multi-platform adapters, troubleshooting, and optimization.
metadata:
  version: "2.2.1"
  author: RuleZ Team
  api_version: "2.2.1"
last_modified: 2026-03-16
last_validated: 2026-03-16
---

# mastering-hooks

## Contents

- [Overview](#overview)
- [Decision Tree](#decision-tree)
- [Capabilities](#capabilities)
- [When NOT to Use](#when-not-to-use)
- [References](#references)

## Overview

RuleZ is a **high-performance AI policy engine** that intercepts AI coding assistant events and executes configured actions. It works across multiple platforms through adapter-based event translation.

```
User Prompt --> AI Assistant --> RuleZ Binary --> [Match Rules] --> Execute Actions
                    |                                 |
                    v                                 v
              PreToolUse                       inject/run/block
              PostToolUse                      context/validation
              BeforeAgent
              PermissionRequest
```

**Supported platforms**:
- **Claude Code** (native) - Full event support
- **Gemini CLI** - Via adapter with dual-fire events
- **GitHub Copilot** - Via adapter
- **OpenCode** - Via adapter with dual-fire events

**System components**:
- **RuleZ Binary** (Rust): Fast, deterministic hook execution at runtime
- **hooks.yaml**: Declarative configuration defining rules, matchers, and actions
- **Platform Adapters**: Translate platform-specific events to unified RuleZ event types
- **This Skill**: Intelligent assistant for setup, debugging, and optimization

## Decision Tree

```
What do you need?
|
+-- New to RuleZ? --> [1. Install & Initialize]
|
+-- Have hooks.yaml but hooks not working? --> [4. Troubleshoot]
|
+-- Need to add new behavior? --> [2. Create Rules]
|
+-- Want to understand existing config? --> [3. Explain Configuration]
|
+-- Performance or complexity issues? --> [5. Optimize]
|
+-- Setting up for Gemini/Copilot/OpenCode? --> [6. Multi-Platform Setup]
```

## Capabilities

### 1. Install & Initialize RuleZ

**Use when**: Setting up RuleZ for the first time in a project or user-wide.

**Checklist**:
1. Verify RuleZ binary is installed: `rulez --version`
2. Initialize configuration: `rulez init` (creates `.claude/hooks.yaml`)
3. Register with Claude Code: `rulez install` (project-local) or `rulez install --global`
4. Validate configuration: `rulez validate`
5. Verify installation: Check `.claude/settings.json` for hook entries

**Reference**: [cli-commands.md](references/cli-commands.md)

---

### 2. Create Hook Rules

**Use when**: Adding new behaviors like context injection, command validation, or workflow automation.

**Checklist**:
1. Identify the event type (PreToolUse, PostToolUse, BeforeAgent, etc.)
2. Define matchers (tools, extensions, directories, patterns)
3. Choose action type (inject, run, block, require_fields)
4. Write the rule in hooks.yaml
5. Validate: `rulez validate`
6. Test with: `rulez debug <event> --tool <tool_name>`

**Rule anatomy**:
```yaml
rules:
  - name: rule-name           # kebab-case identifier
    matchers:
      operations: [PreToolUse]  # When to trigger
      tools: [Write, Edit]    # What to match
      extensions: [.py]       # Optional: file filters
    actions:
      inject: .claude/context/python-standards.md  # What to do
```

**Reference**: [hooks-yaml-schema.md](references/hooks-yaml-schema.md) | [rule-patterns.md](references/rule-patterns.md)

---

### 3. Explain Configuration

**Use when**: Understanding what existing hooks do, why they exist, or how they interact.

**Checklist**:
1. Run `rulez explain rule <rule-name>` for specific rule analysis
2. Run `rulez explain rules` for full configuration overview
3. Check rule precedence (first match wins within same event)
4. Identify potential conflicts or overlaps

**Example output** from `rulez explain rule python-standards`:
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
1. **Validate config**: `rulez validate` - catches YAML/schema errors
2. **Check registration**: `cat .claude/settings.json | grep hooks`
3. **Enable debug logging**: `rulez debug PreToolUse --tool Write --verbose`
4. **Check logs**: `rulez logs --limit 20`
5. **Verify file paths**: Ensure all `path:` references exist

**Common issues**:

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Hook never fires | Event/matcher mismatch | Use `rulez debug` to trace matching |
| "file not found" | Invalid path in action | Check relative paths from project root |
| Context not injected | Script returns invalid JSON | Validate script output format |
| Permission denied | Script not executable | `chmod +x script.sh` |
| Event not firing on Gemini | Wrong event name | Check [platform-adapters.md](references/platform-adapters.md) for mappings |

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

### 6. Multi-Platform Setup

**Use when**: Configuring RuleZ to work with Gemini CLI, GitHub Copilot, or OpenCode in addition to Claude Code.

**Key concepts**:
- RuleZ uses **platform adapters** to translate each platform's native events into unified RuleZ event types
- Write rules using RuleZ event types (e.g., `PreToolUse`) — adapters handle translation automatically
- Some platforms fire **dual events** (e.g., Gemini's `BeforeAgent` fires both `BeforeAgent` and `UserPromptSubmit`)

**Checklist**:
1. Install RuleZ: `rulez install`
2. Write rules using standard RuleZ event types
3. Test with `rulez debug <event>` to verify matching
4. Review [platform-adapters.md](references/platform-adapters.md) for platform-specific event mappings

**Reference**: [platform-adapters.md](references/platform-adapters.md)

---

## When NOT to Use This Skill

- **Simple Claude Code configuration**: Use `settings.json` directly for basic permissions
- **One-time context injection**: Just paste into your prompt
- **Dynamic runtime decisions**: RuleZ is deterministic; use MCP servers for complex logic

---

## References

| Document | Purpose |
|----------|---------|
| [quick-reference.md](references/quick-reference.md) | Events, matchers, actions, file locations |
| [hooks-yaml-schema.md](references/hooks-yaml-schema.md) | Complete YAML configuration reference |
| [cli-commands.md](references/cli-commands.md) | All CLI commands with examples |
| [rule-patterns.md](references/rule-patterns.md) | Common patterns and recipes |
| [troubleshooting-guide.md](references/troubleshooting-guide.md) | Diagnostic procedures |
| [platform-adapters.md](references/platform-adapters.md) | Multi-platform event mappings and dual-fire |

---

## Example: Complete hooks.yaml

```yaml
# .claude/hooks.yaml
version: "1"

rules:
  # Inject Python standards before writing Python files
  - name: python-standards
    matchers:
      operations: [PreToolUse]
      tools: [Write, Edit]
      extensions: [.py]
    actions:
      inject: .claude/context/python-standards.md

  # Block dangerous git commands
  - name: block-force-push
    priority: 10
    matchers:
      operations: [PreToolUse]
      tools: [Bash]
      command_match: "git push.*--force"
    actions:
      block: true

  # Run security check before committing
  - name: pre-commit-security
    matchers:
      operations: [PreToolUse]
      tools: [Bash]
      command_match: "git commit"
    actions:
      run: .claude/validators/check-secrets.sh

  # Track agent activity (works on Claude Code and Gemini)
  - name: log-agent-start
    description: Ensure agents follow project conventions
    matchers:
      operations: [BeforeAgent]
    actions:
      inject_inline: |
        **Agent Policy**: Follow project conventions in CLAUDE.md.
```
