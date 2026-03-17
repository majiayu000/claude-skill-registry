---
name: ralph-zero
description: "Next-generation autonomous development orchestrator with cognitive feedback loops. Executes complex multi-step features from PRDs through iterative agent sessions with quality verification, context synthesis, and recursive learning. Use when implementing features that require multiple stories, exceed single context windows, or need autonomous execution with quality guarantees. Replaces manual iteration with intelligent orchestration."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Amp, and other Agent Skills-compatible agents. Requires Python 3.10+, git, and jq."
metadata:
  author: ralph-zero-team
  version: "0.1.0"
  category: development-automation
  homepage: https://github.com/davidkimai/ralph-zero
  tags: ["automation", "development", "prd", "autonomous", "quality-driven", "cognitive-feedback"]
---

# Ralph Zero: Next-Generation Autonomous Development

Ralph Zero is an intelligent orchestration system that autonomously implements complex features by breaking them into verifiable stories and executing each through fresh agent iterations with comprehensive quality verification and cognitive feedback loops.

## What Makes Ralph Zero Different

Ralph Zero is **not** the original bash-based Ralph implementations. It is a complete reimagining that combines:

1. **Universal Agent Compatibility** - Works with any Agent Skills-compatible agent (Claude Code, Cursor, Copilot, Amp)
2. **Python-Based Orchestration** - Robust meta-layer with intelligent state management and context synthesis
3. **Cognitive Feedback Loops** - System learns and improves via mandatory `AGENTS.md` pattern documentation
4. **Context Synthesizer** - Universal "memory injection" that works across all agents, not just those with auto-handoff
5. **Quality-Driven Execution** - Configurable gates (typecheck, tests, browser verification) enforce standards

## When to Use Ralph Zero

✅ **Use Ralph Zero when:**
- Implementing features with 3+ atomic, verifiable user stories
- Working on features too complex for single agent session
- Need autonomous execution with quality guarantees
- Want the system to learn patterns as it works
- Have well-defined acceptance criteria per story
- Project has automated quality checks (typecheck, tests)

❌ **Don't use for:**
- Single-file changes or quick fixes
- Exploratory coding without clear requirements
- Projects without type safety or automated tests
- Urgent hotfixes requiring immediate human oversight

## Quick Start

### 1. Installation

**Project-local installation** (recommended):
```bash
# From your project root
git clone https://github.com/davidkimai/ralph-zero.git .claude/skills/ralph-zero
cd .claude/skills/ralph-zero
pip install -e .
```

**Global installation:**
```bash
git clone https://github.com/davidkimai/ralph-zero.git ~/.claude/skills/ralph-zero
cd ~/.claude/skills/ralph-zero
pip install -e .
```

For other agents, adjust the skills directory:
- Cursor: `~/.cursor/skills/ralph-zero`
- VS Code Copilot: `~/.vscode/copilot/skills/ralph-zero`
- Amp: `~/.config/amp/skills/ralph-zero`

### 2. Create a PRD

Use the `prd` sub-skill to generate structured requirements:

```
Load the prd skill and create a PRD for [describe your feature]
```

Example:
```
Load the prd skill and create a PRD for adding task priority levels with filtering
```

The skill guides you through clarifying questions and generates `tasks/prd-[feature-name].md`.

### 3. Convert PRD to prd.json

Use the `ralph-convert` sub-skill:

```
Load ralph-convert skill and convert tasks/prd-task-priority.md to prd.json
```

This validates story structure, checks dependencies, and generates `prd.json` with all stories marked incomplete.

### 4. Run Ralph Zero

**Via CLI (direct execution):**
```bash
ralph-zero run --max-iterations 50
```

**Via your agent:**
```
Load ralph-zero skill and run autonomous loop with max 50 iterations
```

Ralph Zero will:
- Create/checkout feature branch from PRD
- Work through stories in priority order
- Run quality gates after each story
- Commit only if gates pass
- Update `prd.json` and `progress.txt`
- Continue until all stories pass or max iterations reached

## How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│     Python Orchestrator (ralph_zero.py)    │
│                                             │
│  • Context Synthesizer (AGENTS.md + progress)
│  • Quality Gates (typecheck, tests, etc.)  │
│  • State Manager (atomic prd.json updates) │
│  • Librarian Check (enforces learning)     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
      ┌───────────────────────┐
      │  Fresh Agent Instance │
      │  (stateless per story)│
      └───────────────────────┘
                  │
                  ▼
      ┌───────────────────────┐
      │   Persistent State    │
      │  • prd.json (tasks)   │
      │  • AGENTS.md (patterns)
      │  • progress.txt (history)
      └───────────────────────┘
```

### Key Principles

1. **Stateless Iterations**: Each story gets a fresh agent instance with no conversation memory
2. **Synthesized Context**: Orchestrator injects AGENTS.md + recent progress as "memory"
3. **Quality Gates**: Code must pass all blocking checks before commit
4. **Cognitive Feedback**: Agents update AGENTS.md with discovered patterns
5. **Atomic Stories**: Each story completable in one context window (~30min-2hrs)

## Sub-Skills

Ralph Zero includes helper skills for the full autonomous development workflow:

- **[prd](skills/prd/SKILL.md)** - Generate structured PRD from feature description
- **[ralph-convert](skills/ralph-convert/SKILL.md)** - Convert markdown PRD to prd.json
- **[ralph-execute](skills/ralph-execute/SKILL.md)** - Execute autonomous development loop

## Configuration

Create `ralph.json` in your project root:

```json
{
  "agent_command": "auto",
  "max_iterations": 50,
  "quality_gates": {
    "typecheck": {
      "cmd": "npm run typecheck",
      "blocking": true,
      "timeout": 60
    },
    "test": {
      "cmd": "npm test",
      "blocking": true,
      "timeout": 120
    }
  },
  "git": {
    "commit_prefix": "[Ralph]",
    "auto_create_branch": true
  },
  "librarian": {
    "check_enabled": true,
    "warning_after_iterations": 3
  }
}
```

See [assets/examples/ralph.json](assets/examples/ralph.json) for complete example.

## CLI Commands

Ralph Zero provides a comprehensive CLI:

```bash
# Run autonomous loop
ralph-zero run [--max-iterations N] [--config PATH]

# Validate prd.json and configuration
ralph-zero validate [--config PATH]

# Show current status
ralph-zero status [--verbose]

# Manually archive current run
ralph-zero archive <branch_name>
```

## Project Files

Ralph Zero creates and manages these files:

| File | Purpose | Created By |
|------|---------|------------|
| `prd.json` | Task list with completion status | ralph-convert |
| `progress.txt` | Append-only iteration log | Ralph Zero |
| `AGENTS.md` | Learned patterns (optional) | You or Ralph Zero |
| `ralph.json` | Project configuration (optional) | You |
| `orchestrator.log` | Detailed debug log | Ralph Zero |
| `archive/` | Completed feature archives | Ralph Zero |

## Story Requirements

For Ralph Zero to work effectively:

### ✅ Right-Sized Stories
Each story must be completable in one iteration.

**Good examples:**
- "Add status column to database with migration"
- "Create StatusBadge component with color logic"
- "Add filter dropdown to task list header"

**Too large (split these):**
- "Build entire dashboard" → 5-10 smaller stories
- "Add authentication system" → 8-12 smaller stories

### ✅ Verifiable Acceptance Criteria
Every story **must** include "Typecheck passes" as final criterion.

**Good criteria:**
- "Add status column: 'pending' | 'in_progress' | 'done'"
- "Badge colors: gray=pending, blue=in_progress, green=done"
- "Typecheck passes"

**Bad criteria (too vague):**
- "Works correctly"
- "Good UX"
- "Handles edge cases"

### ✅ Dependency Ordering
Stories execute in priority order. No forward dependencies.

**Correct order:**
1. Database schema/migrations
2. Backend logic/API
3. UI components
4. Dashboards/views

## Cognitive Feedback Loop

Ralph Zero enforces learning via the **Librarian Check**:

- Tracks code changes vs AGENTS.md updates
- Warns if patterns not documented after 3 iterations
- Ensures knowledge compounds across iterations

**Good AGENTS.md entries:**
```markdown
## Pattern: SQL Aggregations
Use `sql<number>` template literal for complex queries
Example: `const result = await sql<number>`SELECT SUM(amount) FROM...``

## Gotcha: Migration Order
Always run migrations before starting dev server.
Stale schema causes confusing typecheck errors.
```

## Advanced Usage

### Parallel Execution

Use git worktrees for concurrent feature development:

```bash
git worktree add ../feature-a ralph/feature-a
git worktree add ../feature-b ralph/feature-b

cd ../feature-a && ralph-zero run
cd ../feature-b && ralph-zero run
```

### Custom Quality Gates

Add project-specific checks to `ralph.json`:

```json
{
  "quality_gates": {
    "security-scan": {
      "cmd": "npm audit --audit-level=moderate",
      "blocking": false,
      "timeout": 30
    },
    "bundle-size": {
      "cmd": "./scripts/check-bundle-size.sh",
      "blocking": true,
      "timeout": 45
    }
  }
}
```

### Resume Interrupted Runs

Ralph Zero automatically resumes from current `prd.json` state:

```bash
ralph-zero run  # Continues where it left off
```

## Troubleshooting

### Issue: prd.json not found
**Solution:** Create prd.json using ralph-convert skill or manually

### Issue: Agent repeatedly fails same story
**Solution:** Story is too large. Split into 2-3 smaller stories

### Issue: Quality checks failing
**Solution:** Verify commands in ralph.json match your project setup

### Issue: Context overflow warnings
**Solution:** Increase `context_config.token_budget` or reduce `max_progress_lines`

For more help, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Examples

Complete working examples in [assets/examples/](assets/examples/):

- `nextjs-feature.json` - Next.js TypeScript with Prisma
- `python-api.json` - FastAPI with pytest
- `react-component.json` - React component library

## Comparison: Ralph Zero vs Original Ralph

| Feature | Original Ralph | Ralph Zero |
|---------|----------------|------------|
| **Orchestrator** | Bash script | Python with type safety |
| **Agent Support** | Amp-specific | Universal (Agent Skills) |
| **Context Synthesis** | Auto-handoff only | Works with all agents |
| **State Management** | Basic | Validated, atomic, logged |
| **Quality Gates** | Fixed | Configurable per project |
| **Cognitive Feedback** | Optional | Enforced via Librarian |
| **Observability** | Basic logs | Structured JSON logs |

## Credits

Based on [Geoffrey Huntley's Ralph pattern](https://ghuntley.com/ralph/).

Inspired by:
- David Kim's ralph-for-agents (Agent Skills portability)
- Snarktank's ralph (cognitive feedback loops)

## License

MIT License - See [LICENSE](LICENSE) file

## Links

- **Documentation:** [docs/](docs/)
- **Architecture:** [SPEC_RALPH_ZERO.md](../../.gemini/antigravity/brain/4690d535-76a2-42d1-a939-279ff6ff141a/SPEC_RALPH_ZERO.md)
- **Issues:** https://github.com/davidkimai/ralph-zero/issues
- **Agent Skills Spec:** https://agentskills.io/specification
