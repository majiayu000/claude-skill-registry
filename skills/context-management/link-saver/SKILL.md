---
name: link-saver
description: Fetch a URL, summarize it, and save it to memory for later retrieval. Use when the user drops a link and wants it remembered, or asks to "save this link".
homepage: https://github.com/broedkrummen/link-saver
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["mkdir","cat"]}}}
---

# Link Saver

Quickly save any URL to your memory with a summary — perfect for links you drop during conversation.

## When to Use

- User drops a link and says "remember this" or "save this link"
- User asks "save this for later" with a URL
- You want to store an interesting article, doc, or resource for future reference

## How It Works

1. **Fetch** the URL using `web_fetch`
2. **Summarize** the content (or just grab title + excerpt)
3. **Save** to `memory/links/YYYY-MM-DD.md` in Markdown format

## Usage

### Save a link

When user says something like:
- "Save this: https://example.com"
- "Remember this link: ..."
- "Link: https://..."

Do:

```bash
# 1. Fetch the URL
web_fetch url="https://example.com" maxChars=3000

# 2. Extract title + summary
# (manual - read the fetched content)

# 3. Save to memory/links/YYYY-MM-DD.md
# Format:
# ## [Page Title](URL)
# 
# **Saved:** YYYY-MM-DD HH:MM
# **Summary:** 1-2 sentence summary
# **Tags:** #link #topic
```

### Format for memory/links/

```markdown
## [Article: How to Build AI Agents](https://example.com/article)

**Saved:** 2026-02-23 19:45
**Summary:** A guide to building autonomous AI agents with memory, tools, and multi-agent orchestration.
**Tags:** #link #ai #agents

---
```

## File Location

Saved links go to:

```
~/.openclaw/workspace/memory/links/YYYY-MM-DD.md
```

Create the `links` directory if it doesn't exist:

```bash ~/.openclaw/
mkdir -pworkspace/memory/links
```

## Retrieval

To find saved links later:

- Search `memory/links/` directly
- Use `memory_search` with keywords from the title or summary
- Ask "what links did we save about X?"

## Notes

- Only save links when user explicitly asks ("save this", "remember this link", etc.)
- Don't save every URL automatically — that's noise
- Keep summaries brief (1-2 sentences)
- Add relevant tags for better searchability
