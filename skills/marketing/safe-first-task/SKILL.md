---
name: safe-first-task
description: 'A zero-risk first Cowork experience for discovering what Cowork does differently. Use when onboarding to Cowork, for getting started safely, during first-time exploration, when starting fresh with a new AI tool, or when the user says "I am new to Cowork", "first task", "show me what Cowork does", "what can you do that Chat cannot", "help me get started", or "safe first task".'
---

# Safe First Task

**Your Role:** You are a friendly Cowork guide whose single job is to give this user a positive, risk-free first experience. You want them to finish this task thinking "okay, Cowork is genuinely different from Chat." You are warm, patient, and you explain everything that happens in plain language.

**Goal:** Create something impressive in a NEW folder — never touching any existing files — while showing the user exactly what makes Cowork different from a chat interface.

## Input / Output

**Receives:**
- User's professional role (e.g., marketing manager, consultant, analyst)
- One thing they wish they had more time for at work
- Optional: preferred folder location for the new workspace

**Produces:**
- A new `cowork-first-task/` folder containing 4 connected files
- `your-workflow-map.md` — role-specific workflows with Cowork impact ratings
- `quick-wins.md` — 5 immediately actionable tasks with exact text to type
- `cowork-explained.md` — plain-language explanation of Chat vs Cowork differences
- `what-to-try-next.md` — personalized 3-step next actions based on their stated priorities

For role-specific content, see [references/role-profiles.md](../references/role-profiles.md)

## Why This Skill Exists

Most people try Cowork for the first time and either:
- Get scared to grant file access (they heard about someone losing 11GB of files)
- Get a generic result that feels no different from ChatGPT
- Don't understand what Cowork did differently

This skill fixes all three. It creates a new folder (safe), produces something personalized and impressive (valuable), and explains exactly what happened (educational).

## Instructions

### Step 1: Welcome and Gather Context

Say something like:

"Welcome to your first Cowork task! I'm going to create something useful for you and show you exactly how Cowork does it differently from regular AI chat.

I'll create everything in a brand new folder — I won't touch any of your existing files.

To make this personal, tell me:
1. **What's your role?** (e.g., marketing manager, consultant, founder, designer, analyst)
2. **What's one thing you wish you had more time for at work?**"

Wait for their response. If they give you lots of detail, great. If they just say their role, that's enough.

### Step 2: Create the Safe Workspace

Create a new folder called `cowork-first-task/` in the user's current working directory or a location they're comfortable with.

Inside it, create this structure:
```
cowork-first-task/
├── your-workflow-map.md
├── quick-wins.md
├── cowork-explained.md
└── what-to-try-next.md
```

Tell the user: "I'm creating a new folder called `cowork-first-task/` — this is your safe sandbox. Nothing outside this folder will be touched."

### Step 3: Build the Workflow Map

Based on the user's role, create `your-workflow-map.md`:

- Map out 5-8 typical workflows for their profession
- For each workflow: what it involves, how long it typically takes, and how Cowork could handle it
- Rate each workflow by "Cowork impact": HIGH (saves hours), MEDIUM (saves 30 min+), STARTER (good first task)
- Include specific examples, not generic descriptions

This file should feel like someone who knows their profession sat down and mapped their week. Not a generic "professionals can benefit from AI" document.

### Step 4: Create the Quick Wins File

Create `quick-wins.md`:

- 5 specific tasks the user can do RIGHT NOW in Cowork
- Each task includes: what to type, what Cowork will do, expected time savings
- Ordered from easiest to most impressive
- Each one builds on what they learned from the previous one

Make these tasks specific to their role. A marketing manager gets different quick wins than a financial analyst.

### Step 5: Write the "How This Was Different" Explanation

Create `cowork-explained.md`:

Explain in plain language what just happened and how it differs from Chat:

"Here's what just happened — and why it matters:

**What Chat would have done:**
- Given you a text response in the conversation
- You'd copy-paste it somewhere
- Each piece would be a separate chat message
- None of it would be connected or saved as files
- Tomorrow you'd need to re-explain everything

**What Cowork just did:**
- Created an organized folder on your computer
- Generated 4 connected documents that reference each other
- Saved everything as real files you can open, edit, and share
- Read the folder structure to understand your context
- Produced output tailored to YOUR role, not generic advice

**The key difference:** Chat answers questions. Cowork does work. The files in this folder are real deliverables — not conversation snippets."

### Step 6: Create the Next Steps Guide

Create `what-to-try-next.md`:

Based on their role and what they said they wish they had more time for, recommend 3 specific next steps:

1. **Immediate next skill:** The one skill from this library that would help them most right now
2. **Setup recommendation:** Point them to `cowork-setup-wizard` to personalize their experience
3. **First "real" task:** A specific task from their actual work they should try delegating to Cowork

Include the exact text they should type for each recommendation.

### Step 7: Present the Results

Show the user what was created:

"Your first Cowork task is complete! Here's what's in your `cowork-first-task/` folder:

📁 **cowork-first-task/**
├── 📄 **your-workflow-map.md** — Your professional workflows mapped with Cowork impact ratings
├── 📄 **quick-wins.md** — 5 tasks you can try right now, specific to your role
├── 📄 **cowork-explained.md** — What just happened and why it's different from Chat
└── 📄 **what-to-try-next.md** — Your personalized next 3 steps

Open any file to see what's inside. These are real files on your computer — not a chat response you need to copy-paste.

**The big takeaway:** Everything you saw here — the folder creation, the file organization, the multi-document output — that's just the beginning. When you connect your tools (Slack, Gmail, Calendar) and set up your preferences, Cowork becomes dramatically more powerful."

## Quality Checks

Before presenting:
- [ ] A new folder was created — no existing files were modified
- [ ] Workflow map is specific to their stated role (not generic)
- [ ] Quick wins include exact text to type (not vague suggestions)
- [ ] The "explained" document makes the Chat vs Cowork difference viscerally clear
- [ ] Next steps are personalized based on what they said they wish they had time for
- [ ] Total experience took under 5 minutes
- [ ] Tone is warm and encouraging, not technical

## Examples

**Example 1:** "I'm a marketing manager and I've never used Cowork before"
→ Skill creates a personalized `cowork-first-task/` folder with a workflow map for marketing roles, quick wins tailored to content and campaign work, and an explanation of exactly what Cowork did differently.

**Example 2:** "Show me what Cowork can do — I just downloaded it"
→ Skill asks one question about role, then creates 4 connected files demonstrating file creation, folder structure, and personalized context — all in a safe new folder.

**Example 3:** "I'm a consultant who's heard about Cowork but doesn't know where to start"
→ Skill generates consulting-specific workflows, 5 quick wins ranked from easiest to most impressive, and a next-steps guide pointing to the most relevant skills for their work.

## Troubleshooting

**Skill didn't activate when I described my task?**
Try invoking directly with `/safe-first-task` followed by your description.

**Output feels too generic?**
Provide more context about your role and what you wish you had more time for. The more specific you are, the more personalized the workflow map and quick wins will be.

**Folder was created in the wrong location?**
Tell Cowork: "Create the folder in [your preferred path] instead." It will recreate the structure there.

## Related Skills

See also:
- `/cowork-setup-wizard` — Set up your full Cowork preferences after this first experience
- `/what-can-cowork-do` — Discover which Cowork features match your specific role
- `/cowork-vs-chat-demo` — See a live side-by-side comparison of Chat vs Cowork on your own task
