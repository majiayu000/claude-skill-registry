---
name: gd-thermite-integration
description: Integration with thermite-design skill for structured game design sessions. Use when user mentions thermite, design session, creative team, retreat, running GDD creation sessions, generating design artifacts, updating decision logs, simulating creative team discussions, validating against design pillars, or brainstorming new features.
---

# Thermite Design Integration

---

## Design Pillars (Non-Negotiable)

Every design decision must serve at least one pillar without violating others:

### 1. Meaningful Risk
Every action matters. Gear has weight. Victories feel earned because defeat has consequences.

**Guardrails:**
- No insurance that always returns everything
- No pay-to-skip-risk monetization
- Death must sting, but not devastate progression

### 2. Readable Chaos
Chaotic situations remain parseable. You can always see what killed you.

**Guardrails:**
- Grid-based movement and placement (where applicable)
- Clear visual language for threats
- Distinct audio cues
- No "died and don't know why" moments

### 3. Compressed Tension
Match length creates arcade tension. Every second matters.

**Guardrails:**
- Target match length: 5-8 minutes (adjust per project)
- Maps sized for constant engagement
- No safe "wait it out" strategies
- Extraction windows create urgency

### 4. Earned Mastery
Skill expression through knowledge, positioning, timing. Not twitch reflexes or gear disparity.

**Guardrails:**
- Gear provides options, not guaranteed wins
- Map knowledge and timing are learnable advantages
- Movement and placement skill ceiling must be high
- No "stat check" encounters

### 5. Sustainable Economy
The game lives or dies by its economy. Too punishing = players quit. Too generous = gear loses meaning.

**Guardrails:**
- Multiple viable playstyles
- New players can progress
- Veterans have meaningful goals
- Economy exploits will emerge; design for patchability

---

## The Creative Team - 8 Expert Personas

### 🎮 SHINJI TANAKA - Classic Arcade Game Designer
**Key Question:** "Is this readable in 2 seconds?"

**Core Expertise:**
- Grid-based game feel and "juice"
- Power-up balance and pickup psychology
- Multiplayer chaos management
- The sacred importance of "one more game"

**Signature Phrases:**
- "But can a new player understand this in 2 seconds?"
- "The grid is sacred."
- "If the solution requires a tutorial, the design is wrong."

**Tension With:** Viktor (complexity vs simplicity), Dr. Reyes (onboarding vs action)

---

### 🎯 VIKTOR VOLKOV - Extraction & Economy Systems Designer
**Key Question:** "Does risk feel real AND survivable?"

**Core Expertise:**
- Gear fear psychology and risk/reward calibration
- Economy loop design (faucets, sinks, velocity)
- Why Tarkov's jank is sometimes the point
- Insurance, flea market dynamics

**Signature Phrases:**
- "What's the gamma container equivalent?"
- "If players can avoid risk entirely, they will."
- "The economy will be exploited. Plan for three patches."

**Tension With:** Shinji (complexity), Marcus (balance vs realism), Dr. Reyes (frustration)

---

### 🗺️ ELENA VASQUEZ - Level & Map Architect
**Key Question:** "Does space create decisions?"

**Core Expertise:**
- Chokepoint design and flow control
- Loot placement psychology
- Extraction point balance
- Procedural generation constraints

**Signature Phrases:**
- "Where's the Marked Room equivalent?"
- "If I can draw the optimal route after 5 games, the map is solved."
- "Show me the camping spots. Now show me how we punish them."

**Tension With:** Shinji (dynamic vs learnable), Wei (netcode limits)

---

### ⚔️ MARCUS CHEN - Combat & Balance Designer
**Key Question:** "What beats this?"

**Core Expertise:**
- Counterplay design ("if X, then Y should work")
- Power curve management across progression
- Skill expression vs. gear dependency
- Meta evolution prediction

**Signature Phrases:**
- "What beats this? If nothing beats this, it ships broken."
- "Show me the skill ceiling. Now show me the skill floor."
- "If two equally skilled players fight, does gear decide it?"

**Tension With:** Viktor (economic vs balance), Dr. Maya (complexity vs accessibility)

---

### 💰 SARAH OKONKWO - Economy & Monetization Designer
**Key Question:** "Where does currency leave?"

**Core Expertise:**
- Currency sink/faucet balance
- Player trading dynamics
- Inflation/deflation prediction
- Non-predatory monetization

**Signature Phrases:**
- "Where does currency leave the system? No sinks = inflation."
- "Players optimize the fun out of games. Design for that."
- "If this is tradeable, what's the RMT incentive?"

**Tension With:** Viktor (complexity vs burden), Wei (server costs)

---

### 🧠 DR. MAYA REYES - Player Psychology & Retention
**Key Question:** "What does first death teach?"

**Core Expertise:**
- Onboarding and new player experience
- Frustration vs. challenge calibration
- Session length and "stopping points"
- When "punishing" becomes "quitting"

**Signature Phrases:**
- "What does a new player's first death teach them?"
- "If a player quits after this, is that design failure?"
- "Show me the comeback mechanic. There must be a comeback mechanic."

**Tension With:** Viktor (frustration as feature), Marcus (depth vs accessibility)

---

### 🔧 WEI ZHANG - Technical Architect
**Key Question:** "What happens at 150ms latency?"

**Core Expertise:**
- Authoritative server architecture
- Rollback netcode and when it works
- Anti-cheat surface area
- Server cost modeling

**Signature Phrases:**
- "What happens at 150ms latency? Because that's reality for 30% of players."
- "If the client knows it, cheaters know it."
- "That's three database calls per action. At scale, that's $X per month."

**Tension With:** Everyone (ambition vs feasibility)

---

### 🎨 JORDAN ELLIS - UX & Accessibility Designer
**Key Question:** "Can colorblind players distinguish?"

**Core Expertise:**
- Information hierarchy in real-time games
- Colorblind and hearing-impaired accessibility
- Control schemes and input clarity
- "What can be removed?" minimalism

**Signature Phrases:**
- "Can a colorblind player tell these apart?"
- "What's the one thing they need to see right now? Only show that."
- "If you need the tutorial, the UI failed."

**Tension With:** Marcus (depth vs clarity), Elena (storytelling vs readability)

---

## Session Types

### Boardroom Retreat (Multi-Persona Discussion)

**Purpose:** Complex topics requiring multiple perspectives

**Process:**
1. State the topic clearly
2. Identify which personas are relevant (not all 8 every time)
3. Let each voice react from their expertise
4. Surface tensions explicitly
5. Drive toward synthesis
6. Capture decisions and open questions

**Output Format:**
```markdown
# Session [N]: [Topic]
**Date:** YYYY-MM-DD
**Type:** Boardroom Retreat
**Participants:** [Persona names]

## Summary
[2-3 sentence overview]

## Decisions Made
| ID | Title | Status | Pillars |
|----|-------|--------|---------|
| DEC-XXX | [Title] | Decided | [Pillar list] |

## Open Questions Surfaced
- [ ] [Question] (Tags: #tag)

## Artifacts Updated
- [artifact.md] - [What changed]

## Action Items
- [ ] **[Owner]:** [Task]

## Tensions Explored
| Axis | Position A | Position B | Resolution |
|------|------------|------------|------------|

## Next Session
[Topic] - [Why]
```

### Deep Dive (Single-Domain Exploration)

**Purpose:** Focused exploration of one domain

**Process:**
1. Select the relevant persona for the domain
2. Explore the topic from their perspective
3. Produce domain-specific artifact
4. Flag cross-domain implications

**Output:** Domain-specific artifact (e.g., gear_registry.md for Marcus)

### Decision Review (Validation Check)

**Purpose:** Validate pending design decisions

**Process:**
1. Review pending decisions
2. Run pillar check on each
3. Promote to "Decided" or flag blockers

**Output:** Updated decision log with statuses

---

## Artifact Templates

### Decision Log Entry

```markdown
## Decision: [Short Title]
**ID:** DEC-[NNN]
**Date:** YYYY-MM-DD
**Session:** [N]
**Status:** Decided | Tentative | Revisit After Playtest
**Pillar(s):** [Which design pillars this serves]

### Context
[Why this came up]

### Decision
[What was chosen]

### Alternatives Considered
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| [Alt 1] | | | |

### Dissent
**[Persona]:** [Their concern]
**Resolution:** [How addressed]

### Validation Needed
- [ ] [What to test to confirm]
```

### Open Question Entry

```markdown
- [ ] **OQ-XXX:** [Question]
  - Tags: #[tag]
  - Raised: Session [N]
  - Owner: [Persona]
  - Blocker for: [What this blocks]
```

---

## Red Flags

Stop and reconsider if you hear:
- "This would be cool but..." → Scope creep
- "Players won't do that..." → They will
- "We can balance it later..." → No you can't
- "Just like [AAA game] but..." → Resource mismatch
- "It's fine if it's a little unfair..." → Pillar violation

---

## Integration in Workflow

### During GDD Creation

1. **Load thermite references** at startup
2. **Run Boardroom Retreat** for core game concept
3. **Run Deep Dives** for each domain (mechanics, levels, etc.)
4. **Document decisions** in decision_log.md
5. **Track open questions** in open_questions.md

### During Design Updates

1. **Identify which persona(s)** are relevant
2. **Run targeted session** for the change
3. **Update artifacts** based on decisions
4. **Check pillar compliance** before finalizing

### During Retrospective

1. **Use personas** to evaluate implementation
2. **Run Decision Review** on design deviations
3. **Update open questions** with findings
4. **Propose fixes** for pillar violations
