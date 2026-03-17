---
name: improve-flow
description: This skill should be used when users drop off mid-task, motivation fades, or experiences feel flat. Applies Peak-End Rule, Goal-Gradient Effect, and Zeigarnik Effect.
---

# Improve Flow & Experience

Applies these laws from lawsofux.com:
- **Peak-End Rule**: Experiences judged by peak moments and endings
- **Goal-Gradient Effect**: Motivation increases as goal approaches
- **Zeigarnik Effect**: Incomplete tasks are remembered better

## When to Use

- Diagnose user drop-off patterns in mid-flow
- Identify flat or forgettable onboarding experiences
- Address lack of visible progress indicators
- Improve retention when users don't return
- Reduce checkout or form abandonment rates

## How to Use

1. **Analyze the current flow** - Map out the user journey from start to finish
2. **Run diagnosis** - Apply the three diagnostic frameworks below to identify gaps
3. **Identify improvements** - Use the law-specific techniques to address each issue
4. **Apply fixes** - Implement changes following the output format structure
5. **Validate with checklist** - Ensure all flow stages are optimized per the design checklist

## The Laws

### Peak-End Rule

> People judge an experience based on how they felt at its most intense point (peak) and at its end, not on the average.

**Application:**
```
DESIGN FOR:
1. One memorable PEAK moment (delight, success, wow)
2. A strong positive ENDING

The middle can be mundane—peaks and ends are remembered.
```

**Techniques:**
- Celebration on completion (confetti, success screen)
- Delightful micro-interactions at key moments
- End with accomplishment, not error or limbo
- Recovery from errors matters more than preventing them

### Goal-Gradient Effect

> Motivation increases as progress approaches the goal.

**Application:**
```
SHOW PROGRESS VISIBLY:
- Progress bars accelerate motivation
- "2 of 5 steps" creates momentum
- Artificial starting progress works (start at 20%)
- Breaking into smaller goals = more motivation hits
```

**Techniques:**
- Progress indicators on multi-step flows
- "Almost there" messaging near completion
- Chunk long tasks into visible milestones
- LinkedIn-style profile completion meters

### Zeigarnik Effect

> People remember uncompleted tasks better than completed ones.

**Application:**
```
USE INCOMPLETENESS STRATEGICALLY:
- Unfinished profiles pull users back
- Draft states create return triggers
- "You're 80% there" is more compelling than "Complete your profile"
- Cliffhangers in onboarding
```

**Techniques:**
- Save partial progress visibly
- Show what's incomplete on dashboard
- Use incompleteness for retention, not frustration
- Don't lose user's work (increases abandonment anxiety)

## Diagnosis

Apply these diagnostic frameworks to identify flow issues:

1. **Assess Peak-End Rule** - Locate the peak moment in the experience and evaluate the ending quality
2. **Evaluate Goal-Gradient Effect** - Check if progress is visible and if momentum accelerates toward completion
3. **Examine Zeigarnik Effect** - Determine whether incompleteness creates productive return triggers or frustration
4. **Map flow stages** - Identify which stages lack appropriate law applications
5. **Document current state** - Record findings using the output format below

## Output Format

```
FLOW DIAGNOSIS

Peak-End Rule:
Current peak: [moment] or [none]
Current ending: [experience]
FIX: [add peak at X / improve ending Y]

Goal-Gradient Effect:
Progress visibility: [visible/hidden]
Steps shown: [Yes/No]
Artificial progress: [used/not used]
FIX: [add progress bar / show steps / start at 20%]

Zeigarnik Effect:
Incomplete states: [how handled]
Return triggers: [exist/missing]
FIX: [save drafts / show incomplete / add reminders]
```

## Flow Design Checklist

| Stage | Law | Technique |
|-------|-----|-----------|
| Start | Goal-Gradient | Show progress from step 1 |
| Start | Zeigarnik | Let them begin before account creation |
| Middle | Goal-Gradient | Break into visible milestones |
| Middle | Zeigarnik | Auto-save, show "draft saved" |
| Peak | Peak-End | Add delight at key success moment |
| End | Peak-End | Celebrate completion, clear next step |
| After | Zeigarnik | Show what else is incomplete |

## Examples

**Onboarding:**
```
Bad: 10 required fields, then "Account created"
Good: Start with win (choose avatar),
      show "3 of 5 steps",
      end with "Welcome! Here's what you can do"
```

**Checkout:**
```
Bad: Long form, then confirmation email
Good: Progress bar, "Almost done!",
      celebration confetti,
      immediate order summary
```
