---
name: sdd-guidelines
description: |
  Spec-Driven Development framework for maintaining documentation integrity.
  Use when: creating specifications, verifying traceability, managing multi-agent work.
  Triggers: "sdd", "spec-driven", "foundation document", "requirements traceability"
  NOT for: prototypes, single-session work, trivial scope (<1 day), learning/exploration
---

# SDD Guidelines

Reference skill for SDD concepts and procedures. For full details: [reference/guidelines-v4.4.md](reference/guidelines-v4.4.md)

## Core Concept

**Integrity** = Every artifact can answer "Why do I exist?" and "Why this form?"

```
Foundation → Requirements → Design
   ↑            ↑             ↑
 Identity    Success       Implementation
             Criteria
```

## Quick Reference

### Artifacts (§1)

| Artifact | Purpose | Key Element |
|----------|---------|-------------|
| Foundation | What this is | Identity Anchors |
| Requirements | What it must satisfy | `@aligns-to` links |
| Design | How to build it | `@derives` links |

### Links (§2)

| Link | From → To | Required |
|------|-----------|----------|
| `@aligns-to` | REQ → Foundation anchor | Yes |
| `@derives` | Design → REQ | Yes |
| `@rationale` | Any → Decision | If non-obvious |
| `@assumes` | Any → Assumption | When applicable |

### Verification (§3)

| Type | Question | Method |
|------|----------|--------|
| Alignment | REQs serve Foundation? | Heuristics |
| Traceability | Design justified? | Link check |
| Consistency | No contradictions? | Mixed |

### Status (§4)

```
draft → verified → obsolete
  ↓        ↓
blocked ←←←┘ (on change)
```

## Path Convention

All `depends_on` and `inherits` paths are relative to **project root** (no leading slash).

```yaml
# In packages/react-sample/spec/react-sample.requirements.md
depends_on:
  - packages/react-sample/spec/react-sample.foundation.md@1.0.0
inherits:
  - spec/foundation.md@1.0.0
```

| ❌ Wrong | ✅ Correct |
|----------|------------|
| `../../spec/foundation.md` | `spec/foundation.md` |
| `/spec/foundation.md` | `spec/foundation.md` |
| `./react-sample.foundation.md` | `packages/react-sample/spec/react-sample.foundation.md` |

## Instructions

| Task | Read | Key Actions |
|------|------|-------------|
| Start a project | §1.1 | Create Foundation with Identity Anchors |
| Add requirements | §1.2 | Write REQs, add `@aligns-to` for each |
| Write design | §1.3-1.4 | Add `@derives`, document decisions |
| Verify integrity | §3 | Run alignment → traceability checks |
| Track state | §4 | Status per item, handoffs, state file |
| Handle changes | §5 | Propagate: Foundation → REQs → Design |
| Fix broken state | §6 | Detect gaps, restore links |
| Scale to subsystems | §7 | Nested structure, inheritance rules |
| Track versions | §8 | MAJOR.MINOR.PATCH, changelogs |
| Customize for project | §9 | Prefixes, ID formats, severity levels |
| Coordinate agents | §10 | Ownership, locking, escalation |

## Subsystem Checklist

When creating a subsystem (package, module, etc.):

1. [ ] Create Foundation first (`inherits:` parent foundation)
2. [ ] Define subsystem-specific anchors
3. [ ] Create Requirements (`depends_on:` subsystem foundation)
4. [ ] Create Design later (`depends_on:` subsystem requirements)

```
{project}/
├── spec/
│   └── foundation.md          ← parent
└── packages/{name}/
    └── spec/
        ├── {name}.foundation.md      ← inherits parent
        ├── {name}.requirements.md    ← depends_on foundation
        └── {name}.design.md          ← depends_on requirements
```

## Common Mistakes

| Mistake | Why Wrong | Correct |
|---------|-----------|---------|
| Requirements + Design in one doc | Artifacts are separate (§1) | Split into separate files |
| Subsystem without Foundation | Subsystems need identity (§7.2) | Create Foundation first |
| `@aligns-to` in Design | Design links to REQs, not anchors | Use `@derives` |
| `@derives` in Requirements | REQs link to anchors, not other REQs | Use `@aligns-to` |
| Implementation details in REQs | REQs are what, not how | Move to Design |
| Relative paths in `depends_on` | Fragile, breaks on move | Use project-root paths |

## Resources

| Resource | Content |
|----------|---------|
| [reference/guidelines-v4.4.md](reference/guidelines-v4.4.md) | Complete structural rules |
| [reference/philosophy-v5.md](reference/philosophy-v5.md) | Why integrity matters |
| [reference/examples.md](reference/examples.md) | Concrete examples for each artifact |
