---
name: create-micro-skill
description: Single responsibility description
allowed-tools:
- Read
- Write
- Edit
- Bash
- Glob
- Grep
- Task
- TodoWrite
model: claude-3-5-sonnet
x-version: 1.0.0
x-category: workflow
x-vcl-compliance: v3.1.1
binding: skill:micro-skill-creator
category: workflow
---



---



---

## Library-First Directive

This agent operates under library-first constraints:

1. **Pre-Check Required**: Before writing code, search:
   - `.claude/library/catalog.json` (components)
   - `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md` (patterns)
   - `D:\Projects\*` (existing implementations)

2. **Decision Matrix**:
   | Result | Action |
   |--------|--------|
   | Library >90% | REUSE directly |
   | Library 70-90% | ADAPT minimally |
   | Pattern documented | FOLLOW pattern |
   | In existing project | EXTRACT and adapt |
   | No match | BUILD new |

---

## Library-First Directive

This agent operates under library-first constraints:

1. **Pre-Check Required**: Before writing code, search:
   - `.claude/library/catalog.json` (components)
   - `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md` (patterns)
   - `D:\Projects\*` (existing implementations)

2. **Decision Matrix**:
   | Result | Action |
   |--------|--------|
   | Library >90% | REUSE directly |
   | Library 70-90% | ADAPT minimally |
   | Pattern documented | FOLLOW pattern |
   | In existing project | EXTRACT and adapt |
   | No match | BUILD new |

---

## STANDARD OPERATING PROCEDURE

### Purpose
- Primary action: Single responsibility description

### Trigger Conditions
- Command syntax: /create-micro-skill [args]
- Ensure prerequisites are met before execution.

### Inputs and Options
- Inputs: No structured parameters defined; capture user intent explicitly.

### Execution Phases
1. Review the request and confirm scope.
2. Execute the command flow.
3. Summarize outcomes and next actions.

### Success Criteria and Outputs
- Document artifacts, decisions, and follow-up actions clearly.

### Error Handling and Recovery
- If execution fails, capture the failure mode, retry with verbose context, and surface actionable remediation steps.

### Chaining and Coordination

### Memory and Tagging
- Tag session outputs with who/when/why for traceability.

### Example Invocation
- /create-micro-skill example

### Output Format
- Provide a concise summary, actions taken, artifacts generated, and recommended next steps.
- Always include an explicit confidence line: "Confidence: X.XX (ceiling: TYPE Y.YY)".
- Use ceilings — inference/report: 0.70, research: 0.85, observation: 0.95, definition: 0.95.
- Keep user-facing output in plain English; reserve VCL markers for the appendix only.

Confidence: 0.86 (ceiling: observation 0.95) - SOP rewritten to Prompt-Architect pattern based on legacy command content.

---

## VCL COMPLIANCE APPENDIX (Internal Reference)

[[HON:teineigo]] [[MOR:root:PA]] [[COM:PromptArchitect]] [[CLS:ge_command]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[SPC:path:/commands]]
[define|neutral] CONFIDENCE_CEILINGS := {inference:0.70, report:0.70, research:0.85, observation:0.95, definition:0.95} [conf:0.9] [state:confirmed]
[direct|emphatic] L2_LANGUAGE := English; user-facing outputs exclude VCL markers. [conf:0.99] [state:confirmed]
[commit|confident] <promise>CREATE_MICRO_SKILL_VERILINGUA_VERIX_COMPLIANT</promise> [conf:0.88] [state:confirmed]