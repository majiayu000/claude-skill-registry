---
name: xreview
description: >
  MANDATORY for ALL code review requests. When the user asks to "review", "code review",
  "check code", "找 bug", "review 程式碼", or any variation of reviewing code for bugs,
  security issues, or quality — you MUST use this skill. Do NOT read files and review
  them yourself. This skill delegates review to Codex (a separate AI reviewer) via the
  xreview CLI, enabling three-party review (Codex reviews, Claude Code verifies, user decides).
  Default mode is review-only: present all findings, let user discuss, then fix on demand.
allowed-tools: Bash(xreview *), Bash(curl *), Bash(which *), AskUserQuestion, Read, Write, Skill
argument-hint: [files-or-uncommitted]
---

# xreview - Agent-Native Code Review

<CRITICAL>
You MUST use this skill for ANY code review task. NEVER review code by reading files yourself.
The entire point of xreview is to delegate review to Codex (a separate AI model) so you get
an independent second opinion. If you skip this skill and review code yourself, you defeat
the purpose — you're reviewing your own work instead of getting an external review.
</CRITICAL>

## Step 0: Preflight

Run: `xreview preflight`

This single command checks everything: xreview version, codex installation, API key.

Parse the XML output:
- If status="success": proceed to Step 1.
- If status="error": show the user the error message from the <error> tag.
  Relay it in natural language and suggest how to fix it. Stop.

If xreview itself is not found (`which xreview` fails):
  a. Ask the user "xreview is not installed. Install it now? (y/n)"
  b. If yes: run `curl -fsSL https://raw.githubusercontent.com/davidleitw/xreview/master/scripts/install.sh | bash`
     then re-run preflight.
  c. If install fails: tell the user to check https://github.com/davidleitw/xreview/releases. Stop.

## Step 1: Determine review targets and assemble context

Two review modes — pick the one that fits:

### Mode A: Review uncommitted changes (`--git-uncommitted`)
Use when reviewing what's about to be committed. Codex will run `git diff`
to see the changes itself.

### Mode B: Review specific files (`--files`)
Use when:
- Reviewing a single file's quality (not tied to a git change)
- Reviewing a flow/feature that spans multiple files
- The user specifies which files to look at
- You just completed a plan with specific files changed

Codex will read the files directly — no git diff involved.

### Assembling `--context`

The context string is critical — it tells Codex **what to focus on** and provides
background for the final review report. Include as much relevant context as you have.

For **git-uncommitted** (change-focused):
```
--context "【背景】why this change is being made — the motivation or problem being solved
【變更類型】feature | refactor | bugfix
【描述】what was changed — specific functions, modules, or behaviors modified
【進度】current status — e.g. 'implementation complete, pre-commit review' or 'WIP, reviewing direction'
【預期行為】what this code should achieve (for refactor: 'behavior should be identical to before')
【未完成】anything not yet done or known limitations, if applicable"
```

For **files** (flow/feature review):
```
--context "【背景】why this review is needed — e.g. 'new feature ready for review', 'investigating production bug'
【Review 焦點】what to focus on — e.g. 'Review the CMS push event flow:
enqueue → EventQueue.push() → purge logic → SendQueue routing.
Focus on concurrency safety and lock correctness across these files.'
【進度】current status of the work
【預期行為】expected behavior — e.g. 'cache and ordered paths are fully independent, no cross-locking'"
```

For **files** (single file quality):
```
--context "【背景】why reviewing this file — e.g. 'recently refactored, want quality check'
【Review 焦點】General quality review of event_queue.cpp.
Look for bugs, race conditions, error handling issues.
【進度】current status"
```

The better the context, the better Codex's review AND the better the final report.
Be specific about the flow direction, expected behavior, and areas of concern.
Include background motivation — this gets stored in the session and used when
generating the review report.

## Step 2: Run review

Run: `xreview review --files <paths> --context "<structured context>"`
 or: `xreview review --git-uncommitted --context "<structured context>"`

## Step 2.5: Verify + Present

<CRITICAL>
- You MUST independently verify EVERY finding before presenting to the user.
- Do NOT blindly copy Codex output. You are a capable code reviewer — USE your judgement.
- The xreview output includes `<agent-instructions>` after `</xreview-result>`. Follow them.
</CRITICAL>

Parse the XML output from Step 2.

If verdict is APPROVED (zero findings): tell the user "No issues found." Skip to Step 5.

### Phase 1: Verify Each Finding

Group findings by file. For each file, read it ONCE, then verify all findings in that file.

For EACH finding:

1. **Read the actual code** at the file:line (reuse the file content if already read for another finding in the same file).
2. **Analyze validity** — does the issue actually exist?
   - For concurrency/lock findings: check lock scope (nested vs sequential locking),
     whether locks are actually held simultaneously, real contention scenarios.
   - For logic findings: trace the actual code path end-to-end.
   - For security findings: confirm untrusted input actually reaches the vulnerable code.
3. **Classify**:
   - **CONFIRMED**: the issue is real, you verified it in the code.
   - **SUSPECT**: you believe it may be a false positive.

For SUSPECT findings, challenge Codex before dropping them:

Run: `xreview review --session <session-id> --message "F-XXX appears to be a false positive: <your reasoning>. Please re-evaluate."`

Parse the response:
- If Codex agrees → drop the finding (don't present to user)
- If Codex provides valid counter-reasoning → mark as CONFIRMED
- If disagreement persists → present both perspectives to user with a note

### Phase 2: Present All Confirmed Findings

After verification, present ALL confirmed findings to the user. For EACH finding:

1. **Header**: `### F-XXX [SEVERITY/category] title`
2. **Location**: `📍 file:line`
3. **Code**: quote the code you read in Phase 1
4. **Trigger**: the condition that triggers this issue (from YOUR verification)
5. **Impact**: what happens if exploited/triggered
6. **Cascade**: list cascade impacts (what else breaks)
7. **Suggested fixes**: ALL alternatives with effort levels, mark recommended

Low severity findings may use a shorter format but MUST still include suggested fixes.

After ALL findings, tell the user:

```
以上是本次 review 的發現。你可以：
- 討論任何 finding 的細節
- 告訴我要修哪些（例如「修 F-001 和 F-003」）
- 如果有其他想讓 Codex 檢查的方向，也可以告訴我
```

**Stop here. Wait for the user to respond.** Do NOT auto-proceed to fixing.

## Step 3: Discussion

This is a free-form conversation. Handle user messages based on their intent:

- **User asks about a finding** (e.g. "F-001 的影響範圍?")
  → Read code, explain context and details.

- **User challenges a finding** (e.g. "F-002 那邊上層已經檢查過了")
  → Re-verify against code. If the user is right, update classification and tell them.

- **User asks Codex to check something new** (e.g. "還有沒有其他 SQL injection?")
  → Run: `xreview review --session <session-id> --message "<user's question>"`
  → Verify any new findings (Phase 1 process), then present them (Phase 2 format).

- **User requests fixes** (e.g. "修 F-001 和 F-003")
  → Proceed to Step 4.

## Step 4: Fix + Verify

When the user specifies which findings to fix:

1. Apply fixes for the specified findings only.
2. Run verification:
   `xreview review --session <session-id> --message "<message>"`

   The message MUST include:
   - Which findings were fixed and how
   - Which findings were dismissed and why
   - Scope instruction: "Verify fixes and check for new issues introduced by the changes.
     Only report NEW findings directly caused by or exposed by the fixes.
     Do NOT report pre-existing issues unrelated to the changes."

3. Parse the result:
   - All resolved → proceed to Step 5.
   - New/reopened findings → verify and present them (same Phase 1 + Phase 2 format),
     let user decide again.
   - Maximum 5 rounds → inform user of remaining items, proceed to Step 5.

## Step 5: Finalize

<CRITICAL>
You MUST invoke the write-report skill here. Do NOT manually run `xreview report`
or generate the summary yourself. The write-report skill produces a human-readable
markdown report that is far more useful than a raw table.
</CRITICAL>

Call the Skill tool:
- skill: `write-report`
- args: `<session-id>`

Stop here. The write-report skill handles report generation, saving, and session cleanup.

## Important notes

- ALWAYS present findings in plain language, NOT raw XML.
- The <error> messages from xreview are written for you (an AI agent). Use them
  to understand what went wrong and explain it to the user naturally.
- Do NOT read or write .xreview/ directory files directly. Use only xreview CLI commands.
- The session ID is in the XML output's session attribute. Track it for resume calls.
- If any xreview command fails, show the error to the user and ask how to proceed.
- This is a THREE-PARTY REVIEW: Codex (reviewer), you Claude Code (verifier), and the
  user (decision maker). Present ALL verified findings and let the user decide which
  to fix. The user always has final say, including the option to not fix any finding.
- Use --message to convey user decisions and your reasoning to Codex. Codex is smart
  enough to reconsider when given good reasoning from the user.

## XML Schema Reference

See [reference.md](reference.md) for the complete XML schema documentation.
