---
name: os-done-or-not
description: >-
  ALWAYS invoke this skill when work wraps up or the user asks how it went -
  "done or not", "are we done", "what happened", "report" - in any language,
  and when a Stop hook asks for a session report. Produces a ten-line plain-
  language report: a lead, a checkmark table, and a verdict - fully done,
  anything needed from you, new debt, safe to close. Every "yes" names its
  proof; unverified says "not checked". Saves the report so the next session
  starts from it instead of re-exploring the repo.
allowed-tools:
  - "Read(~/.claude/open-steps/**)"
  - "Edit(~/.claude/open-steps/**)"
  - "Bash(gh pr view *)"
  - "Bash(gh pr checks *)"
  - "Bash(gh pr checks)"
---

# os-done-or-not

One question, one screen: **did the agent finish, and what actually happened**
- in words a reader who does not code will understand. Nothing happened (pure
questions, no files touched) → one line saying so, no report.

## Language

The language the user speaks in this session, detected from the conversation
- translate every template label. Code, files, commands stay English.

## Step 1 - gather proof that takes seconds

Fast checks only; never re-run the test suite - use results this session
already produced. Not confirmable in seconds, or still running → **"not
checked"**, never "yes".

```bash
git status --porcelain            # uncommitted?
git log --oneline -10             # what landed
git log origin/HEAD..HEAD --oneline 2>/dev/null   # unpushed?
gh pr view --json state,mergeStateStatus && gh pr checks   # if a PR exists
```

## Step 2 - name the outcome

Sessions end one of eight ways; pick the match **before** writing, or the
report says "fully done: yes" and "safe to close: no" in the same breath.

| # | Outcome | Verdict shape |
|---|---|---|
| 1 | Shipped and verified | done Yes · nothing needed · close Yes |
| 2 | Done - one action is yours | done Yes · needed = that action · close Yes |
| 3 | Stalled on your decision | done No · needed = the decision · close No |
| 4 | Partly done, rest deferred | core Yes, rest recorded as debt · close Yes |
| 5 | Didn't work - rolled back | done No · lead = what was learned · close Yes |
| 6 | Something broke | lead opens with ⚠️ · risk in full (rule 7) · close No |
| 7 | Research only | the answer is the result · skip ship rows · close Yes |
| 8 | Nothing to report | one line, no report, no file |

Outcomes 5 and 6 are where reports start lying; "the approach failed and was
rolled back" is a complete result.

## Step 3 - write the report (translate the labels, keep the shape)

```
<Lead: 1–2 sentences. What changed for the product. Best result first.>

| | |
|---|---|
| ✅ | <done, and what proves it> |
| ⚠️ | <surprise or bad news> |
| ⏳ | <deferred, and until when> |

**Verdict**

| | |
|---|---|
| Fully done?              | Yes / No / Not checked |
| Anything needed from you?| No / <one concrete action> |
| New debt?                | No / <how many, where recorded> / Not checked |
| Safe to close?           | Yes / No - <reason in five words> |
```

Checkmark rows: two to five; drop an empty row, never a non-empty ⚠️. Verdict
cells are one line each - detail lives in the checkmark rows, not the verdict.

Two conditional rows, only when the session makes them real - never "not
applicable": **Easy to undo?** (Yes - how / Hard - why) and **Security
touched?** only when yes - one line: exposed what, closed how. Deliberately no
"live for users?" row: unmerged it repeats the action line; merged but not
reaching users is a surprise - a ⚠️ row.

## Step 4 - save it

Write to both paths, creating directories as needed - never anywhere else
under `~/.claude`, never into the user's project:
- `~/.claude/open-steps/reports/<project-folder-name>/latest.md` - overwritten
- `~/.claude/open-steps/reports/<project-folder-name>/history/<YYYY-MM-DD-HHMM>.md`

Head the file with date, project, ticket. **Two parts; only part one goes in
the chat.** Part one - the report above, for the person. Part two - for the
next session, which reads it instead of re-exploring the repository; the only
home for engineering identifiers.

```
---
## Technical detail - for the next session, not the reader above

- Branch / worktree / PR and their state; commits made this session
- Files changed, with paths; test and check results as measured
- Commands worth re-running; the first thing to look at next
```

Terse, factual, a handover note; nothing changed → omit part two.

## Jargon → plain words

Examples of the move - apply it in the user's language. A ticket or PR number
naming an action ("review PR #892") stays; elsewhere say what it changed.

| Don't write | Write |
|---|---|
| `a1b2c3d`, commit, SHA | "the version" - or drop it |
| deploy, prod | "put it on the live product", "the live product" |
| CI green, checks passed | "all the automatic checks passed" |
| fail-closed, the gate fired | "the safety check refused to ship it - correctly" |
| migration / rollback | "a change to the database" / "put it back as it was" |
| tech debt / flaky test | "an unfinished bit, written down" / "a check that sometimes lies" |

## Hard rules - these rules *are* the skill

1. One screen: about 10 lines, 15 the ceiling.
2. Lead with the outcome - best thing first, never the chronology.
3. Numbers a human can use - counts, money, time; hashes, branch names and
   build IDs stay out unless asked.
4. Translate every term; no plain equivalent → say what the user would *see*.
5. Every "yes" names its proof; no proof → "not checked".
6. Bad news gets its own ⚠️ row - never buried inside another line.
7. Exception, do not compress: an unhandled security risk or data loss is
   spelled out plainly - in the lead and its ⚠️ row, never by inflating a
   verdict cell. A handled risk is one line: exposed what, closed how.

## Known gotchas

- "New debt? - No" gets written when there is no debt and when nobody looked;
  say "no" only after checking.
- Neither a green check nor a merge means users have it: landed-but-unreached
  gets a ⚠️ row naming what would ship it - the most common way a report ends
  up technically true and practically wrong.
- An approval can be revoked - a verdict is a snapshot; say so while a review
  is open.
- Do not grow the table: ten rows is a wall of text in a table costume.
- Matches none of the eight → say what happened; the list serves honesty.
