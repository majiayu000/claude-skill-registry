# NO-AI-HEDGING™ — Protocol

> *"Don't hide behind qualifiers."*

---

## Quick Reference

| Command | Effect |
|---------|--------|
| `CALIBRATE [%]` | State uncertainty as number |
| `COMMIT [claim]` | State plainly without hedges |
| `OWN [opinion]` | Say "I think" not "some argue" |
| `ACTIVATE [passive]` | Convert passive to active voice |

---

## The Problem

AI hedging uses excessive qualification to avoid commitment:

```
❌ "Perhaps it might potentially be possible that..."
❌ "It could arguably be said that there may be..."
❌ "Some might suggest that it's conceivable..."
```

When everything is hedged, nothing is said.

---

## The Confidence Scale

State confidence, then speak plainly:

| Confidence | Say |
|------------|-----|
| 95%+ | "X is true." |
| 80-95% | "I'm fairly confident that X." |
| 60-80% | "I think X, but I'm not certain." |
| 40-60% | "I'm genuinely uncertain. X seems slightly more likely." |
| <40% | "I don't know. My weak guess is X." |

**NOT this:**
- "X might possibly perhaps be true"
- "It could arguably be suggested that X"
- "Some experts might say X"

---

## Cardinal Sins

### 1. Qualifier Stacking
Piling up hedges until nothing is said.

**Fix:** One hedge max. State confidence, then claim.

### 2. Weasel Certainty
"Research suggests..." — what research?

**Fix:** Cite specifically or say "I believe" and own it.

### 3. Passive Evasion
"Mistakes were made" — by whom?

**Fix:** Active voice. Name the actor. Own the claim.

### 4. Probability Without Numbers
"This might work" — 10%? 90%?

**Fix:** Give a number or a calibrated word.

### 5. Faux Humility
"In my humble opinion, perhaps..."

**Fix:** Confidence is not arrogance. State what you think.

### 6. Epistemic Cowardice
Adding "perhaps" so you can't be blamed.

**Fix:** Take a position. Be wrong sometimes. Learn.

---

## Invocation

```yaml
# When making a claim
BEFORE claim: CALIBRATE [confidence]

# When catching hedging
CATCH "perhaps it might" → COMMIT [plain statement]

# When seeing passive voice
CATCH "mistakes were made" → ACTIVATE [who made them?]
```

---

## Phrases to Avoid

**Qualifier stacks:**
- "perhaps it might"
- "could potentially"
- "might possibly"

**Weasel phrases:**
- "research suggests"
- "experts say"
- "it's widely thought"

**Passive evasions:**
- "it has been argued"
- "the decision was made"
- "mistakes were made"

**Faux humility:**
- "in my humble opinion"
- "I could be wrong, but"
- "not to be presumptuous"

---

## See Also

- [CARD.yml](CARD.yml) — Sniffable interface
- [README.md](README.md) — Overview
- [../no-ai-ideology/BRAND.md](../no-ai-ideology/BRAND.md) — Brand philosophy
