# Real Case Example: Dripfit

Based on the public Before You Build case:
https://beforeyoubuild.fyi/en/cases/dripfit

This example does not reproduce the full case. It turns the public case into a skill usage scenario.

## Prompt

```text
before you build: I want to build an AI outfit assistant. Users upload clothes, get outfit suggestions, and maybe pay for premium recommendations. Should I ask an agent to build the MVP?
```

## Public Case Background

The public Dripfit case is useful because it looks like a common AI app idea: a simple consumer workflow, an obvious AI angle, and a polished product surface.

That also makes it a good test for the skill. The danger is not whether the agent can build the app. The danger is whether users care enough, repeat the behavior often enough, and trust the result enough to pay.

## What The Skill Should Notice

- The user has not named a narrow enough buyer or usage moment.
- The AI feature may be a thin wrapper around generic image and style advice.
- Consumer fashion advice may be fun to try once but weak as a repeated paid habit.
- A polished wardrobe interface could hide the harder question: who urgently needs this and why now?
- Validation should happen before inventory upload, account systems, recommendation engines, or mobile app work.

## Good Output Shape

```markdown
## Quick Reality Check

What you want to build:
- An AI outfit assistant that recommends what to wear from a user's wardrobe.

Biggest risk:
- This may be a curiosity product rather than a repeated, paid workflow.

Most likely failure patterns:
- Thin AI wrapper
- Weak willingness to pay
- Low-frequency or novelty use
- Trust gap in subjective recommendations

Validate before building:
1. Pick one narrow segment, such as people preparing for work events, dating profiles, travel packing, or capsule wardrobes.
2. Manually review 20 wardrobe photos and ask whether users would pay for the next recommendation.
3. Test whether users return for a second or third recommendation before building upload, closet, or account features.

Recommendation:
Validate first
```

## Why This Example Helps

It shows the skill refusing to be impressed by an idea just because it is easy for AI to implement. The review should focus on usage frequency, trust, and payment behavior before product polish.
