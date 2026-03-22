---
version: 1.0.0
name: meta-wrap-up
description: >
  End-of-session checklist that reviews deliverables, updates daily memory,
  distills learnings, checks for documentation gaps, and optionally commits work.
  Use when the user says "wrap up", "close session", "end session", "wrap things up",
  "we're done", "that's it for today", "session done", or invokes /meta-wrap-up.
  Run at the end of any working session or after completing a major deliverable.
  Does NOT trigger for regular development work.
disable-model-invocation: false
---

# Wrap-Up — Session End

Execute all steps. Present findings to the user before committing anything.

## Step 1: Review Deliverables

Scan what happened this session:

1. Run `git status` and `git diff --stat` to see all changes
2. List every file created or modified, grouped by location:
   - `context/` — context files updated
   - `.claude/skills/` — skills created or modified
   - Source code — implementation work
   - Docs repo — documentation created/updated (if workflow-enabled)
   - Other locations — flag for review
3. **File placement check:** Verify outputs follow naming conventions:
   - Skills use `{category}-{function}` naming
   - Daily memory uses `YYYY-MM-DD.md` format (main sessions) or `YYYY-MM-DD_{session-name}.md` (sandbox sessions)
   - If anything is in the wrong place, flag it

## Step 2: Detect Sandbox Environment

4. Check if you're running inside an agentsandbox:
   - Check if the `AGENTSANDBOX_SESSION` env var is set
   - OR check if `/workspace/CLAUDE.md` exists (container indicator)
   - OR check if the current branch starts with `asb/` (`git symbolic-ref --short HEAD`)
   - If any is true, you are in a **sandbox session**
5. If in a sandbox session, determine the session name:
   - From `$AGENTSANDBOX_SESSION` env var (preferred)
   - Or from hostname: strip `asb-` prefix from `$HOSTNAME`
   - Or from branch name: strip `asb/{source}-` prefix

## Step 3: Update Daily Memory

6. Choose the correct filename:
   - **Main session**: `context/memory/{YYYY-MM-DD}.md`
   - **Sandbox session**: `context/memory/{YYYY-MM-DD}_{session-name}.md`
     - Example: `context/memory/2026-03-21_ux-study-test.md`
   - This keeps sandbox memory separate from main — no merge conflicts
7. For **full history context** in a sandbox, read from `.context-main/memory/` (read-only mount of main's context)
8. Update the session section with:
   - **Goal**: What the user wanted to accomplish
   - **Work Done**: Bullet points of what was accomplished
   - **Decisions**: Key decisions made and why
   - **Learnings**: Things discovered about the codebase, tools, or patterns
   - **Open Items**: Unfinished work, blockers, things to pick up next

## Step 4: Documentation Check (if workflow-enabled)

9. Read `workflow.json` to check if this is a workflow-enabled project
10. If yes, review the session for documentation gaps:

   **Decisions → ADRs:**
   - Were any architectural or technical decisions made this session?
   - If yes, does an ADR already exist for this decision?
   - If no ADR exists, suggest: "Decision about [topic] — want me to create an ADR?"

   **New features → PRDs/Design Docs:**
   - Was a new feature discussed or started?
   - Does it have a PRD or design doc?
   - If not, suggest: "New feature [name] — want a PRD or design doc?"

   **Architecture changes → C4 Diagrams:**
   - Were new components, services, or integrations added?
   - Do the C4 diagrams in the docs repo reflect these changes?
   - If not, suggest: "Architecture changed — C4 diagrams may need updating"

   **Incidents → Post-Mortems:**
   - Was a production incident investigated or resolved?
   - If yes, suggest a post-mortem

   **Research → Spike Reports:**
   - Was research or option comparison done?
   - If yes, suggest capturing it as a spike report

Present documentation suggestions as a checklist — the user picks what to do:
```
### Documentation Suggestions
- [ ] Create ADR for [decision about X]
- [ ] Update C4 container diagram (new service added)
- [ ] Create spike report for [research topic]
```

## Step 5: Distill to Long-Term Memory

10. Review today's session notes. Ask yourself:
    - Any lessons learned that future-me should know?
    - Any decisions that affect how we work going forward?
    - Any user preferences discovered?
11. If yes, update `context/MEMORY.md` with the distilled insight
12. If any context files (SOUL.md, USER.md) should be updated based on
    what you learned, suggest the changes to the user

## Step 6: Collect Feedback (Optional)

13. Ask the user briefly:
    - "Anything I should do differently next time?"
    - "Any preferences to remember?"
14. If they provide feedback, update the relevant context file

## Step 7: Commit (If Requested)

15. Only if the user asks to commit:
    - Stage relevant files
    - Draft a clean commit message (no AI mentions, no Co-Authored-By)
    - Show the message for approval before committing
    - If changes span multiple repos (project + docs), handle each repo separately

## Step 8: Cost Summary

16. Check if `~/.claude/metrics/costs.jsonl` exists. If it does, calculate today's total spend:
    ```bash
    jq -s '[.[] | select(.timestamp | startswith("'"$(date -u +%Y-%m-%d)"'"))] | {total_eur: (map(.estimated_cost_eur) | add), input_tokens: (map(.input_tokens) | add), output_tokens: (map(.output_tokens) | add), responses: length}' ~/.claude/metrics/costs.jsonl
    ```
17. Present the cost summary to the user:
    ```
    ### Today's Usage
    - Responses: N
    - Tokens: Xk input / Yk output
    - Estimated cost: €X.XX
    ```

## Step 9: Summary

18. Present a brief session summary:
    - What was accomplished
    - What's left for next time
    - Any context files that were updated
    - Any documentation suggestions that were deferred (so we remember next session)
    - Today's cost (from step 16)
