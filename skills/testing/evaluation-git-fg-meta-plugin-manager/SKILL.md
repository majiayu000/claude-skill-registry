---
name: evaluation
description: "Evaluate agent systems with quality gates and LLM-as-judge. Use when you need to measure component quality or implement quality gates. Not for simple unit testing or binary pass/fail checks without nuance."
---

# Evaluation Methods for Agent Systems

<mission_control>
<objective>Build quality gates and measure component quality using outcome-focused evaluation that accounts for non-determinism and multiple valid paths</objective>
<success_criteria>Multi-dimensional rubric implemented with weighted scoring, evidence requirements, and threshold-based quality gates</success_criteria>
</mission_control>

<trigger>When building quality gates, measuring component quality, or implementing LLM-as-judge. Not for: Simple unit testing or binary pass/fail checks without nuance.</trigger>

<interaction_schema>
DEFINE_RUBRIC → BUILD_TEST_SET → IMPLEMENT_EVALUATION → TRACK_METRICS
</interaction_schema>

Agent evaluation requires outcome-focused approaches that account for non-determinism and multiple valid paths. A robust framework enables continuous improvement, catches regressions, and validates that context engineering choices achieve intended effects.

## Core Concepts

### The 95% Finding

Research on BrowseComp evaluation (which tests browsing agents' ability to locate hard-to-find information) found three factors explain 95% of performance variance:

| Factor               | Variance Explained | Implication                       |
| -------------------- | ------------------ | --------------------------------- |
| Token usage          | 80%                | More tokens = better performance  |
| Number of tool calls | ~10%               | More exploration helps            |
| Model choice         | ~5%                | Better models multiply efficiency |

**Critical Insight**: Model upgrades often provide larger gains than doubling token budgets. Claude Sonnet 4.5 > 2× tokens on previous Sonnet.

### Evaluation Challenges

**Non-Determinism and Multiple Valid Paths**

- Agents may take different valid paths to goals
- Traditional evaluations checking specific steps fail
- Solution: Outcome-focused evaluation judging results, not paths

**Context-Dependent Failures**

- Success on simple queries ≠ success on complex ones
- Failures emerge only after extended interaction
- Solution: Test across complexity levels, include extended interactions

**Composite Quality Dimensions**

- Agent quality is multi-dimensional
- Includes: factual accuracy, completeness, coherence, tool efficiency
- Solution: Multi-dimensional rubrics with appropriate weighting

## Evaluation Framework

### Multi-Dimensional Rubrics

**Design Principles**:

- Cover key quality dimensions
- Use descriptive levels (excellent, good, fair, poor, failed)
- Convert to numeric scores (0.0 to 1.0)
- Weight dimensions based on use case

**Core Dimensions**:

**Factual Accuracy**

- Claims match ground truth
- 1.0: All facts correct, no hallucinations
- 0.7: Mostly correct, minor inaccuracies
- 0.5: Mixed accuracy, some errors
- 0.3: Many errors, significant inaccuracies
- 0.0: Mostly false, major hallucinations

**Completeness**

- Output covers all requested aspects
- 1.0: Addresses all requirements comprehensively
- 0.7: Covers most requirements with minor gaps
- 0.5: Partial coverage, missing some aspects
- 0.3: Minimal coverage, many gaps
- 0.0: Fails to address core requirements

**Portability** (Seed System Specific)

- Component works without external dependencies
- 1.0: Zero dependencies, self-contained, portable
- 0.7: Minimal dependencies, mostly portable
- 0.5: Some dependencies, requires configuration
- 0.3: Many dependencies, limited portability
- 0.0: Tightly coupled, non-portable

**Context Efficiency** (Seed System Specific)

- Uses context optimally (progressive disclosure)
- 1.0: Excellent use of progressive disclosure, minimal context
- 0.7: Good context management, some optimization
- 0.5: Adequate context usage, could be improved
- 0.3: Inefficient context usage, verbose
- 0.0: Wasteful context usage, bloats prompts

**Tool Efficiency**

- Uses appropriate tools reasonable number of times
- 1.0: Optimal tool selection, minimal calls
- 0.7: Good tool usage, slightly inefficient
- 0.5: Adequate tool usage, some redundancy
- 0.3: Inefficient tool usage, many redundant calls
- 0.0: Poor tool selection, excessive calls

### Scoring System

**Individual Dimension Scores**: 0.0 to 1.0 for each dimension

**Weighted Overall Score**:

```python
overall_score = sum(score[dim] * weight[dim] for dim in dimensions)
```

**Pass Threshold**: Set based on use case

- Production components: ≥ 0.8
- Development components: ≥ 0.7
- Experimental: ≥ 0.6

### LLM-as-Judge Pattern

**Direct Scoring**

- Evaluate against weighted criteria with rubrics
- Provide clear task description
- Include agent output and ground truth (if available)
- Request structured judgment with evidence

**Prompt Template**:

```
Task: [Description]
Agent Output: [Output]
Evaluation Criteria: [Rubric]

Evaluate the agent output on each dimension:
1. Factual Accuracy (0.0-1.0): [Score] - [Evidence]
2. Completeness (0.0-1.0): [Score] - [Evidence]
3. Portability (0.0-1.0): [Score] - [Evidence]
4. Context Efficiency (0.0-1.0): [Score] - [Evidence]
5. Tool Efficiency (0.0-1.0): [Score] - [Evidence]

Overall Score: [Weighted average]
Pass/Fail: [Threshold-based]
```

**Pairwise Comparison**

- Compare two outputs with position bias mitigation
- Automatically swap positions to reduce bias
- Ask judge to choose better overall output

**Position Swapping**:

```python
def evaluate_pairwise(output_a, output_b):
    # First comparison: A vs B
    result_1 = judge_evaluate(output_a, output_b)

    # Second comparison: B vs A (swapped)
    result_2 = judge_evaluate(output_b, output_a)

    # Combine results
    return reconcile_comparisons(result_1, result_2)
```

## Evaluation Methods

### Test Set Design

**Sample Selection**

- Start small during development (dramatic impacts early)
- Sample from real usage patterns
- Add known edge cases
- Ensure coverage across complexity levels

**Complexity Stratification**

- **Simple**: Single tool call, clear requirements
- **Medium**: Multiple tool calls, some ambiguity
- **Complex**: Many tool calls, significant ambiguity
- **Very Complex**: Extended interaction, deep reasoning

### Context Engineering Evaluation

**Testing Context Strategies**

- Run with different context strategies on same test set
- Compare quality scores, token usage, efficiency metrics
- Validate progressive disclosure effectiveness

**Degradation Testing**

- Test at different context sizes
- Identify performance cliffs
- Establish safe operating limits

### Continuous Evaluation

**Evaluation Pipeline**

- Run automatically on component changes
- Track results over time
- Compare versions to identify improvements/regressions

**Production Monitoring**

- Sample interactions in production
- Evaluate randomly
- Set alerts for quality drops

## Practical Implementation

### Building Evaluation Frameworks

**Step 1**: Define quality dimensions relevant to use case
**Step 2**: Create rubrics with clear level descriptions
**Step 3**: Build test sets from real patterns and edge cases
**Step 4**: Implement automated evaluation pipelines
**Step 5**: Establish baseline metrics before changes
**Step 6**: Run evaluations on all significant changes
**Step 7**: Track metrics over time
**Step 8**: Supplement with human review

### Example: Component Evaluation

```python
def evaluate_component(component, test_set):
    """Evaluate a Seed System component"""

    rubric = {
        "factual_accuracy": {"weight": 0.25},
        "completeness": {"weight": 0.25},
        "portability": {"weight": 0.25},
        "context_efficiency": {"weight": 0.15},
        "tool_efficiency": {"weight": 0.10}
    }

    scores = {}
    for test in test_set:
        result = run_test(component, test)
        for dimension in rubric:
            scores[dimension] = assess_dimension(result, dimension)

    overall = weighted_average(scores, rubric)
    passed = overall >= 0.7

    return {
        "passed": passed,
        "scores": scores,
        "overall": overall,
        "threshold": 0.7
    }
```

## Avoiding Evaluation Pitfalls

❌ **Overfitting to specific paths**

- Evaluate outcomes, not specific steps

❌ **Ignoring edge cases**

- Include diverse test scenarios

❌ **Single-metric obsession**

- Use multi-dimensional rubrics

❌ **Neglecting context effects**

- Test with realistic context sizes

❌ **Skipping human evaluation**

- Automated evaluation misses subtle issues

## Enhanced Validation Workflow

**Phase 1: Component Generation**

- Generate component using meta-skills
- Apply progressive disclosure principles
- Optimize context usage

**Phase 2: Multi-Dimensional Evaluation**

- Run through evaluation framework
- Score on all 5 dimensions
- Calculate weighted overall score

**Phase 3: Quality Gate**

- Block if below threshold (e.g., 0.7)
- Provide detailed feedback
- Suggest improvements

**Phase 4: Evidence Collection**

- Store evaluation results
- Track metrics over time
- Enable regression detection

### Example: Validation Report

```yaml
# Validation Report
component: my-skill
timestamp: 2026-01-26
overall_score: 0.82
threshold: 0.70
passed: true

dimensions:
  factual_accuracy: 0.90
    evidence: "All technical claims verified"
  completeness: 0.85
    evidence: "Covers all requirements with minor gaps"
  portability: 0.80
    evidence: "Self-contained, zero external dependencies"
  context_efficiency: 0.75
    evidence: "Good progressive disclosure, some optimization possible"
  tool_efficiency: 0.85
    evidence: "Optimal tool selection, minimal redundant calls"

recommendations:
  - "Consider further context optimization for large components"
  - "Add more examples to references/"
```

## Guidelines

1. **Judge outcomes, not paths** - Multiple valid routes to goals
2. **Use multi-dimensional rubrics** - Quality is composite
3. **Test across complexity levels** - Simple ≠ Complex
4. **Implement position swapping** - Mitigate pairwise bias
5. **Require evidence** - Justify all scores
6. **Track over time** - Detect regressions
7. **Combine automated and human** - Catch what automation misses
8. **Test context strategies** - Validate progressive disclosure

## References

<routing_table>
Skills referenced for related evaluation capabilities.

| When You Need To...                  | Use This Skill       | Routing Command               |
| ------------------------------------ | -------------------- | ----------------------------- |
| Implement progressive disclosure     | `filesystem-context` | `Skill("filesystem-context")` |
| Validate component quality           | `quality-standards`  | `Skill("quality-standards")`  |
| Build evaluation rubrics and scoring | (this skill)         | (current context)             |

**Research References**:

- BrowseComp evaluation on performance drivers
- Eugene Yan on LLM-evaluators
- Position bias in pairwise comparison

**Key Principle**: Evaluation should be outcome-focused, multi-dimensional, and continuously validated. Judge whether components achieve right outcomes while following reasonable processes.
</routing_table>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming
  MANDATORY: Use multi-dimensional rubrics (not single metrics)
  MANDATORY: Require evidence for all scores
  MANDATORY: Implement position swapping for pairwise comparisons
  MANDATORY: Block below threshold (≥0.7 for production)
  No exceptions. Evaluation without evidence is opinion, not assessment.
  </critical_constraint>
