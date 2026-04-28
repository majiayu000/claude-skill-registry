---
name: write-a-skill
description: Author a single new skill — produce a SKILL.md plus optional bundled references and scripts following Anthropic's progressive-disclosure conventions. Trigger when the user asks to "write a skill", "create a skill", "draft a SKILL.md", or "add a skill" for a specific capability. Distinct from repo onboarding workflows that write AGENTS.md and project conventions.
---

Skill authoring loop: gather requirements, draft against the SKILL.md contract, review with the user, refine. One concern per skill; one skill per directory. Apply the `skill-creator:skill-creator` methodology (three-level progressive disclosure, pushy descriptions, evals.json).

## Scope disambiguation

- `write-a-skill` — authors one SKILL.md for one capability inside an existing skills tree.
- *Repo onboarding* — onboards a whole repository, scaffolds AGENTS.md and project conventions.
- `skill-creator:skill-creator` — the upstream methodology this skill applies; consult it for the canonical contract.

## Authoring loop

1. **Gather requirements** — surface decisions before drafting:
   - Capability boundary: what task does the skill cover, what does it explicitly not cover?
   - Trigger phrases: which user phrases or contexts should load it?
   - Determinism: any operation deterministic enough to live in a script rather than re-generated prose?
   - Bundled references: docs, schemas, or examples to include?
   - Static guarantee context: language family (Rust, TypeScript, Python, Kotlin, Go, OCaml, …) — affects testing-charter scope.

2. **Draft the SKILL.md** — write to the contract below. Keep body terse and decision-oriented.

3. **Review with the user** — present the draft, surface ambiguous decisions, and refine.

4. **Verify** — run any bundled `evals.json` cases; targeted re-read of the SKILL.md to confirm description triggers and body alignment.

## Directory layout

```
skill-name/
  SKILL.md              # contract; required
  references/           # deeper docs loaded on-demand
    REFERENCE.md
    EXAMPLES.md
  scripts/              # deterministic helpers
    helper.{ts,py,sh}
  evals.json            # trigger / behavior evals
```

Reference paths in SKILL.md use `references/X.md`, never `./X.md`.

## SKILL.md contract

```md
---
name: skill-name
description: <what the skill does>. <when to trigger it — concrete phrases or contexts>.
---

<One-line imperative summary of the skill's posture.>

## <Section> — terse decision-oriented prose

<Body in imperative voice with brief why. ≤200 lines.>
```

Frontmatter rules:

- `name` — kebab-case, matches directory.
- `description` — pushy: name *what* AND *when*. Max 1024 chars. Third person. First sentence states capability; second sentence states triggers.
- `disable-model-invocation: true` — preserve verbatim from source if present; do not fabricate.

## Three-level progressive disclosure

1. **Description** (frontmatter) — the only text the harness reads to decide loading. Triggers must be concrete.
2. **SKILL.md body** — loaded once selected. Keep ≤200 lines; offload depth to references.
3. **references/** and **scripts/** — loaded on-demand when the body links to them.

## Pushy description — examples

Weak: *Helps with documents.*
Strong: *Extract text and tables from PDF files, fill forms, merge documents. Trigger when user mentions PDFs, forms, or document extraction.*

## Scripts vs prose

Add a script when the operation is deterministic and the same code would otherwise be regenerated each invocation. Skip scripts when the work is contextual reasoning the model must perform fresh each time.

## Voice and forbidden tooling

Imperative or third person. No "you/your" addressee. English-mandate: grammatical English, articles preserved. Banned tooling absent: prefer `bat -P -p -n`, `fd`, `git grep`, `ast-grep`, `srgn`, `hyperfine`, `difft`, `eza`, `rip` over their banned counterparts.
