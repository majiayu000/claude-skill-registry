---
name: review-documentation
description: Audit README, AHK deep-dive, and LLM development pages for broken links, stale numbers, missing features, and new highlight opportunities
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit the three documentation pages for mechanical errors and content staleness. Use your judgment on what matters — the goal is a prioritized report the human can act on, not an exhaustive lint.

## Scope

The three living documentation pages:
- `README.md` — product page (features, install, config, usage)
- `docs/what-autohotkey-can-do.md` — AHK technical showcase
- `docs/llm-development.md` — Claude Code workflow and guardrail system

**Excluded:** `docs/making-my-unteachable-ai-build-its-own-cage.md` is a published article and time capsule — do not audit it.

## Phase 1 — Mechanical Verification (High Confidence)

These are objectively right or wrong. No judgment needed.

### Link integrity

Every markdown link (`[text](path)`) in all three pages. Verify each target exists:
- Relative file links (`../src/gui/d2d_shader.ahk`, `../tools/mcode/build_mcode.ps1`, etc.)
- Cross-doc links (`what-autohotkey-can-do.md`, `llm-development.md`, etc.)
- External URLs — just verify they're well-formed, don't fetch them
- Anchor links if any

### Numbers and counts

Verify claims against the actual codebase. Use the most efficient method for each:

| Claim | How to verify |
|-------|---------------|
| Shader counts (background, mouse, selection) | Count `.hlsl` files in `src/shaders/`, `src/shaders/mouse/`, `src/shaders/selection/` (exclude `alt_tabby_common.hlsl`) |
| Static analysis check count | Run `powershell -File tests/static_analysis.ps1 -CountOnly` or count `check_*.ps1` files and estimate sub-checks from batch bundle source |
| Query tool count | Count `query_*.ps1` in `tools/` (exclude `_query_helpers.ps1`) |
| Config setting count ("200+") | Run `query_config.ps1` with no args to get section index, or count keys in `config_registry.ahk` |
| Skills count | Count directories in `.claude/skills/` |
| Compute shader pairs | Count `.hlsl` files in `src/shaders/mouse/` that have matching JSON with `"compute"` key |
| Lines of code claims | Use `wc -l` on relevant directories if a specific count is claimed |
| Ownership manifest entries | Count non-empty non-comment lines in `ownership.manifest` |

Don't obsess over exact matches — "200+ settings" is fine if the count is 215. Flag when claims are meaningfully wrong (says 183 shaders but there are now 195, says 71 checks but there are now 78).

## Phase 2 — Feature Coverage (Medium Confidence)

This requires judgment. The goal is to catch features that exist in code but aren't mentioned in documentation, or features mentioned in docs that no longer exist.

### README feature gaps

Scan `src/shared/config_registry.ahk` for top-level config sections. Each section roughly maps to a feature area. Compare against what the README mentions. New sections since the README was last written likely represent missing features.

Also check:
- New shader categories or significant shader count growth
- New command-line flags in `alt_tabby.ahk`
- New diagnostic log types
- New keyboard shortcuts or user-facing behaviors

### README stale features

Check if any features described in the README reference config keys or behaviors that no longer exist. Use `query_config.ps1 -Usage <key>` for specific keys mentioned.

### AHK page — new showcase opportunities

Look for technically impressive additions not yet covered. Potential signals:
- New files in `src/gui/`, `src/core/`, `src/shared/` that represent significant new subsystems
- New Win32 APIs being called via DllCall (grep for `DllCall` in recently modified files)
- New MCode modules beyond `icon_alpha.ahk`
- Growth in the shader pipeline (new shader types, new cbuffer fields, new compute patterns)
- New build pipeline stages in `compile.ps1`

Don't just flag everything new — use judgment on whether it's "wait, AHK does that?" material or routine development.

### LLM page — new guardrail highlights

Look for growth in the tooling that the LLM page should reflect:
- New check scripts or sub-checks not accounted for
- New query tools
- New skills worth calling out (especially review skills with novel methodologies)
- Changes to the pre-gate architecture
- New MCP integrations or context management patterns

## Phase 3 — Cross-Page Consistency (Low Priority)

Check that claims made in multiple pages agree:
- "By the Numbers" tables in both the AHK and LLM pages should have consistent values
- The README's "Behind the Scenes" summary should match what the linked pages actually describe
- Feature descriptions in README should be compatible with technical descriptions in the AHK page

## Explore Strategy

Run in parallel by page — each page is independent:
- **Agent 1**: README mechanical checks (links, feature coverage scan)
- **Agent 2**: AHK page mechanical checks (links, numbers, new showcase candidates)
- **Agent 3**: LLM page mechanical checks (links, numbers, new guardrail highlights)

After agents report, do the cross-page consistency check yourself.

## Output Format

Organize findings into two categories:

### Mechanical Issues

Objectively broken — links, numbers, references.

| Page | Issue | Type | Details | Fix |
|------|-------|------|---------|-----|
| AHK | `compile.ps1` link | Broken link | File moved to `tools/` | Update to `../tools/compile.ps1` |
| LLM | "71 checks" | Stale count | Actual count: 78 | Update to 78 |

### Content Opportunities

Subjective — features, highlights, or coverage gaps worth considering. Include enough context for the human to make a quick yes/no decision.

| Page | Opportunity | Category | Why it matters |
|------|-------------|----------|----------------|
| README | HDR support not mentioned | Missing feature | New config section `[HDR]` with 3 settings |
| AHK | New MCode module `foo.ahk` | New showcase | 400x speedup on bar operation — fits the page thesis |
| README | "Workspace Toggle" description outdated | Stale content | Now supports per-workspace shader selection |

Order by impact: broken links first, stale numbers second, missing features third, nice-to-haves last.

Ignore any existing plans — create a fresh one.
