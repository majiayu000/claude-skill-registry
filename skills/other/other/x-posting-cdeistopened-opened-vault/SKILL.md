---
name: x-posting
description: Post and schedule content to X/Twitter. Use when batch processing social posts, promoting podcasts/blogs, or scheduling content. Handles guest tagging, template matching, and getlate.dev API integration.
---

# X Posting Workflow

End-to-end workflow for creating, approving, and scheduling X/Twitter posts from OpenEd content.

## When to Use

- Batch processing X posts from recent content
- Promoting podcast episodes or blog posts
- Scheduling a week of social content
- Any X posting that involves guest tagging

## Prerequisites

- `GETLATE_API_KEY` in `.env`
- Connected Twitter account in getlate.dev (@OpenEdHQ)

---

## The Workflow

### Step 1: Find Content

Search the Master Content Database for recent/relevant content:

```bash
# Find recent podcasts
ls "Content/Master Content Database/Podcasts/" | head -20

# Find recent blog posts
ls "Content/Master Content Database/Blog Posts/" | head -20
```

Read source files to extract:
- Key insights and quotes
- Guest names
- Actual URLs (from frontmatter `url:` field)

**CRITICAL:** Never hallucinate URLs. Always pull from the source file's frontmatter.

---

### Step 2: Find Guest X Handles

**Before writing any post featuring a guest:**

1. Web search: `"[Guest Name] [Company] Twitter X account"`
2. Verify it's the correct person (check bio)
3. Note both personal handle AND company handle if applicable

Common OpenEd guest handles:
- See `Studio/Social_Scheduling.md` for previously found handles
- Add new handles to the reference table when found

---

### Step 3: Framework Fitting via Sub-Agents

**CRITICAL: Spawn a sub-agent for EACH piece of content.**

This is token-heavy but ensures quality. Each sub-agent does deep framework fitting rather than surface-level template matching.

**Sub-Agent Prompt Template:**

```
You are writing X/Twitter posts for OpenEd. Your job is DEEP FRAMEWORK FITTING - matching this concept to proven templates that amplify it.

## Source Content
[Paste the full content or key excerpts]

## Guest Info
- Name: [Guest Name]
- X Handle: @[handle]
- Company: [Company] (@[company_handle] if applicable)

## URL (use exactly)
[URL from frontmatter]

## Your Task

### Phase 1: Concept Extraction
Extract from this content:
1. Core insight (one sentence)
2. Emotional hook (what feeling does this evoke?)
3. Most quotable moment
4. Surprising fact or statistic
5. Contrarian angle (what does this challenge?)

### Phase 2: Template Review
Read the FULL post-structures.md file. Do not skim.

For this concept, evaluate AT LEAST these template categories:
- Commentary (quote + translation + explanation)
- Contrast Evaluation (X overrated, Y underrated)
- Paradox Hook (present contradiction)
- Comparison with percentages (numbers + question)
- Personal Story (setup → conflict → resolution)
- One Sentence Comparison
- Behavior Dichotomy
- Binary Framing Hook
- Counterintuitive Statement Hook

For each potentially fitting template:
1. Name the template
2. Explain WHY it might work for this concept
3. Rate fit: Strong / Moderate / Weak
4. Draft a quick test version

### Phase 3: Select and Write
Choose 2-3 BEST fitting templates. Write full post variations using the EXACT template structure.

### Phase 4: Voice Validation
For each draft, check against AI-tells:

HARD BLOCKS (reject and rewrite if present):
- Correlative constructions ("X isn't just Y - it's Z")
- Split correlatives ("It wasn't about X. It was about Y.")
- Staccato fragments ("No X. No Y. Just Z.")
- Setup phrases ("Here's the thing:", "The best part?")
- Triple adjective patterns
- Thesaurus words (utilize, leverage, comprehensive, crucial)

VOICE CHECK:
- Does this sound like a person talking or performing "good writing"?
- Is this something you'd actually text to a friend?
- Does it follow the template structure or drift into generic copy?

### Output Format
For each post option:
1. Template used: [Name]
2. Why this template: [1-2 sentences]
3. Post:
> [The actual post text]
>
> [link]
4. Voice validation: [Pass/Fail with notes]
```

**Launch sub-agents in parallel** - one per content piece. They will return structured options ready for the scheduling file.

---

### Step 4: Compile Scheduling File

Collect sub-agent outputs into `Studio/Social_Scheduling.md`:

```markdown
# X Post Scheduling Queue

**Created:** [date]
**Status:** Awaiting approval

---

### 1. [Content Title] - @[guest_handle]

**URL:** [actual URL from source]

**Option A - [Template Name]:**
> [Post content]
>
> [link]

Template reasoning: [Why this template fits]

- [ ] Approve Option A

**Option B - [Template Name]:**
> [Post content]
>
> [link]

Template reasoning: [Why this template fits]

- [ ] Approve Option B
```

User marks approvals with `[X]` and adds notes in `{NOTES: ...}`.

---

### Step 5: Voice Validation (Final Check)

Before posting/scheduling, run final validation:

**Hard Blocks:**
- [ ] No correlative constructions ("X isn't just Y - it's Z")
- [ ] No split correlatives ("X wasn't about Y. It was about Z.")
- [ ] No staccato fragments ("No X. No Y. Just Z.")
- [ ] No setup phrases ("Here's the thing:", "The best part?")

**Soft Checks:**
- [ ] Sounds like a person, not a copywriter
- [ ] Uses actual template structure (can identify which one)
- [ ] Guest tagged correctly
- [ ] URL is real (from source file)

---

### Step 6: Post and Schedule via getlate.dev

**Post immediately:**
```bash
python3 agents/post_tweet.py '[tweet content]'
```

**Schedule for future:**
```python
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

api_key = os.getenv("GETLATE_API_KEY")
base_url = "https://getlate.dev/api/v1"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Get account ID
response = requests.get(f"{base_url}/accounts", headers=headers)
accounts = response.json().get("accounts", [])
twitter_account = next((a for a in accounts if a.get("platform") == "twitter"), None)
account_id = twitter_account.get("_id")

# Schedule post (9am ET = 14:00 UTC in winter)
post_data = {
    "platforms": [{"platform": "twitter", "accountId": account_id}],
    "content": "Your tweet content here",
    "scheduledFor": "2026-01-15T14:00:00Z"  # ISO 8601 format
}

response = requests.post(f"{base_url}/posts", headers=headers, json=post_data)
```

**Time conversion:**
- 9am ET (winter) = 14:00 UTC
- 9am ET (summer/DST) = 13:00 UTC

---

## Quick Reference

### getlate.dev API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/accounts` | GET | List connected accounts |
| `/posts` | POST | Create/schedule post |

**Post payload:**
```json
{
  "platforms": [{"platform": "twitter", "accountId": "..."}],
  "content": "Tweet text",
  "publishNow": true,           // OR
  "scheduledFor": "ISO-8601"    // for scheduling
}
```

### Best Posting Times (ET)

- 8-9am - Morning commute
- 12-1pm - Lunch break
- 7-8pm - Evening wind-down

### Character Limits

- Optimal: 70-100 characters
- Max: 280 characters
- With link: ~250 characters of text

---

## Sub-Agent Required Reading

Each sub-agent MUST read these files before writing posts:

| File | Purpose | Tokens |
|------|---------|--------|
| `.claude/skills/text-content/references/templates/post-structures.md` | 100+ template structures | ~4000 |
| `.claude/skills/ai-tells/SKILL.md` | Voice constraints | ~200 |
| `.claude/skills/ai-tells/references/pirate-wires-examples.md` | Voice examples | ~1500 |
| Source content file | The actual content to promote | varies |

**Why this matters:** The quality difference between skimming templates and deeply reading them is the difference between generic AI copy and posts that actually follow proven structures.

---

## Related Skills

- `text-content` - Template library and framework fitting
- `ai-tells` - Voice validation
- `ghostwriter` - Deeper voice guidance

---

## Files

- `agents/post_tweet.py` - Single tweet posting
- `agents/test_tweet.py` - API testing
- `Studio/Social_Scheduling.md` - Current queue

---

*Last updated: 2026-01-14 (v2 - added sub-agent framework fitting)*
