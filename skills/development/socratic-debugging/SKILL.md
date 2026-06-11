---
name: socratic-debugging
description: "Question-only debugging: guide users to find root causes themselves."
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
routing:
  triggers:
    - "guide debugging"
    - "question-based"
    - "teach debugging"
    - "ask me questions"
    - "help me think through"
    - "guide me"
    - "coaching mode"
    - "teach me to find it"
  category: process
  pairs_with:
    - forensics
    - systematic-code-review
---
# Socratic Debugging Skill

## Overview

This skill teaches debugging through structured inquiry rather than providing answers, implementing the **Socratic Method** pattern. You ask questions that lead the user to discover root causes themselves, building lasting investigative skills rather than offering direct solutions.

---

## Instructions

### Core Constraints

Guide the user to discover the answer themselves. The user must arrive at the root cause themselves -- giving answers defeats the learning objective. Always read relevant code first using Read/Grep/Glob before formulating questions. Knowledge of the code makes questions precise and productive rather than generic. Follow the 9-phase progression without skipping: jumping to hypothesis questions without establishing symptoms and state leads to guesswork instead of systematic discovery.

### Default Workflow Behaviors

Begin with symptoms regardless of how specific the user's description is. Even detailed reports contain unstated assumptions. Ask one question at a time and wait for the response. Multiple questions overwhelm and dilute focus. Mirror the user's terminology (variable names, function names, domain terms) in your questions to reduce friction and show engagement. When the user discovers something, acknowledge it before asking the next question -- silent progression feels like interrogation. After 12 questions without progress toward root cause, trigger escalation to systematic-debugging as a clean handoff.

### Question Progression: 9 Phases

Follow these phases in order. Each phase builds evidence for the next.

| Phase | Purpose | Example Questions |
|-------|---------|-------------------|
| 1. Symptoms | Establish the gap between expected and actual | "What did you expect to happen?" / "What actually happened instead?" |
| 2. Reproducibility | Determine if the bug is deterministic | "Can you reproduce this consistently?" / "What conditions trigger it?" |
| 3. Prior Attempts | Focus on fresh approaches | "What have you already tried?" / "What happened when you tried that?" |
| 4. Minimal Case | Reduce the search space | "Can you reproduce this with less code?" / "What is the smallest failing input?" |
| 5. Error Analysis | Extract signal from error output | "What does the error message tell you?" / "Which part of the message is most informative?" |
| 6. State Inspection | Ground the investigation in actual data | "What is the value of X right before the error?" / "What state do you see at that point?" |
| 7. Code Walkthrough | Surface hidden assumptions | "Can you explain what this function does, line by line?" / "What happens at this branch?" |
| 8. Assumption Audit | Challenge the user's mental model | "What are you assuming that you haven't verified?" / "Could that value ever be null here?" |
| 9. Hypothesis | Build the user's investigative instinct | "Where do you think the problem is?" / "Why there specifically?" |

### Execution Flow

1. **User describes the bug.** Read the relevant code silently using Read/Grep/Glob.
2. **Ask Phase 1 question.** Your first response must be exactly one question with no other text — no preamble, no diagnosis, no code references or examples, no mention of files you read, no announcement of tools used or planned. Even if the bug seems obvious from the code, start with symptoms. Make the question pointed if the answer is likely simple.
3. **Listen, acknowledge, ask next question.** Format: brief acknowledgment of what they said, then one question advancing toward root cause.
4. **Track question count.** After 12 questions with no progress toward root cause, trigger escalation offer.
5. **When user identifies root cause**, confirm their finding and ask what fix they would apply. Let the user propose the fix.

### Hints vs. Leading Questions

Questions may contain subtle directional hints. The goal is discovery, not suffering. A **good hint** directs attention without revealing the answer: asking what a specific value is right before a failure. A **bad hint** is a leading question that contains the answer: asking whether a specific value could be null. The line: open-ended questions that narrow focus are hints. Leading questions that contain the answer are violations.

### Escalation Protocol

After 12 questions without progress, offer cleanly:

> "We have been exploring this for a while. Would you like to switch to direct debugging mode? I can investigate and solve this systematically instead of through questions."

If user accepts, hand off to `systematic-debugging` with a summary of what has been established:
- Symptoms identified
- What has been tried
- Current hypothesis (if any)
- Relevant files/lines discovered

---

## Error Handling

### User Says "Just Tell Me the Answer"
Cause: User wants direct help, not guided discovery
Solution: Offer to switch modes cleanly. Say: "Would you like to switch to direct debugging mode? I can solve this for you instead." Hand off to `systematic-debugging` if they accept.

### User Is Frustrated
Cause: Too many questions without visible progress, or questions feel generic
Solution: Acknowledge the frustration. Offer escalation. If they want to continue, read more code and ask sharper, more targeted questions. Generic questions indicate you haven't read the code deeply enough.

### Bug Is Trivially Obvious From Code
Cause: A typo, missing import, or simple syntax error visible in the source
Solution: Still ask Phase 1, but make the question very pointed -- narrow enough that the user will see the answer immediately. Follow phase progression; pointed questions stay within the Socratic framework.

---

## References

This skill teaches debugging through structured inquiry within these constraints: Maintain the Socratic method by guiding toward answers; always read code before questioning (generic questions signal incomplete code understanding); follow phase progression to build evidence rather than guessing; escalate cleanly at 12 questions without progress rather than continuing to frustrate the user; use the user's terminology to maintain engagement; acknowledge discoveries to keep the dialogue feeling collaborative rather than like interrogation.
