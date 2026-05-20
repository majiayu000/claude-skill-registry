---
name: analyze
description: Deep analysis workflow for codebases, architectures, systems, products, markets, or research topics. Use when the user asks to analyze, investigate, assess, evaluate, compare, or research something in a structured way.
---

# Analyze

Perform structured analysis with explicit scope, evidence, and conclusions.

## 1. Classify the Request

Identify:

- Subject
- Core question
- Scope
- Desired depth
- Audience
- Decision the analysis should inform

## 2. Choose a Framework

Pick one to three frameworks from `analytical-frameworks.md` based on the question type.

Typical pairings:

- Current-state assessment -> gap analysis, architecture assessment
- Root cause -> 5 Whys, fishbone, causal analysis
- Comparison -> weighted scoring, MCDA
- Strategy -> SWOT, Porter's Five Forces, JTBD
- Technical assessment -> architecture review, technical debt assessment

## 3. Plan the Investigation

Break the work into MECE dimensions.

For each dimension, define:

- What evidence is needed
- Where it will come from
- What would confirm or contradict the current hypothesis

## 4. Collect Evidence

Use the minimum set of relevant sources:

- Repository files and docs
- Structured data or metrics
- Targeted commands
- Web research when current external information is required

Track evidence quality and note assumptions.

## 5. Analyze

Rules:

- Lead with evidence, not opinion
- Consider at least one alternative explanation
- State confidence explicitly
- Separate facts, inference, and recommendation

## 6. Present the Result

Use `output-templates.md` to structure the output.

All outputs should include:

- Executive summary
- Context
- Analysis
- Findings
- Recommendations
- Risks and limitations

## Companion Resources

- `analytical-frameworks.md`
- `output-templates.md`