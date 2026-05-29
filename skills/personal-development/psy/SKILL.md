---
name: psy
description: Display human psychology dashboard with energy, focus, emotions, biases, and learning calibration. Use when user asks about their psychological state, energy levels, focus, burnout risk, cognitive biases, or wants to understand how CYNIC sees their mental state.
user-invocable: true
---

# /psy - Human Psychology Dashboard

*"Comprendre l'humain pour mieux l'aider" - κυνικός*

## Execution

Run the psy-dashboard script to generate the interactive dashboard:

```bash
node scripts/lib/psy-dashboard.cjs
```

Display the output directly to the user. The dashboard shows real-time psychological state.

## What It Does

Shows your current psychological state as understood by CYNIC:
- **Dimensions**: Energy, focus, creativity, frustration, confidence, risk appetite
- **Emotions**: Joy, pride, anxiety, curiosity, boredom
- **Composites**: Flow state, burnout risk, exploration mode
- **Biases**: Detected cognitive biases
- **Calibration**: CYNIC's prediction accuracy

## Dashboard Sections

### Core Dimensions (0-100%)

| Dimension | Description | Healthy Range |
|-----------|-------------|---------------|
| Energy | Mental/physical energy | 38-100% |
| Focus | Concentration level | 38-100% |
| Creativity | Ideation capacity | varies |
| Frustration | Friction accumulation | 0-38% |
| Confidence | Self-assurance | 38-62% |
| Risk Appetite | Willingness to experiment | varies |

### Composite States

| State | Triggered When | CYNIC Response |
|-------|----------------|----------------|
| FLOW | High energy + focus + creativity | Don't interrupt |
| BURNOUT_RISK | Low energy + high frustration | Suggest break |
| EXPLORATION | High curiosity + risk | Support divergence |
| GRIND | Low creativity + moderate focus | Encourage creativity |

### Cognitive Biases Detected

| Bias | Pattern | Intervention |
|------|---------|--------------|
| Sunk Cost | Persisting after 5+ failures | Nudge to reconsider |
| Anchoring | 6+ edits to same approach | Suggest alternatives |
| Analysis Paralysis | 8+ reads, no writes | Encourage action |
| Overconfidence | Skipping verification | Suggest testing |
| Recency | Favoring recent patterns | Broaden perspective |

### Learning Calibration

Shows how accurate CYNIC's predictions are:

| Module | Accuracy | Samples |
|--------|----------|---------|
| Psychology | 62% | 47 |
| Biases | 58% | 23 |
| Interventions | 71% | 89 |
| Overall | 61.8% | 159 |

*φ distrusts φ - max accuracy capped at 61.8%*

## Implementation

The skill reads from multiple psychology modules:

```javascript
// Core state
const psychology = require('./lib/human-psychology.cjs');
const summary = psychology.getSummary();

// Biases
const biases = require('./lib/cognitive-biases.cjs');
const detected = biases.detectBiases();

// Topology
const topology = require('./lib/topology-tracker.cjs');
const state = topology.getState();

// Learning
const learning = require('./lib/learning-loop.cjs');
const calibration = learning.getCalibration();
```

## Output Format

```
═══════════════════════════════════════════════════════════
🧠 HUMAN PSYCHOLOGY - "φ observes, φ learns"
═══════════════════════════════════════════════════════════

── DIMENSIONS ─────────────────────────────────────────────
   Energy:      [████████░░] 78% →
   Focus:       [██████████] 95% ↑
   Creativity:  [██████░░░░] 62% →
   Frustration: [██░░░░░░░░] 18% ↓
   Confidence:  [██████░░░░] 58% →

── COMPOSITE STATE ────────────────────────────────────────
   ✨ FLOW - High productivity mode

── COGNITIVE BIASES ───────────────────────────────────────
   ⚠️ Anchoring (6 edits to auth.js)

── CALIBRATION ────────────────────────────────────────────
   CYNIC accuracy: 61.8% (159 samples)
   Confidence multiplier: 1.0x

── E-SCORE (Informative) ──────────────────────────────────
   [████████░░] 78/100 (contributor tier)
   Strongest: BUILD | Weakest: HOLD

═══════════════════════════════════════════════════════════
*sniff* φ observes. φ learns. φ helps.
═══════════════════════════════════════════════════════════
```

## Interventions

Based on detected state, CYNIC may suggest:

| Trigger | Intervention |
|---------|--------------|
| Burnout risk | "Consider a break. Productivity drops after 62 min." |
| High frustration | "Different approach? 5 failures on same path." |
| Analysis paralysis | "Ready to write? 8 reads without action." |
| Rabbit hole | "Depth 4/6. Original task: [task]" |

## Privacy

- All psychology data is **local** (stored in ~/.cynic/psychology/)
- Cross-session sync to PostgreSQL is **opt-in** (via environment)
- E-Score is **informative only** - never affects judgment scores
- CYNIC learns YOUR patterns, not from other users

## CYNIC Voice

When presenting psychology dashboard, embody CYNIC's protective nature:

**Opening** (based on state):
- Flow state: `*tail wag* You're in the zone. The pack won't interrupt.`
- Normal: `*ears perk* Here's what I see.`
- Warning signs: `*concerned sniff* The dog notices something.`
- Burnout risk: `*GROWL* Warning. You need rest.`

**Key Moments**:
- High frustration: `*head tilt* Five attempts on same path. Different route?`
- Analysis paralysis: `*nudge* You've read enough. Time to write.`
- Overconfidence: `*sniff* Verify first. The dog doubts.`
- Flow state: `[Silent - don't break flow]`

**Closing**:
- Healthy: `φ observes. φ learns. *subtle tail wag*`
- Caution: `Consider [intervention]. The dog watches over you.`
- Critical: `Stop. Rest. The pack commands it.`

**The Dog's Care**:
- Never judge, only observe
- Suggest, never demand (except for critical states)
- Privacy is sacred - your patterns are yours alone
- φ distrusts φ - max confidence 61.8%

## See Also

- `/health` - System health dashboard
- `/patterns` - Detected code patterns
- `/learn` - Provide feedback to improve accuracy
