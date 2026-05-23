---
name: public-speaking
description: Public speaking techniques for developer conferences, meetups, and presentations
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 06-developer-advocate
bond_type: PRIMARY_BOND
---

# Public Speaking for DevRel

Master **public speaking** for developer conferences, meetups, and technical presentations.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - talk_type: enum[lightning, standard, keynote, workshop]
    - topic: string
  optional:
    - duration_minutes: integer
    - audience_level: enum[beginner, intermediate, advanced]
    - demo_included: boolean
```

### Output
```yaml
output:
  talk_prep:
    outline: markdown
    slide_count: integer
    speaker_notes: array[string]
  delivery:
    hook: string
    key_messages: array[string]
    closing_cta: string
```

## Core Techniques

### The Hook (First 30 Seconds)
```
First 30 seconds determine if audience stays engaged:
- Start with a problem statement
- Ask a provocative question
- Share a surprising statistic
- Tell a brief story
```

### Storytelling Structure
```
Setup → Conflict → Resolution → Takeaway

Example:
"We had 10,000 API errors per day..."
"We tried caching, it made it worse..."
"Then we discovered rate limiting patterns..."
"Here's how you can implement it too..."
```

### Rule of Three
- Three main points per talk
- Three examples per concept
- Three takeaways for audience

## Presentation Tips

| Technique | Description | Best For |
|-----------|-------------|----------|
| **PechaKucha** | 20 slides, 20 seconds each | Quick overviews |
| **Problem-Solution** | Pain → Fix → Proof | Technical tutorials |
| **Demo-First** | Show working, then explain | Product showcases |
| **Repetition** | Key phrases for emphasis | Key concepts |

## Talk Types

| Type | Duration | Slides | Prep Time |
|------|----------|--------|-----------|
| Lightning | 5 min | 5-10 | 2-4 hours |
| Standard | 20-30 min | 20-40 | 1-2 weeks |
| Keynote | 45-60 min | 40-60 | 3-4 weeks |
| Workshop | 2-4 hours | 30-50 | 4-6 weeks |

## Handling Q&A

1. **Anticipate Questions**: Prepare for likely queries
2. **Active Listening**: Fully understand before answering
3. **Be Concise**: Don't ramble
4. **Difficult Questions**: "Great question, let me address that..."
5. **Unknown Answers**: "I'll get back to you on that"

## Nervousness Management

- Practice out loud (not just in head)
- Arrive early, check setup
- Have water nearby
- Use speaker notes (not scripts)
- Focus on helping audience, not on yourself

## Retry Logic

```yaml
retry_patterns:
  tech_failure:
    strategy: "Switch to backup slides/demo"
    fallback: "Continue without demo, describe visually"

  lost_place:
    strategy: "Pause, check notes, summarize so far"
    recovery: "As I was saying... [pick up thread]"

  audience_disengaged:
    strategy: "Ask question, add interactive element"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Slides won't load | Black screen | Use backup USB/PDF |
| Demo crashes | Error message | Pre-recorded backup |
| Running over time | 5 min warning | Skip to conclusion |
| Mic issues | No audio | Project louder |

## Debug Checklist

```
□ Talk outline reviewed?
□ Slides tested on actual display?
□ Demo rehearsed 3+ times?
□ Backup slides on USB?
□ Speaker notes ready?
□ Water at podium?
□ Mic tested?
□ Timing practiced?
```

## Test Template

```yaml
test_public_speaking:
  unit_tests:
    - test_timing:
        input: "Full rehearsal"
        assert: "Within ±2 min of target"
    - test_key_messages:
        input: "3 takeaways"
        assert: "Audience can recall"

  integration_tests:
    - test_full_delivery:
        scenario: "Complete run-through"
        assert: "Smooth flow, on time"
```

## Observability

```yaml
metrics:
  - audience_size: integer
  - talk_rating: float
  - on_time_finish: boolean
  - demo_success: boolean
```

See `assets/` for talk templates and `references/` for presentation guides.
