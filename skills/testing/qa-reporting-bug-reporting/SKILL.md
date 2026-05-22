---
name: qa-bug-reporting
description: Bug report format and documentation for failed validations. Use when validation fails and status must be set to needs_fixes.
category: reporting
---

# Bug Reporting Skill

> "A good bug report is half the fix – be specific, be reproducible."

## When to Use This Skill

Use when validation fails and `status` must be set to `needs_fixes`.

## Quick Start

```markdown
## Bug Report: {{TASK_ID}}

**Severity**: Critical / High / Medium / Low
**Found in**: Automated tests / Browser testing

### Summary

Brief one-line description of the issue.

### Steps to Reproduce

1. Step one
2. Step two
3. Step three

### Expected Behavior

What should happen.

### Actual Behavior

What actually happens.

### Evidence

- Console errors: {{error text}}
- Screenshot: {{path}}
```

## Bug Report Template

```markdown
# Bug Report: {{TASK_ID}} - {{BRIEF_TITLE}}

**Reported**: {{ISO_TIMESTAMP}}
**Reporter**: QA Agent
**Severity**: {{Critical | High | Medium | Low}}
**Category**: {{Build | TypeScript | Runtime | Visual | Performance}}

---

## Summary

{{One or two sentences describing the issue}}

## Environment

- **Browser**: {{Chrome 120 / Firefox / Safari}}
- **OS**: {{Windows / macOS / Linux}}
- **Node Version**: {{v20.x.x}}
- **Screen Resolution**: {{1920x1080}}

## Steps to Reproduce

1. {{First step}}
2. {{Second step}}
3. {{Third step}}
4. {{...}}

## Expected Behavior

{{What should happen when following the steps}}

## Actual Behavior

{{What actually happens instead}}

## Console Errors

\`\`\`
{{Paste console errors here}}
\`\`\`

## Screenshots

{{Include paths to screenshots or describe what was captured}}

## Additional Context

{{Any other relevant information:

- Related code files
- Recent changes that might have caused this
- Workarounds attempted
- Similar issues seen before}}

## Acceptance Criteria Status

| Criterion       | Status            | Notes     |
| --------------- | ----------------- | --------- |
| {{Criterion 1}} | ✅ Pass / ❌ Fail | {{notes}} |
| {{Criterion 2}} | ✅ Pass / ❌ Fail | {{notes}} |
| {{Criterion 3}} | ✅ Pass / ❌ Fail | {{notes}} |

---

## For Developer

**Files likely involved**:

- {{file1.ts}}
- {{file2.tsx}}

**Suggested investigation**:

- {{Suggestion 1}}
- {{Suggestion 2}}
```

## Severity Levels

| Severity     | Definition                                 | Example                        |
| ------------ | ------------------------------------------ | ------------------------------ |
| **Critical** | App crashes, data loss, blocks all testing | Build fails, app won't load    |
| **High**     | Major feature broken, no workaround        | Player controls don't work     |
| **Medium**   | Feature partially works, has workaround    | Physics jittery but functional |
| **Low**      | Minor issue, cosmetic, edge case           | Slight visual glitch on resize |

## Category Types

| Category        | Description            | Automated Check       |
| --------------- | ---------------------- | --------------------- |
| **Build**       | Build or bundle fails  | `npm run build`       |
| **TypeScript**  | Type errors            | `npm run type-check`  |
| **Lint**        | Code style issues      | `npm run lint`        |
| **Test**        | Unit test failure      | `npm run test`        |
| **Runtime**     | Error during execution | Browser console       |
| **Visual**      | Incorrect appearance   | Browser testing       |
| **Performance** | FPS drops, lag, memory | Performance profiling |

## Anti-Patterns

❌ **DON'T:**

- Report bugs without reproduction steps
- Use vague descriptions ("it doesn't work")
- Omit error messages
- Skip severity classification
- Blame the developer in the report
- **Report code issues without thorough code review** - ALWAYS verify actual code flow before concluding there's a bug
- **Confuse valid async patterns with "bypasses"** - async functions with multiple calls may appear suspicious but can be correct
- **Escalate without investigating** - trace the code flow from entry point to execution before reporting

✅ **DO:**

- Include exact steps to reproduce
- Copy full error messages
- Attach screenshots
- Specify environment details
- Suggest where to investigate
- **Perform thorough code review before reporting** - trace actual code execution flow
- **Verify suspected "bypasses" by testing the actual behavior** - if you suspect code skips connection, verify by running the app
- **Include observed vs. expected behavior** - be specific about what you saw that was wrong, not just code that looked suspicious
- **Code review BEFORE escalating** - read the actual implementation files and understand the flow before filing a bug report

## Code Review Before Bug Reporting

**CRITICAL: Before reporting a code-related bug, you MUST:**

1. **Read the actual implementation files** - Don't guess what code does based on a quick glance
2. **Trace the execution flow** - Follow the code from entry point to the suspected issue
3. **Verify the actual behavior** - Run the app and observe what actually happens
4. **Compare expected vs. actual** - Be specific about what should happen vs. what does happen

### Example: False Positive Prevention

**BAD Bug Report (False Positive)**:

```
Bug: Lobby.tsx lines 44-47 contain DEV mode bypass
Issue: Code appears to skip connection
Severity: Critical
```

This report was WRONG because the reporter didn't trace the actual code flow. Those lines were the `initializeConnection` function which PROPERLY calls `networkManager.connect()` and `networkManager.joinRoom()`.

**GOOD Bug Report (After Thorough Review)**:

```
Bug: Server connection not established
Steps to Reproduce:
1. Start server: npm run server (verified running on port 2567)
2. Start client: npm run dev
3. Browser console shows: "Failed to connect to Colyseus server"
4. Expected: Console shows "Connected to Colyseus server"
5. Actual: Connection timeout despite server running

Code Review:
- Reviewed Lobby.tsx: initializeConnection properly calls networkManager.connect()
- Reviewed NetworkManager.ts: Colyseus client initialized correctly
- Reviewed server logs: Server shows "listening on ws://localhost:2567"
- Issue: CORS error in browser console - server CORS config missing
```

## Bug Report Message (v2.0)

When reporting a bug, send a `bug_report` message to PM with full bug details:

````json
{
  "id": "msg-pm-{timestamp}-001",
  "from": "qa",
  "to": "pm",
  "type": "bug_report",
  "priority": "high",
  "payload": {
    "taskId": "{taskId}",
    "bugs": [{
      "file": "src/file.ts",
      "line": 42,
      "issue": "Type error: Type 'string' is not assignable...",
      "severity": "critical",
      "summary": "Build fails with TypeScript error",
      "steps": ["Run npm run build", "Observe error"],
      "expected": "Build succeeds",
      "actual": "TS2322 error"
    }]
  },
  "timestamp": "{ISO_TIMESTAMP}"
}
````

**⚠️ V2.0:** QA does NOT update prd.json directly. PM syncs bug information from bug_report message.

**Note:** Commit format templates for failed validations are in `qa-workflow` skill.

---

## Checklist

Before submitting bug report:

- [ ] **Code review performed** - Read and traced the actual implementation files
- [ ] **Actual behavior verified** - Ran the app and observed what actually happens
- [ ] Summary is clear and specific
- [ ] Reproduction steps are complete
- [ ] Expected vs actual clearly stated
- [ ] Console errors included
- [ ] Screenshots attached (if visual)
- [ ] Severity assigned
- [ ] Category assigned
- [ ] Environment specified
- [ ] bug_report message sent to PM

## Reference

- [agents/qa/AGENT.md](../../AGENT.md) — Full QA instructions
- [agents/qa/skills/validation-workflow.md](validation-workflow.md) — Full workflow
