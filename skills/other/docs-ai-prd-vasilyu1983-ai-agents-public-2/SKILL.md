---
name: docs-ai-prd
description: Write PRDs, specs, and project context optimized for coding assistants (Claude Code, Cursor, Copilot, Custom GPTs). Includes CLAUDE.md generation, session planning, and templates for creating documentation that tools can execute effectively.
---

# PRDs & Project Context

Create product requirements and project context that humans and coding assistants can execute effectively.

**Two capabilities:**
1. **PRDs & Specs** - Requirements, specs, stories, acceptance criteria
2. **Project Context** - Architecture, conventions, tribal knowledge (CLAUDE.md)

**Modern Best Practices (Jan 2026)**: Context engineering (right info, right format, right time), decision-first docs, testable requirements with acceptance criteria, metrics with formula + timeframe + data source, cross-tool portability.

## Workflow (Use This Order)

1. Pick the deliverable (PRD, AI PRD, tech spec, story map, CLAUDE.md).
2. Gather inputs (problem evidence, users, constraints, dependencies, risks).
3. Fill the template (write decisions first; keep requirements testable).
4. Validate with checklists (requirements, edge cases, security/compliance as needed).
5. Hand off with next actions (implementation plan, owners, open questions).

## Quick Reference

### PRDs & Specs

| Task | Template |
|------|----------|
| PRD creation | [assets/prd/prd-template.md](assets/prd/prd-template.md) |
| Tech spec | [assets/spec/tech-spec-template.md](assets/spec/tech-spec-template.md) |
| Planning checklist | [assets/planning/planning-checklist.md](assets/planning/planning-checklist.md) |
| Story mapping | [assets/stories/story-mapping-template.md](assets/stories/story-mapping-template.md) |
| Gherkin/BDD | [assets/stories/gherkin-example-template.md](assets/stories/gherkin-example-template.md) |
| AI PRD | [assets/prd/ai-prd-template.md](assets/prd/ai-prd-template.md) |

### Project Context (CLAUDE.md)

| Context Type | Template | Priority |
|--------------|----------|----------|
| **Architecture** | [assets/architecture-context.md](assets/architecture-context.md) | Critical |
| **Conventions** | [assets/conventions-context.md](assets/conventions-context.md) | High |
| **Key Files** | [assets/key-files-context.md](assets/key-files-context.md) | Critical |
| **Minimal Start** | [assets/minimal-claudemd.md](assets/minimal-claudemd.md) | 5-min |
| **Cross-Tool** | [assets/cross-tool-context.md](assets/cross-tool-context.md) | Multi-tool |

---

## Decision Tree

```text
User needs:
    ├─► AI-Assisted Coding?
    │   ├─ Non-trivial (>3 files)? → Planning checklist + agentic session
    │   └─ Simple (<3 files)? → Direct implementation
    │
    ├─► Project Onboarding?
    │   ├─ New to codebase? → Generate CLAUDE.md
    │   └─ Quick context? → Minimal CLAUDE.md
    │
    └─► Traditional PRD?
        ├─ Product requirements? → PRD template
        ├─ AI feature? → AI PRD template
        └─ Acceptance criteria? → Gherkin/BDD
```

---

## Cross-Tool Context Files

| Tool | Location | Notes |
|------|----------|-------|
| Claude Code | `CLAUDE.md`, `.claude/` | Auto-loaded |
| Cursor | `.cursor/rules/` | Project rules |
| Copilot | `.github/copilot-instructions.md` | Workspace context |
| Generic | `AGENTS.md` | Tool-agnostic |

---

## CLAUDE.md / AGENTS.md Guidance

- Start minimal: [assets/minimal-claudemd.md](assets/minimal-claudemd.md)
- Add only what’s needed: [assets/architecture-context.md](assets/architecture-context.md), [assets/conventions-context.md](assets/conventions-context.md), [assets/key-files-context.md](assets/key-files-context.md), [assets/dependencies-context.md](assets/dependencies-context.md), [assets/tribal-knowledge-context.md](assets/tribal-knowledge-context.md)
- Keep it executable: commands must run; include no secrets; prefer file paths over pasted code

---

## Do / Avoid

### Do

- Start with executive summary (decision, users, scope, success)
- Define acceptance criteria in testable language
- Keep requirements unambiguous (must/should/may)
- Link to supporting docs instead of pasting

### Avoid

- Vague requirements ("fast", "easy") without definitions
- Mixing draft notes and final requirements
- Metrics without measurement plan
- Docs with no owner or review cadence

---

## Context Extraction

Use:
- [references/architecture-extraction.md](references/architecture-extraction.md) for components/data flows
- [references/convention-mining.md](references/convention-mining.md) for naming/patterns
- [references/tribal-knowledge-recovery.md](references/tribal-knowledge-recovery.md) for git-history “why”
- [references/docs-audit-commands.md](references/docs-audit-commands.md) for audit commands and tool fallbacks

---

## Quality Checklist

### PRD Quality
- [ ] Clear problem statement
- [ ] Measurable success criteria
- [ ] Unambiguous acceptance criteria
- [ ] Edge cases documented
- [ ] AI can execute without clarification

### CLAUDE.md Quality
- [ ] Architecture reflects actual structure
- [ ] Key files exist at listed locations
- [ ] Conventions match actual patterns
- [ ] Commands actually work
- [ ] No sensitive information

---

## Resources

| Resource | Purpose |
|----------|---------|
| [references/agentic-coding-best-practices.md](references/agentic-coding-best-practices.md) | AI coding patterns |
| [references/requirements-checklists.md](references/requirements-checklists.md) | PRD validation |
| [references/traditional-prd-writing.md](references/traditional-prd-writing.md) | Classic PRD format |
| [references/architecture-extraction.md](references/architecture-extraction.md) | Mining architecture |
| [references/convention-mining.md](references/convention-mining.md) | Extracting conventions |
| [references/tribal-knowledge-recovery.md](references/tribal-knowledge-recovery.md) | Git history analysis |
| [references/docs-audit-commands.md](references/docs-audit-commands.md) | Audit shell commands |
| [data/sources.json](data/sources.json) | Curated external sources |

## Templates

| Category | Templates |
|----------|-----------|
| PRDs | prd-template, ai-prd-template, tech-spec-template |
| Planning | planning-checklist, agentic-session-template |
| Stories | story-mapping-template, gherkin-example-template |
| Context | architecture, conventions, key-files, minimal-claudemd |
| Stack-specific | nodejs-context, python-context, react-context, go-context |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [docs-codebase](../docs-codebase/SKILL.md) | README, API docs, ADRs |
| [qa-docs-coverage](../qa-docs-coverage/SKILL.md) | Documentation gaps |
| [product-management](../product-management/SKILL.md) | Product strategy |
| [software-architecture-design](../software-architecture-design/SKILL.md) | System design |
