---
name: agentv-bench
description: >-
  Optimize agents through evaluation-driven iteration. Use when asked to evaluate an agent,
  optimize prompts against evals, run EVAL.yaml or evals.json evaluations, benchmark agent
  performance, compare agent outputs across providers, analyze eval results, or improve agent
  performance. Supports workspace evaluation with real repos, multi-provider targets, multi-turn
  conversations, code judges, tool trajectory scoring, and workspace file change tracking.
  Use this skill whenever the user mentions evaluating, benchmarking, testing, or optimizing
  any agent, prompt, or skill — even if they don't explicitly say "agentv".
---

# AgentV Bench


A skill for evaluating agents and iteratively improving them through data-driven optimization.

At a high level, the process goes like this:

- Understand what the agent does and what "good" looks like
- Write evaluation test cases (EVAL.yaml or evals.json)
- Run the agent on those test cases, grade the outputs
- Analyze the results — what's working, what's failing, and why
- Improve the agent's prompts/skills/config based on the analysis
- Repeat until you're satisfied

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress. Maybe they want to start from scratch — help them write evals, run them, and iterate. Maybe they already have results — jump straight to analysis and improvement.

Be flexible. If the user says "I don't need a full benchmark, just help me debug this failure", do that instead.

After the agent is working well, you can also run description optimization to improve skill triggering accuracy (see the Description Optimization section).

## Bundled scripts layer

This skill ships with a Python scripts layer in `plugins/agentv-dev/skills/agentv-bench/scripts/`. Requires Python 3.11+. No extra dependencies — all scripts use the stdlib only.

The scripts layer wraps AgentV rather than replacing it. Use it when you want a provider-agnostic optimization workflow that still relies on core AgentV commands and artifacts:

- `scripts/quick_validate.py` → validates skill structure and evals.json schema before a run
- `scripts/run_eval.py` → runs evals defined in `evals/evals.json` via `claude -p`
- `scripts/run_loop.py` → plans and executes repeated eval iterations, calling `run_eval.py` each round
- `scripts/aggregate_benchmark.py` → reads `benchmark.json`, `timing.json`, and `results.jsonl`
- `scripts/generate_report.py` → builds a review model and writes a JSON report from AgentV artifacts
- `scripts/improve_description.py` → proposes description experiments from observed failures/false triggers
- `scripts/package_skill.py` → packages the skill directory for distribution
- `eval-viewer/generate_review.py` → reads AgentV artifacts (`--artifacts`) and renders `viewer.html`

Keep code-judge execution, evaluator semantics, and artifact generation in AgentV core. The scripts only orchestrate those primitives and read the artifacts they emit.

## Scripts

All scripts require Python 3.11+ and no external dependencies beyond the Python stdlib.

### Skill management
- `scripts/quick_validate.py` — validate SKILL.md structure and frontmatter
- `scripts/package_skill.py` — package skill into a distributable `.skill` zip

### Eval workflow
- `scripts/run_eval.py` — run trigger evaluation (tests skill description quality)
- `scripts/run_loop.py` — run eval+improve loop until all assertions pass
- `scripts/improve_description.py` — improve skill description using eval failures
- `scripts/aggregate_benchmark.py` — aggregate run results into benchmark statistics
- `scripts/generate_report.py` — generate HTML report from run_loop output

### Review viewer
- `eval-viewer/generate_review.py` — serve live eval review UI (HTTP server + feedback API)

### Note on eval formats
Skills use `evals/evals.json` with `assertions` for both trigger and output quality testing.
A future AgentV PR will add `agentv convert` to migrate existing `dataset.eval.yaml` files to `evals/evals.json`.

## Communicating with the user

This skill is used by people across a wide range of familiarity with evaluation tooling. Pay attention to context cues:

- "evaluation" and "benchmark" are borderline but OK in most cases
- For "YAML", "evaluator", "assertion", "deterministic judge" — see serious cues from the user that they know what those mean before using them without explanation
- Briefly explain terms if in doubt

When presenting results, default to summary tables. Offer detail on request. In CI/headless mode, skip interactive prompts and exit with status codes.

---

## Step 1: Understand the Agent

Before running or optimizing, understand what you're working with.

1. **Read the agent's artifacts** — prompts, skills, configs, recent changes. Understand the full picture: what tools are available, what the expected input/output looks like, what constraints exist.

2. **Identify success criteria** — what does "good" look like for this agent? What are the edge cases? What would a failure look like? Talk to the user if this isn't clear from the artifacts alone.

3. **Understand the target harness** — which provider runs the agent (Claude, GPT, Copilot CLI, Gemini, custom CLI)? This affects what evaluator types are available and how to run tests.

4. **Challenge assumptions** — if evals already exist, review their quality before running:
   - Are the test cases testing the right things?
   - Are assertions specific enough to catch real failures?
   - Are there ambiguous or contradictory test cases?
   - Flag eval issues before proceeding — running bad evals wastes time.

5. **Check integrity** — ensure task prompts (what the agent receives) are not also used as evaluator prompts (how outputs are scored). If a prompt file appears in both locations, note the overlap and optimize only for the task purpose.

---

## Step 2: Write Evaluations

AgentV supports two evaluation formats:

**EVAL.yaml** (native, full features) — supports workspaces, code judges, multi-turn conversations, tool trajectory scoring, workspace file tracking, multi-provider targets. Use this for agent evaluation.

```yaml
# example.eval.yaml
tests:
  - id: basic-code-review
    input: "Review this TypeScript file for bugs and suggest improvements"
    criteria: "Identifies the null pointer bug on line 12 and suggests a fix"
    assertions:
      - type: contains
        value: "null"
      - type: llm-judge
        prompt: "Did the review identify the bug and suggest a concrete fix?"

workspace:
  template: ./workspace-template
  hooks:
    before_each:
      reset: fast
```

Multi-skill evaluation is handled naturally via input messages — describe the task in the test input, and the agent uses whatever skills it needs.

**evals.json** (skill-creator compatible) — auto-promoted to EVAL-equivalent format:
- `prompt` → input messages
- `expected_output` → reference answer
- `assertions` → evaluators
- `files[]` paths resolved relative to the evals.json location

```json
{
  "skill_name": "my-agent",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "assertions": ["Output includes error handling", "Uses async/await"]
    }
  ]
}
```

### Writing good test cases

Start with 2-3 realistic test cases — the kind of thing a real user would actually say. Share them with the user before running: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?"

Good assertions are objectively verifiable and have descriptive names. Subjective quality ("the output is good") is better evaluated qualitatively — don't force assertions onto things that need human judgment.

**Evaluator types** (from cheapest to most expensive):
- `exact`, `contains`, `regex`, `is-json` — deterministic, zero cost, instant
- `field-accuracy` — checks JSON field values against expected
- `composite` — weighted combination of multiple evaluators
- `code-judge` — Python/TypeScript scripts via `defineCodeJudge()` (→ see `agentv-eval-writer` skill)
- `tool-trajectory` — evaluate tool call sequences and patterns
- `llm-judge` — LLM-graded with rubric (most expensive, use when semantic understanding needed)

Prefer deterministic evaluators over LLM judges whenever possible. If an assertion can be checked with `contains` or `regex`, don't use `llm-judge`.

---

## Step 3: Run and Grade

This section is one continuous sequence — don't stop partway through.

Put results in a workspace directory organized by iteration (`iteration-1/`, `iteration-2/`, etc.). Don't create all of this upfront — just create directories as you go.

### Choosing a run mode

Read the mode from `.env` before doing anything:

```bash
grep AGENT_EVAL_MODE .env 2>/dev/null || echo "AGENT_EVAL_MODE=agent"
```

| `AGENT_EVAL_MODE` | Mode | How |
|-------------------|------|-----|
| `cli` (recommended) | **AgentV CLI** | `agentv eval <path>` — end-to-end, multi-provider |
| `agent` (legacy) | **Agent mode** | `python scripts/run_eval.py` (calls `claude -p`, Claude-only) |

Set `AGENT_EVAL_MODE` in `.env` at the project root. If absent, default to `agent`.

**`cli`** — AgentV CLI handles execution, grading, and artifact generation end-to-end. Works with all providers. Recommended for new setups.

**`agent`** — `run_eval.py` runs each test case via `claude -p` and captures outputs for grading. Legacy mode, Claude-only. Use `--mode cli --target <provider>` for multi-provider support.

### Running evaluations

**AgentV CLI mode** (end-to-end, EVAL.yaml):
```bash
agentv eval <eval-path> --artifacts .agentv/artifacts/
```

**Agent mode** (evals.json via `run_eval.py`):
```bash
cd plugins/agentv-dev/skills/agentv-bench
python scripts/quick_validate.py --eval evals/evals.json
python scripts/run_eval.py --eval evals/evals.json --output iteration-1/
# Multi-provider: use cli mode
python scripts/run_eval.py --eval evals/evals.json --output iteration-1/ --mode cli --target copilot
```

**Spawn all runs in the same turn.** For each test case that needs both a "with change" and a "baseline" run, launch them simultaneously. Don't run one set first and come back for the other — launch everything at once so results arrive around the same time.

**Multi-target benchmarking:**
```bash
agentv eval <eval-path> --target claude --target gpt --target copilot
```

**Baseline strategy:**
- **New agent**: baseline is "no prompt" or minimal prompt — same eval, no agent-specific configuration
- **Improving existing**: snapshot the current version before editing (`cp -r <prompt-dir> <workspace>/prompt-snapshot/`), use as baseline throughout
- **Multi-target**: each target is its own baseline — no need for a separate "without" run

### While runs are in progress, draft evaluators

Don't just wait for runs to finish — use this time productively. If assertions don't exist yet, draft them now. If they exist, review them and explain what they check to the user.

Good assertions are *discriminating* — they pass when the agent genuinely succeeds and fail when it doesn't. An assertion that passes for both good and bad outputs is worse than no assertion.

### As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. **Save this data immediately** to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives.

### Grading

Once runs complete:

1. **Deterministic evaluators** run automatically via CLI — `contains`, `regex`, `is-json`, `field-accuracy` produce instant results.

2. **LLM-graded assertions** — dispatch `eval-grader` subagent (read `agents/eval-grader.md`). The grader evaluates each assertion against the outputs with cited evidence. For assertions that can be checked programmatically, it writes and runs a script rather than eyeballing it.

3. **Write grading.json** per run with this structure:
```json
{
  "assertion_results": [
    {"text": "Response includes error handling", "passed": true, "evidence": "Lines 12-15 contain try/catch block"},
    {"text": "Uses async/await pattern", "passed": false, "evidence": "Uses .then() callback pattern instead"}
  ],
  "summary": {"passed": 1, "failed": 1, "total": 2, "pass_rate": 0.5}
}
```

The grading.json `assertion_results` array must use the fields `text`, `passed`, and `evidence` — downstream tooling depends on these exact field names.

### Workspace features (EVAL.yaml only)

- **Workspace isolation** — clone repos, run setup/teardown hooks (before_all, before_each, after_each, after_all)
- **Materialization modes** — `pooled` (reuse slots), `temp` (fresh per run), `static` (existing dir)
- **Multi-repo** — clone multiple repos with sparse checkout and shallow clone support
- **File change tracking** — grade by diffing workspace files before/after agent execution

### Artifacts

All artifacts use established schemas — do not modify the structure:

- **grading.json**: per-test `assertion_results` with `{text, passed, evidence}`, plus `summary`
- **timing.json**: `{total_tokens, duration_ms, total_duration_seconds}`
- **benchmark.json**: per-target aggregate `{pass_rate, time_seconds, tokens}` with `mean ± stddev`

Write artifacts to `.agentv/artifacts/` or the iteration directory.

---

## Step 4: Analyze Results

Once all runs are graded, analyze the results before attempting improvements.

### Pattern analysis

Read the JSONL results and look for:

- **Always-pass tests** — assertion too loose or non-discriminating. If it passes for both good and bad outputs, it's not testing anything.
- **Always-fail tests** — task impossible, eval broken, or assertion misconfigured. Don't optimize against broken evals.
- **Flaky tests** — non-deterministic results across runs. Investigate before treating failures as real.
- **Systematic failures** — same failure pattern across multiple tests. This usually points to a missing instruction or wrong approach.
- **Deterministic upgrade candidates** — LLM-judge assertions that could be replaced with `contains`, `regex`, or `is-json` (cheaper, faster, more reliable).

### Dispatch subagents

- **Dispatch `eval-analyzer`** (read `agents/eval-analyzer.md`) for a structured quality audit: deterministic upgrade suggestions, weak assertion detection, cost/quality flags, and benchmark pattern analysis.

- **Dispatch `eval-comparator`** (read `agents/eval-comparator.md`) for blind N-way comparison between iterations or targets. The comparator blinds provider identities, generates task-specific rubrics, scores each output, then unblinds and attributes improvements.

### Trace analysis

Use CLI tools for deeper investigation:
```bash
agentv trace <results-file>          # Detailed execution trace inspection
agentv compare <file-a> <file-b>     # Structured diff between runs
```

Look for: tool call patterns, error recovery behavior, conversation flow, wasted steps.

### Present results to the user

Show a summary table:

```
| Test ID          | Score | Pass/Fail | Delta | Notes                    |
|------------------|-------|-----------|-------|--------------------------|
| basic-code-review| 0.85  | ✓ PASS    | +0.15 | Found the bug this time  |
| edge-case-empty  | 0.00  | ✗ FAIL    | —     | Crashed on empty input   |
```

Highlight:
- Current pass rate and delta from baseline
- Comparison results (which target/iteration won and why)
- Analyst observations the aggregate stats would hide

Ask: "How does this look? Anything you'd change about the evals or the approach?"

---

## Step 5: Improve

This is the heart of the loop. You've run the test cases, analyzed the results, and now you need to make the agent better.

### How to think about improvements

1. **Generalize from the analysis.** You're iterating on a small eval set, but the agent will be used on many different inputs. Don't overfit to specific test cases. Rather than fiddly patches or oppressively rigid MUSTs, try different approaches and see what works. It's cheap to experiment.

2. **Keep the prompt lean.** Read the execution transcripts, not just the final outputs. If the agent wastes time on unproductive steps, remove the instructions causing that. If it always ignores a section, that section isn't pulling its weight.

3. **Explain the why.** Today's LLMs are smart. They have good theory of mind and can go beyond rote instructions when given good reasoning. If you find yourself writing ALWAYS or NEVER in all caps, that's a yellow flag — reframe as an explanation of why the thing matters. That's more humane, powerful, and effective.

4. **Look for repeated work.** Read the transcripts from test runs and notice if the agent independently takes the same multi-step approach to something across cases. If all test runs result in writing the same helper script, bundle it. If every run makes the same mistake, the instruction is missing or unclear.

### Applying changes

- **Surgical edits**: ADD (new rule for a missing constraint), UPDATE (refine for clarity), DELETE (remove redundant or harmful rules), NEGATIVE CONSTRAINT (explicitly state what NOT to do)
- **One change per iteration** to isolate effects. If you change three things and the score improves, you don't know which change helped.
- **Variant tracking**: When a change helps some tests but hurts others, maintain 2-3 prompt variants. Compare variants to find the best overall approach before converging.
- **When converging**: Generalize specific patches into broad principles. Remove redundancy and contradictions. Ensure the prompt is clear, focused, and under 200 lines.

### Evaluation integrity

**Critical**: Only optimize **task prompts** (what the agent receives), never **judge prompts** (how evaluators score outputs). Modifying judge prompts games the evaluation without improving the agent.

If a prompt file is referenced in both task input and evaluator configs, optimize for the task purpose only. Document which prompts were modified in the optimization log.

### The iteration loop

After improving:

1. Apply your changes to the agent's prompts/skills/config
2. Re-run all test cases into a new `iteration-<N+1>/` directory, including baseline runs
3. Compare against the previous iteration (Step 4)
4. Present results to the user
5. Stop when ANY of:
   - The user says they're happy
   - Feedback is all empty (everything looks good)
   - You're not making meaningful progress (no improvement for 2 consecutive iterations)
   - Target pass rate is reached
   - Maximum iterations exhausted

**Human checkpoints**: At iterations 3, 6, and 9, always present progress to the user regardless of automation settings. Push back if optimization is accumulating contradictory rules or overfitting to specific test cases.

---

## Entering Mid-Lifecycle

Users can start at any step by providing existing data:

| Entry point | Required input | Example prompt |
|------------|---------------|----------------|
| Step 1 (Understand) | `eval-path` | "Optimize my agent against evals/support.yaml" |
| Step 2 (Write Evals) | Agent artifacts | "Write evals for this agent" |
| Step 3 (Run + Grade) | `eval-path` | "Run this eval and show me results" |
| Step 4 (Analyze) | `results-path` | "Analyze why my agent is failing on these results" |
| Step 5 (Improve) | Analysis + strategy | "Apply these optimization suggestions" |

When entering mid-lifecycle, run only the requested step and subsequent steps. Don't re-run earlier steps unless the user requests a full loop.

---

## Advanced: Blind Comparison

For situations where you want a rigorous comparison between two versions (e.g., "is the new version actually better?"), dispatch the `eval-comparator` subagent. It blinds identities, generates task-specific rubrics, scores outputs, then unblinds and explains why the winner won.

This is optional and requires subagents. The human review loop is usually sufficient.

---

## Description Optimization

The `description` field in a skill's SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes the skill. After the agent/skill is working well, offer to optimize the description for better triggering accuracy.

**Provider compatibility**: Description optimization is specific to agents with skill-discovery mechanisms (e.g., Claude Code). Agents like Copilot and Codex don't have skill systems, so description optimization doesn't apply to them. The `skill-trigger` evaluator still works for these providers — it just checks whether the agent invoked the right tools, not whether it discovered the skill via description matching.

### Step 1: Generate trigger EVAL.yaml

Create 20 test cases:
- **10 should-trigger**: realistic prompts where this skill should activate — different phrasings, casual speech, uncommon use cases, edge cases where this skill competes with another but should win
- **10 should-not-trigger**: near-miss prompts that share keywords but actually need something different — adjacent domains, ambiguous phrasing where naive matching would trigger but shouldn't

Prompts must be realistic — include file paths, personal context, typos, casual speech. Not abstract requests like "format data" but concrete ones like "ok so my boss sent me Q4-sales-FINAL-v2.xlsx and she wants me to add a profit margin column..."

The should-not-trigger cases are the most valuable. "Write a fibonacci function" as a negative test for an eval skill is useless — it doesn't test anything. The negative cases should be genuinely tricky near-misses.

Write as EVAL.yaml with top-level input (the user prompt doesn't specify the skill name — it's a natural utterance):

```yaml
# trigger-eval.eval.yaml
tests:
  - id: should-trigger-casual-optimize
    input: "ok so I have this agent that keeps failing on the code review tasks, can you help me figure out why and fix it"
    assertions:
      - type: contains
        value: "agentv-bench"
  - id: should-not-trigger-build-error
    input: "my TypeScript build is failing with type errors in src/auth.ts"
    assertions:
      - type: not-contains
        value: "agentv-bench"
```

### Step 2: Review with user

Present the eval set. The user adjusts queries, toggles should-trigger, adds/removes cases. This step matters — bad eval queries lead to bad descriptions.

### Step 3: Iterate on description

Run the trigger eval, identify misfires, rewrite the description, re-run. Max 5 iterations. Select best description by held-out test accuracy (split 60% train / 40% test) to avoid overfitting.

When you already have `benchmark.json` and `grading.json`, use the scripts bundle to draft the next round of edits:

```bash
cd plugins/agentv-dev/skills/agentv-bench
python scripts/improve_description.py --benchmark .agentv/artifacts/benchmark.json --grading .agentv/artifacts/grading.json
```

### Step 4: Apply

Update the skill's SKILL.md frontmatter with the optimized description. Show the user before/after with accuracy scores.

---

## Environment Adaptation

**CI/headless mode**: Skip interactive prompts. Exit with pass/fail status code. Always generate artifacts for downstream consumption.

**No subagents available** (e.g., Claude.ai): Run test cases serially. Skip blind comparison. Present results directly in conversation — for each test case, show the prompt and output. Ask for feedback inline. Skip benchmarking (it relies on baseline comparisons that aren't meaningful without subagents).

**Provider support matrix**:

| Provider | Tool Calls | `skill-trigger` Evaluator | Description Optimization |
|----------|-----------|---------------------------|-------------------------|
| Claude CLI/SDK | Yes | Built-in (Skill, Read) | Yes (skill discovery) |
| Copilot CLI/SDK | Yes (ACP) | Built-in (Skill, Read File, readFile) | No (no skill discovery) |
| Pi Coding Agent | Yes | Built-in (same as Claude) | Possible (same format) |
| VS Code / VS Code Insiders | Yes | Built-in (Copilot tools) | No |
| Codex | Yes (command_execution, file_change) | Use code-grader (see below) | Yes (.agents/.codex folders) |
| Other providers | Varies | Use code-grader (see below) | No |

**Note**: "Description Optimization" (iterating on SKILL.md descriptions for better triggering accuracy) requires an agent with a skill-discovery mechanism. Agents that don't have skill systems (Copilot, Codex) still benefit from evaluation for testing whether they invoke the right tools.

**Provider-specific notes**:
- **Copilot CLI**: Uses ACP protocol via `copilot --acp --stdio`
- **Claude SDK**: Requires `@anthropic-ai/claude-agent-sdk` installed
- **Codex**: Supports skills via `.agents/` or `.codex/` folders. Emits `command_execution` and `file_change` tool calls.
- **Custom CLI**: Needs `command` and output file pattern in target config
- **Target config**: Uses `${{ ENV_VAR }}` syntax (not `${ENV_VAR}`) for API keys

### Unsupported providers: use a code-grader

The built-in `skill-trigger` evaluator covers Claude, Copilot, Pi, and VS Code out of the box. For providers with different tool-call formats (Codex, custom agents, etc.), write a code-grader that inspects the agent's tool call trace.

A code-grader receives the full evaluation context including the agent's output messages and tool calls. You can inspect these to determine whether the skill was invoked:

```yaml
# Example: code-grader for Codex skill-trigger detection
tests:
  - id: should-trigger-codex
    input: "Analyze this CSV file"
    assertions:
      - type: code-grader
        path: ./judges/codex-skill-trigger.ts
```

```typescript
// judges/codex-skill-trigger.ts
import { defineCodeJudge } from '@agentv/eval';

export default defineCodeJudge(({ output }) => {
  const skillName = 'csv-analyzer';
  const toolCalls = (output ?? []).flatMap((msg) => msg.toolCalls ?? []);
  const firstTool = toolCalls[0];

  if (!firstTool) {
    return { score: 0, reason: 'No tool calls recorded' };
  }

  // Codex reads skill files via shell commands
  if (firstTool.tool === 'command_execution') {
    const cmd = String(firstTool.input ?? '');
    if (cmd.includes(skillName)) {
      return { score: 1, reason: `Skill "${skillName}" triggered via command: ${cmd}` };
    }
  }

  // Check if skill file was read via file_change or other tools
  if (firstTool.tool === 'file_change') {
    const path = String((firstTool.input as Record<string, unknown>)?.path ?? '');
    if (path.includes(skillName)) {
      return { score: 1, reason: `Skill file accessed: ${path}` };
    }
  }

  return { score: 0, reason: `First tool was "${firstTool.tool}" — not a skill invocation for "${skillName}"` };
});
```

This approach is more flexible than config overrides — you can match any tool-call pattern, check multiple fields, and add provider-specific logic as needed.

---

## Subagent Reference

The `agents/` directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

| Agent | File | Purpose | When to dispatch |
|-------|------|---------|-----------------|
| eval-grader | `agents/eval-grader.md` | Grade responses with per-assertion evidence | Step 3 (grading LLM-judged assertions) |
| eval-comparator | `agents/eval-comparator.md` | Blind N-way comparison + post-hoc analysis | Step 4 (comparing iterations/targets) |
| eval-analyzer | `agents/eval-analyzer.md` | Quality audit, deterministic upgrades, benchmarks | Step 4 (pattern analysis) |

The `references/` directory has additional documentation:
- `references/migrating-from-skill-creator.md` — Guide for users coming from Anthropic's skill-creator

---

Repeating the core loop for emphasis:

- Understand what the agent does
- Write evaluation test cases
- Run the agent and grade outputs
- Analyze results — surface patterns, dispatch analyst and comparator subagents
- Improve the agent based on analysis
- Repeat until you and the user are satisfied

Take your time with improvements. Read the transcripts. Understand why failures happened. Make changes that generalize beyond the test set. This is important work.
