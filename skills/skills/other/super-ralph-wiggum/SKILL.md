---
name: super-ralph-wiggum
description: Super Ralph Wiggum - autonomous iteration loops with templates, PRD support, progress tracking, and browser testing. This skill should be used when running Claude Code in autonomous loops for test coverage improvement, PRD-based feature development, documentation generation, dataset creation, lint fixing, code cleanup, or framework migrations. Combines the plugin's in-session loop mechanism with specialized templates and best practices from Geoffrey Huntley, Ryan Carson, and AI Hero.
---

# Super Ralph Wiggum

Autonomous iteration loops for Claude Code. Run the same prompt repeatedly until task completion, with context persisting through files and git history.

## The Ralph Philosophy

> **The agent chooses the task, not you.**

You define the end state. Ralph figures out how to get there.

With multi-phase plans, a human writes a new prompt at the start of each phase. With Ralph, the agent picks what to work on next from your PRD. You describe the destination. Ralph navigates.

## The 11 Tips (Quick Reference)

Based on [AI Hero's definitive guide](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum):

| # | Tip | Key Insight |
|---|-----|-------------|
| 1 | Ralph Is A Loop | Same prompt, multiple iterations |
| 2 | Start HITL, Then AFK | Learn → Trust → Let go |
| 3 | Define The Scope | Explicit stop conditions prevent infinite loops |
| 4 | Track Progress | progress.txt bridges context windows |
| 5 | Use Feedback Loops | Types, tests, linting as guardrails |
| 6 | Take Small Steps | One logical change per commit |
| 7 | Prioritize Risky Tasks | Architecture first, quick wins last |
| 8 | Define Software Quality | Tell Ralph what kind of repo this is |
| 9 | Use Docker Sandboxes | Essential for AFK safety |
| 10 | Pay To Play | HITL still valuable without AFK |
| 11 | Make It Your Own | Alternative loop types, task sources |

See `@references/tips-and-tricks.md` for detailed guidance on each tip.

## Quick Start

To start a Ralph loop with a template:

```
Run the super-ralph-wiggum skill with the test-coverage template, max 20 iterations
```

To start with a PRD file:

```
Run super-ralph-wiggum with feature-prd template using ./prd.json
```

## Available Templates

| Template | Use Case | Default Iterations |
|----------|----------|-------------------|
| `test-coverage` | Improve test coverage to target % | 30 |
| `feature-prd` | Implement features from PRD file | 20 |
| `lint-fix` | Fix all lint errors incrementally | 30 |
| `docs-generation` | Generate documentation for modules | 25 |
| `dataset-generation` | Generate training data samples | 50 |
| `migration` | Migrate to new framework/version | 40 |
| `entropy-loop` | Reverse software entropy (dead code, smells) | 30 |
| `duplication-loop` | Eliminate duplicate code | 25 |

## Invocation Patterns

### Template Mode (Recommended)

Use a pre-built template for common tasks:

```
Use super-ralph-wiggum with [template-name] template
Options: --max-iterations N, --browser (for UI verification)
```

### PRD Mode

For structured feature development with task tracking:

```
Use super-ralph-wiggum with feature-prd template
PRD file: ./prd.json
```

The PRD file tracks features with `passes: true/false`. Loop completes when all features pass.

### HITL Mode (Single Iteration)

For interactive learning and pair programming:

```
Use super-ralph-wiggum with --once flag to [task description]
```

Runs ONE iteration without looping. Great for learning how Ralph works.

### Custom Prompt

For tasks not covered by templates:

```
Use super-ralph-wiggum with custom prompt:
[Your detailed task description with completion criteria]
Completion: Output <promise>COMPLETE</promise> when done
Max iterations: 15
```

## The Two Modes: HITL vs AFK

| Mode | How It Works | Best For |
|------|--------------|----------|
| **HITL** (human-in-the-loop) | Run once, watch, intervene | Learning, prompt refinement, risky tasks |
| **AFK** (away from keyboard) | Run in a loop with max iterations | Bulk work, low-risk tasks, overnight runs |

**The progression is simple:**
1. Start with HITL to learn and refine
2. Go AFK once you trust your prompt
3. Review the commits when you return

For AFK, always cap iterations:
- Small tasks: 5-10 iterations
- Medium tasks: 15-30 iterations
- Large features: 30-50 iterations

## Explicitly Define Software Quality

Ralph doesn't know if this is a throwaway prototype or production code. **Tell it.**

| Repo Type | What To Say | Expected Behavior |
|-----------|-------------|-------------------|
| Prototype | "Speed over perfection. Skip edge cases." | Takes shortcuts |
| Production | "Must be maintainable. Follow best practices." | Adds tests, docs |
| Library | "Public API. Backward compatibility matters." | Careful about breaking changes |

### Code Quality Prompt

If the loop should maintain high code quality, specify it factually:

> Maintain existing code conventions and quality standards.
> Each change should leave test coverage equal to or better than before.
> Prefer incremental improvements over large rewrites.

Avoid motivational framing ("fight entropy", "be thorough")—Claude 4.6 already tends toward thoroughness and these amplify it into over-planning. Factual quality criteria are more effective.

### The Repo Wins

Your instructions compete with your codebase. When Ralph explores your repo, it sees two sources of truth: what you told it to do and what you actually did.

If you write "never use `any` types" but Ralph sees `any` throughout your existing code, it will follow the codebase, not your instructions.

Claude learns patterns from the existing codebase. If the codebase uses `any` types throughout, the loop will follow that pattern regardless of instructions. Clean up the specific patterns you care about before running the loop.

## Task Prioritization Order

When choosing the next task, Ralph should prioritize:

1. **Architectural decisions** and core abstractions
2. **Integration points** between modules
3. **Unknown unknowns** and spike work
4. **Standard features** and implementation
5. **Polish, cleanup**, and quick wins

Fail fast on risky work. Save easy wins for later.

Use HITL Ralph for early architectural decisions—the code from these tasks stays forever. Save AFK Ralph for when the foundation is solid.

## Execution Modes

### 1. In-Session Mode (Default)

Loop runs **inside** your current Claude Code session using stop hooks:

```
Use super-ralph-wiggum with test-coverage template, max 20 iterations
```

- Stop hook intercepts exit attempts
- Same prompt fed back each iteration
- Context persists through files and git
- Best for interactive/monitored work

### 2. Dockerized Mode (External)

Loop runs **externally** via bash script with Docker sandbox:

```bash
# Generate external script
./scripts/setup-ralph-loop.sh --template test-coverage --docker > run-ralph.sh
chmod +x run-ralph.sh

# Run in background
./run-ralph.sh 20 &
```

- Each iteration is a fresh Claude Code instance
- Docker isolation for safety
- Best for overnight/AFK runs
- Memory persists only via files

**Essential for AFK safety**: Docker sandboxes let Ralph edit project files and commit—but can't touch your home directory, SSH keys, or system files.

## How It Works

1. **Setup**: Creates state file at `.claude/ralph-loop.local.md`
2. **Progress**: Auto-creates `progress.txt` in project root
3. **Loop**: Stop hook intercepts exit, feeds same prompt back
4. **Completion**: Detects `<promise>COMPLETE</promise>` or PRD all-pass
5. **Learning**: Patterns accumulate in progress.txt across iterations

## Key Options

| Option | Description | Default |
|--------|-------------|---------|
| `--template <name>` | Use pre-built template | (required or custom prompt) |
| `--prd <file>` | PRD file for task tracking | none |
| `--max-iterations <n>` | Iteration limit | varies by template |
| `--completion-promise <text>` | Custom completion phrase | COMPLETE |
| `--progress <file>` | Progress file location | ./progress.txt |
| `--browser` | Enable browser testing prompts | false |
| `--once` | Single iteration (HITL mode) | false |

## Best Practices

### 1. Small Stories
Tasks must fit in one context window. Break large features into atomic stories.

### 2. Verification First
Always run typecheck + tests before committing. Templates enforce this.

### 3. Cap Iterations
For AFK (unattended) Ralph, always set `--max-iterations`. Infinite loops are dangerous with stochastic systems.

### 4. Clear Completion Criteria
Vague tasks risk infinite loops. Be explicit about when to stop.

### 5. Use Progress File
Previous iteration learnings persist in `progress.txt`. Templates auto-inject this.

### 6. One Change Per Commit
Keep changes small and focused. Prefer multiple small commits over one large commit.

### 7. Structure State Appropriately
Use JSON for structured progress data (coverage percentages, feature pass/fail, migration counts). Use freeform text in progress.txt for observations and session learnings. Use git commits as checkpoints between iterations so each new context window can discover state from the filesystem.

## References

For detailed guidance, read the reference files:

- `@references/tips-and-tricks.md` - The 11 Tips expanded with AI Hero insights
- `@references/prompt-patterns.md` - 10 patterns for convergent prompts
- `@references/prd-schema.md` - PRD file structure and usage
- `@references/cost-estimation.md` - API cost guidelines
- `@references/browser-testing.md` - Dev-browser integration

## Template Details

### test-coverage

Improves test coverage by:
1. Running coverage to find gaps
2. Identifying most important untested user-facing behavior
3. Writing ONE meaningful test per iteration
4. Using `/* v8 ignore */` for non-essential code
5. Committing after each successful test

Read full template: `@templates/test-coverage.md`

### feature-prd

Implements features from a PRD file by:
1. Reading `prd.json` for highest-priority incomplete feature
2. Checking dependencies are satisfied
3. Implementing ONE feature per iteration
4. Running verification (typecheck + tests)
5. Updating AGENTS.md with patterns discovered
6. Marking feature as `passes: true`

Read full template: `@templates/feature-prd.md`

### lint-fix

Fixes lint errors by:
1. Running linter to get error list
2. Picking file with most errors
3. Fixing ALL errors in that file
4. Verifying fixes don't break tests
5. Committing and moving to next file

Read full template: `@templates/lint-fix.md`

### entropy-loop

Reverses software entropy by:
1. Scanning for code smells (unused exports, dead code, TODOs)
2. Fixing ONE issue per iteration
3. Running verification
4. Documenting changes in progress.txt

Read full template: `@templates/entropy-loop.md`

### duplication-loop

Eliminates duplicate code by:
1. Running jscpd to find duplicates
2. Identifying ONE duplication group
3. Extracting shared code into utility/helper
4. Updating all call sites
5. Verifying with tests

Read full template: `@templates/duplication-loop.md`

### docs-generation

Generates documentation by:
1. Identifying undocumented public functions
2. Writing ONE doc per iteration
3. Verifying examples compile/run
4. Including JSDoc and README updates

Read full template: `@templates/docs-generation.md`

### dataset-generation

Generates training data by:
1. Creating samples meeting quality criteria
2. Validating quality per iteration
3. Tracking count in progress.txt
4. Stopping at target count

Read full template: `@templates/dataset-generation.md`

### migration

Migrates codebase by:
1. Reading migration plan from file
2. Migrating ONE module per iteration
3. Ensuring tests pass after each
4. Tracking migrated vs remaining

Read full template: `@templates/migration.md`

## Canceling a Loop

To stop an active Ralph loop, delete the state file:

```bash
rm .claude/ralph-loop.local.md
```

Or wait for max iterations to be reached.

## Attribution

Based on the Ralph Wiggum technique by [Geoffrey Huntley](https://ghuntley.com/ralph/).
Enhanced with learnings from [Ryan Carson](https://x.com/ryancarson), [Matt Pocock](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum), and [AI Hero](https://www.aihero.dev/).
