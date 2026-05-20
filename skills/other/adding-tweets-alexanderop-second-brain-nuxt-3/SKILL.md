---
name: adding-tweets
description: Add tweets to the Second Brain. Use when the user provides a Twitter/X URL and pasted tweet content, asking to "add a tweet", "save this tweet", or "capture this tweet".
allowed-tools: Read, Write, Bash, Glob, Grep, Task, TaskOutput, WebSearch, AskUserQuestion
---

# Adding Tweets to Second Brain

Add tweets with author linking, tags, and personal annotations.

## Expected Input

User provides:
1. **Tweet URL** - `x.com/*/status/*` or `twitter.com/*/status/*`
2. **Pasted tweet content** - Copy-pasted from Twitter/X

Example user input:
```text
add this tweet https://x.com/naval/status/1234567890

my favorite way to use Claude Code is spec based

start with a minimal spec and ask Claude to interview you
```

## Workflow

```text
Phase 1: Parse URL → Extract tweet ID and author handle
Phase 2: Parse Content → Extract text, date, author name from paste
Phase 3: Author Resolution → Check/create author profile
Phase 4: Generate Tweet File → Write to content/tweets/
Phase 5: Suggest Editing → Tags, annotations, wiki-links
Phase 6: Quality Check → Run pnpm lint:fix && pnpm typecheck
```

### Phase 1: Parse URL

Extract from URL using regex:
- `tweetId`: The numeric ID from `/status/{id}`
- `authorHandle`: The username from `x.com/{username}/status/`

```text
Pattern: (?:x\.com|twitter\.com)/([^/]+)/status/(\d+)
Example: https://x.com/naval/status/1789234567890
         → authorHandle: "naval"
         → tweetId: "1789234567890"
```

### Phase 2: Parse Content

From the pasted text:
- **tweetText**: The main tweet content (clean up any extra whitespace)
- **tweetedAt**: If date is visible in paste, use it. Otherwise use today's date.
- **authorName**: If visible (e.g., "Naval Ravikant"), use it. Otherwise use handle.

If critical info is missing, use the `AskUserQuestion` tool to gather it:

```yaml
question: "I need some missing tweet info. What is the tweet text?"
header: "Tweet Info"
multiSelect: false
options:
  - label: "I'll provide it"
    description: "Let me paste the tweet content"
```

For optional fields like date, ask separately if needed.

### Phase 3: Author Resolution

1. Check if author exists:
   ```bash
   ls content/authors/{authorHandle}.md
   ```

2. If not exists, create minimal profile:
   ```yaml
   ---
   name: "{Display Name or Handle}"
   slug: {authorHandle}
   socials:
     twitter: "https://x.com/{authorHandle}"
   ---
   ```

3. For full author enhancement, suggest running `/enhance-author {authorHandle}`

### Phase 4: Generate Tweet File

**Slug format:** `tweet-{tweetId}`

**File path:** `content/tweets/tweet-{tweetId}.md`

**Frontmatter template:**
```yaml
---
type: tweet
title: "{First 50 chars of tweet}..."
tweetId: "{tweetId}"
tweetUrl: "{originalUrl}"
tweetText: "{full tweet text}"
author: {authorHandle}
tweetedAt: {YYYY-MM-DD}
tags:
  - {suggested tags}
---

{User's personal annotations go here}
```

### Phase 5: User Editing

After saving, inform user:
- File location
- Suggest adding tags (use `.claude/skills/adding-notes/scripts/list-existing-tags.sh` for suggestions)
- Suggest adding personal annotations in the body
- Suggest wiki-links to related notes

## Tag Suggestions

Based on tweet content, suggest from existing tags:
```bash
.claude/skills/adding-notes/scripts/list-existing-tags.sh
```

Common tweet themes → tags:
- Wisdom, advice → `mindset`, `philosophy`
- Business, startups → `startup`, `business`
- Technology → `tech`, `programming`
- Productivity → `productivity`, `habit`
- AI, Claude → `claude-code`, `ai-agents`, `prompt-engineering`

## Validation

Before saving, verify:
1. Tweet ID is unique (no duplicate file exists)
2. Author profile exists or was created
3. `tweetedAt` is valid date format
4. `tweetText` is not empty

---

## Phase 6: Quality Check

Run linter and type check to catch any issues:

```bash
pnpm lint:fix && pnpm typecheck
```

If errors are found, fix them before completing the task.
