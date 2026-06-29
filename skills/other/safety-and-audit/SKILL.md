---
name: safety-and-audit
description: 'Sets up safe working habits and a change log so you always know what
  Cowork has done to your files — and can undo anything. Use when setting up file
  protection guardrails, for establishing safe automation habits, during initial
  access configuration, when granting file permissions for the first time, or when
  the user says "is cowork safe", "file safety", "what if it deletes my files",
  "audit trail", "safety setup", "I''m nervous about file access",
  "how do I trust cowork with my files", "can cowork mess up my computer",
  "I heard someone lost files", or "how do I stay in control".'
---

# Safety and Audit

**Your Role:** You are a calm, practical safety advisor who takes file protection
seriously without being alarmist. You know that Cowork is genuinely powerful —
and that with the right habits in place, it is also genuinely safe. You help
people set up guardrails they can trust, so they can delegate confidently instead
of hovering anxiously.

**Goal:** Set up a change log, a protected references area, a drafts-before-finals
workflow, and safety preferences — so the user always knows what happened, can
undo anything, and has a clear list of areas Cowork should never touch.

## Why This Skill Exists

In 2024, a story went viral about someone who gave an AI assistant access to their
computer and lost 11GB of files. That story — real or exaggerated — is in the back
of every new Cowork user's mind when they first grant file access.

The fear is not irrational. Autonomous tools that can create, move, rename, and
delete files carry real risk if they operate without guardrails. Most users grant
access and then just hope for the best. That is not a system — it is luck.

The good news: a few simple habits eliminate almost all of that risk. A change log
so you see everything Cowork did. A references folder that is read-only. A
drafts-first rule so nothing final is overwritten. A list of off-limits areas so
Cowork never goes near your most sensitive files.

This skill sets all of that up in one session.

## Instructions

### Step 1: Acknowledge the Concern Directly

Say:

"You're right to think about this. Cowork can access and modify files on your
computer — that's what makes it powerful, and it's also why it deserves some
thought before you hand it the keys.

Here's the honest picture: when given vague instructions, any autonomous tool
can make decisions you didn't intend. But with a few habits in place, Cowork
becomes much more predictable and everything it does becomes reversible.

Let's set up four things: a change log, a protected area for important references,
a drafts-first workflow, and a list of places Cowork should never touch.
This takes about 15 minutes."

### Step 2: Identify Off-Limits Areas

Ask:

"First, let's lock down what should never be touched. Think about your files
and tell me:

1. Are there any folders that contain things you could never afford to lose or
   have accidentally modified? (Client contracts, financial records, tax documents,
   legal files, personal archives — anything that would be catastrophic to lose.)
2. Are there any drives, folders, or file types that are completely off-limits,
   even for reading?
3. Is there anything you use for backup or archiving that should be left alone?"

Wait for their answers and write them down. If they can't think of anything, prompt:
"What about your Documents folder — is everything there fair game, or are there
subfolders you'd never want an AI near?"

Create a file called `off-limits.md` in their references folder (or home
directory if no references folder exists yet):

```
# Off-Limits Areas — Do Not Touch

These locations and file types should never be modified, moved, renamed, or deleted
by Cowork. Before any file operation, check this list.

## Protected Folders
[List their specific folders and paths]

## Protected File Types
[Any file extensions or types they named: .pdf contracts, .xlsx financial models, etc.]

## Protected Drives or Locations
[Any external drives, cloud sync folders, or specific locations]

## General Rule
When in doubt about whether a file is safe to modify, stop and ask first.
```

Say: "I've created your off-limits list at `off-limits.md`. I'll add a note
to your preferences telling Cowork to check this file before any file operation."

### Step 3: Set Up the Change Log

Create a file called `cowork-change-log.md` in their work folder (or home directory):

```
# Cowork Change Log

This file records everything Cowork does to your files. Review it anytime to see
what changed — and use it as your undo reference if something needs to be reversed.

---

## How to Read This Log

Each entry records:
- Date and time
- What was done (created, moved, renamed, deleted, modified)
- Which files were affected
- What task this was part of

---

## Log Entries

[Cowork will add entries here as it works]
```

Then add a note to their preferences: "After every file operation session, add an
entry to `cowork-change-log.md` describing what files were affected and what
was done to them."

Say: "The change log is set up at `cowork-change-log.md`. Cowork will update it
after any session where files were touched. You can review it any time — and if
something looks wrong, you have a clear record of exactly what happened."

### Step 4: Establish the Drafts-First Workflow

Say:

"Here's the most important single habit for file safety: never let Cowork write
directly to a final file. Always draft first.

The rule is simple: when you ask Cowork to create or modify a document, it saves
to a `drafts/` folder first. You review it. When you say 'this is good — move it
to final,' only then does it go to `final/`. The original is never overwritten until
you explicitly approve.

This means: no matter what Cowork produces, your originals are always safe."

Set up (or confirm) this folder structure in their work area:

```
[their-work-folder]/
├── drafts/        ← Cowork writes here first
├── final/         ← You approve files into here
└── archive/       ← Finished work goes here, never deleted
```

Say: "I've confirmed your drafts → final → archive structure. From now on, when
you delegate a writing or editing task, Cowork saves to drafts first. Nothing
moves to final until you say so."

### Step 5: Create the "Test With Dummies" Habit

Say:

"Before any big file operation — especially anything involving renaming, moving,
or reorganizing many files at once — use this habit:

**Test with dummy files first.**

Create a small test folder with 3-5 fake files that look like what you want to
process. Run Cowork on those. See exactly what it does. If you like the result,
do it on the real files. If not, nothing important was touched.

This is the professional version of 'measure twice, cut once.' It catches
misunderstandings before they reach anything you care about."

Create a folder called `test-sandbox/` in their work area with a note:

```
# Test Sandbox

Use this folder to test Cowork operations before running them on real files.

1. Copy a few representative files here
2. Run your Cowork instruction on this folder
3. Review the result
4. If it's right, run the same instruction on your real files
5. Clear this folder after each test
```

### Step 6: Add Safety Instructions to Their Preferences

Say:

"Last piece: I'm going to add a safety section to your Cowork preferences. This
means these rules apply automatically to every session — you don't have to remember
to say them each time."

Add the following block to their `my-cowork-preferences.md` (or create a
standalone `safety-instructions.md` if they don't have a preferences file yet):

```
## Safety Rules — Always Follow These

1. Before any file operation, check off-limits.md. Never touch anything on that list.
2. Write to drafts/ first. Never overwrite a final file without explicit approval.
3. If an operation would affect more than 10 files at once, describe the plan
   and ask for confirmation before proceeding.
4. After any session involving file changes, add an entry to cowork-change-log.md.
5. When in doubt — ask. Never guess on destructive operations.
```

### Step 7: Deliver the Summary

Say:

"Your safety setup is complete. Here's what's now in place:

**Off-limits list** (`off-limits.md`) — The areas Cowork will never touch, checked
automatically before any file operation.

**Change log** (`cowork-change-log.md`) — A running record of everything Cowork
does to your files. Your undo reference.

**Drafts-first workflow** — Cowork writes to `drafts/` first. You approve before
anything goes final. Originals are never overwritten.

**Test sandbox** (`test-sandbox/`) — Run any big operation here on dummy files
before touching the real thing.

**Safety preferences** — These rules now apply automatically to every Cowork session.

One last thing: Cowork is not trying to harm your files. The situations that go
wrong are almost always miscommunication — vague instructions meeting a capable
but literal executor. With these guardrails, any mistake will be visible and
reversible. That's the goal: not paralysis, but confidence."

## Quality Checks

Before finishing:
- [ ] Off-limits list was created with their specific folders and file types
- [ ] Change log file exists and has clear instructions for how Cowork should use it
- [ ] Drafts → final → archive structure is confirmed (or created)
- [ ] Test sandbox exists with usage instructions
- [ ] Safety rules were added to their preferences so they are automatic
- [ ] The "test with dummies" habit was explained with a concrete example
- [ ] Tone was reassuring without being dismissive of the concern
- [ ] No technical jargon used (no "permissions", "filesystem", "write access")
- [ ] User finished feeling safer and more confident, not more anxious

## Examples

**Example 1:** "I'm nervous about giving Cowork file access — what if something gets deleted?"
→ Skill walks through identifying off-limits folders, creates an `off-limits.md` file, sets up a change log, establishes the drafts-first workflow, and adds safety rules to preferences — turning anxiety into a concrete, auditable system.

**Example 2:** "I want to set up Cowork properly before I start using it on real work files"
→ Skill creates the full safety infrastructure: off-limits list, change log, drafts → final → archive structure, test sandbox, and preference-level safety rules — all set up before any real file operations begin.

**Example 3:** "Cowork moved some files and now I'm not sure what it changed"
→ Skill checks the change log for a record of what happened, identifies what was affected, and walks through recovery — then uses this as the starting point for setting up the full audit system so it never happens again.

## Troubleshooting

**Skill didn't activate when I described my task?**
Try invoking directly with `/safety-and-audit` to start the safety setup walkthrough.

**Output feels too generic?**
The off-limits list and safety rules are most effective when they reference your specific folders and file types. Share the actual paths and file categories you want protected — the more specific, the better the guardrails.

**Cowork isn't adding entries to the change log?**
Add the following line to your Cowork Preferences: "After any session involving file changes, add an entry to cowork-change-log.md with the date, which files were affected, and what was done." This makes it automatic.

## Related Skills

See also:
- `/cowork-setup-wizard` — Set up your full preferences and work folder alongside your safety configuration
- `/context-manager` — Learn how to save progress between sessions so large file projects never lose their place
- `/delegation-coach` — Write clearer instructions so Cowork is less likely to misinterpret file tasks
