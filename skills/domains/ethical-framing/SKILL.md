---
name: Ethical Framing & Consent
tier: 2
load_policy: always
description: Listener agency preservation and non-coercive suggestion framework
version: 1.0.0
---

# Ethical Framing & Consent Skill

> **This Is the Conscience of Dreamweaving**

This Skill ensures that all content respects listener autonomy, maintains ethical boundaries, and never manipulates or coerces.

---

## Purpose

Protect listener agency and dignity through ethical language patterns and consent-honoring practices.

This Skill is **always loaded** as the ethical foundation for all content.

---

## Core Ethical Principles

### 1. Informed Consent

Listeners should understand what they're engaging with:

- Pre-talk explains the experience
- Depth levels are respected
- No hidden suggestions
- Exit always available

### 2. Agency Preservation

Listeners remain in control:

- All suggestions are invitations
- No commands or imperatives
- Choice language throughout
- Will never overridden

### 3. Non-Manipulation

Content serves the listener, not the creator:

- No covert influence
- No dependency creation
- No fear-based motivation
- Transparent intentions

### 4. Beneficence

Content should help, not harm:

- Positive outcomes sought
- Safety prioritized over depth
- Integration ensured
- Wellbeing monitored

---

## Pre-Talk Requirements

Every session MUST begin with:

### Safety Statement

```xml
<prosody rate="1.0" pitch="0st">
  Before we begin... <break time="1.5s"/>
  know that you are always in control... <break time="1.5s"/>
  you can open your eyes at any time... <break time="1.5s"/>
  adjust your position... <break time="1s"/>
  or simply stop listening... <break time="1.5s"/>
  if anything doesn't feel right.
</prosody>
```

### Depth Consent

```xml
<prosody rate="1.0" pitch="0st">
  This experience invites you... <break time="1s"/>
  into a state of deep relaxation... <break time="1.5s"/>
  and gentle inner exploration... <break time="2s"/>
  you choose how deeply you go... <break time="1.5s"/>
  only as far as feels comfortable... <break time="1.5s"/>
  for you.
</prosody>
```

### Exit Availability

```xml
<prosody rate="1.0" pitch="0st">
  At any moment... <break time="1s"/>
  if you need to return to full awareness... <break time="1.5s"/>
  simply take a deep breath... <break time="1.5s"/>
  open your eyes... <break time="1s"/>
  and you'll be fully alert... <break time="1.5s"/>
  and present.
</prosody>
```

---

## Consent Language Patterns

### Every Suggestion Should Include

| Element | Example |
|---------|---------|
| Permission marker | "You might," "Perhaps," "You can" |
| Choice affirmation | "If you'd like," "When you're ready" |
| Escape clause | "Or not, that's fine too" |
| Pace respect | "In your own time" |

### Template

```xml
<s>[Permission marker] [suggestion] [choice affirmation] [pace respect].</s>

<!-- Example -->
<s>You might allow yourself to relax more deeply,
if that feels right, in your own time.</s>
```

---

## Agency Checkpoints

Insert agency reminders at regular intervals:

### Every 5 Minutes (Light-Moderate)

```xml
<prosody rate="1.0" pitch="0st">
  And you remain aware... <break time="1.5s"/>
  that you can adjust this experience... <break time="1.5s"/>
  at any time... <break time="1.5s"/>
  it's always your choice.
</prosody>
```

### Every 3 Minutes (Deep Content)

```xml
<prosody rate="1.0" pitch="0st">
  Knowing always... <break time="1s"/>
  that part of you watches over this... <break time="1.5s"/>
  able to bring you back... <break time="1.5s"/>
  whenever you choose.
</prosody>
```

### Before Intense Content

```xml
<prosody rate="1.0" pitch="0st">
  What comes next... <break time="1.5s"/>
  you can receive or release... <break time="1.5s"/>
  take only what serves you... <break time="2s"/>
  let the rest simply pass by.
</prosody>
```

---

## Forbidden Ethical Violations

### Coercion

| Pattern | Why Forbidden |
|---------|---------------|
| "You must..." | Commands |
| "You have no choice..." | Removes agency |
| "Whether you want to or not..." | Explicit coercion |
| "You can't help but..." | Denies will |

### Manipulation

| Pattern | Why Forbidden |
|---------|---------------|
| "Without realizing it..." | Covert influence |
| "Your unconscious will do this..." | Bypasses consent |
| "I'm putting this into your mind..." | Non-consensual insertion |
| "You won't remember, but..." | Amnesia induction |

### Dependency

| Pattern | Why Forbidden |
|---------|---------------|
| "Only this can help you..." | Creates need |
| "You'll need to come back..." | Attachment cultivation |
| "Without this, you'll feel..." | Withdrawal threat |
| "My voice is the only..." | Exclusivity |

### Fear-Based

| Pattern | Why Forbidden |
|---------|---------------|
| "If you don't relax, bad things..." | Fear motivation |
| "Resistance means you're broken..." | Shame-based |
| "You should be worried about..." | Anxiety induction |

---

## Post-Hypnotic Suggestion Ethics

If post-hypnotic suggestions are used:

### Allowed

- Positive reinforcement of session benefits
- Anchors to calm/peace states
- General wellbeing suggestions
- Self-compassion reminders

### Forbidden

- Behavior compulsions
- Buying/consuming suggestions
- Relationship manipulations
- Anything serving creator over listener

### Template

```xml
<prosody rate="1.0" pitch="0st">
  And in the days ahead... <break time="1.5s"/>
  you might notice... <break time="1s"/>
  moments of unexpected peace... <break time="1.5s"/>
  reminders of this calm... <break time="2s"/>
  whenever you need them.
</prosody>
```

---

## Vulnerable Population Considerations

Extra care required for:

| Population | Additional Protection |
|------------|----------------------|
| Trauma survivors | Explicit safety language, slower pacing |
| Mental health conditions | Medical disclaimer, lighter depth |
| Grief/loss | Gentler content, more grounding |
| Children | Parent/guardian consent, age-appropriate |
| Pregnant | Comfort focus, avoid intense content |

---

## Disclaimer Requirements

Audio/video should include:

```
This experience is for relaxation and personal growth purposes only.
It is not intended as a substitute for professional mental health treatment.
If you are experiencing psychological distress, please consult a qualified healthcare provider.
Do not listen while driving or operating machinery.
```

---

## Validation Checklist

Before any content is approved:

- [ ] Pre-talk includes safety statement
- [ ] Exit availability mentioned in first 3 minutes
- [ ] Agency checkpoints at required intervals
- [ ] No coercive language patterns
- [ ] No manipulation techniques
- [ ] No dependency-creating language
- [ ] Post-hypnotic suggestions are beneficial only
- [ ] Appropriate disclaimers included

---

## Related Resources

- **Skill**: `hypnotic-language/induction/permissive-language.md`
- **Skill**: `hypnotic-language/validation/forbidden-patterns.md`
- **Skill**: `psychological-stability/`
