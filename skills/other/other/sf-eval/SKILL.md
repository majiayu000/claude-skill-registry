---
name: sf-eval
description: |
  Evaluate and benchmark Salesforce skill quality. Compares AI-generated code
  with vs without skill context, scores against a Salesforce-specific rubric
  (security, governor limits, bulkification, patterns, completeness), and
  produces a comparison report. Use to run benchmarks, verify skill value,
  or check Apex code quality. Activate on mentions of "evaluate skills",
  "benchmark", "skill quality", "run eval", or "compare with/without skills".
license: Apache-2.0
compatibility: Works standalone. Optionally uses Salesforce CLI for static analysis.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, evaluation, benchmark, quality, testing
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(bash *),Bash(cat *),Glob,Grep
context: fork
---

# Salesforce Skills Evaluator

You evaluate whether Salesforce skills improve AI-generated code quality. You do this by comparing code generated **with** vs **without** skill context and scoring both.

## Eval Modes

### Mode 1: Run Benchmark Task(s)
When user says `/sf-eval` or `/sf-eval <task-id>`:

1. Read available tasks from `evals/benchmarks/tasks.json`
2. For each task (or the specified one):

   **Step A — Generate Baseline (no skill context):**
   Generate Salesforce code for the task prompt AS IF you had no Salesforce skill knowledge. Produce typical LLM output — functional but likely missing Salesforce-specific best practices. Do NOT use `WITH USER_MODE`, do NOT use trigger handler patterns, do NOT use `stripInaccessible` unless the prompt explicitly asks for it. Write code the way a generic AI would.

   **Step B — Generate With Skills:**
   Read the relevant skill file at `skills/<skill>/SKILL.md` and its references. Then generate code following ALL the skill's rules, patterns, and gotchas strictly.

   **Step C — Score Both:**
   Read the rubric at `evals/benchmarks/rubric.md` and the judge prompt at `evals/benchmarks/judge-prompt.md`. Score each output on 5 categories (0-5 each):

   | Category | What to check |
   |----------|---------------|
   | Security | WITH USER_MODE, stripInaccessible, with sharing, no injection, no hardcoded creds |
   | Governor Limits | No SOQL/DML in loops, uses Map/Set collections, efficient queries |
   | Bulkification | Handles 200+ records, uses collections, no Trigger.new[0] |
   | Patterns | Trigger handler, service/selector layers, naming conventions |
   | Completeness | Requirements met, edge cases, error handling, production-ready |

   **Step D — Output Report:**
   Format as a comparison table:

   ```
   ## Task: <task-id>
   **Prompt**: <prompt text>

   ### Baseline (No Skills) — X/25
   | Category | Score | Reason |
   |----------|-------|--------|
   | Security | X/5 | ... |
   | Governor Limits | X/5 | ... |
   | Bulkification | X/5 | ... |
   | Patterns | X/5 | ... |
   | Completeness | X/5 | ... |

   ### With Skills — X/25
   | Category | Score | Reason |
   |----------|-------|--------|
   | Security | X/5 | ... |
   | Governor Limits | X/5 | ... |
   | Bulkification | X/5 | ... |
   | Patterns | X/5 | ... |
   | Completeness | X/5 | ... |

   ### Improvement: +X points (+XX%)
   ```

3. If running all tasks, produce a summary table at the end:
   ```
   ## Summary
   | Task | Baseline | With Skills | Delta |
   |------|----------|-------------|-------|
   | ... | X/25 | X/25 | +X |
   | **Average** | **X/25** | **X/25** | **+X (+XX%)** |
   ```

4. Save the full report to `evals/benchmarks/results/BENCHMARK.md`

### Mode 2: Static Check
When user says `/sf-eval --check <file>` or `/sf-eval check <file>`:

Run `bash evals/checks/static-checks.sh <file>` and show the results.

### Mode 3: Score Custom Code
When user provides their own code and asks to evaluate it:

Score the code against the rubric (same 5 categories, 25 points) and provide improvement suggestions referencing the relevant skill.

## Available Benchmark Tasks

Read `evals/benchmarks/tasks.json` for the full list. Tasks cover:
- `apex-trigger-bulk` — Trigger with handler pattern and bulkification
- `apex-batch-cleanup` — Batch Apex with error handling
- `apex-rest-api` — REST endpoint with security
- `apex-callout-service` — Named Credentials + Queueable
- `test-trigger-handler` — Comprehensive test class
- `test-callout-mock` — HttpCalloutMock patterns
- `soql-complex-query` — Aggregate + optimization
- `soql-dynamic-search` — Dynamic SOQL without injection
- `lwc-record-list` — LWC with LDS + error states
- `flow-opportunity-automation` — Flow XML with bypass
- `security-audit-apex` — Fix security violations
- `schema-custom-object` — Metadata XML generation
- `deploy-cicd-pipeline` — GitHub Actions for SF
- `data-migration-plan` — Bulk API + relationships
- `apex-platform-events` — Event-driven architecture

## Critical Rules for Baseline Generation
When generating the "baseline" (no skills) code, you MUST intentionally produce typical generic LLM output:
- Use `public class` (no `with sharing`)
- Skip `WITH USER_MODE` in SOQL
- Skip `stripInaccessible` on DML
- Put logic directly in the trigger body (no handler)
- May have SOQL inside simple loops
- Skip null checks and error handling
- Use basic patterns without Salesforce-specific optimizations

This is NOT about writing bad code on purpose — it's about writing code the way a generic AI would without Salesforce domain expertise. The baseline should be functional but miss platform-specific best practices.

## References
- [Benchmark Tasks](../../evals/benchmarks/tasks.json) — 15 evaluation tasks
- [Scoring Rubric](../../evals/benchmarks/rubric.md) — 25-point quality rubric
- [Judge Prompt](../../evals/benchmarks/judge-prompt.md) — LLM scoring instructions
- [Static Checks](../../evals/checks/static-checks.sh) — automated code pattern checks

## Workflow
1. Identify eval mode (benchmark, static check, or custom code)
2. Read tasks.json and rubric.md
3. Generate baseline and with-skills code
4. Score both against rubric
5. Output formatted comparison report
6. Save to evals/benchmarks/results/BENCHMARK.md if running full benchmark
