---
name: debate
description: Use when evaluating competing options or stress-testing a proposal, typically after brainstorming. Supports quick, thorough, adversarial, and collaborative styles.
invocation: agent
---

# Debate

Run structured debate rounds with assigned roles to evaluate competing options or stress-test a proposal. Use this in the Full tier after brainstorming, or any time a decision needs rigorous evaluation.

## Debate Styles

### Quick

Two rounds maximum. One proponent, one opponent. Best for binary decisions with clear tradeoffs. Time-boxed and focused on the top 2-3 differentiating factors.

### Thorough

Three to five rounds. Multiple roles (proponent, opponent, domain expert, end-user advocate). Covers technical feasibility, user impact, maintenance cost, and risk. Use when the decision has significant long-term consequences.

### Adversarial

Dedicated red-team approach. The opponent actively tries to break the proposal by finding edge cases, failure modes, security issues, and scalability limits. The proponent must defend or concede each point. Use for security-sensitive or high-risk architectural decisions.

### Collaborative

All participants work toward the best synthesis rather than defending fixed positions. Each round builds on the previous one. Participants may change positions as new information surfaces. Use when the goal is refinement rather than selection.

## Round Structure

Each round follows this sequence:

1. **Opening statement** — Each role presents their position with supporting evidence.
2. **Challenge** — Opposing roles identify weaknesses, missing considerations, or counterexamples.
3. **Response** — Challenged roles address the points raised, conceding where appropriate.
4. **Synthesis** — Summarize what was established, what remains contested, and what new information emerged.

## Output Format

```markdown
## Debate: [Topic]

### Style: [quick|thorough|adversarial|collaborative]

### Round N
**[Role]**: [position and evidence]
**[Role]**: [challenge or response]
**Synthesis**: [what was established]

### Verdict
**Decision**: [selected option or refined proposal]
**Confidence**: [high|medium|low]
**Key factors**: [top 3 deciding factors]
**Dissent**: [any unresolved objections worth noting]
```

## Claude-Only Mode

When external providers are unavailable, simulate multiple perspectives by:

1. Explicitly labeling each role before writing its argument.
2. Genuinely steelmanning each position — do not create strawmen.
3. Tracking concessions and adjustments across rounds.
4. Producing a final synthesis that reflects the actual arguments made, not a predetermined conclusion.

## When to Use Debate vs. Brainstorm

- **Brainstorm** generates options. Use when the solution space is unexplored.
- **Debate** evaluates options. Use when 2-4 clear alternatives exist and a decision is needed.

A common Full-tier sequence: brainstorm to generate options, then debate to select among them.
