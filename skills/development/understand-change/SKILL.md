---
name: understand-change
description: "Teach the user to deeply understand a change through interactive tutoring: restating understanding, drilling into why/what/how, and quizzing until mastery. The active counterpart to a one-shot explanation. Use when the user asks to \"understand this change\", \"teach me this change\", \"help me understand what changed\", \"walk me through this change\", \"make sure I understand this\", \"quiz me on this\", or \"teach me what we did\"."
---

# Understand Change

Act as an effective teacher whose goal is the user's deep understanding of a change. Work incrementally, confirm mastery at each stage before advancing, and keep going until the user has demonstrated understanding of everything on the checklist.

## Step 1: Identify the Change

Pick the subject in priority order:

1. A commit, PR, or path passed as an argument — use that
2. The work produced in the current session — use that
3. Uncommitted work from `git status` and `git diff` — use that
4. The most recent commit when nothing else is in scope

When the guess is not obvious, name what was picked so the user can redirect before teaching starts.

## Step 2: Build the Understanding Checklist

Read the change in full: the diff, the touched files, related code, and any commit messages, plan, or PR description that explain intent. Then write a running checklist to `.turbo/understand/<slug>.md` where `<slug>` describes the change. Use a checkbox per item, grouped into three sections:

- **Problem** — what the problem was, why it existed, and the alternative approaches that were on the table.
- **Solution** — what the change does, why it was resolved this way, the design decisions, and the edge cases.
- **Context** — why this matters and what the change impacts elsewhere.

Cover both high level (motivation) and low level (business logic, edge cases). Update this file as the session progresses: check items off only once the user has demonstrated understanding, and add items when teaching surfaces a gap.

## Step 3: Teach Each Item Incrementally

Work through the checklist one item at a time. Do not advance to the next item until the user has demonstrated mastery of the current one. For each item:

1. **Have the user restate first.** Ask what they already understand about the item before explaining anything. This reveals where the gaps are.
2. **Fill the gaps from there.** Correct misconceptions and supply what is missing. Drill into why, then the deeper why behind it, and cover what and how as well.
3. **Adjust depth on request.** The user may ask for a simpler explanation, more detail, or a worked walkthrough as if onboarding a new teammate. Match the level they ask for.
4. **Show the evidence.** Display the relevant code, or use the debugger, when seeing it makes the point land.
5. **Confirm mastery by quizzing.** Verify understanding before checking the item off. Pose open-ended recall questions as plain text. For multiple-choice questions, use `request_user_input`: vary the position of the correct answer across questions, and reveal the correct answer only after the question is submitted. If the answer reveals a gap, return to step 2 for that item before moving on.

## Step 4: Confirm Full Mastery

The session continues until every checklist item is checked off. When the user signals they want to stop early but items remain, use `request_user_input` to confirm whether to end now or keep going. Once all items are demonstrated, summarize what the user now understands and close out.
