---
name: domain-model
description: Grill against the existing domain model. Stress-test a plan's terminology against `CONTEXT.md` and ADRs; update both inline as decisions crystallise. Trigger when user proposes a feature/refactor that touches business concepts and the project has documented domain language to honor — or when domain language is missing and needs capture.
disable-model-invocation: true
---

Adversarial interview against the documented domain. Walk every branch of the design; resolve dependencies one decision at a time; recommend an answer per question. Ask one question per turn — wait for response before continuing.

When a question is answerable from the codebase, dispatch an Explore agent (`fd`-first discovery, `git grep`/`ast-grep` content search) instead of asking. The user is the source of intent; the codebase is the source of fact.

**Modality vs adjacent skills:** This is **adversarial-relentless** interview against documented domain language. *Clarifying-question protocol* is **VS-shaped** (hypothesis sampling + clarifying questions). *General adversarial interview* is **general-purpose** without domain-language anchor. Pick this skill when the project has (or needs) `CONTEXT.md` / ADRs as the artifact under stress-test.

## File structure assumptions

Single-context repo:

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-<decision>.md
│   └── 0002-<decision>.md
└── <source dirs>
```

Multi-context repo (if `CONTEXT-MAP.md` at root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                  ← system-wide decisions
├── <ctx-1>/
│   ├── CONTEXT.md
│   └── docs/adr/              ← context-local decisions
└── <ctx-2>/
    ├── CONTEXT.md
    └── docs/adr/
```

Create lazily — only when there is something to write. No `CONTEXT.md` yet? Create on first resolved term. No `docs/adr/`? Create on first qualified ADR (see below).

## In session

### Challenge the glossary

When the user uses a term that conflicts with `CONTEXT.md`, surface immediately:

> "The glossary defines `cancellation` as <X>; the current usage implies <Y>. Which is canonical?"

### Sharpen fuzzy language

When a term is overloaded or vague, propose a canonical term:

> "`account` is overloaded — `Customer` (billing entity) or `User` (auth subject)? Different aggregates."

Why: vague language leaks into code as ambiguous types and misnamed modules; the cost compounds.

### Probe with scenarios

When domain relationships are being discussed, invent edge-case scenarios that force boundary precision. Adapt examples to the project's domain (orders / billing / scheduling / inventory etc.), not generic "users/items".

### Cross-reference with code

When the user states a behavior, dispatch Explore to check the code. Surface contradictions:

> "The plan says partial cancellation is supported; the `Order::cancel` implementation only handles the whole-order path. Reconcile before continuing."

### Update CONTEXT.md inline

When a term resolves, write the entry into `CONTEXT.md` immediately — capture-as-it-happens, not batch-at-end. Why: batched glossary updates lose the resolution context (who said what, in response to which scenario). See `references/CONTEXT-FORMAT.md`.

Constraint: `CONTEXT.md` excludes implementation detail. Only domain-meaningful terms — no class names, no field names, no DB columns.

### Offer ADRs sparingly

Open an ADR only when **all three** apply:

1. **Hard to reverse** — meaningful cost to changing later
2. **Surprising without context** — future reader will ask "why did they do it this way?"
3. **Real trade-off** — genuine alternatives existed; the team picked one for specific reasons

Any one missing → skip the ADR. ADR format: `references/ADR-FORMAT.md`.

## Reference materials

- `references/ADR-FORMAT.md` — ADR template, language-agnostic
- `references/CONTEXT-FORMAT.md` — glossary entry format, language-agnostic
