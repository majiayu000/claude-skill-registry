---
name: challenge
description: Presents adaptive codebase challenge questions with multiple-choice and trace exercises. Use when testing contributor knowledge of the codebase.
model_hint: standard
---

# Run Gauntlet Challenge

Present challenges from the knowledge base and evaluate answers.

## In-Loop Provider Setup

Before generating a challenge, register the in-loop variation
provider so we do not call out to the Anthropic API just to spawn
a sibling Claude (issue #464). Outside Claude Code this is a
no-op and the default Anthropic provider remains active.

```python
from gauntlet.providers.in_loop import (
    register_in_loop_provider_if_inside_claude_code,
)
register_in_loop_provider_if_inside_claude_code()
```

## Steps

1. **Load state**: read `.gauntlet/knowledge.json` and developer
   progress

2. **Check for pending challenge**: if
   `.gauntlet/state/pending_challenge.json` exists, evaluate the
   developer's most recent message as an answer before generating
   a new one

3. **Generate challenge**: use adaptive weighting to select a
   knowledge entry and challenge type

4. **Present challenge**: show the question with context

5. **Evaluate answer**: score the response (pass/partial/fail)

6. **Record result**: update developer progress and streak

7. **On pass**: write pass token if from pre-commit gate. Show
   next challenge if in session.

8. **On fail**: show correct answer with explanation. Present a
   new challenge.

## Scoring

| Result | Score | Streak |
|--------|-------|--------|
| Pass | 1.0 | +1 |
| Partial | 0.5 | reset |
| Fail | 0.0 | reset |
