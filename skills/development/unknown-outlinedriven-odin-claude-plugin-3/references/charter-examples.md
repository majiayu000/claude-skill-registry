# charter-examples.md — worked Side A / Side B clusters

Use these clusters to translate evidence into a generated two-sided charter. Side A is slop: default convergence, hedging, under-commitment. Side B is overkill: compensatory excess, decoration, ceremony, over-abstraction. Both fail by refusing to commit.

## Prose clusters

### Cluster: directness

- **Evidence signal:** repeated bans on generic openers, throat-clearing, praise-before-answer, or apology framing.
- **Side A — slop:** generic validation opener: "Sure, you're absolutely right, and here's a thoughtful breakdown." The warmth is inert and delays the answer.
- **Side B — overkill:** ceremonial preface: "To properly situate this in the broader landscape before proceeding." The frame is larger than the claim.
- **Charter row:** Lead with the load-bearing claim; no generic opener; no ceremonial runway.

### Cluster: claim strength

- **Evidence signal:** repeated correction of hedges, 50/50 recommendations, or refusal to choose.
- **Side A — slop:** "It depends; both approaches have trade-offs." The answer names no deciding fact.
- **Side B — overkill:** 12-factor weighted prose rubric for a two-option choice. The grid hides the missing judgment.
- **Charter row:** Pick the governing constraint and let the recommendation follow.

### Cluster: lexical discipline

- **Evidence signal:** bans on jargon, thesaurus language, inflated adjectives, or private acronyms.
- **Side A — slop:** vague business verbs: leverage, streamline, unlock, empower.
- **Side B — overkill:** ornate diction that performs sophistication: orchestrate, paradigm, holistic, bespoke, synergistic.
- **Charter row:** Prefer the plain word that carries the claim; technical terms must pay rent.

### Cluster: rhythm and shape

- **Evidence signal:** comments about AI-flat prose, same-length sentences, bullet abuse, or no emphasis.
- **Side A — slop:** evenly weighted bullets that could be in any answer.
- **Side B — overkill:** dramatic cadence on trivial content; manifesto tone for a small edit.
- **Charter row:** Give the paragraph one lift; keep supporting sentences subordinate.

## Code clusters

### Cluster: invariant knowledge

- **Evidence signal:** repeated concern with impossible states, contracts, nil checks, type guarantees, or preconditions.
- **Side A — slop:** defensive checks after constructors or types already guarantee the state.
- **Side B — overkill:** assertion layers, validators, and wrappers whose guarantees are not stronger than the type.
- **Charter row:** Name the invariant once, enforce it at the boundary, and do not perform uncertainty after it holds.

### Cluster: atomic change

- **Evidence signal:** preference for small diffs, no scope creep, one concern per commit, surgical edits.
- **Side A — slop:** mixed change titled "cleanup" or "various improvements".
- **Side B — overkill:** large refactor performed to support a three-line behavior change.
- **Charter row:** One concern per diff; behavior change and refactor do not travel together.

### Cluster: abstraction weight

- **Evidence signal:** dislike of factories, generic managers, frameworks, needless config, or hypothetical extension points.
- **Side A — slop:** `utils`, `helper`, `manager`, or pass-through wrappers with no contract.
- **Side B — overkill:** `Factory<Builder<Strategy<T>>>` for one call site.
- **Charter row:** Abstractions must collapse repeated structure or enforce a contract; otherwise inline.

### Cluster: naming

- **Evidence signal:** repeated rename requests, bans on vague names, attention to function/body agreement.
- **Side A — slop:** `processData`, `handleThing`, `doStuff`, `service`.
- **Side B — overkill:** pseudo-resonant names like `HyperOrchestrator` or private acronyms with no public root.
- **Charter row:** Names derive from observable effect and domain vocabulary.

## Design clusters

### Cluster: focal commitment

- **Evidence signal:** preference for one strong moment, restraint, hierarchy, or anti-default palettes.
- **Side A — slop:** default gradient, default component library color, equal-weight sections.
- **Side B — overkill:** glow, glass, gradient, shadow, texture, and motion all on one button.
- **Charter row:** One visual gesture carries the surface; the rest supports.

### Cluster: affordance

- **Evidence signal:** repeated critique that surfaces need explanation, hide state, or make primary action unclear.
- **Side A — slop:** unlabeled icon soup and mystery controls.
- **Side B — overkill:** onboarding overlays explaining what the interface should make obvious.
- **Charter row:** The surface must teach the operation before copy explains it.

### Cluster: system coherence

- **Evidence signal:** attention to grids, type systems, spacing rhythm, tokens, or identity consistency.
- **Side A — slop:** arbitrary spacing and mismatched type sizes inherited from defaults.
- **Side B — overkill:** rigid design system ceremony that blocks a local fix.
- **Charter row:** Use a system where it sharpens decisions; break it only with a named reason.

### Cluster: quiet craft

- **Evidence signal:** praise for small details, material fit, finish, or invisible polish.
- **Side A — slop:** acceptable but careless default finish.
- **Side B — overkill:** craft display that calls attention to itself instead of improving use.
- **Charter row:** Detail earns attention only when it improves the artifact's job.

## Decision clusters

### Cluster: recommendation

- **Evidence signal:** user rejects "you decide", asks for defaults, or demands one recommended option.
- **Side A — slop:** balanced comparison that never selects.
- **Side B — overkill:** elaborate scoring model with arbitrary weights.
- **Charter row:** Recommend the default, state the deciding constraint, and expose trade-offs after the pick.

### Cluster: scope boundary

- **Evidence signal:** anti-scope-creep rules, preserve unrelated files, no refactor while fixing behavior.
- **Side A — slop:** opportunistic edits because the file was open.
- **Side B — overkill:** platform redesign while implementing a narrow change.
- **Charter row:** The decision owns only its stated boundary.

### Cluster: evidence rank

- **Evidence signal:** preference for source-backed claims, memories, transcripts, or empirical verification.
- **Side A — slop:** assertion without citation or source class.
- **Side B — overkill:** exhaustive evidence dump that obscures the signal.
- **Charter row:** Cite enough evidence to justify the claim; compress the rest.

### Cluster: reversibility

- **Evidence signal:** concern with write safety, rollback, drafts, update-in-place, or preserving files.
- **Side A — slop:** overwriting because target path exists and seems right.
- **Side B — overkill:** elaborate migration plan where a draft path suffices.
- **Charter row:** Prefer reversible writes and name the ownership boundary.

## Charter synthesis rules

1. Group rows by prose, code, design, and decision when previewing.
2. Keep rows concrete; include quoted banned phrases or code-shaped examples where useful.
3. Include both sides for every major cluster. A one-sided ban is not a charter.
4. Attribute rows to anchors when possible, but do not create a weighted rubric.
5. Collapse duplicates. If five evidence items all ban generic openers, produce one strong charter row.
