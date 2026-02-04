---
name: legal-sanity
description: "Scan code for client project names, proprietary tool references, and legally sensitive content"
version: 1.0.0
category: workspace-hub
capabilities:
  - legal_reference_scanning
  - client_name_detection
  - deny_list_management
tools:
  - Bash
  - Read
  - Glob
  - Grep
related_skills:
  - compliance-check
---

# Legal Sanity Skill

> Version: 1.0.0
> Category: Workspace
> Trigger: Before PRs, after code porting, on demand

## Quick Start

```bash
# Scan a specific submodule
./scripts/legal/legal-sanity-scan.sh --repo=worldenergydata

# Scan all submodules
./scripts/legal/legal-sanity-scan.sh --all

# Scan only git-changed files (fast mode for PRs)
./scripts/legal/legal-sanity-scan.sh --repo=worldenergydata --diff-only

# JSON output for automation
./scripts/legal/legal-sanity-scan.sh --repo=worldenergydata --json
```

## When to Use

- **After code porting**: Any time code is imported from a client project
- **Before PR creation**: Automated via pr-manager pre-hooks
- **During cross-review**: Runs as a mandatory pre-gate before Codex/Gemini
- **On demand**: When adding new deny-list patterns or auditing repos

## How It Works

1. **Deny lists** define patterns to block:
   - Global: `.legal-deny-list.yaml` (workspace root)
   - Per-project: `<submodule>/.legal-deny-list.yaml`
2. **Scanner** merges both lists and runs `rg` (ripgrep) against the target
3. **Exclusions** skip files like `.git/`, `*.md`, `*.lock`
4. **Exit code**: 0 = pass, 1 = block violations found

## Deny List Format

```yaml
version: "1.0"
updated: "2026-02-02"

client_references:
  - pattern: "CLIENT_NAME"
    case_sensitive: true
    description: "Why this is blocked"

proprietary_tools:
  - pattern: "ToolName"
    case_sensitive: false
    description: "Client proprietary tool"

exclusions:
  - ".legal-deny-list.yaml"
  - ".git/"

default_severity: "block"
```

## Execution Checklist

When invoked as a skill:

1. Identify target scope (specific repo, all repos, or diff-only)
2. Run the scan script with appropriate flags
3. If violations found:
   - List each violation with file:line detail
   - Suggest replacement text
   - Block PR creation until resolved
4. If clean:
   - Report PASS
   - Proceed to next review gate

## Output Format

### Terminal (default)
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Legal Sanity Scanner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scanning: worldenergydata
  RESULT: PASS — no violations found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### JSON (`--json`)
```json
{"repo":"worldenergydata","pattern":"ENIGMA","file":"src/main.py","line":42,"severity":"block"}
```

## Related

- Rule file: `.claude/rules/legal-compliance.md`
- Workflow: `.claude/skills/_internal/workflows/legal-sanity-review/SKILL.md`
- Cross-review: `.claude/skills/_internal/workflows/cross-review-policy/SKILL.md`
