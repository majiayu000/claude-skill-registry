---
name: spool-research
description: "Conduct structured research for feature development, technology evaluation, or problem investigation. Use when the user needs to explore options, analyze trade-offs, or investigate technical approaches."
---

# Spool Research

Structured research skill for feature development, technology evaluation, and problem investigation.

## When to Use

Use this skill when you need to:

- Evaluate technology stacks or library choices
- Research architecture patterns for a new feature
- Analyze competitive features and prioritize
- Identify pitfalls and anti-patterns to avoid
- Review a change for security, scale, or edge cases
- Synthesize research findings into recommendations

## Research Templates

This skill includes templates for different research and review activities. Use the appropriate template based on the research goal.

### Research Templates (for new features/technologies)

| Template | Use When |
|----------|----------|
| @research-stack.md | Evaluating technology choices, libraries, frameworks |
| @research-features.md | Mapping feature landscape, competitor analysis |
| @research-architecture.md | Designing system architecture, patterns |
| @research-pitfalls.md | Identifying common mistakes and anti-patterns |
| @research-synthesize.md | Combining all research into recommendations |

### Review Templates (for change proposals)

| Template | Use When |
|----------|----------|
| @review-security.md | Security audit of a change proposal |
| @review-scale.md | Performance and scaling analysis |
| @review-edge.md | Edge case and error handling review |

## Workflow

### For New Feature/Technology Research

1. **Start with stack analysis** - Use @research-stack.md to evaluate technology options
2. **Map the feature landscape** - Use @research-features.md to understand what's needed
3. **Design the architecture** - Use @research-architecture.md for patterns and decisions
4. **Identify pitfalls** - Use @research-pitfalls.md to learn from others' mistakes
5. **Synthesize findings** - Use @research-synthesize.md to create actionable recommendations

### For Change Proposal Review

1. **Security review** - Use @review-security.md to find vulnerabilities
2. **Scale review** - Use @review-scale.md to identify bottlenecks
3. **Edge case review** - Use @review-edge.md to find error handling gaps

## Output Location

Save research outputs to:
- `.spool/research/{{topic}}/` for feature/technology research
- `.spool/changes/{{change_id}}/reviews/` for change reviews

## Example Usage

### Technology Research

```
User: Research options for implementing real-time notifications

Agent: I'll use the spool-research skill to evaluate options.

1. First, I'll use @research-stack.md to compare:
   - WebSockets vs SSE vs Polling
   - Library options (socket.io, ws, etc.)

2. Then @research-architecture.md for:
   - Pub/sub patterns
   - Scaling considerations

3. Finally @research-synthesize.md to recommend an approach.
```

### Change Review

```
User: Review the auth refactor change for security issues

Agent: I'll use @review-security.md to audit the change:
- Map attack surface
- Check for auth bypasses
- Verify input validation
- Review cryptographic usage
```

## Integration with Spool Workflow

Research outputs can feed into change proposals:

1. Complete research using templates above
2. Save findings to `.spool/research/{{topic}}/`
3. Reference research in `proposal.md` or `design.md`
4. Use research to inform `tasks.md` prioritization
