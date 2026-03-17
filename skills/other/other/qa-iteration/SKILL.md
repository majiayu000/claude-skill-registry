---
name: qa-iteration
version: "1.0.0"
description: "Assess and improve report quality. Use when the user asks to check, grade, review, or improve a research report."

tools:
  - run_qa
  - research_company

resources:
  - file://references/scoring

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY
---

# QA Iteration

Primr grades reports on a 0-100 scale across four dimensions. See `references/scoring.md` for the scoring framework and common issues.

## Operational Capabilities

### Run Quality Assessment

```
run_qa(company="Acme Corp")
run_qa(file_path="output/acme_corp/report.docx")
run_qa(company="Acme Corp", detailed=True)
```

### Interpret Results

The result includes an overall score, per-dimension scores (clarity, completeness, insight depth, accuracy), and per-section feedback with specific issues.

### Section Refinement

For sections scoring below 70:
1. Identify specific issues from feedback
2. Determine if additional research is needed
3. Either request targeted deep research or suggest manual edits

## Refinement Workflow

**Automatic** (via QAGateHook): Runs after report generation. If score < 70, logs a warning and includes feedback in the result. User decides on action.

**Manual** (user-triggered):
1. User requests QA: `run_qa(company)`
2. Review scores and feedback
3. For low-scoring sections, identify root cause and suggest approach
4. Execute refinement if approved

## Section Priorities

When refining, address sections in this order:
1. **Executive Summary** -- sets tone for entire report
2. **Financial Analysis** -- factual accuracy is critical
3. **Competitive Landscape** -- highest strategic value
4. **SWOT Analysis** -- synthesis quality matters

## Example Workflow

```
User: "Check the quality of the Acme Corp report"

1. run_qa("Acme Corp")

   Results:
   Overall: 72 (B)
   - Clarity: 85
   - Completeness: 65
   - Insight Depth: 75
   - Accuracy: 63

2. Present findings:
   "The Acme Corp report scores 72/100 (B grade).

   Strong: Clarity (85), Insight Depth (75)

   Needs work:
   - Completeness (65): Missing competitor TechCorp
   - Accuracy (63): Revenue figures need citations

   Would you like me to:
   1. Run targeted research on TechCorp?
   2. Find citations for financial claims?
   3. Both?"

3. If user approves research:
   research_company(company="TechCorp", url="https://techcorp.com", mode="scrape")

4. After additional research:
   "I've gathered information on TechCorp.
    The report can now be updated with:
    - TechCorp's market position
    - Competitive comparison

    Shall I regenerate the Competitive Landscape section?"
```

## Constraints

- **Threshold**: Default QA gate threshold is 70
- **Iteration Limit**: Max 2 refinement cycles recommended
- **Cost Awareness**: Each refinement may incur API costs
- **User Approval**: Always get approval before re-research
