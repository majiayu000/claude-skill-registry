---
name: token-budget-advisor
description: Proactive token budget assessment and task chunking strategy. Use this skill when queries involve multiple large file uploads, requests for comprehensive multi-document analysis, complex multi-step workflows with heavy research (10+ tool calls), phrases like "complete analysis", "full audit", "thorough review", "deep dive", or tasks combining extensive research with large output artifacts. This skill helps assess token consumption risk early and recommend chunking strategies before beginning work.
---

# Token Budget Advisor

This skill provides early assessment of token-heavy tasks and recommends chunking strategies to ensure successful completion within context window constraints.

## When to Use This Skill

Trigger this skill **before beginning work** when you detect:

- Multiple file uploads (3+ documents) combined with analysis requests
- Requests for "comprehensive", "complete", "thorough", or "full" analysis
- Multi-document comparative analysis
- Complex workflows requiring 10+ tool calls (extensive web research + synthesis)
- Tasks combining heavy research with large artifacts (reports, presentations)
- Queries spanning multiple dimensions (temporal + categorical + quantitative)
- Requests to "analyze everything" or "create a complete report on all aspects"

## Core Function

This skill serves two purposes:

1. **Early warning system**: Assess whether a task will likely exceed token limits
2. **Strategic planning**: Provide specific, actionable chunking recommendations

## Token Estimation Framework

### Quick Assessment Heuristics

Estimate token consumption using these rough guidelines:

**Input costs:**
- Uploaded document: ~1,000-5,000 tokens each (depending on length)
- Web search result: ~500-1,500 tokens
- Web fetch (full article): ~2,000-8,000 tokens
- Google Drive document: ~1,000-10,000 tokens (varies significantly)

**Output costs:**
- Simple response: 500-2,000 tokens
- Detailed analysis: 2,000-5,000 tokens
- Long-form report: 5,000-15,000 tokens
- Complex artifact (presentation, document): 5,000-20,000 tokens

**Tool call overhead:**
- Each tool call includes the query, results, and reasoning: ~1,000-3,000 tokens average

**Warning thresholds:**

- **Caution zone** (60-80% of budget): Task is achievable but tight; consider efficiency
- **Danger zone** (80-95% of budget): High risk; strongly recommend chunking
- **Exceeds budget** (95%+ of budget): Task requires chunking; cannot complete in one conversation

### Task Complexity Multipliers

Apply these mental adjustments:

- **Synthesis required**: Add 30-50% to output estimate (comparing, integrating multiple sources)
- **Iterative refinement**: Add 20-30% (when task involves reviewing and improving)
- **Multiple formats**: Add 20% per additional output type (report + presentation + spreadsheet)

## Chunking Strategy Framework

When a task exceeds token budget, recommend specific chunking approaches. Choose strategies based on task structure:

### 1. Sequential Processing

**Best for:** Time-series data, chronological analysis, ordered workflows

**Pattern:**
```
"This analysis of 12 months of data will exceed our token budget. I recommend we split it into quarters:
- Part 1: Q1-Q2 analysis (Jan-Jun)
- Part 2: Q3-Q4 analysis (Jul-Dec)  
- Part 3: Synthesis and recommendations

Should I start with Part 1?"
```

**When to use:**
- Historical data analysis
- Period-over-period comparisons
- Multi-phase projects

### 2. Dimensional Breakdown

**Best for:** Multi-faceted analysis, different aspects of same topic

**Pattern:**
```
"A complete market analysis covering financial, competitive, regulatory, and technological factors will strain our token budget. Let's break it into:
- Session 1: Financial performance and market size
- Session 2: Competitive landscape and positioning
- Session 3: Regulatory environment and compliance
- Session 4: Technology trends and synthesis

Which dimension should we tackle first?"
```

**When to use:**
- Multi-stakeholder analysis
- Different analytical lenses on same subject
- Complex business cases

### 3. Depth Progression

**Best for:** Tasks requiring outline → draft → refinement

**Pattern:**
```
"Creating a comprehensive 50-slide presentation with detailed research will exceed our budget. I recommend:
- Round 1: Build structure and outline (30 min)
- Round 2: Develop content for slides 1-25 (45 min)
- Round 3: Develop content for slides 26-50 (45 min)
- Round 4: Refinement pass (30 min)

Let's start with the outline?"
```

**When to use:**
- Large documents or presentations
- When quality refinement is important
- Creative projects benefiting from iteration

### 4. Subset Sampling

**Best for:** Large document sets where representative sampling works

**Pattern:**
```
"Analyzing all 15 contracts will exceed our budget. I suggest:
- Part 1: Analyze 5 representative contracts (different types/dates)
- Part 2: Based on patterns found, confirm with 5 more
- Part 3: Quick scan of remaining 5 for exceptions, then synthesize

This gives thorough coverage while managing tokens. Sound good?"
```

**When to use:**
- Document review at scale
- Pattern identification across many files
- Risk-based sampling approaches

### 5. Parallel Track Processing

**Best for:** Independent workstreams that can be combined later

**Pattern:**
```
"Comparing our product vs 5 competitors across features, pricing, and positioning is too large for one session. Let's split by competitor:
- Session 1: Competitors A & B full analysis
- Session 2: Competitors C & D full analysis  
- Session 3: Competitor E + synthesis matrix

Each session stays focused and manageable."
```

**When to use:**
- Comparative analysis
- Multiple independent subjects
- When parts don't need each other's context

## Communication Guidelines

### Messaging Framework

When recommending chunking, use this structure:

1. **Acknowledge the request clearly**
2. **Provide token budget assessment** (brief, 1 sentence)
3. **Recommend specific chunking approach** (numbered list, 2-4 parts)
4. **Ask for confirmation to proceed** (keep user in control)

**Example:**
```
I'll help you analyze these 8 financial reports and create a comprehensive presentation. 
This task will exceed our token budget given the research and artifact creation required. 
I recommend splitting it into:
1. Reports 1-4: Analysis and key findings
2. Reports 5-8: Analysis and key findings  
3. Synthesize all findings into presentation

Should I start with reports 1-4?
```

### What NOT to Do

❌ Don't over-explain token budgets or get technical about context windows
❌ Don't apologize excessively or sound limiting
❌ Don't provide vague suggestions like "maybe split this up somehow"
❌ Don't start work and then stop mid-task saying "we've run out of tokens"

✅ Do be matter-of-fact and solution-oriented
✅ Do provide specific, actionable breakdowns
✅ Do keep the momentum going toward task completion
✅ Do frame chunking as a quality improvement (thoroughness) not limitation

## Handling Edge Cases

### User Insists on Single Session

If user pushes back on chunking:

```
"I understand you'd prefer this in one go. I'll do my best to complete it, but I may need to:
- Prioritize the most critical elements
- Provide a condensed version
- Focus on breadth over depth in some areas

Let me start and we'll see how far we can get. What aspects are highest priority?"
```

### Task Becomes Too Large Mid-Stream

If partway through, token budget becomes concerning:

```
"I'm about halfway through and we're approaching token limits. I have two options:
1. Complete this current section and continue in a fresh conversation (recommended - maintains quality)
2. Accelerate through remaining sections with lighter analysis

Which approach works better for you?"
```

### Uncertain Estimation

When task scope is ambiguous:

```
"I want to make sure we complete this successfully. The scope could go in different directions. Could you clarify:
- [Specific question about depth]
- [Specific question about breadth]

This helps me gauge whether we should chunk this task."
```

## Integration with Other Skills

This skill works in conjunction with domain-specific skills:

- **Before heavy document analysis**: Check token budget, then use docx/pdf/xlsx skills
- **Before comprehensive research**: Assess scope, then execute research process
- **Before complex artifacts**: Plan chunking, then use pptx/docx/xlsx creation skills

Think of this skill as a "pre-flight check" before embarking on token-intensive tasks.

## Examples in Action

### Example 1: Multi-Document Analysis

**User query:** "Analyze all these uploaded contracts and tell me the common terms and differences"
*[User has uploaded 12 PDF contracts]*

**Response:**
"I'll help you analyze these 12 contracts. Given the volume, I recommend we process this in batches to ensure thorough analysis:

1. Contracts 1-4: Extract key terms, obligations, and unique clauses
2. Contracts 5-8: Same analysis
3. Contracts 9-12: Same analysis  
4. Synthesis: Common terms across all + key differences

This ensures I can give each contract proper attention. Should I start with contracts 1-4?"

### Example 2: Comprehensive Research Report

**User query:** "Research the AI chip market and create a detailed report covering market size, key players, technology trends, and 5-year forecast"

**Response:**
"I'll create a comprehensive AI chip market report. This research and report creation will be substantial, so I recommend:

1. Market overview: Size, growth, segments (research + draft)
2. Competitive landscape: Key players, market share, strategies (research + draft)
3. Technology trends: Current developments, emerging tech (research + draft)
4. Future outlook: 5-year forecast, implications (research + draft)
5. Final report assembly: Executive summary, polish, formatting

Each section gets thorough research and quality writing. Should I begin with the market overview?"

### Example 3: Simple Task (No Chunking)

**User query:** "Summarize this 10-page PDF and give me the key takeaways"

**Response:**
*[No trigger - proceed normally without invoking this skill]*
"I'll read through the PDF and extract the key points for you."

*Rationale: Single document summary is well within normal token budget.*

## Skill Maintenance

This skill should be updated when:

- Token budget limits change
- New patterns of token-heavy tasks emerge
- Chunking strategies prove ineffective in practice
- User feedback indicates communication could be clearer
