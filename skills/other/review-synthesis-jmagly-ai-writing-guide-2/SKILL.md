# review-synthesis

Aggregate multi-reviewer feedback into consolidated, actionable recommendations.

## Triggers

- "synthesize reviews"
- "merge feedback"
- "consolidate comments"
- "combine reviewer input"
- "summarize all feedback"
- "what do reviewers say"

## Purpose

This skill aggregates feedback from multiple reviewers into cohesive, prioritized recommendations by:
- Collecting feedback from parallel review processes
- Identifying consensus and conflicts
- Prioritizing by impact and frequency
- Resolving contradictions with rationale
- Generating actionable synthesis reports

## Behavior

When triggered, this skill:

1. **Collects review inputs**:
   - Gather all reviewer feedback files
   - Parse structured and unstructured comments
   - Identify reviewer roles and expertise areas

2. **Categorizes feedback**:
   - Group by feedback type (content, design, technical, legal)
   - Tag by severity (blocking, major, minor, suggestion)
   - Map to asset sections/elements

3. **Identifies patterns**:
   - Find consensus (multiple reviewers agree)
   - Detect conflicts (reviewers disagree)
   - Note unique insights (single reviewer)

4. **Resolves conflicts**:
   - Apply priority rules
   - Document both positions
   - Provide resolution rationale
   - Flag for escalation if needed

5. **Prioritizes actions**:
   - Rank by business impact
   - Consider implementation effort
   - Group quick wins vs major changes

6. **Generates synthesis**:
   - Executive summary
   - Detailed action items
   - Conflict resolution notes
   - Approval recommendations

## Review Categories

### Content Reviews

```yaml
content_feedback:
  sources:
    - content-writer
    - editor
    - copywriter
    - content-strategist

  aspects:
    - messaging_clarity
    - value_proposition
    - tone_voice
    - cta_effectiveness
    - audience_alignment

  weight: high
  priority_in_conflict: medium
```

### Brand Reviews

```yaml
brand_feedback:
  sources:
    - brand-guardian
    - creative-director
    - art-director

  aspects:
    - visual_identity
    - verbal_identity
    - brand_consistency
    - guideline_compliance

  weight: high
  priority_in_conflict: high
```

### Technical Reviews

```yaml
technical_feedback:
  sources:
    - quality-controller
    - production-coordinator
    - technical-marketing-writer

  aspects:
    - specifications
    - file_formats
    - rendering_quality
    - platform_compatibility

  weight: medium
  priority_in_conflict: high_for_blocking
```

### Legal Reviews

```yaml
legal_feedback:
  sources:
    - legal-reviewer
    - legal-liaison

  aspects:
    - claims_substantiation
    - disclosures
    - trademark_usage
    - regulatory_compliance

  weight: critical
  priority_in_conflict: highest
```

### Strategic Reviews

```yaml
strategic_feedback:
  sources:
    - campaign-strategist
    - marketing-analyst
    - positioning-specialist

  aspects:
    - campaign_alignment
    - competitive_positioning
    - market_fit
    - kpi_potential

  weight: medium
  priority_in_conflict: medium
```

## Conflict Resolution Rules

### Priority Hierarchy

```yaml
conflict_resolution:
  priority_order:
    1: legal_compliance  # Always wins
    2: brand_guidelines  # Strong preference
    3: technical_requirements  # If blocking
    4: strategic_alignment  # Business logic
    5: content_preference  # Style choices
    6: design_preference  # Aesthetic choices

  escalation_triggers:
    - legal_vs_brand
    - strategy_vs_brand
    - multiple_blockers
    - no_clear_winner

  resolution_methods:
    consensus: Majority agreement (3+ reviewers)
    expertise: Defer to domain expert
    priority: Apply priority hierarchy
    escalate: Flag for stakeholder decision
```

### Conflict Types

```yaml
conflict_types:
  direct_contradiction:
    description: Reviewer A says X, Reviewer B says not-X
    resolution: Apply priority hierarchy
    documentation: Required

  style_preference:
    description: Different aesthetic preferences
    resolution: Defer to brand/creative director
    documentation: Optional

  scope_disagreement:
    description: Disagree on what needs changing
    resolution: Defer to strategic alignment
    documentation: Required

  priority_disagreement:
    description: Agree on issue, disagree on severity
    resolution: Take higher severity
    documentation: Optional
```

## Synthesis Report Format

```markdown
# Review Synthesis Report

**Asset**: Q1 Product Launch Campaign - Landing Page
**Reviews Collected**: 6
**Date**: 2025-12-08
**Synthesizer**: review-synthesis skill

## Executive Summary

| Metric | Count |
|--------|-------|
| Total Comments | 47 |
| Consensus Items | 28 |
| Conflicts Resolved | 8 |
| Escalations Needed | 2 |
| Blocking Issues | 3 |
| Major Issues | 12 |
| Minor Issues | 25 |
| Suggestions | 7 |

**Overall Assessment**: Asset requires revisions before approval.

## Reviewer Participation

| Reviewer | Role | Comments | Focus Areas |
|----------|------|----------|-------------|
| Sarah Chen | Brand Guardian | 12 | Visual identity, logo usage |
| Marcus Johnson | Editor | 8 | Copy clarity, grammar |
| Elena Rodriguez | Legal Reviewer | 5 | Claims, disclosures |
| David Kim | Campaign Strategist | 10 | Messaging, positioning |
| Amy Liu | Quality Controller | 7 | Technical specs |
| James Wilson | Creative Director | 5 | Overall creative |

## Consensus Items (High Confidence)

### 1. Hero Headline Needs Strengthening
- **Reviewers**: Sarah, Marcus, David (3/6 = consensus)
- **Current**: "Introducing Our New Product"
- **Issue**: Generic, doesn't communicate value
- **Recommendation**: "Cut Your Workflow Time in Half"
- **Priority**: High
- **Effort**: Low (copy change only)

### 2. CTA Button Color
- **Reviewers**: Sarah, Amy, James (3/6 = consensus)
- **Current**: Light gray (#CCCCCC)
- **Issue**: Low contrast, doesn't stand out
- **Recommendation**: Brand green (#00AA55)
- **Priority**: High
- **Effort**: Low

### 3. Missing Privacy Disclosure
- **Reviewers**: Elena (legal = authoritative)
- **Issue**: Form collects email without privacy notice
- **Requirement**: Add privacy policy link
- **Priority**: Blocking
- **Effort**: Low

## Conflicts Resolved

### Conflict 1: Product Image Style
- **Position A** (Sarah, Brand Guardian): Use lifestyle photography
- **Position B** (James, Creative Director): Use product-only shots
- **Resolution**: Lifestyle photography
- **Rationale**: Brand guidelines specify lifestyle imagery for hero sections
- **Priority Rule Applied**: Brand guidelines (priority 2)

### Conflict 2: Headline Tone
- **Position A** (Marcus, Editor): Professional, formal tone
- **Position B** (David, Strategist): Casual, conversational tone
- **Resolution**: Professional with conversational elements
- **Rationale**: Hybrid approach matches brand voice profile (Friendly Professional)
- **Priority Rule Applied**: Brand alignment via voice profile

### Conflict 3: Feature List Length
- **Position A** (David, Strategist): Show all 10 features
- **Position B** (Sarah, Brand Guardian): Limit to top 5
- **Resolution**: Top 5 features with "See all features" link
- **Rationale**: Balances completeness with visual clarity
- **Priority Rule Applied**: Consensus via compromise

## Escalations Required

### Escalation 1: Pricing Display
- **Issue**: Whether to show pricing on landing page
- **Position A** (David): Show pricing for transparency
- **Position B** (Marcus): Hide pricing, focus on value
- **Why Escalated**: Strategic decision beyond reviewer authority
- **Decision Needed From**: Marketing Director
- **Deadline**: Before final approval

### Escalation 2: Competitor Comparison
- **Issue**: Include comparison chart with competitors?
- **Position A** (David): Yes, differentiates product
- **Position B** (Elena): Risk of legal issues without substantiation
- **Why Escalated**: Legal/strategy conflict
- **Decision Needed From**: Marketing Director + Legal
- **Deadline**: Before final approval

## Action Items by Priority

### Blocking (Must Fix)

| # | Item | Owner | Effort | Source |
|---|------|-------|--------|--------|
| 1 | Add privacy disclosure | Legal | 15 min | Elena |
| 2 | Fix contrast ratio on CTA | Design | 10 min | Consensus |
| 3 | Add alt text to images | Tech | 20 min | Amy |

### High Priority

| # | Item | Owner | Effort | Source |
|---|------|-------|--------|--------|
| 4 | Revise hero headline | Copy | 30 min | Consensus |
| 5 | Update product image style | Design | 2 hrs | Conflict resolution |
| 6 | Add feature limit with "more" link | Dev | 1 hr | Conflict resolution |

### Medium Priority

| # | Item | Owner | Effort | Source |
|---|------|-------|--------|--------|
| 7 | Tighten body copy | Copy | 45 min | Marcus |
| 8 | Adjust mobile spacing | Dev | 30 min | Amy |
| 9 | Update testimonial format | Design | 1 hr | Sarah |

### Low Priority / Suggestions

| # | Item | Owner | Effort | Source |
|---|------|-------|--------|--------|
| 10 | Consider A/B test on CTA copy | Strategy | - | David |
| 11 | Add social proof counter | Dev | 2 hrs | James |
| 12 | Optimize image file sizes | Tech | 30 min | Amy |

## Revision Summary

**Total Revisions Required**: 12 action items
**Estimated Total Effort**: 8.5 hours
**Blocking Items**: 3 (must fix before approval)
**Escalations Pending**: 2 (need stakeholder decision)

## Approval Path

1. [ ] Complete blocking fixes (3 items)
2. [ ] Resolve escalations with Marketing Director
3. [ ] Complete high-priority items (3 items)
4. [ ] Re-review by Brand Guardian
5. [ ] Legal sign-off (if escalation resolved)
6. [ ] Final approval

## Appendix: Raw Feedback by Reviewer

### Sarah Chen (Brand Guardian)
[Full feedback text...]

### Marcus Johnson (Editor)
[Full feedback text...]

[etc.]
```

## Usage Examples

### Full Synthesis

```
User: "Synthesize reviews for the landing page"

Skill processes:
1. Collect reviews from .aiwg/marketing/reviews/landing-page/
2. Parse 47 total comments
3. Categorize by type and severity
4. Identify 28 consensus items
5. Resolve 8 conflicts
6. Flag 2 escalations
7. Generate prioritized action list

Output:
"Review Synthesis Complete

6 reviewers, 47 comments analyzed:
- Consensus items: 28
- Conflicts resolved: 8
- Escalations needed: 2

Blocking Issues (3):
1. Missing privacy disclosure
2. CTA contrast ratio
3. Missing alt text

Key Conflicts Resolved:
- Image style: Lifestyle (brand guidelines win)
- Headline tone: Professional with conversational elements

Report: .aiwg/marketing/synthesis/landing-page-synthesis.md"
```

### Conflict Focus

```
User: "What conflicts exist in the reviews?"

Skill identifies:
- Direct contradictions
- Style disagreements
- Priority conflicts

Output:
"8 Conflicts Found:

Resolved (6):
1. Image style (lifestyle vs product-only) → Lifestyle
2. Headline tone (formal vs casual) → Hybrid
3. Feature count (10 vs 5) → 5 with link

Needs Escalation (2):
1. Pricing display - strategic decision
2. Competitor comparison - legal concern

See full rationale in synthesis report."
```

### Quick Summary

```
User: "Summarize all feedback"

Skill generates:
- Comment counts
- Key themes
- Top action items

Output:
"Review Summary:

Top 3 Themes:
1. CTA needs more visibility (4 reviewers)
2. Hero messaging too generic (3 reviewers)
3. Legal disclosures missing (blocker)

Estimated Revision Effort: 8.5 hours
Blocking Items: 3
Approval ETA: After escalation decisions"
```

## Integration

This skill uses:
- `parallel-dispatch`: Launch multiple reviewers
- `artifact-metadata`: Track review status
- `project-awareness`: Context for priority decisions

## Agent Orchestration

```yaml
synthesis_workflow:
  input_agents:
    - brand-guardian
    - editor
    - legal-reviewer
    - campaign-strategist
    - quality-controller
    - creative-director

  synthesis_agent: documentation-synthesizer

  escalation_path:
    - marketing-project-manager
    - creative-director
    - legal-liaison
```

## Configuration

### Synthesis Rules

```yaml
synthesis_config:
  consensus_threshold: 3  # reviewers for consensus
  auto_resolve_style: true  # resolve style conflicts automatically
  escalation_timeout: 48h  # escalate if no decision

  priority_weights:
    legal: 100
    brand: 80
    technical_blocking: 75
    strategic: 60
    content: 50
    design: 40
```

### Output Settings

```yaml
output_config:
  include_raw_feedback: true
  anonymize_reviewers: false
  generate_action_tickets: true
  notify_escalation_owners: true
```

## Output Locations

- Synthesis reports: `.aiwg/marketing/synthesis/{asset}-synthesis.md`
- Action items: `.aiwg/marketing/synthesis/{asset}-actions.json`
- Escalation log: `.aiwg/marketing/escalations/`
- Raw feedback archive: `.aiwg/marketing/reviews/{asset}/`

## References

- Review templates: templates/governance/review-checklist.md
- Conflict resolution guide: docs/conflict-resolution.md
- Escalation procedures: docs/escalation-process.md
