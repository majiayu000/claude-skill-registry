---
name: bvssh-check
description: "Use to evaluate whether current work aligns with Better Value Sooner Safer Happier. Run at diamond completion and periodically."
---

# BVSSH Check Skill

Evaluate alignment with Better Value Sooner Safer Happier.

## Workflow

For each dimension, assess current state:

### Better
- [ ] Quality improving or stable (not degrading)?
- [ ] Technical debt under control (not growing unchecked)?
- [ ] User satisfaction metrics stable or improving?
- [ ] Defect rate stable or declining?
- Evidence: [cite specific metrics or observations]

### Value
- [ ] Delivering measurable user or business outcomes?
- [ ] Outcome metrics moving (not just output metrics)?
- [ ] Work aligned with strategic priorities?
- [ ] Not shipping features nobody uses?
- Evidence: [cite specific metrics or observations]

### Sooner
- [ ] Lead time stable or decreasing?
- [ ] Batch sizes small?
- [ ] WIP limits respected?
- [ ] Handoffs minimized?
- [ ] No unnecessary waiting or queuing?
- Evidence: [cite specific metrics or observations]

### Safer
- [ ] Security posture maintained or improved?
- [ ] Compliance requirements met?
- [ ] Risk being actively managed (not ignored)?
- [ ] Rollback capability tested?
- [ ] No new single points of failure?
- [ ] Error budget healthy? (SRE -- check dora-metrics.yml sre section)
- Evidence: [cite specific metrics or observations]

### Happier
Smart's Happier covers four stakeholders: **customers, colleagues, citizens, and climate**. "Not 'more for less' at any human or climatic cost."

**Colleagues:**
- [ ] Team working at sustainable pace? No chronic overtime? (XP -- Beck)
- [ ] AI tools helping or adding cognitive load? (APEX DevX)
- [ ] No signs of burnout?
- [ ] Team has autonomy and purpose?
- [ ] Learning happening continuously?

**Customers:**
- [ ] Users expressing satisfaction?
- [ ] Customer advocacy high? (Not just retained — actively recommending?)

**Citizens:**
- [ ] Positive societal impact? (Open knowledge sharing, accessibility, inclusivity)
- [ ] No harm to communities or vulnerable groups?

**Climate:**
- [ ] Compute/token usage proportionate to value delivered? (Not brute-forcing with retries)
- [ ] Waste prevented? (Projects killed before unnecessary code, discovery before delivery)
- [ ] Sustainable resource usage patterns?

- Evidence: [cite specific metrics or observations]

### CALMS Culture Assessment (Willis & Humble)

*CALMS originated as CAMS (Culture, Automation, Measurement, Sharing) coined by Damon Edwards and John Willis at DevOpsDays Mountainview 2010. Jez Humble added the L (Lean) to create CALMS.*

Assess the five cultural dimensions that explain WHY DORA outcomes are what they are:

- [ ] **Culture**: Is there a learning culture? Blameless post-mortems? Psychological safety? Or blame-and-fear?
- [ ] **Automation**: Are repetitive tasks automated (testing, deployment, provisioning)? Or manual and error-prone?
- [ ] **Lean**: Are batch sizes small? WIP limited? Waste actively identified and removed? Or big-batch waterfall?
- [ ] **Measurement**: Are you measuring outcomes (DORA, BVSSH) or outputs (velocity, story points)? Watch for MORF anti-pattern.
- [ ] **Sharing**: Is knowledge shared across teams? Cross-functional collaboration? Or siloed expertise?
- Evidence: [cite specific observations or team feedback]

**Interpreting CALMS with DORA**: DORA tells you WHAT your delivery performance is. CALMS explains WHY. If DORA metrics are poor, CALMS identifies the cultural root cause. If DORA is good but CALMS is weak, the performance is fragile.

## Output

```
## BVSSH Assessment
Date: [date]
Diamond: [ID if applicable]

| Dimension | Status | Trend | Key Evidence |
|-----------|--------|-------|-------------|
| Better | Green/Amber/Red | Improving/Stable/Declining | ... |
| Value | Green/Amber/Red | Improving/Stable/Declining | ... |
| Sooner | Green/Amber/Red | Improving/Stable/Declining | ... |
| Safer | Green/Amber/Red | Improving/Stable/Declining | ... |
| Happier | Green/Amber/Red | Improving/Stable/Declining | ... |

### CALMS Culture Health
| Dimension | Status | Key Signal |
|-----------|--------|-----------|
| Culture | Green/Amber/Red | ... |
| Automation | Green/Amber/Red | ... |
| Lean | Green/Amber/Red | ... |
| Measurement | Green/Amber/Red | ... |
| Sharing | Green/Amber/Red | ... |

Overall: [summary and recommended actions]
```

## Theory Citations
- Smart: Sooner Safer Happier (BVSSH framework)
- Willis & Humble: CALMS (Willis coined CAMS at DevOpsDays 2010, Humble added Lean -- explains WHY DORA outcomes are what they are)
- Forsgren: Accelerate (metrics alignment)
