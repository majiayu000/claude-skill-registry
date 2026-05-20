---
name: sync-claude
description: |
  Synchronize and validate Claude documentation (CLAUDE.md files and skills) before commits.
  Ensures documentation accuracy by validating all claims against actual codebase state.

  Use when: (1) Before creating a PR to ensure docs are accurate, (2) After making changes
  that might invalidate documentation claims, (3) When explicitly syncing Claude docs,
  (4) When reviewing documentation for staleness.

  Triggers: "sync claude", "validate claude docs", "check documentation", "update CLAUDE.md",
  "before commit", "docs out of sync", "/sync-claude", "stale documentation"

  Two modes:
  - full: Exhaustive validation of all Claude docs in repository
  - changed: Smart detection of docs affected by current branch changes
user-invocable: false
---

# Claude Documentation Sync

Validate and synchronize all Claude-related documentation before commits.

## Quick Start

```
Mode selection:
- full    → Exhaustive validation of all docs
- changed → Only docs affected by current branch (default)
```

## Execution Flow

### Phase 1: Discovery

**Full mode**: Find all Claude docs in repository:
- `**/CLAUDE.md` (excluding `.terragrunt-cache/`, `.terragrunt-stack/`)
- `.claude/skills/*/SKILL.md`
- `.claude/skills/*/references/*.md`

**Changed mode**: Analyze branch diff:
1. Get changed files: `git diff --name-only origin/main...HEAD`
2. Find directly modified Claude docs
3. Find docs that reference changed paths (smart detection)

### Phase 2: Parallel Validation (Haiku Agents)

Spawn parallel Haiku agents organized by validation type:

#### Agent Group A: Path Validators (by directory)
One agent per major directory validates file/directory references:
- `infrastructure/` paths
- `kubernetes/` paths
- `.taskfiles/` paths
- Root and other paths

**Validation checks:**
- File paths mentioned exist: `[path/to/file](path/to/file)`
- Directory paths exist: `infrastructure/modules/`
- Glob patterns return results: `**/*.tf`

#### Agent Group B: Code Reference Validators
Validate code-level claims:
- Function/class names exist where documented
- Line number references are approximately accurate (±10 lines)
- Variable names in examples exist in referenced files

#### Agent Group C: Command Validators
Validate command examples:
- `task <name>` commands exist in Taskfile
- CLI tools referenced are in Brewfile
- Command syntax is valid (dry-run where safe)

#### Agent Group D: Cross-Reference Validators
Validate documentation consistency:
- Skill references in CLAUDE.md match actual skills
- Table entries match actual directories
- Runbook references exist

### Phase 3: Aggregation

Collect results from all agents into a unified report:

```
┌─────────────────────────────────────────────────────────────┐
│ SYNC-CLAUDE VALIDATION REPORT                               │
├─────────────────────────────────────────────────────────────┤
│ Mode: [full|changed]                                        │
│ Docs Scanned: N                                             │
│ Issues Found: N                                             │
├─────────────────────────────────────────────────────────────┤
│ ISSUES BY CATEGORY:                                         │
│                                                             │
│ 🔴 Path References (N issues)                               │
│   • infrastructure/CLAUDE.md:45 - path not found            │
│     Referenced: infrastructure/units/foo/                   │
│     Suggestion: Path was renamed to infrastructure/units/bar│
│                                                             │
│ 🟡 Command References (N issues)                            │
│   • .taskfiles/CLAUDE.md:67 - task not found                │
│     Referenced: task tg:deploy-live                         │
│     Suggestion: Task was renamed to task tg:apply-live      │
│                                                             │
│ 🟢 Valid References: N                                      │
└─────────────────────────────────────────────────────────────┘
```

### Phase 4: Opus Validation

Spawn Opus agent to:
1. Review aggregated findings
2. Prioritize by impact (breaking vs cosmetic)
3. Generate proposed edits for each issue
4. Present final change list for approval

## Agent Prompts

### Discovery Agent (Haiku)

```
Discover all Claude documentation files in the repository.

Search patterns:
- **/CLAUDE.md (exclude .terragrunt-cache/, .terragrunt-stack/)
- .claude/skills/*/SKILL.md
- .claude/skills/*/references/*.md

For each file found, extract:
1. All file path references (markdown links, code blocks)
2. All directory references
3. All command examples (task, kubectl, git, etc.)
4. All cross-references to other docs/skills

Return structured JSON:
{
  "file": "path/to/doc.md",
  "path_refs": ["path1", "path2"],
  "dir_refs": ["dir1/", "dir2/"],
  "commands": ["task foo", "kubectl get"],
  "cross_refs": ["skill:name", "doc:path"]
}
```

### Path Validator Agent (Haiku)

```
Validate file and directory references in Claude documentation.

Input: List of {doc_path, references}

For each reference:
1. Check if path exists using Glob/Read
2. If not found, search for similar paths (fuzzy match)
3. Determine if path was renamed, moved, or deleted

Return:
{
  "valid": [...],
  "invalid": [
    {
      "doc": "path/to/doc.md",
      "line": 45,
      "reference": "infrastructure/foo/",
      "status": "not_found",
      "suggestion": "Renamed to infrastructure/bar/"
    }
  ]
}
```

### Command Validator Agent (Haiku)

```
Validate command examples in Claude documentation.

Input: List of {doc_path, commands}

Validation steps:
1. task commands: Verify in Taskfile.yaml or .taskfiles/*
2. CLI tools: Verify in Brewfile
3. kubectl commands: Syntax check only (no cluster access)
4. git commands: Syntax validation

Return:
{
  "valid": [...],
  "invalid": [
    {
      "doc": "path/to/doc.md",
      "line": 67,
      "command": "task tg:deploy",
      "status": "task_not_found",
      "suggestion": "Did you mean: task tg:apply-*"
    }
  ]
}
```

### Change Impact Analyzer (Haiku) - Changed Mode Only

```
Analyze git diff to find impacted documentation.

Steps:
1. Parse diff: git diff --name-only origin/main...HEAD
2. For each changed file, find docs that might reference it:
   - Direct path references
   - Parent directory references
   - Related command references (if Taskfile changed)
3. Include any directly modified Claude docs

Return list of doc paths requiring validation.
```

### Opus Validator Agent

```
Review sync-claude validation results and propose fixes.

Input: Aggregated validation results from all Haiku agents

Tasks:
1. Deduplicate findings
2. Categorize by severity:
   - CRITICAL: Broken references users will hit
   - WARNING: Outdated but still functional
   - INFO: Style/cosmetic issues
3. For each issue, generate a proposed Edit:
   - old_string: exact text to replace
   - new_string: corrected text
4. Verify proposed edits don't break other references

Output format:
{
  "summary": {
    "total_issues": N,
    "critical": N,
    "warning": N,
    "info": N
  },
  "proposed_edits": [
    {
      "file": "path/to/doc.md",
      "severity": "CRITICAL",
      "description": "Fix broken path reference",
      "old_string": "[foo](infrastructure/foo/)",
      "new_string": "[foo](infrastructure/bar/)"
    }
  ]
}

Present edits for user approval before applying.
```

## Mode Selection Logic

```
IF user specifies mode:
  USE specified mode
ELSE IF on main branch:
  USE full mode
ELSE IF branch has commits ahead of origin/main:
  USE changed mode
ELSE:
  USE full mode (no changes to analyze)
```

## Exclusions

Always exclude from scanning:
- `.terragrunt-cache/`
- `.terragrunt-stack/`
- `node_modules/`
- `.git/`
- `*.rendered/`

## Error Handling

If an agent fails:
1. Log the failure with context
2. Continue with other agents
3. Mark affected validations as "INCOMPLETE"
4. Include in final report for manual review
