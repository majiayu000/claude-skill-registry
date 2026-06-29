---
name: memory-system
description: "Sets up a file-based memory system so Cowork always knows who you are, how you work, and where your projects stand. For eliminating repetitive re-introductions at session start, when building persistent context across multiple projects, or during initial Cowork onboarding. Use when the user says \"claude doesn't remember me\", \"memory system\", \"persistent context\", \"why does it forget\", \"remember my preferences\", \"I keep re-explaining myself\", or \"how do I make Claude remember things\"."
---

# Memory System

**Your Role:** You are the person who finally explains how Cowork's memory actually works — and then sets it up so it never frustrates this user again. You are matter-of-fact and reassuring. The user is likely mildly annoyed ("I told it this last week!"). Your job is to validate that frustration, explain why it happens in one sentence, and spend the rest of the session fixing it.

**Goal:** Build a complete, working memory system using files — so every future Cowork session starts with full context about who this user is, what they're working on, and how they like to work.

## Why This Skill Exists

Cowork does not have a brain that remembers conversations. Each session starts fresh. This is not a bug — it is simply how AI assistants work — but it becomes a genuine problem for users who work on ongoing projects and have to re-explain their role, their company, and their preferences every single session.

The solution is elegantly simple: files. Cowork can read files at the start of any session. If you put your context in files, you have persistent memory. This skill builds that system in under 20 minutes.

## Instructions

### Step 1: Acknowledge and Explain

Say something like:

"You're right — Cowork doesn't have a memory that persists between sessions. Every conversation starts from zero.

But here's the fix: Cowork can read files. So instead of relying on it to 'remember' you, we build files that contain everything it needs to know. At the start of any session, you (or an automatic task) load those files, and Cowork has full context instantly.

Let's build your memory system right now. It takes about 15 minutes and you'll never re-explain yourself again."

### Step 2: Gather the Raw Information

Interview the user across four categories. Ask these questions conversationally — not as a form:

**About them:**
- Name, role, company, and industry
- How long they've been using Cowork
- The 2-3 things they use Cowork for most often

**About their work:**
- What active projects are they running right now? (Just names and one-sentence descriptions)
- What decisions have they made recently that Cowork should know about?
- Any recurring meetings, reports, or deliverables Cowork helps with?

**About their preferences:**
- How do they like outputs formatted? (Length, structure, tone)
- Anything they hate seeing in Cowork's responses?
- Any terminology, acronyms, or internal language Cowork should know?

**About their tools:**
- Which connected tools do they use most? (Calendar, Gmail, Slack, Notion, etc.)
- How do they like Cowork to interact with those tools?

### Step 3: Build the Memory Files

Create a folder: `cowork-memory/`

Inside it, create these four files:

**`about-me.md`**
```
# About Me
Name: [Name]
Role: [Role] at [Company]
Industry: [Industry]

## How I Use Cowork
[2-3 sentences on their main use cases]

## My Communication Style
[Tone preferences, format preferences, what to avoid]

## Terminology I Use
[Company name, internal acronyms, product names, anything Cowork should recognize]
```

**`active-projects.md`**
```
# Active Projects
Last updated: [Today's date]

## [Project 1 Name]
Status: [In progress / On hold / Wrapping up]
What it is: [1-2 sentences]
Recent decisions: [Anything Cowork should know]
Next steps: [What's coming]

## [Project 2 Name]
[Same format]

[One section per project they mentioned]
```

**`decisions-and-context.md`**
```
# Running Context and Decisions
Last updated: [Today's date]

## Decisions Made
[Date] — [Decision and brief rationale]
[Date] — [Decision and brief rationale]

## Things to Always Remember
[Standing instructions that apply to all work — e.g., "Always recommend checking with legal before committing to anything contractual"]

## Things Currently in Flux
[Open questions, things being decided, things that might change soon]
```

**`how-to-load-this-memory.md`**
```
# How to Load Your Memory in Any Session

At the start of any Cowork session, paste this:

---
"Before we start, please read these files to understand my context:
- cowork-memory/about-me.md
- cowork-memory/active-projects.md
- cowork-memory/decisions-and-context.md

Confirm when you've read them and we'll begin."
---

That's it. Cowork will read all three files and have full context for the session.
```

### Step 4: Explain How to Use It

Walk the user through the simple habit:

"Here's your new routine:

1. **Start every session:** Paste the loader text from `how-to-load-this-memory.md`. Takes 3 seconds.
2. **End of a project:** Open `active-projects.md` and update the status.
3. **Made a big decision:** Add it to `decisions-and-context.md` while it's fresh.

That's the whole system. You don't need to maintain it perfectly — even a half-updated file is infinitely better than no context at all."

### Step 5: Offer to Add to Cowork Preferences

"Want to take this one step further? I can help you add your core context to your Cowork preferences — that way some of this information loads automatically without you needing to paste the loader text.

The memory files handle detailed, changing context. Preferences handle the stable stuff: who you are, your tone, your format preferences. Both working together is the best setup."

If they say yes, guide them to their Cowork preferences and help them add a condensed version of `about-me.md`.

## Quality Checks

Before finishing:
- [ ] All four files are created and populated with real information (not placeholder text)
- [ ] `active-projects.md` has at least one real project from their current work
- [ ] `how-to-load-this-memory.md` contains exact copy-paste text — no editing required
- [ ] User understands the 3-step habit (start session, update after projects, log decisions)
- [ ] No technical jargon was used — no mention of "context windows" or "tokens"
- [ ] The user feels the system is manageable, not like a new chore

## Examples

**Example 1 — Frustrated user who keeps re-explaining their role:**
User types: "claude doesn't remember me, I keep re-explaining myself every session"
Cowork acknowledges the frustration, explains the file-based solution in one sentence, then interviews the user and creates all four memory files — `about-me.md`, `active-projects.md`, `decisions-and-context.md`, and `how-to-load-this-memory.md` — populated with real content.

**Example 2 — New user setting up from scratch:**
User types: "I want persistent context so cowork always knows my situation"
Cowork builds the full memory system during the session, walks through the three-step habit (load, update projects, log decisions), and optionally adds a condensed version to Cowork preferences for automatic loading.

**Example 3 — User managing multiple simultaneous projects:**
User types: "I'm running three client projects at once and cowork keeps mixing them up"
Cowork creates separate project sections in `active-projects.md` for each client, with status, recent decisions, and next steps — so each session starts with all three clearly distinguished and ready.

## Troubleshooting

**Issue: User says the memory files feel like too much work to maintain.**
Solution: Emphasize the minimum-viable approach: even `about-me.md` alone (never needs updating) is a major improvement over no memory. Only `active-projects.md` needs regular updates — suggest linking it to a habit already in place, like end-of-week review. A half-maintained system is still dramatically better than nothing.

**Issue: User isn't sure what to put in `decisions-and-context.md`.**
Solution: Start it nearly empty with one or two examples. Tell them: "Whenever you make a decision in Cowork that you don't want to re-explain next week, paste it in here. It grows naturally." Don't try to fill it perfectly on day one.

**Issue: User loads the memory files but Cowork still seems to forget things mid-session.**
Solution: This is expected — files load context at session start, but Cowork's in-session window can only hold so much. For long sessions, suggest re-pasting the loader text halfway through, or breaking the work into shorter focused sessions with a fresh load each time.

## Related Skills

See also: **cowork-health-check** — often the entry point that identifies memory setup as a Priority 1 improvement.
Related: **workflow-builder** — workflows that reference memory files run with full context automatically; build these in tandem.
See also: **first-scheduled-task** — the weekly project status scheduled task pairs perfectly with `active-projects.md` to keep memory files current without manual effort.
