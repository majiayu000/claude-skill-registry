---
name: usability-testing
description: Design and plan usability tests - task creation, think-aloud protocols, moderator scripts, metrics definition, and analysis frameworks.
allowed-tools: Read, Glob, Grep, Task
---

# Usability Testing

Design and execute usability tests to evaluate how well users can accomplish tasks with your product.

## When to Use This Skill

Use this skill when:

- **Usability Testing tasks** - Working on design and plan usability tests - task creation, think-aloud protocols, moderator scripts, metrics definition, and analysis frameworks
- **Planning or design** - Need guidance on Usability Testing approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Skill Loading First

Before answering ANY usability testing question:

2. Use established usability testing methodology sources
3. Base all guidance on validated UX research practices

## Usability Testing Types

### Moderated vs Unmoderated

| Aspect | Moderated | Unmoderated |
|--------|-----------|-------------|
| **Facilitator** | Present, guides session | Absent, automated |
| **Depth** | Deep insights, probing | Surface-level, task-focused |
| **Sample Size** | 5-8 typical | 20-100+ typical |
| **Cost** | Higher (facilitator time) | Lower (scale) |
| **Turnaround** | Days-weeks | Hours-days |
| **Best For** | Complex flows, discovery | Validation, benchmarking |

### Testing Formats

| Format | Description | When to Use |
|--------|-------------|-------------|
| **In-Person Moderated** | Face-to-face, controlled environment | High-fidelity prototypes, sensitive topics |
| **Remote Moderated** | Video call, screen share | Geographic diversity, convenience |
| **Remote Unmoderated** | Recorded tasks, no moderator | Scale, quick validation |
| **Guerrilla Testing** | Quick tests in public spaces | Early concepts, low budget |
| **First-Click Testing** | Where users click first | Navigation, labeling |
| **5-Second Test** | First impressions | Visual hierarchy, messaging |
| **Benchmark Testing** | Repeated measurement | Tracking improvements |

## Task Design

### Task Writing Principles

**Good tasks are:**

- **Realistic:** Based on actual user goals
- **Actionable:** Have a clear completion state
- **Specific enough:** Provide necessary context
- **Open enough:** Don't dictate path
- **Measurable:** Success can be defined

### Task Structure Template

```markdown
## Task [N]: [Short Name]

**Scenario:**
[Context setting - why user is doing this]

**Task:**
[What to accomplish - goal, not steps]

**Success Criteria:**
- [ ] [Observable completion indicator]
- [ ] [Secondary success measure if applicable]

**Metrics:**
- Task success (binary or graded)
- Time on task
- Errors/assists needed
- Satisfaction rating

**Probes (Moderated):**
- What are you thinking right now?
- What did you expect to happen?
- What would you do next?
```

### Task Examples

**Poor Task:**
"Click the hamburger menu, then click Settings, then Privacy, then change your notification preferences."

**Good Task:**
"You've been receiving too many email notifications from this app. Find where you can change your notification settings."

**Poor Task:**
"Test the checkout flow."

**Good Task:**
"You've been shopping for a birthday gift and found a book you want to purchase. Complete your purchase using the credit card already saved in your account."

### Task Difficulty Progression

Structure tasks from easy to difficult:

1. **Warm-up task** - Simple, builds confidence
2. **Primary tasks** - Core functionality being tested
3. **Secondary tasks** - Related but less critical
4. **Stretch tasks** - Edge cases, advanced features

## Think-Aloud Protocol

### Concurrent Think-Aloud (CTA)

Participant verbalizes thoughts while performing tasks.

**Moderator Prompts:**

- "Keep talking..."
- "What are you looking at?"
- "What's going through your mind?"
- "What do you expect to happen?"

**Advantages:**

- Real-time insight into thought process
- Natural capture of confusion points
- Rich qualitative data

**Disadvantages:**

- May slow task completion
- Unnatural for some participants
- Can affect behavior

### Retrospective Think-Aloud (RTA)

Participant reviews recording and explains thoughts after.

**Moderator Approach:**

- Play back recording
- Pause at key moments
- Ask "What were you thinking here?"

**Advantages:**

- Doesn't interfere with task
- More accurate time measurements
- Good for complex/fast tasks

**Disadvantages:**

- Memory decay
- Post-hoc rationalization
- Longer sessions

### Hybrid Approach

- Silent task completion
- Brief in-task probes at natural pauses
- Post-task debrief questions

## Moderator Script

### Session Structure

```markdown
# Usability Test Script: [Product/Feature]

## Pre-Session Setup (10 min before)
- [ ] Test recording equipment
- [ ] Verify prototype/product works
- [ ] Review participant background
- [ ] Prepare task cards/materials
- [ ] Set up note-taking template

## Introduction (5 min)

"Hello [Name], thank you for helping us today. I'm [Researcher] and
I'll be guiding our session. [Observer] is taking notes.

We're testing [product], not you. There are no wrong answers or
mistakes—everything you do helps us improve the design.

I'll ask you to complete some tasks and think out loud as you go.
Please share whatever comes to mind—your thoughts, reactions,
questions, even frustrations. There's no need to be polite about
problems you encounter.

We're recording the session to help with our notes. The recording
is confidential and only for our team.

Do you have any questions before we begin?"

## Warm-up Questions (3 min)
- Tell me briefly about your role and typical day.
- How familiar are you with [product category]?
- What tools do you currently use for [relevant activity]?

## Task Introduction
"I'm going to give you a series of tasks. I'll read each task aloud
and you'll also have it written down. Please read it back to me so
I know we're on the same page.

Remember to think out loud. If you get stuck or would normally give
up, just let me know—we can move on. Ready?"

## Tasks

### Task 1: [Name] (Warm-up)
[Read task aloud, hand written card]

**Observer Notes:**
- Start time: ___
- End time: ___
- Success: [ ] Complete [ ] Partial [ ] Fail
- Errors: ___
- Assists: ___
- Path taken: ___

**Post-task Questions:**
- How difficult was that task? (1-7 scale)
- What, if anything, was confusing?

### Task 2: [Name] (Primary)
[Continue pattern...]

### Task 3: [Name] (Primary)
...

## Post-Test Questions (5 min)
- What stood out to you about this experience?
- What was the most frustrating part?
- What was the most satisfying part?
- How does this compare to [competitor/current solution]?
- Would you recommend this to a colleague? Why/why not?

## SUS Questionnaire (3 min)
[Administer System Usability Scale]

## Wrap-up (2 min)
"Thank you so much for your time and feedback. Your insights will
directly influence how we improve [product].

Do you have any final questions for me?

[Explain incentive process]"

## Post-Session
- [ ] Save recording
- [ ] Complete observer notes
- [ ] Note immediate impressions
- [ ] Highlight key quotes/moments
- [ ] Debrief with observers
```

## Usability Metrics

### Task-Level Metrics

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Task Success** | Completed successfully | Binary (0/1) or Graded (0/0.5/1) |
| **Time on Task** | Duration to complete | Seconds/minutes |
| **Errors** | Mistakes made | Count |
| **Assists** | Help requests | Count |
| **Lostness** | Navigation efficiency | (N/S) - (S/N) where N=nodes visited, S=minimum |
| **First Click** | Correct initial action | Binary |

### Study-Level Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **Task Success Rate** | Successes / Attempts | 78% average (Sauro) |
| **Average Time** | Sum(times) / n | Task-dependent |
| **Error Rate** | Errors / Tasks | Lower = better |
| **SUS Score** | Standardized formula | 68 = average |
| **SEQ (Single Ease)** | 7-point post-task | 5.5 = average |
| **SUPR-Q** | Website UX benchmark | Percentile rank |

### System Usability Scale (SUS)

```csharp
// SUS Score calculation
public class SusCalculator
{
    private static readonly string[] Questions =
    [
        "I think that I would like to use this system frequently.",
        "I found the system unnecessarily complex.",
        "I thought the system was easy to use.",
        "I think that I would need the support of a technical person.",
        "I found the various functions well integrated.",
        "I thought there was too much inconsistency.",
        "I imagine most people would learn to use quickly.",
        "I found the system very cumbersome to use.",
        "I felt very confident using the system.",
        "I needed to learn a lot before I could get going."
    ];

    public decimal Calculate(int[] responses)
    {
        if (responses.Length != 10)
            throw new ArgumentException("SUS requires exactly 10 responses");

        // Responses are 1-5 (Strongly Disagree to Strongly Agree)
        decimal score = 0;

        for (int i = 0; i < 10; i++)
        {
            // Odd questions (1,3,5,7,9): score = response - 1
            // Even questions (2,4,6,8,10): score = 5 - response
            score += i % 2 == 0
                ? responses[i] - 1
                : 5 - responses[i];
        }

        // Multiply by 2.5 to get 0-100 scale
        return score * 2.5m;
    }

    public SusInterpretation Interpret(decimal score) => score switch
    {
        >= 85 => SusInterpretation.Excellent,    // Top 10%
        >= 72 => SusInterpretation.Good,         // Top 30%
        >= 68 => SusInterpretation.Average,      // Median
        >= 51 => SusInterpretation.BelowAverage,
        _ => SusInterpretation.Poor
    };
}
```

### Task Success Grading

```csharp
public enum TaskSuccessLevel
{
    Complete = 100,      // Completed without assistance
    PartialMinor = 75,   // Completed with minor struggle
    PartialMajor = 50,   // Completed with significant difficulty
    Assisted = 25,       // Required moderator hint
    Failure = 0          // Could not complete
}

public class TaskResult
{
    public required Guid TaskId { get; init; }
    public required Guid ParticipantId { get; init; }
    public required TaskSuccessLevel Success { get; init; }
    public required TimeSpan Duration { get; init; }
    public required int ErrorCount { get; init; }
    public required int AssistCount { get; init; }
    public required int SingleEaseQuestion { get; init; } // 1-7 scale
    public string? Notes { get; init; }
    public List<string> ClickPath { get; init; } = [];
}
```

## Remote Unmoderated Testing

### Platform Setup Considerations

```csharp
// Configuration for unmoderated test
public class UnmoderatedTestConfig
{
    public required string TestName { get; init; }
    public required string WelcomeMessage { get; init; }
    public required List<ScreenerQuestion> Screener { get; init; }
    public required List<UnmoderatedTask> Tasks { get; init; }
    public required List<PostTestQuestion> PostQuestions { get; init; }

    public TestSettings Settings { get; init; } = new()
    {
        RecordScreen = true,
        RecordAudio = true,
        RecordWebcam = false,
        RequireThinkAloud = true,
        MaxTestDuration = TimeSpan.FromMinutes(30),
        AllowTaskSkip = true
    };
}

public class UnmoderatedTask
{
    public required int Order { get; init; }
    public required string Scenario { get; init; }
    public required string TaskInstructions { get; init; }
    public required string PrototypeUrl { get; init; }
    public TimeSpan? TimeLimit { get; init; }
    public bool RequireRecording { get; init; } = true;
    public List<PostTaskQuestion> FollowUp { get; init; } = [];
}
```

### Unmoderated Task Writing Tips

- **More specific** than moderated (no moderator to clarify)
- **Include context** in the scenario itself
- **Define clear endpoints** (how do they know they're done?)
- **Provide escape hatch** ("If you can't complete this, click 'I'm stuck'")

## Analysis Framework

### Session Analysis Template

```markdown
# Session Analysis: P[N]

**Participant:** [ID/Code]
**Date:** [Date]
**Duration:** [Time]

## Task Performance

| Task | Success | Time | Errors | Assists | SEQ |
|------|---------|------|--------|---------|-----|
| T1 | ✓ | 1:23 | 0 | 0 | 6 |
| T2 | ~ | 3:45 | 2 | 1 | 4 |
| T3 | ✗ | 5:00+ | 3 | - | 2 |

## Key Observations

### Positive
- [What worked well]

### Issues Found
1. **[Issue Name]** - Severity: [Critical/Major/Minor]
   - Location: [Where in interface]
   - Behavior: [What user did]
   - Quote: "[Participant verbalization]"
   - Impact: [Effect on task]

### Notable Quotes
- "[Quote]" - Re: [Topic]

## Recommendations
- [Immediate action]
- [Design consideration]
```

### Severity Rating Scale

| Severity | Definition | Action |
|----------|------------|--------|
| **Critical (4)** | Prevents task completion | Must fix before launch |
| **Major (3)** | Causes significant difficulty | Should fix before launch |
| **Minor (2)** | Causes slight hesitation | Fix if possible |
| **Cosmetic (1)** | Noted but didn't affect task | Consider for future |

### Rainbow Spreadsheet

Track issues across participants:

```markdown
| Issue | P1 | P2 | P3 | P4 | P5 | Count | Severity |
|-------|----|----|----|----|-------|-----|----------|
| Can't find settings | X | X |   | X |   | 3/5 | Major |
| Confusing label | X | X | X | X |   | 4/5 | Major |
| Slow load time |   | X |   |   | X | 2/5 | Minor |
```

## .NET Test Management Model

```csharp
public class UsabilityTest
{
    public Guid Id { get; init; }
    public required string Name { get; init; }
    public required UsabilityTestType Type { get; init; }
    public required string ProductVersion { get; init; }
    public required List<UsabilityTask> Tasks { get; init; }
    public required int TargetParticipants { get; init; }

    public List<TestSession> Sessions { get; } = [];
    public List<UsabilityIssue> Issues { get; } = [];

    public UsabilityTestMetrics CalculateMetrics()
    {
        var completedSessions = Sessions.Where(s => s.Status == SessionStatus.Completed);

        return new UsabilityTestMetrics
        {
            TotalParticipants = completedSessions.Count(),
            OverallSuccessRate = CalculateOverallSuccess(completedSessions),
            AverageSusScore = CalculateAverageSus(completedSessions),
            TaskMetrics = Tasks.Select(t => CalculateTaskMetrics(t, completedSessions)).ToList(),
            IssuesBySeverity = Issues.GroupBy(i => i.Severity)
                .ToDictionary(g => g.Key, g => g.Count())
        };
    }
}

public class UsabilityIssue
{
    public Guid Id { get; init; }
    public required string Title { get; init; }
    public required string Description { get; init; }
    public required IssueSeverity Severity { get; init; }
    public required string Location { get; init; }
    public required List<Guid> AffectedParticipants { get; init; }
    public string? Recommendation { get; init; }
    public IssueStatus Status { get; set; } = IssueStatus.Open;
}

public record UsabilityTestMetrics
{
    public required int TotalParticipants { get; init; }
    public required decimal OverallSuccessRate { get; init; }
    public required decimal AverageSusScore { get; init; }
    public required List<TaskMetrics> TaskMetrics { get; init; }
    public required Dictionary<IssueSeverity, int> IssuesBySeverity { get; init; }
}
```

## Checklist: Usability Test Planning

### Design Phase

- [ ] Test objectives defined
- [ ] Tasks written and reviewed
- [ ] Success criteria established
- [ ] Metrics selected
- [ ] Moderator script drafted

### Preparation

- [ ] Prototype/product ready
- [ ] Recording tools tested
- [ ] Participant schedule set
- [ ] Pilot test completed
- [ ] Script refined from pilot

### Execution

- [ ] Consistent protocol across sessions
- [ ] Notes captured during sessions
- [ ] Issues logged as encountered
- [ ] Daily debriefs conducted

### Analysis

- [ ] All sessions reviewed
- [ ] Metrics calculated
- [ ] Issues compiled and rated
- [ ] Findings synthesized
- [ ] Recommendations prioritized

## Related Skills

- `user-research-planning` - Overall research planning
- `heuristic-evaluation` - Expert review methods
- `accessibility-planning` - Inclusive testing practices
- `prototype-strategy` - Prototype fidelity for testing

**Last Updated:** 2025-12-27
