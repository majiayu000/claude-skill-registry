---
name: render-output
description: Renders structured data to terminal with optimal formatting. Use when presenting agent results, displaying data to users, formatting command output, or showing validation reports. Transforms raw data into clear, scannable terminal output.
---

<objective>
Transform structured data from agents into clear, scannable terminal output. This skill provides patterns for presenting information to users in the most readable format based on data type and context.

Key principle: Output should be scannable in under 5 seconds. Choose the simplest pattern that communicates the information effectively.
</objective>

<quick_start>
Select pattern based on data type:

| Data Type | Pattern | Use When |
|-----------|---------|----------|
| Machine-readable | TOON block | Returning data to subagents |
| Listings | Markdown table | Human comparisons, listings |
| Action result | Status line | Single operation outcome |
| Validation | Box report | Multi-check with pass/fail |
| Counts | Summary line | Aggregates, distributions |

Default to the simplest pattern. Escalate complexity only when needed.
</quick_start>

<patterns>
<toon_pattern>
For structured data returned to subagents or machine processing:

```toon
@type: [SchemaType]
@id: [unique-identifier]
[scalar properties]

[table]{columns|tab}:
[row1 tab-separated]
[row2 tab-separated]
```

Rules:
- ALWAYS include `@type` and `@id`
- Use tab-separated tables for arrays
- Prefer flat structure (avoid nesting >2 levels)
- No prose - data only
- Use `toon` language tag for syntax highlighting

Example:
```toon
@type: AssessAction
@id: 005-auth
actionStatus: CompletedActionStatus

validationStatus: VALID
checksPerformed: 10
issues.critical: 0
issues.warning: 1
```
</toon_pattern>

<table_pattern>
For human-readable listings and comparisons:

```markdown
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| value1  | value2  | value3  |
```

Rules:
- Maximum 6 columns (truncate or split if more)
- Align columns consistently
- Truncate cells >30 chars with `...`
- Right-align numbers
- Keep header row concise

Example:
```markdown
| ID         | Name           | Stage       | Priority |
|------------|----------------|-------------|----------|
| 005-auth   | Implement Auth | in-progress | P1       |
| 006-mgmt   | User Management| ready       | P2       |
```
</table_pattern>

<status_pattern>
For single action outcomes:

```
[symbol] [action verb] [target]: [brief result]
```

Symbols:
- `✓` success
- `✗` failure
- `⚠` warning
- `→` transition

Examples:
```
✓ Created outcome 005-auth in queued/
✓ Synced capabilities-info.toon (12 capabilities)
✗ Validation failed: 3 critical issues
⚠ Index stale, auto-syncing...
```

For short lists (<5 items), use indented bullets:
```
✓ Created 3 outcomes
  - 005-auth (queued)
  - 006-mgmt (queued)
  - 007-report (queued)
```
</status_pattern>

<box_pattern>
For validation reports and multi-section results:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Section1:     [✓/✗] [details]
Section2:     [✓/✗] [details]
Section3:     [✓/✗] [details]

Overall: [PASS ✓ / FAIL ✗ / NEEDS_ATTENTION ⚠]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use box drawing characters:
- `━` horizontal line
- `│` vertical line (if needed)
- `┌┐└┘` corners (if needed)

Reserve for:
- Validation reports (>3 checks)
- Multi-section summaries
- Error reports with details
</box_pattern>

<summary_pattern>
For counts, distributions, and quick stats:

Single line for simple counts:
```
Summary: 11 total | 3 queued | 2 ready | 1 in-progress | 5 completed
```

Two lines for distributions:
```
Summary: 11 total | 3 queued | 2 ready | 1 in-progress | 5 completed
         9 parent | 2 child | P1: 6 | P2: 4 | P3: 1
```

Rules:
- Use `|` as separator
- Align related groups
- Maximum two lines
</summary_pattern>

<distribution_pattern>
For visual distribution of values:

```
Maturity Distribution:
  0-29%:   ### (3)
  30-59%:  ##### (5)
  60-79%:  ### (3)
  80-100%: # (1)
```

Rules:
- Use `#` for bar chart
- Include count in parentheses
- Align labels and bars
</distribution_pattern>
</patterns>

<pattern_selection>
Choose pattern based on:

1. **Audience**: Subagent (TOON) vs Human (table/status/box)
2. **Complexity**: Simple (status) → Complex (box)
3. **Data shape**: List (table) vs Result (status) vs Validation (box)

Decision tree:
```
Is output for another agent?
├─ Yes → TOON block
└─ No → Is it a single action result?
        ├─ Yes → Status line
        └─ No → Is it validation with pass/fail?
                ├─ Yes → Box report
                └─ No → Is it a list/comparison?
                        ├─ Yes → Markdown table
                        └─ No → Summary line
```
</pattern_selection>

<symbols>
Standard symbols for consistent output:

| Symbol | Meaning | Unicode | Usage |
|--------|---------|---------|-------|
| ✓ | Success/pass | U+2713 | Completed actions, passing checks |
| ✗ | Failure/fail | U+2717 | Failed actions, failing checks |
| ⚠ | Warning | U+26A0 | Needs attention, non-critical |
| → | Transition | U+2192 | State changes, version bumps |
| • | Bullet | U+2022 | List items |
| ━ | Horizontal | U+2501 | Box borders |
| │ | Vertical | U+2502 | Box borders |

DO NOT use emoji. Stick to these standard symbols.
</symbols>

<anti_patterns>
Avoid these common mistakes:

- **Excessive whitespace**: Don't add blank lines between every element
- **Nested boxes**: Don't put boxes inside boxes
- **Mixed styles**: Don't combine table + box in same output
- **Emoji overuse**: Stick to standard symbols (✓✗⚠)
- **Long prose**: Output should be data-focused, not explanatory
- **Missing language tags**: Always tag code blocks (`toon`, `markdown`)
- **Inconsistent alignment**: Align columns and values consistently
- **Over-engineering**: Don't use box for simple status
- **Column overflow**: Keep tables under 6 columns
</anti_patterns>

<success_criteria>
Output meets quality standards when:

- Pattern matches data type (use decision tree)
- Symbols used consistently throughout
- No excessive whitespace or blank lines
- Code blocks have language tags
- Tables stay under 6 columns
- Box reports used only for complex validation
- TOON used for machine-readable returns
- Human output is scannable in <5 seconds
- No mixed patterns in single output
</success_criteria>

<examples>
<example name="outcome_list">
Outcomes Overview (synced: 2025-12-02T10:30:00Z)

Summary: 11 total | 3 queued | 2 ready | 1 in-progress | 0 blocked | 5 completed

Current Focus: 005-implement-auth (in-progress)

| ID                 | Name              | Stage       | Priority | Capabilities    |
|--------------------|-------------------|-------------|----------|-----------------|
| 005-implement-auth | Implement Auth    | in-progress | P1       | auth-system:30% |
| 006-user-mgmt      | User Management   | ready       | P2       | user-mgmt:25%   |
| 007-reporting      | Reporting         | queued      | P3       | reporting:20%   |

Blocked: None
</example>

<example name="action_result">
ws Plugin Published

4745a58 feat(ws): add out/list command
0.9.2 → 0.9.3 (minor)

✓ Committed, pushed, synced
</example>

<example name="validation_report">
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Validation Report: 005-auth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Schema:         ✓ Valid YAML frontmatter
Achievement:    ✓ Behavioral focus
Effects:        ✓ 3 Given-When-Then
Capabilities:   ✓ Links valid
Actors:         ⚠ 1 unknown actor ID

Overall: NEEDS_ATTENTION ⚠
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
</example>

<example name="toon_return">
```toon
@type: ItemList
@id: outcome-list-result
numberOfItems: 11

summary.total: 11
summary.queued: 3
summary.completed: 5

outcome{id,name,stage|tab}:
005-auth	Implement Auth	in-progress
006-mgmt	User Management	ready
```
</example>
</examples>
