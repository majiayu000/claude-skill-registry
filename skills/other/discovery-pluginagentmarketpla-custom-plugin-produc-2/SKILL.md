---
name: user-discovery-research
version: "2.0.0"
description: Master user research methodologies, customer interviews, persona development, and journey mapping. Understand customer problems deeply before building.
sasmp_version: "1.3.0"
bonded_agent: 02-discovery-research
bond_type: PRIMARY_BOND
parameters:
  - name: research_type
    type: string
    enum: [interviews, surveys, usability, mixed]
    required: true
  - name: sample_size
    type: number
    default: 20
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# User Discovery & Research Skill

Become an expert at understanding customers deeply. Master interview techniques, extract meaningful insights, create accurate personas, and map customer journeys.

## Interview Mastery

### 30-60 Minute Interview Structure

**Opening (5 min)** - Build rapport
- "Thanks for time. I want to understand your experience with [topic]."
- Warm conversation (not a interrogation)
- Note-taking permission, recording permission

**Context (10 min)** - Background
- "Tell me about your role..."
- "What does a typical day look like?"
- "What tools do you use?"
- "Who do you work with?"

**Deep Dive (15-20 min)** - Core problem
- "Walk me through how you currently [solve X]..."
- "Tell me about the last time [problem] happened..."
- "What frustrates you most about [current solution]?"
- "How often does [issue] occur?"

**Impact Questions (5-10 min)** - Consequence
- "What's the impact when [problem] happens?"
- "How much time do you spend on [workaround]?"
- "What's the cost if [issue] isn't resolved?"

**Exploration (5-10 min)** - Future state
- "What would make your life easier?"
- "Describe your ideal [solution]..."
- "What would you be willing to pay to solve [problem]?"

**Closing (3-5 min)** - Wrap up
- "Is there anything else important?"
- "Can I follow up?"
- "Can you introduce me to others?"

### Interview Techniques

**The Socratic Method**
- Ask questions instead of proposing solutions
- Let them discover insights
- Ask "Why?" 5 times to get root cause
- Example:
  - Q: "Why do you use spreadsheets?"
  - A: "It's what we have"
  - Q: "Why not use a database?"
  - A: "Don't have budget"
  - Q: "Why no budget?"
  - A: "ROI wasn't clear"
  - → Real problem: ROI uncertainty

**Listen 70%, Talk 30%**
- You have two ears, one mouth
- Let silence linger (they fill it)
- Take notes but stay engaged
- Nod and show genuine interest

**Avoid Leading Questions**
- ❌ "Don't you think mobile is important?"
- ✅ "What devices do you primarily use?"
- ❌ "Wouldn't X solve your problem?"
- ✅ "What would an ideal solution look like?"

**Look for Emotions**
- Frustration, excitement, anxiety
- These reveal true pain points
- "I can see this is frustrating. Tell me more..."

### Interview Logistics

**Recruitment:**
- Target: 20-25 interviews minimum
- Mix: power users, light users, non-users
- Incentive: $50-100 or product credit
- Screening: Ensure they fit target segment

**Recording & Notes:**
- Always record (with permission)
- Take live notes (rough OK)
- Timestamps for quotes
- Video is better than audio if possible

**Debrief Immediately:**
- Write key insights within 24 hours
- While memory fresh, fill in gaps
- Highlight best quotes
- Note any bias you notice

## Synthesis & Analysis

### Affinity Mapping

**Process:**
1. Write every quote/insight on sticky note
2. Group similar insights
3. Find themes
4. Rank by frequency/impact
5. Extract top 10-15 themes

**Example themes:**
- Time pressure (everyone mentions)
- Tool switching costs (8 of 20 people)
- Lack of automation (7 of 20 people)
- Data fragmentation (15 of 20 people)

### Persona Development

**5 Element Persona:**

1. **Demographics**
   - Role, company size, industry
   - Education, experience level
   - Geographic location
   - Company revenue/growth stage

2. **Goals & Motivations**
   - What's their job-to-be-done?
   - How is success measured?
   - What drives them?
   - What keeps them up at night?

3. **Challenges & Pain Points**
   - Top 3 problems (research-backed)
   - Current workarounds
   - Cost of problem (time, money, stress)
   - What they've tried

4. **Current Solutions**
   - What tools do they use?
   - How do they work together?
   - What's missing?
   - Tech stack

5. **Quote & Story**
   - Real, powerful quote
   - Day-in-the-life scenario
   - Decision journey story

**Persona Document Format:**
- 1-2 pages max
- Include photo (stock image)
- Real quotes (3-5)
- Scenario/story
- Key behaviors
- Success metrics

## Journey Mapping

### Current State Journey (As-Is)

**Stages:**
1. **Awareness** - Realizes problem exists
2. **Consideration** - Researches solutions
3. **Purchase** - Buys solution
4. **Onboarding** - Learns to use
5. **Usage** - Day-to-day work
6. **Support** - Gets help
7. **Renewal** - Continues or leaves

### For Each Stage Map:

**Actions** - What customer does
- Searches online
- Talks to colleagues
- Evaluates options
- etc.

**Emotions** - How they feel
- Frustrated (searching)
- Cautious (evaluating)
- Confident (purchased)
- Overwhelmed (onboarding)
- etc.

**Touchpoints** - Interactions
- Website
- Sales calls
- Email
- Product UI
- Support chat
- etc.

**Pain Points** - Frustrations
- Hard to find info
- Slow response times
- Confusing UI
- etc.

**Opportunities** - Where you can help
- Better documentation
- Faster support
- Simpler onboarding
- etc.

## Research Methods

### Quantitative

**Surveys**
- Reach: 100+ people
- Speed: 2-3 days
- Depth: Medium
- Best for: Validation, scale

**Net Promoter Score (NPS)**
- "How likely to recommend?" (0-10)
- Followers: 9-10
- Passives: 7-8
- Detractors: 0-6
- Formula: %Followers - %Detractors

### Qualitative

**Interviews**
- Reach: 15-25 people
- Speed: 2-3 weeks
- Depth: Very high
- Best for: Understanding "why"

**Focus Groups**
- Reach: 8-12 people
- Speed: 1-2 weeks
- Depth: High
- Bonus: Group dynamic reveals thinking

**Observations**
- Reach: 3-5 people
- Speed: 2-3 days
- Depth: Very high
- Best for: Seeing vs. hearing

### Mixed Methods

**Combine research methods:**
- Start with interviews (understand why)
- Then survey (validate with 100+)
- Iterate based on findings

## Key Insights Extraction

### Five Key Metrics

1. **Problem Severity**
   - How badly does it hurt?
   - Frequency of problem
   - Impact magnitude
   - Urgency to solve

2. **Current Solution Satisfaction**
   - Is current approach acceptable?
   - What's missing?
   - Workarounds needed?
   - Would switch if better option?

3. **Willingness to Pay**
   - What would they pay for solution?
   - Price sensitivity?
   - ROI expectations?

4. **Decision Making**
   - Who decides?
   - Who influences?
   - Budget process?
   - Timeline?

5. **Switching Costs**
   - What prevents switching?
   - Integration challenges?
   - Learning curve acceptable?
   - Migration effort?

### Top 5 Questions to Answer

From your research:
1. What's the #1 problem?
2. Who has the problem most acutely?
3. How do they solve it today?
4. What would ideal solution look like?
5. Would they pay for it, and how much?

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Düşük interview katılımı | Yanlış incentive | $50-100 gift card |
| Yüzeysel insights | Leading questions | "Why?" 5x sor |
| Conflicting feedback | Mixed segments | Segment-based analysis |
| Persona generic | Insufficient data | +10 interview |

### Debug Checklist

```
[ ] Sample size yeterli mi? (min 15-20)
[ ] Questions leading değil mi?
[ ] Recording consent alındı mı?
[ ] Synthesis 24h içinde yapıldı mı?
[ ] Bias check yapıldı mı?
```

### Recovery Procedures

1. **Low Participation** → Adjust incentive or channel
2. **Conflicting Data** → Segment by user type
3. **Interviewer Bias** → Add second interviewer

---

**Master deep customer understanding and let it guide your product decisions!**
