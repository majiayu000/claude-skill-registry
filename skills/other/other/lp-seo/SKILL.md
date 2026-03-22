---
name: lp-seo
description: S6B phased SEO strategy skill - keyword research, content clustering, SERP analysis, technical audit, and snippet optimization for any business
---

# SEO Strategy Skill (S6B)

Systematic, phased SEO planning for organic search visibility. Works for any business with web presence — SaaS, e-commerce, content, services, or B2B.

## Invocation

```bash
# Run a specific phase
/lp-seo keyword-universe --business <BIZ>
/lp-seo content-clusters --business <BIZ>
/lp-seo serp-briefs --business <BIZ>
/lp-seo tech-audit --business <BIZ>
/lp-seo snippet-optimization --business <BIZ>

# Run all phases sequentially
/lp-seo all --business <BIZ>
```

**Required**: `--business <BIZ>` flag pointing to the business directory under `docs/business-os/strategy/`.

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

**Optional flags**:
- `--locale <LOCALE>`: Target locale for keyword research (default: en-US)
- `--competitors <COMMA_SEPARATED_URLS>`: Competitor URLs for analysis
- `--existing-content <PATH>`: Path to existing content inventory for tech audit

## Module Routing

Always load `modules/phase-base-contract.md` first. Then load the relevant phase module:

| Invocation Flag | Module |
|---|---|
| `keyword-universe` | `modules/phase-1.md` |
| `content-clusters` | `modules/phase-2.md` |
| `serp-briefs` | `modules/phase-3.md` |
| `tech-audit` | `modules/phase-4.md` |
| `snippet-optimization` | `modules/phase-5.md` |

**When running `--all`**: Execute phases sequentially. Load `phase-base-contract.md` once, then dispatch each phase module in order (1→2→3→4→5). Pass phase output paths forward to the next phase. Do not reload base contract between phases.

## Integration with Startup Loop

**Upstream (required before running)**:
- lp-offer (S2B): Positioning, value prop, ICP, differentiation
- lp-channels (S6B): Confirms organic search is a prioritized channel. If organic is not prioritized, confirm with user before proceeding.

**Downstream consumers**:
- lp-content / draft-marketing: Uses Phase 3 SERP briefs for content creation
- lp-launch-qa: Uses Phase 4 tech audit checklist for SEO readiness verification

## Red Flags

Stop and ask the user if:
- Organic search was not prioritized in lp-channels output
- Keyword universe comes back under 30 keywords (indicates too-narrow scope or insufficient research)
- All keywords are high-difficulty with no quick wins
- Tech audit reveals site is not indexable (critical launch blocker — content strategy is premature)
- lp-offer artifacts are missing or positioning is unclear

## Version

1.0 — last updated 2026-02-18
