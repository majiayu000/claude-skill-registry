---
name: dnd-5e-rules
description: This skill provides guidance on finding and using D&D 5e rules for campaign
  content creation.
---

# D&D 5e Rules Reference

This skill provides guidance on finding and using D&D 5e rules for campaign content creation.

## Quick Reference

For most content creation tasks, agents should:
1. Use general D&D knowledge (training data includes extensive 5e coverage)
2. State mechanical assumptions explicitly so humans can verify
3. Prefer narrative-first design over mechanical precision

## When to Look Up Rules

**Always verify:**
- Exact spell effects and ranges
- Monster stat blocks (CR, HP, AC, abilities)
- Class features at specific levels
- Magic item properties

**Usually fine from memory:**
- General combat flow (actions, bonus actions, reactions)
- Advantage/disadvantage mechanics
- Skill checks and DCs
- Common conditions (prone, grappled, frightened)

## SRD Reference Sources

### Primary: D&D 5e SRD in Markdown

The System Reference Document (SRD) contains the core rules released under Creative Commons CC-BY-4.0.

**Best repository:** [OldManUmby/DND.SRD.Wiki](https://github.com/OldManUmby/DND.SRD.Wiki)
- 362+ stars, actively maintained (updated January 2025)
- Organized into folders: Classes, Spells, Monsters, Equipment, Gamemastering
- Optimized for Obsidian.md but works as plain markdown
- Contains SRD 5.1 with all errata through November 2018

**Alternative:** [ucffool/OGL-SRD5](https://github.com/ucffool/OGL-SRD5)
- Searchable website at www.ogl-srd5.com
- Also fully maintained in markdown

### SRD 5.2 (2024 Rules)

Released April 2025, SRD 5.2 reflects the 2024 Player's Handbook revision:
- 361 pages of updated rules
- New class features (Fighter weapon mastery, Ranger spells at level 1, etc.)
- 16 additional feats (Alert, Magic Initiate, Savage Attacker, etc.)
- Updated backgrounds with ability score bonuses
- Monster stat blocks from 2025 Monster Manual

**Source:** [Official D&D Beyond SRD](https://www.dndbeyond.com/srd)
**Markdown version:** [springbov/dndsrd5.2_markdown](https://github.com/springbov/dndsrd5.2_markdown)

### Quick Reference Cheat Sheets

For session-time lookups (DCs, conditions, combat options):

**Sly Flourish's Lazy 5e Cheat Sheet** - Single page covering:
- Improvised statistics for objects/traps/hazards
- Difficulty class descriptions
- Deadly encounter benchmark
- Area of effect guidelines
- Condition descriptions
- Random names

Source: [slyflourish.com/revised_5e_cheat_sheet.html](https://slyflourish.com/revised_5e_cheat_sheet.html)

**D&D Compendium Cheat Sheets** - Multiple formats:
- Player's Actions and Effects QuickRef
- Combat Cheat Sheet
- Various presentation styles

Source: [dnd-compendium.com/player-guides/cheat-sheets](https://www.dnd-compendium.com/player-guides/cheat-sheets)

## Rules Philosophy for Content Creation

### "Right Enough" Standard

The goal is rules that enable fun roleplay, not perfect simulation. When designing content:

1. **Narrative coherence > mechanical precision** - A dragon's breath should feel terrifying even if we estimate the DC
2. **Player agency > strict rules** - If a creative solution could work, lean toward allowing it
3. **Consistency within campaign > RAW** - House rules that stick are better than looking up edge cases

### Common Agent Pitfalls

From CLAUDE.md guidance on agent limitations with rules:

> Training mixes up similar systems and homebrew. Exact modifiers and edge cases may be wrong. Always verify mechanical details against source material.

Specific watch-outs:
- Pathfinder 2e vs D&D 5e (different action economy)
- D&D 5e 2014 vs 2024 rules (significant class changes)
- Homebrew that got into training data
- Video game adaptations (Baldur's Gate 3 has differences)

### Stating Assumptions

When creating content with mechanical elements, be explicit:

**Good:**
> The trap triggers on a DC 15 Perception check to notice, DC 12 Dexterity save to avoid, dealing 2d6 piercing damage (appropriate for a level 3 party).

**Bad:**
> The trap is moderately difficult to detect and does some damage.

## Downloading SRD for Local Reference

To add SRD content to this repository for agent reference:

```bash
# Clone the SRD wiki (5.1)
git clone https://github.com/OldManUmby/DND.SRD.Wiki.git references/srd-5.1

# Or just the specific folders you need
# The full repo is ~10MB
```

Consider adding only the sections most relevant to your campaigns to keep the repo focused.

## See Also

- `references/` - Local copies of rules excerpts (if downloaded)
- `/resources/tools-and-generators.md` - Online tools for mechanics
- Campaign-specific house rules in `campaigns/<name>/CLAUDE.md`
