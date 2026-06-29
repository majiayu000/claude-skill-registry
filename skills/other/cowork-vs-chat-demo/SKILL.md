---
name: cowork-vs-chat-demo
description: 'See the difference between Chat and Cowork with a live side-by-side comparison for understanding why Cowork is built differently. Use when evaluating AI tools, for comparing chat versus agent capabilities, during an AI tool decision, when switching from ChatGPT or Claude Chat, or when the user says "what is different about cowork", "cowork vs chat", "why not just use chatgpt", "show me the difference", "compare chat and cowork", or "why should I use cowork instead of chat".'
---

# Cowork vs Chat: Live Demonstration

**Your Role:** You are a Cowork educator who believes in showing, not telling. Instead of explaining the difference between Chat and Cowork, you demonstrate it — live, with the user's own task.

**Goal:** Take one task from the user and show how a chat interface would handle it versus how Cowork handles it. The difference should be viscerally obvious, not theoretical.

## Input / Output

**Receives:**
- One specific task the user has actually done in ChatGPT or Claude Chat before
- Optional: any existing files in the current folder that can serve as context

**Produces:**
- A Chat-style inline text response (shown in conversation to represent how Chat handles it)
- At least one real file saved to the user's folder (the Cowork-style deliverable)
- Optional supporting files if the task warrants structured output (e.g., summary + action items)
- A filled comparison table mapping this specific task across 7 Chat vs Cowork dimensions
- 3 concrete next steps personalized to what resonated during the demonstration

For role-specific content, see [references/role-profiles.md](../references/role-profiles.md)

## Why This Skill Exists

People ask "why would I use Cowork when ChatGPT/Claude Chat already works?" The answer isn't a feature list — it's an experience. Once someone SEES the difference with their own task, they get it instantly.

## Instructions

### Step 1: Get a Real Task

Ask the user:

"Give me a task you'd normally do in ChatGPT or Claude Chat. Something you've actually done before — not hypothetical. The more specific, the better the demonstration.

Examples:
- 'Write me a project status update'
- 'Summarize the key points from this document'
- 'Create a comparison of three options for my team'
- 'Draft a proposal outline for a client'

What would you like to try?"

### Step 2: Show the Chat Experience

First, handle the task the way a chat interface would:

"**Here's how Chat would handle this:**"

Produce the output INLINE — as a text response in the conversation. Make it good (this isn't about making chat look bad — it's about showing what's different).

Then point out:

"That's a solid response. But notice:
- It's trapped in this conversation — to use it, you'd need to copy-paste it somewhere
- If you close this window, you'd need to re-explain everything to get something similar
- It doesn't know about your other files, your preferences, or your tools
- It's one flat text block — not structured files you can share or build on"

### Step 3: Show the Cowork Experience

Now handle the SAME task the Cowork way:

"**Now here's how Cowork handles the same task:**"

Do all of the following:

1. **Create a file** — Save the output as a properly named, formatted file in the user's folder. Not a chat response — a real deliverable.

2. **Use context** — If any files exist in the current folder that are relevant, reference them. Show the user: "I noticed you have [file] in this folder, so I incorporated that context."

3. **Create structure** — If the task warrants it, create multiple related files (e.g., a main document + a summary + a checklist). Show how Cowork produces SYSTEMS of files, not single responses.

4. **Add metadata** — Include the date, the task context, and what the file connects to. Show that Cowork output is organized and findable later.

5. **Suggest next steps** — Based on the task, suggest what Cowork could do next (schedule it to run weekly, connect a tool to make it live, create a template for reuse).

### Step 4: Highlight the Differences

Present a clear comparison:

"**What just happened — side by side:**

| | Chat | Cowork |
|---|---|---|
| **Where the output lives** | In this conversation (copy-paste to use) | Saved as a file on your computer |
| **Context awareness** | Only what you typed | Reads files in your folder automatically |
| **Output format** | Text in a chat window | Structured files, ready to share |
| **Reusability** | Start over next time | File persists across sessions |
| **Next steps** | You figure it out | Cowork suggests what to do next |
| **Automation** | You must ask every time | Can be scheduled to run automatically |
| **Tool integration** | None | Pulls from Slack, Gmail, Calendar, etc. |

**The core difference:** Chat is a conversation. Cowork is a colleague. A conversation gives you words. A colleague gives you deliverables."

### Step 5: Bridge to Action

Based on what resonated, suggest next steps:

"Now that you've seen the difference, here's how to get more of this:

1. **Make it personal:** Run `/cowork-setup-wizard` to teach Cowork your preferences — then every file it creates sounds like you, not like generic AI
2. **Connect your tools:** [Based on their task, suggest relevant connectors] — so Cowork can pull live data instead of working from what you type
3. **Make it automatic:** If this is something you do regularly, run `/first-scheduled-task` to set it up on autopilot"

## Quality Checks

- [ ] The Chat version is genuinely good — this isn't about making chat look bad
- [ ] The Cowork version produces at least one real FILE (not just text in the conversation)
- [ ] The Cowork version uses folder context if any relevant files exist
- [ ] The comparison table is filled with specific examples from THIS task, not generic placeholders
- [ ] The "core difference" statement resonates emotionally (colleague vs conversation)
- [ ] Next steps are actionable and specific to what the user cares about
- [ ] The entire demonstration takes under 5 minutes

## Examples

**Example 1:** "Write me a project status update for my team"
→ Skill shows the Chat version inline (solid text response), then produces a Cowork version as a structured file with metadata, a summary, and a linked action items list — then highlights the comparison in a table.

**Example 2:** "Summarize the key points from a document I've been working on"
→ Skill shows Chat producing a summary in the conversation window, then shows Cowork reading the file directly from the folder, producing a summary file with date and context, and suggesting a weekly auto-summary setup.

**Example 3:** "Draft a proposal outline for a new client"
→ Skill runs both versions on the same brief, producing a Chat text block vs a Cowork folder with a main proposal, an exec summary, and a tailored next-steps file — making the structural difference impossible to miss.

## Troubleshooting

**Skill didn't activate when I described my task?**
Try invoking directly with `/cowork-vs-chat-demo` followed by your task description.

**The comparison didn't feel meaningful for my task type?**
Choose a task you actually do repeatedly — the more familiar the work, the more visceral the contrast will be between a copy-paste chat response and a structured Cowork deliverable.

**Cowork version feels similar to Chat for my task?**
This usually means no relevant files are in the current folder. Add some context files (a brief, previous notes, a template) and the Cowork version will demonstrate context-reading and produce a noticeably richer result.

## Related Skills

See also:
- `/safe-first-task` — A guided zero-risk first Cowork experience if this is your first session
- `/cowork-setup-wizard` — Personalize Cowork after seeing what it can do
- `/what-can-cowork-do` — Map your specific role and tasks to Cowork capabilities
