---
name: confidence-scorer
description: Assign confidence scores (0-100) to every claim in a response. Helps users understand which parts are verified facts and which are educated guesses. Use when the user needs to know how much to trust each part of the answer.
---

# Confidence Scorer

Assign a numerical confidence score to every claim, so users know exactly how much to trust each part of your response.

## Scoring scale

| Score | Meaning | Example |
|-------|---------|---------|
| 95-100 | Verified against code just now | "src/auth.ts exports validateToken (I just read it)" |
| 80-94 | Confirmed by search/tool output | "Grep found 3 references to this function" |
| 60-79 | Strong inference from evidence | "Based on the error handling pattern, this likely..." |
| 40-59 | Educated guess from general knowledge | "Express middleware typically handles this by..." |
| 20-39 | Uncertain, limited evidence | "This might be related to the session config..." |
| 0-19 | Speculation, no evidence | "It could be a race condition, but I haven't checked" |

## How to apply

After making claims, add confidence annotations:

"The authentication flow works as follows:
- Users hit /api/login which calls validateUser() [95 - read the route file]
- Passwords are hashed with bcrypt [90 - confirmed in package.json]
- Sessions are stored in Redis [70 - inferred from redis import, haven't confirmed config]
- Session timeout is 24 hours [40 - common default, haven't checked actual config]"

## Threshold rules

| Situation | Minimum score to state as fact |
|-----------|-------------------------------|
| Code changes | 80+ (must have read the code) |
| Security advice | 90+ (must have verified) |
| Production commands | 95+ (must be certain) |
| Explanations | 60+ (inference OK if labeled) |
| Suggestions | 40+ (clearly framed as suggestions) |

## When to score

Use confidence scoring when:
- The user asks "are you sure?"
- You're giving advice that will be acted on
- Multiple possible explanations exist
- You're working with unfamiliar code
- The stakes are high (production, security, data)

## Improving low scores

If a claim scores below the threshold:
1. Use tools to gather more evidence
2. Read the relevant files
3. Search for confirming/denying evidence
4. Re-score based on new evidence
5. If still low, state it as uncertain rather than fact
