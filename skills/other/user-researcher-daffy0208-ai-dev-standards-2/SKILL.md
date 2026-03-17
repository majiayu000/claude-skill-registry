---
name: User Researcher
description: Conduct user research and validation. Use when discovering user needs, validating assumptions, creating personas, or understanding pain points. Covers interviews, surveys, analysis, and synthesis.
version: 1.0.0
---

# User Researcher

Understand user needs through systematic research before building products.

## Core Principle

**Users are not you.** Validate assumptions with real user behavior, not opinions or what users say they'll do.

## 5-Phase User Research Process

### Phase 1: Research Planning

**Goal**: Define what you need to learn and how

**Activities**:

- Define research objectives (2-4 key questions to answer)
- Identify target user segments and recruitment criteria
- Select research methods (interviews, surveys, observation)
- Prepare interview guides or survey questions
- Define sample size (5-12 per segment for qualitative)

**Research Questions Examples**:

- What are users' current workflows for [task]?
- What pain points do users experience with [current solution]?
- What motivates users to switch from current solution?
- How do users make decisions about [domain]?

**Validation**:

- [ ] Research objectives documented
- [ ] Target segments defined with criteria
- [ ] Methods selected with protocols ready
- [ ] Stakeholder buy-in obtained

---

### Phase 2: User Recruitment

**Goal**: Find and schedule representative participants

**Recruitment Sources**:

- Existing customers (in-app recruiting, email)
- Prospect lists (sales leads, newsletter subscribers)
- User research platforms (UserTesting, Respondent.io)
- Social media and communities (LinkedIn, Reddit, Slack)
- Referrals from existing participants

**Screening Criteria**:

- Role or job title
- Experience level (novice, intermediate, expert)
- Use case relevance
- Tool stack (current solutions used)
- Willingness to participate (time commitment)

**Compensation**:

- B2B: $75-150 for 30-60 min interview
- B2C: $25-50 for 30-60 min interview
- Gift cards are easier than cash transfers

**Sample Size**:

- Qualitative: 5-12 participants per segment
- Quantitative: 50-100 minimum for statistical significance
- Stop when you reach saturation (no new insights)

**Validation**:

- [ ] 5-12 participants recruited per segment
- [ ] Diverse representation (include edge cases, power users)
- [ ] Sessions scheduled with consent forms sent
- [ ] Compensation method arranged

---

### Phase 3: Data Collection

**Goal**: Gather rich user insights through chosen methods

**User Interviews** (Primary method):

**Interview Structure** (30-60 minutes):

1. **Intro** (5 min): Build rapport, explain purpose
2. **Context** (10 min): Role, current workflow, tools
3. **Deep Dive** (30 min): Pain points, needs, behaviors
4. **Wrap-up** (5 min): Questions, next steps

**Good Interview Questions**:

```
✅ Open-ended:
- "Tell me about the last time you [task]."
- "Walk me through your process for [activity]."
- "What's the most frustrating part of [workflow]?"
- "How do you currently solve [problem]?"

❌ Leading questions (avoid):
- "Would you use a feature that...?" (Everyone says yes)
- "Don't you think it would be better if...?" (Confirming bias)
- "How much would you pay for this?" (Hypothetical)
```

**Ask "Why" Five Times**:

```
User: "I use Excel for tracking leads."
You: "Why Excel specifically?"
User: "It's what I know."
You: "Why is familiarity important?"
User: "Learning new tools takes time."
You: "Why is time a concern?"
User: "I'm measured on closed deals, not tool expertise."
→ Root insight: Avoid tools with steep learning curves
```

**Contextual Inquiry**:

- Observe users in their natural environment
- Watch them complete actual tasks (not simulated)
- Note workarounds, frustrations, and hacks
- Take photos of physical workspace, sticky notes, checklists

**Surveys** (for quantitative validation):

- Use for validating qualitative findings at scale
- Mix closed (rating scales) and open-ended questions
- Keep under 10 questions (completion rate drops fast)
- Target 50-100+ responses for statistical significance

**Validation**:

- [ ] All sessions recorded (with permission)
- [ ] Notes taken during or immediately after
- [ ] Artifacts collected (screenshots, workflows)
- [ ] Early patterns emerging

---

### Phase 4: Analysis & Synthesis

**Goal**: Identify patterns, themes, and insights from raw data

**Affinity Diagramming**:

1. Write each insight on a sticky note
2. Group similar notes together
3. Label groups with themes
4. Look for patterns across groups

**Common Themes to Look For**:

- Pain points (frequent frustrations)
- Workarounds (hacks users created)
- Unmet needs (things users wish existed)
- Behavioral patterns (how users actually work)
- Decision criteria (what influences choices)

**Jobs-to-be-Done (JTBD) Framework**:

```
When [situation],
I want to [motivation],
So I can [expected outcome].

Example:
When preparing for a client meeting,
I want to quickly find all previous conversations,
So I can provide personalized recommendations without looking unprepared.

Analysis:
- Functional job: Find information quickly
- Emotional job: Appear competent
- Social job: Demonstrate attentiveness
```

**User Segmentation** (by behavior, not demographics):

- Power users vs. casual users
- Early adopters vs. late majority
- DIY vs. managed service preference
- Price-sensitive vs. value-focused

**Validation**:

- [ ] Data transcribed and coded
- [ ] Themes identified across participants
- [ ] Patterns validated (not one-off comments)
- [ ] Behavioral segments defined

---

### Phase 5: Research Deliverables

**Goal**: Communicate findings in actionable formats

**1. User Personas** (3-5 evidence-based profiles):

```yaml
persona_name: 'Sarah the Sales Manager'
role: 'Regional Sales Manager'
demographics:
  experience_level: 'Intermediate (5 years)'
  team_size: '12 sales reps'
goals:
  - Track team performance in real-time
  - Coach underperforming reps effectively
pain_points:
  - Data scattered across 3 systems
  - Can't see at-risk deals until too late
current_tools:
  - 'Salesforce: CRM tracking'
  - 'Excel: Custom reports (2 hrs/week)'
behaviors:
  - Checks dashboard first thing every morning
  - Spends 2 hours weekly compiling reports manually
quote: "I feel like I'm flying blind until the end of the quarter"
opportunity: 'Unified dashboard with predictive risk scoring'
```

**2. Journey Maps** (current-state experience):

```
Stages: Awareness → Research → Purchase → Onboarding → Usage → Support

For each stage:
- Actions: What users do
- Pain points: Frustrations and blockers
- Emotions: How users feel (frustrated, confident, confused)
- Opportunities: Where to improve
```

**3. Research Report**:

- Executive summary (1-page findings)
- Methodology (how research was conducted)
- Key insights (5-10 most important findings)
- Supporting quotes (evidence from users)
- Recommendations (what to build or change)
- Appendix (full data, transcripts)

**4. Opportunity Areas** (prioritized problems):

```
| Opportunity | Impact | Effort | Priority |
|-------------|--------|--------|----------|
| Unified dashboard | High | Medium | P0 |
| Predictive alerts | High | High | P1 |
| Mobile access | Medium | Low | P1 |
```

**Validation**:

- [ ] 3-5 personas created with evidence
- [ ] Journey maps show pain points
- [ ] Research report written and shared
- [ ] Opportunities prioritized with team
- [ ] Artifacts stored in shared repository

---

## Key Research Principles

### 1. Observe Behavior, Not Just Words

What users do > what they say they do > what they say they'll do

### 2. Ask "Why" Five Times

Surface root causes and motivations, not symptoms

### 3. Recruit for Diversity

Include edge cases, power users, and struggling users—not just ideal customers

### 4. No Leading Questions

Ask "Tell me about..." not "Would you like..."

### 5. Research is Continuous

Not a one-time phase—continue throughout product lifecycle

### 6. Validate Assumptions Early

Test riskiest assumptions first with minimal investment

---

## Research Methods by Stage

### Exploratory (Early Discovery)

- User interviews: 1-on-1 conversations about context and pain points
- Contextual inquiry: Observe users in natural environment
- Diary studies: Users record experiences over days/weeks

### Evaluative (Testing Ideas)

- Concept testing: Show mockups, gather reactions
- Usability testing: Watch users attempt tasks with prototypes
- A/B testing: Compare variants with real usage data

### Quantitative (Validation at Scale)

- Surveys: Validate findings across larger populations
- Analytics: Track behavior patterns in existing products
- Card sorting: Understand how users categorize information

---

## Common Research Mistakes

❌ **Talking to friends and family** → They'll tell you what you want to hear
❌ **Asking hypothetical questions** → "Would you use...?" is not predictive
❌ **Leading questions** → "Don't you think...?" confirms your bias
❌ **Only talking to early adopters** → They're not representative
❌ **Skipping synthesis** → Raw data isn't insights
❌ **Ignoring negative feedback** → Pay extra attention to criticism
❌ **One-time research** → User needs change, research continuously

---

## Research Outputs Template

```yaml
research_summary:
  objectives:
    - '<key question 1>'
    - '<key question 2>'
  participants:
    total: <number>
    segments:
      - name: '<segment>'
        count: <number>
  methods:
    - 'User interviews (12 participants)'
    - 'Survey (87 responses)'
  key_insights:
    - insight: '<finding>'
      evidence: '<quote or data>'
      impact: 'high/medium/low'
  personas:
    - name: '<persona name>'
      goals: ['<goal>']
      pain_points: ['<pain>']
  opportunities:
    - opportunity: '<problem to solve>'
      impact: 'high'
      effort: 'medium'
      priority: 'P0'
  recommendations:
    - '<action item 1>'
    - '<action item 2>'
```

---

## Related Resources

**Related Skills**:

- `product-strategist` - For validating product-market fit
- `ux-designer` - For creating designs based on research
- `mvp-builder` - For prioritizing features from research

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Research method selection
- `STANDARDS/best-practices/user-research-ethics.md` - Research ethics (when created)

**Related Playbooks**:

- `PLAYBOOKS/conduct-user-interviews.md` - Interview procedure (when created)
- `PLAYBOOKS/synthesize-research-findings.md` - Analysis workflow (when created)
