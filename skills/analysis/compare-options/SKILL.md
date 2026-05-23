---
name: compare-options
description: >
  Multi-expert comparison and ranking of options with structured deliberation.
  PROACTIVELY activate for: (1) decision making between alternatives, (2) trade-off analysis,
  (3) option evaluation, (4) vendor/tool comparison, (5) strategy selection.
  Triggers: "compare options", "evaluate alternatives", "rank options", "which should I choose",
  "compare these", "trade-off analysis", "decision between"
argument-hint: [options as comma-separated list or description]
---

# Compare Options

Multi-expert comparison and ranking of options using structured deliberation.

## When to Use

Use this skill when you need to:
- Compare multiple alternatives systematically
- Evaluate trade-offs between options
- Get diverse expert perspectives on a decision
- Rank options with transparent criteria
- Make decisions with documented rationale

## Workflow

Invoke the `expert-panel-deliberation` skill for:

Options to compare: $ARGUMENTS

### Default Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `panel_size` | 5 | Diverse perspectives without analysis paralysis |
| `output_format` | ranking | Produces prioritized list with scores |
| `deliberation_depth` | standard | Balanced thoroughness |
| `include_challenger` | true | Include devil's advocate perspective |
| `consensus_required` | false | Allow minority opinions |

### Expert Panel Assembly

The panel is dynamically composed based on the decision domain:

**For Technical Decisions:**
- Solution Architect
- Performance Specialist
- Security Expert
- DevOps/Operations
- End User Advocate

**For Business Decisions:**
- Strategic Planner
- Financial Analyst
- Market Expert
- Operations Lead
- Customer Representative

**For Product Decisions:**
- Product Strategist
- UX Designer
- Engineering Lead
- Business Analyst
- Customer Advocate

### Deliberation Process

#### Round 1: Independent Assessment
Each expert evaluates all options against criteria:
- Scores each option (1-10) on their specialty dimensions
- Documents key strengths and weaknesses
- Identifies critical risks or blockers

#### Round 2: Cross-Examination
Experts challenge each other's assessments:
- Surface hidden assumptions
- Probe trade-off implications
- Identify overlooked factors

#### Round 3: Synthesis
Panel converges on:
- Weighted ranking of options
- Key trade-offs documented
- Recommended choice with rationale
- Conditions under which ranking changes

### Evaluation Criteria Framework

Standard criteria (customized to domain):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Effectiveness | 25% | How well does it solve the core problem? |
| Cost/Effort | 20% | Total cost of ownership, implementation effort |
| Risk | 20% | What can go wrong? Likelihood and impact |
| Scalability | 15% | Does it grow with needs? |
| Reversibility | 10% | Can we change course if needed? |
| Time to Value | 10% | How quickly do we see benefits? |

## Output Format

The comparison produces:

```xml
<option-comparison>
  <header>
    <id>[unique identifier]</id>
    <decision_context>[What we're deciding]</decision_context>
    <options_count>[number of options]</options_count>
  </header>

  <options>
    <option id="[A|B|C|...]" name="[option name]">
      <description>[Brief description]</description>
    </option>
  </options>

  <expert-panel>
    <expert role="[role]" specialty="[area]">
      <scores>
        <score option="A" value="[1-10]" rationale="[brief reason]"/>
        <score option="B" value="[1-10]" rationale="[brief reason]"/>
      </scores>
      <recommendation>[Expert's top pick and why]</recommendation>
    </expert>
    <!-- ... more experts ... -->
  </expert-panel>

  <deliberation-summary>
    <consensus_points>
      <point>[What experts agreed on]</point>
    </consensus_points>
    <debate_points>
      <point>[Where experts disagreed and resolution]</point>
    </debate_points>
  </deliberation-summary>

  <final-ranking>
    <rank position="1" option="[option]" score="[weighted score]">
      <rationale>[Why this is ranked first]</rationale>
      <caveats>[When this might not be the best choice]</caveats>
    </rank>
    <rank position="2" option="[option]" score="[weighted score]">
      <rationale>[Why second]</rationale>
      <when_preferred>[Conditions where this beats #1]</when_preferred>
    </rank>
    <!-- ... more ranks ... -->
  </final-ranking>

  <trade-off-matrix>
    <trade-off>
      <options>[Option A vs Option B]</options>
      <dimension>[What you trade off]</dimension>
      <analysis>[Detailed trade-off analysis]</analysis>
    </trade-off>
  </trade-off-matrix>

  <recommendation>
    <primary>[Top recommended option]</primary>
    <confidence>[high|medium|low]</confidence>
    <conditions>[When this recommendation applies]</conditions>
    <alternative>[When to choose differently]</alternative>
  </recommendation>

  <next-steps>
    <step>[Concrete action to proceed]</step>
  </next-steps>
</option-comparison>
```

## Quality Gates

- [ ] All options fairly represented
- [ ] Criteria weights appropriate for context
- [ ] Each expert provided independent assessment
- [ ] Trade-offs explicitly documented
- [ ] Minority opinions captured
- [ ] Recommendation includes confidence and conditions
- [ ] Next steps are actionable

## Related Skills

After comparing options, consider:
- Run `/research-brief` to deep-dive on top choice
- Run `/write-howto` for implementation guide
- Run `/evaluate-schema` if choice involves data design
- Run `/optimize-prompt` if choice involves AI/prompting
