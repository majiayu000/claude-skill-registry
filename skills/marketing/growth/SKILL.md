---
name: growth
description: Growth engine for ID8Labs. Systematic experimentation and optimization to scale products through data-driven decisions, retention focus, and sustainable acquisition channels.
version: 1.0.0
mcps: [Supabase, Perplexity]
subagents: []
skills: [analytics-tracking]
---

# ID8GROWTH - Growth Engine

## Purpose

Scale your launched product through systematic experimentation. Growth is not magic—it's methodology.

**Philosophy:** Retention beats acquisition. One channel mastered beats five attempted. Data over intuition.

---

## When to Use

- Product is launched and has initial users
- User needs to grow user base
- User asks "how do I get more users?"
- User wants to improve retention
- User needs help with analytics
- User wants to optimize conversion
- Project is in LAUNCHING or GROWING state

---

## Commands

### `/growth <project-slug>`

Run full growth analysis and planning.

**Process:**
1. BASELINE - Understand current metrics
2. MODEL - Map growth mechanics
3. DIAGNOSE - Find bottlenecks
4. HYPOTHESIZE - Generate experiments
5. PRIORITIZE - ICE scoring
6. EXECUTE - Run experiments
7. LEARN - Analyze and iterate

### `/growth metrics`

Audit current analytics and define key metrics.

### `/growth funnel`

Analyze conversion funnel and identify drop-offs.

### `/growth experiment <hypothesis>`

Design a specific growth experiment.

### `/growth retention`

Deep dive on retention and engagement.

---

## Growth Philosophy

### Solo Builder Reality

| What Works | What Doesn't |
|------------|--------------|
| Focused effort on one channel | Spray-and-pray multi-channel |
| Retention optimization | Endless acquisition |
| Organic/content marketing | Expensive paid acquisition |
| Personal touch | Automated spam |
| Slow compounding | Viral hacks |

### Growth Priorities

**Stage 1: Pre-PMF (< 100 users)**
- Focus: Finding users who love it
- Metric: Qualitative feedback, NPS
- Don't worry about: Scale

**Stage 2: Early Traction (100-1000 users)**
- Focus: Retention and activation
- Metric: Day 1/7/30 retention
- Don't worry about: Growth rate

**Stage 3: Growth (1000+ users)**
- Focus: Scalable acquisition
- Metric: CAC, LTV, growth rate
- Now optimize: Everything

---

## Process Detail

### Phase 1: BASELINE

**Establish current state:**

| Metric | Value | Source |
|--------|-------|--------|
| Total users | {N} | Database |
| Active users (DAU/WAU/MAU) | {N} | Analytics |
| Activation rate | {%} | Funnel |
| Retention (D1/D7/D30) | {%} | Cohort |
| Conversion (free→paid) | {%} | Funnel |
| Revenue (MRR/ARR) | ${X} | Payments |
| NPS | {score} | Survey |

**If no tracking:**
- Set up analytics first
- Use `analytics-tracking` skill
- Minimum: Sign-ups, activation, retention

### Phase 2: MODEL

**Map your growth mechanics:**

```
ACQUISITION
How do users find you?
├── Organic search
├── Social/content
├── Referrals
├── Paid (if any)
└── Direct

ACTIVATION
What's the "aha moment"?
├── First action completed
├── Value received
└── Setup finished

RETENTION
Why do they come back?
├── Core value loop
├── Notifications
├── Habit formation
└── New content/features

REVENUE
How do you monetize?
├── Subscription
├── Usage-based
├── One-time
└── Freemium conversion

REFERRAL
How do they spread it?
├── Word of mouth
├── Built-in sharing
├── Incentivized referral
└── Social proof
```

### Phase 3: DIAGNOSE

**Find the bottleneck:**

| Stage | Benchmark | Your Rate | Status |
|-------|-----------|-----------|--------|
| Visitor → Sign-up | 2-5% | {%} | {OK/LOW} |
| Sign-up → Activated | 20-40% | {%} | {OK/LOW} |
| Activated → Day 7 | 20-30% | {%} | {OK/LOW} |
| Day 7 → Day 30 | 50-70% | {%} | {OK/LOW} |
| Free → Paid | 2-5% | {%} | {OK/LOW} |

**Diagnosis framework:**
1. Compare to benchmarks
2. Identify biggest drop-off
3. That's your focus

### Phase 4: HYPOTHESIZE

**Generate experiment ideas:**

For each bottleneck, generate 3-5 hypotheses:

```
If we [change]
Then [metric] will [improve/increase/decrease]
Because [reasoning]
```

**Example:**
```
If we add an onboarding checklist
Then activation rate will increase by 20%
Because users will know what to do next
```

### Phase 5: PRIORITIZE

**ICE Scoring:**

| Experiment | Impact | Confidence | Ease | Score |
|------------|--------|------------|------|-------|
| {exp 1} | {1-10} | {1-10} | {1-10} | {avg} |
| {exp 2} | {1-10} | {1-10} | {1-10} | {avg} |

**Definitions:**
- **Impact:** How much will this move the metric?
- **Confidence:** How sure are we it will work?
- **Ease:** How easy is it to implement?

**Rule:** Do highest ICE score first.

### Phase 6: EXECUTE

**For each experiment:**

1. Define hypothesis clearly
2. Define success metric
3. Define sample size needed
4. Implement change
5. Run for sufficient time
6. Analyze results
7. Document learnings

**Minimum experiment duration:**
- High traffic: 1-2 weeks
- Low traffic: 2-4 weeks
- Statistical significance matters

### Phase 7: LEARN

**After each experiment:**

| Question | Answer |
|----------|--------|
| Did it work? | {Yes/No/Inconclusive} |
| What was the lift? | {X}% |
| Why did it work/fail? | {reasoning} |
| What did we learn? | {insight} |
| What's next? | {next experiment} |

---

## Framework References

### Growth Loops
`frameworks/growth-loops.md` - Viral, content, flywheel mechanics

### Analytics
`frameworks/analytics.md` - Metrics, tracking, dashboards

### Acquisition
`frameworks/acquisition.md` - Channels, CAC, scale

### Retention
`frameworks/retention.md` - Engagement, churn, habit

### Optimization
`frameworks/optimization.md` - A/B testing, CRO

---

## Output Templates

### Growth Model
`templates/growth-model.md` - Growth strategy document

### Metrics Dashboard
`templates/metrics-dashboard.md` - KPI tracking structure

---

## Tool Integration

### MCPs

**Supabase:**
- Query user data for analysis
- Cohort analysis
- Funnel tracking

**Perplexity:**
- Research growth tactics
- Find benchmarks
- Competitor analysis

### Skills

**analytics-tracking:**
- Set up tracking
- Define events
- Create dashboards

---

## Handoff

After completing growth analysis:

1. **Save outputs:**
   - Growth model → `docs/GROWTH_MODEL.md`
   - Metrics → `docs/METRICS.md`

2. **Log to tracker:**
   ```
   /tracker log {project-slug} "GROWTH: Analysis complete. Focus: {bottleneck}. Top experiment: {experiment}."
   ```

3. **Update state:**
   ```
   /tracker update {project-slug} GROWING
   ```

4. **Next steps:**
   - Execute top-priority experiments
   - Review results weekly
   - When stable, transition to ops

---

## Key Metrics Cheat Sheet

### AARRR Funnel

| Stage | What to Track |
|-------|---------------|
| **Acquisition** | Traffic, channels, CAC |
| **Activation** | Sign-up rate, onboarding completion |
| **Retention** | DAU/MAU, D1/D7/D30, churn |
| **Revenue** | MRR, ARPU, LTV |
| **Referral** | K-factor, invite rate |

### Benchmarks

| Metric | Poor | OK | Good | Great |
|--------|------|----|----- |-------|
| D1 retention | <10% | 10-20% | 20-30% | >30% |
| D7 retention | <5% | 5-10% | 10-20% | >20% |
| D30 retention | <2% | 2-5% | 5-10% | >10% |
| Free→Paid | <1% | 1-2% | 2-5% | >5% |
| NPS | <0 | 0-30 | 30-50 | >50 |

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Vanity metrics | Don't drive business | Focus on actionable metrics |
| Too many experiments | No learnings | One experiment at a time |
| No hypothesis | Can't learn | Always have clear hypothesis |
| Short experiments | Inconclusive | Run to significance |
| Ignoring retention | Leaky bucket | Fix retention first |
| Copying others | Context matters | Adapt to your situation |

---

## Quality Checks

Before finalizing growth plan:

- [ ] Baseline metrics established
- [ ] Biggest bottleneck identified
- [ ] Hypotheses are testable
- [ ] Experiments are prioritized
- [ ] Success metrics defined
- [ ] Realistic timeline set
- [ ] Learning process planned
