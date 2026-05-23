---
name: pop-assessment-anthropic
description: "Validates PopKit compliance with Claude Code patterns using concrete standards and automated checks"
triggers:
  - assess anthropic
  - claude code compliance
  - hook protocol check
  - plugin validation
version: 1.0.0
---

# Pop Assessment: Anthropic Engineer

Validates PopKit compliance with official Claude Code patterns, hook protocols, and Anthropic engineering best practices using **concrete standards** and **automated validation**.

## How This Skill Works

Unlike prose-based assessments, this skill uses:

1. **Machine-Readable Standards** - JSON schemas defining exact requirements
2. **Automated Validation Scripts** - Python scripts that programmatically check compliance
3. **Consistent Scoring** - Same input = same output, every time

## Invocation

When invoked, follow this process:

### Step 1: Run Automated Checks

Execute the validation scripts in order:

```bash
# From packages/plugin directory
python skills/pop-assessment-anthropic/scripts/validate_plugin_structure.py
python skills/pop-assessment-anthropic/scripts/validate_hooks.py
python skills/pop-assessment-anthropic/scripts/validate_routing.py
python skills/pop-assessment-anthropic/scripts/calculate_score.py
```

### Step 2: Read Standards (if manual review needed)

If automated checks identify issues requiring context:

```
Read: skills/pop-assessment-anthropic/standards/hook-protocol.md
Read: skills/pop-assessment-anthropic/standards/plugin-schema.md
Read: skills/pop-assessment-anthropic/standards/agent-routing.md
Read: skills/pop-assessment-anthropic/standards/progressive-disclosure.md
```

### Step 3: Load Checklists

For comprehensive review:

```
Read: skills/pop-assessment-anthropic/checklists/claude-code-compliance.json
Read: skills/pop-assessment-anthropic/checklists/hook-patterns.json
Read: skills/pop-assessment-anthropic/checklists/blog-practices.json
```

### Step 4: Generate Report

Use the output style `assessment-report` and include:

1. **Automated Results** - From script execution
2. **Manual Findings** - From checklist review
3. **Score Calculation** - Using `calculate_score.py` output
4. **Recommendations** - Prioritized by severity

## Standards Directory

| File                        | Purpose                                       |
| --------------------------- | --------------------------------------------- |
| `hook-protocol.md`          | Exact JSON stdin/stdout protocol requirements |
| `plugin-schema.md`          | plugin.json and hooks.json required fields    |
| `agent-routing.md`          | Routing configuration rules and coverage      |
| `progressive-disclosure.md` | Tiered loading and context efficiency         |

## Checklists Directory

| File                          | Purpose                                    |
| ----------------------------- | ------------------------------------------ |
| `claude-code-compliance.json` | Machine-readable plugin structure checks   |
| `hook-patterns.json`          | Hook implementation validation rules       |
| `blog-practices.json`         | Anthropic engineering blog recommendations |

## Scripts Directory

| Script                         | Purpose                                  | Output            |
| ------------------------------ | ---------------------------------------- | ----------------- |
| `validate_plugin_structure.py` | Check plugin.json, hooks.json, .mcp.json | JSON findings     |
| `validate_hooks.py`            | Verify JSON protocol in all hooks        | JSON findings     |
| `validate_routing.py`          | Check routing coverage and conflicts     | JSON findings     |
| `calculate_score.py`           | Calculate final score from findings      | Score + breakdown |

## Scoring System

Each check has a severity and point deduction:

| Severity | Deduction | Description                |
| -------- | --------- | -------------------------- |
| critical | -20       | Must fix before release    |
| high     | -10       | Should fix, blocks quality |
| medium   | -5        | Recommended to fix         |
| low      | -2        | Nice to have               |
| warning  | -1        | Minor improvement          |

**Starting Score**: 100
**Minimum Score**: 0

## Pass/Fail Criteria

| Score Range | Status     | Meaning                   |
| ----------- | ---------- | ------------------------- |
| 90-100      | EXCELLENT  | Production ready          |
| 80-89       | GOOD       | Minor improvements needed |
| 70-79       | ACCEPTABLE | Should address issues     |
| 60-69       | NEEDS WORK | Several issues to fix     |
| 0-59        | FAILING    | Critical issues present   |

## Example Output

```markdown
# Anthropic Engineer Assessment Report

**Assessed:** PopKit Plugin v0.2.0
**Date:** 2025-12-12
**Score:** 87/100 (GOOD)

## Automated Check Results

### Plugin Structure (validate_plugin_structure.py)

| Check              | Status | Details                     |
| ------------------ | ------ | --------------------------- |
| plugin.json schema | PASS   | All required fields present |
| hooks.json schema  | PASS   | Valid event types           |
| .mcp.json valid    | PASS   | Schema reference included   |

### Hook Protocol (validate_hooks.py)

| Hook             | stdin | stdout | error_handling | Status |
| ---------------- | ----- | ------ | -------------- | ------ |
| pre-tool-use.py  | PASS  | PASS   | PASS           | PASS   |
| post-tool-use.py | PASS  | PASS   | PASS           | PASS   |
| session-start.py | PASS  | PASS   | WARN           | WARN   |

### Routing Coverage (validate_routing.py)

| Category       | Coverage | Missing     |
| -------------- | -------- | ----------- |
| Keywords       | 95%      | 2 agents    |
| File Patterns  | 90%      | yaml, yml   |
| Error Patterns | 85%      | ImportError |

## Score Breakdown

| Category               | Max     | Earned | Deductions         |
| ---------------------- | ------- | ------ | ------------------ |
| Plugin Structure       | 25      | 25     | 0                  |
| Hook Protocol          | 30      | 28     | -2 (1 warning)     |
| Agent Routing          | 25      | 21     | -4 (medium issues) |
| Progressive Disclosure | 20      | 13     | -7 (2 medium)      |
| **Total**              | **100** | **87** | **-13**            |

## Recommendations

1. **HIGH**: Add error patterns for ImportError, ConnectionError
2. **MEDIUM**: Add file patterns for _.yaml, _.yml
3. **LOW**: session-start.py error handling could be improved
```

## Why This Approach

1. **Reproducible** - Scripts produce same results every time
2. **Objective** - JSON checklists remove interpretation
3. **Fast** - Automated checks run in seconds
4. **Actionable** - Specific file:line references
5. **Versionable** - Standards tracked in git

## Related

- Agent: `agents/assessors/anthropic-engineer/AGENT.md`
- Output Style: `output-styles/assessment-report.md`
- Other Assessments: security, performance, ux, architect, docs
