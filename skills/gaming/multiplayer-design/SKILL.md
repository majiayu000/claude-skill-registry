---
name: Multiplayer Design (Conceptual)
description: |
  Use this skill for CONCEPTUAL multiplayer design - game modes, cooperation patterns, and player dynamics. Trigger phrases: "co-op design", "asymmetric multiplayer", "competitive balance", "how to design multiplayer", "controller sharing ideas", "versus mode design".

  This skill provides GAME DESIGN THEORY - what makes good multiplayer, mode types, player interaction patterns.

  For ZX IMPLEMENTATION (GGRS, determinism rules, viewport FFI): use zx-game-design:multiplayer-patterns instead.
version: 1.0.1
---

# Multiplayer Design

Frameworks for designing 1-4 player local and online multiplayer. Focused on controller-based gameplay with rollback netcode support.

## Context: Nethercore Multiplayer

Nethercore fantasy consoles provide:
- 1-4 player support
- Rollback netcode (GGRS) built-in
- Controller-based input
- Local and online play

This skill covers design—see platform-specific plugins for implementation.

---

## Multiplayer Modes

### Mode Selection

| Mode | Player Count | Relationship | Best For |
|------|--------------|--------------|----------|
| **Single-player** | 1 | Solo | Story, complex systems |
| **Local co-op** | 2-4 same device | Cooperative | Social, casual |
| **Online co-op** | 2-4 networked | Cooperative | Distance play |
| **Local versus** | 2-4 same device | Competitive | Party games |
| **Online versus** | 2-4 networked | Competitive | Ranked, serious |
| **Asymmetric** | 2+ mixed roles | Varies | Unique dynamics |

### Mode Checklist

- [ ] Which modes are supported?
- [ ] Can modes be mixed (online + local)?
- [ ] Is single-player always available?
- [ ] How does matchmaking work (if online)?

---

## Cooperative Design

### Co-op Pillars

1. **Shared goals:** Players work toward same objective
2. **Complementary roles:** Each player has value
3. **Coordination opportunities:** Teamwork beats solo play
4. **Shared stakes:** Victory and defeat together

### Co-op Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Same role** | All players identical | Twin-stick shooters |
| **Class-based** | Distinct but equal roles | Tank/healer/DPS |
| **Leader + support** | One primary, others assist | Adventure + helpers |
| **Asymmetric** | Completely different gameplay | One fights, one manages |

### Co-op Design Checklist

- [ ] Can one player complete objectives alone? (Should often be no)
- [ ] Is every player always engaged?
- [ ] Are skill disparities handled? (Carry vs dead weight)
- [ ] Does communication feel rewarding?
- [ ] Is friendly fire on/off/optional?

---

## Competitive Design

### Versus Pillars

1. **Fair start:** No inherent advantages
2. **Skill expression:** Better player usually wins
3. **Comeback potential:** Down but not out
4. **Quick resolution:** Games don't drag

### Competitive Modes

| Mode | Structure | Design Focus |
|------|-----------|--------------|
| **Deathmatch** | Kill to win | Combat balance |
| **Objective** | Capture/hold goals | Map control |
| **Race** | First to finish | Movement skill |
| **Survival** | Last standing | Resource management |
| **Score attack** | Highest points | Optimization |

### Competitive Balance

| Factor | Imbalanced | Balanced |
|--------|------------|----------|
| Start position | Some spots better | Equal or random |
| Character power | Tiers with gaps | All viable |
| Game knowledge | Secrets win games | Skill + knowledge |
| Randomness | Luck determines outcome | Skill dominates |

---

## Shared Screen Design

### Screen Sharing Options

| Option | Best For | Challenge |
|--------|----------|-----------|
| **Single shared screen** | Same-area gameplay | Camera management |
| **Split screen** | Independent exploration | Screen real estate |
| **Tethered players** | Co-op with limits | Tension design |

### Shared Camera Checklist

- [ ] All players visible (or clear reason why not)
- [ ] Camera doesn't fight players
- [ ] Important information visible to all
- [ ] Screen doesn't stretch too far

---

## Controller Sharing Patterns

### Same Device, Multiple Controllers

Standard local multiplayer:
- Each player has full controller
- Input mapping identical or per-player
- UI shows player 1, 2, 3, 4 colors

### Pass-and-Play

Sequential gameplay:
- One controller
- Players take turns
- Clear turn boundaries

### Asymmetric Input

Different input per player:
- Example: Player 1 controller, Player 2 keyboard
- Good for different roles
- Clear about who controls what

---

## Rollback-Friendly Design

### Why It Matters

Rollback netcode rewrites game state when inputs arrive late. Design for:
- **Determinism:** Same inputs = same result always
- **Small state:** Less data to rollback
- **Visual tolerance:** Small corrections aren't jarring

### Design Considerations

| Element | Rollback-Friendly | Avoid |
|---------|-------------------|-------|
| Randomness | Seeded, synced | External RNG |
| Timing | Frame-based | System clock |
| State size | Minimal necessary | Bloated game state |
| Visual effects | Non-gameplay affecting | Effects that cause desyncs |

See ZX-specific plugins for implementation details.

---

## Player Count Scaling

### Design for Range

| Players | Adjustments |
|---------|-------------|
| 1 | AI companions? Solo viable? |
| 2 | Core design target |
| 3 | Odd number handling |
| 4 | Maximum chaos balance |

### Scaling Patterns

| Element | How to Scale |
|---------|--------------|
| Enemy count | More enemies with more players |
| Boss HP | +50-100% per additional player |
| Resources | Per player, not per group |
| Difficulty | Dynamic based on player count |

---

## Quick Design Template

```
MULTIPLAYER DESIGN

Modes: [ ] Solo [ ] Local co-op [ ] Online co-op [ ] Local vs [ ] Online vs
Player count: _____ to _____
Screen sharing: [ ] Shared [ ] Split [ ] Tethered

CO-OP (if applicable):
Role structure: [ ] Same [ ] Class-based [ ] Asymmetric
Friendly fire: [ ] On [ ] Off [ ] Optional
Revive system: _______________

VERSUS (if applicable):
Win condition: _______________
Match length: _____ minutes
Balancing approach: _______________

NETWORK (if applicable):
Rollback-safe: [ ] Yes [ ] Needs review
Max latency tolerance: _____ ms
```

---

## Additional Resources

### Reference Files

- **`references/coop-patterns.md`** — Co-op design patterns
- **`references/competitive-patterns.md`** — Versus mode design
- **`references/controller-sharing.md`** — Input design for local play

### Related Skills

- **`game-balance`** — Competitive balance
- **`replayability-engineering`** — For competitive replayability
