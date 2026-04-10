---
name: think-harder
description: 4-phase structured analysis wrapper for vibe pre-routing (compatible with claude-code-settings think-harder semantics).
---

# think-harder (Codex Compatibility)

Use this skill before implementation when the task needs deeper reasoning or tradeoff analysis.

## 4-Phase Analysis

1. Problem Clarification
- Define the core question and constraints.
- List assumptions and success criteria.
- Identify ambiguities that must be resolved.

2. Multi-Dimensional Analysis
- Structural decomposition: break into components/dependencies.
- Temporal impact: short-term vs long-term effects.
- Causal links: key cause-effect and feedback loops.
- Context factors: operational, team, and environmental constraints.

3. Critical Evaluation
- Challenge assumptions and possible bias.
- Compare alternatives and opportunity costs.
- Run pre-mortem: what can fail, how, and impact.
- Mark uncertainty and confidence level explicitly.

4. Synthesis
- Summarize key insights and decision rationale.
- Reconcile contradictions.
- Produce actionable next steps.

## Output Contract

1. Problem reframing
2. Key insights
3. Reasoning chain
4. Alternatives considered
5. Uncertainties
6. Actionable recommendations

## Vibe Integration

- M/L pre-routing analysis entry.
- If code-risk analysis is required, pair with `code-review`.
