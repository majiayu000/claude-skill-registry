---
name: hiring-and-interviews
description: "Use when designing technical interview processes, creating system design questions, building evaluation rubrics, structuring take-home assessments, or reducing bias in hiring."
---

# Hiring and Interviews

## Pipeline Design

### Standard Technical Hiring Pipeline

| Stage | Duration | Owner | Purpose | Pass Rate |
|-------|----------|-------|---------|-----------|
| 1. Sourcing | Ongoing | Recruiter | Build candidate pool | N/A |
| 2. Recruiter Screen | 30 min | Recruiter | Role fit, logistics, comp range | ~50% |
| 3. Technical Screen | 45-60 min | Engineer | Core competency check | ~30-40% |
| 4. Technical Deep Dive | 2-4 hrs | Panel (2-3) | Coding + system design | ~25-35% |
| 5. Team/Culture Fit | 45 min | Hiring manager | Values alignment, collaboration | ~80% |
| 6. Offer & Close | 1-2 weeks | Recruiter + HM | Comp, start date, negotiation | ~70-80% |

### Pipeline Customization

| Role Level | Skip Screen? | System Design? | Take-Home? | Panel Size |
|---|---|---|---|---|
| Junior (0-2 yr) | No | No | Optional | 2 |
| Mid (3-5 yr) | No | Simplified | Optional | 3 |
| Senior (5-8 yr) | Sometimes | Yes (45 min) | Optional | 3-4 |
| Staff+ (8+ yr) | Yes | Yes (60 min) | No | 4-5 |

## Question Type Selection

### When to Use Each Format

| Format | Best For | Avoid When | Duration |
|--------|----------|------------|----------|
| Live coding | Algorithm thinking, code fluency | Senior+ roles (too artificial) | 45 min |
| System design | Architecture skills, tradeoff reasoning | Junior roles (<2 yr experience) | 45-60 min |
| Behavioral | Leadership, conflict resolution, values | Sole evaluation method | 30-45 min |
| Take-home | Real-world code quality, completeness | Candidate has <3 days, senior roles | 2-4 hrs |
| Pair programming | Collaboration, communication, debugging | Remote async interviews | 60 min |
| Code review | Reading comprehension, feedback quality | Candidates unfamiliar with language | 30-45 min |
| Portfolio review | Candidates with public work (OSS, etc.) | Roles requiring specific tech assessment | 30 min |

### Live Coding Best Practices
- Provide the problem statement in writing (don't make them memorize it)
- Allow language choice when possible
- Focus on problem-solving process, not syntax recall
- Give hints when stuck for >5 min (evaluate how they use hints)
- Reserve 10 min at end for questions

## System Design Interview Structure

### 45-Minute Format

| Phase | Time | Interviewer Role | Candidate Should |
|-------|------|------------------|------------------|
| Problem statement | 2 min | Present the scenario | Listen, take notes |
| Requirements | 8 min | Answer questions, guide scope | Ask clarifying questions, define scope |
| Estimation | 5 min | Validate assumptions | Back-of-envelope math, state assumptions |
| High-level design | 12 min | Probe decisions | Draw components, explain data flow |
| Deep dive | 13 min | Push on weak spots | Go deep on 1-2 components |
| Tradeoffs & wrap-up | 5 min | Ask "what would you change?" | Discuss alternatives, limitations |

### Requirements Phase — Guide the Candidate

```
Functional requirements (what it does):
- "Users can upload photos up to 10MB"
- "Feed shows posts from followed users, reverse chronological"
- "Search returns results within 200ms p99"

Non-functional requirements (how it performs):
- Scale: 10M DAU, 500 req/s average, 5000 req/s peak
- Availability: 99.9% uptime
- Latency: p50 < 50ms, p99 < 200ms
- Consistency: eventual is acceptable for feed, strong for payments
```

### Evaluation Dimensions

| Dimension | Junior | Mid | Senior | Staff |
|-----------|--------|-----|--------|-------|
| Requirements gathering | Needs prompting | Asks good questions | Drives the scoping | Identifies hidden requirements |
| Estimation | Struggles | Reasonable with help | Quick, accurate | Challenges given constraints |
| Component design | Basic boxes | Appropriate services | Justified choices | Novel approaches |
| Data modeling | Simple schemas | Normalized + indexes | Partitioning, replication | Cross-system data strategy |
| Tradeoff discussion | Binary thinking | Names tradeoffs | Quantifies tradeoffs | Connects to business impact |
| Communication | Needs structure | Clear with prompting | Proactive, structured | Adapts to audience |

### Example System Design Questions by Level

| Level | Question | Key Evaluation Focus |
|-------|----------|---------------------|
| Mid | Design a URL shortener | Data modeling, basic scale |
| Senior | Design a notification system | Pub/sub, delivery guarantees, priority |
| Senior | Design a rate limiter | Distributed systems, consistency |
| Staff | Design a multi-region deployment strategy | CAP tradeoffs, failover, data sovereignty |
| Staff | Design the technical interview platform itself | Meta-thinking, full-stack architecture |

## Evaluation Rubrics

### Structured Scoring Template

Score each dimension 1-4. Avoid 5-point scales (the middle becomes a dumping ground).

| Score | Label | Meaning |
|-------|-------|---------|
| 1 | Does not meet | Significant gaps, could not perform at this level |
| 2 | Partially meets | Some capability shown, needs development |
| 3 | Meets | Competent at expected level for the role |
| 4 | Exceeds | Notably strong, above typical for this level |

### Coding Interview Rubric

| Dimension | 1 | 2 | 3 | 4 | Weight |
|-----------|---|---|---|---|--------|
| Problem solving | Can't break down problem | Needs significant hints | Solves with minor hints | Elegant solution, considers edge cases | 30% |
| Code quality | Unreadable, no structure | Works but messy | Clean, well-named, modular | Production-quality, defensive | 25% |
| Communication | Silent or confused | Explains when asked | Thinks aloud naturally | Drives conversation, checks assumptions | 20% |
| Testing mindset | No mention of tests | Tests when prompted | Identifies key test cases | Tests first, edge cases, error paths | 15% |
| Technical depth | Surface-level answers | Knows basics | Explains tradeoffs | Deep knowledge, references real experience | 10% |

### Calibration Sessions

Run calibration before each hiring cycle:

1. Interviewers independently score the same recorded interview (or written scenario)
2. Compare scores; discuss any dimension with >1 point spread
3. Align on what "3 - Meets" looks like for this specific role
4. Document calibrated examples in the rubric

Frequency: once per quarter or when adding new interviewers.

## Take-Home Assessment Design

### Design Principles

| Principle | Implementation |
|-----------|---------------|
| Time-boxed | "Spend no more than 3 hours" (state explicitly) |
| Realistic scope | Resembles actual work, not algorithmic puzzles |
| Clear evaluation criteria | Share the rubric with the candidate |
| Starter code provided | Reduce boilerplate time, focus on the interesting part |
| Multiple valid approaches | No single "right" answer |

### Take-Home Structure

```markdown
# Assessment: [Title]

## Context
You're building [realistic scenario]. The existing codebase has [starter code description].

## Requirements
1. [Core requirement — must complete]
2. [Core requirement — must complete]
3. [Stretch goal — bonus if time allows]

## Provided
- Starter repo: [link]
- API documentation: [link]
- Sample data: included in repo

## Time Expectation
Please spend no more than 3 hours. We value a well-structured partial solution over a rushed complete one.

## Submission
- Push to a private fork or email a zip
- Include a README explaining your approach, tradeoffs, and what you'd do with more time

## Evaluation Criteria
We'll assess:
- Code organization and readability
- Error handling and edge cases
- Testing approach
- Technical decision rationale (in README)
```

### Take-Home Anti-Patterns
- "Build a full app from scratch" (too broad, biases toward free time)
- No time limit (candidates spend 20+ hours, creates inequity)
- Hidden evaluation criteria (candidates can't optimize for what matters)
- Requiring a specific framework/language without business justification

## Hiring Metrics

### Core Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Time to hire | <30 days (eng) | Offer accepted date - req opened date |
| Pipeline velocity | <2 weeks per stage | Average days between stage transitions |
| Pass-through rate | See pipeline table above | Candidates advancing / candidates entering stage |
| Offer acceptance rate | >80% | Offers accepted / offers extended |
| Interview-to-offer ratio | 3:1 to 5:1 | Final round interviews / offers made |
| Interviewer load | <4 hrs/week | Interview hours per interviewer per week |
| Candidate NPS | >60 | Post-interview survey (even for rejects) |

### Quality Metrics (Lagging)

| Metric | Timeframe | Signal |
|--------|-----------|--------|
| New hire performance rating | 6 months | Were our assessments predictive? |
| 90-day retention | 3 months | Did we set correct expectations? |
| 1-year retention | 12 months | Culture and role fit assessment quality |
| Time to productivity | 3 months | Onboarding effectiveness (related to hiring) |
| Regretted attrition | Ongoing | Are we losing people we wanted to keep? |

### Using Metrics

- Track pass-through rates by interviewer to detect outliers (too harsh or too lenient)
- If offer acceptance < 70%, investigate comp, speed, or candidate experience
- If time-to-hire > 45 days, audit where candidates stall

## Anti-Bias Practices

### Structured Interview Protocol

| Practice | Why | How |
|----------|-----|-----|
| Same questions for all candidates | Prevents ad-hoc difficulty variance | Maintain a question bank per role |
| Rubric-first evaluation | Anchors to criteria, not gut feeling | Write rubric before seeing candidates |
| Independent scoring | Prevents groupthink | Interviewers submit scores before debrief |
| Diverse interview panels | Reduces affinity bias | Min 1 interviewer from underrepresented group |
| Blind resume review | Reduces name/school/company bias | Strip identifying info in initial screen |
| Standardized debrief format | Prevents loudest-voice-wins | Each interviewer presents scores, then discussion |

### Debrief Structure

```
1. Each interviewer shares:
   - Score per dimension (already submitted)
   - One strongest signal (positive)
   - One concern (if any)

2. Hiring manager synthesizes:
   - Areas of agreement
   - Areas of disagreement (discuss these)
   - Overall hire/no-hire recommendation

3. Decision:
   - Strong hire: ≥3 interviewers at 3+ average
   - Lean hire: mixed signals, discuss specific concerns
   - No hire: ≥2 interviewers below 2.5 average
```

### Language to Avoid in Evaluations

| Biased Language | Better Alternative |
|---|---|
| "Not a culture fit" | "Specific concern about [collaboration/communication/X]" |
| "Not technical enough" | "Scored 2 on problem solving: needed hints on [specific topic]" |
| "Seemed nervous" | "Communication score reflects difficulty articulating approach" |
| "Overqualified" | "Concern about long-term engagement given stated career goals" |
| "Would be great in a few years" | "Scored 2 on [dimension], meets bar for [lower level] role" |

### Process Audits

Run quarterly:
- Are pass-through rates consistent across demographic groups?
- Are certain interviewers consistently harsh/lenient?
- Do take-home completion rates differ by candidate background?
- Is time-to-hire equitable across candidate sources?

## Gotchas

- **Over-indexing on algorithms**: LeetCode-style questions test a narrow skill. Use them as one signal, not the primary filter. Pair programming or take-homes test more relevant skills.
- **Culture fit bias**: "Culture fit" often means "similar to us." Replace with "values alignment" and define specific values with behavioral indicators.
- **Inconsistent evaluation**: Without rubrics, interviewers anchor on different things. Two interviewers can both say "strong hire" for completely different (even contradictory) reasons.
- **Speed vs. quality tradeoff**: Pressure to fill roles fast leads to lowered bars. Track quality metrics (new hire performance) alongside speed metrics.
- **Take-home inequity**: Candidates with families, multiple jobs, or disabilities may have less discretionary time. Always offer an alternative format (live session with same problem).
- **Interviewer burnout**: Senior engineers doing 6+ hours/week of interviews burn out and give worse evaluations. Cap at 4 hours/week maximum.
- **Feedback black holes**: Candidates who never hear back poison your employer brand. Send rejection emails within 5 business days of decision, always.
- **Panel homogeneity**: All-male, all-senior, all-same-background panels introduce systematic blind spots. Diverse panels catch different signals.
- **Anchoring on pedigree**: FAANG experience or top-school degrees are weak predictors of job performance. Evaluate demonstrated skills, not credentials.
- **Moving the goalposts**: Changing evaluation criteria mid-pipeline because a favored candidate didn't score well. Lock rubrics before interviewing starts.
