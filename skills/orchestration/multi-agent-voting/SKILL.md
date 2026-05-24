# Multi-Agent Voting Skill

Execute multi-agent voting for critical decisions using MAKER-style first-to-ahead-by-k error correction.

## When to Use

Use this skill when:
- Making critical decisions that benefit from consensus (code review, breaking changes, spec validation)
- Voting is enabled in `.spec-flow/config/voting.yaml` for the operation type
- High-stakes decisions where single-agent errors are unacceptable

## Theoretical Foundation

Based on MAKER paper (arXiv:2511.09030):
- **First-to-ahead-by-k voting**: Candidate must be k votes ahead to win
- **Formula**: `p_correct = p^k / (p^k + (1-p)^k)`
- **Scaling**: Cost grows log-linearly O(s ln s) with decomposition

With k=2 and individual agent accuracy of 70%:
- Single agent: 70% accuracy
- 3 agents with k=2: ~84% accuracy
- 5 agents with k=3: ~91% accuracy

## Prerequisites

<prerequisites>
<item>Read voting configuration</item>
<action>Read .spec-flow/config/voting.yaml</action>
<reason>Understand voting strategy and parameters for target operation</reason>
</prerequisites>

## Workflow

<workflow>
<phase name="Configuration">
<step>Determine operation type from context</step>
<step>Load operation-specific voting config from voting.yaml</step>
<step>Validate voting is enabled for this operation</step>
<step>Extract: strategy, k value, agent count, model, decorrelation settings</step>
</phase>

<phase name="Agent Spawning">
<step>Calculate temperature variations if decorrelation enabled</step>
<step>Prepare prompt variations if enabled</step>
<step>Launch N parallel agents via Task tool</step>
<format>
Each agent receives:
- Same core prompt/task
- Different temperature (if variation enabled)
- Different prompt phrasing (if variation enabled)
- Independent context (no memory of other agents)
</format>
</phase>

<phase name="Vote Collection">
<step>Collect responses from all agents</step>
<step>Apply red-flag filtering (discard flagged responses)</step>
<step>Parse structured output from each valid response</step>
<step>Extract consensus field value from each</step>
</phase>

<phase name="Consensus Determination">
<step>Apply voting strategy</step>
<strategies>
<strategy name="first_to_ahead_by_k">
Count votes for each candidate.
If any candidate is k votes ahead of all others → Winner.
If no winner after all votes → Request more samples (up to max_rounds).
If max_rounds reached → Escalate or use tie_breaker.
</strategy>
<strategy name="majority">
Candidate with >50% votes wins.
Ties use tie_breaker.
</strategy>
<strategy name="unanimous">
All agents must agree.
Any disagreement → Escalate.
</strategy>
</strategies>
</phase>

<phase name="Result Aggregation">
<step>Combine non-voting fields per aggregation rules</step>
<step>Lists: union all items</step>
<step>Numbers: take median</step>
<step>Severity: take maximum (conservative)</step>
<step>Format final result with consensus and aggregated data</step>
</phase>

<phase name="Learning">
<step>Log voting outcome to observations</step>
<step>Track: rounds to consensus, cost, agreement rate</step>
<step>Update adaptive k if accuracy threshold not met</step>
</phase>
</workflow>

## Implementation Patterns

### Spawning Parallel Agents

Use Task tool with multiple parallel invocations:

```
<parallel_agents>
<agent id="1" temperature="0.5">
[Core prompt for operation]
</agent>
<agent id="2" temperature="0.7">
[Core prompt for operation]
</agent>
<agent id="3" temperature="0.9">
[Core prompt for operation]
</agent>
</parallel_agents>
```

### Structured Output Parsing

Require agents to output in parseable format:

```yaml
# Expected output structure
verdict: PASS  # or FAIL
confidence: 0.85
issues:
  - severity: HIGH
    description: "..."
  - severity: MEDIUM
    description: "..."
```

### First-to-ahead-by-k Algorithm

```
function first_to_k_vote(votes, k):
    counts = count_each_candidate(votes)
    sorted_candidates = sort_by_count_desc(counts)

    if len(sorted_candidates) == 1:
        return sorted_candidates[0]

    leader = sorted_candidates[0]
    runner_up = sorted_candidates[1]

    if counts[leader] - counts[runner_up] >= k:
        return leader

    return NO_CONSENSUS
```

## Red Flag Integration

Before counting votes:
1. Check each response against red-flags.yaml
2. Discard responses with red flags
3. Request replacement samples if below min_votes_required
4. Only count clean responses

## Cost Optimization

Minimize c/p (cost per success), not just cost:

<cost_guidance>
<rule>Use haiku for simple validation tasks (spec completeness)</rule>
<rule>Use sonnet for complex analysis (code review, security)</rule>
<rule>Reserve opus for architecture decisions (voting optional)</rule>
<rule>Start with k=2; increase only if accuracy below threshold</rule>
<rule>Track cost vs accuracy tradeoff in learnings</rule>
</cost_guidance>

## Example: Code Review Voting

```yaml
Operation: code_review
Strategy: first_to_ahead_by_k
k: 2
Agents: 3
Model: sonnet

Agent 1 (temp 0.5): PASS, 2 issues
Agent 2 (temp 0.7): PASS, 3 issues
Agent 3 (temp 0.9): PASS, 2 issues

Vote count: PASS=3, FAIL=0
PASS leads by 3 (>= k=2) → Consensus: PASS

Aggregated issues (union): 4 unique issues
Final: PASS with 4 issues to address
```

## Example: Breaking Change Detection

```yaml
Operation: breaking_change_detection
Strategy: first_to_ahead_by_k
k: 2
Agents: 3
Tie-breaker: BREAKING (conservative)

Agent 1: NON_BREAKING
Agent 2: BREAKING
Agent 3: NON_BREAKING

Vote count: NON_BREAKING=2, BREAKING=1
NON_BREAKING leads by 1 (< k=2) → No consensus yet

Request 2 more samples:
Agent 4: NON_BREAKING
Agent 5: NON_BREAKING

New count: NON_BREAKING=4, BREAKING=1
NON_BREAKING leads by 3 (>= k=2) → Consensus: NON_BREAKING
```

## Escalation

When voting cannot reach consensus:

<escalation>
<condition>Max rounds reached without k-ahead winner</condition>
<action>
1. Present all agent responses to user
2. Show vote distribution
3. Highlight disagreement points
4. Request user decision
</action>
</escalation>

## References

- `.spec-flow/config/voting.yaml` — Voting configuration
- `.spec-flow/config/red-flags.yaml` — Red flag definitions
- `docs/maker-integration.md` — MAKER concepts documentation
