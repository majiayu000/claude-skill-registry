---
name: kai-brief
description: Create a structured content brief using the Kai CMO Harness brief schema. Selects persona, defines angle, sets quality targets. Use when "create a brief", "content brief", "plan this content", "brief for [topic]", "what persona should I use", or before any content creation to define the strategy. Outputs a brief that /kai-write and /kai-email-system consume.
---

Create a content brief using the Kai CMO Harness schema. Every piece of content starts with a brief.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Process

### 1. Gather Inputs

Read from `MARKETING.md`. Only ask about things not covered there:

- **What are we writing?** (blog, email, LinkedIn, ad, etc.)
- **What's the topic/keyword?**
- **Who's it for?** (suggest a persona from the list below)
- **What's the angle?** Not just the topic — the specific frame. "AI for law firms" is a topic. "Why law firms lose 40% of leads after 5pm" is an angle.
- **What should the reader do?** (CTA)
- **Any proof/data we can use?**

### 2. Select Persona

Read `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md` for the full list. Quick reference:

| Persona | Core Hook | Best For |
|---------|-----------|----------|
| Competent Cog | "The system treats you like a child" | B2B SaaS, enterprise |
| Shock Absorber | "Accountability without authority" | Middle management |
| Ghosted Applicant | "The game is rigged" | Job seekers, HR tech |
| Subscription Serf | "They bet you won't fight back" | Consumer SaaS |
| System Manager | "No village, only vendors" | Parents, household managers |
| Admin Martyr | "Death by a thousand tasks" | Admin/ops roles |
| Obsolescence Anxious | "Working hard isn't the variable" | Career-concerned professionals |
| Credibility Fighter | "You're not crazy" | Experts fighting misinformation |

Load the full persona file before writing the brief. It contains language patterns, pain points, and hooks that shape the angle.

### 3. Output Brief

Follow the schema from `E:\Dev2\kai-cmo-harness-work\harness\brief-schema.md`:

```json
{
  "target_site": "[site]",
  "target_keyword": "[primary keyword]",
  "secondary_keywords": ["2-3 terms"],
  "format": "[blog|linkedin|email|ad|press]",
  "persona": "[archetype name]",
  "angle": "[specific frame]",
  "hook_options": ["Hook 1", "Hook 2", "Hook 3"],
  "audience_pain": "[single biggest frustration]",
  "proof_available": "[data, stories, examples]",
  "cta": "[desired action]",
  "word_count_target": 0,
  "publish_date": "YYYY-MM-DD"
}
```

### 4. Validate

Before passing the brief to `/kai-write`:
- `hook_options` has exactly 3 variants
- `angle` is differentiated from `target_keyword` (not a restatement)
- `proof_available` references actual data or a named example (not vague)
