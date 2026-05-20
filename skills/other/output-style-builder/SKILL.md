---
name: output-style-builder
type: standard
depth: extended
description: >-
  Creates structured output formats (JSON/YAML/Markdown-KV/XML) and response style scope
  configurations via accuracy-token tradeoff analysis. Use when defining agent schemas,
  building CLAUDE.md output sections, configuring hierarchy overrides, or standardizing
  serialization patterns across agents/commands.
---

# [H1][OUTPUT-STYLE-BUILDER]
>**Dictum:** *Parsing clarity requires structured serialization.*

<br>

Build agent response formats. Configure scope-based style.

[DELEGATE] Voice, formatting, constraint rules → `style-standards` skill.

**Tasks:**
1. Read [index.md](./index.md) — Reference file listing for navigation
2. Select domain — FORMATS (structured data) or CONFIGURATION (response style scope)
3. (formats) Read [formats.md](./references/formats.md) — Selection metrics, embedding, validation scoring
4. (configuration) Read [configuration.md](./references/configuration.md) — Scope hierarchy, embedding patterns
5. (schema) Read [schema.md](./references/schema.md) — Delimiter syntax, canonical examples
6. (structure) Read [structure.md](./references/structure.md) — Ordering patterns, composition
7. (prose) Load `style-standards` skill — Voice, formatting, constraints
8. Execute per domain — Apply Guidance and Best-Practices
9. Validate — Quality gate; see §VALIDATION

**Scope:**
- *Formats:* Structured data serialization (JSON, YAML, Markdown-KV, XML) for agent output.
- *Configuration:* Response style scope hierarchy (global → project → skill → command).

**Domain Navigation:**
- *[FORMATS]* — Structured data output. Load for: agent schemas, API responses, validation scoring.
- *[CONFIGURATION]* — Scope hierarchy. Load for: CLAUDE.md output sections, precedence rules.
- *[SCHEMA]* — Delimiters, examples. Load for: syntax reference, canonical patterns.
- *[STRUCTURE]* — Ordering, composition. Load for: section sequencing, chaining.

[REFERENCE]: [index.md](./index.md) — Complete reference file listing

---
## [1][FORMATS]
>**Dictum:** *Format optimization requires accuracy-token tradeoff analysis.*

<br>

[IMPORTANT] Format choice impacts accuracy (16pp variance) and tokens (6.75x variance).

**Guidance:**
- `Selection` — Markdown-KV: 60.7% accuracy, 2.7x tokens. JSON: 52.3% accuracy, 0.85x tokens.
- `Embedding` — Inline for single use. Reference (`@.claude/styles/`) for 3+ consumers.
- `Validation` — 100-point scoring. Deployment requires score >= 80.

**Best-Practices:**<br>
- Single format per output type.
- Max 5 variables per format; every optional has default.
- Constrained decoding guarantees 97-100% schema compliance.

**References:**<br>
- [→formats.md](./references/formats.md): Selection, embedding, validation.
- [→format.template.md](./templates/format.template.md): Format scaffold.

---
## [2][CONFIGURATION]
>**Dictum:** *Narrow context requires specialized output rules.*

<br>

[IMPORTANT] Higher precedence overrides lower (command level 5 > global level 1).

**Guidance:**
- `Global` — CLAUDE.md `[OUTPUT]` section. 50-100 LOC optimal.
- `Project` — PROJECT.md overrides. Document divergence reason.
- `Skill/Agent` — Inline or reference pattern. Match reuse requirements.
- `Command` — Narrowest scope. Specialized output for single invocation.

**Best-Practices:**<br>
- Global rules in CLAUDE.md; overrides minimal (max 30 LOC).
- Reference `style-standards` for voice/formatting rules—no duplication.
- Place weight-10 constraints first in all scopes.

**References:**<br>
- [→configuration.md](./references/configuration.md): Scope hierarchy, embedding.
- [→style.template.md](./templates/style.template.md): Style scaffold.
- [DELEGATE] `style-standards` skill: Voice, formatting, constraints.

---
## [3][SCHEMA]
>**Dictum:** *Performance consistency requires delimiter standardization.*

<br>

[IMPORTANT] Maintain delimiter consistency throughout output.

**Guidance:**
- `Delimiters` — Code fence (` ``` `), separator (`---`), soft break (`<br>`).
- `Consistency` — Prohibit mixed delimiter styles within single output.

**References:**<br>
- [→schema.md](./references/schema.md): Syntax reference.

---
## [4][STRUCTURE]
>**Dictum:** *Attention decay requires priority-first placement.*

<br>

[IMPORTANT] Primacy effect assigns 5.79x weight to early items.

**Guidance:**
- `Ordering` — Action-first, Priority-first, or Context-first patterns.
- `Hierarchy` — Maximum 3 levels. 2-7 items per container.
- `Composition` — Base-override inheritance. Shallow or deep merge.

**References:**<br>
- [→structure.md](./references/structure.md): Sequencing, composability.

---
## [5][TEMPLATES]
>**Dictum:** *Structural consistency requires scaffold reuse.*

<br>

**FORMATS Domain:**<br>
- [→format.template.md](./templates/format.template.md): Structured data format scaffold.

**CONFIGURATION Domain:**<br>
- [→style.template.md](./templates/style.template.md): Response style scaffold.

---
## [6][VALIDATION]
>**Dictum:** *Gates prevent incomplete artifacts.*

<br>

[VERIFY] Completion:
- [ ] Domain: Selected FORMATS or CONFIGURATION scope.
- [ ] References: Required domain files loaded per Tasks.
- [ ] Style: `style-standards` delegation applied—zero duplication.
- [ ] Format: Validation score >= 80 (formats domain).
- [ ] Quality: LOC within limits, weight-10 constraints first.

[REFERENCE] Operational checklist: [→validation.md](./references/validation.md)
