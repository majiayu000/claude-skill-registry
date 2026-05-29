---
name: session-begin
description: Complete verification steps before starting any work session
---

# Session Begin Checklist

**⚠️ IMPORTANT - Duplicate Detection:**

Before proceeding with the full checklist, check if this session was already
started:

1. **Read the current conversation context** - Have I already completed this
   checklist in the current conversation?
2. **Check SESSION_CONTEXT.md timestamp** - Was "Last Updated" modified today?
   - **Note**: Field stores date only (YYYY-MM-DD), not time. Sub-day duplicate
     detection relies on conversation context check (#1) and session counter
     check (#3).
3. **Check session counter** - Did I already increment the session counter
   earlier in this conversation?

**If ANY of these are true:**

- ✅ Session is already active
- ⚠️ DO NOT re-run the checklist
- ⚠️ DO NOT re-increment the session counter
- ⚠️ DO NOT re-run startup scripts
- 💬 Example response: "Session #35 already active (started earlier in this
  conversation). Checklist completed earlier. What would you like to work on?"

**If ALL are false:**

- ✅ This is a new session
- ✅ Proceed with full checklist below

---

Before starting any work, complete these verification steps:

## 0. Secrets Decryption Check (REMOTE SESSIONS)

**Check if MCP tokens need decrypting:**

```bash
# Check secrets status
if [ -f ".env.local.encrypted" ] && [ ! -f ".env.local" ]; then
  echo "⚠️ Encrypted secrets found but not decrypted"
fi
```

**If secrets need decrypting:**

1. **Ask the user for their passphrase** - Example: "Your MCP tokens need
   decrypting. What's your passphrase?"
2. **Run the decrypt command** using stdin (avoids shell history exposure):
   ```bash
   echo "<user_passphrase>" | node scripts/secrets/decrypt-secrets.js --stdin
   ```
3. **Verify success** - Check that `.env.local` now exists with tokens
4. **Never store or log the passphrase** - Only use it for the decrypt command

**Security note:** Using `--stdin` with echo pipe is safer than env vars, which
can leak to shell history and process listings.

**If secrets are already decrypted or no encrypted file exists:**

- Skip this step and continue to Context Loading

---

## 1. Context Loading (MANDATORY)

- [ ] Read [SESSION_CONTEXT.md](../../SESSION_CONTEXT.md) - Current status,
      active blockers, next goals
- [ ] Increment session counter in
      [SESSION_CONTEXT.md](../../SESSION_CONTEXT.md)
- [ ] Check [ROADMAP.md](../../ROADMAP.md) for priority changes

## 1b. Stale Documentation Check (MANDATORY - NEW)

**Documentation often drifts from reality.** Before trusting any status in docs,
verify against actual commits:

```bash
# Check recent commits to see actual work done
git log --oneline -30

# Check commits since last documented session date
git log --oneline --since="YYYY-MM-DD"
```

**Compare commits against documented status:**

1. Look for PR/feature commits (e.g., "PR7:", "refactor:", "fix:")
2. Cross-reference with INTEGRATED_IMPROVEMENT_PLAN.md task checkboxes
3. If commits show work done but docs show incomplete → **UPDATE THE DOCS**

**Common discrepancies to check:**

- Step 4B PRs: Check for commits like "PR7:", "PR8:", etc. and verify checkboxes
  match
- Session counter: Check AI_REVIEW_LEARNINGS_LOG.md version history for session
  numbers
- Test counts: Run `npm test` to verify actual vs documented

**If docs are stale:**

1. Update the stale document with correct status
2. Note which sessions failed to update docs
3. Commit the corrections before proceeding

## 2. Consolidation Status Check

Check [AI_REVIEW_LEARNINGS_LOG.md](../../docs/AI_REVIEW_LEARNINGS_LOG.md) for
the "Consolidation Trigger" section:

- If "Reviews since last consolidation" >= 10: **⚠️ CONSOLIDATION WAS MISSED**
- This means patterns from previous reviews are NOT in claude.md context
- Previous session should have consolidated but didn't

**If consolidation was missed:**

1. Note this in your session summary
2. The patterns are still available in AI_REVIEW_LEARNINGS_LOG.md (read if
   needed)
3. Consolidation will happen at THIS session's end

## 3. Documentation & Planning Awareness

- [ ] Check
      [INTEGRATED_IMPROVEMENT_PLAN.md](../../docs/archive/completed-plans/INTEGRATED_IMPROVEMENT_PLAN.md)
      for current step
- [ ] Note: Archive files in `docs/archive/` are excluded from linting
- [ ] Completed plans are archived to `docs/archive/completed-plans/`

## 4. Skill Selection (BEFORE starting work)

```
DECISION TREE:
├─ Bug/Error? → Use 'systematic-debugging' skill FIRST
├─ Writing code? → Use 'code-reviewer' agent AFTER completion
├─ Security work? → Use 'security-auditor' agent
├─ UI/Frontend? → Use 'frontend-design' skill
├─ Complex task? → Check available skills with /skills
└─ Multi-step task? → Use TodoWrite to track progress
```

## 5. Code Review Handling Procedures

When receiving code review feedback (CodeRabbit, Qodo, etc.):

1. **Analyze ALL suggestions** - Read through every comment multiple times
2. **Create TodoWrite checklist** - Track each suggestion as a task
3. **Address systematically** - Don't skip items; mark as resolved or note why
   skipped
4. **Verify CI impact** - Check if changes affect workflows (ci.yml,
   docs-lint.yml)
5. **Test after changes** - Run `npm test` and `npm run lint` before committing

## 6. Anti-Pattern Awareness

**Before writing code**, scan claude.md Section 4 "Critical Anti-Patterns" and
[CODE_PATTERNS.md](../../docs/agent_docs/CODE_PATTERNS.md) Quick Reference
section (🔴 = critical patterns). Key patterns:

- **Read before edit** - Always read files before attempting to edit
- **Regex performance** - Avoid greedy `.*` in patterns; use bounded
  `[\s\S]{0,N}?`
- **ESLint flat config** - Spread plugin configs, don't use directly
- **Path-based filtering** - Add pathFilter for directory-specific patterns
- **Archive exclusions** - Historical docs should be excluded from strict
  linting

## 7. Session Start Scripts (AUTO-RUN)

**Execute these scripts automatically** when processing this command:

```bash
# Surface known anti-patterns (errors should be visible, not suppressed)
npm run patterns:check

# Check if multi-AI review thresholds reached
npm run review:check

# Surface past lessons relevant to current work
npm run lessons:surface
```

**Important**: These scripts are **required**. If any script fails:

1. Note the error in session summary
2. Investigate if it's a real issue vs missing script
3. If script missing, note it as "N/A" in audit

**Record results in session audit** - these must be marked as "Ran" or "Failed
(reason)" in `/session-end` audit.

## 8. Incident Documentation Reminder

**After encountering any significant errors or issues:**

- Document the issue in
  [AI_REVIEW_LEARNINGS_LOG.md](../../docs/AI_REVIEW_LEARNINGS_LOG.md)
- Use the standard "Review #XX" format
- Include: cause, fix, pattern identified, prevention steps
- This builds institutional knowledge for future sessions

---

Ready to begin session. What would you like to work on?
