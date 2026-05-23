---
name: researching-market
description: Guided market research workflow covering TAM/SAM/SOM market sizing, competitive landscape analysis, and customer interview preparation
version: "1.0"
tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Agent
---

# Market Research Guided Workflow

Guided market research skill covering three phases: TAM/SAM/SOM market sizing with web research, competitive landscape analysis with positioning matrices, and hypothesis-driven customer interview question generation. Adapts questions to the user's business knowledge level.

---

## Purpose

This skill produces credible, data-backed market size estimates for a business plan. It generates a structured output file at `devforgeai/specs/business/market-research/market-sizing.md` containing:

- **TAM** (Total Addressable Market) - the total revenue opportunity
- **SAM** (Serviceable Addressable Market) - the segment you can reach
- **SOM** (Serviceable Obtainable Market) - the realistic near-term capture

Each tier includes a dollar value estimate, methodology notes, source citations, and a confidence level.

---

## When to Use This Skill

**Use when:**
- A founder needs to validate market size for a business idea
- A business plan requires TAM/SAM/SOM estimates with cited sources
- Market research data is needed before investor conversations

**Invoked by:**
- `/market-research` command
- `planning-business` skill (market research phase)

---

## Execution Mode and Phase Routing

This skill supports two execution modes: **standalone** and **full workflow**.

### Standalone Mode

Each phase can run standalone without requiring prior phases. There is no prerequisite for running any individual phase independently:

- **market-sizing** standalone - Runs market sizing analysis independently, producing `market-sizing.md` without prior phases
- **competitive-analysis** standalone - Runs competitive landscape analysis independently, producing `competitive-analysis.md` without prior phases
- **customer-interviews** standalone - Generates interview questions independently, producing `customer-interviews.md` without prior phases

Each phase independently completes and produces its designated output. No prior phase outputs are required.

### Full Workflow Mode

When invoked with the `full` argument, all three phases run sequentially:

1. **market-sizing** (Phase 1)
2. **competitive-analysis** (Phase 2)
3. **customer-interviews** (Phase 3)

In full mode, context is passed between phases: market sizing outputs carry forward into competitive analysis, and both carry forward into customer interview question generation. This context passing enriches later phases with data from earlier ones.

**Existing Output Reuse (BR-003):** Before starting each phase in full mode, check for existing outputs. If a phase output already exists, offer to reuse or regenerate via AskUserQuestion.

### Adaptive Pacing and Task Chunking

When a user profile exists (via EPIC-072), the skill reads it at initialization to adapt pacing and task chunking to user preferences. The profile's `business_knowledge` field controls question depth and adaptive chunking behavior. If the profile is missing, default pacing applies (beginner level, 5 questions per prompt, medium detail).

---

## Output Specification

The output file `devforgeai/specs/business/market-research/market-sizing.md` contains:

### Output Template

```markdown
# Market Sizing: [Business Description]

## TAM (Total Addressable Market)
- **Value**: $X.XB (dollar estimate)
- **Methodology**: top-down | bottom-up | Fermi
- **Confidence**: High | Medium | Low
- **Sources**:
  - [Source 1 with URL or report name]
  - [Source 2 with URL or report name]

## SAM (Serviceable Addressable Market)
- **Value**: $X.XM (dollar estimate)
- **Methodology**: top-down | bottom-up | Fermi
- **Confidence**: High | Medium | Low
- **Sources**:
  - [Source with attribution]

## SOM (Serviceable Obtainable Market)
- **Value**: $X.XM (dollar estimate)
- **Methodology**: bottom-up | Fermi
- **Confidence**: High | Medium | Low
- **Sources**:
  - [Source with attribution]
```

### Business Rules

**BR-001: Ordering Invariant** - TAM >= SAM >= SOM > 0. All tier values must be positive (greater than zero) and maintain this ordering invariant. If values violate this constraint, flag the inconsistency and prompt the user for correction via AskUserQuestion.

**BR-002: Source Attribution** - All data points must have source attribution. Every figure in the output must cite its source (URL, report name, or "user-provided"). No unsourced figures are permitted.

---

## Workflow

Questions are presented sequentially using progressive disclosure. Each step collects one piece of information before proceeding to the next. Users may cancel or abort the workflow at any AskUserQuestion step.

### Step 0: Load User Profile and Determine Knowledge Level

Read the user profile to adapt question depth:

```
Read(file_path="devforgeai/specs/business/user-profile.md")
```

Extract the `business_knowledge` field from the user profile. This field determines question depth:

- **beginner** - Explain TAM, SAM, SOM concepts with full context before each question. Beginner users receive explanatory context about what TAM/SAM/SOM means, why it matters, and how to think about each tier.
- **intermediate** - Provide standard prompts with brief context. Intermediate users receive standard question prompts without extended explanations.
- **advanced** - Use abbreviated prompts with option for direct input. Advanced users receive abbreviated prompts and can input known figures directly without guided estimation.

**Default behavior when profile is missing:** If the user-profile.md file is not found or the `business_knowledge` field is absent, default to beginner level. Log a warning that the profile was not found: "WARNING: user-profile.md not found or business_knowledge field missing. Defaulting to beginner knowledge level."

### Step 1: Collect Target Market Description

Use AskUserQuestion to gather the target market or industry:

```
AskUserQuestion:
  Question: "What is your target market or industry?"
  Header: "Market Description"
  Description: "Describe the market your product/service operates in. Be as specific as possible."
  Options:
    - label: "Enter market description"
      description: "Provide a free-text description of your target market"
    - label: "Cancel workflow"
      description: "Exit the market sizing workflow"
  multiSelect: false
```

If the user selects cancel, abort the workflow gracefully.

### Step 2: Collect Geographic Scope

Use AskUserQuestion to determine geographic scope and region:

```
AskUserQuestion:
  Question: "What is the geographic scope for your market?"
  Header: "Geographic Scope"
  Options:
    - label: "Global"
      description: "Worldwide market"
    - label: "North America"
      description: "US and Canada"
    - label: "Europe"
      description: "EU and UK markets"
    - label: "Specific region/country"
      description: "Specify a particular location"
    - label: "Cancel"
      description: "Abort market sizing"
  multiSelect: false
```

### Step 3: Collect Customer Segment

Use AskUserQuestion to identify the target customer segment:

```
AskUserQuestion:
  Question: "Who is your primary customer segment?"
  Header: "Customer Segment"
  Description: "Define the specific customer group you intend to serve."
  Options:
    - label: "B2B (Business customers)"
      description: "Selling to other businesses"
    - label: "B2C (Consumer customers)"
      description: "Selling directly to consumers"
    - label: "B2B2C (Both)"
      description: "Business and consumer channels"
    - label: "Cancel"
      description: "Abort market sizing"
  multiSelect: false
```

### Step 4: Collect Pricing Assumptions

Use AskUserQuestion to gather pricing information for bottom-up estimation:

```
AskUserQuestion:
  Question: "What is your expected average price point or revenue per customer?"
  Header: "Pricing Assumptions"
  Description: "This helps calculate bottom-up market size estimates."
  Options:
    - label: "Enter pricing details"
      description: "Provide average price, subscription cost, or transaction value"
    - label: "Skip (use industry averages)"
      description: "Let the workflow estimate based on industry data"
    - label: "Cancel"
      description: "Abort market sizing"
  multiSelect: false
```

### Step 5: Research Market Data via Internet-Sleuth

Invoke the internet-sleuth subagent to gather external market data. The skill invokes internet-sleuth to find industry reports, market sizes, and growth rates.

```
Task(
  subagent_type="internet-sleuth",
  description="Research market size data for [industry] in [geography]",
  prompt="Find TAM data: total industry revenue, market size reports, growth rates for [market]. Find at least 2 data points from external sources with source attribution. Return URLs and report names for all data."
)
```

**Data Point Requirements:**
- At least 2 external data points must be gathered from internet-sleuth research
- Each data point must include source attribution (URL or report name)
- All external sources must be cited in the final output

**Invocation Limits (NFR-002):**
- Maximum 3 internet-sleuth invocations per workflow run
- Budget calls as: (1) TAM industry data, (2) SAM segment data, (3) SOM competitive data

**Fermi Fallback (BR-003):**
- If internet-sleuth returns no data or fails, fallback to Fermi estimation
- When using Fermi fallback, mark confidence as Low for affected tiers
- Note data limitations in the output: "Limited external data available; estimate based on Fermi estimation"

For detailed Fermi estimation methodology, see: [fermi-estimation.md](references/fermi-estimation.md)

### Step 6: Calculate TAM (Total Addressable Market)

Calculate TAM using the gathered data:

1. Apply top-down methodology if industry-level data is available from research
2. Apply bottom-up methodology if unit-level data is available
3. Apply Fermi estimation as fallback when external data is insufficient

For detailed methodology guidance, see: [market-sizing-methodology.md](references/market-sizing-methodology.md)

**Confidence Level Assignment:**
- **High** confidence: Multiple corroborating external sources with recent data (< 2 years old)
- **Medium** confidence: Single external source or data older than 2 years
- **Low** confidence: Fermi estimation only, no external data, or highly uncertain assumptions

### Step 7: Calculate SAM (Serviceable Addressable Market)

Filter TAM by serviceable segment:

1. Apply geographic filters from Step 2
2. Apply customer segment filters from Step 3
3. Apply technology/channel accessibility filters

SAM value must be <= TAM value (ordering invariant).

### Step 8: Calculate SOM (Serviceable Obtainable Market)

Estimate realistic near-term capture:

1. Consider competitive landscape
2. Apply market penetration assumptions
3. Factor in go-to-market constraints

SOM value must be <= SAM value (ordering invariant).

### Step 9: Validate and Write Output

**Validation Checks:**
1. Verify TAM >= SAM >= SOM > 0 (ordering invariant, BR-001)
2. Verify all figures have source attribution (BR-002)
3. Verify confidence levels are assigned (High, Medium, or Low)

If validation fails, use AskUserQuestion to resolve:

```
AskUserQuestion:
  Question: "Market size ordering violation detected. TAM must be >= SAM >= SOM > 0. How would you like to proceed?"
  Header: "Validation Error"
  Options:
    - label: "Review and correct values"
      description: "Re-enter the problematic tier values"
    - label: "Cancel"
      description: "Abort without saving"
  multiSelect: false
```

**Write Output:**

```
Write(file_path="devforgeai/specs/business/market-research/market-sizing.md", content=output)
```

---

## Competitive Analysis Phase

After market sizing is complete (or independently when invoked for competitive landscape research), execute the competitive analysis phase.

### Step 10: Invoke Market-Analyst for Competitive Analysis

Invoke the market-analyst subagent to research competitors and build a positioning matrix:

```
Task(
  subagent_type="market-analyst",
  description="Analyze competitive landscape for [business] in [market]",
  prompt="Research competitors in [market]. Build positioning matrix with name, category, strengths, weaknesses, market position summary, and differentiation for each competitor. Enforce 3-10 competitor bounds. Write output to devforgeai/specs/business/market-research/competitive-analysis.md"
)
```

**Competitive Analysis Output:**
- Positioning matrix with per-competitor profiles
- Differentiation opportunities analysis
- Written to `devforgeai/specs/business/market-research/competitive-analysis.md`

For detailed competitive analysis framework, see: [competitive-analysis-framework.md](references/competitive-analysis-framework.md)

---

## Customer Interview Question Generation Phase

After market sizing and competitive analysis (or independently when invoked for interview preparation), generate hypothesis-driven customer interview questions.

### Step 11: Load Interview Best Practices

Load the customer interview guide reference for methodology guidance:

```
Read(file_path=".claude/skills/researching-market/references/customer-interview-guide.md")
```

For detailed interviewing methodology, see: [customer-interview-guide.md](references/customer-interview-guide.md) (Open-Ended Question Techniques)

### Step 12: Identify Business Hypotheses

Extract business hypotheses from prior market research outputs or user input:

```
# Check for existing research outputs
Glob(pattern="devforgeai/specs/business/market-research/market-sizing.md")

# If no prior research, prompt user for hypotheses
IF no hypotheses found:
    AskUserQuestion:
      Question: "What business assumptions do you want to validate through customer interviews?"
      Header: "Business Hypotheses"
      Description: "List 2-5 specific assumptions about your customers, market, or product that you want to test."
      Options:
        - label: "Enter hypotheses"
          description: "Provide your business assumptions to validate"
        - label: "Cancel"
          description: "Abort interview question generation"
      multiSelect: false

IF zero hypotheses identified:
    HALT: "No business hypotheses found. Please articulate at least one assumption to validate."
    AskUserQuestion:
      Question: "Please describe at least one business assumption you want to validate."
      Header: "Required: Business Hypothesis"
```

### Step 13: Generate Interview Questions

Generate 10-20 hypothesis-driven questions following these rules:

**Question Rules:**
- Each question must map to a named hypothesis
- All questions must be open-ended (start with: How, What, Tell me about, Describe, Walk me through)
- No closed-ended questions (starting with: Do, Is, Are, Was, Were, Will, Would, Can, Could, Should, Did, Has)
- No leading phrasing (don't you think, wouldn't you agree, isn't it true, obviously, clearly, of course)
- 2-5 questions per hypothesis
- 10-20 questions total

**Question Count Validation:**
```
IF total_questions < 10: Regenerate with more questions per hypothesis
IF total_questions > 20: Prune to highest-priority questions per hypothesis
```

### Step 14: Write Interview Output

Write the interview questions to `devforgeai/specs/business/market-research/customer-interviews.md`:

**Output Format:**
```markdown
---
date: YYYY-MM-DD
hypothesis_count: N
question_count: N
---

# Customer Interview Questions

## Hypothesis: [Hypothesis Name]

1. [Open-ended question mapped to this hypothesis]
2. [Open-ended question mapped to this hypothesis]
...

## Next Steps

[Actionable guidance for conducting interviews and analyzing results]
```

**Validation Before Write:**
1. Verify question count (10-20 total)
2. Verify questions per hypothesis (2-5 each)
3. Verify all questions are open-ended
4. Verify no leading phrasing
5. Verify YAML frontmatter counts match actual counts

```
Write(file_path="devforgeai/specs/business/market-research/customer-interviews.md", content=output)
```

---

## Reference Files

| Reference | Path | When to Load |
|-----------|------|--------------|
| Market Sizing Methodology | references/market-sizing-methodology.md | During TAM/SAM/SOM calculation (Steps 6-8) |
| Fermi Estimation | references/fermi-estimation.md | When internet-sleuth fails or as supplementary method |
| Competitive Analysis Framework | references/competitive-analysis-framework.md | During competitive analysis phase (Step 10) |
| Customer Interview Guide | references/customer-interview-guide.md | During interview question generation (Steps 11-14) |

---

## Integration

### Subagent Dependencies

- **internet-sleuth**: Web research for market data. Invoked via Task() with subagent_type="internet-sleuth". Maximum 3 calls per workflow run.
- **market-analyst**: Competitive landscape analysis. Invoked via Task() with subagent_type="market-analyst". Synthesizes research into positioning matrix.

### Skill Dependencies

- **planning-business**: May invoke this skill during business plan creation
- **coaching-entrepreneur**: May reference market sizing output for coaching

### Input Files

- `devforgeai/specs/business/user-profile.md` - User profile with `business_knowledge` field

### Output Files

- `devforgeai/specs/business/market-research/market-sizing.md` - Final market sizing output
- `devforgeai/specs/business/market-research/competitive-analysis.md` - Competitive analysis output
- `devforgeai/specs/business/market-research/customer-interviews.md` - Customer interview questions

---

## Error Handling

| Error | Recovery |
|-------|----------|
| internet-sleuth unavailable | Fermi fallback with Low confidence |
| User profile not found | Default to beginner, warn: "profile not found" |
| TAM < SAM violation | AskUserQuestion for correction |
| No market data found | Complete with Fermi estimation, Low confidence |
| User cancels mid-workflow | Exit gracefully, no partial output |

---

## Success Criteria

- [ ] Output file contains TAM, SAM, SOM sections with dollar value estimates
- [ ] Each tier has methodology notes (top-down, bottom-up, or Fermi)
- [ ] Each tier has confidence level (High, Medium, or Low)
- [ ] All data points have source attribution (URL, report name, or user-provided)
- [ ] TAM >= SAM >= SOM > 0 invariant holds
- [ ] At least 2 external data points incorporated (when internet-sleuth available)
- [ ] Questions adapted to user knowledge level
- [ ] Output written to devforgeai/specs/business/market-research/market-sizing.md
- [ ] Interview questions written to devforgeai/specs/business/market-research/customer-interviews.md
- [ ] 10-20 open-ended questions generated with hypothesis mapping
