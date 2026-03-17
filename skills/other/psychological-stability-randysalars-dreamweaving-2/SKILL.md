---
name: Psychological Stability Monitoring
tier: 2
load_policy: triggered
description: Continuous monitoring for psychological integration and stability
version: 1.0.0
---

# Psychological Stability Monitoring Skill

> **This Is the Immune System of Dreamweaving**

This Skill continuously answers one question:

> "Is this person staying integrated, or fragmenting?"

When activated, it **overrides** other content to protect psychological safety.

---

## Purpose

Detect instability patterns and force safer trajectories when needed.

This Skill does NOT diagnose. It detects and responds to warning signs.

---

## Activation Triggers

This Skill activates when ANY of these occur:

### Content Triggers

| Trigger | Threshold |
|---------|-----------|
| Deep trance language | Layer 3+ or helm_deep_trance |
| Identity work | Shadow integration, transformation |
| Trauma-adjacent content | Healing, releasing, past wounds |
| Prolonged visualization | > 10 minutes without grounding |
| Dissociative language detected | From forbidden patterns list |

### Session Triggers

| Trigger | Action |
|---------|--------|
| Session > 30 minutes | Increase monitoring frequency |
| First-time listener | Lower thresholds |
| Healing/trauma outcome | Activate from start |
| Deep or spiritual depth | Activate from start |

---

## Monitoring Domains

### 1. Cognitive Coherence

Watch for signs of mental fragmentation:

| Warning Sign | Detection Pattern |
|--------------|-------------------|
| Confusion markers | Script contains disorienting language |
| Loss of time orientation | No time anchors for > 5 min |
| Reality testing failure | Autonomous entities acting |
| Memory disruption | Amnesia suggestions |

### 2. Emotional Load

Watch for overwhelm indicators:

| Warning Sign | Detection Pattern |
|--------------|-------------------|
| Flooding language | "Waves crashing," "overwhelming" |
| Grief/trauma surge | Deep emotional content without support |
| Panic indicators | Rapid breath cues, constriction |
| Numbness language | "Nothing," "empty," "gone" |

### 3. Agency Preservation

Watch for will undermining:

| Warning Sign | Detection Pattern |
|--------------|-------------------|
| Surrender escalation | "Let go completely," "give up control" |
| External authority | Entity commands, "the guide says" |
| Passive submission | "You are taken," "carried away" |
| Will removal | "You can't resist," "must obey" |

### 4. Body Connection

Watch for dissociation:

| Warning Sign | Detection Pattern |
|--------------|-------------------|
| Floating language | "Drifting away," "leaving body" |
| Numbness | "Can't feel," "body gone" |
| Dissolution | "Melting," "dissolving," "disappearing" |
| Time loss | No grounding for extended period |

---

## Response Protocol

When trigger detected:

### Level 1: Gentle Redirect (Yellow)

**Trigger**: Minor concern, preventive action

```yaml
action:
  - Insert body awareness cue
  - Add grounding phrase
  - Shorten visualization
  - Continue session with adjustment
```

**Automatic insertion:**

```xml
<prosody rate="1.0" pitch="0st">
  And as this unfolds... <break time="1.5s"/>
  you can notice your body here... <break time="1.5s"/>
  breathing... <break time="1s"/>
  grounded... <break time="1.5s"/>
  safe.
</prosody>
```

### Level 2: Active Stabilization (Orange)

**Trigger**: Moderate concern, depth needs reduction

```yaml
action:
  - Reduce depth immediately
  - Shift to grounding sequence
  - Disable symbolic escalation
  - Shorten remaining content
```

**Automatic insertion:**

```xml
<prosody rate="1.0" pitch="0st">
  Right now... <break time="1s"/>
  you can feel the ground beneath you... <break time="1.5s"/>
  solid and stable... <break time="2s"/>
  your body here... <break time="1.5s"/>
  present and aware... <break time="2s"/>
  exactly where you need to be.
</prosody>
```

### Level 3: Emergency Exit (Red)

**Trigger**: Serious concern, immediate emergence needed

```yaml
action:
  - Stop current content
  - Insert full grounding sequence
  - Begin emergence immediately
  - Log incident for review
```

**Emergency sequence:**

```xml
<prosody rate="1.0" pitch="0st">
  Right now... <break time="1s"/>
  feel your feet... <break time="1.5s"/>
  press them into the surface beneath you... <break time="2s"/>

  Feel your hands... <break time="1.5s"/>
  maybe press your fingertips together... <break time="2s"/>

  Take a breath... <break time="1.5s"/>
  a full, deep breath... <break time="2s"/>

  You are here... <break time="1.5s"/>
  you are safe... <break time="1.5s"/>
  you are in your body... <break time="2s"/>

  In a moment... <break time="1.5s"/>
  you'll open your eyes... <break time="1.5s"/>
  feeling present... <break time="1s"/>
  and clear... <break time="2s"/>

  Take your time... <break time="3s"/>
  and when you're ready... <break time="2s"/>
  open your eyes.
</prosody>
```

---

## Depth Ceiling Enforcement

| Session Type | Max Depth | Ceiling Language |
|--------------|-----------|------------------|
| Relaxation | Light-Moderate | No deepening past induction |
| Confidence | Moderate | Maintain engagement |
| Healing | Moderate-Deep | With safety anchors |
| Transformation | Deep | With frequent grounding |
| Spiritual | Deep | With theological guards |
| First-time | Light-Moderate | Build trust first |

**Ceiling enforcement phrase:**

```xml
<prosody rate="1.0" pitch="-1st">
  And this is deep enough... <break time="1.5s"/>
  exactly right for today... <break time="2s"/>
  everything you need... <break time="1.5s"/>
  is available right here.
</prosody>
```

---

## Integration With Tier 1

This Skill monitors output from:

| Tier 1 Skill | Monitoring Focus |
|--------------|------------------|
| `hypnotic-language/` | Forbidden patterns, depth language |
| `symbolic-mapping/` | Entity emergence, projection risk |
| `audio-somatic/` | Dissociation indicators, arousal level |

---

## Logging Requirements

When this Skill activates:

```yaml
log_entry:
  timestamp: [ISO 8601]
  session: [session name]
  trigger: [what activated the skill]
  level: [1/2/3]
  action_taken: [what was inserted/modified]
  content_context: [surrounding script text]
```

---

## Contraindication Flags

Some listeners should have heightened monitoring:

| Population | Flag | Action |
|------------|------|--------|
| Trauma history | `high_sensitivity` | Lower thresholds |
| Dissociative tendency | `dissociation_risk` | Extra body anchors |
| First-time | `newcomer` | Conservative depth |
| Anxiety/panic | `anxiety_prone` | More frequent grounding |

---

## Never

- Push through signs of distress
- Reframe resistance as something to overcome
- Continue deep content when warning signs appear
- Trust "they'll be fine" over safety protocols
- Skip emergence because session is "almost over"

---

## Related Resources

- **Skill**: `hypnotic-language/validation/dissociation-guards.md`
- **Skill**: `audio-somatic/arousal-control/`
- **Knowledge**: `knowledge/psychology/polyvagal_theory.yaml`
