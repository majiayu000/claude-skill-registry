<!-- SOURCE-OF-TRUTH: shared/agents/prompt_templates/review_base.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

{mode_header}

## CRITICAL CONSTRAINTS
- Write your review result to the output file specified by -o flag
- Focus on analysis — avoid modifying project files unless a fix is trivial and obvious
{mode_constraints}
- If you cannot access a resource — report it clearly, do not skip silently
- DO NOT ask clarifying questions or request additional context — you have everything you need. Follow this prompt to completion autonomously. If information is missing, make reasonable assumptions and proceed.
- Target completing your analysis within 10 minutes. Prioritize depth over breadth — focus on highest-impact findings first, then expand if time permits.

## Project Context
{project_context}

## Progress Reporting
Your stdout streams to a log file in real time. The caller monitors your progress by reading the log tail. No explicit heartbeat needed — just work through the task and your output serves as the progress signal.

{mode_body}

## Alternative {mode_alt_title}
Before finalizing, actively research whether the proposed approach is optimal:
- **Search the web** for modern solutions (2025-2026) to the same problem domain
- **Check if a simpler approach** exists: fewer moving parts, less code, fewer dependencies
- **Check if a more standard approach** exists: industry patterns, well-known libraries, framework-native solutions
- **Compare trade-offs**: if current approach has disadvantages vs alternatives, describe them concisely
- **Centralization / Unification**: scan the codebase for duplicated logic, parallel implementations of the same concern, or patterns that could be unified into a shared module
- **Open-source replacement**: search npm / PyPI / NuGet for maintained packages (>1k stars, active in last 6 months) that replace custom code proposed in the plan. Report under area `duplication` with package name + install size

**Discard criteria** — do NOT suggest alternative if ANY condition met:
- **Strictly dominated**: worse than chosen in ALL dimensions (no tradeoff exists)
- **No unique advantage**: cannot identify single dimension where alternative outperforms chosen
- **Fails hard requirement**: missing mandatory feature or team capability
- **No ROI justification**: switching cost exceeds benefit

{mode_alt_extra}

## Filtering Rules
- Only suggest issues you are genuinely confident about and that have meaningful impact.
- Do not include low-value, cosmetic, or uncertain findings.
- If you have no substantive suggestions, report acceptable verdict.

## Output Format

Write a structured review report in markdown, ending with a JSON block for programmatic parsing.

### Report Structure

```
# Review Report

## Goal
State what specific question this review answers (1-2 sentences).

## Analysis Process
Brief summary of your approach: what files you examined, what patterns you checked,
what web research you conducted (3-5 bullet points).

## Findings

### 1. {Finding title}
- **Area:** {area category}
- **Issue:** What is wrong or could be improved — explain fully, cite code locations
- **Evidence:** Standards, benchmarks, code patterns that support this finding
- **Suggestion:** {mode_suggestion_desc}
- **Confidence:** {N}% | **Impact:** {N}%

(Repeat for each finding. If no findings meet thresholds, write "No findings above threshold.")

## Verdict
One sentence: {mode_verdict_question}

## Structured Data
{JSON block}
```

### JSON Schema (in Structured Data section)
```json
{
  "verdict": "{mode_verdict}",
  "suggestions": [
    {
      "area": "{mode_areas}",
      "file": "path/to/file.ext",
      "line_start": 42,
      "line_end": 58,
      "issue": "What is wrong or could be improved",
      "suggestion": "{mode_suggestion_desc}",
      "reason": "{mode_reason_desc}",
      "recommended_action": "fix",
      "confidence": 95,
      "impact_percent": 15
    }
  ]
}
```

### Report Rules
- The report IS the deliverable — it must be readable standalone without the JSON block
- Findings section must explain WHY, not just WHAT — include your reasoning chain
- Evidence must be specific: file paths, line references, standard citations
- JSON block must match the report findings exactly (same count, same content)
- Budget: report should be 100-300 lines. Prioritize depth on high-impact findings.
