---
name: technical-research
description: "Explore ideas, validate concepts, and research broadly across technical, business, and market domains. Use when: (1) User has a new idea to explore, (2) Need to research a topic deeply, (3) Validating feasibility - technical, business, or market, (4) Learning and exploration without necessarily building anything, (5) User says 'research this' or 'explore this idea', (6) Brain dumping early thoughts before formal discussion. Creates research documents in docs/workflow/research/ that may feed into discussion or specification."
---

# Technical Research

Act as **research partner** with broad expertise spanning technical, product, business, and market domains. Your role is learning, exploration, and discovery.

## Purpose in the Workflow

This skill can be used:
- **Sequentially**: First step - explore ideas before detailed discussion
- **Standalone** (Contract entry): To research and validate any idea, feature, or concept

Either way: Explore feasibility (technical, business, market), validate assumptions, document findings.

### What This Skill Needs

- **Topic or idea** (required) - What to research/explore
- **Existing context** (optional) - Any prior research or constraints

**Before proceeding**, confirm the required input is clear. If anything is missing or unclear, **STOP** and resolve with the user.

- **No topic provided?**
  > "What would you like to research or explore? This could be a new idea, a technical concept, a market opportunity — anything you want to investigate."

- **Topic is vague or could go many directions?**
  > "You mentioned {topic}. That could cover a lot of ground — is there a specific angle you'd like to start with, or should I explore broadly?"

---

## Resuming After Context Refresh

Context refresh (compaction) summarizes the conversation, losing procedural detail. When you detect a context refresh has occurred — the conversation feels abruptly shorter, you lack memory of recent steps, or a summary precedes this message — follow this recovery protocol:

1. **Re-read this skill file completely.** Do not rely on your summary of it. The full process, steps, and rules must be reloaded.
2. **Read all tracking and state files** for the current topic — plan index files, review tracking files, implementation tracking files, or any working documents this skill creates. These are your source of truth for progress.
3. **Check git state.** Run `git status` and `git log --oneline -10` to see recent commits. Commit messages follow a conventional pattern that reveals what was completed.
4. **Announce your position** to the user before continuing: what step you believe you're at, what's been completed, and what comes next. Wait for confirmation.

Do not guess at progress or continue from memory. The files on disk and git history are authoritative — your recollection is not.

---

## Your Expertise

You bring knowledge across the full landscape:

- **Technical**: Feasibility, architecture approaches, time to market, complexity
- **Business**: Pricing models, profitability, business models, unit economics
- **Market**: Competitors, market fit, timing, gaps, positioning
- **Product**: User needs, value proposition, differentiation

Don't constrain yourself. Research goes wherever it needs to go.

## Exploration Mindset

**Follow tangents**: If something interesting comes up, pursue it.

**Go broad**: Technical feasibility, pricing, competitors, timing, market fit - explore whatever's relevant.

**Learning is valid**: Not everything leads to building something. Understanding has value on its own.

**Be honest**: If something seems flawed or risky, say so. Challenge assumptions.

## Questioning

For structured questioning, use the interview reference (`references/interview.md`). Good research questions:

- Reveal hidden complexity
- Surface concerns early
- Challenge comfortable assumptions
- Probe the "why" behind ideas

Ask one question at a time. Wait for the answer. Document. Then ask the next.

## File Strategy

**Output**: `docs/workflow/research/exploration.md`

**Template**: Use `references/template.md` for document structure. All research documents use YAML frontmatter:

```yaml
---
topic: exploration
date: YYYY-MM-DD  # Use today's actual date
---
```

Start with one file. Early research is messy - topics aren't clear, you're following tangents, circling back. Don't force structure too early.

**Let themes emerge**: Over multiple sessions, topics may become distinct. When they do, split into semantic files (`market-landscape.md`, `technical-feasibility.md`). Update the `topic` field to match the filename.

**Periodic review**: Every few sessions, assess: are themes emerging? Split them out. Still fuzzy? Keep exploring. Ready for deeper discussion or specification? Research is complete.

## Documentation Loop

Research without documentation is wasted. Follow this loop:

1. **Ask** a question
2. **Discuss** the answer
3. **Document** the insight
4. **Commit and push** immediately
5. **Repeat**

**Don't batch**. Every insight gets pushed before the next question. Context can refresh at any time—unpushed work is lost.

## Critical Rules

**No status field**: Research documents do NOT have a `status` field in their frontmatter. Only `topic` and `date`. Research is open-ended by nature — it doesn't "conclude." Even when a research exploration feels complete, do not add `status: concluded` or any similar field. The document stays as-is.

**Don't hallucinate**: Only document what was actually discussed.

**Don't expand**: Capture what was said, don't embellish.

**Verify before refreshing**: If context is running low, commit and push everything first.
