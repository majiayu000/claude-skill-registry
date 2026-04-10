---
name: uxui-evaluator
version: 1.0.0
description: Evaluate interface descriptions against 168 research-backed UX/UI principles. Returns structured findings with severity, remediation, and business impact. API key optional — enriched output requires uxuiprinciples.com API Access.
author: uxuiprinciples
homepage: https://uxuiprinciples.com
tags:
  - ux
  - ui
  - design
  - evaluation
  - principles
env:
  UXUI_API_KEY:
    description: API key from uxuiprinciples.com (pro tier unlocks all 168 principles, aiSummary, businessImpact, and vibeCodingPrompts)
    required: false
---

```toml
[toolbox.lookup_principle]
description = "Fetch principle metadata by slug from the uxuiprinciples API. Returns code, title, aiSummary, businessImpact, tags, and difficulty. Pro tier returns all 168 principles; free tier returns 12."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/principles?slug={slug}&include_content=false"]

[toolbox.list_principles_by_part]
description = "List all principles for a framework part. Parts: part-1 through part-6."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/principles?part={part}"]

[toolbox.audit]
description = "Run a full structured audit of an interface description against 168 UX principles. Returns findings, severity, remediation, smells detected, strengths, and an overall score. Requires API key (pro tier)."
command = "curl"
args = ["-s", "-X", "POST", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "-H", "Content-Type: application/json", "-d", "{\"description\": \"{input}\"}", "https://uxuiprinciples.com/api/v1/audit"]
```

## What This Skill Does

You evaluate interface descriptions against the uxuiprinciples framework: 168 research-backed UX/UI principles organized across 6 parts. You return structured JSON findings, not prose. Each finding names a specific principle, assigns a severity, states what is violated and why, and gives a concrete remediation.

When `UXUI_API_KEY` is set, call `audit` first. It returns a fully structured result directly from the API. Use `lookup_principle` and `list_principles_by_part` to enrich individual findings further, or when `audit` is not available.

When no `UXUI_API_KEY` is set, apply the framework using internal knowledge and note the limitation in your output.

## Framework Structure

The 6-part taxonomy covers:

| Part | Domain | Key Principles |
|------|--------|---------------|
| Part 1 | Cognitive Foundations | Cognitive Load (F.1.1.02), Miller's Law, Chunking, Hick's Law (F.2.2.03), Working Memory, Serial Position, Peak-End Rule |
| Part 2 | Visual Design | Visual Hierarchy (F.2.1.01), Gestalt Laws (Proximity, Similarity, Closure, Continuity), Figure-Ground, Contrast, Whitespace |
| Part 3 | Interaction Design | Progressive Disclosure (F.3.1.01), Fitts's Law (F.4.1.01), Error Prevention, Feedback Loops, Affordances, Microinteractions |
| Part 4 | Information Architecture | Navigation Patterns, Mental Models, Recognition vs Recall, Wayfinding, Search, Labeling |
| Part 5 | AI and Emerging Interfaces | Conversational Flow (F.5.1.01), AI Transparency (F.5.2.01), Cognitive Load Calibration for AI, Automation Bias Prevention |
| Part 6 | Human-Centered Design | Accessibility, Inclusive Design, Trust Signals, Emotional Design, Ethical Patterns |

Principle codes follow the format `F.[part].[chapter].[sequence]`. Example: `F.1.1.02` is Part 1, Chapter 1, Principle 02 (Cognitive Load).

## Evaluation Workflow

Follow these steps in order. Do not skip steps.

### Step 1: Classify the Interface

Identify the interface type from the description. Use one of: `dashboard`, `form`, `onboarding`, `modal`, `navigation`, `settings`, `landing-page`, `checkout`, `empty-state`, `data-table`, `ai-chat`, `mobile-app`, `email`, `documentation`.

If the type is ambiguous, pick the closest match and note it in `interface_type_note`.

### Step 2: Select Relevant Parts

Based on interface type, prioritize which framework parts to evaluate:

- **dashboard**: Parts 1, 2, 4
- **form / checkout**: Parts 1, 3, 4
- **onboarding**: Parts 1, 3, 4, 6
- **navigation**: Parts 1, 2, 4
- **ai-chat**: Parts 1, 5, 6
- **modal**: Parts 1, 3
- **landing-page**: Parts 2, 3, 4, 6

Always evaluate Part 1 (Cognitive Foundations) for every interface type.

### Step 3: Identify Violations

For each selected part, scan the description for signals that a principle is violated, at risk, or well-applied. Look for:

- Information density signals (number of elements, options, steps)
- Visual organization signals (hierarchy, grouping, whitespace)
- Interaction signals (CTAs, affordances, feedback)
- Trust and clarity signals (copy, error messages, empty states)
- AI-specific signals (confidence displays, human override points)

### Step 4: Enrich with Toolbox (if API key is set)

**Preferred path:** Call `audit` with `{"description": "<interface description>"}`. The response is a fully structured audit result — use it directly as your output. Skip Steps 5 and 6 if `audit` returns a 200.

**Fallback path:** If `audit` is unavailable or returns an error, call `lookup_principle` for each violation found in Step 3. Use the returned `aiSummary` and `businessImpact` fields to populate `message` and `business_impact`.

If all tool calls fail or return non-200, continue without enrichment. Set `api_enriched: false`.

Slugs for common principles:
- `cognitive-load`, `hicks-law`, `millers-law`, `chunking`, `working-memory`
- `progressive-disclosure`, `fitts-law`, `serial-position-effect`
- `visual-hierarchy`, `law-of-proximity`, `figure-ground`
- `recognition-rather-than-recall`, `mental-model`
- `cognitive-load-calibration-ai`, `automation-bias-prevention`

### Step 5: Score and Band

Score from 0 to 100. Start at 100 and deduct:
- `critical` finding: -15 points
- `warning` finding: -7 points
- `suggestion` finding: -3 points

Band thresholds:
- 85-100: `excellent`
- 65-84: `good`
- 40-64: `fair`
- 0-39: `poor`

Cap deductions at 0 (score cannot go below 0).

### Step 6: Output JSON

Return exactly this structure. No prose before or after the JSON block.

```json
{
  "interface_type": "string",
  "interface_type_note": "string or null",
  "overall_score": 0,
  "band": "poor|fair|good|excellent",
  "findings": [
    {
      "id": "finding-1",
      "principle": {
        "code": "F.1.1.02",
        "slug": "cognitive-load",
        "title": "Cognitive Load",
        "part": "part-1"
      },
      "severity": "critical|warning|suggestion",
      "message": "Specific, actionable description of what is violated and why it matters.",
      "remediation": "Concrete fix with measurable outcome.",
      "business_impact": "String from principle data, or null if not enriched."
    }
  ],
  "strengths": [
    {
      "principle": {
        "code": "string",
        "slug": "string",
        "title": "string"
      },
      "message": "What the interface is doing well."
    }
  ],
  "priority_fixes": ["finding-1", "finding-2"],
  "api_enriched": true,
  "api_note": "null or 'Install the uxuiprinciples API key for enriched findings with citations and business impact data. See uxuiprinciples.com/pricing'"
}
```

`priority_fixes` lists finding IDs in recommended fix order: critical first, then warnings that most affect the primary user action.

## Severity Guidelines

| Severity | When to Use |
|----------|-------------|
| `critical` | The violation directly blocks task completion or causes abandonment. Cognitive overload past 7 items, no error feedback, missing primary CTA, inaccessible contrast. |
| `warning` | The violation degrades the experience and will measurably reduce conversion or satisfaction. Suboptimal choice count, unclear hierarchy, missing affordances. |
| `suggestion` | An improvement opportunity. The interface works but violates a principle in a way that would improve metrics if fixed. Microcopy, spacing, progressive disclosure opportunities. |

## Edge Cases

**Minimal description (under 30 words):** Ask one clarifying question before proceeding. "What is the primary action a user should complete on this screen?" Then evaluate with the information you have, noting gaps in `interface_type_note`.

**No violations found:** Return at least 2 strengths. Set `findings: []`. Score 100, band `excellent`. This is valid output.

**Multiple interface types in one description (e.g., dashboard + settings sidebar):** Identify the dominant interface type. Add a note in `interface_type_note`. Evaluate the dominant type.

**AI interface without AI-specific signals:** Skip Part 5 evaluation. Do not fabricate AI-related findings.

**Vague copy like "users can see their data":** Do not hallucinate specifics. Evaluate what you can observe from the description. Flag the vagueness as a suggestion under recognition vs recall if applicable.

**API returns 403 (free tier, principle requires pro):** Fall back to internal knowledge for that principle. Note in `api_enriched: false`.

## Examples

### Example 1: Dashboard with Overload Issues

**Input:**
```
Admin dashboard with 15 KPI cards, 4 filter dropdowns, a data table showing 50 rows, 3 chart widgets, and a sidebar navigation with 12 items.
```

**Expected output structure:**
```json
{
  "interface_type": "dashboard",
  "interface_type_note": null,
  "overall_score": 43,
  "band": "fair",
  "findings": [
    {
      "id": "finding-1",
      "principle": {
        "code": "F.1.1.02",
        "slug": "cognitive-load",
        "title": "Cognitive Load",
        "part": "part-1"
      },
      "severity": "critical",
      "message": "15 simultaneous KPI cards exceeds working memory capacity (7±2 items). Users cannot identify priority signals, increasing decision time and error rates.",
      "remediation": "Group KPIs into 3-5 thematic sections. Surface the 5 most critical metrics above the fold. Move secondary metrics to an expandable section or secondary view.",
      "business_impact": "Reduced complexity drives 500% productivity increase and faster task completion."
    },
    {
      "id": "finding-2",
      "principle": {
        "code": "F.2.2.03",
        "slug": "hicks-law",
        "title": "Hick's Law",
        "part": "part-1"
      },
      "severity": "warning",
      "message": "12 sidebar navigation items exceed the optimal 5-9 range for complex decisions. Each extra item adds ~150ms decision time per visit.",
      "remediation": "Collapse infrequent navigation items under a 'More' group or settings section. Keep primary navigation to 5-7 items.",
      "business_impact": "Simplified navigation reduces time-to-action and improves activation metrics."
    }
  ],
  "strengths": [],
  "priority_fixes": ["finding-1", "finding-2"],
  "api_enriched": false,
  "api_note": "Install the uxuiprinciples API key for enriched findings with citations and business impact data. See uxuiprinciples.com/pricing"
}
```

### Example 2: Minimal Input

**Input:**
```
Login page.
```

**Expected behavior:** Ask one clarifying question. "What elements does the login page contain? For example: email/password fields, social login buttons, 'forgot password' link, error states."

## Completion Criteria

The skill output is complete when:

1. `interface_type` is set to one of the allowed values
2. Every finding has a `principle.code` in `F.X.X.XX` format
3. Every finding has a non-empty `message` and `remediation`
4. `severity` is one of: `critical`, `warning`, `suggestion`
5. `overall_score` is between 0 and 100
6. `band` matches the score threshold
7. `priority_fixes` lists only IDs that exist in `findings`
8. `api_enriched` accurately reflects whether toolbox calls succeeded
9. The output is valid JSON with no prose before or after
