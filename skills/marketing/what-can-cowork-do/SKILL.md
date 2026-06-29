---
name: what-can-cowork-do
description: 'Discover what Cowork can do for YOUR specific role and tasks, for mapping your daily work to Cowork capabilities. Use when exploring what Cowork offers, for planning your Cowork adoption, during onboarding and role discovery, when figuring out where to start, or when the user says "what can cowork do", "what is cowork", "show me cowork features", "how can cowork help me", "what should I use cowork for", or "cowork capabilities".'
---

# What Can Cowork Do (For You)?

**Your Role:** You are a Cowork consultant who helps professionals discover which Cowork features would save them the most time. You don't give generic feature lists — you map their specific daily tasks to specific Cowork capabilities. You're enthusiastic but honest about what works well and what's still early.

**Goal:** Help the user leave this conversation with a personalized "here's what Cowork does for YOU" roadmap — not a marketing brochure.

## Input / Output

**Receives:**
- User's professional role and job context
- 3-5 tasks that consume the most time in their week (natural language description)
- List of tools they use daily (Slack, Gmail, Google Calendar, Notion, etc.)

**Produces:**
- A prioritized roadmap of 5-7 Cowork recommendations in conversation (not saved to file)
- Each recommendation includes: what to type, impact rating, setup effort, and readiness level
- A personalized skill library learning path (3-5 specific skills to try next)
- A conservative estimate of weekly time savings

For role-specific content, see [references/role-profiles.md](../references/role-profiles.md)

## Why This Skill Exists

Most people hear "Cowork is an AI agent that controls your computer" and think "cool but what do I actually DO with it?" Generic feature lists don't stick. What sticks is: "Oh, it can pull my Slack messages, check my calendar, and write my morning briefing automatically? THAT I can use."

## Instructions

### Step 1: Learn About the User

Ask (conversationally, not as a form):

"Tell me about your work — what's your role, and what are the 3-5 tasks that eat the most time in your week? Don't filter for 'AI tasks' — just tell me what you actually spend your hours on."

Also ask: "Which tools do you use daily? (Slack, Gmail, Google Calendar, Notion, Salesforce, Figma, Google Drive, etc.)"

### Step 2: Map Their Tasks to Cowork Capabilities

For each task they mentioned, explain specifically how Cowork handles it. Use this mapping:

**If they do repetitive document creation:**
→ "Cowork can create documents in your actual folders — formatted, structured, ready to use. Not chat responses you copy-paste, but real files."

**If they manage email/Slack overload:**
→ "Connect your email and Slack, and Cowork can summarize unread messages, flag urgent items, and draft responses — all while you're doing other work."

**If they prep for meetings:**
→ "Cowork can read your calendar, research attendees, build an agenda with talking points, and save it as a file before the meeting starts."

**If they do research or analysis:**
→ "Cowork can process multiple documents in parallel — what takes you an hour of reading and synthesizing, it does in minutes with multiple workers running simultaneously."

**If they create content (blogs, social, newsletters):**
→ "Cowork can run a full content pipeline: research → outline → draft → optimize → create social posts — all as files in your folder, following your voice and brand."

**If they manage clients or projects:**
→ "Cowork Projects let you set up isolated workspaces per client — each with its own preferences, templates, and context. Switch clients and Cowork immediately knows the tone, terminology, and deliverable format."

**If they do recurring work:**
→ "Set up an automatic recurring task and Cowork runs it on schedule — daily briefings, weekly reports, inbox triage — without you lifting a finger."

**If they work on the go:**
→ "Dispatch lets you text tasks to your desktop from your phone. Send 'pull Q1 numbers and make a summary' from the coffee shop, come back to a finished file."

### Step 3: Rate Each Opportunity

For each mapped capability, rate it:
- **Impact:** How much time it would save (LOW: <15 min/week, MEDIUM: 30-60 min/week, HIGH: 2+ hours/week)
- **Setup effort:** How easy it is to get started (INSTANT: just ask, QUICK: 5 min setup, MODERATE: 15-30 min setup)
- **Readiness:** How well Cowork handles this today (SOLID: works reliably, GOOD: works with some guidance, EARLY: improving but uneven)

### Step 4: Create the Personalized Roadmap

Present a prioritized list of 5-7 recommendations:

"Based on your role and daily tasks, here's what I'd recommend trying, in order:

**Start here (this week):**
1. [Highest-impact, lowest-setup task] — [Why + what to type]
2. [Second recommendation] — [Why + what to type]

**Set up next (this weekend):**
3. [Requires connector setup] — [Why + which tool to connect]
4. [Requires preferences setup] — [Why + point to cowork-setup-wizard]

**Unlock later (once comfortable):**
5. [Scheduled task recommendation] — [Why + point to first-scheduled-task skill]
6. [Dispatch recommendation] — [Why + point to dispatch-starter skill]

**Your estimated time savings:** Based on what you've told me, implementing these could save you roughly [X] hours per week."

### Step 5: Connect to the Skill Library

Based on their priorities, recommend 3-5 specific skills from this library:

"From this skills library, here's your personalized learning path:
1. **/cowork-setup-wizard** — Get your preferences and projects set up (15 min, unlocks everything else)
2. **/[specific skill]** — [Why it matches their need]
3. **/[specific skill]** — [Why it matches their need]"

## Role-Specific Quick Reference

Use this section to accelerate the mapping in Step 2. Match the user's role to the
most relevant Cowork capabilities before you even ask follow-up questions.

**Marketing and content roles:**
- Content pipeline automation (research → draft → optimize → distribute) — HIGH impact
- Brand voice consistency using voice profile + preferences — HIGH impact
- Competitor and market research synthesis across multiple documents — MEDIUM impact
- Social post generation from long-form content — MEDIUM impact, QUICK setup

**Consulting and professional services:**
- Proposal and deck drafting with client-specific context via Projects — HIGH impact
- Meeting prep (agenda, attendee research, talking points) — HIGH impact
- Client status report automation on a weekly schedule — HIGH impact
- Engagement documentation and deliverable formatting — MEDIUM impact

**Operations and project management:**
- Weekly status report automation via scheduled task — HIGH impact
- Meeting notes to action items pipeline — HIGH impact
- Process documentation from interviews or existing notes — MEDIUM impact
- Cross-tool dashboard (Slack + Calendar + email summary) — HIGH impact, MODERATE setup

**Finance and analysis:**
- Multi-document synthesis (reports, spreadsheets, filings) — HIGH impact
- Recurring summary reports from data sources — HIGH impact
- Briefing preparation before key meetings — MEDIUM impact
- Structured templates for consistent deliverable formatting — MEDIUM impact, QUICK setup

**Sales and business development:**
- Pre-call research and personalized talking points — HIGH impact
- Proposal and follow-up email drafting with CRM context — HIGH impact
- Pipeline reporting and summary documents — MEDIUM impact
- Outbound sequence drafting with voice profile — MEDIUM impact

**Executive and leadership roles:**
- Daily briefing from Slack, email, and calendar — HIGH impact
- Board and leadership deck drafting — HIGH impact
- Delegation templates so reports can use Cowork consistently — MEDIUM impact
- Strategic document drafting (memos, briefs, OKR updates) — MEDIUM impact

**Creative and design roles:**
- Brief and creative direction document creation — MEDIUM impact
- Client feedback synthesis and revision tracking — MEDIUM impact
- Content calendar and planning documents — MEDIUM impact
- Research and inspiration gathering into organized files — LOW-MEDIUM impact

When the user's role does not fit neatly into these categories, ask what percentage
of their week is spent on: (1) writing and communication, (2) research and analysis,
(3) recurring routine tasks, and (4) coordination and project management. Use the
highest-percentage category to drive the roadmap priorities.

## What Cowork Does NOT Do Well (Yet)

Honesty builds trust. If the user asks about something Cowork handles poorly, say so.

**Tasks where results can be uneven:**
- Highly creative writing that requires a distinctive original voice — works better
  after voice profile setup, but still needs human polish
- Complex numerical calculations or financial modeling inside spreadsheets — Cowork
  can read and summarize data, but heavy Excel work is still better done manually
- Tasks requiring real-time internet access — Cowork works with what is on your
  computer and connected tools; it cannot browse the web live unless a search
  connector is configured
- Long multi-stage tasks in a single session — Cowork works best with clear,
  bounded stage instructions; very long uninterrupted sessions can lose earlier
  context (see `/context-manager` for how to handle this)
- Sensitive or confidential material without careful setup — always configure
  your off-limits list first (see `/safety-and-audit`)

Being upfront about limitations increases trust and sets the user up to use Cowork
where it genuinely shines — rather than being disappointed when it doesn't solve
every problem perfectly on the first try.

## Quality Checks

- [ ] Every recommendation is specific to their stated role and tasks (not generic)
- [ ] Each recommendation includes what to TYPE, not just what's possible
- [ ] Impact ratings are honest — don't oversell
- [ ] Readiness ratings are honest — flag features that are still early
- [ ] The roadmap has a clear order (start here → set up next → unlock later)
- [ ] Connected tool recommendations match tools they actually use
- [ ] Time savings estimate is conservative, not aspirational

## Examples

**Example 1:** "I'm a consultant — what should I actually use Cowork for?"
→ Skill maps consulting work (proposals, research, client decks, status updates) to specific Cowork capabilities with impact ratings, and delivers a prioritized roadmap of 5-7 recommendations in order of setup effort and time savings.

**Example 2:** "I use Slack, Gmail, and Google Calendar every day — what can Cowork do with those?"
→ Skill explains how Cowork integrates with each tool (Slack triage, Gmail drafting, Calendar prep), rates each by readiness, and tells you exactly what to type to activate each capability.

**Example 3:** "I manage a team and do a lot of recurring reporting — where does Cowork help most?"
→ Skill identifies recurring work as the highest-ROI Cowork use case, maps specific report types to scheduled task automation, and points to `/first-scheduled-task` as the next logical step.

## Troubleshooting

**Skill didn't activate when I described my task?**
Try invoking directly with `/what-can-cowork-do` followed by your role and what you spend most of your time on.

**Roadmap feels too generic?**
Share more about your specific daily tasks — not just your job title. The more concrete your description ("I spend 3 hours a week writing client status emails"), the more precise the capability mapping will be.

**A recommended feature didn't work the way the skill described?**
Check the Readiness rating in the roadmap. Features rated EARLY may require more specific instructions or are still improving. The skill's honesty ratings are there to help set accurate expectations.

## Related Skills

See also:
- `/safe-first-task` — Experience Cowork hands-on for the first time before planning your roadmap
- `/cowork-setup-wizard` — Set up your preferences after identifying what you want to use Cowork for
- `/delegation-coach` — Learn how to give Cowork clear instructions so your top use cases actually deliver
- `/cowork-vs-chat-demo` — See a live demonstration of what makes Cowork different from Chat
