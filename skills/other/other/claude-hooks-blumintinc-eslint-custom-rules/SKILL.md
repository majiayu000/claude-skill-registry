---
name: claude-hooks
description: "Use when understanding the automated agent quality checks, hooks, and workflow system."
user-invocable: false
---

# Claude Code Hooks and GitHub Workflows System

## Purpose

This system automates the ESLint rule development lifecycle using **Claude Code Hooks** for local quality enforcement and **GitHub Workflows** for triggering agents on issue events.

## Why the System Was Built

Automation reduces manual toil by enforcing local quality gates and launching background agents so repetitive rule work does not block developers.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            GitHub Issue Created                              │
│                          (with rule-request label)                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               claude-rule-research-agent.yml (claude-research)               │
│     • Searches web for existing ESLint rules                                 │
│     • Posts findings as issue comment                                        │
│     • Labels: research-complete, claude-implement (if NO MATCH)              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                        (if NO MATCH → claude-implement)
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│             claude-implement-rule-agent.yml (claude-implement)               │
│     • Creates new branch from develop                                        │
│     • Implements rule using .claude/agents/implement-rule.md               │
│     • Claude Code Hooks enforce quality (build, lint, tests, structure)    │
│     • Opens PR on completion                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Definitions

| Term | Description |
|------|-------------|
| **Claude Code Hook** | Lifecycle event handler that runs automated checks at key agent milestones |
| **Stop Hook** | Quality gate that blocks completion until required checks succeed |
| **Validation Loop** | Iterative rerun cycle triggered by failing checks, bounded by MAX_LOOPS to avoid infinite prompting |
| **Quality Gate** | Ordered set of build, lint, test, and structure checks applied before an agent can finish |
| **Rule Implementation Lifecycle** | Multi-stage flow from issue triage through research, implementation, validation, and PR creation |

## Core Components

- Claude Code Hooks: Local lifecycle scripts that enforce lint/build/test and prompt tracking on every agent run.
- GitHub Workflows: Issue and review triggers that launch background agents for research, implementation, and bug fixes.
- Validation Layers: Stop hook checks that gate completion on build, lint, tests, and rule structure for reliability.
- Change Log: Per-session file tracking that keeps prompts idempotent and resumes validation across loops.

## How It Makes Developers' Lives Easier

- Automated quality gates prevent manual babysitting of lint/build/test steps.
- Structured prompts and rule scaffolding reduce errors and keep implementations consistent.
- Loop prevention and concurrency controls avoid duplicated agent runs and wasted API cycles.

## Directory Structure

```
.claude/
├── settings.json                        # Hook configuration
├── hooks/
│   ├── stop.sh                          # Stop hook entry point
│   ├── track-changes.sh                 # File change tracking
│   ├── track-prompt.sh                  # Prompt tracking & rule-request detection
│   └── skill-activation-llm-eval.sh    # Forces explicit skill evaluation
├── agents/
│   ├── implement-rule.md                # New rule implementation guide
│   └── fix-bug.md                       # Bug fix guide
├── skills/
│   ├── task-completion-standards/SKILL.md  # Quality checklist
│   └── claude-hooks/SKILL.md           # This documentation
└── tmp/
    └── hooks/
        └── agent-change-log.json        # Auto-created change log

scripts/
├── check-merge-conflicts.sh          # Lists remaining conflicted files (merge conflict stop hook)
├── claude-hooks/
│   ├── agent-check.ts                   # Main stop hook logic
│   ├── change-log.ts                    # Change log utilities
│   ├── lint-diff.ts                     # Lint changed files only
│   ├── merge-conflict-check.ts          # Merge conflict stop logic (Priority 0)
│   ├── pr-review-check.ts               # PR review comment check for stop hook (Priority 1)
│   ├── track-changes.ts                 # Track file modifications
│   ├── track-prompt.ts                  # Track prompts & detect flags
│   ├── types.ts                         # Shared TypeScript types
│   └── validate-rule-structure.ts       # Validate rule has all files
├── cli/
│   ├── git-utils.ts                     # Git CLI utilities
│   └── git-merge/                       # Merge-conflict context utilities
│       ├── types.ts
│       ├── isInMergeConflictState.ts
│       ├── getConflictedFiles.ts
│       ├── getMergeBase.ts
│       ├── getSquashedDiff.ts
│       ├── getBranchLastCommitDate.ts
│       ├── getAssociatedPr.ts
│       ├── fetchPrMetadata.ts
│       └── buildMergeContext.ts
└── github/
    └── post-research-comment.ts         # Post research findings to issue

.github/workflows/
├── claude-rule-research-agent.yml       # Research existing rules
├── claude-implement-rule-agent.yml      # Implement new rules
└── claude-fix-bug-agent.yml             # Fix bugs in rules
```

## GitHub Labels

| Label | Purpose |
|-------|---------|
| `rule-request` | New ESLint rule request |
| `bug` | Bug in existing rule |
| `claude-research` | Triggers research workflow |
| `research-complete` | Research has been performed |
| `claude-implement` | Triggers implementation workflow |
| `claude-fix` | Triggers bug fix workflow |

## Workflow Details

### 1. Research Workflow (`claude-rule-research-agent.yml`)

**Trigger**: Issue labeled with `claude-research`

**Purpose**: Search for existing ESLint rules before implementing

**Flow**:
1. Check if research comment already exists (short-circuit)
2. Launch agent to search web
3. Agent writes findings to `.claude/tmp/research-results.md`
4. Agent runs `post-research-comment.ts` which:
   - Posts findings as issue comment
   - Removes `claude-research` label
   - Adds `research-complete` label
   - If NO MATCH: Adds `claude-implement` label

### 2. Implementation Workflow (`claude-implement-rule-agent.yml`)

**Trigger**: Issue labeled with `claude-implement` (requires `rule-request` + `research-complete`)

**Purpose**: Implement new ESLint rule

**Flow**:
1. Create branch: `develop-implement-rule-{issue_number}`
2. Build prompt from `.claude/agents/implement-rule.md` + issue body
3. Include `<!-- rule-request -->` flag for expanded test prompts
4. Launch Claude Code agent
5. Claude Code Hooks enforce quality until completion
6. Open PR targeting `develop`

### 3. Bug Fix Workflow (`claude-fix-bug-agent.yml`)

**Trigger**: Issue labeled with `claude-fix` (requires `bug`)

**Purpose**: Fix bugs in existing rules

**Flow**:
1. Create branch: `develop-fix-bug-{issue_number}`
2. Build prompt from `.claude/agents/fix-bug.md` + issue body
3. No `<!-- rule-request -->` flag (skip expanded test prompts)
4. Launch Claude Code agent
5. Claude Code Hooks enforce quality until completion
6. Open PR targeting `develop`

## Claude Code Hooks System

### Hook Configuration (`.claude/settings.json`)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/track-changes.sh" }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": ".claude/hooks/track-prompt.sh" },
          { "type": "command", "command": ".claude/hooks/skill-activation-llm-eval.sh" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": ".claude/hooks/stop.sh" }]
      }
    ]
  }
}
```

### Hook Input/Output Formats

**PostToolUse (track-changes)**:

```json
{
  "session_id": "abc123",
  "tool_use_id": "tool_xyz",
  "tool_name": "Edit",
  "tool_input": { "file_path": "src/rules/my-rule.ts" },
  "cwd": "/path/to/repo"
}
```

**UserPromptSubmit (track-prompt)**:

```json
{
  "hook_event_name": "UserPromptSubmit",
  "session_id": "abc123",
  "prompt": "Implement the my-rule ESLint rule <!-- rule-request -->"
}
```
Output: `{}` (empty object allows prompt through)

**Stop (agent-check)**:

```json
{
  "session_id": "abc123",
  "transcript_path": "/tmp/transcript.jsonl",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```
Output: `{ "decision": "block", "reason": "..." }` to block, `{}` to allow stop.

### Stop Hook Execution Order

1. **Heartbeat Update**: Record activity timestamp
2. **Status Check**: Skip checks if `stop_hook_active === true` (prevents infinite loops)
3. **Merge Conflict Check (Priority 0)**: If a `git merge` is in progress and conflicts remain, block completion and provide a fresh conflict-resolution prompt. Use `npm run address-merge-conflicts` to generate the initial prompt.
4. **PR Review Check (Priority 1)**: For PR review branches (`*-review-pr-*`), check for unresolved comments (see `.claude/skills/automated-review-addressing/SKILL.md`)
5. **Build Validation**: `npm run build` must succeed
6. **Linting Validation**: ESLint on changed files only
7. **Test Validation**: `npm test` must pass
8. **Rule Structure Validation**: For rule implementations, verify:
   - `src/rules/{rule-name}.ts` exists
   - `src/tests/{rule-name}.test.ts` exists
   - `docs/rules/{rule-name}.md` exists
   - `src/index.ts` updated in 3 places (import, config, rules)
   - `README.md` mentions the rule
9. **Check-Your-Work Prompt**: Self-review prompt
10. **Expand Tests Prompt**: For rule implementations only (requires 20+ tests)

#### Critical Insights for Maintainers

- Order is fail-fast by design: stop on build errors before lint/test to avoid long runs on broken builds, prevent expensive lint/test runs, and reduce agent API costs.
- Common pain points: flaky tests or slow lint/test runs can loop; rerun locally with the same commands in stop.sh and scope to changed files when possible.
- Rule structure validation loops if required files are missing or src/index.ts exports are incomplete; ensure all items in the checklist above exist before reruns.
- MAX_LOOPS in change-log.ts prevents infinite prompting; increase only when intentionally allowing longer runs.
- Hook side-effects cascade: PR review checks can short-circuit quality checks, and change-log updates influence later prompts; watch the console output to see which stage stopped the run.

### Rule Request Detection

The `<!-- rule-request -->` flag in the first prompt marks conversations as rule implementations:

```typescript
function detectRuleRequestFlag(prompt: string): boolean {
  return prompt.includes('<!-- rule-request -->');
}
```

This triggers the "Expand Tests" prompt after the first "Check Your Work" prompt.

### Change Log Structure

`.claude/tmp/hooks/agent-change-log.json`:

```json
{
  "session-abc123": {
    "_metadata": {
      "hasCheckWorkPrompted": true,
      "hasExpandTestsPrompted": false,
      "isRuleRequest": true,
      "lastUserMessage": "...",
      "endTimestamp": null,
      "lastActivityTimestamp": 1700000100000
    },
    "tool-use-xyz": ["src/rules/new-rule.ts", "src/tests/new-rule.test.ts"]
  }
}
```

## Quality Enforcement

### Required Files for New Rules

1. `src/rules/{rule-name}.ts` - Rule implementation
2. `src/tests/{rule-name}.test.ts` - Test suite (20+ tests required)
3. `docs/rules/{rule-name}.md` - Documentation
4. `src/index.ts` updates:
   - Import statement
   - `configs.recommended.rules` entry
   - `rules` object entry
5. `README.md` mention

### Test Requirements

- Minimum 20 tests per rule
- 10+ valid cases (code that should NOT trigger)
- 10+ invalid cases (code that SHOULD trigger)
- Edge cases from issue specification
- Auto-fix tests if rule has `fixable: 'code'`

## Loop Prevention

The system uses `MAX_LOOPS = 200` to prevent infinite loops. After 200 iterations, agents complete even if checks fail.

## GitHub Secrets Required

| Secret | Purpose |
|--------|---------|
| `CURSOR_API_KEY` | API authentication for background agents |
| `GITHUB_TOKEN` | Auto-provided, used for issue/PR operations |

## Common Issues

### Agent Stuck in Loop

If an agent keeps failing the same check:
- Check the error output in the agent conversation
- The agent will auto-stop after MAX_LOOPS iterations
- Review the failing validation and fix manually if needed

### Research Workflow Not Triggering

- Ensure issue has `claude-research` label
- Check if research comment already exists (short-circuit logic)
- Verify `CURSOR_API_KEY` secret is configured

### Implementation Workflow Not Triggering

- Requires all three labels: `rule-request`, `research-complete`, `claude-implement`
- Research workflow auto-adds `claude-implement` only on NO MATCH
- For MATCH cases, human must decide to proceed

### Structure Validation Failing

Common mistakes:
1. Missing import in `src/index.ts`
2. Missing entry in `configs.recommended.rules`
3. Missing entry in `rules` object
4. Documentation not created
5. README not updated

## Development Tips

### Running Hooks Locally

```bash
# Test stop hook
echo '{"session_id":"test","hook_event_name":"Stop","stop_hook_active":false,"transcript_path":"/tmp/x.jsonl","permission_mode":"default"}' \
  | npx tsx scripts/claude-hooks/agent-check.ts

# Test lint-diff
npx tsx scripts/claude-hooks/lint-diff.ts --conversation-id "test"

# Test validate-rule-structure
node -e "const {validateRuleStructure} = require('./scripts/claude-hooks/validate-rule-structure'); console.log(validateRuleStructure('my-rule-name'));"
```

### Debugging Change Log

```bash
# View current change log
cat .claude/tmp/hooks/agent-change-log.json | jq .

# Clear change log (for testing)
rm .claude/tmp/hooks/agent-change-log.json
```

### Verifying Script Execution

```bash
# Ensure shell scripts are executable
chmod +x .claude/hooks/*.sh

# Test shell script directly
echo '{"session_id":"test","hook_event_name":"Stop","stop_hook_active":false,"transcript_path":"/tmp/x.jsonl","permission_mode":"default","cwd":"/path/to/repo"}' \
  | .claude/hooks/stop.sh
```
