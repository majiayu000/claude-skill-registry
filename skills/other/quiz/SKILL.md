---
name: quiz
description: Generates multiple choice quiz questions based on current conversation context. Use when testing understanding, reviewing what was discussed, or wanting a knowledge check on the session.
allowed-tools: Bash(date *), Read, Write
---

# Conversation Quiz

Generate multiple choice questions testing understanding of the current conversation.

## Instructions

1. Analyze the conversation context for quizzable content:
   - Technical concepts discussed
   - Decisions made
   - Code patterns or implementations
   - Key facts or configurations

2. Generate 3-10 questions with 4 options each (default 5, or as many as the user/arguments request)

3. **Question Quality Guidelines**
   - Questions should test understanding, not memorization of exact wording
   - Include plausible distractors (wrong answers that could seem right)
   - Vary difficulty: mix straightforward recall with deeper comprehension
   - Descriptions should explain WHY the option is correct/incorrect (shown only after answering)
   - If conversation lacks substance for 3 questions, generate what's reasonable and note the limitation

4. **Write questions to file and launch external quiz runner**:
   - Generate a unix timestamp: `date +%s` via Bash
   - Write questions JSON to `/tmp/quiz_questions_$TIMESTAMP.json` using the format below
   - Tell the user to run in a separate terminal: `python3 ~/.claude/skills/quiz/quiz.py /tmp/quiz_questions_$TIMESTAMP.json`
   - The quiz runner writes results to `/tmp/quiz_results_$TIMESTAMP.json` (same timestamp, auto-derived from questions filename)
   - Wait for user to report back that they finished
   - Read results from `/tmp/quiz_results_$TIMESTAMP.json`
   - Provide feedback: celebrate correct answers, explain wrong ones with the description from the correct option

## Questions JSON Format

```json
[
  {
    "question": "What network mode allows containers to share the host's network namespace?",
    "options": [
      {"label": "bridge", "correct": false, "description": "Bridge creates an isolated network — containers get their own namespace"},
      {"label": "host", "correct": true, "description": "Host mode removes network isolation — container shares the host's network stack"},
      {"label": "overlay", "correct": false, "description": "Overlay enables multi-host networking, but still uses separate namespaces"},
      {"label": "macvlan", "correct": false, "description": "Macvlan assigns a MAC address to the container — separate namespace with direct network access"}
    ]
  }
]
```

## Important

- Each question MUST have exactly ONE option with `"correct": true`
- The `description` field is NOT shown during the quiz — only used for post-quiz feedback
- Options are shuffled automatically by the quiz runner — no need to randomize in the JSON
- The quiz runner handles: display, input, timing, scoring, and writes results to file
