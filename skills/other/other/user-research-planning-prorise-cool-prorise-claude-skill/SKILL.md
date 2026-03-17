---
name: user-research-planning
description: Plan user research studies - method selection, participant recruitment, study design, and research questions for generative and evaluative research.
allowed-tools: Read, Glob, Grep, Task
---

# User Research Planning

Plan and design user research studies for gathering insights about users, their needs, behaviors, and pain points.

## When to Use This Skill

Use this skill when:

- **User Research Planning tasks** - Working on plan user research studies - method selection, participant recruitment, study design, and research questions for generative and evaluative research
- **Planning or design** - Need guidance on User Research Planning approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Skill Loading First

Before answering ANY user research question:

2. Use official UX research methodology sources
3. Base all guidance on established research practices

## Research Method Selection

### Method Categories

| Category | Purpose | When to Use |
|----------|---------|-------------|
| **Generative/Discovery** | Understand problem space, user needs | Early product development, problem framing |
| **Evaluative/Formative** | Test solutions, gather feedback | During design, iteration |
| **Summative** | Measure success, validate | Post-launch, benchmarking |

### Research Methods Matrix

| Method | Type | Sample Size | Time | Best For |
|--------|------|-------------|------|----------|
| **Contextual Inquiry** | Generative | 5-10 | 2-3 hours each | Understanding workflows in context |
| **User Interviews** | Generative | 8-12 | 45-60 min each | Deep understanding of needs/motivations |
| **Diary Studies** | Generative | 10-20 | 1-4 weeks | Longitudinal behavior patterns |
| **Ethnographic Observation** | Generative | 5-15 | Full days | Natural behavior in environment |
| **Focus Groups** | Generative | 6-10 per group | 90-120 min | Group dynamics, idea generation |
| **Surveys** | Evaluative | 100+ | Varies | Quantitative validation, reach |
| **Card Sorting** | Evaluative | 15-30 | 30-60 min | Information architecture |
| **Tree Testing** | Evaluative | 50+ | 10-20 min | Navigation validation |
| **Usability Testing** | Evaluative | 5-8 | 45-60 min | Interface evaluation |
| **A/B Testing** | Summative | 1000+ | Days-weeks | Comparing alternatives at scale |

### Method Selection Decision Tree

```text
What do you want to learn?
├── About users, their needs, and context
│   ├── In their natural environment → Contextual Inquiry / Ethnography
│   ├── Their motivations and attitudes → User Interviews
│   └── Behavior over time → Diary Studies
├── About your solution's effectiveness
│   ├── Can they complete tasks? → Usability Testing
│   ├── Can they find content? → Tree Testing / Card Sorting
│   └── Which version performs better? → A/B Testing
└── About broad patterns and preferences
    └── Large-scale validation → Surveys
```

## Study Design Framework

### Research Plan Structure

```markdown
# Research Plan: [Study Name]

## Background
- Business context
- What we know already
- Knowledge gaps

## Research Objectives
1. [Primary objective - what must we learn?]
2. [Secondary objective]
3. [Secondary objective]

## Research Questions
- RQ1: [Specific, answerable question]
- RQ2: [Specific, answerable question]
- RQ3: [Specific, answerable question]

## Methodology
- **Method:** [Selected method with justification]
- **Participants:** [Number and characteristics]
- **Duration:** [Session length, overall timeline]
- **Location:** [Remote/in-person, specific locations]

## Participant Criteria
### Must Have
- [Criterion 1]
- [Criterion 2]

### Nice to Have
- [Criterion 1]

### Exclusions
- [People who should not participate]

## Recruitment
- **Source:** [How we'll find participants]
- **Screener:** [Key screening questions]
- **Incentive:** [Compensation details]

## Materials
- [ ] Screener questionnaire
- [ ] Discussion guide / Protocol
- [ ] Consent forms
- [ ] Recording setup
- [ ] Note-taking templates

## Timeline
| Phase | Dates | Activities |
|-------|-------|------------|
| Setup | Week 1 | Finalize protocol, recruit |
| Fieldwork | Week 2-3 | Conduct sessions |
| Analysis | Week 4 | Synthesize findings |
| Report | Week 5 | Present recommendations |

## Team
- **Lead Researcher:** [Name]
- **Note Taker:** [Name]
- **Stakeholder Observer:** [Name]

## Deliverables
- [ ] Raw notes and recordings
- [ ] Affinity diagram / Themes
- [ ] Research report
- [ ] Presentation to stakeholders
```

## Participant Recruitment

### Sample Size Guidelines

| Method | Minimum | Recommended | Notes |
|--------|---------|-------------|-------|
| Interviews | 5 | 8-12 | Until saturation |
| Usability Tests | 5 | 5-8 | 85% issues found at 5 |
| Card Sorts (Open) | 15 | 30+ | More = more stable patterns |
| Card Sorts (Closed) | 15 | 30+ | Statistical significance |
| Tree Tests | 50 | 100+ | Quantitative validity |
| Surveys | 100 | 300+ | Depends on analysis |
| Diary Studies | 10 | 15-20 | Account for dropout |

### Screener Question Types

```csharp
// Example: Screener model for .NET research recruitment system
public class ScreenerResponse
{
    public Guid RespondentId { get; init; }
    public DateTimeOffset CompletedAt { get; init; }
    public required List<ScreenerAnswer> Answers { get; init; }
    public ScreenerResult Result { get; private set; }

    public void Evaluate(ScreenerCriteria criteria)
    {
        var score = 0;
        var disqualified = false;

        foreach (var answer in Answers)
        {
            if (criteria.Disqualifiers.Contains(answer))
            {
                disqualified = true;
                break;
            }

            if (criteria.MustHave.Contains(answer))
                score += 10;
            else if (criteria.NiceToHave.Contains(answer))
                score += 5;
        }

        Result = disqualified
            ? ScreenerResult.Disqualified
            : score >= criteria.MinimumScore
                ? ScreenerResult.Qualified
                : ScreenerResult.NotQualified;
    }
}

public record ScreenerCriteria
{
    public required HashSet<ScreenerAnswer> MustHave { get; init; }
    public required HashSet<ScreenerAnswer> NiceToHave { get; init; }
    public required HashSet<ScreenerAnswer> Disqualifiers { get; init; }
    public required int MinimumScore { get; init; }
}
```

### Screener Best Practices

**Do:**

- Start with general questions, get specific later
- Include behavioral questions (past actions > hypotheticals)
- Add attention check questions
- Screen for articulation ability (open-ended response)
- Verify availability and technology requirements

**Don't:**

- Lead with qualifying questions (gaming)
- Use double-barreled questions
- Make qualifying criteria obvious
- Ask about future intentions only

### Example Screener Structure

```markdown
## Screener: [Study Name]

### Section 1: Demographics (General)
1. What is your age range?
2. What is your occupation?

### Section 2: Behavioral Screening
3. How often do you [relevant behavior]?
   - Daily [QUALIFY]
   - Weekly [QUALIFY]
   - Monthly [CONSIDER]
   - Rarely/Never [DISQUALIFY]

4. In the past 3 months, have you [specific action]?
   - Yes, multiple times [QUALIFY]
   - Yes, once [CONSIDER]
   - No [DISQUALIFY]

### Section 3: Experience Level
5. How would you describe your experience with [tool/product]?
   - Expert (3+ years) [SEGMENT A]
   - Intermediate (1-3 years) [SEGMENT B]
   - Beginner (< 1 year) [SEGMENT C]

### Section 4: Articulation Check
6. Please describe a recent time when [relevant scenario].
   What happened and what did you do?
   [Open-ended - evaluate quality of response]

### Section 5: Logistics
7. Are you available for a 60-minute session during [date range]?
8. Do you have access to [required technology]?
9. Are you comfortable with [video recording/screen sharing]?
```

## Research Questions

### SMART Research Questions

Research questions should be:

- **S**pecific: Focused on one concept
- **M**easurable: Can be answered with data
- **A**chievable: Within scope and resources
- **R**elevant: Addresses business/user needs
- **T**ime-bound: Scoped to study timeline

### Question Hierarchy

```text
Research Goal (High-level)
└── Research Question (Study-level)
    └── Interview Questions (Session-level)
        └── Follow-up Probes (Moment-level)
```

### Example Transformation

**Business Question:** Why aren't users completing checkout?

**Research Questions:**

- RQ1: What are users' mental models of the checkout process?
- RQ2: At what points do users experience friction or confusion?
- RQ3: What information do users need to feel confident completing purchase?

**Interview Questions:**

- "Walk me through your last online purchase experience."
- "What goes through your mind when you reach a checkout page?"
- "What would make you abandon a purchase at checkout?"

**Probes:**

- "Tell me more about that..."
- "What did you expect to happen?"
- "How did that make you feel?"

## Interview Guide Structure

### Template: Semi-Structured Interview

```markdown
# Interview Guide: [Study Name]

## Before Session (5 min)
- [ ] Test recording equipment
- [ ] Review participant background
- [ ] Prepare materials

## Introduction (5 min)
"Hi [Name], thank you for joining us today. I'm [Researcher] and I'll be
facilitating our conversation. [Note-taker] will be taking notes.

We're interested in learning about [topic]. There are no right or wrong
answers—we want to understand your genuine experiences and perspectives.

This session will last about [X] minutes. We'll record for our notes,
but the recording won't be shared outside the research team.

Do you have any questions before we begin?"

## Warm-up (5 min)
- Tell me a bit about yourself and your role.
- How long have you been [relevant context]?

## Core Questions (30-40 min)

### Topic 1: [Theme]
- Question 1 [Primary]
  - Probe: [Follow-up if needed]
  - Probe: [Alternative angle]
- Question 2 [Secondary]

### Topic 2: [Theme]
- Question 3 [Primary]
- Question 4 [Primary]

### Topic 3: [Theme]
- Question 5 [Primary]

## Concept/Prototype Feedback (if applicable, 10 min)
"I'd like to show you something we're considering..."
- What's your first impression?
- What would you expect [feature] to do?
- What questions do you have?

## Wrap-up (5 min)
- Is there anything else you'd like to share?
- Do you have any questions for me?

"Thank you so much for your time today. Your insights are incredibly
valuable. [Incentive details]"

## After Session
- [ ] Quick debrief with note-taker
- [ ] Note immediate impressions
- [ ] Flag key quotes
```

## Research Outputs

### Deliverable Types

| Output | Purpose | Audience |
|--------|---------|----------|
| **Research Report** | Comprehensive findings | Full team |
| **Executive Summary** | Key insights, 1-2 pages | Leadership |
| **Affinity Diagram** | Organized themes | Research/Design |
| **Journey Map** | User experience flow | Product/Design |
| **Personas** | User archetypes | All teams |
| **Video Highlights** | Evidence and empathy | Stakeholders |
| **Recommendations** | Actionable next steps | Product team |

### Findings Framework

```markdown
## Finding: [Descriptive Title]

**Theme:** [Category this belongs to]

**Observation:** What we saw/heard
[Factual description of behavior or statement]

**Evidence:**
- P3: "Direct quote supporting observation"
- P7: "Another supporting quote"
- [X/N participants exhibited this]

**Insight:** What it means
[Interpretation - why this matters, what it reveals]

**Implication:** What to do about it
[Recommendation or design opportunity]

**Severity/Opportunity:** [High/Medium/Low]
```

## .NET Research Data Model

```csharp
// Research study management
public class ResearchStudy
{
    public Guid Id { get; init; }
    public required string Name { get; init; }
    public required ResearchType Type { get; init; }
    public required string Objective { get; init; }
    public required List<string> ResearchQuestions { get; init; }
    public required ParticipantCriteria Criteria { get; init; }
    public required int TargetParticipants { get; init; }
    public required DateRange FieldworkPeriod { get; init; }
    public StudyStatus Status { get; private set; }

    public List<ResearchSession> Sessions { get; } = [];
    public List<Finding> Findings { get; } = [];
}

public enum ResearchType
{
    ContextualInquiry,
    UserInterview,
    DiaryStudy,
    UsabilityTest,
    CardSort,
    TreeTest,
    Survey,
    FocusGroup
}

public record ParticipantCriteria
{
    public required List<string> MustHave { get; init; }
    public required List<string> NiceToHave { get; init; }
    public required List<string> Exclusions { get; init; }
}

public class Finding
{
    public Guid Id { get; init; }
    public required string Theme { get; init; }
    public required string Observation { get; init; }
    public required List<Evidence> Evidence { get; init; }
    public required string Insight { get; init; }
    public required string Implication { get; init; }
    public required Severity Severity { get; init; }
}

public record Evidence(
    Guid ParticipantId,
    string Quote,
    TimeSpan? Timestamp,
    string? Context
);
```

## Checklist: Research Planning

### Before Starting

- [ ] Clearly defined business question
- [ ] Stakeholder alignment on objectives
- [ ] Timeline and resources confirmed
- [ ] Ethics/legal review if needed

### Study Design

- [ ] Method selected and justified
- [ ] Research questions documented
- [ ] Sample size determined
- [ ] Participant criteria defined
- [ ] Screener created

### Materials

- [ ] Discussion guide/protocol
- [ ] Consent forms
- [ ] Recording setup tested
- [ ] Note-taking templates
- [ ] Stimulus materials (if any)

### Recruitment

- [ ] Recruitment channels identified
- [ ] Screener deployed
- [ ] Participants scheduled
- [ ] Incentives arranged
- [ ] Confirmation emails sent

### During Fieldwork

- [ ] Pre-session checklist
- [ ] Consistent protocol across sessions
- [ ] Daily debriefs scheduled
- [ ] Issue escalation plan

### After Fieldwork

- [ ] All sessions completed
- [ ] Notes organized
- [ ] Analysis approach defined
- [ ] Synthesis sessions scheduled
- [ ] Report timeline set

## Related Skills

- `usability-testing` - Test design and execution
- `information-architecture` - Card sorting, tree testing
- `service-blueprinting` - Service design research
- `journey-mapping` (business-analysis) - Journey research synthesis
