---
name: faion-researcher
description: "Researcher role: idea generation (SCAMPER, mind maps), market research, competitor analysis, persona building, pricing research, problem validation, niche evaluation, project naming, trend analysis. 9 research modes."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite
---

# Research Domain Skill

**Communication: User's language. Docs: English.**

## Purpose

Orchestrate all research and discovery activities for product/startup development. This domain skill combines idea discovery, product research, and project naming into a unified research workflow.

---

## Agents (2)

| Agent | Model | Purpose | Modes |
|-------|-------|---------|-------|
| faion-research-agent | opus | Research orchestrator | ideas, market, competitors, pains, personas, validate, niche, pricing, names |
| faion-domain-checker-agent | sonnet | Domain availability verification | — |

**Mode Mapping:**
| Mode | Replaces | Output |
|------|----------|--------|
| ideas | faion-research-agent (mode: ideas) | 15-20 candidates |
| market | faion-research-agent (mode: market) | market-research.md |
| competitors | faion-research-agent (mode: competitors) | competitive-analysis.md |
| pains | faion-research-agent (mode: pains) | pain-points.md |
| personas | faion-research-agent (mode: personas) | user-personas.md |
| validate | faion-research-agent (mode: validate) | problem-validation.md |
| niche | faion-research-agent (mode: niche) | niche-evaluation.md |
| pricing | faion-research-agent (mode: pricing) | pricing-research.md |
| names | faion-research-agent (mode: names) | name-candidates.md |

---

## Methodologies (20)

This skill references 20 research methodologies:

| # | Methodology | Description | Agent (Mode) |
|---|-------------|-------------|--------------|
| M-RES-001 | 7 Ps of Ideation | Pain, Passion, Profession, Process, Platform, People, Product | faion-research-agent (ideas) |
| M-RES-002 | Paul Graham Questions | Tedious tasks, surprisingly hard, build for self | faion-research-agent (ideas) |
| M-RES-003 | Personal Pain Points | Daily problems, complaints, workarounds | faion-research-agent (ideas) |
| M-RES-004 | Idea Scoring Matrix | Multi-criteria scoring (market, competition, fit) | faion-research-agent (niche) |
| M-RES-005 | TAM/SAM/SOM Analysis | Total, Serviceable, Obtainable market sizing | faion-research-agent (market) |
| M-RES-006 | Market Trend Analysis | Industry trends, growth drivers, threats | faion-research-agent (market) |
| M-RES-007 | Competitive Landscape Mapping | Direct, indirect, substitute competitors | faion-research-agent (competitors) |
| M-RES-008 | Feature Gap Analysis | Missing features in competitor products | faion-research-agent (competitors) |
| M-RES-009 | Pricing Benchmarking | Competitor pricing models comparison | faion-research-agent (pricing) |
| M-RES-010 | Jobs To Be Done (JTBD) | Functional, emotional, social jobs | faion-research-agent (personas) |
| M-RES-011 | User Persona Creation | Demographics, behaviors, pain points, goals | faion-research-agent (personas) |
| M-RES-012 | Problem Validation | Evidence gathering for problem existence | faion-research-agent (validate) |
| M-RES-013 | Pain Point Mining | Reddit, forums, reviews, social listening | faion-research-agent (pains) |
| M-RES-014 | Niche Viability Scoring | 5-criteria scoring (market, competition, barriers, profit, fit) | faion-research-agent (niche) |
| M-RES-015 | Blue Ocean Strategy | Uncontested market space identification | faion-research-agent (niche) |
| M-RES-016 | Value Proposition Canvas | Customer profile vs. value map | faion-research-agent (personas) |
| M-RES-017 | Project Naming Strategies | Descriptive, invented, compound, metaphor, portmanteau | faion-research-agent (names) |
| M-RES-018 | Domain Availability Check | .com, .io, .co, social handles | faion-domain-checker-agent |
| M-RES-019 | Pricing Model Selection | Freemium, subscription, one-time, usage-based | faion-research-agent (pricing) |
| M-RES-020 | Customer Interview Framework | Discovery interviews, problem interviews | faion-research-agent (validate) |


> **Note:** Full methodology details available in `methodologies/` folder.

---

## Section 1: Idea Discovery

### Workflow

```
1. Gather Context (AskUserQuestion)
   - Skills, interests, resources
   ↓
2. Generate Ideas (faion-research-agent mode: ideas)
   - Apply 7 Ps framework + other methods
   ↓
3. User Selection (AskUserQuestion)
   - Pick 3-5 ideas to research
   ↓
4. Pain Point Research (faion-research-agent mode: pains)
   - Reddit, forums, reviews mining
   ↓
5. Niche Evaluation (faion-research-agent mode: niche)
   - Market size, competition, barriers
   ↓
6. Present Results
   ↓
   User selects idea? → YES → Write to product_docs/idea-validation.md
                     → NO  → Loop back to step 2
```

### Phase 1: Gather Context

Use AskUserQuestion:

```
Question 1: "What are your skills/experience?"
Options:
- Software development
- Design/UX
- Marketing/Sales
- Domain expertise (specific industry)

Question 2: "What motivates you?"
Options:
- Solve my own problem
- Big market opportunity
- Passion project
- Side income

Question 3: "How much time can you invest?"
Options:
- Nights & weekends (side project)
- Part-time (20h/week)
- Full-time
```

### Phase 2: Generate Ideas

Call faion-research-agent (mode: ideas) agent:

```python
Task(
    subagent_type="faion-research-agent (mode: ideas)",
    prompt=f"""Generate startup ideas for:
    Skills: {skills}
    Motivation: {motivation}
    Time commitment: {time}

    Use frameworks: 7 Ps, Paul Graham, Personal Pain Points
    Generate 15-20 ideas across categories.
    """,
    description="Generate startup ideas"
)
```

### Phase 3: User Selection

Present ideas grouped by category. Use AskUserQuestion:

```
Question: "Which ideas do you want to research deeper?"
multiSelect: true
Options:
- {idea1} - {category}
- {idea2} - {category}
- {idea3} - {category}
- {idea4} - {category}
- "None, generate different ones"
```

### Phase 4: Pain Point Research

For each selected idea, call faion-research-agent (mode: pains):

```python
Task(
    subagent_type="faion-research-agent (mode: pains)",
    prompt=f"""Research pain points for: {idea}

    Search:
    - Reddit complaints: "problem with {keyword}" site:reddit.com
    - Forum discussions: "{keyword} frustrating" OR "{keyword} hate"
    - App store reviews: "{competitor} review" 1-star

    Find: frequency, intensity, existing solutions, gaps
    """,
    description="Research pain points"
)
```

### Phase 5: Niche Evaluation

For ideas with validated pain points, call faion-research-agent (mode: niche):

```python
Task(
    subagent_type="faion-research-agent (mode: niche)",
    prompt=f"""Evaluate niche for: {idea}

    Criteria:
    - Market size (TAM/SAM/SOM estimates)
    - Competition level (red/blue ocean)
    - Entry barriers (technical, regulatory, capital)
    - Profitability potential (unit economics)
    - Your fit (skills match)

    Score each 1-10, provide total score.
    """,
    description="Evaluate niche viability"
)
```

### Phase 6: Present Results & Decision

Show evaluation results. Use AskUserQuestion:

```
Question: "Evaluation results. What's next?"
Options:
- {idea1} (score: 42/50) - select for development
- {idea2} (score: 38/50) - select for development
- Generate new ideas
- Research other niches for {ideaX}
```

### Phase 7: Write to Documentation

When user selects idea, create `aidocs/sdd/{project}/product_docs/idea-validation.md`:

```markdown
# Idea Validation: {idea_name}

## Summary
- **Problem:** {pain point}
- **Solution:** {proposed solution}
- **Target audience:** {who}

## Pain Point Evidence
- Source 1: {quote, link}
- Source 2: {quote, link}

## Niche Evaluation
| Criterion | Score | Notes |
|-----------|-------|-------|
| Market size | X/10 | {notes} |
| Competition | X/10 | {notes} |
| Barriers | X/10 | {notes} |
| Profitability | X/10 | {notes} |
| Fit | X/10 | {notes} |
| **Total** | **XX/50** | |

## Next Steps
- [ ] Customer interviews
- [ ] MVP definition
- [ ] Create spec.md
```

### 7 Ps of Ideation Framework

| P | Question | Example |
|---|----------|---------|
| **Pain** | What frustrates you daily? | Scheduling meetings across timezones |
| **Passion** | What do you love doing? | Teaching coding to kids |
| **Profession** | What's broken in your industry? | Medical billing complexity |
| **Process** | What workflow is inefficient? | Code review bottlenecks |
| **Platform** | What can be improved on existing platform? | Better Slack integrations |
| **People** | Who do you know with problems? | Freelancers need invoicing |
| **Product** | What product do you wish existed? | AI meeting summarizer |

### Paul Graham's Questions

- What's tedious but necessary?
- What's surprisingly hard to do?
- What do you find yourself building for yourself?
- What would you pay for that doesn't exist?

### Personal Pain Points

- Problems you face daily
- Complaints you make often
- Workarounds you've built
- Tools you wish were better

### Niche Evaluation Criteria

| Criterion | 1-3 | 4-6 | 7-10 |
|-----------|-----|-----|------|
| **Market size** | <$10M | $10M-100M | >$100M |
| **Competition** | Red ocean | Moderate | Blue ocean |
| **Barriers** | High (capital, regulatory) | Medium | Low |
| **Profitability** | Thin margins | Ok margins | High margins |
| **Fit** | No relevant skills | Some skills | Perfect match |

**Total score interpretation:**
- 40-50: Excellent opportunity
- 30-39: Good potential
- 20-29: Proceed with caution
- <20: Consider other ideas

---

## Section 2: Product Research

### Workflow

```
1. Parse project from ARGUMENTS
2. Read: constitution.md, roadmap.md
3. AskUserQuestion: modules + mode (quick/deep)
4. Run agents SEQUENTIALLY (not parallel)
5. Write executive-summary.md
```

### Module Selection

```python
AskUserQuestion(
    questions=[{
        "question": "Which modules to run?",
        "multiSelect": True,
        "options": [
            {"label": "Market Research", "description": "TAM/SAM/SOM, trends"},
            {"label": "Competitors", "description": "Features, pricing"},
            {"label": "Personas", "description": "Pain points, JTBD"},
            {"label": "Validation", "description": "Problem evidence"},
            {"label": "Pricing", "description": "Benchmarks"}
        ]
    }]
)
```

### Execution

```python
AGENTS = {
    "market": "faion-research-agent (mode: market)",
    "competitors": "faion-research-agent (mode: competitors)",
    "personas": "faion-research-agent (mode: personas)",
    "validation": "faion-research-agent (mode: validate)",
    "pricing": "faion-research-agent (mode: pricing)"
}

for module in selected_modules:
    Task(
        subagent_type=AGENTS[module],
        prompt=f"""
PROJECT: {project}
PRODUCT: {product_description}
MODE: {quick|deep}
OUTPUT: aidocs/sdd/{project}/product_docs/{output_file}
"""
    )
```

### Output Structure

```
aidocs/sdd/{project}/product_docs/
├── market-research.md
├── competitive-analysis.md
├── user-personas.md
├── problem-validation.md
├── pricing-research.md
├── executive-summary.md
└── gtm-manifest/              # Optional, after research complete
    └── gtm-manifest-full.md
```

### Market Research Output Template

```markdown
# Market Research: {project}

## TAM (Total Addressable Market)
- Global market size: ${X}B
- Growth rate: X% CAGR
- Source: {citation}

## SAM (Serviceable Addressable Market)
- Geographic focus: {regions}
- Segment focus: {segments}
- SAM estimate: ${X}M

## SOM (Serviceable Obtainable Market)
- Year 1 realistic target: ${X}M
- Key assumptions: {list}

## Market Trends
1. Trend 1: {description}
2. Trend 2: {description}
3. Trend 3: {description}

## Drivers & Threats
| Drivers | Threats |
|---------|---------|
| {driver1} | {threat1} |
| {driver2} | {threat2} |
```

### Competitor Analysis Output Template

```markdown
# Competitive Analysis: {project}

## Competitive Landscape

| Competitor | Type | Founded | Funding | Pricing |
|------------|------|---------|---------|---------|
| {name1} | Direct | {year} | ${X}M | {pricing} |
| {name2} | Indirect | {year} | ${X}M | {pricing} |

## Feature Comparison

| Feature | Us | Comp1 | Comp2 | Comp3 |
|---------|----|----|----|----|
| {feature1} | Y | Y | N | Y |
| {feature2} | Y | N | Y | N |

## Gap Analysis
- Gap 1: {description}
- Gap 2: {description}

## Positioning Strategy
{how to differentiate}
```

### Persona Output Template

```markdown
# User Personas: {project}

## Persona 1: {name}

### Demographics
- Age: {range}
- Role: {job title}
- Income: ${range}
- Location: {regions}

### Behaviors
- {behavior1}
- {behavior2}

### Pain Points
1. {pain1}
2. {pain2}
3. {pain3}

### Goals
- {goal1}
- {goal2}

### Jobs To Be Done
- Functional: {job}
- Emotional: {job}
- Social: {job}
```

### Research Modes

| Mode | Searches | Depth |
|------|----------|-------|
| Quick | 3-5 | Surface-level trends |
| Deep | 8-12 | Detailed analysis |

### Rules

- Run agents ONE BY ONE
- Agents cite sources with URLs
- If data not found → "Data not available"
- Quick: 3-5 searches, Deep: 8-12 searches

---

## Section 3: Project Naming

### Workflow

```
GATHER CONCEPT → GENERATE NAMES → USER SELECTS → CHECK DOMAINS → PRESENT RESULTS → WRITE TO CONSTITUTION
     ↑                                                               ↓
     └───────────────── Loop if user wants more ─────────────────────┘
```

### Phase 1: Gather Concept

AskUserQuestion: description, tone (Professional/Playful/Technical/Premium)

Extract: product type, benefits, audience, constraints

### Phase 2: Generate Names (15-20 candidates)

**Naming Strategies:**

| Strategy | Description | Example |
|----------|-------------|---------|
| Descriptive | What it does | DropBox |
| Invented | Made-up word | Spotify |
| Compound | Two words | Facebook |
| Metaphor | Symbolic meaning | Amazon |
| Portmanteau | Blended words | Pinterest |
| Alliteration | Same sound | PayPal |
| Acronym | Letter combination | IBM |

Call `faion-research-agent (mode: names)` agent with context + rejected names.

### Phase 3: User Selection

AskUserQuestion (multiSelect): show names, allow "generate more"

If "generate more" → add to rejected, loop to Phase 2.

### Phase 4: Check Selected

Call `faion-domain-checker-agent` for:
- .com availability
- .io availability
- .co availability
- GitHub username
- Twitter/X handle

### Phase 5: Present Results

AskUserQuestion: "{name} - select as final" or "generate more"

If final selected → Phase 6. Else → loop to Phase 2.

### Phase 6: Write to Constitution

Update `aidocs/sdd/{project}/constitution.md`:

```markdown
## Project Identity
- **Name:** {name}
- **Domain:** {name}.com
```

Confirm with next steps: register domain, create GitHub, claim Twitter.

### Name Scoring

| Factor | Points |
|--------|--------|
| .com available | 10 |
| .io available | 5 |
| No trademark | 5 |
| GitHub available | 3 |
| Twitter available | 3 |
| Easy to spell | 2 |
| **Max Total** | **28** |

---

## Error Handling

| Error | Action |
|-------|--------|
| No ideas resonate | Try different framework, ask about hobbies |
| No pain points found | Broaden search, try adjacent problems |
| High competition | Look for underserved segment |
| User rejects all ideas | Generate more with different angle |
| All .com taken | Suggest .io, check premium domains |
| Trademark conflict | Remove name, note reason |
| Data not found | Mark as "Data not available", continue |

---

## Integration

### Entry Point

This skill is invoked via `/faion-net` command when user intent is research-related:

```python
# Intent detection
if intent in ["idea", "research", "market", "competitors", "naming", "personas", "pricing"]:
    invoke("faion-research-domain-skill")
```

### Next Steps After Research

After research complete, offer:
- "Create GTM Manifest?" → Call `faion-marketing-domain-skill`
- "Create spec.md?" → Call `faion-sdd-domain-skill`
- "Start development?" → Call `faion-development-domain-skill`

---

## Output Files

| Module | Output File |
|--------|-------------|
| Idea Discovery | `product_docs/idea-validation.md` |
| Market Research | `product_docs/market-research.md` |
| Competitors | `product_docs/competitive-analysis.md` |
| Personas | `product_docs/user-personas.md` |
| Validation | `product_docs/problem-validation.md` |
| Pricing | `product_docs/pricing-research.md` |
| Summary | `product_docs/executive-summary.md` |
| Naming | Updates `constitution.md` |

---

## Quick Reference

### Invoke Idea Discovery
```python
Task(
    subagent_type="faion-research-agent (mode: ideas)",
    prompt="Generate ideas using 7 Ps framework"
)
```

### Invoke Market Research
```python
Task(
    subagent_type="faion-research-agent (mode: market)",
    prompt="Research TAM/SAM/SOM for {product}"
)
```

### Invoke Competitor Analysis
```python
Task(
    subagent_type="faion-research-agent (mode: competitors)",
    prompt="Analyze competitors for {product}"
)
```

### Invoke Persona Building
```python
Task(
    subagent_type="faion-research-agent (mode: personas)",
    prompt="Create personas using JTBD for {product}"
)
```

### Invoke Naming
```python
Task(
    subagent_type="faion-research-agent (mode: names)",
    prompt="Generate names for {product_description}"
)
```

---

---

# Methodologies Reference (Detailed)

## M-RES-001: 7 Ps of Ideation

### Problem
Aspiring entrepreneurs struggle to find viable startup ideas that match their skills and interests.

### Framework

| P | Question | Exploration |
|---|----------|-------------|
| **Pain** | What frustrates you daily? | List 5 daily annoyances, rate severity 1-10 |
| **Passion** | What do you love doing? | Activities you'd do for free, hobbies |
| **Profession** | What's broken in your industry? | Insider knowledge of inefficiencies |
| **Process** | What workflow is inefficient? | Tasks taking 10x longer than needed |
| **Platform** | What can be improved on existing platform? | Missing integrations, poor UX |
| **People** | Who do you know with problems? | Friends, family, colleagues complaints |
| **Product** | What product do you wish existed? | Tools you'd pay for immediately |

**Scoring:**
- For each P, generate 3-5 ideas
- Score each: Market size (1-5) + Your fit (1-5) + Urgency (1-5)
- Top 3 scores proceed to validation

### Templates

**Ideation Worksheet:**
```markdown
## Pain Ideas
1. {idea} - Score: {X}/15 - Notes: {why interesting}
2. {idea} - Score: {X}/15

## Passion Ideas
1. {idea} - Score: {X}/15

## Profession Ideas
1. {idea} - Score: {X}/15
...

## Top 3 to Validate
1. {idea} from {P} - Total: {X}/15
2. {idea} from {P} - Total: {X}/15
3. {idea} from {P} - Total: {X}/15
```

### Examples

| P | Example Idea | Score |
|---|--------------|-------|
| Pain | Meeting scheduling across timezones | 12/15 |
| Passion | Teaching coding to kids | 9/15 |
| Profession | Medical billing automation | 14/15 |

### Agent
faion-research-agent (mode: ideas)

---

## M-RES-002: Paul Graham Questions

### Problem
Entrepreneurs miss obvious opportunities hiding in plain sight.

### Framework

**4 Questions:**
1. **What's tedious but necessary?**
   - Tasks everyone hates but must do
   - High frequency, low satisfaction

2. **What's surprisingly hard to do?**
   - Should be simple but isn't
   - Indicates market failure

3. **What do you find yourself building for yourself?**
   - Personal tools that could scale
   - Validates genuine need

4. **What would you pay for that doesn't exist?**
   - Identifies willingness to pay
   - Validates business model

**Exploration Process:**
1. Spend 30 min per question
2. Write stream-of-consciousness
3. Circle recurring themes
4. Cross-reference with daily activities

### Templates

**PG Questions Journal:**
```markdown
## Question 1: Tedious but Necessary
### List
- Expense reports
- Code reviews
- Meeting scheduling
- ...

### Themes
- Administrative overhead
- Communication friction

### Top Ideas
- Automated expense categorization
- AI code review assistant
```

### Examples

**Successful Companies from PG Questions:**
- Dropbox: "Sync files is tedious" → Tedious but necessary
- Stripe: "Payments are hard" → Surprisingly hard
- Notion: "I built my own wiki" → Built for yourself

### Agent
faion-research-agent (mode: ideas)

---

## M-RES-003: Personal Pain Points

### Problem
Entrepreneurs overlook problems they face daily because they've normalized them.

### Framework

**Mining Techniques:**

1. **Complaint Audit** (1 week)
   - Log every complaint you make
   - Note frequency and intensity
   - Categorize: work, personal, tools

2. **Workaround Inventory**
   - List all workarounds you've built
   - Spreadsheets, scripts, processes
   - Time spent maintaining them

3. **Tool Stack Analysis**
   - List all tools you use
   - Rate satisfaction 1-5
   - Identify gaps between tools

4. **Time Tracker**
   - Track where time goes for 3 days
   - Identify time sinks
   - Calculate cost of inefficiency

**Scoring:**
| Factor | Weight |
|--------|--------|
| Frequency | 30% |
| Intensity | 30% |
| Current solutions | 20% |
| Your ability to solve | 20% |

### Templates

**Pain Point Log:**
```markdown
| Date | Complaint | Category | Freq | Intensity | Notes |
|------|-----------|----------|------|-----------|-------|
| 01/18 | Can't find file | Tools | Daily | 7/10 | Slack + Drive + Email |
| 01/18 | Meeting ran over | Work | Weekly | 5/10 | No time boundaries |
```

### Examples

- "I can never find that one Slack message" → Search tool idea
- "Updating all docs after API change" → Auto-sync documentation
- "Switching between 10 tabs" → Dashboard aggregator

### Agent
faion-research-agent (mode: ideas)

---

## M-RES-004: Idea Scoring Matrix

### Problem
Too many ideas, no objective way to prioritize.

### Framework

**Scoring Dimensions:**

| Dimension | 1-2 | 3-4 | 5 |
|-----------|-----|-----|---|
| **Market Size** | <$10M | $10M-$100M | >$100M |
| **Competition** | Red ocean, 10+ | Moderate, 3-10 | Blue ocean, <3 |
| **Barriers** | High (capital, regulatory) | Medium | Low |
| **Monetization** | Unclear | Possible | Obvious |
| **Your Fit** | No relevant skills | Some skills | Perfect match |

**Process:**
1. Score each idea 1-5 on all dimensions
2. Weight dimensions (optional)
3. Calculate total (max 25)
4. Rank ideas

**Decision Thresholds:**
- 20-25: Strong proceed
- 15-19: Proceed with caution
- 10-14: Needs pivot
- <10: Pass

### Templates

**Scoring Matrix:**
```markdown
| Idea | Market | Competition | Barriers | Monetization | Fit | Total |
|------|--------|-------------|----------|--------------|-----|-------|
| A | 4 | 3 | 4 | 5 | 4 | 20 |
| B | 5 | 2 | 3 | 4 | 3 | 17 |
| C | 3 | 4 | 5 | 3 | 5 | 20 |
```

### Examples

**SaaS Idea Scored:**
- Market: $500M (5)
- Competition: 5 competitors (3)
- Barriers: Technical only (4)
- Monetization: SaaS model (5)
- Fit: Developer background (4)
- **Total: 21/25 → Strong proceed**

### Agent
faion-research-agent (mode: niche)

---

## M-RES-005: TAM/SAM/SOM Analysis

### Problem
Entrepreneurs can't quantify market opportunity or set realistic targets.

### Framework

**Definitions:**
- **TAM** (Total Addressable Market): Everyone who could buy
- **SAM** (Serviceable Addressable Market): Those you can reach
- **SOM** (Serviceable Obtainable Market): Realistic Year 1 target

**Calculation Methods:**

1. **Top-Down:**
   - Start with industry reports
   - Apply filters (geography, segment)
   - Risk: Often inflated

2. **Bottom-Up:**
   - Count potential customers
   - Multiply by price point
   - Risk: May miss segments

3. **Value Theory:**
   - Calculate value created
   - Apply capture rate (1-10%)
   - Most defensible

**SOM Reality Check:**
- Typical SOM = 1-5% of SAM in Year 1
- With unfair advantage: 5-10%
- With viral growth: 10-20%

### Templates

**Market Sizing:**
```markdown
## TAM
- Global market: $XX billion
- Growth: X% CAGR
- Source: {report name}

## SAM
- Geographic focus: {regions}
- Segment focus: {segments}
- SAM = $XX million

## SOM (Year 1)
- Target customers: X
- Average revenue: $Y
- SOM = $Z million
- % of SAM: X%

## Assumptions
1. {assumption 1}
2. {assumption 2}
```

### Examples

**HR SaaS:**
- TAM: $30B (global HR software)
- SAM: $500M (US SMB HR)
- SOM: $2M (500 customers x $4K)
- SOM % of SAM: 0.4%

### Agent
faion-research-agent (mode: market)

---

## M-RES-006: Market Trend Analysis

### Problem
Entrepreneurs miss timing opportunities or build for declining markets.

### Framework

**Trend Categories:**

| Category | Timeframe | Examples |
|----------|-----------|----------|
| Macro | 5-10 years | AI adoption, remote work |
| Industry | 2-5 years | No-code tools, creator economy |
| Micro | 6-24 months | Specific tech adoption |

**Analysis Framework:**

1. **Growth Drivers**
   - What accelerates this trend?
   - Technology, regulation, demographics

2. **Adoption Curve**
   - Where are we? (Innovators → Early Adopters → Majority)
   - Sweet spot: Early Majority

3. **Threats**
   - What could reverse this trend?
   - Competition, regulation, substitutes

4. **Timing Assessment**
   - Too early: Education cost too high
   - Just right: Market aware, solutions emerging
   - Too late: Established winners

### Templates

**Trend Analysis:**
```markdown
## Trend: {Name}

### Overview
- Stage: {Emerging | Growing | Mature | Declining}
- Growth rate: X% annually
- Market size: $X billion

### Drivers
1. {driver} - Impact: High/Medium/Low
2. {driver} - Impact: High/Medium/Low

### Threats
1. {threat} - Likelihood: High/Medium/Low
2. {threat} - Likelihood: High/Medium/Low

### Timing Assessment
- Current stage: Early Majority
- Window: 2-3 years
- Recommendation: {proceed/wait/pivot}
```

### Examples

**AI Coding Assistants (2026):**
- Stage: Early Majority
- Growth: 45% CAGR
- Window: Now optimal
- Threat: Large players (GitHub, OpenAI)

### Agent
faion-research-agent (mode: market)

---

## M-RES-007: Competitive Landscape Mapping

### Problem
Entrepreneurs underestimate competition or miss indirect competitors.

### Framework

**Competitor Types:**

| Type | Definition | Example |
|------|------------|---------|
| Direct | Same solution, same customer | Slack vs Teams |
| Indirect | Different solution, same problem | Slack vs Email |
| Substitute | Alternative approach entirely | Slack vs In-person |
| Potential | Could enter market | Apple into wearables |

**Mapping Process:**

1. **Identify all competitors** (aim for 15-20)
2. **Categorize by type**
3. **Assess each:**
   - Founded, funding, team size
   - Pricing model
   - Key features
   - Positioning

4. **Plot on matrix:**
   - X-axis: Price (low → high)
   - Y-axis: Features (simple → complex)

5. **Find whitespace**

### Templates

**Competitive Landscape:**
```markdown
## Direct Competitors

| Name | Founded | Funding | Pricing | Differentiator |
|------|---------|---------|---------|----------------|
| {name} | 2020 | $10M | $99/mo | Feature X |
| {name} | 2018 | $50M | $199/mo | Enterprise |

## Indirect Competitors

| Name | How they compete | Weakness |
|------|-----------------|----------|
| {name} | {explanation} | {gap} |

## Market Position Map

```
High Price
    │
    │     [Enterprise A]
    │                      [Our opportunity]
    │  [Competitor B]
    │
Low Price ────────────────────── High Features
```

## Whitespace Identified
- {gap 1}: {description}
- {gap 2}: {description}
```

### Examples

**Project Management Tools:**
- Direct: Asana, Monday, ClickUp
- Indirect: Spreadsheets, Slack, Email
- Whitespace: AI-native PM for solopreneurs

### Agent
faion-research-agent (mode: competitors)

---

## M-RES-008: Feature Gap Analysis

### Problem
Entrepreneurs don't know which features are missing in the market.

### Framework

**Analysis Process:**

1. **Feature Inventory**
   - List all features across top 5 competitors
   - Categorize: Core, Differentiator, Nice-to-have

2. **Feature Matrix**
   - Competitors as columns
   - Features as rows
   - Mark: Has (Y), Partial (P), Missing (N)

3. **Gap Identification**
   - Features no one has
   - Features only 1-2 have (opportunity)
   - Features everyone has (table stakes)

4. **Gap Validation**
   - Is this gap intentional (hard, unprofitable)?
   - Do customers want it? (check reviews)
   - Can we build it better?

### Templates

**Feature Matrix:**
```markdown
| Feature | Us | Comp A | Comp B | Comp C | Gap? |
|---------|-------|--------|--------|--------|------|
| Core 1 | Y | Y | Y | Y | No (table stakes) |
| Core 2 | Y | Y | P | Y | No |
| Diff 1 | Y | N | N | P | Yes - Opportunity |
| Diff 2 | P | Y | Y | N | Build out |
| Nice 1 | N | N | N | N | Validate demand |
```

**Gap Validation:**
```markdown
## Gap: {Feature Name}

### Evidence
- Reviews mentioning need: X
- Forum discussions: X links
- Search volume: X/month

### Why Competitors Don't Have It
- {reason}: Technical difficulty / Low priority / Not aware

### Our Advantage
- {why we can build it}

### Recommendation
- Pursue / Investigate / Skip
```

### Examples

**Email Marketing Tools Gap:**
- Gap: Native A/B testing for subject lines
- Evidence: 50+ feature requests in Mailchimp community
- Why missing: Requires ML infrastructure
- Our advantage: Have ML expertise

### Agent
faion-research-agent (mode: competitors)

---

## M-RES-009: User Interviews

### Problem
Entrepreneurs build based on assumptions rather than validated user needs.

### Framework

**Interview Types:**

| Type | When | Goal | Questions |
|------|------|------|-----------|
| Problem | Early | Validate problem exists | Open-ended exploration |
| Solution | After problem validated | Test solution fit | Prototype feedback |
| Usability | With prototype | Test UX | Task-based |

**Interview Structure (45 min):**
1. Warm-up (5 min): Build rapport
2. Current state (10 min): How do they do it today?
3. Pain exploration (15 min): What's frustrating?
4. Solution probing (10 min): Would X help?
5. Wrap-up (5 min): Would they pay? Referrals?

**Golden Rules:**
- Talk less than 20% of the time
- Never pitch, only probe
- Ask about past behavior, not future intent
- Look for emotion (frustration, excitement)

**Sample Questions:**
- "Tell me about the last time you [problem]..."
- "What did you try? What happened?"
- "On a scale of 1-10, how frustrating is this?"
- "How much time/money does this cost you?"

### Templates

**Interview Script:**
```markdown
## Warm-up
"Thanks for joining. I'm researching [topic]. No sales pitch, just learning."

## Current State
"Walk me through how you currently [task]."
"What tools do you use?"
"How often do you do this?"

## Pain Exploration
"What's the most frustrating part?"
"Tell me about the last time it went wrong."
"What workarounds have you tried?"

## Solution Probing (show concept/prototype)
"Would something like this help?"
"What's missing?"
"Would you pay for this? How much?"

## Wrap-up
"Who else should I talk to?"
"Can I follow up in 2 weeks?"
```

### Examples

**Key Insights from 10 Interviews:**
- 8/10 mentioned same frustration
- Average time wasted: 3 hours/week
- Willingness to pay: $50-100/month
- Quote: "I would kill for this solution"

### Agent
faion-research-agent (mode: validate)

---

## M-RES-010: Jobs To Be Done (JTBD)

### Problem
Features don't connect to real user motivations.

### Framework

**JTBD Statement:**
```
When I [situation/trigger],
I want to [motivation/action],
So I can [expected outcome/benefit].
```

**Job Dimensions:**

| Dimension | Question | Example |
|-----------|----------|---------|
| Functional | What task? | Send invoice |
| Emotional | How feel? | Confident, professional |
| Social | How perceived? | Reliable, organized |

**Job Mapping Process:**
1. Identify situation triggers
2. Map functional jobs
3. Uncover emotional jobs (harder)
4. Discover social jobs (hardest)
5. Prioritize by frequency + importance

**Hiring/Firing Framework:**
- Why do customers "hire" solutions?
- Why do they "fire" (abandon) solutions?
- What makes them switch?

### Templates

**JTBD Canvas:**
```markdown
## Job: {Name}

### Situation/Trigger
When I {situation}...

### Functional Job
I want to {action}...

### Emotional Job
So I can feel {emotion}...

### Social Job
And be seen as {perception}...

### Current Solutions
- {solution 1}: Hired because {reason}, fired because {reason}
- {solution 2}: Hired because {reason}, fired because {reason}

### Our Opportunity
We can {do X better} by {approach}
```

### Examples

**Invoicing Software JTBD:**
- Situation: When I finish a project for a client
- Functional: I want to send a professional invoice quickly
- Emotional: So I can feel confident I'll get paid
- Social: And be seen as a legitimate business

### Agent
faion-research-agent (mode: personas)

---

## M-RES-011: User Persona Creation

### Problem
Teams build for abstract "users" rather than specific people with distinct needs.

### Framework

**Persona Components:**

| Component | Description | Source |
|-----------|-------------|--------|
| Demographics | Age, role, income, location | Analytics, surveys |
| Behaviors | Tools used, habits, workflows | Interviews, observation |
| Pain Points | Top 3-5 frustrations | Interviews, support tickets |
| Goals | What success looks like | Interviews |
| Quote | Representative statement | Verbatim from interview |

**Persona Types:**

| Type | Priority | Focus |
|------|----------|-------|
| Primary | 1 | Design for this person |
| Secondary | 2 | Consider their needs |
| Negative | Exclude | Explicitly not for them |

**Creation Process:**
1. Conduct 5-10 user interviews
2. Identify patterns (cluster similar users)
3. Create 2-3 personas (not more)
4. Validate with team
5. Post visibly (always reference)

### Templates

**Persona Template:**
```markdown
# Persona: {Name} ({Type})

## Photo
[Stock photo representing this person]

## Demographics
- **Age:** 32
- **Role:** Product Manager at startup
- **Income:** $120K
- **Location:** San Francisco
- **Tech savviness:** High

## Behaviors
- Works 50+ hours/week
- Uses: Slack, Notion, Figma, Jira
- Checks phone first thing in morning
- Reads newsletters over coffee

## Pain Points
1. Too many tools, context switching
2. Stakeholder alignment meetings
3. Data scattered across systems

## Goals
- Ship features faster
- Better work-life balance
- Get promoted to Director

## Quote
"I spend more time coordinating than creating."

## Jobs To Be Done
- When I [situation], I want to [action], so I can [outcome]
```

### Examples

**SaaS Personas:**
1. Primary: "Startup Sarah" - PM at early-stage startup
2. Secondary: "Enterprise Eric" - PM at Fortune 500
3. Negative: "Agency Alex" - Freelance consultant

### Agent
faion-research-agent (mode: personas)

---

## M-RES-012: Problem Validation

### Problem
Entrepreneurs build solutions for problems that don't exist or aren't painful enough.

### Framework

**Validation Criteria:**

| Criterion | Threshold | How to Measure |
|-----------|-----------|----------------|
| **Frequency** | Weekly+ | "How often do you face this?" |
| **Intensity** | 7+/10 | "How painful is this? (1-10)" |
| **Willingness to Pay** | Yes | "Would you pay to solve this?" |
| **Search Behavior** | Exists | Check search volume |
| **Competition** | Exists | Someone trying to solve it |

**Evidence Types:**

| Type | Strength | Source |
|------|----------|--------|
| Verbatim quotes | Strong | Interviews |
| Forum discussions | Medium | Reddit, communities |
| Review complaints | Medium | App stores, G2 |
| Search volume | Medium | Google Trends, Ahrefs |
| Competitor existence | Weak | Market research |

**Validation Process:**
1. State the problem hypothesis
2. Define evidence needed
3. Collect evidence (10+ data points)
4. Assess against criteria
5. Decide: Proceed / Pivot / Kill

### Templates

**Problem Validation Report:**
```markdown
## Problem: {Statement}

### Hypothesis
{Who} struggles with {what} because {why}

### Evidence Collected

| Type | Source | Finding |
|------|--------|---------|
| Interview | User 1 | "I spend 3 hours/week on this" |
| Interview | User 2 | "Would pay $50/month" |
| Forum | Reddit | 50 upvotes on complaint post |
| Review | G2 | "Missing feature X" (repeated 10x) |
| Search | Google | "solve X problem" - 5K/month |

### Assessment

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Frequency | Weekly | Interviews |
| Intensity | 8/10 | Interviews |
| WTP | Yes | 4/5 would pay |
| Search | Medium | 5K/month |
| Competition | Yes | 3 competitors |

### Decision
**PROCEED** - Strong problem-solution fit
```

### Examples

**Validated Problem:**
- Hypothesis: Freelancers struggle tracking time across projects
- Evidence: 8/10 interviews confirmed, avg 5 hrs/week lost
- Decision: Proceed to solution validation

### Agent
faion-research-agent (mode: validate)

---

## M-RES-013: Pain Point Mining

### Problem
Entrepreneurs don't know where customers express frustrations.

### Framework

**Mining Sources:**

| Source | Search Strategy | Signal Strength |
|--------|-----------------|-----------------|
| Reddit | "r/{niche} + frustrating/hate/problem" | High (honest) |
| Twitter/X | "{product} sucks" OR "wish {product}" | High (real-time) |
| App Reviews | 1-3 star reviews | High (specific) |
| Forums | Product-specific communities | Medium |
| Quora | "{problem} solution" | Medium |
| LinkedIn | Industry discussions | Low (filtered) |

**Search Queries:**
```
"{keyword} frustrating" site:reddit.com
"{competitor} alternative" site:reddit.com
"{product} review" 1-star
"I wish {tool} could"
"hate using {tool}"
"looking for {solution}"
```

**Analysis Process:**
1. Collect 50+ pain point mentions
2. Categorize by theme
3. Count frequency per theme
4. Note intensity language
5. Identify gaps in solutions

### Templates

**Pain Point Mining Report:**
```markdown
## Topic: {Area}

### Sources Searched
- Reddit: r/x, r/y, r/z
- App Store: {app1}, {app2}
- Forums: {forum1}

### Pain Points Identified

| Theme | Frequency | Sample Quote | Intensity |
|-------|-----------|--------------|-----------|
| Slow sync | 23 mentions | "Takes forever to sync" | High |
| Missing feature X | 15 mentions | "Why doesn't it have X?" | Medium |
| Expensive | 12 mentions | "Not worth $99/month" | High |

### Key Insights
1. {insight 1}
2. {insight 2}

### Opportunity
{What solution addresses top pain points}
```

### Examples

**Project Management Pain Mining:**
- Top pain: "Too many clicks to create task" (35 mentions)
- Opportunity: One-click task creation from anywhere

### Agent
faion-research-agent (mode: pains)

---

## M-RES-014: Niche Viability Scoring

### Problem
Entrepreneurs can't objectively assess if a niche is worth pursuing.

### Framework

**5 Criteria Model:**

| Criterion | Weight | 1-3 | 4-6 | 7-10 |
|-----------|--------|-----|-----|------|
| Market Size | 25% | <$10M | $10-100M | >$100M |
| Competition | 20% | Red ocean (10+) | Moderate (3-10) | Blue ocean (<3) |
| Barriers | 20% | High (capital, regulatory) | Medium | Low |
| Profitability | 20% | Thin margins (<20%) | OK (20-40%) | High (>40%) |
| Your Fit | 15% | No relevant skills | Some skills | Perfect match |

**Scoring Process:**
1. Research each criterion
2. Score 1-10 with justification
3. Apply weights
4. Calculate weighted average
5. Compare to thresholds

**Decision Thresholds:**
- 7.5-10: Strong opportunity
- 5.5-7.4: Proceed with caution
- 3.5-5.4: Significant risks
- <3.5: Pass

### Templates

**Niche Viability Scorecard:**
```markdown
## Niche: {Name}

| Criterion | Score | Weight | Weighted | Justification |
|-----------|-------|--------|----------|---------------|
| Market Size | 7 | 25% | 1.75 | $80M SAM |
| Competition | 6 | 20% | 1.20 | 5 competitors |
| Barriers | 8 | 20% | 1.60 | Technical only |
| Profitability | 7 | 20% | 1.40 | SaaS margins |
| Your Fit | 9 | 15% | 1.35 | 10 yrs experience |
| **Total** | | | **7.30** | |

### Decision
**PROCEED WITH CAUTION** - Good opportunity, watch competition

### Risk Mitigation
- {risk 1}: {mitigation}
- {risk 2}: {mitigation}
```

### Examples

**AI Writing Tool Niche:**
- Market: 8 ($200M)
- Competition: 4 (crowded)
- Barriers: 6 (ML expertise needed)
- Profitability: 7 (SaaS)
- Fit: 8 (ML background)
- **Total: 6.5 → Proceed with differentiation**

### Agent
faion-research-agent (mode: niche)

---

## M-RES-015: Blue Ocean Strategy

### Problem
Entrepreneurs compete in crowded markets instead of creating new ones.

### Framework

**Red vs Blue Ocean:**

| Red Ocean | Blue Ocean |
|-----------|------------|
| Compete in existing market | Create uncontested space |
| Beat the competition | Make competition irrelevant |
| Exploit existing demand | Create new demand |
| Value-cost trade-off | Break value-cost trade-off |

**Four Actions Framework:**

| Action | Question | Result |
|--------|----------|--------|
| **Eliminate** | What factors can we eliminate? | Remove costly/unnecessary |
| **Reduce** | What can we reduce below standard? | Simplify |
| **Raise** | What can we raise above standard? | Differentiate |
| **Create** | What new factors can we create? | Innovate |

**Strategy Canvas:**
- X-axis: Key competing factors
- Y-axis: Offering level (low to high)
- Plot competitors and your new curve

### Templates

**Blue Ocean Canvas:**
```markdown
## Industry: {Name}

### Current Red Ocean Factors
| Factor | Industry Level | Customer Value |
|--------|---------------|----------------|
| Price | High | Medium |
| Features | Many | Low (unused) |
| Support | 24/7 | Low (rarely needed) |

### Four Actions

#### Eliminate
- {factor}: Why? {reason}

#### Reduce
- {factor}: From {X} to {Y}

#### Raise
- {factor}: From {X} to {Y}

#### Create
- {new factor}: {description}

### New Value Curve
[Strategy canvas visualization]

### Blue Ocean Opportunity
{Description of uncontested space}
```

### Examples

**Cirque du Soleil:**
- Eliminated: Animals, star performers, aisle concessions
- Reduced: Fun/humor, thrill/danger
- Raised: Unique venue, refined watching environment
- Created: Theme, artistic music/dance, multiple productions

### Agent
faion-research-agent (mode: niche)

---

## M-RES-016: Value Proposition Canvas

### Problem
Products don't clearly match customer needs.

### Framework

**Two Parts:**

**1. Customer Profile (right side):**
```
┌─────────────────────────┐
│     Customer Jobs       │
│  (tasks, problems)      │
├─────────────────────────┤
│     Pains               │
│  (obstacles, risks)     │
├─────────────────────────┤
│     Gains               │
│  (desired outcomes)     │
└─────────────────────────┘
```

**2. Value Map (left side):**
```
┌─────────────────────────┐
│  Products & Services    │
│  (what we offer)        │
├─────────────────────────┤
│     Pain Relievers      │
│  (how we reduce pains)  │
├─────────────────────────┤
│     Gain Creators       │
│  (how we create gains)  │
└─────────────────────────┘
```

**FIT = Pain Relievers address Pains + Gain Creators enable Gains**

**Prioritization:**
- Focus on pains rated 8+/10
- Focus on gains customers measure success by
- Ignore "nice to have" pains/gains

### Templates

**Value Proposition Canvas:**
```markdown
## Customer Segment: {Name}

### Customer Profile

#### Jobs
- Functional: {job}
- Emotional: {job}
- Social: {job}

#### Pains (ranked by intensity)
1. {pain} - 9/10
2. {pain} - 8/10
3. {pain} - 6/10

#### Gains (ranked by relevance)
1. {gain} - Essential
2. {gain} - Expected
3. {gain} - Desired

### Value Map

#### Products & Services
- {product/feature}
- {product/feature}

#### Pain Relievers
- {pain 1} → {how we relieve it}
- {pain 2} → {how we relieve it}

#### Gain Creators
- {gain 1} → {how we create it}
- {gain 2} → {how we create it}

### FIT Assessment
- Pain coverage: 2/3 top pains addressed
- Gain coverage: 2/3 top gains enabled
- **FIT Score: 80%**
```

### Examples

**Freelancer Invoicing Tool:**
- Pain: Takes too long to create invoice (9/10)
- Pain Reliever: Auto-generate from time tracking
- Gain: Get paid faster
- Gain Creator: Automated payment reminders

### Agent
faion-research-agent (mode: personas)

---

## M-RES-017: Project Naming Strategies

### Problem
Entrepreneurs struggle to find memorable, available names.

### Framework

**Naming Strategies:**

| Strategy | Description | Examples |
|----------|-------------|----------|
| **Descriptive** | What it does | Dropbox, YouTube |
| **Invented** | Made-up word | Spotify, Kodak |
| **Compound** | Two words combined | Facebook, Snapchat |
| **Metaphor** | Symbolic meaning | Amazon, Apple |
| **Portmanteau** | Blended words | Pinterest, Instagram |
| **Alliteration** | Same sound | PayPal, Coca-Cola |
| **Acronym** | Letters | IBM, NASA |

**Good Name Criteria:**
- Easy to spell
- Easy to pronounce
- Memorable
- Domain available (.com preferred)
- No trademark conflicts
- Works internationally

**Generation Process:**
1. Define brand attributes (3-5 adjectives)
2. List keywords (product, benefit, emotion)
3. Apply each strategy to keywords
4. Generate 20+ candidates
5. Check availability
6. Test with target audience

### Templates

**Naming Brief:**
```markdown
## Project: {Description}

### Brand Attributes
- {attribute 1}
- {attribute 2}
- {attribute 3}

### Keywords
- Product: {words}
- Benefits: {words}
- Emotions: {words}

### Name Candidates

| Name | Strategy | .com | Meaning |
|------|----------|------|---------|
| {name} | Descriptive | Y/N | {why} |
| {name} | Invented | Y/N | {why} |
| {name} | Compound | Y/N | {why} |

### Top 3 Recommendations
1. {name}: {reasoning}
2. {name}: {reasoning}
3. {name}: {reasoning}
```

### Examples

**Task Management Tool:**
- Attributes: Simple, fast, powerful
- Candidates: TaskFlow (compound), Tasko (invented), QuickTask (descriptive)
- Winner: TaskFlow (.com available, memorable)

### Agent
faion-research-agent (mode: names)

---

## M-RES-018: Domain Availability Check

### Problem
Great names are unusable due to domain/handle unavailability.

### Framework

**Check Priority:**

| Type | Priority | Importance |
|------|----------|------------|
| .com | 1 | Essential for credibility |
| .io | 2 | Acceptable for tech |
| .co | 3 | Alternative |
| GitHub | 1 | Essential for open source |
| Twitter/X | 2 | Important for marketing |
| LinkedIn | 3 | Nice to have |

**Availability Actions:**

| Status | Action |
|--------|--------|
| Available | Register immediately |
| Premium ($X) | Consider if <$5K |
| Taken (parked) | Check price, usually overpriced |
| Taken (active) | Move to next name |

**Alternative Strategies:**
- Add "get", "try", "use" prefix: getTaskFlow.com
- Add "app", "hq" suffix: taskflowhq.com
- Different TLD: taskflow.io
- Creative spelling: taskflw.com

### Templates

**Domain Check Report:**
```markdown
## Name: {name}

### Domain Availability

| Domain | Status | Price | Notes |
|--------|--------|-------|-------|
| {name}.com | Available | $12/yr | Register now |
| {name}.io | Taken | - | Active site |
| {name}.co | Premium | $2,500 | Parked |

### Social Handles

| Platform | Handle | Status |
|----------|--------|--------|
| Twitter | @{name} | Available |
| GitHub | {name} | Taken |
| LinkedIn | /company/{name} | Available |

### Trademark Check
- USPTO: No conflicts found
- Note: Not legal advice, consult attorney

### Recommendation
**Register {name}.com and @{name} immediately**

### Alternatives if Unavailable
1. get{name}.com
2. {name}app.com
3. {name}.io
```

### Examples

**TaskFlow Availability:**
- taskflow.com: Taken (active SaaS)
- gettaskflow.com: Available
- taskflow.io: Available
- @taskflow: Taken
- @gettaskflow: Available
- Recommendation: gettaskflow.com + @gettaskflow

### Agent
faion-domain-checker-agent

---

## M-RES-019: Pricing Model Selection

### Problem
Entrepreneurs choose wrong pricing models that limit growth or revenue.

### Framework

**Pricing Models:**

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| **Freemium** | High volume, low marginal cost | Viral growth | Low conversion (2-5%) |
| **Subscription** | Recurring value | Predictable revenue | Churn risk |
| **Usage-based** | Variable consumption | Scales with value | Unpredictable revenue |
| **One-time** | Complete product | Simple | No recurring revenue |
| **Tiered** | Diverse segments | Captures more value | Complex |
| **Per-seat** | Team tools | Clear pricing | Resistance to add users |

**Selection Criteria:**

| Factor | Question |
|--------|----------|
| Value delivery | Continuous or one-time? |
| Usage patterns | Consistent or variable? |
| Customer type | Individual or team? |
| Competition | What do they charge? |
| Marginal cost | Cost to serve additional user? |

**Pricing Research:**
1. List top 5 competitors' pricing
2. Calculate value delivered
3. Survey willingness to pay (Van Westendorp)
4. Test with early users

### Templates

**Pricing Strategy:**
```markdown
## Product: {Name}

### Competitor Pricing

| Competitor | Model | Price Range | Notes |
|------------|-------|-------------|-------|
| {name} | Subscription | $X-Y/mo | |
| {name} | Freemium | Free-$X | |

### Value Analysis
- Cost of problem: $X/month
- Time saved: X hours/month
- Value captured: 10-20% of savings

### Recommended Model
**Tiered Subscription**

### Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| Free | $0 | {features} | Try before buy |
| Pro | $19/mo | {features} | Individuals |
| Team | $49/mo | {features} | Small teams |
| Enterprise | Custom | {features} | Large orgs |

### Justification
- Freemium drives awareness
- Pro captures 80% of revenue
- Enterprise for large accounts
```

### Examples

**SaaS Pricing Decision:**
- Model: Tiered subscription
- Free: 1 project, basic features
- Pro ($19): Unlimited projects
- Team ($49/user): Collaboration features
- Justification: Match competitor pricing, capture team value

### Agent
faion-research-agent (mode: pricing)

---

## M-RES-020: Customer Interview Framework

### Problem
Interviews fail to extract actionable insights due to poor questions and structure.

### Framework

**Interview Types:**

| Type | Stage | Goal | Duration |
|------|-------|------|----------|
| Discovery | Problem validation | Understand context | 30 min |
| Problem | Problem validation | Deep dive on pain | 45 min |
| Solution | Solution validation | Test concepts | 45 min |
| Usability | Product development | Test prototype | 60 min |

**Interview Flow:**

```
1. Warm-up (5 min)
   - Build rapport
   - Set expectations
   ↓
2. Context (10 min)
   - Their role, background
   - Current situation
   ↓
3. Deep dive (20 min)
   - Pain exploration
   - Past behavior
   - Emotional triggers
   ↓
4. Concept test (10 min)
   - Show solution
   - Get reaction
   ↓
5. Wrap-up (5 min)
   - Willingness to pay
   - Referrals
```

**Question Types:**

| Type | Purpose | Example |
|------|---------|---------|
| Open | Explore | "Tell me about..." |
| Probing | Go deeper | "Why is that?" |
| Clarifying | Understand | "Can you give an example?" |
| Summary | Confirm | "So you're saying..." |

**Anti-patterns:**
- Leading questions: "Don't you think X is great?"
- Future hypotheticals: "Would you use...?"
- Pitching: Explaining your solution too early
- Multiple questions: Asking 2+ questions at once

### Templates

**Interview Guide:**
```markdown
## Interview: {Type}

### Preparation
- Hypothesis to test: {hypothesis}
- Key questions: 5 max
- Recording setup: {yes/no}

### Script

#### Warm-up
"Thanks for joining. I'm researching [topic]. No right/wrong answers, just honest feedback."

#### Context
"Tell me about your role."
"Walk me through a typical day."

#### Deep Dive
"Tell me about the last time you [problem]."
"What happened? What did you do?"
"How did that make you feel?"
"What would you change?"

#### Concept Test
[Show prototype/concept]
"What do you think this is?"
"Would this help? How?"
"What's missing?"

#### Wrap-up
"Would you pay for this? How much?"
"Who else should I talk to?"

### Notes Template

| Question | Answer | Insight |
|----------|--------|---------|
| {question} | {verbatim} | {interpretation} |
```

### Examples

**Key Interview Insights:**
- 8/10 mentioned same frustration
- Verbatim: "I would pay $100 to not deal with this"
- Behavior: Currently using 3 tools as workaround
- Insight: Strong problem-solution fit

### Agent
faion-research-agent (mode: validate)

---

*faion-research-domain-skill v1.1*
*Merged from: faion-idea-discovery, faion-product-research, faion-project-naming*
*Methodologies: M-RES-001 to M-RES-020 (20 total)*
*Agents: 8 research + 2 naming*
