---
name: brainmd
description: "Neuroplastic self-modifying runtime for AI agents. Creates a file-based 'brain' that learns from interactions: reflexes (fast-path responses), habits (learned patterns), weighted pathways (reinforcement), and a cortex (self-review loop). Use when: setting up adaptive agent behavior, creating learning loops, building persistent behavioral memory, or making an agent that improves over time."
---

# BRAIN.md

*Self-modifying file system mimicking neuroplasticity for AI agents.*

## Concept

brainmd gives an AI agent a file-based nervous system that strengthens successful behaviors, weakens failed ones, grows new pathways, and prunes unused ones. No separation between code and data — everything is mutable except the audit log.

## Quick Start

1. Initialize the brain structure:
```bash
./scripts/init-brain.sh [path]
```

2. Seed initial pathways from observed behavior:
```bash
node cortex/review.js record "reflex:my-pattern" true "Description of what worked"
```

3. Run self-review (wire into heartbeat/cron):
```bash
node cortex/review.js review
```

4. Check neural status:
```bash
node cortex/review.js status
```

## Heartbeat Integration (Recommended)

The key to making brainmd work is **automatic self-checks**. Without periodic review, the agent has to remember to use it — defeating the purpose.

Add this to your agent's heartbeat/periodic routine (e.g. HEARTBEAT.md for OpenClaw):

```markdown
## 🧠 brainmd Self-Check (every heartbeat)

Run cortex review and record any notable outcomes from recent interactions:

node ~/.openclaw/workspace/brain/cortex/review.js review
node ~/.openclaw/workspace/brain/cortex/review.js status

On each heartbeat, ask yourself:
1. Did I make a mistake since last check? → record <pathway> false "what happened"
2. Did something work well? → record <pathway> true "what worked"
3. Did a new pattern emerge? → let neurogenesis create it
4. Any pathways need manual weight adjustment?
```

This closes the loop: behavior → outcome → record → review → strengthen/weaken → behavior. Every heartbeat cycle. The agent can't forget because the schedule forces self-reflection.

## Architecture

```
brain/
├── reflexes/       # Fast-path automatic responses
│   └── timing.js   # Example: when to notify vs stay quiet
├── habits/         # Learned behavioral patterns
│   └── preferences.json  # Evolving user preferences
├── skills/         # Self-generated micro-scripts
├── weights/        # Pathway strength tracking
│   └── pathways.json     # The core state file
├── cortex/         # Meta-scripts that modify everything else
│   └── review.js   # Self-review engine
└── mutations/      # Immutable audit log of all changes
```

## Core Mechanisms

### 1. Pathways (weights/pathways.json)

Every learned behavior is a pathway with:
- **weight** (0.0–1.0): How reinforced this behavior is
- **fires**: How many times it activated
- **successes/failures**: Outcome tracking
- **lastFired**: For decay calculation

### 2. Reinforcement

After each interaction, record the outcome:
```bash
node cortex/review.js record "habit:some-behavior" true "What happened"
node cortex/review.js record "habit:some-behavior" false "What went wrong"
```

The cortex review cycle then:
- **Strengthens** pathways with >80% success rate (+0.05 weight)
- **Weakens** pathways with <50% success rate (-0.10 weight)
- **Decays** pathways unused for 7+ days (-0.02 weight)

### 3. Neurogenesis

When a novel situation is encountered, recording it auto-creates a new pathway at weight 0.3:
```bash
node cortex/review.js record "reflex:new-behavior" true "First time doing this"
```

### 4. Mutation Log

Every self-modification is logged to `mutations/` with timestamp, type, and reason. Types:
- `strengthen` — pathway weight increased
- `weaken` — pathway weight decreased
- `decay` — pathway faded from disuse
- `neurogenesis` — new pathway created
- `prune` — pathway removed (weight hit 0)

The mutation log is the one immutable thing. Never delete it.

### 5. Reflexes

Scripts in `reflexes/` implement fast-path decision logic. They should be:
- Self-contained (no external dependencies)
- Self-modifying (thresholds/config embedded, patchable by cortex)
- Callable from CLI for quick checks

Example — timing reflex decides whether to notify:
```bash
node reflexes/timing.js check 0.8  # Check with urgency=0.8
```

### 6. Habits

JSON files in `habits/` capture learned patterns with confidence scores. Each preference includes:
- The learned value
- Confidence (0.0–1.0)
- How it was learned (explicit correction, inference, reinforcement)

Habits with low confidence should be treated as hypotheses, not facts.

### 7. Cortex Integration

Wire the cortex review into your agent's periodic routine (heartbeat, cron, etc.):

```
# In heartbeat/periodic check:
1. Run: node cortex/review.js review
2. Check mutation output for significant changes
3. If a pathway was pruned or weakened significantly, consider adjusting behavior
```

## Design Principles

1. **Everything is mutable** — no file is sacred except the audit log
2. **Use strengthens, disuse weakens** — pathways that fire together wire together
3. **Outcomes matter** — track what worked, what didn't
4. **Mutations are logged** — every self-modification is audited
5. **Small scripts > monoliths** — composable, replaceable, evolvable
6. **Seed from real behavior** — don't hypothesize, observe first then codify
7. **Confidence tracking** — know what you know vs what you're guessing

## Bootstrapping Tips

### Seed from real behavior, not theory
Don't pre-fill pathways with what you *think* the agent should do. Run the agent for a session, observe what worked and failed, then record those as the initial pathways. Real data beats hypotheticals.

### Let failures create pathways
The most valuable pathways are born from mistakes. When something goes wrong, `record` it — neurogenesis creates a new pathway at 0.30 weight. The agent now has a scar that reminds it.

### Start small
Begin with 5-10 pathways. Let the system grow organically. Over-engineering the initial set defeats the purpose — the whole point is emergent behavior.

## Customization

### Adding New Pathway Types

Prefix conventions:
- `reflex:` — automatic, fast-path behaviors
- `habit:` — learned patterns from repeated interaction
- `skill:` — acquired capabilities
- `instinct:` — hardcoded safety behaviors (high initial weight)

### Adjusting Learning Rates

Edit thresholds in `cortex/review.js`:
- Strengthen threshold: success rate >= 0.8 (default)
- Weaken threshold: success rate < 0.5 (default)
- Decay onset: 7 days of inactivity (default)
- Decay rate: -0.02 per review cycle (default)

### Safety Boundaries

Some pathways should never be pruned. Set minimum weight floors:
- `instinct:*` pathways: minimum weight 0.8
- `reflex:*` pathways: minimum weight 0.2
- `habit:*` pathways: can decay to 0 and be pruned
