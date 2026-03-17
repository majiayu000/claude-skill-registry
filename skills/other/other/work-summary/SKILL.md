---
name: work-summary
description: Summarize today's git commits into plain-language work updates for Slack. Translates technical changes into what colleagues understand - no coding jargon, sounds like manual work you did yourself.
---

# Work Summary for Slack

Generate a colleague-friendly summary of today's work for posting to Slack.

## When to Use

- End of day to share what you accomplished
- When asked "what did you work on today?"
- Before standup or team check-ins

## Process

### Step 1: Get Today's Commits

```bash
git log --since="midnight" --oneline --no-merges
```

Or for more detail:
```bash
git log --since="midnight" --pretty=format:"%s" --no-merges
```

### Step 2: Translate to Plain Language

**Transform technical language → colleague-friendly language:**

| Technical | Plain Language |
|-----------|----------------|
| "Refactored SKILL.md" | "Cleaned up the workflow documentation" |
| "Fixed broken references" | "Fixed some broken links between documents" |
| "Added TEMPLATE_INDEX.md" | "Created a quick-reference guide for social media templates" |
| "Committed content engine refactor" | "Reorganized our content production system" |
| "Updated NOW.md" | "Updated project status notes" |
| "Created SKILL_ARCHITECTURE_MAP.md" | "Mapped out how our content workflows connect" |
| "Fixed frontmatter" | "Fixed some document formatting issues" |
| "Extracted references to separate files" | "Organized reference materials into their own sections" |

**Rules:**
- Never mention: Claude, AI, skills, SKILL.md, git, commits, refactor, frontmatter, tokens
- Frame as manual work: "I reorganized..." not "The system was updated..."
- Use action verbs: cleaned up, organized, created, updated, fixed, mapped out
- Focus on outcomes: what's better now, not how it was done

### Step 3: Group by Theme

Cluster related changes into coherent updates:

**Example groupings:**
- Newsletter workflow improvements
- Social media template organization
- Documentation cleanup
- New guides/references created

### Step 4: Format for Slack

**Format:**
```
Here's what I worked on today:

• [Theme 1]: [1-2 sentence description]
• [Theme 2]: [1-2 sentence description]
• [Theme 3]: [1-2 sentence description]

[Optional: One sentence about what this enables or improves]
```

**Keep it:**
- 3-5 bullet points max
- Conversational, not formal
- Focused on value/outcomes
- Brief - respect people's time

## Example

**Git commits:**
```
ab604a8 Content engine refactor: architecture map, skill fixes, philosophy
b0a8751 Fix Ray Peat RAG search: use Qdrant Cloud instead of local
95d10f0 Add Frictionless Content Engine + Elijah onboarding docs
```

**Slack output:**
```
Here's what I worked on today:

• Mapped out our content production workflows - created a visual guide showing how newsletters, podcasts, and social posts connect
• Cleaned up some documentation that had broken links between sections
• Added onboarding materials for Elijah on our content system

This should make it easier to see how all our content pieces fit together.
```

## Save Summary

Save to `.claude/work-summaries/YYYY-MM-DD.md` for consolidation.

## Post to Slack

Use the Slack MCP to post to `#market-daily` or appropriate channel:

```
Post this to #market-daily
```

---

## Quick Reference

**Never say:** refactored, committed, merged, SKILL.md, frontmatter, tokens, Claude, AI, skill, git

**Always frame as:** "I worked on...", "Cleaned up...", "Created...", "Organized..."

**Tone:** Casual, helpful, like you're catching up a colleague over coffee
