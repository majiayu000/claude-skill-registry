---
name: plan-rfc
description: Plan and draft RFCs (Request for Comments) for major features or architectural changes. Use when user wants to propose a significant feature, system redesign, or cross-cutting change that requires stakeholder alignment before implementation. Triggers on phrases like "RFC", "proposal", "major feature", "architectural change", "need buy-in", or when user describes a feature too large for a single ticket. Guides through structured questioning to produce a complete RFC draft in Notion.
---

# RFC Planning Skill

Guide the user through planning an RFC by exploring the codebase, asking clarifying questions for each section, and drafting a complete RFC document to Notion.

## Input

The user provides a freeform feature description. Example:

> I've been building AlgoJuke, an AI-powered playlist generator backed by the user's Tidal music library and Tidal search, and an ingestion pipeline which interprets lyrics for the tracks in the user's library so it can make recommendations which fit a theme / mood.
>
> I'd like to turn it into a personal radio station that interleaves your favourite music (+ recommendations based on your mood and natural language input) with excerpts / summaries from articles that are interesting to you, that you've bookmarked via the Readwise API with voiceover using ElevenLabs.

## Workflow

### Step 1: Enter Plan Mode

Call `EnterPlanMode` to begin planning. All exploration and questioning happens in plan mode.

### Step 2: Explore Context

Before asking questions, silently gather context:

1. **Read existing specs**: Search `specs/*/spec.md` for related features
2. **Explore architecture**: Identify key services, data flows, integrations
3. **Check prior art**: Look for similar patterns in the codebase
4. **Note dependencies**: What existing systems would this touch?

Do NOT output exploration results verbatim. Synthesize into understanding.

### Step 3: Section-by-Section Questioning

For each RFC section, ask **up to 5 clarifying questions** based on:

- Gaps in the user's description
- Ambiguities that affect scope
- Technical constraints discovered during exploration
- Stakeholder concerns to anticipate

Present questions as a numbered list. User can answer in shorthand.

#### Section Order

Work through sections in this order (skip none):

1. **Summary** — Confirm the one-paragraph pitch
2. **Motivation** — Why now? What's the business driver?
3. **Goals and Non-Goals** — Scope boundaries, success criteria
4. **User's Explanation** — How users experience this
5. **Engineer's Explanation** — Technical approach, system interactions
6. **Drawbacks** — What could go wrong? What are we trading off?
7. **Rationale and Alternatives** — Why this approach over others?
8. **Cost and Operations** — Infrastructure, LLM costs, operational burden
9. **Prior Art** — Similar systems, lessons learned
10. **Unresolved Questions** — What needs resolution during RFC review?
11. **Future Possibilities** — Natural extensions, long-term vision

#### Questioning Pattern

For each section:

```markdown
## {Section Name}

Based on your description and what I found in the codebase:

- {Relevant context from exploration}

Questions:

1. {Question addressing a gap}
2. {Question about scope/boundary}
3. {Question about technical constraint}
4. {Question anticipating stakeholder concern}
5. {Question about success/failure criteria}

Answer in shorthand (e.g., "1: yes, 2: via Readwise API, 3: out of scope").
```

After user answers, summarize what will go in that section. Confirm before moving on.

### Step 4: Build Plan Document

As sections are confirmed, accumulate them in the plan file (NOT the final RFC yet).

Structure:

```
# RFC Plan: {Title}

## Status
- [x] Summary confirmed
- [x] Motivation confirmed
- [ ] Goals and Non-Goals — in progress
- [ ] ...

## Summary
{Confirmed content}

## Motivation
{Confirmed content}

...
```

### Step 5: Exit Plan Mode

When all sections are confirmed, call `ExitPlanMode` with the complete plan.

Present a final summary:

- RFC title
- Key decisions made
- Sections completed
- Ready to write to Notion

### Step 6: Write to Notion (After Acceptance)

On plan acceptance, create the RFC in Notion:

```
mcp__notion__create_page with:
- database_id: 2e7258b8-ba0c-80d1-a580-cbab6bca3ddd
- properties:
  - Title: {RFC title}
  - Status: "Draft"
  - Created: {ISO date}
- content: {Full RFC markdown}
```

Output the Notion URL for the user to share with stakeholders.

### Step 7: Suggest Next Steps

After RFC creation:

```
RFC created: {Notion URL}

Next steps:
1. Share with stakeholders for review
2. Address comments in Notion
3. Once approved, run `/breakdown-rfc {notion-url}` to create tickets
```

## RFC Template

The final RFC should follow this structure:

```markdown
# RFC: {Title}

## 🗒️ Summary

{One paragraph explanation}

## 💪 Motivation

{Why are we doing this? Use cases? Expected outcome?}

## 🎯 Goals and Non-Goals

**Goals:**

- {Goal 1}
- {Goal 2}

**Non-Goals:**

- {Explicitly out of scope}

**Success Criteria:**

- {Measurable outcome}

## 🧑‍🎤 User's Explanation

{Explain as if teaching a user. New concepts, UX, impact on existing features.}

## 🧑‍💻 Engineer's Explanation

{Technical design. System interactions. Corner cases with examples.}

## ⚠️ Drawbacks

{Why should we NOT do this? Tradeoffs? New challenges?}

## 🤔 Rationale and Alternatives

{Why this design? Alternatives considered? Impact of not doing this?}

## 💸 Cost and Operations

{Infrastructure costs, LLM call estimates, operational complexity, deployment targets.}

## ⚛️ Prior Art

{Similar systems, lessons learned, good and bad examples.}

## ❓ Unresolved Questions

{What to resolve during RFC review? Out of scope follow-ups?}

## 🚀 Future Possibilities

{Natural extensions, long-term vision, related ideas for later.}
```

## Question Bank by Section

Reference questions to draw from (select most relevant, don't ask all):

### Summary

- Can you distill this to one sentence: "We will {action} so that {outcome}"?
- What's the elevator pitch for stakeholders who have 30 seconds?
- Is there a working title that captures the essence?

### Motivation

- What's the business driver? Revenue, retention, competitive pressure?
- What user pain point does this address?
- Why now vs. 6 months from now?
- What happens if we don't do this?
- Is there a specific user request or feedback driving this?

### Goals and Non-Goals

- What's the minimum viable version of this feature?
- What should we explicitly NOT build in v1?
- How will we measure success? (metrics, user feedback, etc.)
- What's the failure mode we're most worried about?
- Are there phasing considerations (v1, v2, future)?

### User's Explanation

- How does a user discover this feature?
- What's the primary interaction flow?
- How does this change existing workflows?
- Are there new concepts users need to learn?
- What's the "aha moment" for users?

### Engineer's Explanation

- What existing services/components does this touch?
- What new services or data stores are needed?
- How does data flow through the system?
- What are the critical integration points?
- What's the most technically risky part?

### Drawbacks

- What's the biggest technical risk?
- What user experience tradeoffs are we making?
- What maintenance burden does this add?
- Could this break existing functionality?
- What's the worst-case failure scenario?

### Rationale and Alternatives

- What other approaches did you consider?
- Why is this approach better than {alternative}?
- Is there an off-the-shelf solution we're rejecting?
- What would a simpler version look like?
- What would we do with 10x the resources?

### Cost and Operations

- What new infrastructure is required?
- Are there new vendor dependencies?
- What's the estimated LLM cost per user/query?
- How does this affect our deployment targets (BYOC, etc.)?
- What monitoring/alerting do we need?

### Prior Art

- Are there similar features in competing products?
- Have we built something similar before?
- Are there open-source implementations to learn from?
- What industry patterns apply here?
- What cautionary tales should we heed?

### Unresolved Questions

- What technical spikes are needed before committing?
- What stakeholder input is still needed?
- Are there security/compliance reviews required?
- What's blocked on external dependencies?
- What decisions can be deferred to implementation?

### Future Possibilities

- What's the obvious v2 of this feature?
- What adjacent features does this enable?
- How does this fit the product roadmap?
- What would we build if this succeeds wildly?
- Are there platform/API implications?

## Notes

- Stay in plan mode throughout questioning — no file writes until acceptance
- Questions should build on previous answers — don't ask in isolation
- If user seems fatigued, offer to batch remaining sections with reasonable defaults
- Codebase exploration informs questions but isn't shared verbatim
- RFC quality depends on question quality — invest in understanding the feature
