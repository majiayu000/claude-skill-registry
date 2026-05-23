---
name: Translating Technical Articles
description: Translates English technical articles (engineering blogs, documentation) to Japanese while preserving layout and structure. Use when the user asks to translate an article, convert English content to Japanese, or mentions translating a URL or technical blog post.
---

# Translating Technical Articles

## Overview

This Skill translates English technical articles to Japanese Markdown while preserving:
- Heading structure and hierarchy
- Image links and URLs
- Code blocks and formatting
- List structures (numbered, bulleted)

## Translation workflow

Copy this checklist and track progress:

```
Translation Progress:
- [ ] Step 1: Fetch article content
- [ ] Step 2: Translate to Japanese
- [ ] Step 3: Save to file
- [ ] Step 4: Verify translation (no garbled text)
- [ ] Step 5: Create implementation log
```

### Step 1: Fetch article content

**Priority order for fetching**:

1. **Firecrawl MCP** (`mcp__firecrawl__firecrawl_scrape`): Most reliable
   ```
   🌟Claudeは Firecrawl MCP サーバー を唱えた！
   ```
   Use `formats: ["markdown"]` and `maxAge` for caching

2. **Brave Search MCP**: If Firecrawl unavailable

3. **WebFetch**: Last resort

### Step 2: Translate to Japanese

**Key translation principles**:

- **Preserve layout**: Keep all heading levels, lists, images, code blocks
- **Technical terms**:
  - Proper nouns: Keep original (e.g., "Claude Code", "Agent Skills")
  - Common tech terms: Translate with original in parentheses on first use
  - Industry terms: Use original if well-established
- **Natural Japanese**: Avoid literal translation, use natural expressions
- **Consistency**: Use same translation for same terms throughout

**Add metadata header**:

```markdown
# [Translated Title]

**公開日:** YYYY年MM月DD日

**原文:** [Original URL]

---

[Translated content]
```

### Step 3: Save to file

**File naming**:
- Directory: User-specified path or kebab-case title directory
- Filename: Kebab-case title + `.md`
- Example: `cc-catch-up/agent-skills/agent-skills.md`

### Step 4: Verify translation quality

**Critical verification step**:

After saving the translated file, **必ず必ず必ず最終確認**を実行すること：

1. **Read the saved file** to verify content
2. **Check for garbled text** (文字化け):
   - Japanese characters display correctly
   - No mojibake (e.g., "æ–‡å­—åŒ–ã'" instead of "文字化け")
   - Code blocks and special characters intact
3. **If garbled text found**:
   - Identify the cause (encoding issue, incorrect character conversion)
   - Fix the garbled sections immediately
   - Save the corrected version
   - Re-verify until no issues remain
4. **If no issues found**:
   - Confirm completion to user
   - Proceed to Step 5

**Important**: Do not skip this verification. Garbled text makes the translation unusable.

### Step 5: Create implementation log

Save log to `_docs/templates/YYYY-MM-DD_translated-title.md`:

```markdown
# [Feature Name]

- **日付**: YYYY-MM-DD HH:MM:SS (from `date "+%Y-%m-%d %H:%M:%S"`)
- **概要**: Translation purpose and background
- **実装内容**: MCP server used, translation approach
- **設計意図**: Why preserve layout, how handle technical terms
- **翻訳のポイント**: Key translation decisions
- **副作用**: Any concerns (e.g., external image dependencies)
- **関連ファイル**: Path to translated file, original URL
```

## Quality checklist

Before completion, verify:

- [ ] Heading structure matches original
- [ ] Image links and URLs preserved
- [ ] Code blocks properly formatted
- [ ] Technical terms consistent
- [ ] Natural Japanese expressions
- [ ] No garbled text (文字化けなし)
- [ ] Metadata header included
- [ ] Implementation log created

## Example translation

**Input**: "Agent Skills extend Claude's capabilities..."

**Output**: "Agent Skillsは、Claudeの機能を拡張し..."

Note: "Agent Skills" kept as original (proper noun), natural Japanese structure.
