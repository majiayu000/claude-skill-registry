---
name: qa-iteration
version: "2.0.0"
description: "Section refinement workflow and quality assessment"

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY

mcp_server: primr
tools:
  - run_qa
  - research_company
resources:
  - primr://output/latest
  - primr://output/artifacts
---

# QA Iteration Skill (v2.0)

You are an expert at quality assessment and iterative report refinement.

## Quality Grading Framework

Primr grades reports on a 0-100 scale across four dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Clarity | 25% | Readability, structure, flow |
| Completeness | 25% | Coverage of key topics |
| Insight Depth | 25% | Strategic value, non-obvious findings |
| Accuracy | 25% | Alignment with source data |

## Score Interpretation

| Score | Grade | Meaning |
|-------|-------|---------|
| 85-100 | A | Excellent, ready for use |
| 70-84 | B | Good, minor improvements possible |
| 55-69 | C | Acceptable, notable gaps |
| 40-54 | D | Below standard, needs revision |
| 0-39 | F | Unacceptable, major issues |

## QA Gate Hook

The QAGateHook automatically triggers after report generation:

```python
# Default threshold: 70
if qa_score < 70:
    return HookResponse(
        result=HookResult.WARN,
        message=f"QA score {qa_score} below threshold"
    )
```

## Operational Capabilities

### 1. Run Quality Assessment

**Tool**: `run_qa`

```
# QA most recent report
run_qa(company="Acme Corp")

# QA specific file
run_qa(file_path="output/acme_corp/report.docx")

# QA with detailed feedback
run_qa(company="Acme Corp", detailed=True)
```

### 2. Interpret QA Results

```yaml
qa_result:
  overall_score: 78
  dimensions:
    clarity: 85
    completeness: 72
    insight_depth: 80
    accuracy: 75
  feedback:
    - section: "Executive Summary"
      score: 82
      issues: []
    - section: "Competitive Landscape"
      score: 65
      issues:
        - "Missing key competitor: TechCorp"
        - "Market share data outdated"
    - section: "Financial Analysis"
      score: 70
      issues:
        - "Revenue figures need citation"
```

### 3. Section Refinement

**Trigger**: Section scores below threshold
**Tool**: `research_company` (with section focus)

```
For sections scoring < 70:
1. Identify specific issues from feedback
2. Determine if additional research needed
3. Either:
   - Request targeted deep research
   - Suggest manual edits to user
```

## Refinement Workflow

### Automatic (via QAGateHook)
```
1. Report generated
2. QAGateHook runs QA
3. If score < threshold:
   - Log warning
   - Include feedback in result
4. User decides on action
```

### Manual (user-triggered)
```
1. User requests QA: run_qa(company)
2. Review scores and feedback
3. For low-scoring sections:
   - Identify root cause
   - Suggest refinement approach
4. Execute refinement if approved
```

## Common Quality Issues

### Clarity Issues
| Problem | Solution |
|---------|----------|
| Long paragraphs | Break into bullet points |
| Jargon overuse | Add definitions or simplify |
| Poor structure | Reorganize with clear headers |
| Passive voice | Rewrite in active voice |

### Completeness Issues
| Problem | Solution |
|---------|----------|
| Missing competitor | Run targeted deep research |
| Sparse financials | Check SEC filings, news |
| No leadership info | Search LinkedIn, press releases |
| Outdated data | Re-scrape or deep research |

### Insight Depth Issues
| Problem | Solution |
|---------|----------|
| Surface-level analysis | Add "so what" implications |
| Missing trends | Research industry context |
| No strategic recommendations | Add actionable insights |
| Generic conclusions | Make company-specific |

### Accuracy Issues
| Problem | Solution |
|---------|----------|
| Uncited claims | Add source citations |
| Contradictory info | Verify against primary sources |
| Outdated facts | Update with current data |
| Speculation as fact | Mark as hypothesis |

## Section-Level Refinement

### High-Priority Sections
1. Executive Summary (sets tone)
2. Financial Analysis (factual accuracy critical)
3. Competitive Landscape (strategic value)
4. SWOT Analysis (synthesis quality)

### Refinement Strategies

**For Executive Summary**:
```
If score < 70:
- Ensure key findings are highlighted
- Check for clear value proposition
- Verify strategic recommendations present
```

**For Competitive Landscape**:
```
If score < 70:
- Identify missing competitors
- Run deep research: "competitors of [company]"
- Update market positioning analysis
```

**For Financial Analysis**:
```
If score < 70:
- Check for citation gaps
- Verify numbers against sources
- Add trend analysis if missing
```

## Example Workflow

```
User: "Check the quality of the Acme Corp report"

Agent:
1. run_qa("Acme Corp")
   
   Results:
   Overall: 72 (B)
   - Clarity: 85 ✓
   - Completeness: 65 ⚠
   - Insight Depth: 75 ✓
   - Accuracy: 63 ⚠

2. Present findings:
   "The Acme Corp report scores 72/100 (B grade).
   
   ✓ Strong: Clarity (85), Insight Depth (75)
   
   ⚠ Needs work:
   - Completeness (65): Missing competitor TechCorp
   - Accuracy (63): Revenue figures need citations
   
   Would you like me to:
   1. Run targeted research on TechCorp?
   2. Find citations for financial claims?
   3. Both?"

3. If user approves research:
   research_company(
       company="TechCorp",
       url="https://techcorp.com",
       mode="scrape"
   )
   
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
