---
name: create-runbook
description: Create an operational runbook when the user asks to document a procedure, write a runbook, create an ops guide, or document how to handle a specific operational task
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[service, process, or operational procedure to document]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: ops, runbook, docs
---

# Create Runbook

## Overview

Generate an operational runbook with step-by-step procedures, copy-pasteable commands, troubleshooting decision trees, and clear escalation paths. Runbooks are designed to be followed under pressure by an on-call engineer who may not be familiar with the system, so every step must be explicit, every command must be runnable, and every decision point must have clear criteria.

## Workflow

1. **Read architecture context** — Scan `.chalk/docs/engineering/` for:
   - Architecture docs (service names, endpoints, infrastructure components)
   - Previous runbooks (to match format and avoid duplication)
   - Incident reports and postmortems (to identify procedures that should exist but do not)
   - Monitoring and alerting docs (dashboard links, alert names)
   Also check `.chalk/docs/` root for any configuration or infrastructure documentation.

2. **Parse the runbook scope** — From `$ARGUMENTS`, identify:
   - Which service or process the runbook covers
   - What scenario it addresses (deployment, rollback, scaling, failover, data recovery, etc.)
   - Whether this is a routine procedure or an emergency procedure
   If the scope is too broad (e.g., "runbook for everything"), ask the user to narrow to a specific service or scenario.

3. **Gather operational details** — Use `Bash` to inspect the codebase for:
   - Service configuration files, deployment scripts, and infrastructure-as-code
   - Environment variables and configuration references
   - Health check endpoints, monitoring integrations
   - Database connection details (without exposing credentials)
   This ensures commands reference real service names and endpoints, not generic placeholders.

4. **Write procedures as numbered steps** — Each step must:
   - Describe what the step does and why
   - Include a copy-pasteable command in a code block (if applicable)
   - Show expected output so the operator can verify success
   - State what to do if the step fails (go to troubleshooting, retry, or escalate)

5. **Build the troubleshooting decision tree** — For common failure modes:
   - Start with the symptom the operator observes
   - Branch based on observable conditions (log messages, status codes, metrics)
   - Each branch leads to a specific action or escalation
   - No dead ends: every branch must terminate in either a fix or an escalation

6. **Define escalation criteria** — Specify:
   - When to escalate (time thresholds, severity conditions)
   - Who to escalate to (team, role, or on-call channel — not individual names)
   - What information to include in the escalation

7. **Write verification steps** — After each procedure, include steps to confirm success:
   - Health check commands
   - Expected metric values
   - Log patterns that confirm normal operation
   - How long to monitor before considering the procedure complete

8. **Write rollback procedures** — For every procedure that changes state, include:
   - How to undo the change
   - What data or state may be affected by the rollback
   - Verification steps specific to the rollback

9. **Validate commands** — Review all commands in the runbook to ensure:
   - No generic placeholders like `<your-service-name>` or `$SERVICE` without definition
   - Environment-specific values are clearly documented at the top as prerequisites
   - Commands use actual service names, endpoints, and paths from the codebase

10. **Determine the next file number** — List files in `.chalk/docs/engineering/` to find the highest numbered file. Increment by 1.

11. **Write the file** — Save to `.chalk/docs/engineering/<n>_runbook_<service_or_process>.md`.

12. **Confirm** — Present the runbook with a summary of procedures covered, prerequisites, and any gaps that need input from the team.

## Runbook Structure

```markdown
# Runbook: <Service/Process Name>

**Last Updated**: <YYYY-MM-DD>
**Owner**: <team or role>
**Review Cadence**: <quarterly / after each incident>

## Purpose

<When should an operator use this runbook? What scenario does it address?>

## Prerequisites

Before starting, ensure you have:

- [ ] Access to <system/tool> (request via <channel>)
- [ ] <CLI tool> installed (version <X.Y+>)
- [ ] Environment variables set:
  ```bash
  export SERVICE_URL=<actual-url>
  export DB_HOST=<actual-host>
  ```
- [ ] Familiarity with <relevant dashboard or monitoring tool>

## Procedures

### Procedure 1: <Name>

**When to use**: <trigger condition>
**Estimated duration**: <time>
**Risk level**: Low / Medium / High

1. **<Step description>**

   Why: <brief explanation of purpose>

   ```bash
   <copy-pasteable command>
   ```

   Expected output:
   ```
   <what the operator should see>
   ```

   If this fails: <go to Troubleshooting section X / retry / escalate>

2. **<Next step>**

   ```bash
   <command>
   ```

   Expected output:
   ```
   <expected result>
   ```

### Procedure 2: <Name>

<Same format as above>

## Troubleshooting

### Symptom: <What the operator observes>

```
Is <condition A> true?
├── Yes → <Action or next check>
│   └── Did it resolve?
│       ├── Yes → Done. Verify with <command>
│       └── No → Escalate to <team>
└── No → Check <condition B>
    ├── <condition B> true → <Action>
    └── <condition B> false → Escalate to <team>
```

### Symptom: <Another common issue>

<Decision tree for this symptom>

## Escalation

| Condition | Escalate To | Channel | Include |
|-----------|-------------|---------|---------|
| <when to escalate> | <team or role> | <Slack channel / PagerDuty / etc.> | <what info to provide> |
| Procedure exceeds <X> minutes | <team> | <channel> | Timeline of steps taken, current state |
| Data integrity concern | <team> | <channel> | Affected records, scope of impact |

## Verification

After completing any procedure, verify success:

1. **Health check**
   ```bash
   <health check command>
   ```
   Expected: `<healthy response>`

2. **Metrics check**
   - <metric name> should return to <normal range> within <timeframe>
   - Dashboard: <link>

3. **Log check**
   ```bash
   <command to check for error patterns>
   ```
   Expected: No errors matching `<pattern>` in the last <timeframe>

4. **Monitoring period**: Watch for <duration> before considering the procedure complete.

## Rollback

If the procedure needs to be undone:

1. **<Rollback step>**
   ```bash
   <rollback command>
   ```

2. **Verify rollback**
   ```bash
   <verification command>
   ```
   Expected: <state returns to pre-procedure baseline>

**Rollback risks**: <any data or state that cannot be recovered>
```

## Output

- **File**: `.chalk/docs/engineering/<n>_runbook_<service_or_process>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Runbook: <Service/Process Name>`

## Anti-patterns

- **Prose instead of steps** — "First you'll want to check the service health and then maybe restart it if needed" is not a runbook. "Step 1: Check service health. Step 2: If unhealthy, restart." Runbooks are followed under pressure. Use numbered steps, not paragraphs.
- **Non-copyable commands** — Commands with placeholders like `<your-service>`, `$REPLACE_ME`, or `[insert name here]` force the operator to think and substitute under pressure. Define all variables in the Prerequisites section and use actual values in commands.
- **Missing escalation path** — A runbook without escalation criteria leaves the operator stranded when the procedure does not work. Every runbook must answer: "What do I do if this doesn't fix it?"
- **No verification step** — Completing a procedure without verifying success is dangerous. The operator must be able to confirm the system is healthy before walking away. Include health checks, metric thresholds, and monitoring duration.
- **Outdated commands** — Runbooks that reference decommissioned services, old endpoints, or deprecated CLI flags are worse than no runbook at all. Include a review cadence and last-updated date. Flag commands that depend on specific versions.
- **Missing rollback** — Any procedure that changes system state must include instructions to undo it. If a procedure is irreversible, that must be stated explicitly so the operator understands the risk before proceeding.
- **Assuming expertise** — Runbooks are often used by on-call engineers who did not build the system. Do not assume familiarity with internals. Explain what each step does and why, not just how.
