---
name: strategy-memo
description: Use when creating formal strategy memo from session or standalone - systematic extraction, framework-driven analysis, evidence-based recommendations with citation rigor
---

# Strategy Memo

## Purpose

Generate formal strategic decision memo with:
- Systematic content extraction from session artifacts
- Framework-based analysis and stakeholder mapping
- Evidence-based recommendations with quantitative grounding
- MECE structure (Problem→Evidence→Options→Recommendation)
- Full citation compliance with verbatim source quotes

## When to Use

Activate when:
- User invokes `/strategy:memo`
- After strategy-session completion
- Standalone strategic decision documentation needed

## Input Requirements

### From Completed Session (Preferred)

**Required Session Artifacts:**
- `context.md` - Research context and sources assembled
- `framework.md` - Framework applied and analysis
- `session-log.md` - Decision-making process record
- `recommendations.md` - Final recommendations and rationale

**Validation:**
- Session must be "completed" (has clear recommendation)
- All required files exist with substantive content
- Decision rationale documented with evidence

### Standalone Memo (Alternative)

If no session exists:
1. **Ask user** for decision question and context
2. **Invoke:** `research-gathering` skill for evidence base
3. **Invoke:** `meeting-synthesis` skill for customer signals
4. Build memo directly from assembled context

## Memo Generation Process

### Step 1: Content Extraction

**From Session Artifacts:**

Extract systematically (don't construct narrative):
- **Decision Question**: From session-log.md header
- **Problem Context**: From context.md situation analysis
- **Research Evidence**: Key insights from assembled sources (with citations)
- **Framework Analysis**: From framework.md with specific findings
- **Stakeholder Analysis**: If framework included stakeholder mapping
- **Options Analysis**: From session-log.md with pros/cons/evidence
- **Recommendation**: From recommendations.md with rationale
- **Success Metrics**: From recommendations.md measurement criteria
- **Risk Analysis**: From session discussion and framework application

**Quality Check:**
- Do NOT add content not present in session
- Do NOT generalize specific findings into abstractions
- Preserve quantitative data (percentages, targets, metrics)
- Keep concrete examples and scenarios from session

### Step 2: Framework Application

**If framework was used in session:**
- Include framework name and key components analyzed
- Reference specific framework findings (e.g., "Porter's Five Forces: Buyer power HIGH due to...")
- Map framework insights to recommendation rationale

**If stakeholder framework was applied:**
- Include explicit stakeholder mapping table
- Document stakeholder interests and decision impact
- Reference in options analysis

**If no framework in session:**
- Recommend appropriate framework for decision type
- Note limitation in memo ("Framework recommendation: [X] for future similar decisions")

### Step 3: MECE Structure Assembly

**Required Structure:**

```markdown
---
title: "[Decision Title from Session]"
date: "[YYYY-MM-DD]"
author: "[Author Name]"
decision_type: "[strategic|tactical|operational]"
topic: "[Topic from Session]"
status: "[draft|final]"
stakeholders: ["[From Session]"]
context_session: "[Path to Session Folder]"
---

# [Decision Title]

## Problem Statement

[Clear, 1-2 sentence statement of decision requirement. Extract from session, don't editorialize.]

## Key Evidence & Analysis

[Decision-relevant insights from research context with citations]

### Research Findings

[Synthesize key research insights that inform decision. Include citations with verbatim quotes.]

**Example:**
"Competitor X's pricing change resulted in 30% customer churn within 60 days."[^1]

[^1]: Competitive Analysis Report (path/to/source.md): "The forced migration to new pricing tiers resulted in 30% of enterprise customers churning within the first 60 days of implementation."

### Customer/Market Signals

[From meeting synthesis if relevant. Include specific customer quotes or patterns.]

### Framework Applied

[Framework name and key findings]

**Example (Porter's Five Forces):**
- **Supplier Power**: LOW - Multiple vendor alternatives available
- **Buyer Power**: HIGH - Customers can switch with minimal cost
- **Competitive Rivalry**: HIGH - 5 direct competitors with similar offerings
- **Threat of Substitution**: MEDIUM - DIY solutions viable for some segments
- **New Entrants**: LOW - High technical barrier to entry

[Map framework findings to decision implications]

### Stakeholder Analysis (If Applicable)

[If session included stakeholder mapping]

| Stakeholder | Interest | Impact | Mitigation |
|-------------|----------|--------|------------|
| [Name] | [Interest] | [High/Med/Low] | [Strategy] |

### Options Considered

[For each option analyzed in session:]

**Option 1: [Name]**

**Description**: [What this option entails - from session]

**Pros**:
- [Advantage with evidence source]
- [Advantage with evidence source]

**Cons**:
- [Disadvantage with evidence or risk]
- [Disadvantage with evidence or risk]

**Expected Impact**: [Quantitative where available]
- [Metric 1]: [Expected change from session analysis]
- [Metric 2]: [Expected change from session analysis]

**Risk Level**: [Low|Medium|High - from session assessment]

[Repeat for each option]

**Trade-off Analysis**: [Systematic comparison if session included]

## Recommendation

**We recommend: Option [N] - [Name]**

**Rationale** (from session recommendations.md):
1. [Reason backed by research/framework]
2. [Reason backed by customer signals]
3. [Reason backed by risk analysis]

**Expected Outcomes** (from session):
- [Outcome 1 with metric if available]
- [Outcome 2 with metric if available]

**Success Metrics** (from session):
- [How we'll measure success - specific, measurable]
- [Timeline for evaluation]

## Implementation Considerations

[Strategic guidance from session - NOT project plan]

**Key Dependencies**: [From session analysis]

**Critical Decision Points**: [Gates or thresholds identified in session]

**Timeline** (high-level only): [Strategic phases if session identified]

**Risk Management**:

[For each risk identified in session:]

**Risk [N]: [Description]**
- **Likelihood**: [Low|Medium|High]
- **Impact**: [Low|Medium|High]
- **Mitigation**: [Strategy from session]
- **Trigger/Threshold** (if specified): [When to escalate or pivot]

## Sources & Citations

[Full reference list following citation standards]

**Research Sources**:
[^1]: [Source path/title]: "[5-25 word verbatim quote]"
[^2]: [Source path/title]: "[5-25 word verbatim quote]"

**Internal Context**:
- [Meeting references with dates and key points]
- [Product roadmap references if relevant]

**Session Documentation**:
- Generated from: [Session folder path]
- Session date: [Date]
- Framework applied: [Framework name]
- Participants: [If documented]

---

## Appendix (Optional)

[Include only if session had detailed supporting analysis]

**Scenario Analysis** (if session included concrete scenarios)
**Economic Model** (if session included cost/revenue projections)
**Technical Details** (if session included architecture/implementation specifics)
```

### Step 4: Citation Compliance Validation

**Invoke:** `citation-compliance` skill

**Requirements:**
- All factual claims must have sources
- Research sources require verbatim quotes (5-25 words)
- All citations must be accessible (verify paths)
- Internal meeting references must include dates and context

**Validation:**
- Read each cited source file
- Confirm verbatim quote exists in source
- No "(source needed)" markers allowed
- Flag any unsupported claims

**If citation validation fails:**
- STOP memo generation
- Report missing/invalid citations
- User must update session artifacts or provide sources

### Step 5: Quality Gates

**Structure Validation:**
- [ ] Problem statement clear and concise (1-2 sentences)
- [ ] Evidence section includes research with citations
- [ ] Framework applied (or absence noted with recommendation)
- [ ] All options from session included with pros/cons
- [ ] Recommendation clear and actionable
- [ ] Success metrics specific and measurable
- [ ] Risk analysis includes likelihood/impact
- [ ] Citations complete with verbatim quotes

**Content Validation:**
- [ ] Quantitative data preserved from session (no vague abstractions)
- [ ] Concrete examples/scenarios from session included
- [ ] MECE structure maintained (no overlap between sections)
- [ ] No unsupported projections or speculation
- [ ] Appropriate detail level for decision type
- [ ] Strategic focus (no implementation project planning)

**Completeness Check:**
- [ ] All session recommendations reflected in memo
- [ ] Framework findings integrated into rationale
- [ ] Stakeholder analysis included (if session had it)
- [ ] Risk mitigation strategies documented
- [ ] Success criteria measurable

**Flag for revision if:**
- Missing economic analysis for pricing/investment decisions
- Missing customer impact for user-facing decisions
- Missing competitive analysis for positioning decisions
- Vague recommendations without clear action
- Implementation details mixed with strategy
- Excessive background relative to decision content

## File Management

### Naming Convention
- **Pattern**: `{YYYY}-{MM-DD}_{decision-slug}.md`
- **Location**: `/datasets/strategy/memos/{YYYY}/`

### Archive Management (If from session)
After memo generation:
1. **Session Archive**: Move session folder to `/datasets/strategy/archive/{YYYY}/`
2. **Link Preservation**: Memo includes link back to archived session
3. **Version Control**: If memo needs updates, create `{slug}_v2.md`

### Integration Points
- **Future Sessions**: Memo becomes context for related decisions
- **Research System**: Memo insights can seed new research sources
- **Product Planning**: Link strategic decisions to roadmap
- **Meeting References**: Include memo in future strategic discussions

## Output

**Write to:** `datasets/strategy/memos/{YYYY}/{MM-DD}_{decision-slug}.md`

**Announce:**
```
📝 Strategy Memo Generated

**Decision**: [Title]
**Framework**: [Framework used]
**Sources**: [N research sources, M meetings cited]
**Path**: [File path]

**Recommendation**: [One sentence summary]

**Next**: Review memo, share with stakeholders, or invoke `/strategy:session` for related decision
```

## Success Criteria

- Memo extracted systematically from session (not narrative construction)
- MECE structure maintained (Problem→Evidence→Options→Recommendation)
- Framework analysis integrated with clear findings
- Options include concrete examples/scenarios from session
- Quantitative data preserved (percentages, targets, metrics)
- Citations validated with verbatim quotes
- Risk analysis includes likelihood/impact
- Success metrics specific and measurable
- Quality gates passed before file write

## Related Skills

- `strategy-session`: Generates input session for memo
- `citation-compliance`: Validates source backing
- `research-gathering`: Provides research context
- `meeting-synthesis`: Provides customer evidence
- `source-integrity`: Checks research source validity
