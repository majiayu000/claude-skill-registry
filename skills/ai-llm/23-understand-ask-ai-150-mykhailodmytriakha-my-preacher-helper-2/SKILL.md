---
name: 23-understand-ask-ai-150
description: "[23] UNDERSTAND. Consult external AI models when internal sources are exhausted. Build quality prompts using Prompt150 formula (Context + Query + Method + Style). Use when Loop150 exhausts internal sources, need real-world precedents, confidence <75%, or require reasoning from specialized AI models."
---

# Understand-Ask-AI 150 Protocol

**Core Principle:** When internal knowledge isn't enough, consult external AI expertise. Build quality prompts that get quality answers. Validate what comes back.

## What This Skill Does

When you invoke this skill, you're asking AI to:
- **Verify internal exhaustion** — Confirm internal sources are depleted
- **Build quality prompt** — Use Prompt150 formula
- **Target the right model** — Choose appropriate external AI
- **Send and receive** — Get external AI response
- **Validate response** — Check credibility and integrate

## The Prompt150 Formula

```
PROMPT150 = Context150 + Query + Method + Style

┌─────────────────────────────────────────────────────┐
│ CONTEXT150 (100% core facts + 50% supporting)       │
│ ├── Core situation and background                   │
│ ├── Key data points and constraints                 │
│ ├── Actions taken so far                            │
│ └── What we DON'T know (explicit unknowns)          │
├─────────────────────────────────────────────────────┤
│ QUERY (specific, answerable question)               │
│ ├── Single, focused question                        │
│ ├── Answerable with available information           │
│ └── NOT vague ("analyze this" ❌)                   │
├─────────────────────────────────────────────────────┤
│ METHOD (how to approach)                            │
│ ├── "Verify claims against real data"               │
│ ├── "Provide confidence levels (%)"                 │
│ ├── "Cite specific precedents with sources"         │
│ └── "Be conservative if data insufficient"          │
├─────────────────────────────────────────────────────┤
│ STYLE (output format)                               │
│ ├── Structured response (sections, tables)          │
│ ├── Confidence % for each claim                     │
│ ├── Facts vs assumptions clearly separated          │
│ └── Actionable recommendations if applicable        │
└─────────────────────────────────────────────────────┘
```

## When to Use This Skill

**TRIGGER CONDITIONS:**
1. **Loop150 exhausted internally** — All workspace files searched, no data
2. **Need real-world precedents** — Case studies, actual outcomes
3. **Need current information** — Data after knowledge cutoff
4. **Need statistical data** — Industry patterns, benchmarks
5. **Need scenario modeling** — Complex decision trees
6. **Confidence <75%** — Cannot reach 90% with internal data

**DO NOT USE FOR:**
- ❌ Facts already in workspace (use grep/search)
- ❌ Simple calculations (do yourself)
- ❌ Questions answerable by reading files
- ❌ First resort (always try internal first)

## Execution Protocol

### Step 1: EXHAUSTION VERIFICATION
```
🔍 **INTERNAL EXHAUSTION CHECK**

**Internal Sources Tried:**
- [ ] Codebase search: [Results]
- [ ] Documentation: [Results]
- [ ] Git history: [Results]
- [ ] Project files: [Results]

**Current Confidence:** [X]%
**Gap Identified:** [What we need but don't have]

**External Query Justified:** ✅ Yes | ❌ No (try more internal)
```

### Step 2: PROMPT CONSTRUCTION

Build using Prompt150 formula:

```
📝 **PROMPT150 CONSTRUCTION**

**CONTEXT150:**
[100% core facts]
- Situation: [What's happening]
- Data points: [Key numbers/facts]
- Constraints: [Limits and requirements]
- Actions taken: [What's been done]

[50% supporting details]
- Background: [Broader context]
- Unknowns: [What we explicitly don't know]
- Stakes: [Why this matters]

**QUERY:**
"[Specific, answerable question]"

Example good queries:
✅ "What were timelines for SSN breach cases with 5-500 affected?"
✅ "What is typical regulator response time for consumer complaints?"
❌ "Analyze my case" (too vague)
❌ "What should I do?" (too broad)

**METHOD:**
- Use Loop150-like verification
- Provide confidence levels (%)
- Cite real precedents with sources
- Be conservative if data insufficient

**STYLE:**
- Structured sections/tables
- Confidence % on each claim
- Facts vs assumptions separated
- Actionable recommendations
```

### Step 3: MODEL SELECTION
```
🤖 **MODEL SELECTION**

**Query Type:** [Research/Reasoning/Coding/Creative]

**Recommended Model:**
- Complex reasoning: ChatGPT-4/Claude (thinking models)
- Coding help: Claude/GPT-4
- Research synthesis: Perplexity/ChatGPT with browsing
- Current events: Models with web access

**Selected:** [Model name]
**Reason:** [Why this model]
```

### Step 4: USER APPROVAL
```
🌐 **ASK-AI 150 REQUEST**

**Justification:** Internal sources exhausted
**Confidence Gap:** [Current X%] → [Need Y%]

**Prompt Preview:**
"""
[Full Prompt150 to be sent]
"""

**Target Model:** [Model name]

**Approve external query?** (Yes / No / Modify)
```

### Step 5: SEND AND RECEIVE
Execute the query and capture response.

### Step 6: RESPONSE VALIDATION
```
✅ **RESPONSE VALIDATION**

**Source Credibility:**
- Model used: [Name]
- Claims verifiable: [Yes/Partially/No]
- Confidence stated: [Yes/No]

**Content Assessment:**
- Answers query: ✅ Yes | ⚠️ Partially | ❌ No
- Facts vs opinions: [Clear/Mixed/Unclear]
- Actionable: [Yes/Needs interpretation/No]

**Integration:**
- Confidence boost: [+X% → new total]
- Gaps remaining: [What's still unknown]
- Action items: [What to do with this info]
```

## Output Format

Request:
```
🌐 **ASK-AI 150 REQUEST**

**Internal Sources Exhausted:** ✅
**Current Confidence:** [X]%
**Gap:** [What we need]

**Prompt150:**
---
CONTEXT:
[Context150 content]

QUERY:
[Specific question]

METHOD:
- Verify against real data
- Provide confidence %
- Cite real precedents
- Be conservative

STYLE:
- Structured response
- Confidence per claim
- Facts vs assumptions
---

**Target:** [AI Model]
**Approve?**
```

Response integration:
```
🌐 **ASK-AI 150 RESPONSE INTEGRATED**

**Query:** [What was asked]
**Model:** [What answered]

**Key Findings:**
1. [Finding 1] — [Confidence %]
2. [Finding 2] — [Confidence %]
3. [Finding 3] — [Confidence %]

**Validation:**
├── Claims verifiable: [Yes/Partially]
├── Sources cited: [Yes/No]
└── Consistent with known facts: [Yes/No]

**Confidence Update:** [X%] → [Y%]
**Remaining Gaps:** [What's still unknown]

**Next Steps:** [How to use this information]
```

## Operational Rules

1. **INTERNAL FIRST:** Never skip internal research
2. **JUSTIFY EXTERNAL:** Document why internal is insufficient
3. **QUALITY PROMPTS:** Use full Prompt150 formula
4. **USER APPROVAL:** Get permission before external query
5. **VALIDATE RESPONSE:** Don't blindly trust external AI
6. **DOCUMENT INTEGRATION:** Log what was learned and confidence change

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Premature External** | Didn't exhaust internal | Complete internal search first |
| **Poor Prompt** | Vague, context-poor | Reformulate with Prompt150 |
| **Unreliable Response** | Unverifiable claims | Find better sources or reject |
| **No Validation** | Used response blindly | Cross-check before acting |

## Examples

### ❌ Bad Ask-AI
```
Query: "How to build web app?"
Context: [None provided]
Result: Got generic outdated advice, wasted time
```

### ✅ Good Ask-AI 150
```
🌐 ASK-AI 150 REQUEST

Internal Sources Exhausted: ✅
- Checked all project docs
- Searched codebase
- No breach precedent data found

Current Confidence: 65%
Gap: Need real-world timeline data for similar cases

Prompt150:
---
CONTEXT:
- SSN data breach affecting 47 individuals
- Breach discovered: 2024-03-15, Notified: 2024-06-20 (97 days)
- Washington State (RCW 19.255.010 requires 45 days)
- HIPAA-covered entity (45 CFR §164.524)
- Complaints filed with AG and HHS/OCR

QUERY:
"What were actual timelines and outcomes for SSN data 
breach cases similar to this (5-500 people affected) in 
the past 5 years?"

METHOD:
- Cite specific cases with dates and outcomes
- Provide confidence levels for predictions
- Distinguish confirmed data from estimates
- Be conservative if data insufficient

STYLE:
- Table format for cases
- Confidence % on predictions
- Separate facts from projections
---

Target: ChatGPT-4 (with web search)
Approve? Yes

---

🌐 ASK-AI 150 RESPONSE INTEGRATED

Key Findings:
1. Similar cases settled in 6-18 months (75% confidence)
2. Typical per-person compensation: $100-500 (70% confidence)
3. AG response time: 30-90 days (80% confidence)

Validation:
├── Claims verifiable: Partially (cited 3 real cases)
├── Sources cited: Yes (court records referenced)
└── Consistent with known facts: Yes

Confidence Update: 65% → 82%
Remaining Gaps: Specific WA state precedents

Next Steps: Use timeline estimates for planning, 
continue monitoring for WA-specific cases
```

## Relationship to Other Skills

- **research-deep-150** → Exhausts internal sources
- **ask-ai-150** → Consults external when internal insufficient
- **proof-grade-150** → Validates external information

---

**Remember:** Ask-AI is like calling a consultant — you don't call before doing your homework, you come with specific questions, and you verify their advice. Quality in, quality out.

