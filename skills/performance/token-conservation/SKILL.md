---
name: token-conservation
description: |

Triggers: token, conservation
  Minimize token usage through conservative prompting, work delegation,
  and quota tracking.

  Triggers: token usage, quota, token limits, prompt size, token conservation,
  usage tracking, delegation, context compression, token budget

  Use when: session starts (mandatory), prompt sizes spike, tool calls increase,
  before long-running analyses or massive context loads

  DO NOT use when: context-optimization already handles the scenario.
  DO NOT use when: simple queries with minimal context.

  Use this skill at the START of every session. This is MANDATORY for quota management.
location: plugin
token_budget: 300
progressive_loading: true
dependencies:
  hub: []
  modules: []
---

# Token Conservation Workflow

## When to Use
- Run at the start of every session and whenever prompt sizes or tool calls begin to spike.
- Mandatory before launching long-running analyses, wide diffs, or massive context loads.

## Required TodoWrite Items
1. `token-conservation:quota-check`
2. `token-conservation:context-plan`
3. `token-conservation:delegation-check`
4. `token-conservation:compression-review`
5. `token-conservation:logging`

## Step 1 – Quota Check (`quota-check`)
- Record current session duration and weekly usage (from `/status` or notebook).
  Note the 5-hour rolling cap + weekly cap highlighted in the Claude community notice.
- Capture remaining budget and set a max token target for this task.

## Step 2 – Context Plan (`context-plan`)
- Decide exactly which files/snippets to expose. Prefer `rg`/`sed -n` slices
  instead of whole files.
- Convert prose instructions into bullet lists before prompting so only essential
  info hits the model.

## Step 3 – Delegation Check (`delegation-check`)
- Evaluate whether compute-intensive tasks can go to Qwen MCP or other external
  tooling (use `qwen-delegation` skill if needed).
- For local work, favor deterministic scripts (formatters, analyzers) instead
  of LLM reasoning when possible.

## Step 4 – Compression Review (`compression-review`)
- Summarize prior steps/results before adding new context.
  Remove redundant history, collapse logs, and avoid reposting identical code.
- Use `prompt caching` ideas: reference prior outputs instead of restating them
  when the model has already processed the information (cite snippet IDs).
- Decide whether the current thread should be compacted:
  - If the active workflow is finished and earlier context will not be reused,
    instruct the user to run `/new`
  - If progress requires the existing thread but the window is bloated,
    prompt them to run `/compact` before continuing

## Step 5 – Logging (`logging`)

Document the conservation tactics that were applied and note the remaining
token budget. If the budget is low, explicitly warn the user and propose secondary
plans. Record any recommendations made regarding the use of `/new` or `/compact`,
or justify why neither was necessary, to inform future context-handling decisions.

## Output Expectations
- A short explanation of token-saving steps, delegated tasks, and remaining runway.
- Concrete next-action list that keeps the conversation lean (e.g.):
  - "next turn: provide only failing test output lines 40-60"
- Explicit reminder about `/new` or `/compact` whenever you determine it would save
  tokens (otherwise state that no reset/compaction is needed yet).
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
