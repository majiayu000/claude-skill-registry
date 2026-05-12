---
name: generate-my-taste
description: Evidence-first generator for a personal <name>-taste Claude Code skill. Mines local memories and agent histories for influences, slop bans, and overkill bans; asks compact confirmation forks; previews the synthesis; then writes a right-sized taste skill with exactly 5 anchors by default. Trigger with "generate my taste skill", "make my taste skill", or "derive my taste spine".
disable-model-invocation: true
---

# generate-my-taste

Generate a personal Claude Code taste skill from local evidence. The output is a `<name>-taste` skill shaped like `spine` / `taste`: frontmatter, posture, modes, two-sided charter, anchors, audit output shape, anchor mode output shape, auto-clarity exception.

Evidence leads. Questions confirm. Generation writes only after a preview gate.

## Posture

Derive taste from observed patterns, not self-report alone. Mine memories and local agent histories for repeated positive influences, Side A slop bans, and Side B overkill bans. Convert those signals into exactly 5 portable anchors unless the user explicitly selects update-in-place for an existing owned skill with a different anchor count.

Keep the generator right-sized: one generated `SKILL.md`, `references/anchors.md`, and `references/charter.md`. No scripts, no evals, no SOUL file, no elegance file, no examples skeleton.

## Modes [LOAD-BEARING]

### Mode-selection

This skill has one mode: generate. If invoked for audit of an artifact, route to an existing taste/spine skill instead.

### generate mode procedure

1. Resolve the target name.
2. Scan evidence sources.
3. Extract influence, slop, and overkill signals.
4. Ask compact confirmation forks.
5. Compose and show the synthesis preview.
6. Write generated references first and generated `SKILL.md` last.
7. Report written paths and verification notes.

## Evidence scan order

Prefer indexed sources when available; fall back to files. Missing sources are not failures.

1. Indexed ICM tools or memory search tools exposed by the current harness.
2. Indexed session-history tools exposed by the current harness.
3. Local memory files:
   - `/home/alpha/.claude/projects/**/memory/*.md`
   - `/home/alpha/.claude/projects/**/memory/**/*.md`
   - `/home/alpha/.claude/CLAUDE.md`
   - `/home/alpha/.claude/CLAUDE.local.md`
4. Local transcript and conversation stores, when readable:
   - Claude Code project histories under `/home/alpha/.claude/projects/`
   - Codex histories under common local config paths
   - Gemini CLI histories under common local config paths
   - OpenCode histories under common local config paths
   - Amp histories under common local config paths
   - Pi histories under common local config paths
   - Cursor histories under common local config paths

Treat Claude Code, Codex, Gemini CLI, OpenCode, Amp, Pi, and Cursor as optional source classes. Record missing classes in the evidence summary as `not present` or `not readable`; do not block.

Do not dump exhaustive transcripts. Extract compact evidence: quoted phrase, source class, path or index label, and inferred signal.

## Candidate inclusion criteria

Use `references/influence-catalogue.md` as the candidate pool and gate. An influence can become an anchor only when it has:

- Portable principle across at least two domains.
- Recognizable Side A and Side B failure modes.
- Concrete exemplar.
- Contrast value against neighboring candidates.
- Non-fandom operational framing.

If local evidence suggests an influence not in the catalogue, include it only when the same five criteria are satisfied; otherwise map the signal to the nearest catalogue influence and cite the mapping.

## Confirmation forks

Ask at most three questions per fire. Axis-with-default questions are single-select via `AskUserQuestion`. Put the recommended option first and append `(Recommended)` to its label. Ask only unresolved forks; evidence-backed defaults can pass straight to preview.

### Q1 — Target name, single-select

Ask only if the name is ambiguous.

- `<user-or-handle>-taste (Recommended)` — personal skill name derived from local context.
- `spine` update — only when existing `spine` is detected and update-in-place is intended.
- Custom name — free-text via annotations; do not add an explicit Other option.

### Q2 — Evidence scope, single-select

- `ICM + local files (Recommended)` — indexed recall first, direct memory/transcript inspection as fallback.
- `Local files only` — memory indexes and transcript files without indexed tools.
- `Current project only` — restrict to current checkout and its memories.

### Q3 — Domain set, single-select

- `Prose + Code + Design + Decision (Recommended)` — mirrors `taste`, `spine`, the user's two-sided table, and the fixed template fields.
- `Four-domain with one emphasis` — keep all four domains but weight examples toward the evidence-dominant domain.
- `Stop for custom template` — pause generation when a narrower domain set is required; conditional templates are out of scope for this right-sized generator.

### Q4 — Anchor picks, additive multiSelect

Q4 is the only multiSelect exception. Use it only after presenting evidence-ranked candidates. It is additive selection, not default override semantics.

- `multiSelect: true`.
- Require exactly 5 picks.
- Present 8-12 candidates, with the top 5 evidence-ranked candidates first.
- If fewer or more than 5 are selected, ask one correction question.
- If the user accepts the recommendation without edits, use the top 5 evidence-ranked candidates.

### Preview-confirmed defaults

Do not add more upfront questions merely to restate defaults. Derive these from evidence and show them in the synthesis preview:

- **Charter:** evidence-ranked Side A and Side B clusters, grouped by prose, code, design, and decision.
- **Mode discipline:** hybrid audit + anchor behavior with slash-arg override, unless evidence supports audit-only or anchor-only.
- **Collision policy:** draft new by default; update in place only for detected `spine` or `*-taste`; otherwise keep the preview gate in control of whether any write occurs.

If evidence contradicts one of these defaults, ask a separate single-select fork after Q4 and before preview. Never batch more than three questions in one `AskUserQuestion` call.

Never use `multiSelect` for Q1, Q2, Q3, preview-confirmed defaults, collision policy, or any axis-with-default question.

## Synthesis-preview gate [LOAD-BEARING]

Before any discoverable write, show a preview containing:

1. Composed frontmatter: `name` and compact `description`.
2. Evidence summary: source classes scanned, strongest quoted signals, missing optional sources.
3. 5-anchor table: anchor name, influence, concept, evidence rationale.
4. Side A charter: slop bans grouped by prose, code, design, decision.
5. Side B charter: overkill bans grouped by prose, code, design, decision.
6. Mode block: audit and anchor behavior.
7. Generated file paths.
8. Collision policy and ownership boundary.

Then ask a single-select gate:

- `Write draft (Recommended)` — proceed with safe write.
- `Revise preview` — ask for specific corrections.
- `Abort` — write nothing.

Do not write generated files before this gate.

## Write safety [LOAD-BEARING]

Use a draft path for new writes when a collision exists. Recommended draft path:

`/home/alpha/.claude/claude/skills/<name>-taste.draft/`

For non-colliding writes, use:

`/home/alpha/.claude/claude/skills/<name>-taste/`

Write order:

1. Create target directories.
2. Write `references/anchors.md`.
3. Write `references/charter.md`.
4. Write generated `SKILL.md` last.

Do not overwrite unless update-in-place was explicitly selected. Existing `spine` or `*-taste` skills can be update candidates. Update-in-place replaces only:

- `SKILL.md`
- `references/anchors.md`
- `references/charter.md`

Preserve every other file in the target skill. Preserve all files not owned by this generator.

## Generated skill shape

Use `assets/template/` as the skeleton. The generated `SKILL.md` order is fixed:

1. Frontmatter.
2. Posture.
3. Modes `[LOAD-BEARING]`.
4. Two-sided charter.
5. Anchors.
6. Audit output shape.
7. Anchor mode output shape.
8. Auto-clarity exception.

Generated skill defaults:

- Exactly 5 anchors.
- Cross-domain anchors for prose, code, design, and decisions.
- Audit mode walks all 5 anchors, cites Side A / Side B when violated, and closes with top-3 fixes.
- Anchor mode loads the 5 anchors and charter bans as imperatives.
- Auto-clarity exception suspends taste register for destructive confirmations, security or data-loss warnings, order-sensitive procedures, and direct clarification requests.

## Self-discipline

Never generate:

- Generic validation openers.
- Hedge prefaces.
- Phrases that invite skipping the discipline.
- Summary after every answer.
- Weighted rubric.
- Exhaustive transcript dump.
- Unresolved placeholders in generated output.

Template slot markers may appear only in `assets/template/`, never in generated output.

## References

| File | Load when |
|---|---|
| `references/influence-catalogue.md` | Building candidate anchors and applying inclusion criteria |
| `references/charter-examples.md` | Translating evidence into Side A / Side B charter clusters |
| `references/anchor-derivation.md` | Converting evidence into anchors and preview rationale |
| `assets/template/SKILL.md` | Writing generated skill body |
| `assets/template/references/anchors.md` | Writing generated anchor reference |
| `assets/template/references/charter.md` | Writing generated charter reference |

## Manual verification guidance

After writing a generated skill, verify:

1. Evidence scan: source classes are listed; missing optional classes are not treated as failure.
2. Question shape: Q1, Q2, Q3, and preview gate are single-select; Q4 is the only `multiSelect`; Q4 requires exactly 5 picks.
3. Generated shape: `SKILL.md` follows the fixed order above.
4. Anti-slop search: generated files contain no generic opener, hedge preface, weighted rubric, exhaustive transcript dump, or unresolved slot marker.
5. Frontmatter length: description is compact enough to be read in a skill picker; target one paragraph, not a manifesto.
6. Write safety: references were written before generated `SKILL.md`; collisions used draft path unless update-in-place was selected.
