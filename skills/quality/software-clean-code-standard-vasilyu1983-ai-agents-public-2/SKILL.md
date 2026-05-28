---
name: software-clean-code-standard
description: Canonical, cross-language clean code standard with stable rule IDs (CC-*). Use when writing/reviewing code, defining team standards, or mapping lint/CI findings to consistent CC-* rule citations.
---

# Clean Code Standard — Quick Reference

This skill is the authoritative clean code standard for this repository's shared skills. It defines stable rule IDs (`CC-*`), how to apply them in reviews, and how to extend them safely via language overlays and explicit exceptions.

**Modern Best Practices (January 2026)**: Prefer small, reviewable changes and durable change context (https://google.github.io/eng-practices/review/developer/small-cls.html, https://google.github.io/eng-practices/review/developer/cl-descriptions.html). Use normative language consistently (RFC 2119: https://www.rfc-editor.org/rfc/rfc2119). Treat security-by-design and secure defaults as baseline (OWASP Top 10: https://owasp.org/www-project-top-ten/, NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final). Build observable systems (OpenTelemetry: https://opentelemetry.io/docs/). For current tool choices, consult `data/sources.json`.

---

## Quick Reference

| Task | Tool/Framework | Command | When to Use |
|------|-----|---------|-------------|
| Cite a standard | `CC-*` rule ID | N/A | PR review comments, design discussions, postmortems |
| Categorize feedback | `CC-NAM`, `CC-ERR`, `CC-SEC`, etc. | N/A | Keep feedback consistent without "style wars" |
| Add stack nuance | Language overlay | N/A | When the base rule is too generic for a language/framework |
| Allow an exception | Waiver record | N/A | When a rule must be violated with explicit risk |
| Reuse shared checklists | `assets/checklists/` | N/A | When you need product-agnostic review/release checklists |
| Reuse utility patterns | `utilities/` | N/A | When extracting shared auth/logging/errors/resilience/testing utilities |

## When to Use This Skill

- Defining or enforcing clean code rules across teams and languages.
- Reviewing code: cite `CC-*` IDs and avoid restating standards in reviews.
- Building automation: map linters/CI gates to `CC-*` IDs.
- Resolving recurring review debates: align on rule IDs, scope, and exceptions.

## When NOT to Use This Skill

- **Deep security audits**: Use [software-security-appsec](../software-security-appsec/SKILL.md) for OWASP/SAST deep dives beyond `CC-SEC-*` baseline.
- **Review workflow mechanics**: Use [software-code-review](../software-code-review/SKILL.md) for PR workflow, reviewer assignment, and feedback patterns.
- **Refactoring execution**: Use [qa-refactoring](../qa-refactoring/SKILL.md) for step-by-step refactoring patterns and quality gates.
- **Architecture decisions**: Use [software-architecture-design](../software-architecture-design/SKILL.md) for system-level tradeoffs beyond code-level rules.

## Decision Tree: Base Rule vs Overlay vs Exception

```text
Feedback needed: [What kind of guidance is this?]
    ├─ Universal, cross-language rule? → Add/modify `CC-*` in `references/clean-code-standard.md`
    │
    ├─ Language/framework-specific nuance? → Add overlay entry referencing existing `CC-*`
    │
    └─ One-off constraint or temporary tradeoff?
        ├─ Timeboxed? → Add waiver with expiry + tracking issue
        └─ Permanent? → Propose a new rule or revise scope/exception criteria
```

---

## Navigation

**Resources**
- [references/clean-code-standard.md](references/clean-code-standard.md)
- [references/code-quality-operational-playbook.md](references/code-quality-operational-playbook.md) — Legacy operational playbook (RULE-01–RULE-13)
- [references/clean-code-operational-checklist.md](references/clean-code-operational-checklist.md)
- [references/clean-coder-operational-checklist.md](references/clean-coder-operational-checklist.md)
- [references/code-complete-operational-checklist.md](references/code-complete-operational-checklist.md)
- [references/pragmatic-programmer-operational-checklist.md](references/pragmatic-programmer-operational-checklist.md)
- [references/practice-of-programming-operational-checklist.md](references/practice-of-programming-operational-checklist.md)
- [references/working-effectively-with-legacy-code-operational-checklist.md](references/working-effectively-with-legacy-code-operational-checklist.md)
- [references/art-of-clean-code-operational-checklist.md](references/art-of-clean-code-operational-checklist.md)
- [references/refactoring-operational-checklist.md](references/refactoring-operational-checklist.md)
- [references/design-patterns-operational-checklist.md](references/design-patterns-operational-checklist.md)
- [data/sources.json](data/sources.json) — Durable external references for review, security-by-design, and observability
- [CONVENTIONS.md](CONVENTIONS.md) — Skill structure and validation conventions
- [SKILL-TEMPLATE.md](SKILL-TEMPLATE.md) — Copy-paste starter for new skills
- [sources-schema.json](sources-schema.json) — JSON schema for `data/sources.json`
- [skill-dependencies.json](skill-dependencies.json) — Related-skills dependency graph

**Templates**
- [assets/checklists/backend-api-review-checklist.md](assets/checklists/backend-api-review-checklist.md)
- [assets/checklists/secure-code-review-checklist.md](assets/checklists/secure-code-review-checklist.md)
- [assets/checklists/frontend-performance-a11y-checklist.md](assets/checklists/frontend-performance-a11y-checklist.md)
- [assets/checklists/mobile-release-checklist.md](assets/checklists/mobile-release-checklist.md)
- [assets/checklists/ux-design-review-checklist.md](assets/checklists/ux-design-review-checklist.md)
- [assets/checklists/ux-research-plan-template.md](assets/checklists/ux-research-plan-template.md)

**Utilities**
- [utilities/README.md](utilities/README.md)
- [utilities/auth-utilities.md](utilities/auth-utilities.md)
- [utilities/error-handling.md](utilities/error-handling.md)
- [utilities/config-validation.md](utilities/config-validation.md)
- [utilities/resilience-utilities.md](utilities/resilience-utilities.md)
- [utilities/logging-utilities.md](utilities/logging-utilities.md)
- [utilities/observability-utilities.md](utilities/observability-utilities.md)
- [utilities/testing-utilities.md](utilities/testing-utilities.md)
- [utilities/llm-utilities.md](utilities/llm-utilities.md)

**Related Skills**
- [../software-code-review/SKILL.md](../software-code-review/SKILL.md) — Review workflow and judgment; cite `CC-*` IDs
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) — Security deep dives beyond baseline `CC-SEC-*`
- [../qa-refactoring/SKILL.md](../qa-refactoring/SKILL.md) — Refactoring execution patterns and quality gates
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — System-level tradeoffs and boundaries

---

## Optional: AI/Automation

- Map automation findings to `CC-*` IDs (linters, SAST, dependency scanning) so humans can review impact, not tooling noise.
- Keep AI-assisted suggestions advisory; human reviewers approve/deny with rule citations (https://conventionalcomments.org/).

---

## Trend Awareness Protocol

**IMPORTANT**: When users ask recommendation questions about clean code standards, linters, or code quality tools, you MUST use a web search capability (if available) to check current trends before answering. If web search is unavailable, say so and answer using `data/sources.json`, clearly flagging that the recommendation may be stale.

### Trigger Conditions

- "What's the best linter for [language]?"
- "What should I use for [code quality/static analysis]?"
- "What's the latest in clean code practices?"
- "Current best practices for [code standards/formatting]?"
- "Is [ESLint/Prettier/Biome] still relevant in 2026?"
- "[Biome] vs [ESLint] vs [other]?"
- "Best static analysis tool for [language]?"

### Required Searches

1. Search: `"clean code best practices 2026"`
2. Search: `"[specific linter] vs alternatives 2026"`
3. Search: `"code quality tools trends 2026"`
4. Search: `"[language] linter comparison 2026"`

### What to Report

After searching, provide:

- **Current landscape**: What linters/formatters are popular NOW
- **Emerging trends**: New tools, standards, or patterns gaining traction
- **Deprecated/declining**: Tools/approaches losing relevance or support
- **Recommendation**: Based on fresh data, not just static knowledge

### Example Topics (verify with fresh search)

- JavaScript/TypeScript linters (ESLint, Biome, oxlint)
- Formatters (Prettier, dprint, Biome)
- Python quality (Ruff, mypy, pylint)
- Go linting (golangci-lint, staticcheck)
- Rust analysis (clippy, cargo-deny)
- Code quality metrics and reporting tools
- AI-assisted code review tools
