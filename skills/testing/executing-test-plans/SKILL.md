---
name: executing-test-plans
description: Execute a structured test plan and emit a concise, comprehensive results document (JSON + Markdown). Use when running test plans, executing QA workflows, verifying acceptance criteria systematically, or producing test results documentation.
context: fork
argument-hint: "[plan-file] [env-profile] [out-dir]"
model: claude-sonnet-4-5
allowed-tools:
  - "Bash(curl:*)"
  - "Bash(docker:*)"
  - "Bash(aws sqs:*)"
  - "Bash(mysql:*)"
  - "Bash(jq:*)"
  - "Bash(grep:*)"
  - "Bash(watch:*)"
---

# Executing Test Plans

Execute test plans end-to-end with strict state control and concise reporting.

## Policy (per section, in order)

1. **Sense-check** section; if incoherent, propose minimal fix -> `suggested_adjustments`
2. **State prep**: verify prerequisites; run minimal corrective actions. If impossible, mark `BLOCKED` with reason
3. **Execute** exactly; record precise **inputs** and raw **outputs**
4. **Verify** vs expected; set `status` = `PASS` | `FAIL` | `BLOCKED`
5. **Notes**: timings, IDs, logs, env diffs (terse)
6. **Keep adjustments** (don't lose edits or ordering changes)

## Pre-flight

- Check env profile from arguments
- Docker services: `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -20`
- Service health checks as applicable

## Execution Rules

- Follow plan sections strictly; only minimal fixes allowed (record them)
- Prefer tiny adjustments over skips; never reorder unless required (record it)
- Continue after failures unless they hard-block subsequent steps

## For Each Test Step

Document clearly:

- Test step description/objective
- All inputs provided
- Actual output/result received
- Expected vs actual comparison
- Pass/Fail determination with reasoning

## Output

Write `<out-dir>/test-results.json` with this schema:

```json
{
  "metadata": {
    "sut": "",
    "env": {},
    "plan_sections": 0,
    "timestamp": ""
  },
  "sections": [
    {
      "id": "",
      "title": "",
      "precheck_ok": true,
      "pre_state": { "assessed": [], "actions": [], "ready": true },
      "inputs": [],
      "outputs": [],
      "expected": [],
      "comparison": { "match": true, "diffs": [] },
      "status": "PASS",
      "suggested_adjustments": [],
      "notes": []
    }
  ],
  "overall": {
    "pass_rate": "0/0",
    "failing_or_blocked_sections": [],
    "verdict": "PASS"
  }
}
```

Also write a human-readable Markdown summary alongside the JSON.

## Quality Standards

- Be thorough and methodical -- missing a test step undermines the process
- Remain objective in pass/fail -- base decisions on evidence, not assumptions
- Document unexpected findings even if not part of the plan
- Documentation should be detailed enough for reproduction
