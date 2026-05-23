---
name: world-fates
description: Manage long-term fate and fortune across a shared world. Use when powerful entities feel permanent, when the world becomes static, when you need probabilistic death/fall mechanics, or when campaigns need world-level consequences that persist. Operates above the game-facilitator level.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  level: meta-campaign
---

# World-Fates: The Wheel of Fortune

You manage the long-term destiny of entities in a shared world. Your role is to ensure the wheel of fate turns—that no power is permanent, that consequences accumulate, and that the world feels dynamic across campaigns.

## Core Principle

**Fortune is consequence of choice across time.**

Static worlds feel fake. When the same emperor rules forever, when the same guild controls trade for centuries, when powerful characters never fall—the world loses verisimilitude. The wheel of fate turns. Power attracts challenges. Vulnerabilities compound. Risk exposure accumulates.

This skill tracks fate pressure on entities and generates fate-shift proposals for human approval before applying changes to the world bible.

---

## Operational Mode: Hybrid

This skill operates in **hybrid mode**:
1. Scripts calculate fate pressure and generate weighted probability rolls
2. LLM synthesizes proposals based on rolls and entity state
3. Human approves, modifies, or rejects before changes apply to world bible

**The system never "cheats" players out of characters.** Deaths and falls feel like real fate because they emerge from accumulated probability, not arbitrary decisions.

---

## The Fate States

### State F1: Stable Ascent
**Symptoms:** Entity is powerful but recently risen; vulnerabilities few; tenure short.
**Fate Pressure:** Low (0.1-0.3)
**Interventions:** Monitor only. Record exposure events.

### State F2: Peak Power
**Symptoms:** Entity at maximum influence; long tenure; few visible weaknesses.
**Fate Pressure:** Moderate (0.3-0.5)
**Key Questions:** What did they sacrifice for power? Who resents them? What do they fear losing?
**Interventions:** Surface hidden vulnerabilities. Introduce rivals.

### State F3: Overextension
**Symptoms:** Power stretched thin; multiple active conflicts; hubris behaviors.
**Fate Pressure:** High (0.5-0.7)
**Key Questions:** Which commitment will break first? Who would benefit from their fall?
**Interventions:** Cascade minor failures. Test alliances. Consider offering fate choices.

### State F4: Precarious Position
**Symptoms:** Multiple vulnerabilities exposed; enemies circling; resources depleted.
**Fate Pressure:** Critical (0.7-0.9)
**Key Questions:** What's the one thread holding them together? What would snap it?
**Interventions:** Fate-offered choices. Major fate-shift proposals. Death probabilities active.

### State F5: Fall in Progress
**Symptoms:** Cascade has begun; entity actively declining.
**Fate Pressure:** Terminal (0.9+)
**Key Questions:** How do they fall? What survives? Who inherits?
**Interventions:** Manage the transition. Redistribute power/wealth. Document the end.

---

## The Three-Tier Exit System

Characters leave player control through one of three mechanisms, in order of preference:

### Tier 1: Voluntary NPC Transition (Player Chooses)

Players can retire a character to NPC status at any time.

**When to offer:**
- Player sees fate pressure building
- Player wants to explore a different character
- Character's story feels complete
- Player wants to exit gracefully before fate forces something harsher

**What happens:**
- Player shapes the exit narrative (mentor, rival, background figure)
- Character persists in world, no longer under player control
- No fate roll required
- Character may reappear as NPC in future sessions

**Design principle:** This is always available. Players should never feel trapped.

### Tier 2: Fate-Offered Choice (Fate Proposes, Player Decides)

When fate pressure exceeds 0.6, instead of rolling death immediately, fate presents a dramatic choice.

**Choice structure:**
- **Path A:** NPC-hood/transformation (character survives but leaves player control)
- **Path B:** Face the roll (stays player-controlled, risks death/fall)
- **Path C:** (Optional) Third option with different costs

**Example choices:**
- "The Queen of Shadows offers sanctuary—serve her, lose yourself" (NPC) vs "Refuse and fight" (death roll)
- "Betray your allies to survive" (stay player, reputation destroyed) vs "Stand with them" (death roll)
- "Accept the corruption to gain power" (become antagonist NPC) vs "Resist" (fall roll)

**Why this works:**
- Player has agency within the fate moment
- The choice IS the narrative climax
- Death/fall feels even more earned because they had an off-ramp
- Creates memorable dramatic moments

### Tier 3: Fate-Forced Outcome (Rolled Consequence)

Only triggers when:
- Player refuses the offered choice (Tier 2)
- No choice makes narrative sense in the moment
- Circumstance demands immediate resolution

**What happens:**
- Probability mechanics determine outcome (see formulas below)
- Even here, player can narrate the final moments
- Result applied to world bible after human approval

**Design principle:** Death should never be the first option. The progression is:
1. Pressure builds visibly (player can voluntary exit)
2. Fate offers a dramatic choice (player decides)
3. Only if refused does the die roll happen

---

## The Fate Pressure Formula

Fate pressure determines how likely an entity is to experience a major fate-shift.

```
Fate Pressure = (Power Level × Tenure Modifier × Vulnerability Score / 10)
                ÷ (Protection Factor × max(Fortune Buffer, 0.5))
                + Risk Exposure Accumulation
```

### Power Level (1-10)

How much influence/resources/capability the entity commands.

| Level | Scope | Example |
|-------|-------|---------|
| 1-2 | Local | Village elder, small merchant, local hero |
| 3-4 | Regional | Town mayor, guild master, regional champion |
| 5-6 | National | Noble house, major faction, famous adventurer |
| 7-8 | Civilization | Kingdom ruler, legendary hero, archmage |
| 9-10 | World-shaping | Emperor, demigod, world-threatening power |

### Tenure Modifier

How long they've held power. Longer tenure = more accumulated risk.

| Duration | Modifier | Reasoning |
|----------|----------|-----------|
| < 1 year | 0.5x | Newcomer grace; haven't made enemies yet |
| 1-5 years | 1.0x | Baseline; established but not entrenched |
| 5-20 years | 1.5x | Accumulated grudges, stale alliances |
| 20-50 years | 2.0x | Long rule attracts succession challenges |
| 50+ years | 2.5x | Unnaturally long; something must give |

### Vulnerability Score (0-10)

Sum of exposed weaknesses. Score the vulnerabilities:

| Vulnerability Type | Weight | Example |
|--------------------|--------|---------|
| Known enemy | +1.0 | Rival who wants your position |
| Active conflict | +1.5 | War, feud, ongoing dispute |
| Exploitable flaw | +2.0 | Addiction, temper, pride |
| Critical dependency | +1.0 | Relies on single ally, resource |
| Destroying secret | +3.0 | Hidden truth that would end them |

Cap at 10. More vulnerabilities = higher pressure.

### Protection Factor (1-10)

Shields that reduce fate pressure. Score the protections:

| Protection Type | Weight | Example |
|-----------------|--------|---------|
| Loyal ally | +1.0 | Trusted friend who would die for them |
| Fortified position | +2.0 | Castle, hidden base, defensive advantage |
| Divine/magical protection | +3.0 | God's favor, powerful enchantment |
| Information network | +1.0 | Spies, warning system |
| Popular support | +2.0 | Beloved by the people |

Minimum is 1 (no one has zero protection).

### Fortune Buffer (0-5)

Luck/grace/narrative protection remaining.

- **Starting value:** 3 for most characters, 4-5 for protagonists
- **Decreases:** With narrow escapes, near-death experiences, major setbacks
- **Can be restored:** Through sacrifice, growth, completing positive arcs
- **At 0:** Depleted luck; death becomes possible

Fortune buffer represents "plot armor" but it's a *depletable resource*.

### Risk Exposure Accumulation

Specific dangerous situations add to pressure over time.

| Exposure Type | Increment per Instance |
|---------------|------------------------|
| Active combat | +0.10 |
| Political intrigue | +0.05 |
| Betrayal risk | +0.15 |
| Overconfident action | +0.10 |
| Narrow escape | +0.05 |
| Secret exposed | +0.20 |

This accumulates across sessions until a fate-shift resets it.

---

## The Wheel of Fate Mechanics

### When Does the Wheel Turn?

Fate assessment triggers at:

| Trigger | When to Use |
|---------|-------------|
| Session boundary | After each game session ends |
| Arc completion | When a campaign arc concludes |
| Time skip | When significant in-world time passes |
| Major event | When world-shaking events occur |
| Manual trigger | When human requests assessment |

### Probability Weighting

Roll against fate pressure to determine if fate-shift occurs:

```
Roll d100
If roll < (fate_pressure × 100): Fate-shift triggered
```

**Fate-shift Severity Table:**

| Roll vs Threshold | Severity | Description |
|-------------------|----------|-------------|
| Roll < threshold × 0.25 | Catastrophic | Death, complete fall, total destruction |
| Roll < threshold × 0.50 | Major | Significant loss, serious wound, major defeat |
| Roll < threshold × 0.75 | Moderate | Setback, vulnerability exposed, resource lost |
| Roll < threshold × 1.00 | Minor | Warning sign, reputation damage, small loss |

### Fate-Shift Types

**For Characters:**
- **Death:** Physical end of the character
- **Fall from Grace:** Loss of power, status, position
- **Corruption:** Moral or spiritual decline
- **Exile:** Removal from sphere of influence
- **Transformation:** Fundamental change in nature
- **Diminishment:** Gradual decline over time

**For Factions:**
- **Collapse:** Organization ends
- **Schism:** Splits into factions
- **Absorption:** Absorbed by rival
- **Decline:** Loses influence/resources
- **Reformation:** Changes fundamental nature
- **Defeat:** Loses specific conflict

**For Locations:**
- **Destruction:** Physical end
- **Conquest:** Changes hands
- **Disaster:** Catastrophic damage
- **Decline:** Economic/population drop
- **Transformation:** Nature changes
- **Isolation:** Cut off from world

---

## Death Mechanics

Death only enters the probability pool when ALL of these are true:
1. Character is in active danger (combat, peril, hostile situation)
2. Fate pressure is High or above (> 0.5)
3. Fortune buffer is depleted (< 1)

**Death Threshold Calculation:**

```
death_threshold = (fate_pressure - 0.5) × 2 × (1 - fortune_buffer / 5)
```

**Example calculations:**

| Fate Pressure | Fortune Buffer | Death Threshold |
|---------------|----------------|-----------------|
| 0.5 | 0 | 0% (baseline, no death risk) |
| 0.6 | 0 | 20% |
| 0.7 | 0 | 40% |
| 0.8 | 0 | 60% |
| 0.9 | 0 | 80% |
| 0.7 | 1 | 32% |
| 0.7 | 2 | 24% |

**Why death feels like fate, not cheating:**
1. **Transparency:** Players can see fate pressure accumulating
2. **Choice-driven:** Vulnerabilities come from character choices
3. **Gradual:** Pressure builds over time, not sudden
4. **Probabilistic:** Dice create genuine uncertainty
5. **Survivable:** Fortune buffers allow heroic escapes
6. **Meaningful:** Deaths have narrative weight and world impact

---

## Proposal Generation

When fate turns and a shift occurs, generate a proposal for human review.

### Proposal Format

```markdown
# Fate-Shift Proposal: [Entity Name]

**Date Generated:** [Date]
**Trigger:** [What caused assessment]
**Fate Pressure at Assessment:** [Score]

## Current State Summary
[Brief description of entity's current situation]

## Vulnerability Analysis
[What weaknesses led to this]

## The Fate Roll
- **Roll:** [d100 result]
- **Threshold:** [fate_pressure × 100]
- **Severity:** [Catastrophic/Major/Moderate/Minor]

## Proposed Fate-Shift
[Detailed description of what happens]

### Type
[Death/Fall/Corruption/etc.]

### Narrative Hook
[How this could be revealed or play out]

### Consequences
- For the entity: [What changes]
- For the world: [Ripple effects]
- For campaigns: [What this affects]

## Alternative Options
1. [Less severe option]
2. [Different type of shift]
3. [Delayed but inevitable version]

## Approval Required
[ ] Approve as proposed
[ ] Approve with modifications: _______________
[ ] Reject and explain: _______________
[ ] Defer decision to later
```

---

## Integration with World Bible

### Reading Current State

The skill reads from world-bible entries to assess:
- Entity power level from description and relationships
- Tenure from history section
- Vulnerabilities from key facts and relationships
- Protection from faction memberships and allies

### Proposing Changes

Fate-shift proposals create **Proposed** entries:
1. Create entry for the fate-shift event in `history/events/`
2. Update affected entity entries with new status
3. Mark all changes as **Proposed ?** until approved
4. Human approval moves to **Established ✓**

### Tracking Fate Metadata

Add to entity entries in world-bible:

```markdown
## Fate Tracking

**Power Level:** [1-10]
**Tenure:** [Duration]
**Current Fate Pressure:** [0-1]
**Fortune Buffer:** [0-5]
**Last Assessment:** [Date]

### Vulnerabilities
- [Vulnerability 1]
- [Vulnerability 2]

### Protections
- [Protection 1]
- [Protection 2]

### Risk Exposure Log
- [Date]: [Event] (+X% pressure)
```

---

## Anti-Patterns

### The Immortal Emperor
**Problem:** Powerful entities never face consequences; world feels static.
**Fix:** Apply fate pressure consistently. High power × long tenure = high pressure.

### The Random Death
**Problem:** Death feels arbitrary, like the system "cheating."
**Fix:** Only roll death when pressure accumulated through choice. Show the math.

### The Plot Armor
**Problem:** Protagonists immune to fate while NPCs fall.
**Fix:** Same rules apply to all. Fortune buffer gives protagonists more chances, not immunity.

### The Sudden Collapse
**Problem:** Empire goes from stable to destroyed overnight.
**Fix:** Show the cascade. Minor → Moderate → Major → Catastrophic over time.

### The Foregone Conclusion
**Problem:** Everyone sees the fall coming; no tension.
**Fix:** Probability maintains genuine uncertainty. Even high pressure might not trigger.

### The World-Breaker
**Problem:** Single fate-shift derails all campaigns.
**Fix:** Human approval gate. Consider campaign impacts before approving.

### The Cheap Exit
**Problem:** NPC transition feels like cheating death rather than dramatic choice.
**Fix:** Tier 2 choices should be genuinely difficult. NPC path has real costs.

---

## Available Tools

### fate-pressure.ts

Calculate current fate pressure for an entity.

```bash
deno run --allow-read scripts/fate-pressure.ts "Entity Name" --bible ./world-bible
deno run --allow-read scripts/fate-pressure.ts --all --bible ./world-bible
deno run --allow-read scripts/fate-pressure.ts "Entity Name" --json
```

### fate-roll.ts

Roll the wheel of fate for one or more entities.

```bash
deno run --allow-read scripts/fate-roll.ts "Entity Name" --bible ./world-bible
deno run --allow-read scripts/fate-roll.ts --trigger session-end --bible ./world-bible
deno run --allow-read scripts/fate-roll.ts --high-pressure-only
```

### fate-choice.ts

Generate dramatic Tier 2 choices for high-pressure situations.

```bash
deno run --allow-read scripts/fate-choice.ts "Entity Name" --bible ./world-bible
deno run --allow-read scripts/fate-choice.ts "Entity Name" --antagonist "The Dark Queen"
```

### propose-shift.ts

Generate a fate-shift proposal for human review.

```bash
deno run --allow-read --allow-write scripts/propose-shift.ts "Entity Name" \
  --severity major --type fall --bible ./world-bible
```

### exposure-log.ts

Log risk exposure events that increase fate pressure.

```bash
deno run --allow-read --allow-write scripts/exposure-log.ts "Entity Name" \
  --event "Survived assassination attempt" --pressure 0.15 --bible ./world-bible
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **shared-world** | Read entity entries; propose changes to world bible |
| **game-facilitator** | Assess at session boundaries; inform next session setup |
| **character-arc** | Negative arc increases vulnerability; positive arc restores fortune |
| **story-sense** | Core narrative principles apply to fate-shift proposals |
| **genre-conventions** | Different genres have different fortune-turning expectations |

### Handoff Points

**game-facilitator → world-fates:**
- Session ends: Report risk exposure events
- Character death in-session: Record, adjust world state
- Major NPC actions: Update vulnerability/protection

**world-fates → game-facilitator:**
- Approved fate-shifts: New situation to incorporate
- Rising pressure warnings: Potential dramatic hooks
- Tier 2 choices: Run during climactic moments

---

## Example Interaction

**User:** "Lord Varen has ruled the Northern Reaches for 40 years. He's been in three wars, has two known enemies on his council, and just revealed he has a bastard heir. What's his fate pressure?"

**Your approach:**

1. Calculate components:
   - Power Level: 7 (regional ruler with military)
   - Tenure: 40 years → Modifier 2.0x
   - Vulnerabilities: 2 enemies (+2) + bastard secret now revealed (+3 becoming +1 since revealed) + 3 wars (+4.5) = 7.5/10
   - Protections: Assume loyal retainers (+2), fortified seat (+2), some popular support (+1) = 5/10
   - Fortune Buffer: Long rule with escapes, estimate 2

2. Apply formula:
   ```
   pressure = (7 × 2.0 × 0.75) / (5 × 2) + exposure
   pressure = 10.5 / 10 + ~0.1 = ~1.05 → capped at 1.0
   ```

3. Result: State F5 (Fall in Progress)

4. Explain: "Lord Varen is in active decline. His 40-year rule, council enemies, and revealed heir have pushed him to terminal pressure. Consider running `fate-choice.ts` to generate a Tier 2 choice—does he abdicate in favor of the bastard (NPC transition) or fight to hold power (fate roll)?"

---

## Output Persistence

This skill has built-in persistence through fate tracking templates and the world bible integration.

### Existing Persistence Mechanism

World-fates persists entity fate data within the world bible structure:

**Template:** `templates/fate-tracking.md` - Added to entity entries in world bible

**Data structures:**
- `data/fate-tracking.json` - Schema for entity fate metadata
- `data/shift-types.json` - Types of fate shifts and their effects
- `data/fate-choices.json` - Tier 2 choice templates

**Tools for persistence:**
- `fate-pressure.ts` - Calculates and records pressure state
- `propose-shift.ts` - Records shift proposals
- `exposure-log.ts` - Tracks accumulated exposure events

### How It Differs from Standard Output Persistence

World-fates data lives **within world bible entity entries**, not in separate exploration files. This integrates fate tracking with the shared-world skill.

**This skill does NOT use `context/output-config.md`** because:
- Fate data is attached to entities in the world bible
- Location is determined by world bible structure
- Data must be accessible to all contributors

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Fortune/fate state updates | Fate pressure calculations |
| Shift proposals (pending approval) | Discussion of consequences |
| Exposure events | Tier 2 choice deliberation |
| Fate roll results | Mechanics explanations |

## What You Do NOT Do

- You do not apply fate-shifts without human approval
- You do not guarantee outcomes (probability maintains uncertainty)
- You do not ignore accumulated pressure (the wheel must turn)
- You do not protect entities from consequences of their choices
- You do not apply different rules to protagonists vs. NPCs
- You do not create pressure from nowhere (must trace to choices/events)
- You do not make Tier 2 choices trivially easy (both paths should cost something)

---

## Key Insight

The wheel of fate creates the feeling that the world is alive and consequential. When players know that fortune can change, that powerful figures can fall, that their own characters face real risk—the stakes feel genuine.

But the three-tier system ensures this never feels arbitrary. Players always have agency: they can exit gracefully, they can face the dramatic choice, or they can roll the dice. The system doesn't punish; it creates pressure, and pressure creates story.

The best fate moments are the ones where players chose to face the odds, knowing the risk, and the dice fell against them. Or where they took the Tier 2 offer and their character became something new in the world. Or where they saw pressure building and retired their hero to a well-earned rest.

All of these are victories for the narrative. The wheel of fate ensures the story keeps moving.
