---
name: agent-evals
description: Design and implement evaluation frameworks for AI agents. Use when testing agent reasoning quality, building graders, doing error analysis, or establishing regression protection. Framework-agnostic concepts that apply to any SDK.
---

# Agent Evaluations: Measuring Reasoning Quality

**Core Thesis**: "One of the biggest predictors for whether someone is able to build agentic workflows really well is whether or not they're able to drive a really disciplined evaluation process." — Andrew Ng

Evaluations (evals) are exams for your agent's reasoning. Unlike traditional testing (TDD) that checks code correctness with PASS/FAIL outcomes, evals measure reasoning quality with probabilistic scores. The distinction is critical:

| Aspect | TDD (Code Testing) | Evals (Agent Evaluation) |
|--------|-------------------|-------------------------|
| **Tests** | Does function return correct output? | Did agent make the right decision? |
| **Outcome** | PASS or FAIL (deterministic) | Scores (probabilistic) |
| **Example** | "Does get_weather() return valid JSON?" | "Did agent correctly interpret user intent?" |
| **Analogy** | Testing if calculator works | Testing if student knows WHEN to use multiplication |

## When to Activate

Activate this skill when:
- Building systematic quality checks for any AI agent
- Designing evaluation datasets (typical, edge, error cases)
- Creating graders to define "good" automatically
- Performing error analysis to find failure patterns
- Setting up regression protection for agent changes
- Deciding when to use end-to-end vs component-level evals

## Core Concepts

### 1. Evals as Exams

Think of evals like course exams for your agent:

| Eval Type | Analogy | Purpose |
|-----------|---------|---------|
| **Initial Eval** | Final exam | Does agent pass the course? Handles all scenarios? |
| **Regression Eval** | Pop quiz | Did the update break what was working? |
| **Component Eval** | Subject test | Test individual skills (routing, tool use, output) |
| **End-to-End Eval** | Comprehensive exam | Test the full experience |

### 2. The Two Evaluation Axes

Evals vary on two dimensions:

|  | **Objective (Code)** | **Subjective (LLM Judge)** |
|---|---|---|
| **Per-example ground truth** | Invoice dates, expected values | Gold standard talking points |
| **No per-example ground truth** | Word count limits, format rules | Rubric-based grading |

**Examples**:
- Invoice date extraction: Objective + per-example ground truth
- Marketing copy length: Objective + no per-example ground truth
- Research article quality: Subjective + per-example ground truth
- Chart clarity rubric: Subjective + no per-example ground truth

### 3. Graders

**What**: Automated quality checks that turn subjective assessment into measurable scores.

**Key Insight**: Don't use 1-5 scales (LLMs are poorly calibrated). Use **binary criteria** instead:

```
❌ BAD: "Rate this response 1-5 on quality"

✅ GOOD: "Check these 5 criteria (yes/no each):
   1. Does it have a clear title?
   2. Are axis labels present?
   3. Is it the appropriate chart type?
   4. Is the data accurately represented?
   5. Is the legend clear?"
```

Binary criteria → sum up → get reliable scores (0-5).

**LLM-as-Judge Pattern**:
```
Determine how many of the 5 gold standard talking points are present
in the provided essay.

Talking points: {talking_points}
Essay: {essay_text}

Return JSON: {"score": <0-5>, "explanation": "..."}
```

**Position Bias**: Many LLMs prefer the first option when comparing two outputs. Avoid pairwise comparisons; use rubric-based grading instead.

### 4. Error Analysis (Most Critical Skill)

**The Build-Analyze Loop**:
```
Build → Look at outputs → Find issues → Build evals → Improve → Repeat
```

**Don't guess what's wrong—MEASURE**:

1. **Build spreadsheet**: Case | Component | Error Type
2. **Count patterns**: "45% of errors from web search results"
3. **Focus effort where errors cluster**
4. **Prioritize by**: Error frequency × Feasibility to fix

**Trace Analysis Terminology**:
- **Trace**: All intermediate outputs from agent run
- **Span**: Output of a single step
- **Error Analysis**: Reading traces to find which component caused failures

**Example Error Analysis Table**:
| Prompt | Search Terms | Search Results | Best Sources | Final Output |
|--------|-------------|---------------|--------------|--------------|
| Black holes | OK | Too many blogs (45%) | OK | Missing key points |
| Seattle rent | OK | OK | Missed blog | OK |
| Fruit robots | Generic (5%) | Poor quality | Poor | Missing company |

### 5. End-to-End vs Component-Level Evals

**End-to-End Evals**:
- Test entire agent output quality
- Expensive to run (full workflow)
- Noisy (multiple components introduce variance)
- Use for: Ship decisions, production monitoring

**Component-Level Evals**:
- Test single component in isolation
- Faster, clearer signal
- Use for: Debugging, tuning specific components
- Example: Eval just the web search quality, not full research agent

**Decision Framework**:
1. Start with end-to-end to find overall quality
2. Use error analysis to identify problem component
3. Build component-level eval for that component
4. Tune component using component eval
5. Verify improvement with end-to-end eval

### 6. Dataset Design

**Quality Over Quantity**: Start with 10-20 high-quality cases, NOT 1000 random ones.

**Three Categories**:
| Category | Count | Purpose |
|----------|-------|---------|
| **Typical** | 10 | Common use cases |
| **Edge** | 5 | Unusual but valid inputs |
| **Error** | 5 | Should fail gracefully |

**Use REAL Data**: Pull from actual user queries, support tickets, production logs. Synthetic data misses the messiness of reality.

**Grow Dataset Over Time**: When evals fail to capture your judgment about quality, add more cases to fill the gap.

### 7. Regression Protection

**Run evals on EVERY change**:
```
Change code → Run eval suite → Compare to baseline
  ↓
If pass rate drops → Investigate before shipping
  ↓
If pass rate stable/improved → Safe to deploy
```

**The Eval-Driven Development Loop**:
```
prompt v1 → eval 70% → error analysis → fix routing → eval 85%
         → error analysis → fix output format → eval 92%
         → ship
```

## Practical Guidance

### Building Quick-and-Dirty Evals

1. **Start immediately** (don't wait for perfect)
2. **10-20 examples** is fine to start
3. **Look at outputs manually** alongside metrics
4. **Iterate on evals** as you iterate on agent
5. **Upgrade evals** when they fail to capture your judgment

### Creating Effective Graders

```python
# Grader for structured feedback
def grader_feedback_structure(output: dict) -> dict:
    """
    Check if feedback follows required structure:
    1. Strengths section present
    2. Gaps section present
    3. Actionable suggestions present
    """
    feedback = output.get("student_feedback", "")

    checks = {
        "has_strengths": "strength" in feedback.lower(),
        "has_gaps": "improvement" in feedback.lower() or "gap" in feedback.lower(),
        "has_actions": "suggest" in feedback.lower() or "recommend" in feedback.lower()
    }

    score = sum(checks.values())
    return {
        "passed": score == 3,
        "score": score,
        "checks": checks,
        "explanation": f"Passed {score}/3 structure checks"
    }
```

### LLM Grader Template

```python
GRADER_PROMPT = """
Evaluate the agent response against these criteria:

Response: {response}
Criteria: {criteria}

For each criterion, answer YES or NO:
{criteria_list}

Return JSON:
{
  "criteria_results": {"criterion_1": true/false, ...},
  "total_passed": <count>,
  "total_criteria": <count>,
  "passed": <true if all passed>
}
"""
```

### Error Analysis Workflow

```python
def analyze_errors(test_results: list) -> dict:
    """
    Systematic error analysis across test cases.
    """
    error_counts = {
        "routing": 0,
        "tool_selection": 0,
        "output_format": 0,
        "content_quality": 0,
        "other": 0
    }

    for result in test_results:
        if not result["passed"]:
            # Analyze trace to find error source
            error_type = classify_error(result["trace"])
            error_counts[error_type] += 1

    # Prioritize by frequency
    total_errors = sum(error_counts.values())
    return {
        "error_counts": error_counts,
        "percentages": {
            k: v / total_errors * 100
            for k, v in error_counts.items() if total_errors > 0
        },
        "recommendation": max(error_counts, key=error_counts.get)
    }
```

## The Complete Quality Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE EVAL-DRIVEN LOOP                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   1. BUILD quick-and-dirty agent v1                             │
│        ↓                                                        │
│   2. CREATE eval dataset (10-20 cases)                          │
│        ↓                                                        │
│   3. RUN evals → Find 70% pass rate                             │
│        ↓                                                        │
│   4. ERROR ANALYSIS → "45% errors from routing"                 │
│        ↓                                                        │
│   5. FIX routing → Re-run evals → 85% pass rate                 │
│        ↓                                                        │
│   6. ERROR ANALYSIS → "30% errors from output format"           │
│        ↓                                                        │
│   7. FIX format → Re-run evals → 92% pass rate                  │
│        ↓                                                        │
│   8. DEPLOY with regression protection                          │
│        ↓                                                        │
│   9. MONITOR production → Add failed cases to dataset           │
│        ↓                                                        │
│   10. REPEAT (continuous improvement)                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | What to Do Instead |
|-------------|--------------|-------------------|
| Waiting for perfect evals | Delays useful feedback | Start with 10 quick cases |
| 1000+ test cases first | Quantity without quality | 20 thoughtful cases |
| 1-5 scale ratings | LLMs poorly calibrated | Binary criteria summed |
| Ignoring traces | Miss root cause | Read intermediate outputs |
| End-to-end only | Too noisy for debugging | Add component-level evals |
| Synthetic test data | Misses real-world messiness | Use actual user queries |
| Going by gut | May work on wrong component | Count errors systematically |
| Skipping regression tests | Breaks working features | Run evals on every change |

## Integration with Other Skills

This skill connects to:
- **building-with-openai-agents**: Evaluating OpenAI agents specifically
- **building-with-claude-agent-sdk**: Evaluating Claude agents
- **building-with-google-adk**: Evaluating Google ADK agents
- **evaluation**: Broader context engineering evaluation
- **context-degradation**: Detecting context-related failures

## Framework-Agnostic Application

These concepts apply to ANY agent framework:

| Framework | Trace Access | Grader Integration | Dataset Storage |
|-----------|-------------|-------------------|-----------------|
| OpenAI Agents SDK | Built-in tracing | Custom graders | JSON/CSV files |
| Claude Agent SDK | Hooks for tracing | Custom graders | JSON/CSV files |
| Google ADK | Evaluation module | Built-in graders | Vertex AI datasets |
| LangChain | LangSmith traces | LangSmith evals | LangSmith datasets |
| Custom | Logging middleware | Custom graders | Any storage |

The thinking is portable. The skill is permanent.

---

## Skill Metadata

**Created**: 2025-12-30
**Source**: Andrew Ng's Agentic AI Course + OpenAI AgentKit Build Hour
**Author**: Claude Agent Factory
**Version**: 1.0.0
