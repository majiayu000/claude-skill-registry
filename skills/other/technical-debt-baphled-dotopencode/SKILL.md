---
name: technical-debt
description: Identifying, documenting, and systematically managing technical debt to maintain codebase health
category: Domain Architecture
---

# Skill: technical-debt

## What I do

I provide a framework for managing technical debt. I help distinguish between strategic and unintentional debt, quantify its impact, and prioritise remediation whilst balancing delivery speed with long-term sustainability.

## When to use me

- Discovering code that requires improvement during feature development
- Planning refactoring or cleanup work for a project
- Assessing the overall health of a codebase
- Communicating quality issues and risks to stakeholders
- Prioritising remediation tasks based on impact and effort

## Core principles

1. **Strategic Debt** — Accept debt consciously to meet critical deadlines (MVP validation)
2. **Visibility** — Never leave debt hidden; document it with explicit markers
3. **Boy Scout Rule** — Always leave the code slightly better than you found it
4. **Quantified Impact** — Prioritise debt that affects high-churn files or performance
5. **Continuous Remediation** — Build debt reduction into every sprint (target <20% capacity)

## Patterns & examples

**In-Code Documentation:**
```go
// TODO(tech-debt): [HIGH] User search has O(n) complexity
// Problem: Linear search through 10k+ users causes timeouts
// Impact: Search page takes 5+ seconds, affecting customer satisfaction
// Effort: ~8 hours (add database index + refactor query)
// Tracked in: https://github.com/org/repo/issues/456
func SearchUsers(query string) []User { ... }
```

**Prioritisation Matrix:**
- **High Impact, Low Effort** — Do First (Quick wins)
- **High Impact, High Effort** — Plan & Schedule (Strategic)
- **Low Impact, Low Effort** — Fill spare time (Opportunistic)
- **Low Impact, High Effort** — Avoid (Not worth the cost)

## Anti-patterns to avoid

- ❌ **Hiding Debt** — Failing to document known issues or workarounds
- ❌ **Debt Freeze** — Stopping all progress to fix all debt (unrealistic)
- ❌ **Analysis Paralysis** — Documenting debt more than fixing it
- ❌ **Big Bang Rewrites** — Replacing the entire system at once (extremely high risk)
- ❌ **Silent Failures** — Allowing debt to cause bugs without alerting stakeholders

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Technical Debt.md`

## Related skills

- `refactor` - Systematic code refactoring techniques
- `clean-code` - Writing maintainable code to prevent future debt
- `code-reviewer` - Identifying debt during the review process
- `architecture` - Managing long-term design and structural debt
