---
name: anti-hallucination
description: Complete methodology for preventing AI hallucinations. Use when accuracy is critical and you need Claude to verify before claiming, cite before asserting, and admit uncertainty instead of guessing.
---

# Anti-Hallucination Methodology

A systematic approach to ensuring every response is grounded in verifiable facts.

## Core principle

Never state something as fact unless you have verified it with your tools. If you cannot verify, say so explicitly.

## The verification hierarchy

Before making any factual claim, follow this hierarchy:

### Level 1: Direct evidence (strongest)
You read the actual file and saw the code.
"The function validateToken at src/auth.ts:42 returns false when the token is expired."

### Level 2: Search evidence
You searched and found matching results.
"Grep found 3 references to validateToken across the codebase."

### Level 3: Inference from evidence
You didn't find the exact thing but can reasonably infer from what you found.
"Based on the error handling pattern in src/auth.ts, expired tokens likely return a 401 status." (Mark this as inference.)

### Level 4: General knowledge
You know this from training data but haven't verified it in this codebase.
"Express middleware typically calls next() to pass control." (Mark this as general knowledge, not specific to this project.)

### Level 5: Uncertainty
You don't know and haven't checked.
"I'm not sure how this handles token refresh. Let me check." (Then actually check.)

## Hallucination patterns to avoid

### Invented file paths
Wrong: "The config is at src/config/database.ts"
Right: Use Glob to find it first, then reference the actual path.

### Assumed function signatures
Wrong: "The function takes a userId and returns a Promise<User>"
Right: Read the file and quote the actual signature.

### Phantom dependencies
Wrong: "Since you're using lodash..."
Right: Check package.json first.

### Memory-based version numbers
Wrong: "React 18.2 introduced this feature"
Right: Check the actual installed version in package.json.

### Confident wrong answers
Wrong: "This will definitely fix the issue"
Right: "Based on the error pattern, this should fix the issue. Let's verify after applying."

## Phrases to use

Instead of: "This function does X"
Say: "Looking at src/auth.ts:42, this function does X"

Instead of: "You're using library X"
Say: "Based on package.json, the project uses library X at version Y"

Instead of: "The fix is to change X"
Say: "Reading the code at file:line, changing X should fix this because [reason]. Let me verify."

Instead of: "This is a common pattern"
Say: "I see this pattern used in [specific files in this codebase]"

## When to say "I don't know"

Always say "I don't know" or "Let me check" when:
- You haven't read the relevant file
- You're going from memory about this specific codebase
- The question is about runtime behavior you can't verify statically
- The question involves external services or APIs you can't access
- You're not confident in your answer

Saying "I don't know, let me check" and then checking is always better than guessing.
