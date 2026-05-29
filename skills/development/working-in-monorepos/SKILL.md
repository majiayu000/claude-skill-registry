---
name: working-in-monorepos
description: Use when working in repositories with multiple subprojects (monorepos) where commands need to run from specific directories - prevents directory confusion, redundant cd commands, and ensures commands execute from correct locations
---

# Working in Monorepos

## Overview

Helps Claude work effectively in monorepo environments by ensuring commands always execute from the correct location using absolute paths.

**Core principle:** Bash shell state is not guaranteed between commands. Always use absolute paths.

**Announce at start:** "I'm using the working-in-monorepos skill."

## When to Use

Use this skill when:

- Repository contains multiple subprojects (ruby/, cli/, components/\*, etc.)
- Commands must run from specific directories
- Working across multiple subprojects in one session

Don't use for:

- Single-project repositories
- Repositories where all commands run from root

## The Iron Rule: Always Use Absolute Paths

When executing ANY command in a monorepo subproject:

✅ **CORRECT:**

```bash
cd /Users/josh/workspace/schemaflow/ruby && bundle exec rspec
cd /Users/josh/workspace/schemaflow/cli && npm test
```

❌ **WRONG:**

```bash
# Relative paths (assumes current directory)
cd ruby && bundle exec rspec

# No cd prefix (assumes location)
bundle exec rspec

# Chaining cd (compounds errors)
cd ruby && cd ruby && rspec
```

**Why:** You cannot rely on shell state. Absolute paths guarantee correct execution location regardless of where the shell currently is.

## Constructing Absolute Paths

### With .monorepo.json Config

If `.monorepo.json` exists at repo root:

1. Read `root` field for absolute repo path
2. Read subproject `path` from `subprojects` map
3. Construct: `cd {root}/{path} && command`

Example:

```json
{
  "root": "/Users/josh/workspace/schemaflow",
  "subprojects": { "ruby": { "path": "ruby" } }
}
```

→ `cd /Users/josh/workspace/schemaflow/ruby && bundle exec rspec`

### Without Config

Use git to find repo root, then construct absolute path:

1. First get the repo root: `git rev-parse --show-toplevel`
2. Use that absolute path: `cd /absolute/path/to/repo/ruby && bundle exec rspec`

**Example workflow:**

```bash
# Step 1: Get repo root
git rev-parse --show-toplevel
# Output: /Users/josh/workspace/schemaflow

# Step 2: Use absolute path in commands
cd /Users/josh/workspace/schemaflow/ruby && bundle exec rspec
```

**Why not use command substitution:** `cd $(git rev-parse --show-toplevel)/ruby` requires user approval. Instead, run `git rev-parse` once, then use the absolute path directly in all subsequent commands.

**⚠️ Git subtree caveat:** In repositories containing git subtrees (nested git repos), `git rev-parse --show-toplevel` returns the innermost repo root, not the monorepo root. This makes it unreliable for subtree scenarios. Creating a `.monorepo.json` config is the robust solution that works in all cases.

## Workflow When Working Without Config

When working in a repo without `.monorepo.json`:

1. **Get repo root ONCE at start of session:** Run `git rev-parse --show-toplevel`
2. **Store the result mentally:** e.g., `/Users/josh/workspace/schemaflow`
3. **Use absolute paths for ALL commands:** `cd /Users/josh/workspace/schemaflow/subproject && command`

**Do NOT use command substitution like `cd $(git rev-parse --show-toplevel)/subproject`** - this requires user approval every time. Get the path once, then use it directly.

**Important limitation:** `git rev-parse --show-toplevel` may not work correctly in repositories with git subtrees (nested git repos), as it returns the innermost repository root. For subtree scenarios, a `.monorepo.json` config is strongly recommended to explicitly define the true monorepo root.

## Setup Workflow (No Config Present)

When skill activates in a repo without `.monorepo.json`:

1. **Detect:** "I notice this appears to be a monorepo without a .monorepo.json config."
2. **Offer:** "I can run ~/.claude/skills/working-in-monorepos/scripts/monorepo-init to auto-detect subprojects and generate config. Would you like me to?"
3. **User accepts:** Run `~/.claude/skills/working-in-monorepos/scripts/monorepo-init --dry-run`, show output, ask for approval, then `~/.claude/skills/working-in-monorepos/scripts/monorepo-init --write`
4. **User declines:** "No problem. I'll get the repo root once with git rev-parse and use absolute paths for all commands."
5. **User wants custom:** "You can also create .monorepo.json manually. See example below."

**Helper Script Philosophy:**

The `monorepo-init` script is designed as a **black-box tool**:

- **Always run with `--help` first** to see usage
- **DO NOT read the script source** unless absolutely necessary - it pollutes your context window
- The script exists to be called directly, not analyzed
- All necessary usage information is in the help output

**Script Location:**

The script is located at `~/.claude/skills/working-in-monorepos/scripts/monorepo-init` (absolute path). Since skills are symlinked from the dotfiles repo via `home/.claude/skills/` → `~/.claude/skills/`, this path works universally regardless of which project directory you're currently in.

```bash
# Run from any directory - use the absolute path
~/.claude/skills/working-in-monorepos/scripts/monorepo-init --help
~/.claude/skills/working-in-monorepos/scripts/monorepo-init --dry-run
~/.claude/skills/working-in-monorepos/scripts/monorepo-init --write
```

## Command Execution Rules (With Config)

If `.monorepo.json` defines command rules:

```json
{
  "commands": {
    "rubocop": { "location": "root" },
    "rspec": {
      "location": "subproject",
      "command": "bundle exec rspec",
      "overrides": { "root": { "command": "bin/rspec" } }
    }
  }
}
```

**Check rules before executing:**

1. Look up command in `commands` map
2. Check `location`: "root" | "subproject"
3. Check for `command` override
4. Check for context-specific `overrides`

**Example:**

- rubocop: Always run from repo root
- rspec in ruby/: Use `bundle exec rspec`
- rspec in root project: Use `bin/rspec`

## Common Mistakes to Prevent

❌ **"I just used cd, so I'm in the right directory"**
Reality: You cannot track shell state reliably. Always use absolute paths.

❌ **"The shell remembers where I am"**
Reality: Shell state is not guaranteed between commands. Always use absolute paths.

❌ **"It's wasteful to cd every time"**
Reality: Explicitness prevents bugs. Always use absolute paths.

❌ **"Relative paths are simpler"**
Reality: They break when assumptions are wrong. Always use absolute paths.

## Quick Reference

| Task                    | Command Pattern                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| Get repo root           | `git rev-parse --show-toplevel` (run once, use result in all commands)                                  |
| Run tests in subproject | `cd /absolute/path/to/repo/subproject && test-command`                                                  |
| With config             | `cd {root}/{subproject.path} && command`                                                                |
| Check for config        | `test -f .monorepo.json`                                                                                |
| Generate config         | `~/.claude/skills/working-in-monorepos/scripts/monorepo-init --dry-run` (works from any directory)      |
| Always rule             | Use absolute path + cd prefix for EVERY command. Get repo root first, then use absolute paths directly. |

## Configuration Schema

`.monorepo.json` at repository root:

```json
{
  "root": "/absolute/path/to/repo",
  "subprojects": {
    "subproject-id": {
      "path": "relative/path",
      "type": "ruby|node|go|python|rust|java",
      "description": "Optional"
    }
  },
  "commands": {
    "command-name": {
      "location": "root|subproject",
      "command": "optional override",
      "overrides": {
        "context": { "command": "context-specific" }
      }
    }
  }
}
```

**Minimal example:**

```json
{
  "root": "/Users/josh/workspace/schemaflow",
  "subprojects": {
    "ruby": { "path": "ruby", "type": "ruby" },
    "cli": { "path": "cli", "type": "node" }
  }
}
```
