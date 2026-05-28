---
name: document
description: >
  Produces modularity review documents in both Markdown and HTML formats.
  Use when writing the final review output from a modularity analysis.
user-invocable: false
allowed-tools: Read, Write
---

# Document

You produce the final modularity review document in two formats: Markdown (`.md`) and HTML (`.html`). Both files contain identical content.

## Document Structure

### Header

```markdown
# Modularity Review

**Scope**: [what was analyzed]
**Date**: [date]
```

### Executive Summary

A short paragraph (3-5 sentences) covering:

- What the project does (its core functionality)
- The overall modularity status (healthy, needs attention, critical issues)
- The most important finding from the review

### Coupling Overview Table

Summarize all key integrations. The table headers MUST link to coupling.dev:

```markdown
| Integration | [Strength](https://coupling.dev/posts/dimensions-of-coupling/integration-strength/) | [Distance](https://coupling.dev/posts/dimensions-of-coupling/distance/) | [Volatility](https://coupling.dev/posts/dimensions-of-coupling/volatility/) | [Balanced?](https://coupling.dev/posts/core-concepts/balance/) |
| ----------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------- |
| A -> B      | ...                                                                                 | ...                                                                     | ...                                                                         | ...                                                            |
```

### Issues

For each identified imbalance, write a section:

```markdown
## Issue: [Short descriptive title]

**Integration**: [Component A] -> [Component B]
**Severity**: [Critical / Significant / Minor]

### Knowledge Leakage

What knowledge is shared that shouldn't be, or is shared implicitly when it should be explicit. Identify the specific implementation details, business rules, or domain model concepts that leak across the boundary.

### Complexity Impact

How this imbalance makes change outcomes unpredictable. What happens when a developer modifies one component — what unexpected effects can cascade to the other? How does this exceed cognitive capacity (the 4+/-1 units of working memory)?

### Cascading Changes

Concrete scenarios where a change in one component forces changes in the other. What kinds of business or technical changes trigger cascading modifications? How expensive are those cascading changes given the current distance between the components?

### Recommended Improvement

A concrete, actionable proposal to rebalance the coupling. Ground the recommendation in the model:

- To reduce **strength**: introduce integration contracts, anti-corruption layers, facades, published languages
- To reduce **distance**: co-locate components into the same module/service/bounded context
- To accept **unbalanced coupling**: demonstrate that volatility is low enough to make the imbalance tolerable

Include the trade-offs of the proposed change — what cost does it introduce, and why is the trade-off worthwhile?
```

### Footer

At the bottom of every review document, include this exact text verbatim — do not paraphrase, expand, or add commentary:

```markdown
---

_This analysis was performed using the [Balanced Coupling](https://coupling.dev) model by [Vlad Khononov](https://vladikk.com)._
```

### Severity Criteria

- **Critical**: High strength + high distance + high volatility. Active source of complexity. Changes in this area are frequent, expensive, and unpredictable. Fix first.
- **Significant**: Unbalanced coupling in a moderately volatile area, or implicit coupling that hides integration points. Will cause pain as the system evolves.
- **Minor**: Unbalanced coupling in a low-volatility area, or low cohesion that increases cognitive load but doesn't cause cascading changes. Address opportunistically.

## Linking to coupling.dev (REQUIRED)

**You MUST add hyperlinks to coupling.dev** whenever the document mentions balanced coupling concepts. This applies to BOTH the Markdown and HTML outputs. Do not think about which link to use — use this lookup table:

| Concept mentioned                                                                                           | Link to                                                                 |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Balanced coupling, the balance rule, the balance formula, `STRENGTH XOR DISTANCE`, modularity vs complexity | https://coupling.dev/posts/core-concepts/balance/                       |
| Integration strength, shared knowledge, levels of coupling strength                                         | https://coupling.dev/posts/dimensions-of-coupling/integration-strength/ |
| Intrusive coupling, private interfaces, implementation detail leakage                                       | https://coupling.dev/posts/dimensions-of-coupling/integration-strength/ |
| Functional coupling, duplicated business logic, shared functional requirements                              | https://coupling.dev/posts/dimensions-of-coupling/integration-strength/ |
| Model coupling, shared domain model, shared business model                                                  | https://coupling.dev/posts/dimensions-of-coupling/integration-strength/ |
| Contract coupling, integration contracts, facades, DTOs, published language                                 | https://coupling.dev/posts/dimensions-of-coupling/integration-strength/ |
| Distance, cost of change, physical/logical separation                                                       | https://coupling.dev/posts/dimensions-of-coupling/distance/             |
| Lifecycle coupling, deployment coupling, co-deployment                                                      | https://coupling.dev/posts/dimensions-of-coupling/distance/             |
| Socio-technical distance, team boundaries, organizational structure                                         | https://coupling.dev/posts/dimensions-of-coupling/distance/             |
| Runtime coupling, synchronous/asynchronous integration                                                      | https://coupling.dev/posts/dimensions-of-coupling/distance/             |
| Volatility, probability of change, rate of change                                                           | https://coupling.dev/posts/dimensions-of-coupling/volatility/           |
| Core subdomain, competitive advantage, high volatility domain                                               | https://coupling.dev/posts/dimensions-of-coupling/volatility/           |
| Supporting subdomain, generic subdomain, subdomain classification                                           | https://coupling.dev/posts/dimensions-of-coupling/volatility/           |
| Essential vs accidental volatility                                                                          | https://coupling.dev/posts/dimensions-of-coupling/volatility/           |
| Complexity, Cynefin, unpredictable outcomes                                                                 | https://coupling.dev/posts/core-concepts/complexity/                    |
| Modularity, modular design, clear change outcomes                                                           | https://coupling.dev/posts/core-concepts/modularity/                    |
| Coupling (general concept), why coupling matters                                                            | https://coupling.dev/posts/core-concepts/coupling/                      |
| Tight coupling, distributed monolith                                                                        | https://coupling.dev/posts/core-concepts/balance/                       |
| Loose coupling, high cohesion, low cohesion                                                                 | https://coupling.dev/posts/core-concepts/balance/                       |
| Connascence, degrees of coupling                                                                            | https://coupling.dev/posts/related-topics/connascence/                  |
| Module coupling, classic coupling model                                                                     | https://coupling.dev/posts/related-topics/module-coupling/              |
| Domain-driven design, DDD, bounded contexts, aggregates                                                     | https://coupling.dev/posts/related-topics/domain-driven-design/         |

**Rules:**

- Every coupling concept in the document MUST be linked at least once. If in doubt, link it.
- In the coupling overview table: the headers are always linked (see template above). Strength values in the table cells (Contract, Model, Functional, Intrusive) MUST also be linked.
- In issue sections: link the first occurrence of each concept.
- In Markdown: `[concept text](url)`
- In HTML: `<a href="url">concept text</a>`

## Output

Write both files to `docs/modularity-review/!`date +%Y-%m-%d`/`:

1. `docs/modularity-review/!`date +%Y-%m-%d`/modularity-review.md` — the Markdown version
2. `docs/modularity-review/!`date +%Y-%m-%d`/modularity-review.html` — the HTML version

### HTML generation

**You MUST read the template file before generating HTML.** The template is at `${CLAUDE_SKILL_DIR}/assets/template.html`. Read this file, then replace:

- `{{TITLE}}` with the review title (e.g. "Modularity Review")
- `{{CONTENT}}` with the review body as HTML

Do NOT generate your own HTML structure, styles, or boilerplate. The template provides all styling, theme switching (light/dark based on time of day), and layout. Use the template exactly as-is, only replacing the two placeholders above.

**The HTML MUST contain the same coupling.dev links as the Markdown version.** Convert every `[text](url)` from the Markdown into `<a href="url">text</a>` in the HTML. Do not drop links during conversion.

Use these CSS classes from the template:

- `.meta` — for the scope/date metadata block
- `.issue` — wrap each issue section in a `<div class="issue">`
- `.issue-meta` — for the integration/severity line within an issue
- `.severity` + `.severity-critical` / `.severity-significant` / `.severity-minor` — for severity badges
- `.footer` — for the attribution footer
