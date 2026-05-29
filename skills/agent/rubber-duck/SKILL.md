---
name: rubber-duck
description: |
  When a user is stuck, frustrated, or describing a problem vaguely, do NOT
  immediately suggest solutions. First, force structured problem articulation
  through targeted questions: What did you expect? What happened instead? What
  have you tried? Only after the problem is clearly defined, propose solutions.
allowed-tools: |
  bash: cat, grep, head, ls
  file: read
---

# Rubber Duck

<purpose>
Users often know the solution to their own problem - they just haven't articulated
it clearly yet. Jumping to solutions before understanding the problem wastes time
and often misses the real issue. This skill enforces the rubber duck debugging
pattern: make them explain it properly first.
</purpose>

## When To Activate

Trigger when you see:

- Vague problem descriptions: "it's not working", "something's wrong"
- Frustration signals: "I've been stuck for hours", "I don't know why"
- Missing context: no error messages, no expected vs actual
- Shotgun debugging: "I tried X, Y, Z and nothing works"
- XY problems: asking about solution B when problem A is the real issue

## Instructions

### Step 1: Resist the Urge to Solve

Do NOT immediately propose solutions. Even if you think you know the answer.

### Step 2: Ask The Three Questions

```
Let me make sure I understand the problem clearly.

1. **What did you expect to happen?**
   [Get specific desired outcome]

2. **What actually happened?**
   [Get specific observed behaviour, error messages, symptoms]

3. **What have you tried so far?**
   [Understand their mental model and eliminate paths]
```

### Step 3: Probe Deeper If Needed

If answers are still vague, follow up:

```
A few more questions to narrow this down:

- When did it last work correctly?
- What changed between then and now?
- Does it fail every time, or intermittently?
- Can you show me the exact error message/output?
- What's the simplest case where it still fails?
```

### Step 4: Reflect Back

Before solving, confirm understanding:

```
Let me make sure I've got this right:

You expected: [X]
But instead: [Y]
You've already ruled out: [Z]

Is that accurate?
```

### Step 5: Now Solve

Only after confirmation, propose solutions - starting with most likely based on their answers.

## The XY Problem

Watch for this pattern:

> User: "How do I get the last 3 characters of a filename in bash?"
> Real problem: They want to check file extensions

When you suspect an XY problem:

```
I can answer that, but I want to make sure I'm solving the right problem.

What are you ultimately trying to accomplish? Sometimes there's a more
direct approach.
```

## Frustration Handling

When user is clearly frustrated:

```
I can tell this has been frustrating. Let's slow down and be systematic.

[Then proceed with the three questions, but with softer framing]
```

Do NOT:
- Be condescending
- Say "calm down"
- Ignore their emotional state
- Rush to solutions to make them feel better

## NEVER

- Jump to solutions on vague problem statements
- Assume you know what they mean
- Skip confirmation step
- Ask more than 3-4 questions before attempting to help
- Be patronising ("have you tried turning it off and on")

## ALWAYS

- Get expected vs actual behaviour
- Understand what they've already tried
- Reflect back your understanding before solving
- Watch for XY problems
- Match their energy (frustrated = calm and methodical)

## Examples

### Example 1: Vague Problem

User: "My API isn't working"

```
Let me make sure I understand.

1. What did you expect the API to do?
2. What's actually happening? (Error message? Wrong response? No response?)
3. What have you tried so far?
```

### Example 2: XY Problem Detection

User: "How do I parse JSON in bash?"

```
I can show you that, but parsing JSON in bash is usually painful.

What are you ultimately trying to do with the JSON? There might be a
cleaner approach depending on your goal.
```

### Example 3: After Clarification

User: "The login doesn't work"
Claude: [asks three questions]
User: "I expect to see the dashboard after login. Instead I get redirected back to login. I've cleared cookies and tried incognito."

```
Got it. So:
- Expected: Login -> Dashboard
- Actual: Login -> Redirected back to login
- Ruled out: Browser cookies/cache

This sounds like a session persistence issue. Let me check a few things...
```

### Example 4: Frustrated User

User: "I've spent 3 hours on this stupid bug and NOTHING works"

```
I hear you - that's genuinely frustrating. Let's be methodical and
figure this out together.

Start from the beginning: what's the expected behaviour, and what
are you seeing instead?
```

<failed-attempts>
What DOESN'T work:

- **Jumping to solutions**: "Have you tried restarting?" misses the actual problem 80% of the time.
- **Asking too many questions at once**: Overwhelms the user. Three questions max, then pause.
- **Generic debugging suggestions**: "Check the logs" without knowing what the problem is.
- **Assuming you understand**: "Oh, that's probably X" before getting the full picture.
- **Skipping the reflection step**: Not confirming understanding leads to solving the wrong problem.
- **Being patronizing**: "Did you try turning it off and on" to someone who's been debugging for hours.
- **Matching frustrated energy**: Stay calm even when user is frustrated. Don't escalate.
- **Solving XY problems literally**: User asks "how to parse JSON in bash" when they should use Python.
- **Taking their first description literally**: The first description is rarely the actual problem.
</failed-attempts>
