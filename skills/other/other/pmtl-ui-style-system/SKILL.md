---
name: pmtl-ui-style-system
description: PMTL_VN visual system and style variants. Use for new frontend UI, redesigns, typography, layout rhythm, premium polish, and explicit style directions such as default, soft, minimalist, or redesign mode.
---

# PMTL UI Style System

## Purpose

Route PMTL frontend work to the right visual direction while keeping the canonical style layer smaller than the preserved design-library aliases.

## Use When

- Starting a new PMTL surface and needing a default visual direction.
- Redesigning an existing page or component family.
- The user asks for a specific PMTL style variant or a preserved legacy design skill.

## Expected Output

- A deliberate visual direction with the correct variant references loaded.
- Fewer overlapping style instructions across local PMTL skills.

## Variant selection

- Default: read `references/default.md`
- Soft / luxury: read `references/soft.md`
- Minimalist / editorial: read `references/minimalist.md`
- Redesign of an existing surface: read `references/redesign.md`

For the preserved design-library skills:

- If the user explicitly says `taste-skill`, read `../taste-skill/SKILL.md`
- If the user explicitly says `soft-skill`, read `../soft-skill/SKILL.md`
- If the user explicitly says `minimalist-skill`, read `../minimalist-skill/SKILL.md`
- If the user explicitly says `redesign-skill`, read `../redesign-skill/SKILL.md`

If the user does not request a variant explicitly, use the default variant.

## Shared rules

- Keep PMTL warm, calm, and premium. Avoid neon, generic SaaS gradients, and purple-glow AI defaults.
- Do not use Inter as the default personality font for premium surfaces.
- Respect mobile collapse and avoid layout gimmicks that break below `md`.
- Prefer one strong accent and restrained contrast over noisy multi-accent palettes.
- Pair this skill with `pmtl-fe-implementation` and `pmtl-ui-behavior`.

## Verification

- Confirm the chosen variant matches the user request or the default PMTL direction.
- Check that mobile collapse, hierarchy, and surface density still read clearly after styling changes.

## References

- `references/default.md`
- `references/soft.md`
- `references/minimalist.md`
- `references/redesign.md`
