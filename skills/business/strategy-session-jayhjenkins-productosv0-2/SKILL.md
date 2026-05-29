---
name: strategy-session
description: Use when conducting strategic decision-making session - systematic context assembly, rigorous framework application, concrete scenario analysis, and structured session documentation
---

# Strategy Session

## Purpose

Conduct systematic strategic decision-making with:
- Auto-context assembly (research + meetings)
- Rigorous framework application with specific findings
- Concrete scenario analysis and quantitative grounding
- Stakeholder mapping when relevant
- Risk assessment with likelihood/impact ratings
- Structured session artifacts for memo generation

## When to Use

Activate when:
- User invokes `/strategy:session`
- Strategic decision needed
- Multiple options require systematic evaluation

## Workflow

### 1. Define Session Topic

**Ask user:**
- Topic (competitive-analysis, pricing-strategy, product-strategy, market-positioning, etc.)
- Specific decision question to address
- Time horizon (tactical: 3-6 months, strategic: 12+ months)
- Key stakeholders (optional)

**Document:**
- Create session folder: `/datasets/strategy/sessions/{YYYY}/{MM-DD}_{topic}/`
- Initialize `session-log.md` with metadata

### 2. Gather Research Context

**Invoke:** `research-gathering` skill

**Parameters:**
- Topic matching session focus
- Exclude expired sources (default)
- Include related topics if relevant

**Output to:** `{session-folder}/context.md`

**Structure:**
```markdown
# Research Context

**Session**: [Decision question]
**Date**: [YYYY-MM-DD]
**Topic**: [Topic]

## Research Sources ([N] sources)

### [Source 1 Title]
**Path**: [File path]
**Date**: [Source date]
**Key Insight**: [1-2 sentence insight relevant to decision]
**Citation-ready quote**: "[Verbatim 5-25 word quote]"

[Repeat for each source]

## Evidence Summary

**Key Finding 1**: [Synthesis with citations]
**Key Finding 2**: [Synthesis with citations]

**Quantitative Data**:
- [Metric/benchmark from research]
- [Metric/benchmark from research]

**Research Gaps**: [Note what's missing if relevant to decision]
```

### 3. Synthesize Meeting Context

**Invoke:** `meeting-synthesis` skill

**Parameters:**
- Time window: 90 days (broader for strategy)
- Topic keywords (from decision question)
- Customer/stakeholder filter if relevant

**Append to:** `{session-folder}/context.md`

**Add section:**
```markdown
## Customer/Stakeholder Signals ([N] meetings)

### [Signal 1]
**Source**: [Meeting date, participants]
**Context**: [What was discussed]
**Quote**: "[Verbatim customer/stakeholder quote]"
**Implication**: [How this informs decision]

[Repeat for each significant signal]

## Pattern Summary

**Cross-customer pattern 1**: [What multiple customers said]
**Cross-customer pattern 2**: [What multiple customers said]

**Stakeholder concerns**: [Concerns raised]
```

### 4. Select Decision Framework

**Framework options based on decision type:**

**Competitive Analysis:**
- Porter's Five Forces (industry structure analysis)
- Competitive Positioning Matrix (relative positioning)
- SWOT Analysis (strengths/weaknesses/opportunities/threats)

**Product Strategy:**
- Jobs-to-be-Done (customer need mapping)
- Opportunity Solution Tree (problem-solution alignment)
- RICE Prioritization (reach/impact/confidence/effort)
- Product-Market Fit Canvas

**Pricing Strategy:**
- Value-Based Pricing Framework
- Price Elasticity Analysis
- Competitive Pricing Analysis
- Cost-Plus vs. Value Pricing Trade-offs

**Market Positioning:**
- Segmentation-Targeting-Positioning (STP)
- Positioning Canvas
- Perceptual Mapping

**Organizational/Stakeholder:**
- Stakeholder Mapping (power/interest grid)
- RACI Matrix (responsibility assignment)
- Change Impact Analysis

**Ask user:** "Which framework fits this decision best? [List 2-3 most relevant]"

**If user unsure:** Recommend based on decision type and explain why

### 5. Apply Framework Rigorously

**Output to:** `{session-folder}/framework.md`

**General structure:**
```markdown
# Framework Analysis

**Framework**: [Framework name]
**Decision**: [Decision question]
**Date**: [YYYY-MM-DD]

## Framework Overview

[Brief description of framework and why it's appropriate for this decision]

## [Framework-Specific Components]

[Use framework structure below based on selection]

## Key Findings from Framework

**Finding 1**: [Specific insight with evidence from context]
**Finding 2**: [Specific insight with evidence from context]

**Quantitative Insights** (if applicable):
- [Metric/comparison from framework application]
- [Metric/comparison from framework application]

## Decision Implications

[What this framework analysis means for the decision at hand]
```

#### Porter's Five Forces Template

```markdown
## Porter's Five Forces Analysis

### 1. Supplier Power
**Rating**: [LOW | MEDIUM | HIGH]
**Factors**:
- [Factor with evidence]
- [Factor with evidence]
**Implication**: [How this affects decision]

### 2. Buyer Power
**Rating**: [LOW | MEDIUM | HIGH]
**Factors**:
- [Factor with evidence]
- [Factor with evidence]
**Implication**: [How this affects decision]

### 3. Competitive Rivalry
**Rating**: [LOW | MEDIUM | HIGH]
**Factors**:
- [Factor with evidence]
- [Factor with evidence]
**Key competitors**: [List with specific comparison]
**Implication**: [How this affects decision]

### 4. Threat of Substitution
**Rating**: [LOW | MEDIUM | HIGH]
**Alternatives**:
- [Alternative with adoption barrier]
- [Alternative with adoption barrier]
**Implication**: [How this affects decision]

### 5. Threat of New Entrants
**Rating**: [LOW | MEDIUM | HIGH]
**Barriers to Entry**:
- [Barrier]
- [Barrier]
**Implication**: [How this affects decision]

## Overall Industry Attractiveness
[Synthesis: Is this an attractive market/position? Why/why not?]
```

#### Stakeholder Mapping Template

```markdown
## Stakeholder Analysis

| Stakeholder | Power | Interest | Current Stance | Strategy |
|-------------|-------|----------|----------------|----------|
| [Name/Group] | [H/M/L] | [H/M/L] | [Support/Neutral/Oppose] | [Engage/Monitor/Inform] |

### High Power, High Interest (Manage Closely)
[Stakeholder]: [Specific concerns and engagement strategy]

### High Power, Low Interest (Keep Satisfied)
[Stakeholder]: [Specific concerns and engagement strategy]

### Low Power, High Interest (Keep Informed)
[Stakeholder]: [Specific concerns and engagement strategy]

### Low Power, Low Interest (Monitor)
[Stakeholder]: [Monitoring approach]

## Decision Impact by Stakeholder
[How this decision affects each key stakeholder group]
```

#### Pricing Framework Template

```markdown
## Value-Based Pricing Analysis

### Customer Value Assessment
**Value Metric**: [What customers get]
**Quantified Value**: [$ or % improvement from research/customer data]
**Value Drivers**:
- [Driver 1 with evidence]
- [Driver 2 with evidence]

### Competitive Pricing Context
| Competitor | Price | Positioning | Value Gap |
|------------|-------|-------------|-----------|
| [Name] | [Price] | [How positioned] | [Relative value] |

### Cost Structure
**Variable Costs**: [Per unit/per customer if known]
**Fixed Costs**: [Relevant fixed costs]
**Target Margin**: [If defined]

### Price Elasticity Considerations
**Elasticity estimate**: [HIGH/MEDIUM/LOW based on evidence]
**Evidence**: [Customer signals, competitive responses, research]

### Pricing Scenarios
[See section 6 for scenario development]
```

### 6. Develop Concrete Scenarios

**Interactive with user - document in:** `{session-folder}/session-log.md`

**Scenario Analysis Structure:**

```markdown
## Option Analysis

### Option 1: [Descriptive Name]

**Description**: [What this option entails specifically]

**Concrete Scenario**: [Walk through specific example]
- **Example**: [E.g., "Agency with 15 DTC brand clients, average $50k MRR"]
- **Impact**: [What happens in this scenario]
- **Numbers**: [Quantitative impact if estimable]

**Pros**:
- [Advantage with evidence source - be specific]
- [Advantage with evidence source - be specific]

**Cons**:
- [Disadvantage or risk - be specific]
- [Disadvantage or risk - be specific]

**Expected Impact** (quantitative where possible):
- [Metric]: [Expected change with confidence level]
- [Metric]: [Expected change with confidence level]

**Risk Assessment**:
- **Likelihood of success**: [HIGH/MEDIUM/LOW - why?]
- **Impact if fails**: [HIGH/MEDIUM/LOW - what happens?]
- **Reversibility**: [Can we reverse this decision? At what cost?]

**Framework alignment**: [How framework analysis supports/contradicts this option]

[Repeat for each option - aim for 2-4 options]
```

**Scenario depth guidelines:**
- Use concrete customer examples from meetings
- Include quantitative estimates (with confidence levels)
- Show trade-offs with specific numbers
- Reference framework findings in analysis
- Note stakeholder impacts per option

### 7. Facilitate Trade-off Analysis

**Add to session-log.md:**

```markdown
## Trade-off Analysis

| Dimension | Option 1 | Option 2 | Option 3 | Winner |
|-----------|----------|----------|----------|--------|
| [Criterion 1] | [Rating/score] | [Rating/score] | [Rating/score] | [Option] |
| [Criterion 2] | [Rating/score] | [Rating/score] | [Rating/score] | [Option] |

**Key Trade-offs**:
- **[Dimension 1] vs. [Dimension 2]**: [Analysis of trade-off]
- **[Dimension 3] vs. [Dimension 4]**: [Analysis of trade-off]

**Decision Criteria Weighting** (if user provides):
- [Criterion]: [Weight/importance]
- [Criterion]: [Weight/importance]
```

### 8. Develop Recommendation

**Interactive - capture in:** `{session-folder}/recommendations.md`

```markdown
# Recommendations

**Session**: [Decision question]
**Date**: [YYYY-MM-DD]

## Recommendation

**We recommend: Option [N] - [Name]**

## Rationale

1. **[Reason 1]**: [Detailed explanation with evidence]
   - Framework support: [How framework analysis supports]
   - Evidence: [Citations from research/meetings]
   - Quantitative basis: [Numbers if available]

2. **[Reason 2]**: [Detailed explanation with evidence]
   - Framework support: [How framework analysis supports]
   - Evidence: [Citations from research/meetings]
   - Quantitative basis: [Numbers if available]

3. **[Reason 3]**: [Detailed explanation with evidence]
   - Framework support: [How framework analysis supports]
   - Evidence: [Citations from research/meetings]
   - Quantitative basis: [Numbers if available]

## Expected Outcomes

**Primary Outcomes**:
- [Outcome 1 with metric and timeframe]
- [Outcome 2 with metric and timeframe]

**Secondary Outcomes**:
- [Outcome 3]
- [Outcome 4]

## Success Metrics

**Must be specific and measurable:**

| Metric | Baseline | Target | Timeline | Measurement Method |
|--------|----------|--------|----------|-------------------|
| [Metric 1] | [Current] | [Target] | [When] | [How to measure] |
| [Metric 2] | [Current] | [Target] | [When] | [How to measure] |

**Review Cadence**: [When to assess progress]

## Risk Management

### Risk 1: [Description]
- **Likelihood**: [LOW/MEDIUM/HIGH]
- **Impact**: [LOW/MEDIUM/HIGH]
- **Mitigation**: [Specific strategy]
- **Trigger/Threshold**: [When to escalate or pivot - if applicable]
- **Contingency**: [What to do if risk materializes]

[Repeat for each significant risk - aim for 3-5 risks]

## Key Dependencies

**Internal Dependencies**:
- [Dependency 1 - what needs to happen]
- [Dependency 2 - what needs to happen]

**External Dependencies**:
- [Dependency 3 - outside our control]
- [Dependency 4 - outside our control]

## Decision Gates (If Applicable)

[Critical decision points where we pause and reassess]

**Gate 1** ([Timeframe]): [What we assess and decision to make]
**Gate 2** ([Timeframe]): [What we assess and decision to make]

## Implementation Considerations (High-Level)

[Strategic guidance only - NOT project plan]

**Critical path items**: [What must happen in what order]
**Resource requirements**: [High-level resource needs]
**Timeline**: [Strategic phases - high-level only]

**Note**: Detailed implementation planning should be separate project management work.
```

### 9. Offer Memo Generation

**Ask user:** "Generate formal strategy memo from this session?"

**If yes:**
- Announce: "I'm using strategy-memo to create formal documentation"
- **Invoke:** `strategy-memo` skill
- Provide session folder path

**If no:**
- Confirm session artifacts saved
- Note memo can be generated later with `/strategy:memo`

## Session Quality Checklist

**Before marking session complete:**

- [ ] Context assembled with research sources (citations ready)
- [ ] Customer/meeting signals synthesized
- [ ] Framework selected and applied rigorously
- [ ] Framework findings documented with specific insights
- [ ] Options developed with concrete scenarios
- [ ] Each option includes pros/cons with evidence
- [ ] Quantitative analysis where appropriate
- [ ] Trade-offs analyzed systematically
- [ ] Recommendation clear with multi-point rationale
- [ ] Success metrics specific and measurable
- [ ] Risks assessed with likelihood/impact
- [ ] Risk mitigations documented
- [ ] All session artifacts written to folder

**Quality flags - need more work if:**
- Vague recommendations without concrete action
- Missing quantitative grounding for quantifiable decisions
- Options lack concrete scenarios or examples
- Framework applied superficially without specific findings
- Success metrics not measurable or no timeline
- Risks identified without mitigation strategies
- Unsupported projections or speculation

## File Structure

**Session folder:** `/datasets/strategy/sessions/{YYYY}/{MM-DD}_{topic}/`

**Required files:**
- `context.md` - Research and meeting context
- `framework.md` - Framework application and findings
- `session-log.md` - Interactive discussion and option analysis
- `recommendations.md` - Final recommendation with rationale

**Optional files:**
- `scenarios.md` - If extensive scenario modeling
- `stakeholders.md` - If detailed stakeholder analysis
- `data.csv` or `analysis.xlsx` - If quantitative modeling

## Success Criteria

- Context systematically assembled from research and meetings
- Framework applied rigorously with specific findings
- Options analyzed with concrete scenarios
- Quantitative data included where decision benefits from it
- Trade-offs analyzed explicitly
- Recommendation backed by framework and evidence
- Success metrics measurable with timelines
- Risk assessment includes likelihood/impact
- All artifacts ready for memo generation
- Session documented to enable future reference

## Related Skills

- `research-gathering`: Assembles research context
- `meeting-synthesis`: Provides customer evidence
- `strategy-memo`: Generates formal memo from session
- `citation-compliance`: Used in memo for validation
