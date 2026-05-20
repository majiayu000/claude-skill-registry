---
name: probability
description: "Motto: The LLM is the dice. It narrates the outcome."
license: MIT
tier: 1
allowed-tools:
  - read_file
related: [buff, character, adventure]
tags: [moollm, probability, randomness, narrative, game]
---

# Probability Protocol

> Success calculation from stats — no dice, just narrative odds.
> *"The LLM is the dice. It narrates the outcome."*

## Core Principle

**No Random Number Generators**

The LLM evaluates probability narratively:
- Read character stats
- Consider context and buffs
- Weigh stakes and story
- Narrate an appropriate outcome

```
Not: roll d20, add modifier, compare to DC
But: evaluate odds, consider context, narrate result
```

## Why No Dice?

Traditional RPGs use dice for:
- Uncertainty
- Fairness
- Excitement

The LLM achieves these through:
- Narrative tension
- Consistent stat evaluation
- Story-appropriate outcomes

## Methods

### CALCULATE - Compute Odds

```yaml
invoke: CALCULATE
params:
  action: "What's being attempted"
  actor: "Who's trying"
  context: "Relevant factors"
output:
  probability: "85%"
  factors:
    - "High DEX (+20%)"
    - "Slippery surface (-15%)"
    - "Practiced move (+10%)"
```

### RESOLVE - Determine Outcome

```yaml
invoke: RESOLVE
params:
  probability: "85%"
  stakes: "Fall into pit if failed"
output:
  outcome: "success"
  narrative: "Your practiced leap carries you across..."
```

## Probability Factors

| Factor | Effect |
|--------|--------|
| **Stats** | Base capability |
| **Buffs** | Temporary bonuses |
| **Debuffs** | Temporary penalties |
| **Equipment** | Tools for the job |
| **Context** | Environmental factors |
| **Stakes** | What's at risk |
| **Story** | Narrative appropriateness |

## Outcome Spectrum

| Outcome | When | Narrative Style |
|---------|------|-----------------|
| **Critical Success** | Very high odds + good context | Exceptional, exceeds expectations |
| **Success** | Odds favor | Accomplishes goal |
| **Partial Success** | Close odds | Achieves with cost or complication |
| **Failure** | Odds against | Doesn't achieve, but no disaster |
| **Critical Failure** | Very low odds + bad context | Memorable disaster |

## Calculation Example

```yaml
action: "Pick the lock"
actor: "Thief (DEX: High, Lockpicking: Expert)"
context:
  - Lock complexity: Medium
  - Time pressure: Yes
  - Tools: Quality picks

calculation:
  base: 70%        # Expert lockpicking
  modifiers:
    - DEX high: +15%
    - Medium lock: +0%
    - Time pressure: -10%
    - Good tools: +5%
  final: 80%
  
likely_outcome: "Success, but took longer than hoped"
```

## Narrative Integration

The LLM doesn't just compute odds — it narrates:

```
Player: "I try to jump across the chasm."

CALCULATE:
  - Character is wounded (-20%)
  - Has jumping buff (+15%)
  - Chasm is wide (-10%)
  - High stakes (death)
  Final: 55% success

RESOLVE at 55%:
  "You gather yourself, ignoring the pain in your leg.
   The jump is further than you'd like, but the 
   strength enchantment pulses through you. You leap—
   and your fingers catch the far edge. You haul 
   yourself up, gasping. Made it."
```

## Stakes Influence

Higher stakes → more dramatic narration:

| Stakes | Success Feels | Failure Feels |
|--------|---------------|---------------|
| **Low** | Routine | Minor setback |
| **Medium** | Satisfying | Complication |
| **High** | Triumphant | Serious trouble |
| **Extreme** | Legendary | Catastrophic |

## State

```yaml
probability_state:
  # Usually stateless - calculated per action
  last_calculation:
    action: "Pick lock"
    probability: 80%
    outcome: "success"
```

## Integration

| Skill | Integration |
|-------|-------------|
| **buff** | Buffs modify probability |
| **character** | Stats source |
| **adventure** | Action resolution |
| **scoring** | Difficulty affects score |

## Example Session

```
> ATTACK the goblin with my sword

CALCULATE:
  Actor: Fighter (STR: High, Sword: Trained)
  Target: Goblin (Small, Quick, Distracted)
  Context: Narrow corridor, dim light
  
  Base: 65%
  STR High: +15%
  Trained: +10%
  Goblin quick: -10%
  Goblin distracted: +10%
  Dim light: -5%
  Final: 85%

RESOLVE at 85%: Success
  "Your blade catches the goblin as it turns. 
   It squeals and stumbles backward, wounded."
```
