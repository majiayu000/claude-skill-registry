---
name: rss-catchup
description: Fetch and summarize latest articles from RSS feeds. Creates notes with article summaries as bullet points. Use to catch up on blogs without reading everything. Triggers on "rss catchup", "blog catchup", "check feeds", "summarize articles".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch
---

Catch up on RSS feeds by auto-summarizing new articles.

## Prerequisites

Requires `feedparser`:
```bash
pip install feedparser
```

## Helper Script

Use `scripts/rss_helper.py` for fetching data:

```bash
# List recent articles from a feed
python3 scripts/rss_helper.py feed URL [limit]

# Get article content (fetches full page)
python3 scripts/rss_helper.py article URL
```

## Workflow

1. **Load configuration**
   - Read feed list from `references/feeds.json`
   - Read last run timestamp from `references/state.json`
   - If first run: go back ~3 months
   - Otherwise: only articles since last run

2. **For each enabled feed:**
   - Run: `python3 scripts/rss_helper.py feed "FEED_URL" 20`
   - Filter to articles published since last run
   - **Deduplicate against existing notes:**
     ```bash
     grep -rl "media: {article_url}" "my-vault/07 Knowledge Base/Capture/Articles/"
     ```
   - If a note with that URL exists: skip (already processed, may be missing from state)

3. **For each new article:**
   - If feed provides full content, use that
   - Otherwise, run: `python3 scripts/rss_helper.py article "ARTICLE_URL"` to fetch full text
   - Summarize the content into bullet points (3-8 based on length/density)
   - Create article note with status: `Summarized`
   - **Extract discoveries** (see below)

4. **Create discovery notes:**
   - While summarizing, identify any products, services, frameworks, tools, libraries, or technologies mentioned that might be worth exploring
   - Search my-vault to check if a note already exists for each discovery
   - For new discoveries, create a note in `my-vault/01 Inbox/`
   - Link the discovery note from the article's Related field

5. **Update state**
   - Write current timestamp to `references/state.json`
   - Report summary of what was processed

## Tagging

**IMPORTANT: Read `my-vault/09 System/Tag Index.md` before processing to verify valid tags.**

Tags MUST come from the canonical list - do not invent new tags. Common valid tags for this skill:
- `#ai` - LLMs, agents, prompting, AI tools
- `#llm` - Large Language Models, model comparisons
- `#dev-tools` - IDEs, Git tooling, developer productivity
- `#python`, `#javascript`, `#typescript` - language-specific
- `#devops`, `#api`, `#databases` - infrastructure topics
- `#atlassian`, `#jira`, `#confluence` - Atlassian products

Each feed in `references/feeds.json` has a `tags` array specifying default tags. Use these for article notes. Format: `tags: ["tag1", "tag2"]`

For discovery notes, choose tags based on what the discovery is (e.g., a Python library gets `#python`, an AI tool gets `#ai`).

## Article Note Format

Create in: `my-vault/07 Knowledge Base/Capture/Articles/[Feed Name]/[Title].md`

Sanitize filenames: remove special characters, limit length to ~80 chars.

```markdown
---
class: Article
media: https://example.com/article-url
publishDate: YYYY-MM-DD
status: Summarized
author: Author Name
reviewFrequency:
lastReviewedDate:
review:
aliases:
tags: ["tag1", "tag2"]
cssclasses:
archived:
---
Related:

## Summary

Capture the actual conclusions and insights - what would someone learn from reading this? Not topic labels or "this article discusses X" but the substance:

**Good:** "Multi-agent systems outperform single agents when context exceeds what fits in one prompt - Anthropic's research system with Opus 4 lead + Sonnet 4 subagents beat single-agent Opus 4 by 90.2%"

**Bad:** "Discusses multi-agent architectures and when to use them"

Aim for 4-8 substantive bullets that capture the key takeaways, conclusions, data points, and actionable insights.

## Discoveries

- [[Product Name]] - brief context from article
- (or "None" if nothing noteworthy)

## Why Read?

[One sentence on whether this seems worth actually reading in full]
```

## Feed Config

Edit `references/feeds.json`:
```json
{
  "feeds": [
    {
      "name": "Feed Display Name",
      "url": "https://example.com/feed",
      "folder": "Folder Name",
      "tags": ["tag1", "tag2"],
      "priority": "high",
      "enabled": true
    }
  ]
}
```

Tags should be from the canonical list in `my-vault/09 System/Tag Index.md`.

## Discovery Note Format

Create in: `my-vault/01 Inbox/[Name].md`

```markdown
---
class: Note
reviewFrequency:
lastReviewedDate:
review:
aliases:
tags: ["tag1", "tag2"]
cssclasses:
archived:
---
Up:
Related: [[Article Title]]

## What is it?

[One sentence description of the product/service/framework]

## Why look into it?

[Brief note on why it seemed interesting from the article context]

## Links

- [Official site or docs if mentioned]
```

**What counts as a discovery:**
- Products or services (SaaS tools, apps, platforms)
- Frameworks or libraries (programming, ML, etc.)
- Technologies or protocols
- Notable companies or projects
- Methodologies or techniques worth researching

**Skip creating notes for:**
- Well-known mainstream things (e.g., "Python", "AWS", "React")
- Generic concepts that don't warrant their own note
- Things already covered extensively in existing notes

## Processing Tips

- Process one feed at a time and report progress
- For long articles, focus on main arguments/takeaways
- If article content can't be fetched, summarize from title/description
- Skip articles that already exist in my-vault
- Keep summaries concise - this is for deciding what to read, not replacing reading
- When extracting discoveries, be selective - only create notes for things genuinely worth exploring
- Deduplicate by URL - some articles may appear in multiple feeds

## Path Handling

**CRITICAL - Never escape spaces with backslashes:**
- Use paths exactly as shown: `my-vault/07 Knowledge Base/...` (with literal spaces)
- The Write tool handles spaces correctly - backslash escaping creates literal `\` characters in directory names
- When using Bash commands, wrap paths in double quotes: `"my-vault/07 Knowledge Base/..."`
