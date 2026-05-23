---
name: usability-tester
description: Conduct usability tests and identify UX issues through systematic observation. Use when testing user flows, validating designs, identifying friction points, or ensuring users can complete core tasks. Covers test planning, think-aloud protocol, task scenarios, and severity rating.
---

# Usability Tester

Validate that users can successfully complete core tasks through systematic observation.

## Core Principle

**Watch users struggle.** The best way to find UX issues is to observe real users attempting real tasks. Their struggles reveal truth that surveys and analytics cannot.

## Test Planning

### 1. Define Test Objectives

```yaml
Good Objectives:
  - "Can users complete onboarding in <5 minutes?"
  - "Can users find and use the export feature?"
  - "Do users understand the pricing page?"

Bad Objectives:
  - "Test the UI" (too vague)
  - "See if users like it" (subjective, not behavioral)
```

### 2. Research Questions

```yaml
Examples:
  - Where do users get stuck during sign-up?
  - Can users find the settings page?
  - Do users understand what each tier includes?
  - What errors do users encounter?
```

### 3. Identify Core Tasks

Choose 3-5 tasks that represent key user journeys:

```yaml
Example Tasks (Project Management Tool): 1. Sign up and create account
  2. Create your first project
  3. Invite a team member
  4. Assign a task to someone
  5. Export project data
```

### 4. Recruit Participants

```yaml
Sample Size:
  - 5-8 users per persona
  - After 5 users, diminishing returns (Nielsen's research)
  - Test in waves: 5 users → fix issues → test 5 more

Recruitment Criteria:
  - Match target persona
  - Haven't used product before (for onboarding tests)
  - Or: Active users (for feature tests)

Incentives:
  - $50-100 per hour (B2C)
  - $100-200 per hour (B2B professionals)
  - Gift cards work well
```

## Task Scenarios

### Best Practices

✅ **Good task scenario**:

```
"Your team is launching a new project next week. Create a project
called 'Q2 Launch' and invite john@example.com to collaborate."
```

**Why it works**:

- Realistic context
- Clear goal
- Natural language
- Doesn't give step-by-step instructions

❌ **Bad task scenario**:

```
"Click the 'New Project' button, then enter 'Q2 Launch', then
click Settings, then click Invite, then enter email."
```

**Why it fails**:

- Step-by-step instructions
- No context
- Doesn't test discoverability
- User just follows orders

### Task Scenario Template

```yaml
Scenario: [Context/Motivation]
Goal: [What they need to accomplish]
Success Criteria: [How to know they completed it]

Example:
  Scenario: You're preparing for a client meeting tomorrow and need to review past conversations.
  Goal: Find all conversations with "Acme Corp" from the last 30 days
  Success Criteria: User successfully uses search/filter to find conversations
```

## Conducting Tests

### Think-Aloud Protocol

**Key instruction to participant**:

```
"Please think aloud as you work. Tell me what you're looking for,
what you're thinking, what you're trying to do. There are no
wrong answers - we're testing the product, not you."
```

**What to listen for**:

- "I'm looking for..." (what they expect)
- "I thought this would..." (mental models)
- "This is confusing because..." (friction points)
- "I'm not sure if..." (uncertainty)

### Facilitation Rules

✅ **Do**:

- Observe silently
- Take notes
- Let them struggle (reveals issues)
- Ask follow-up questions AFTER task
- Stay neutral

❌ **Don't**:

- Help or explain
- Lead them ("maybe try clicking...")
- Defend design choices
- Interrupt during task
- Show frustration

### Questions to Ask After Each Task

```yaml
Completion Questions:
  - 'On a scale of 1-5, how easy was that task?'
  - 'What were you expecting to see?'
  - 'What was confusing about that?'
  - 'If you could change one thing, what would it be?'

Discovery Questions:
  - 'Where did you expect to find that?'
  - 'What do you think this [feature] does?'
  - 'Why did you click there?'
```

## Metrics to Track

### Task Success Rate

```yaml
Measurement:
  - Completed: User achieved goal without help
  - Partial: User achieved goal with hints
  - Failed: User could not complete task

Calculation: Task Success Rate = (Completed Tasks / Total Attempts) × 100

Target: ≥80% for core tasks
```

### Time on Task

```yaml
Measurement:
  - Start timer when task begins
  - Stop when user completes or gives up

Analysis:
  - Compare to baseline/previous tests
  - Identify outliers (very fast or very slow)

Target: Varies by task complexity
  - Simple task (e.g., log in): <30 seconds
  - Medium task (e.g., create project): 1-2 minutes
  - Complex task (e.g., configure integration): 3-5 minutes
```

### Error Rate

```yaml
Errors:
  - Wrong path taken
  - Incorrect button clicked
  - Had to backtrack
  - Gave up and tried different approach

Calculation: Errors per Task = Total Errors / Number of Users

Target: <2 errors per task
```

### Satisfaction Rating

```yaml
Post-Task Question:
  "How satisfied are you with completing this task?" (1-5 scale)

  1 = Very Dissatisfied
  2 = Dissatisfied
  3 = Neutral
  4 = Satisfied
  5 = Very Satisfied

Target: ≥4.0 average
```

## Issue Severity Rating

### Severity Formula

```
Severity = Impact × Frequency
```

### Impact Scale (1-3)

```yaml
1 - Low Impact:
  - Minor inconvenience
  - User can easily recover
  - Cosmetic issue

2 - Medium Impact:
  - Causes delay or confusion
  - User eventually figures it out
  - Moderate frustration

3 - High Impact:
  - Blocks task completion
  - User cannot proceed without help
  - Critical to core functionality
```

### Frequency Scale (1-3)

```yaml
1 - Rare:
  - Only 1-2 users encountered
  - Edge case
  - Specific conditions

2 - Occasional:
  - 3-5 users encountered
  - Somewhat common
  - Specific user types

3 - Frequent:
  - Most/all users encountered
  - Consistent issue
  - All user types
```

### Combined Severity

```yaml
Critical (8-9):
  - Impact: 3, Frequency: 3
  - Blocks most users
  → Fix immediately before release

High (6-7):
  - Impact: 3, Frequency: 2 OR Impact: 2, Frequency: 3
  - Significant delay or frequent minor issue
  → Fix before release

Medium (4-5):
  - Impact: 2, Frequency: 2 OR Impact: 3, Frequency: 1
  - Minor frustration or rare blocker
  → Fix in next release

Low (1-3):
  - Impact: 1, Frequency: 1-3
  - Cosmetic or rare minor issue
  → Backlog
```

## System Usability Scale (SUS)

**10-question survey** (post-test, 1-5 Likert scale):

```yaml
Questions (Odd = Positive, Even = Negative): 1. I think I would like to use this product frequently
  2. I found the product unnecessarily complex
  3. I thought the product was easy to use
  4. I think I would need support to use this product
  5. I found the various functions well integrated
  6. I thought there was too much inconsistency
  7. I imagine most people would learn this quickly
  8. I found the product cumbersome to use
  9. I felt very confident using the product
  10. I needed to learn a lot before getting going

Scoring:
  - Odd questions: Score - 1
  - Even questions: 5 - Score
  - Sum all scores
  - Multiply by 2.5
  - Result: 0-100 score

Interpretation:
  ≥80: Excellent
  68-79: Good (industry average)
  51-67: OK
  <51: Needs significant improvement
```

## Test Report Template

```yaml
usability_test_summary:
  date: '2024-01-20'
  participants: 8
  participant_profile: 'New users, age 25-45, tech-savvy'

  tasks:
    - task: 'Create a new project'
      success_rate: '87.5% (7/8)'
      avg_time: '1m 24s'
      errors: 1.2 per user
      satisfaction: 4.3/5

    - task: 'Invite team member'
      success_rate: '62.5% (5/8)'
      avg_time: '2m 45s'
      errors: 2.8 per user
      satisfaction: 3.1/5

  issues:
    - issue: "Users can't find 'Invite' button"
      severity: high
      impact: 3
      frequency: 3
      affected_users: 7/8
      recommendation: "Move 'Invite' button to top of project page, make it more prominent"

    - issue: 'Confusion about project vs workspace'
      severity: medium
      impact: 2
      frequency: 3
      affected_users: 6/8
      recommendation: 'Add tooltip explaining difference, update onboarding'

    - issue: 'Export button text unclear'
      severity: low
      impact: 1
      frequency: 2
      affected_users: 2/8
      recommendation: "Change 'Export' to 'Export to CSV'"

  sus_score: 72 (Good)

  key_insights:
    - 'Onboarding is smooth (87.5% success)'
    - 'Team collaboration features hard to discover'
    - 'Overall product easy to use once features are found'

  recommended_actions:
    1. "High priority: Redesign invite flow"
    2. "Medium priority: Add contextual help for workspace vs project"
    3. "Low priority: Update button labels"
```

## Remote vs In-Person Testing

### Remote Testing (Moderated)

**Tools**: Zoom, Google Meet, UserTesting.com

```yaml
Pros:
  - Can test with users anywhere
  - Lower cost (no travel)
  - Easier to recruit
  - Record sessions easily

Cons:
  - Can't see body language as well
  - Technical issues possible
  - Harder to build rapport
  - Screen sharing can lag

Best Practices:
  - Test your setup beforehand
  - Have backup communication method
  - Ask user to share screen + turn on camera
  - Record session (with permission)
```

### In-Person Testing

```yaml
Pros:
  - See full body language
  - Better rapport
  - No technical issues
  - Can see facial expressions

Cons:
  - Limited geographic reach
  - Higher cost
  - Harder to schedule
  - Need physical space

Best Practices:
  - Set up quiet room
  - Have snacks/water
  - Use screen recording software
  - Position yourself behind/beside user
```

## Test Frequency

```yaml
When to Test:
  - Pre-launch: Test prototypes/designs
  - Post-launch: Test new features
  - Ongoing: Test every major release
  - Quarterly: Full usability audit

Continuous Testing:
  - Week 1: Test with 5 users
  - Week 2: Fix issues
  - Week 3: Test with 5 new users
  - Repeat until success rate ≥80%
```

## Tools & Software

```yaml
Remote Testing:
  - UserTesting.com (recruit + test)
  - UserZoom (enterprise solution)
  - Lookback (live testing)
  - Maze (unmoderated testing)

Recording:
  - Zoom (screen + audio)
  - Loom (quick recordings)
  - OBS (advanced recording)

Analysis:
  - Dovetail (organize insights)
  - Notion (collaborative notes)
  - Miro (affinity mapping)
  - Excel/Sheets (metrics tracking)
```

## Quick Start Checklist

### Planning Phase

- [ ] Define test objectives
- [ ] Write 3-5 task scenarios
- [ ] Recruit 5-8 participants
- [ ] Prepare test script
- [ ] Set up recording

### Testing Phase

- [ ] Welcome participant
- [ ] Explain think-aloud protocol
- [ ] Conduct tasks (don't help!)
- [ ] Ask follow-up questions
- [ ] Administer SUS survey
- [ ] Thank participant

### Analysis Phase

- [ ] Calculate success rates
- [ ] Identify common issues
- [ ] Rate issue severity
- [ ] Create report
- [ ] Share with team
- [ ] Prioritize fixes

## Common Pitfalls

❌ **Testing with employees**: They know the product too well
❌ **Helping users during tasks**: Let them struggle to find real issues
❌ **Only testing happy path**: Test error cases and edge cases too
❌ **Not enough participants**: 5 minimum per persona
❌ **Ignoring low-severity issues**: They add up to poor experience
❌ **Testing but not fixing**: Usability tests are worthless if you don't act

## Summary

Great usability testing:

- ✅ Test with 5-8 users per persona
- ✅ Use realistic task scenarios (not step-by-step)
- ✅ Think-aloud protocol (understand mental models)
- ✅ Don't help users during tasks
- ✅ Track success rate, time, errors, satisfaction
- ✅ Rate issues by severity (impact × frequency)
- ✅ Fix high-priority issues before release
- ✅ Test continuously, not just once
