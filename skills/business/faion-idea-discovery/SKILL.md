---
name: faion-idea-discovery
description: "Startup idea generation and business niche research. Brainstorm ideas, research pain points, evaluate niches, validate problems. Use when starting new projects, exploring opportunities, or validating business ideas."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task
---

# Idea Discovery Skill

**Communication with user: User's language. Documents: English.**

## Purpose

Generate and validate startup/product ideas through systematic research.

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| faion-idea-generator-agent | opus | Creative idea brainstorming |
| faion-pain-point-researcher-agent | sonnet | Research pain points via Reddit/forums |
| faion-niche-evaluator-agent | sonnet | Evaluate niche viability |

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. Gather Context (AskUserQuestion)                    │
│     - Skills, interests, resources                      │
│     ↓                                                   │
│  2. Generate Ideas (faion-idea-generator-agent)                 │
│     - Apply 7 Ps framework + other methods              │
│     ↓                                                   │
│  3. User Selection (AskUserQuestion)                    │
│     - Pick 3-5 ideas to research                        │
│     ↓                                                   │
│  4. Pain Point Research (faion-pain-point-researcher-agent)     │
│     - Reddit, forums, reviews mining                    │
│     ↓                                                   │
│  5. Niche Evaluation (faion-niche-evaluator-agent)              │
│     - Market size, competition, barriers                │
│     ↓                                                   │
│  6. Present Results                                     │
│     ↓                                                   │
│  ┌─── User selects idea? ───┐                           │
│  │ NO                   YES │                           │
│  │  ↓                    ↓  │                           │
│  │ Loop back         7. Write to product_docs/          │
│  │ to step 2            idea-validation.md              │
│  └──────────────────────────┘                           │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Gather Context

Use AskUserQuestion:

```
Question 1: "Який у тебе досвід/навички?"
Options:
- Software development
- Design/UX
- Marketing/Sales
- Domain expertise (specific industry)

Question 2: "Що тебе мотивує?"
Options:
- Solve my own problem
- Big market opportunity
- Passion project
- Side income

Question 3: "Скільки готовий інвестувати часу?"
Options:
- Nights & weekends (side project)
- Part-time (20h/week)
- Full-time
```

---

## Phase 2: Generate Ideas

Call faion-idea-generator-agent agent:

```python
Task(
    subagent_type="faion-idea-generator-agent",
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

---

## Phase 3: User Selection

Present ideas grouped by category. Use AskUserQuestion:

```
Question: "Які ідеї хочеш дослідити глибше?"
multiSelect: true
Options:
- {idea1} - {category}
- {idea2} - {category}
- {idea3} - {category}
- {idea4} - {category}
(+ "Жодна, генеруй інші")
```

---

## Phase 4: Pain Point Research

For each selected idea, call faion-pain-point-researcher-agent:

```python
Task(
    subagent_type="faion-pain-point-researcher-agent",
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

---

## Phase 5: Niche Evaluation

For ideas with validated pain points, call faion-niche-evaluator-agent:

```python
Task(
    subagent_type="faion-niche-evaluator-agent",
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

---

## Phase 6: Present Results & Decision

Show evaluation results. Use AskUserQuestion:

```
Question: "Результати оцінки. Що далі?"
Options:
- ✅ {idea1} (score: 42/50) - обрати для розробки
- ✅ {idea2} (score: 38/50) - обрати для розробки
- 🔄 Жодна, генеруй нові ідеї
- 📊 Досліджуй інші ніші для {ideaX}
```

---

## Phase 7: Write to Documentation

When user selects idea:

1. Create `aidocs/sdd/{project}/product_docs/idea-validation.md`:
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

2. Offer next action:
   ```
   ✅ Ідея "{idea_name}" записана!

   Наступні кроки:
   - /faion-product-research {project} - глибше дослідження ринку
   - /faion-net {project} - створити першу фічу
   ```

---

## Idea Generation Frameworks

### 7 Ps of Ideation

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

---

## Niche Evaluation Criteria

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

## Error Handling

| Error | Action |
|-------|--------|
| No ideas resonate | Try different framework, ask about hobbies |
| No pain points found | Broaden search, try adjacent problems |
| High competition | Look for underserved segment |
| User rejects all | Generate more with different angle |
