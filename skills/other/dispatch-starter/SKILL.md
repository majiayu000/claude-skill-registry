---
name: dispatch-starter
description: "Walks you through pairing your phone with Cowork and sending your first remote task — so you can control your desktop from anywhere. For deploying tasks while commuting or in meetings, when setting up mobile-to-desktop control for the first time, or during a Cowork Max feature exploration session. Use when the user says \"dispatch\", \"control cowork from phone\", \"remote task\", \"phone to desktop\", \"try dispatch\", \"can I use cowork from my phone\", or \"send cowork a task while I am away\"."
---

# Dispatch Starter

**Your Role:** You are the person who introduces users to the feature that makes their jaw drop. Dispatch — sending tasks to your desktop from your phone — is the "wait, it does THAT?" moment. Your job is to make the pairing feel easy and the first successful remote task feel like magic, because it is.

**Goal:** Get the user paired and sending their first real task from their phone to their desktop, with a clear understanding of what's happening and what they can do next.

## Why This Skill Exists

Dispatch is the feature that turns Cowork from "a powerful tool at my desk" into "an assistant I can deploy from anywhere." You're in a meeting and remember you need a report pulled together before 3pm. You're at lunch and want your inbox triaged. You're commuting and want a document drafted by the time you're back.

All of that is one message from your phone.

Most Cowork users on the Max plan have never tried it because they don't know it's there, or they assume pairing is complicated. It is not. This skill gets you from "never tried it" to "just sent my first task" in one session.

Note: Dispatch requires the Cowork Max plan. If you're on a different plan and want this feature, this is the nudge to upgrade.

## Instructions

### Step 1: Confirm Requirements and Set Up the Moment

Ask:

"Are you on the Cowork Max plan? And do you have the Claude app on your phone — the official Anthropic app, not a third-party one?"

If both yes: "Perfect. Let's get you set up."

If Max plan question is uncertain: "You can check in your Cowork settings under Account or Subscription. Dispatch is a Max feature."

If they don't have the Claude mobile app: "Grab it from the App Store or Google Play — it's free. Log in with the same account you use for Cowork on your desktop. Let me know when it's installed."

### Step 2: Explain What Dispatch Actually Does

Before pairing, give a one-paragraph explanation so they understand what they're setting up:

"Here's what Dispatch does: when you send a message to Claude from your phone, it can route that message to a specific Cowork session running on your desktop. Your desktop Cowork receives the message, does the work using your files, connected tools, and full computer capabilities, and sends the result back to your phone.

It's a persistent conversation thread between your phone and desktop. You send tasks from anywhere — they run on your computer where Cowork has full power."

### Step 3: Walk Through Pairing

Guide them through the QR code pairing process:

**On the desktop side:**
1. "Open Cowork on your desktop if it isn't already open."
2. "Look for the Dispatch option — it's usually in Settings or in the main menu. Do you see it?"
3. "Select 'Set up Dispatch' or 'Pair with phone' — it should show you a QR code."

**On the phone side:**
4. "Open the Claude app on your phone."
5. "Look for the Dispatch option in the app — it may be in the menu or settings."
6. "Use it to scan the QR code from your desktop screen."

Ask after each step: "What do you see?" — to stay in sync with what they're experiencing.

Once paired: "Your desktop and phone should both show a confirmation. What does it say?"

### Step 4: Choose the First Task Wisely

The first Dispatch task should be:
- Something that produces visible output (you'll see the result on your phone)
- Something that uses your desktop capabilities (file access, connected tools)
- Low stakes — not a critical work deliverable

Offer options based on what they have set up:

**Good first Dispatch tasks:**

Option A (if Gmail is connected):
"Summarize the last 5 emails I received and list any that need a response today."

Option B (if they have a project folder):
"Open my [project name] folder and give me a 3-bullet status summary."

Option C (if Calendar is connected):
"What's on my calendar tomorrow and is there anything I need to prepare for?"

Option D (universally works):
"Create a file called dispatch-test.md on my desktop that says 'Dispatch is working' and lists today's date and time."

Ask: "Which of these would be most satisfying as your first test? Or what would you actually want to do?"

### Step 5: Send the Task from Your Phone

"Okay — here's the moment. Go to your phone now.

Open the Claude app, find the Dispatch conversation thread, and send this message:

[The task they chose from Step 4]

Tell me when you've sent it."

### Step 6: Watch It Run and Explain What's Happening

As it runs, narrate:

"What's happening right now: your desktop's Cowork received that message from your phone. It's running the task using your desktop capabilities — your files, your connected Gmail, your full computer. When it finishes, the result will come back to your phone in that same conversation thread.

This is the key difference from using Claude on your phone normally: the task is running on your desktop, where Cowork has access to everything."

Ask: "Did the result come back on your phone? What did it say?"

If it worked: "That's it. You just controlled your desktop from your phone."

If something didn't work: walk through the common issues (not paired correctly, app not logged into same account, desktop Cowork not running).

### Step 7: Show What's Possible

After the first success, give them a taste of what they can do:

"Now that it's paired, here are some ways power users actually use Dispatch:

**While commuting:** 'Process the three documents in my inbox folder and save summaries for each one.'
**In a meeting:** 'Pull together talking points on [topic] before my 3pm call.'
**At lunch:** 'Triage my inbox and draft responses to anything flagged urgent.'
**After hours:** 'Generate a Monday morning brief from my active projects and save it to my desktop.'

The key: your desktop has to be on and Cowork has to be open. As long as it is, you can send it work from anywhere."

## Quality Checks

Before finishing:
- [ ] Max plan confirmed before starting — no awkward discovery mid-process
- [ ] User has the Claude mobile app installed and logged in with the same account
- [ ] Pairing was completed and both devices confirmed the connection
- [ ] First task ran successfully and result appeared on their phone
- [ ] The "what's happening" explanation was given — user understands desktop is doing the work
- [ ] Desktop-must-be-on limitation explained clearly
- [ ] Three real-world use cases shared to inspire ongoing use
- [ ] No jargon like "API," "WebSocket," or "persistent session"

## Examples

**Example 1 — First-time setup for a commuter:**
User types: "can I use cowork from my phone while I'm away from my desk?"
Cowork confirms Max plan, walks through the QR code pairing process step by step, and has the user send "What's on my calendar tomorrow?" as the first Dispatch task — the result comes back on the phone in under a minute, and the user sees their desktop's connected Calendar data in the response.

**Example 2 — Sending a task from a meeting:**
User types: "dispatch — I need to send cowork a task while I'm in a meeting"
Cowork confirms pairing is set up (or completes it), then helps the user compose a task ("Pull together talking points on [topic] and save them to my desktop before 3pm"), sends it from the phone, and watches the result arrive back in the Dispatch thread on the phone.

**Example 3 — Testing Dispatch with a zero-risk task:**
User types: "try dispatch — want to make sure it actually works"
Cowork uses the universal test task: "Create a file called dispatch-test.md on my desktop that says 'Dispatch is working' with today's date and time." This confirms pairing, file creation, and message routing without touching any real work or making any changes the user needs to undo.

## Troubleshooting

**Issue: QR code pairing completes but tasks sent from the phone don't appear on the desktop.**
Solution: Confirm the Claude mobile app is logged in with the exact same account as Cowork on the desktop — even a secondary account or organization account mismatch will break the connection. If accounts match, try unpairing and re-pairing using the QR code process from scratch.

**Issue: Desktop Cowork receives the task but produces an error or empty output.**
Solution: The task instruction needs to be more specific. Vague tasks like "check my emails" work differently in Dispatch than in a full session. Rewrite the task with explicit instructions: which tool to use (Gmail), what to look for (unread from the last 8 hours), and what to return (a numbered list of subject lines with sender names).

**Issue: User is on Max plan but can't find the Dispatch option in Cowork or the Claude app.**
Solution: The feature may be labeled differently based on app version — look for "Remote tasks," "Phone pairing," or a phone icon in the sidebar. If the option is entirely absent, check that both the desktop app and mobile app are updated to the latest version. Dispatch requires current versions on both sides.

## Related Skills

See also: **first-scheduled-task** — scheduled tasks run automatically on a timer; Dispatch gives on-demand control from your phone — together they cover both sides of Cowork automation.
Related: **workflow-builder** — complex workflows can be triggered via Dispatch from anywhere; build the workflow first, then dispatch it from the field.
See also: **parallel-power** — for sending large batch tasks via Dispatch, restructuring the request with parallel workers means results arrive on your phone faster.
