---
name: hook-management
description: Central authority for Claude Code hooks management in this repository. Automates enforcement of critical repository rules through hooks. Use when adding hooks, managing hooks, configuring hooks, troubleshooting hooks, or understanding hook behavior. Delegates to docs-management skill for official hooks documentation. Provides organization-specific patterns, configuration management, and workflow guidance.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill
---

# Hooks Meta Skill

## 🚨 MANDATORY: Invoke docs-management First

> **STOP - Before providing ANY response about Claude Code hooks:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** using keywords: hooks, PreToolUse, PostToolUse, hook events, hook configuration, or related topics
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**

### Verification Checkpoint

Before responding, verify:

- [ ] Did I invoke docs-management skill?
- [ ] Did official documentation load?
- [ ] Is my response based EXCLUSIVELY on official docs?

If ANY checkbox is unchecked, STOP and invoke docs-management first.

## Overview

Central authority for managing Claude Code hooks in this repository. Automates enforcement of critical repository rules that were previously manual in CLAUDE.md.

**Architecture:** Vertical slice organization with externalized configuration, multi-language support, immediate config reload, and comprehensive testing.

## When to Use This Skill

**Keywords:** hooks, hook management, automation, validation, enforcement, PreToolUse, PostToolUse, SessionStart, SessionEnd, Setup hook, hook configuration, plugin hooks, local hooks, CLAUDE_HOOK_ENABLED, hook environment variables, enable hook, disable hook, --init, --init-only, --maintenance

**Use this skill when:**

- Adding new hooks to the repository
- Modifying existing hook behavior
- Troubleshooting hook issues
- Disabling/enabling hooks
- Understanding what hooks are active
- Configuring hook enforcement levels

## 🚨 CRITICAL: Official Hooks Documentation

**For ALL Claude Code hooks capabilities, configuration patterns, and syntax, you MUST use the docs-management skill.**

### What to Delegate to docs-management

> ⚠️ **STALENESS WARNING:** Do NOT hardcode hook event names, decision values, or environment variables.
> ALWAYS query docs-management for the authoritative list of hook capabilities.

**Query Patterns for Official Hook Documentation:**

| Topic | Query Pattern | What You'll Find |
| --- | --- | --- |
| Hook event types | "hooks.md hook events", "hook event types" | Complete list of available events |
| Hook configuration | "hooks.md configuration syntax" | JSON structure and required fields |
| Matchers | "hooks.md matchers tool names" | Tool matching patterns |
| Decision control | "hooks.md decision control", "hook return values" | Valid decision values and behavior |
| Exit codes | "hooks.md exit codes" | Exit code meanings |
| JSON output | "hooks.md JSON output schema" | Output schema for hook responses |
| Environment variables | "hooks.md environment variables" | Available env vars in hooks |
| Command vs prompt hooks | "hooks.md command prompt based" | Hook type differences |
| Plugin hooks | "hooks.md plugin hooks integration" | Plugin-specific patterns |

**Example queries:**

```text
docs-management: "hooks.md hook event types"
docs-management: "hooks.md decision control values"
docs-management: "hooks.md environment variables available"
```

**Frontmatter Hooks (v2.1.x):**

- Keywords: `frontmatter hooks`, `skill hooks`, `agent hooks`, `command hooks`, `once true`
- Use case: Defining hooks in skill/agent/command YAML frontmatter (not just .claude/hooks/)

**SessionStart Hook Input (v2.1.2+):**

- Keywords: `SessionStart`, `agent_type`, `--agent flag`
- Use case: SessionStart hooks receive `agent_type` field when invoked with `--agent` CLI flag
- Note: This field is documented in CHANGELOG v2.1.2 but may not yet be in official hooks.md - query docs-management for current state

**PreToolUse additionalContext Return (v2.1.9+):**

- Keywords: `PreToolUse`, `additionalContext`, `hook return`, `context injection`
- Use case: PreToolUse hooks can return an `additionalContext` field to provide additional context to the model
- Query pattern: `docs-management: "hooks.md PreToolUse additionalContext return"`

**Setup Hook Event (v2.1.10+):**

- Keywords: `Setup hook`, `Setup event`, `--init`, `--init-only`, `--maintenance`, `repository setup`
- Use case: Setup hooks run during repository initialization/maintenance via CLI flags
- Triggers: `--init`, `--init-only`, or `--maintenance` CLI flags
- Query pattern: `docs-management: "hooks.md Setup hook event"`

### What This Skill Provides

**Organization-specific implementation:**

- Directory structure and conventions
- Configuration management patterns
- Shared utilities (json, path, git, config helpers)
- Active hooks inventory
- Multi-language implementation strategy
- Troubleshooting for this repository's hooks

## Quick Decision Tree

**What do you want to do?**

1. **Understand design principles** → See [Design Principles](references/architecture/design-principles.md)
2. **View active hooks** → See [Active Hooks](references/inventory/active-hooks.md)
3. **Manage hook lifecycle** (enable/disable/modify) → See [Hook Lifecycle](references/inventory/hook-lifecycle.md)
4. **Configure hooks** → See [Configuration Guide](references/configuration/hook-config-guide.md)
5. **Create new hook** → See [Creating Hooks Workflow](references/development/creating-hooks-workflow.md)
6. **Test hooks** → See [Testing Guide](references/development/testing-guide.md)
7. **Follow best practices** → See [Best Practices](references/development/best-practices.md)
8. **Troubleshoot issues** → See [Common Issues](references/troubleshooting/common-issues.md)
9. **Debug hooks** → See [Debugging Guide](references/troubleshooting/debugging-guide.md)
10. **Official hooks documentation** → Use docs-management skill with keywords above
11. **Create/configure plugin hooks** → Use `plugin-development` skill (see below)

### Plugin Hooks Delegation

**If you're working with plugin hooks** (hooks bundled in a Claude Code plugin), use the `plugin-development` skill instead. Plugin hooks use a different configuration pattern:

| Aspect | Local Hooks (this skill) | Plugin Hooks |
| --- | --- | --- |
| Location | `.claude/hooks/` directory | Plugin `hooks/hooks.json` |
| Configuration | YAML files (`config.yaml`) | Environment variables |
| Consumer Control | Edit config files directly | Via `settings.json` `env` section |

**For plugin hooks:** Invoke `plugin-development` skill and see the Plugin Hook Configuration section.

## Reference Loading Guide

**All references in this skill are conditional load** - they are loaded only when needed based on the workflow you're following.

### When to Load Each Reference

**Architecture References** (load when understanding design):

- `references/architecture/design-principles.md` → When understanding vertical slice, DRY, config-over-hardcoding principles
- `references/architecture/multi-language-strategy.md` → When implementing or migrating to Python/TypeScript

**Inventory References** (load when working with hooks):

- `references/inventory/active-hooks.md` → When reviewing what hooks are active and their configurations
- `references/inventory/hook-lifecycle.md` → When enabling/disabling hooks or changing enforcement modes

**Configuration References** (load when configuring):

- `references/configuration/hook-config-guide.md` → When modifying global.yaml or config.yaml files

**Development References** (load when creating/testing):

- `references/development/creating-hooks-workflow.md` → When creating a new hook from scratch
- `references/development/testing-guide.md` → When writing tests for hooks
- `references/development/best-practices.md` → When ensuring code quality and following patterns

**Troubleshooting References** (load when debugging):

- `references/troubleshooting/common-issues.md` → When encountering problems (hook not running, config not applying, etc.)
- `references/troubleshooting/debugging-guide.md` → When performing advanced debugging or profiling

### Progressive Disclosure Strategy

#### Layer 1: Always in Context

- SKILL.md (this file) - Navigation hub and decision trees

#### Layer 2: Load on Demand

- Reference files based on specific workflow or task

#### Layer 3: External Delegation

- Official documentation via `docs-management` skill queries (always)

This architecture ensures optimal token efficiency while maintaining comprehensive
guidance coverage.

## Active Hooks Summary

For complete details, see [Active Hooks Reference](references/inventory/active-hooks.md).

### PreToolUse Hooks (Validation Before Execution)

1. **prevent-backup-files** - Blocks .bak/.backup file creation for git-tracked content
2. **require-gpg-signing** - Blocks git commits with --no-gpg-sign flag
3. **require-explicit-commit** - Asks approval for direct git commits (encourages git-commit skill)
4. **block-absolute-paths** - Blocks absolute paths in markdown files for portability

### PostToolUse Hooks (Auto-Fix After Execution)

1. **markdown-lint** - Auto-fixes markdown files using markdownlint-cli2

## Configuration Quick Reference

All hooks use environment variables for configuration. See [Configuration Guide](references/configuration/hook-config-guide.md) for complete details.

**Quick actions:**

- **Enable a hook**: Set `CLAUDE_HOOK_{NAME}_ENABLED=1` in `.claude/settings.json` `env` section
- **Disable a hook**: Set `CLAUDE_HOOK_{NAME}_ENABLED=0` or remove the variable
- **Change enforcement**: Set `CLAUDE_HOOK_ENFORCEMENT_{NAME}` to `block`, `warn`, or `log`
- **Enable debug mode**: Set `CLAUDE_HOOK_DEBUG=1`

**Example configuration in `.claude/settings.json`:**

```json
{
  "env": {
    "CLAUDE_HOOK_MARKDOWN_LINT_ENABLED": "1",
    "CLAUDE_HOOK_LOG_EVENTS_ENABLED": "1"
  }
}
```

For environment variable patterns, default states, and legacy YAML configuration, see [Configuration Reference](references/configuration/hook-config-guide.md).

## Directory Structure (Vertical Slice)

```text
.claude/hooks/
├── config/
│   └── global.yaml                 # Shared configuration
├── shared/                         # Shared utilities (all hooks)
│   ├── json-utils.sh               # JSON parsing helpers
│   ├── path-utils.sh               # Path manipulation utilities
│   ├── config-utils.sh             # Config loading utilities
│   └── test-helpers.sh             # Test assertion framework
├── prevent-backup-files/           # Vertical slice: Hook 1
│   ├── bash/                       # Language-specific implementation
│   ├── config.yaml                 # User configuration (enabled, enforcement)
│   ├── hook.yaml                   # Hook metadata (name, version, description)
│   ├── README.md                   # Hook documentation
│   └── tests/                      # Tests for THIS hook
├── require-gpg-signing/            # Vertical slice: Hook 2
│   ├── bash/
│   ├── config.yaml
│   ├── hook.yaml
│   ├── README.md
│   └── tests/
├── <other-hooks>/                  # Additional hooks follow same pattern
├── test-runner.sh                  # Discovers & runs all *.test.sh files
└── README.md                       # Quick reference
```

**Key principles:**

- **High cohesion:** All hook code, config, docs, and tests in one directory
- **Low coupling:** Hooks don't depend on each other
- **Easy to modify:** Changes isolated to single directory
- **Clear ownership:** One directory = one feature

For complete architecture details, see [Design Principles](references/architecture/design-principles.md).

## Shared Utilities Quick Reference

All hooks have access to shared helper functions in `.claude/hooks/shared/`. See [Best Practices](references/development/best-practices.md) for usage examples.

> **Note:** Bash utilities maintained for legacy compatibility. New hooks should use Python with pathlib for cross-platform compatibility.

## Common Workflows

### Quick Actions

**Disable all hooks temporarily:**

```bash
# Edit .claude/hooks/config/global.yaml
enabled: false
```

**View hook activity:**

```bash
# Edit .claude/hooks/config/global.yaml
log_level: debug
```

**Run all tests:**

```bash
bash .claude/hooks/test-runner.sh
```

**Test specific hook:**

```bash
bash .claude/hooks/<hook-name>/tests/integration.test.sh
```

**Test manually:**

```bash
echo '{"tool": "Write", "file_path": "test.txt"}' | \
  bash .claude/hooks/<hook-name>/bash/<hook-name>.sh
```

For complete workflow guidance, see [Hook Lifecycle](references/inventory/hook-lifecycle.md).

## Integration with Repository

CLAUDE.md references hooks for automated enforcement. See [Active Hooks](references/inventory/active-hooks.md) for the complete list of rules automated by hooks.

## Next Steps

### For First-Time Users

1. Review [Active Hooks](references/inventory/active-hooks.md) to understand what's enforced
2. Read [Configuration Guide](references/configuration/hook-config-guide.md) to learn how to customize
3. Check [Common Issues](references/troubleshooting/common-issues.md) for troubleshooting tips

### For Hook Developers

1. Read [Design Principles](references/architecture/design-principles.md) to understand architecture
2. Follow [Creating Hooks Workflow](references/development/creating-hooks-workflow.md) for new hooks
3. Study [Best Practices](references/development/best-practices.md) for code quality
4. Use [Testing Guide](references/development/testing-guide.md) for comprehensive testing

### For Troubleshooting

1. Check [Common Issues](references/troubleshooting/common-issues.md) for known problems
2. Use [Debugging Guide](references/troubleshooting/debugging-guide.md) for advanced techniques
3. Query docs-management skill for official documentation

## Auditing Hooks

This skill provides the validation criteria used by the `hook-auditor` agent for formal audits.

### Audit Resources

| Resource | Location | Purpose |
| --- | --- | --- |
| Audit Framework | `references/audit-framework.md` | Query guides and scoring criteria |

### Scoring Categories

| Category | Points | Key Criteria |
| --- | --- | --- |
| Configuration Structure | 25 | Valid hooks.json, required fields, valid event types |
| Hook Scripts | 20 | Scripts exist, proper structure, exit codes |
| Matchers | 20 | Appropriate tool/path matchers |
| Environment Variables | 15 | Follows naming convention, documented |
| Testing | 20 | Has tests, tests pass, adequate coverage |

**Thresholds:** 85+ = PASS, 70-84 = PASS WITH WARNINGS, <70 = FAIL

### Related Agent

The `hook-auditor` agent (Haiku model) performs formal audits using this skill:

- Auto-loads this skill via `skills: hook-management`
- Uses audit framework and docs-management for rules
- Generates structured audit reports
- Invoked by `/audit-hooks` command

### External Technology Validation

When auditing hooks that use external technologies (scripts, packages, runtimes), the auditor MUST validate claims using MCP servers before flagging findings.

**Technologies Requiring MCP Validation:**

- .NET/C# scripts: Validate with microsoft-learn + perplexity
- Node.js/npm packages: Validate with context7 + perplexity
- Python scripts/packages: Validate with context7 + perplexity
- Shell scripts: Validate with perplexity
- Any version-specific claims: ALWAYS validate with perplexity

**Validation Rule:**

Never flag a technology usage as incorrect without first:

1. Querying appropriate MCP server(s) for current documentation
2. Verifying with perplexity for recent changes (especially .NET 10+)
3. Documenting MCP sources in the finding

**Stale Data Warning:**

- microsoft-learn can return cached/outdated documentation
- ALWAYS pair microsoft-learn with perplexity for version verification
- Trust perplexity for version numbers and recently-released features

## References

**Detailed Documentation:**

- [Design Principles](references/architecture/design-principles.md) - Vertical slice, DRY, config-over-hardcoding
- [Multi-Language Strategy](references/architecture/multi-language-strategy.md) - Bash, Python, TypeScript implementation patterns
- [Active Hooks](references/inventory/active-hooks.md) - Complete list of active hooks with descriptions
- [Hook Lifecycle](references/inventory/hook-lifecycle.md) - Enable/disable/modify hooks
- [Configuration Guide](references/configuration/hook-config-guide.md) - Global and per-hook configuration
- [Creating Hooks Workflow](references/development/creating-hooks-workflow.md) - Step-by-step hook creation
- [Testing Guide](references/development/testing-guide.md) - Comprehensive testing patterns
- [Best Practices](references/development/best-practices.md) - Code quality and patterns
- [Common Issues](references/troubleshooting/common-issues.md) - Known problems and solutions
- [Debugging Guide](references/troubleshooting/debugging-guide.md) - Advanced debugging techniques

**Quick Access:**

- **Hooks Directory:** `.claude/hooks/`
- **Shared Utilities:** `.claude/hooks/shared/` (includes unit tests)
- **Global Config:** `.claude/hooks/config/global.yaml`
- **Quick Reference:** `.claude/hooks/README.md`
- **Test Runner:** `.claude/hooks/test-runner.sh`
- **Official Hooks Docs:** Via docs-management skill (keywords: "hooks", "PreToolUse", "PostToolUse")

## Test Scenarios

### Scenario 1: Direct Activation

**Query**: "Use the hook-management skill to add a new hook"

**Expected Behavior**:

- Skill activates on keywords "hook-management", "add", "hook"
- Loads SKILL.md as navigation hub
- Directs user to Creating Hooks Workflow reference
- Delegates official hooks documentation to docs-management skill

**Success Criteria**: User receives step-by-step guidance for hook creation

### Scenario 2: Troubleshooting Request

**Query**: "My hook isn't running, help me debug it"

**Expected Behavior**:

- Skill activates on keywords "hook", "debug"
- Loads Common Issues or Debugging Guide reference
- Provides diagnostic steps for hook execution issues
- Delegates official hook event documentation to docs-management if needed

**Success Criteria**: User identifies and resolves hook execution issue

### Scenario 3: Configuration Change

**Query**: "How do I disable the GPG signing hook?"

**Expected Behavior**:

- Skill activates on keywords "disable", "hook", "GPG"
- Provides quick reference from Configuration Quick Reference section
- Points to Hook Lifecycle reference for detailed guidance
- Shows exact config file path and YAML syntax

**Success Criteria**: User successfully disables specific hook

### Scenario 4: Architecture Understanding

**Query**: "Explain the hooks directory structure"

**Expected Behavior**:

- Skill activates on keywords "hooks", "directory", "structure"
- Provides Directory Structure section from SKILL.md
- Links to Design Principles reference for deeper understanding
- Explains vertical slice architecture pattern

**Success Criteria**: User understands hook organization principles

### Scenario 5: Official Documentation Delegation

**Query**: "What hook events are available in Claude Code?"

**Expected Behavior**:

- Skill activates on keywords "hook events", "Claude Code"
- Recognizes this requires official documentation
- Delegates to docs-management skill with appropriate keywords
- Does NOT provide hardcoded hook event list (may become stale)

**Success Criteria**: User receives current official documentation via docs-management

## Version History

- **v1.4.3** (2026-01-16): Added Setup hook event keyword (v2.1.10)
  - Added "Setup Hook Event (v2.1.10+)" keyword section
  - Keywords: Setup hook, Setup event, --init, --init-only, --maintenance, repository setup
  - Triggers: --init, --init-only, or --maintenance CLI flags
  - Enables discovery of repository initialization/maintenance hooks

- **v1.4.2** (2026-01-16): Added PreToolUse additionalContext keyword (v2.1.9)
  - Added "PreToolUse additionalContext Return (v2.1.9+)" keyword section
  - Keywords: PreToolUse, additionalContext, hook return, context injection
  - Enables discovery of context injection via PreToolUse hook returns

- **v1.4.1** (2026-01-12): Added SessionStart agent_type keyword (v2.1.2)
  - Added "SessionStart Hook Input (v2.1.2+)" keyword section for agent_type field
  - Keywords: SessionStart, agent_type, --agent flag
  - Documents field available when --agent CLI flag is used

- **v1.4.0** (2026-01-09): Added v2.1.x frontmatter hooks keyword registry entry
  - Added "Frontmatter Hooks (v2.1.x)" keyword section for skill/agent/command hooks
  - Keywords: frontmatter hooks, skill hooks, agent hooks, command hooks, once true
  - Enables discovery of v2.1.x frontmatter hooks feature via docs-management

- **v1.3.0** (2025-12-01): Environment variable standardization
  - Standardized all hook environment variables to `CLAUDE_HOOK_{NAME}_ENABLED` pattern
  - Added authoritative "Environment Variable Convention" section as single source of truth
  - Documented hook default states (Essential=enabled, Opt-in=disabled, Log Events=disabled)
  - Documented log events special logic (master toggle + individual toggles)
  - Added keywords: CLAUDE_HOOK_ENABLED, hook environment variables, enable hook, disable hook
  - Marked legacy YAML configuration sections appropriately

- **v1.2.2** (2025-11-30): Plugin hooks delegation
  - Added decision tree entry for plugin hooks (delegates to plugin-development skill)
  - Added Plugin Hooks Delegation section with comparison table
  - Added "plugin hooks", "local hooks" keywords
  - Clarifies scope: this skill is for local hooks (`.claude/hooks/`), plugin hooks use different patterns

- **v1.2.1** (2025-11-25): Audit improvements
  - Added Test Scenarios section for activation testing
  - Added Last Audit tracking to metadata
  - Updated Last Verified date
  - Minor documentation improvements based on comprehensive audit

- **v1.2.0** (2025-11-24): Configuration architecture clarification
  - Clarified separation between `config.yaml` (user config) and `hook.yaml` (metadata)
  - Updated documentation to reference `config.yaml` for runtime configuration
  - Updated directory structure to show both configuration files
  - Updated hook-config-guide.md with dual-file configuration pattern
  - Updated creating-hooks-workflow.md with config.yaml creation step
  - Based on comprehensive hooks audit from 2025-11-24

- **v1.1.0** (2025-11-18): Progressive disclosure refactoring
  - Extracted detailed content into references/ directory (10 reference files)
  - Reduced SKILL.md from 1014 to ~350 lines (65% reduction)
  - Improved token efficiency by ~55% for common queries
  - Added Reference Loading Guide for explicit conditional loading
  - Hub architecture with clear decision tree and navigation
  - Based on audit recommendations from 2025-11-18 skill audit

- **v1.0.0** (2025-11-18): Initial release
  - Centralized hooks management documentation
  - Delegation pattern to docs-management
  - Active hooks inventory
  - Multi-language support architecture
  - Vertical slice organization
  - Comprehensive shared utilities
  - Testing framework

---

## Last Updated

**Date:** 2026-01-16
**Model:** claude-opus-4-5-20251101
