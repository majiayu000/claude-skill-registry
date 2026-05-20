---
name: game-balancing
version: 0.1.0
description: >
  Use this skill when working with game balancing - economy design, difficulty
  curves, progression systems, reward schedules, playtesting analysis, or tuning
  game parameters. Triggers on any game design task involving resource sinks and
  faucets, XP curves, loot tables, difficulty scaling, player retention mechanics,
  or interpreting playtest data to adjust game feel.
category: engineering
tags: [game-design, balancing, economy, progression, playtesting, difficulty]
recommended_skills: [unity-development, game-design-patterns, product-analytics]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
  - mcp
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Game Balancing

Game balancing is the discipline of tuning numbers, curves, and systems so that a
game feels fair, engaging, and rewarding across its entire play arc. It spans
economy design (ensuring resources flow without inflation or deflation), difficulty
curves (matching challenge to player skill growth), progression systems (giving
players meaningful choices and a sense of advancement), and playtesting (using real
player data to validate or invalidate design assumptions). A well-balanced game
keeps players in flow state - challenged but never frustrated, rewarded but never
bored.

---

## When to use this skill

Trigger this skill when the user:
- Needs to design or tune an in-game economy (currencies, sinks, faucets, exchange rates)
- Wants to create or adjust a difficulty curve for levels, enemies, or encounters
- Is building a progression system (XP, skill trees, unlocks, prestige loops)
- Needs to design loot tables, drop rates, or reward schedules
- Wants to analyze playtest data to find balance problems
- Is tuning player power curves against content difficulty
- Needs to model inflation, deflation, or resource equilibrium over time
- Wants to design or evaluate a monetization-adjacent economy (free-to-play, gacha rates)

Do NOT trigger this skill for:
- General game programming or engine-specific questions (use engine-specific skills)
- Narrative design, level layout, or art direction unrelated to balance numbers

---

## Key principles

1. **Every faucet needs a sink** - For any resource entering the economy, there must
   be a corresponding drain. Without sinks, inflation is inevitable. Map every source
   of currency/items to at least one consumption mechanism. Audit the ratio regularly.

2. **Balance for the median, gate for the tail** - Tune core difficulty for the
   50th-percentile player. Use optional challenges (hard modes, bonus bosses, ranked
   ladders) to serve the top 10% and accessibility options to serve the bottom 10%.
   Never let outlier players distort the core experience.

3. **Progression must feel earned, not given** - The value of a reward is proportional
   to the perceived effort required. If players get powerful items too easily, nothing
   feels special. If progress is too slow, players churn. Target a "just right" cadence
   where each session ends with a meaningful gain.

4. **Playtest data beats intuition** - Designer instinct is a starting point, not a
   conclusion. Every balance hypothesis must be validated against real player behavior.
   Track completion rates, time-to-complete, resource stockpiles, and churn points.
   Let the data tell you where the pain is.

5. **Small changes, measured impact** - Never change more than one system at a time.
   Adjust parameters by 10-20% increments, measure, then adjust again. Large sweeping
   changes make it impossible to attribute cause and effect.

---

## Core concepts

### The Economy Loop

A game economy is a closed (or semi-closed) system of **faucets** (sources of
resources), **stocks** (player inventories/wallets), and **sinks** (consumption
points). Healthy economies maintain equilibrium where the average player's stock
grows slowly over time without runaway inflation. Model this as a flow diagram
before implementing any numbers.

### Difficulty Curves

Difficulty is the relationship between player power and content challenge over time.
The most common models are: **linear** (steady increase), **logarithmic** (steep
early, flattening later - good for onboarding), **exponential** (gentle start,
steep endgame - good for hardcore), and **sawtooth** (periodic spikes followed by
relief - good for tension pacing). Choose based on your target audience and genre.

### Progression Systems

Progression gives players a sense of growth. The key entities are: **XP/level
curves** (how much effort per level), **unlock gates** (what content opens when),
**power curves** (how stats scale with level), and **prestige/reset loops** (trading
progress for permanent bonuses). The XP curve formula `xp_for_level(n) = base *
n^exponent` is the foundation - exponent values between 1.5 and 2.5 are typical.

### Playtesting Metrics

The core metrics for balance validation are: **completion rate** (% of players
finishing a level/quest), **time-to-complete** (median session/level duration),
**resource velocity** (earn rate vs spend rate over time), **churn points** (where
players quit), and **Gini coefficient** (wealth distribution inequality among
players in multiplayer economies).

---

## Common tasks

### Design an economy with sinks and faucets

Map every resource flow in the game. For each currency or item type, list all
sources (quest rewards, drops, purchases, crafting) and all drains (shops, upgrades,
consumables, repair costs, taxes). Calculate the net flow per hour of play.

**Framework - Economy audit table:**

| Resource | Faucets (per hour) | Sinks (per hour) | Net flow | Health |
|---|---|---|---|---|
| Gold | Quests: 500, Drops: 200, Sales: 100 | Shop: 400, Repairs: 150, Tax: 50 | +200/hr | Mild inflation |
| Gems (premium) | Daily login: 5, Achievements: 2 | Gacha: 10, Cosmetics: 5 | -8/hr | Deflationary - needs more faucets |

Target net flow should be slightly positive (players feel progress) but controlled
by periodic large sinks (major upgrades, prestige resets).

> Gotcha: Multiplayer economies need a global sink (auction house tax, item
> degradation) or veteran players will hoard and crash the market.

### Build an XP/level curve

Define the effort required per level using an exponential formula. The two key
parameters are the base XP and the scaling exponent.

**Formula:** `xp_required(level) = base_xp * level ^ exponent`

| Exponent | Feel | Best for |
|---|---|---|
| 1.0 | Linear - same effort every level | Short games, tutorials |
| 1.5 | Moderate curve - accessible | RPGs, casual progression |
| 2.0 | Quadratic - standard MMO feel | MMOs, long-lifecycle games |
| 2.5 | Steep - hardcore | Prestige systems, endgame grinds |

**Example (base=100, exponent=1.8):**

| Level | XP required | Cumulative XP | Hours at 200 XP/hr |
|---|---|---|---|
| 1 | 100 | 100 | 0.5 |
| 5 | 1,552 | 4,237 | 7.8 |
| 10 | 6,310 | 22,540 | 31.5 |
| 20 | 25,119 | 130,891 | 112.7 |

> Gotcha: Always validate the curve at level 1, midpoint, and cap. If the last
> 10% of levels take more than 40% of total playtime, most players will never
> see endgame content.

### Design a difficulty curve

Choose a curve shape, then map player power and enemy/content difficulty as two
separate curves. The gap between them is the "challenge delta."

**Sawtooth pattern (recommended for most games):**
1. Each world/chapter starts slightly below player power (breathing room)
2. Ramps up to match player power by mid-chapter
3. Boss/climax exceeds player power by 10-20% (challenge spike)
4. Next chapter resets to below (reward feeling from new area)

**Checklist for difficulty tuning:**
- [ ] Can a median player complete the tutorial in under 5 minutes?
- [ ] Is the first death/failure no earlier than 10-15 minutes in?
- [ ] Does each major section have at least one "relief" moment?
- [ ] Is the final boss beatable without grinding (with skill)?
- [ ] Are optional hard challenges clearly marked as optional?

### Design loot tables and drop rates

Use weighted random selection with rarity tiers. Standard rarity distribution:

| Tier | Drop weight | Typical % | Power relative to Common |
|---|---|---|---|
| Common | 60 | 60% | 1.0x |
| Uncommon | 25 | 25% | 1.3x |
| Rare | 10 | 10% | 1.7x |
| Epic | 4 | 4% | 2.2x |
| Legendary | 1 | 1% | 3.0x |

**Pity system:** Guarantee a rare-or-better drop every N pulls to prevent
frustration streaks. Typical pity thresholds: 10 pulls for Rare, 50 for Epic,
90 for Legendary.

> Gotcha: Without a pity system, ~37% of players will go 100 pulls without a
> 1% drop. That feels terrible. Always implement pity mechanics.

### Analyze playtest data for balance issues

When reviewing playtest results, look for these red flags:

**Completion rate signals:**
- Below 70% completion on a required level = too hard, tune down
- Above 95% completion with zero deaths = too easy, tune up
- Sharp drop-off at a specific point = difficulty spike or unclear objective

**Economy signals:**
- Average player stockpile growing faster than content releases = inflation
- Players unable to afford core upgrades at the expected level = too stingy
- Top 10% of players holding 80%+ of wealth = need progressive sinks

**Session length signals:**
- Sessions under 5 minutes = poor hook, first 3 minutes need work
- Sessions over 3 hours with no break points = add natural stopping points
- Consistent 20-40 minute sessions = healthy engagement

### Tune a monetization-adjacent economy

<!-- VERIFY: These conversion benchmarks are based on general industry data
     from 2020-2024. Rates vary significantly by genre and platform. -->

For free-to-play games, balance the free and premium economies separately:

**Rules for ethical F2P balancing:**
1. Free players must be able to complete all core content (time, not money, is the gate)
2. Premium currency should buy convenience or cosmetics, not power (pay-to-skip, not pay-to-win)
3. Free currency earn rate should be ~60-70% of the "comfortable" spend rate
4. Premium items should never be more than 2x as efficient as free alternatives
5. Daily login rewards should give meaningful premium currency (5-10% of a small purchase)

---

## Anti-patterns / common mistakes

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Tuning by feel without data | Designer bias leads to difficulty that matches YOUR skill, not the median player's | Instrument everything, playtest with target audience, use completion rate data |
| Adding faucets without sinks | Economy inflates, currency becomes meaningless, late-game balance collapses | For every new reward source, add a corresponding consumption mechanism |
| Linear XP curves | Every level feels the same, no sense of acceleration or accomplishment | Use exponential curves (1.5-2.5 exponent) so early levels are fast and later ones feel earned |
| Nerfing popular strategies | Players feel punished for finding optimal play; generates resentment | Buff underused alternatives instead - bring the floor up, don't lower the ceiling |
| Changing multiple systems at once | Impossible to know which change caused which effect | Change one variable at a time, measure for at least one full play-cycle, then adjust the next |
| No pity system on random drops | ~37% of players hit frustration streaks on 1% drops within 100 attempts | Implement guaranteed minimum drops after N failed attempts |
| Flat difficulty throughout | Players either get bored (too easy) or frustrated (too hard) with no variation | Use sawtooth curves with tension peaks and relief valleys |

---

## Gotchas

1. **Balancing the median player silently destroys your hardest content** - If you tune difficulty for the 50th percentile, the top 10% of players will find late content trivial within a week of release. Segment playtesting explicitly - run sessions with expert players separately from casual ones, and tune different content tiers to different targets.

2. **Pity systems need a persistent counter, not a session counter** - If the pity counter resets on app restart or session end, players who hit the pity threshold just before quitting restart from zero next session. The pity counter must persist to permanent storage and survive all session boundaries.

3. **XP curve validation is useless without a realistic earn rate** - The formula looks right on paper, but if you model `200 XP/hr` and real players average `80 XP/hr`, the curve is 2.5x harder than designed. Always validate the curve against measured in-game earn rates from playtests, not theoretical maximums.

4. **Buffing alternatives that nobody uses doesn't fix the problem** - If one strategy is dominant because it synergizes with a core mechanic, buffing weak alternatives doesn't break the dominance - it just makes the game slightly more powerful overall. First identify WHY the dominant strategy is dominant (usually a core mechanic interaction), then address the root cause.

5. **Free-to-play "ethical" balance breaks if premium items stack** - Premium items that are individually 2x free alternatives become 8x when players stack three of them. Always model stacking scenarios during balance review, not just individual item comparisons.

---

## References

For detailed content on specific sub-domains, read the relevant file
from the `references/` folder:

- `references/economy-design.md` - Deep dive on sink/faucet modeling, inflation
  prevention, and multiplayer market dynamics
- `references/progression-formulas.md` - XP curve formulas, power scaling math,
  prestige loop design, and worked numerical examples
- `references/playtesting-guide.md` - How to run playtests, what metrics to track,
  statistical significance for small samples, and interpreting results

Only load a references file if the current task requires it - they are
long and will consume context.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
