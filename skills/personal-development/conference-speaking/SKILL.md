---
name: conference-speaking
description: CFP submissions, talk preparation, and conference speaking strategies
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 06-developer-advocate
bond_type: SECONDARY_BOND
---

# Conference Speaking

Land **speaking opportunities** and deliver memorable conference talks.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - submission_type: enum[cfp, abstract, bio, outline]
    - talk_topic: string
  optional:
    - conference_name: string
    - talk_length: enum[lightning, standard, keynote]
```

### Output
```yaml
output:
  cfp_submission:
    title: string
    abstract: string
    outline: array[Section]
    speaker_bio: string
```

## CFP Strategy

### Finding CFPs
- [Confs.tech](https://confs.tech) - Tech conference aggregator
- [PaperCall](https://www.papercall.io/events) - CFP listings
- [CFP Land](https://www.cfpland.com/) - Conference tracker
- Twitter #CFP hashtag

### CFP Submission Formula

```
Title: Catchy + Clear + Benefit
       "How We Reduced API Latency by 90%"

Abstract: Problem → Solution → Takeaway
       "APIs slowing you down? Learn the three
       techniques we used to cut latency from
       2s to 200ms. Walk away with actionable
       patterns for your own services."

Outline: Show you've thought it through
       1. The latency problem (5 min)
       2. Technique 1: Caching (10 min)
       3. Technique 2: Query optimization (10 min)
       4. Technique 3: Edge computing (10 min)
       5. Results and takeaways (5 min)
```

### Winning CFP Elements

| Element | Why It Works |
|---------|--------------|
| Specific results | "90% faster" vs "faster" |
| Clear takeaways | Audience knows what they'll learn |
| Novel angle | Fresh perspective |
| Speaker credibility | Show you've done this |

## Talk Preparation Timeline

| Weeks Out | Task |
|-----------|------|
| 8 | Outline complete |
| 6 | First draft slides |
| 4 | Full run-through |
| 2 | Refinement + practice |
| 1 | Final polish |
| Day of | Tech check |

## Slide Design Principles

- One idea per slide
- Minimal text (≤6 words per point)
- Large fonts (32pt minimum)
- High contrast colors
- Code with syntax highlighting

## Delivery Tips

1. **Know your opening cold** - First 30 seconds are crucial
2. **Use stories** - Data + narrative = memorable
3. **Live demos** - Risky but impactful (have backup)
4. **End strong** - Clear call to action
5. **Leave time for Q&A** - 5-10 minutes minimum

## Retry Logic

```yaml
retry_patterns:
  cfp_rejected:
    strategy: "Request feedback, revise angle"
    max_attempts: 3

  low_acceptance_rate:
    strategy: "Build portfolio at meetups first"

  demo_fails:
    strategy: "Pre-recorded backup"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| CFP rejection | Email received | Request feedback |
| Demo fails | Crashes on stage | Pre-recorded backup |
| Time runs over | 5-min warning | Skip to conclusion |

## Debug Checklist

```
□ CFP deadline confirmed?
□ Abstract under word limit?
□ Slides tested on 1080p?
□ Demo backed up?
□ Talk rehearsed 3+ times?
□ Travel confirmed?
```

## Test Template

```yaml
test_conference_speaking:
  unit_tests:
    - test_cfp_elements:
        assert: "Title, abstract, outline present"
    - test_abstract_length:
        assert: "150-300 words"

  integration_tests:
    - test_talk_delivery:
        assert: "Within time limit"
```

## Success Metrics

| Metric | Target |
|--------|--------|
| CFP acceptance rate | >20% |
| Talk rating | >4/5 |
| Repeat invitations | 1+ |

## Observability

```yaml
metrics:
  - cfps_submitted: integer
  - cfps_accepted: integer
  - talks_delivered: integer
  - average_rating: float
```

See `assets/` for CFP templates.
