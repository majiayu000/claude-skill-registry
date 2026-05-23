---
name: agent-audit
description: |
  When reviewing, optimizing, or inheriting an LLM agent, systematically identify
  what's actually load-bearing vs. cruft. Instruments usage, ablates components,
  and strips the agent to minimum viable form. Answers: "What can we remove
  without degrading quality?" The goal is the leanest agent that still works.
allowed-tools: |
  bash: grep, find, wc, python
  file: read, write
  mcp: task
---

# Agent Audit

<purpose>
Most agents are over-engineered. Built for edge cases that never happen. Stuffed
with tools that never get called. System prompts bloated with instructions that
don't affect behavior. Running on expensive models for tasks that don't need them.

This skill treats agent optimization like dead code elimination: instrument,
measure, identify what's actually used, strip the rest. The goal isn't "what
could be useful" but "what's actually necessary."
</purpose>

## When To Activate

Trigger when:

- Inheriting or reviewing an existing agent
- Agent costs are higher than expected
- Agent is slower than it should be
- "Can we make this cheaper/faster without breaking it?"
- Preparing for production deployment
- Refactoring agent architecture

## The Audit Framework

<framework>
```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENT AUDIT                               │
├─────────────────────────────────────────────────────────────────┤
│  1. INSTRUMENT    What's actually happening?                    │
│  2. MEASURE       How often? How much? How expensive?           │
│  3. ABLATE        What breaks if we remove X?                   │
│  4. STRIP         Remove what's not load-bearing                │
│  5. VERIFY        Does it still work? Run evals.                │
└─────────────────────────────────────────────────────────────────┘
```
</framework>

## Instructions

### Step 1: Instrument the Agent

Before optimizing, understand current behavior. Add logging for:

```
INSTRUMENTATION CHECKLIST:

□ Tool calls
  - Which tools are called?
  - How often?
  - What arguments?
  - What's returned?
  - How long do they take?

□ Model usage
  - Which model handles which tasks?
  - Token counts (input/output)
  - Latency per call
  - Cost per call

□ Context composition
  - What's in the system prompt?
  - What's retrieved/injected?
  - What's the token breakdown?

□ Control flow
  - Which branches are taken?
  - How many iterations per task?
  - Where does it loop/retry?

□ Errors and fallbacks
  - Which error paths fire?
  - How often?
  - What triggers fallbacks?
```

### Step 2: Measure Baseline

Run representative workload and capture metrics:

```
BASELINE METRICS:

Task sample: [N tasks, representative of production]

Cost:
- Total spend: $X
- Cost per task: $Y
- Breakdown: model A ($), model B ($), API calls ($)

Performance:
- Mean latency: Xms
- P95 latency: Xms
- Tokens per task: X input, Y output

Quality:
- Eval score: X%
- Error rate: X%
- Human escalation rate: X%

Component usage (from instrumentation):
- Tool A: called X times (Y% of tasks)
- Tool B: called X times (Y% of tasks)
- Tool C: called 0 times ← CANDIDATE FOR REMOVAL
```

### Step 3: Identify Audit Targets

Look for waste in these categories:

<audit-targets>
**Unused Tools**
```
Tool usage analysis:
- tool_search_docs: 847 calls (95% of tasks) ← KEEP
- tool_run_code: 234 calls (26% of tasks) ← KEEP
- tool_send_email: 0 calls (0% of tasks) ← REMOVE
- tool_calendar: 3 calls (0.3% of tasks) ← CANDIDATE
```
Question: Is the 0.3% use case worth the context cost of having the tool?

**Bloated System Prompt**
```
System prompt analysis:
- Total tokens: 2,847
- Section A (core instructions): 400 tokens - referenced in 95% of outputs
- Section B (edge case handling): 800 tokens - referenced in 3% of outputs
- Section C (formatting rules): 200 tokens - referenced in 80% of outputs
- Section D (legacy instructions): 600 tokens - never referenced ← REMOVE
```

**Over-Tiered Models**
```
Model usage analysis:
- GPT-4: 100% of calls, $0.12 average per task
- Task breakdown:
  - Complex reasoning: 15% of tasks ← NEEDS GPT-4
  - Simple extraction: 45% of tasks ← COULD BE GPT-3.5
  - Classification: 40% of tasks ← COULD BE GPT-3.5
```
Potential savings: 85% of tasks could use cheaper model.

**Unnecessary Context**
```
Context budget analysis:
- System prompt: 2,847 tokens (28%)
- Retrieved docs: 4,200 tokens (42%)
- Conversation history: 2,100 tokens (21%)
- Tool definitions: 900 tokens (9%)

Retrieved doc analysis:
- Doc chunks used in response: 1,200 tokens average
- Doc chunks ignored: 3,000 tokens average ← RETRIEVAL TOO BROAD
```

**Defensive Code That Never Fires**
```
Error handling analysis:
- Retry logic triggered: 2% of tasks
- Circuit breaker triggered: 0% of tasks ← REMOVE OR SIMPLIFY
- Fallback to secondary model: 0.1% of tasks
- Input validation failures: 0% of tasks ← MAYBE OVER-VALIDATING
```
</audit-targets>

### Step 4: Ablation Testing

For each removal candidate, test impact:

```
ABLATION TEST: [Component X]

Hypothesis: Removing X won't degrade quality

Test:
1. Run eval suite WITHOUT component X
2. Compare to baseline metrics

Results:
- Quality: 94.2% → 94.1% (within noise) ✓
- Latency: 1.2s → 0.9s (25% improvement) ✓
- Cost: $0.08 → $0.06 (25% reduction) ✓

Decision: REMOVE - no quality impact, meaningful savings
```

```
ABLATION TEST: [Component Y]

Hypothesis: Removing Y won't degrade quality

Test:
1. Run eval suite WITHOUT component Y
2. Compare to baseline metrics

Results:
- Quality: 94.2% → 87.3% (significant drop) ✗

Decision: KEEP - quality regression unacceptable
```

### Step 5: Strip and Verify

Apply removals incrementally:

```
STRIPPING PLAN:

Round 1 - Low risk removals:
□ Remove tool_send_email (0% usage)
□ Remove tool_calendar (0.3% usage, confirmed not needed)
□ Remove system prompt Section D (never referenced)
→ Run evals → Verify quality holds

Round 2 - Model tiering:
□ Route classification tasks to GPT-3.5
□ Route simple extraction to GPT-3.5
□ Keep complex reasoning on GPT-4
→ Run evals → Verify quality holds

Round 3 - Context optimization:
□ Tighten retrieval (top-3 instead of top-5)
□ Summarize conversation history beyond 3 turns
□ Trim tool definitions to essentials
→ Run evals → Verify quality holds

FINAL VERIFICATION:
- Run full eval suite on stripped agent
- Compare all metrics to baseline
- Confirm no quality regression
```

## Output Format

After audit, produce:

```markdown
## Agent Audit Report: [Agent Name]

### Baseline
| Metric | Value |
|--------|-------|
| Cost per task | $X |
| Mean latency | Xms |
| Eval score | X% |
| Context tokens | X |

### Findings

**Removable (no quality impact):**
- [Component]: [Reason] → Saves [X]
- [Component]: [Reason] → Saves [X]

**Optimizable (can downgrade):**
- [Component]: [Current] → [Proposed] → Saves [X]

**Load-bearing (must keep):**
- [Component]: [Why it's necessary]

### Recommended Stripped Config

[Minimal agent specification]

### Expected Savings
| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Cost | $X | $Y | Z% |
| Latency | Xms | Yms | Z% |
| Context | X tokens | Y tokens | Z% |

### Verification
- Eval score maintained: [X% → Y%]
- Test coverage: [N tasks]
```

## The Minimum Viable Agent Test

<mva-test>
Ask these questions:

1. **Tools:** If this tool was never called in 1000 tasks, why is it here?

2. **System prompt:** If I delete this paragraph, does output quality change?

3. **Model tier:** Could a dumber model handle this specific subtask?

4. **Context:** Is this information actually used, or just "might be useful"?

5. **Error handling:** Has this error path ever fired in production?

6. **Features:** Is this solving a real problem or an imagined one?

The MVA is the agent where every component has earned its place through
demonstrated necessity, not speculative usefulness.
</mva-test>

## NEVER

- Remove components without ablation testing
- Optimize based on intuition instead of measurement
- Strip in production without staged rollout
- Assume "might need it" justifies the cost
- Ignore the eval suite - it's your safety net
- Conflate "used rarely" with "not needed" (some rare cases are critical)

## ALWAYS

- Instrument before optimizing
- Measure baseline before changes
- Ablate one component at a time
- Verify with eval suite after each removal
- Document what was removed and why
- Keep the "before" config for rollback
- Consider: is the rare case worth the constant cost?

## Examples

### Example 1: Tool Audit

```
Agent has 12 tools defined. Instrumentation shows:

Tool                  | Calls/1000 | % Tasks | Decision
---------------------|------------|---------|----------
search_knowledge     | 2,341      | 94%     | KEEP
execute_code         | 567        | 43%     | KEEP
read_file            | 445        | 38%     | KEEP
write_file           | 234        | 21%     | KEEP
web_search           | 89         | 8%      | KEEP
send_slack           | 12         | 1%      | ABLATE TEST
create_jira          | 3          | 0.3%    | ABLATE TEST
query_database       | 0          | 0%      | REMOVE
send_email           | 0          | 0%      | REMOVE
calendar_lookup      | 0          | 0%      | REMOVE
translate_text       | 0          | 0%      | REMOVE
image_generate       | 0          | 0%      | REMOVE

Action: Remove 5 unused tools immediately (saves 450 context tokens).
Ablation test the 1% and 0.3% tools.
```

### Example 2: Model Tiering

```
Current: All tasks use Claude Opus ($15/1M input)

Task analysis:
- Intent classification: 40% of calls, simple
- Entity extraction: 30% of calls, moderate
- Complex reasoning: 20% of calls, hard
- Code generation: 10% of calls, hard

Proposed tiering:
- Haiku ($0.25/1M): Classification, simple extraction
- Sonnet ($3/1M): Moderate extraction, simple code
- Opus ($15/1M): Complex reasoning, complex code

Projected savings:
- Before: $0.15 per task average
- After: $0.04 per task average
- Reduction: 73%

Ablation results:
- Classification on Haiku: 96% accuracy (was 97%) ✓
- Extraction on Sonnet: 94% accuracy (was 95%) ✓

Decision: Implement tiering
```

### Example 3: System Prompt Trim

```
System prompt: 3,200 tokens

Ablation testing each section:

Section                    | Tokens | Quality Δ | Decision
--------------------------|--------|-----------|----------
Core identity             | 150    | -8%       | KEEP
Task instructions         | 400    | -12%      | KEEP
Output formatting         | 200    | -3%       | KEEP
Tool usage guidelines     | 300    | -2%       | KEEP
Edge case handling        | 800    | -0.5%     | TRIM (keep critical only)
Example conversations     | 600    | -0.2%     | REMOVE
Historical context        | 400    | 0%        | REMOVE
Personality guidelines    | 350    | 0%        | REMOVE

Trimmed prompt: 1,150 tokens (64% reduction)
Quality impact: -0.5% (within acceptable range)
```

<failed-attempts>
What DOESN'T work:

- **Removing without measuring:** "We probably don't need this" → broke critical edge case
- **Optimizing the wrong thing:** Spent days on prompt when model tier was the cost driver
- **Over-trimming system prompt:** Removed "obvious" instructions, quality tanked
- **Ignoring rare but critical paths:** 0.1% of tasks were high-value, removed their tool
- **A/B testing in production without eval suite:** No way to detect regression
- **Assuming all tasks are equal:** Optimized for volume, degraded high-value tasks
- **One big strip:** Changed 10 things, something broke, couldn't identify what
- **Trusting intuition over data:** "This tool seems important" - it wasn't called once
</failed-attempts>

## Why This Skill Exists

Every agent accumulates cruft. Features added "just in case." Tools for use cases
that never materialized. System prompt sections copy-pasted from templates.
Models chosen for capability ceiling, not actual need.

The result: agents that cost 3x what they should, run 2x slower than they could,
and carry context debt that crowds out actual useful information.

This skill is the discipline of asking "prove it's necessary" instead of
"prove we can remove it." The minimum viable agent isn't the starting point -
it's the goal you iterate toward by removing everything that doesn't earn its place.

Lean agents are cheaper, faster, and often more reliable. The best code is no code.
The best agent component is the one you didn't need to include.
