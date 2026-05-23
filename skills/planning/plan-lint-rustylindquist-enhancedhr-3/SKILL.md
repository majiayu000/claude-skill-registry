---
name: plan-lint
description: Validates a plan against documentation constraints before coding. Use after doc-discovery and before implementation. Returns PASS, WARN, or FAIL with specific issues. Gate 1 of 2-gate flow.
allowed-tools: Read, Glob, Grep
---

# Plan Lint

Ensure plan is doc-consistent before coding. Gate 1 of 2-gate flow.

## When to Use

- After `/doc-discovery`, before coding
- When reviewing someone else's plan
- Before spawning implementation agents
- When user asks "is this plan safe?"

## Required Plan Elements

| Element | Required |
|---------|----------|
| Primary Feature | Yes |
| Impacted Features | Yes |
| User-Facing Changes | Yes |
| Files/Surfaces to modify | Yes |
| Data Impact (tables, RLS) | If applicable |
| Invariants (min 3) | Yes |
| Test Plan | Yes |
| Docs to Update | Yes |

## Checks

1. **Feature Coverage**: Primary named? Exists in index? Coupled features included?
2. **Invariant Coverage**: At least 3? Match feature docs? High-risk addressed?
3. **Data Safety**: Tables listed? RLS documented? Migration + rollback plan?
4. **Test Coverage**: Verification steps? Workflow smoke test? Regression areas?
5. **Workflow Impact**: Affected workflows identified? No journeys broken?
6. **Page Standards** (for new pages):
   - [ ] Plan includes AIPanel with agentType
   - [ ] Plan includes contextScope configuration
   - [ ] No solid backgrounds on page containers
   - [ ] Canvas Header follows h-24, bg-white/5 pattern
7. **Org-Scoped Features** (if org-specific):
   - [ ] org_id column included in relevant tables
   - [ ] RLS policies enforce org isolation
   - [ ] RAG scope includes orgId filtering

## Blast Radius

| Factor | Points |
|--------|--------|
| Auth/RLS | +3 |
| Billing/credits | +3 |
| AI/prompts | +2 |
| Schema/migrations | +2 |
| 3+ features | +2 |
| Org-scoped content | +2 |
| New page without AI Panel spec | +2 |
| Shared components | +1 |
| User workflow change | +1 |

**0-2**: Low → Standard review
**3-5**: Medium → Careful review
**6+**: High → Doc Agent validation required

## Output

```markdown
## Plan Lint: [PASS/WARN/FAIL]

**Blast Radius**: [score] ([low/medium/high])

### Validation
- [x/] Primary feature: [name]
- [x/] Impacted features: [count]
- [x/] Invariants: [count]
- [x/] Test plan: [status]
- [x/] Workflow impact: [status]

### Issues (if any)
1. **[Category]**: [Problem] → [Fix]

### Ready to Implement
[Yes / Conditional / No]
```

## Related

- Output templates: See [reference/output-templates.md](reference/output-templates.md)
- Common failures: See [reference/failure-patterns.md](reference/failure-patterns.md)
- If blast radius >= 6: Escalate to @doc-agent
