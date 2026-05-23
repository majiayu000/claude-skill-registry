---
name: gd-design-game-loop
description: Core gameplay loop design documentation. Use when defining the core gameplay loop, mapping the player experience over time, designing session structures, or identifying pacing issues.
---

# Game Loop Design

## Core Loop Template

```markdown
# Core Loop Specification v[X.X]
**Last Updated:** YYYY-MM-DD
**Owners:** [Designers]

## Loop Overview
```
[PRE-GAME] → [SESSION] → [POST-GAME] → [LOOP BACK]
```

## Session Structure

### Pre-Game Phase
**Duration:** [Target time]

**Player Actions:**
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Emotional Beat:** [Feeling player has]

**Objectives:**
- [Goal 1]
- [Goal 2]

---

### Session Start (0:00 - [X:XX])

**State:** Players [enter spawn/start]
**Objectives:** [Initial goals]
**Threats:** [What can hurt players]
**Emotional Beat:** [Feeling]

**Key Events:**
- [X:XX] - [Event 1]
- [Y:YY] - [Event 2]

---

### Early Game ([X:XX] - [Y:YY])

**State:** [Game state description]
**Objectives:** [What players should do]
**Threats:** [What challenges exist]
**Emotional Beat:** [Feeling]

---

### Mid Game ([Y:YY] - [Z:ZZ])

**State:** [Game state description]
**Objectives:** [What players should do]
**Threats:** [What challenges exist]
**Emotional Beat:** [Feeling]

---

### Late Game ([Z:ZZ] - [End])

**State:** [Game state description]
**Objectives:** [Final objectives]
**Threats:** [Maximum challenges]
**Emotional Beat:** [Feeling]

---

### End Game

**Victory Conditions:**
- [Condition 1]
- [Condition 2]

**Defeat Conditions:**
- [Condition 1]
- [Condition 2]

**Rewards:**
- [What players earn]
- [Progression updates]

---

## Post-Game Phase

**Duration:** [Target time]

**Player Actions:**
1. [Action 1]
2. [Action 2]

**Emotional Beat:** [Feeling]

**Session Loop:** [What brings players back]
```

## Loop Design Principles

### Engagement

Keep players engaged by:
- **Immediate action** - Something to do right away
- **Clear goals** - Know what to do next
- **Meaningful choices** - Decisions that matter
- **Feedback** - See results of actions

### Pacing

Create tension through:
- **Buildup** - Escalate towards climax
- **Variation** - Mix fast/slow moments
- **Surprises** - Unexpected events
- **Release** - Tension breaks

### Progression

Enable growth through:
- **Learning** - Skills improve over time
- **Unlocking** - New content available
- **Building** - Accumulate resources
- **Advancing** - Move through content

## Session Flow Diagrams

### Text-Based Flow

```
┌─────────┐
│ LOBBY   │
└────┬────┘
     │
     ▼
┌─────────┐
│ MATCH   │◄──────────────────────┐
└────┬────┘                        │
     │                            │
     ├──────────┬─────────┐      │
     │          │         │      │
     ▼          ▼         ▼      ▼
┌────────┐ ┌───────┐ ┌──────┐ ┌──────┐
│EXPLORE│ │FIGHT  │ │LOOT  │ │OBJ   │
└────────┘ └───────┘ └──────┘ └──────┘
     │          │         │      │
     └──────────┴─────────┴──────┘
                    │
                    ▼
              ┌─────────┐
              │EXTRACT  │
              └─────────┘
                    │
                    ▼
              ┌─────────┐
              │ SUMMARY │
              └────┬────┘
                   │
                   ▼
              ┌─────────┐
              │  LOBBY  │
              └─────────┘
```

## Common Loop Patterns

### Round-Based

Discrete turns with planning phases:
1. Plan phase
2. Execution phase
3. Resolution phase
4. Reward phase

### Real-Time

Continuous action with moments:
1. Constant engagement
2. Peaks and valleys
3. No pausing
4. Immediate feedback

### Session-Based

Complete matches with:
1. Preparation phase
2. Main gameplay
3. Conclusion phase
4. Summary/rewards

## Loop Review Checklist

Before finalizing the core loop:

- [ ] Minute-by-minute flow documented
- [ ] Session phases defined
- [ ] Emotional beats mapped
- [ ] Pacing is appropriate
- [ ] Engagement maintained
- [ ] Goals are clear
- [ ] Feedback is immediate
- [ ] Win/lose conditions defined
- [ ] Progression tied to loop
- [ ] Technical feasibility confirmed

---

## Multiplayer State Synchronization (NEW - 2026-01-28)

**Design considerations for server-authoritative multiplayer games.**

### State Authority Model

```
┌─────────────────────────────────────────────────────────────┐
│                      SERVER AUTHORITATIVE                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Game State │◄───│   Physics   │◄───│   Player    │     │
│  │   (Truth)   │    │  Simulation │    │   Inputs    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
         │                                          │
         │ State sync (20Hz)                        │ Input (client)
         ▼                                          ▼
┌─────────────────┐                     ┌─────────────────────┐
│  CLIENT STATE   │                     │   PREDICTED STATE   │
│  (Display only) │                     │   (Immediate feedback)│
└─────────────────┘                     └─────────────────────┘
```

### State Design Principles

**Server State (Authoritative):**
- Player positions (x, y, z, rotation)
- Health, armor, weapon state
- Match state (lobby, playing, ended)
- Projectile positions and velocities

**Client State (Predicted):**
- Local player position (client-side prediction)
- Visual effects (immediate feedback)
- UI state (local only)

**Shared State (Synced):**
- Match scores
- Leaderboard
- Player alive/dead status

### State Update Categories

| Category | Update Rate | Authority | Rollback |
|----------|-------------|-----------|----------|
| Player Input | Client → Server (immediate) | Client | No |
| Player Position | Server → Client (20Hz) | Server | Yes |
| Health/Armor | Server → Client (on change) | Server | Yes |
| Visual Effects | Client only | Client | No |
| Match State | Server → Client (on change) | Server | No |

### Prediction vs Reconciliation

```
Client sends input → Client predicts result → Display immediately
                      ↓
                      Server processes input → Sends correction
                      ↓
                      Client reconciles (smooth correction)
```

### Design Checklist for Multiplayer Features

Before adding gameplay features:

- [ ] Is this feature server-authoritative or client-authoritative?
- [ ] What happens if state sync is delayed (100ms+ latency)?
- [ ] Can this feature exploit prediction/reconciliation?
- [ ] What visual feedback is needed during network delays?
- [ ] Does this feature need rollback support?

### State Management for Multiplayer

**Store Structure:**
```
src/store/
├── connectionStore.ts  - Server connection status
├── playerStore.ts      - Local player state (predicted)
├── matchStore.ts       - Match/server state (authoritative)
└── uiStore.ts          - UI state (local only)
```

**Integration Points:**
- `connectionStore.sessionId` - Unique player identifier
- `playerStore.position` - Predicted local position
- `matchStore.players` - Server-authoritative player list
- `matchStore.leaderboard` - Synced match state

**Sources:**
- https://docs.colyseus.io/state
- https://docs.colyseus.io/state/best-practices
- **Learned from arch-002 retrospective (2026-01-28)**
