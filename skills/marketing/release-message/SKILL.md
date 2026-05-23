---
name: release-message
description: Generate release messages for social media (LinkedIn, Bluesky, X) and ray.so code snippets. Use when the user says "release", "/release", "release message", wants to announce a new release, needs help writing release posts, or wants to create social media content for a software release.
---

# Release Message Generator

Generate professional release announcements for LinkedIn (Danish), Bluesky (Danish), and X (English), plus ray.so code snippets to visualize key changes.

## Workflow

1. Gather context (PR URL/number and git diff)
2. Analyze key changes from diff
3. Load writing style from references
4. Generate posts for all three platforms
5. Create ray.so code snippet
6. Save output to `.releases/<version>/`

## Step 1: Gather Context

Ask the user for:
- PR URL or PR number
- Version number (e.g., v1.0.0)

Then gather the diff:

```bash
# Get PR details (if using PR number)
gh pr view <pr-number> --json title,body,url

# Get the diff from the PR
gh pr diff <pr-number>

# Or if merged, get diff between tags
git diff <previous-tag>..<new-tag>
```

## Step 2: Analyze Changes

From the diff, identify:
- **Primary feature/fix**: The main change to highlight
- **Key code changes**: Code snippets worth visualizing
- **User benefit**: How this helps users

Focus on what matters to users, not internal refactoring.

## Step 3: Load Writing Style

Read the user's writing style reference:

```
references/writing-style.md
```

Match their:
- Tone and vocabulary
- Emoji usage
- Hashtag preferences
- Call-to-action style

If no style reference exists, use a neutral professional/casual mix.

## Step 4: Generate Posts

### LinkedIn (Danish)

Format:
- 1-3 short paragraphs
- Professional but approachable tone
- Include the key change and why it matters
- End with call-to-action

Requirements:
- Language: Danish
- Include link to merged PR
- Include star request: "Giv en stjerne hvis du finder det nyttigt: https://github.com/kasperjunge/agent-resources/"

### Bluesky (Danish)

Format:
- Max 300 characters
- Casual, conversational tone
- One key highlight

Requirements:
- Language: Danish
- Include link to merged PR
- Brief star request

### X/Twitter (English)

Format:
- Max 280 characters
- Casual, engaging tone
- One key highlight

Requirements:
- Language: English
- Include link to merged PR
- Brief star request

## Step 5: Create ray.so Snippet

Select the most visually interesting code change from the diff.

Guidelines:
- Keep it short (5-15 lines)
- Show the "before and after" or just the new code
- Remove unnecessary context
- Focus on the clever/interesting part

Output format:
```
// Title: <what this shows>
<code snippet>

// Generate at: https://ray.so
// Recommended settings: Dark theme, padding 32, language auto-detect
```

## Step 6: Save Output

Create the output directory and files:

```bash
mkdir -p .releases/<version>
```

Save files:
- `.releases/<version>/linkedin.md` - LinkedIn post
- `.releases/<version>/bluesky.md` - Bluesky post
- `.releases/<version>/x.md` - X/Twitter post
- `.releases/<version>/rayso-snippet.txt` - Code for ray.so

## Output Templates

### linkedin.md
```markdown
# LinkedIn Release Post - <version>

<post content>

---
PR: <pr-url>
```

### bluesky.md
```markdown
# Bluesky Release Post - <version>

<post content>

---
Characters: <count>/300
PR: <pr-url>
```

### x.md
```markdown
# X Release Post - <version>

<post content>

---
Characters: <count>/280
PR: <pr-url>
```

### rayso-snippet.txt
```
<code snippet>

---
Generate at: https://ray.so
Settings: Dark theme, padding 32
```

## Example Output

### LinkedIn (Danish)
```
Ny release af agent-resources!

Nu kan du tilføje og fjerne ressourcer med en enkelt kommando - ingen grund til at huske forskellige flags. CLI'en gætter automatisk typen baseret på filstien.

Se ændringerne her: https://github.com/kasperjunge/agent-resources/pull/42

Giv en stjerne hvis du finder det nyttigt: https://github.com/kasperjunge/agent-resources/
```

### Bluesky (Danish)
```
agent-resources v1.1.0: Unified commands er her! Nu gætter CLI'en automatisk ressource-typen. Meget nemmere.

PR: github.com/kasperjunge/agent-resources/pull/42
```

### X (English)
```
agent-resources v1.1.0: Unified commands are here! The CLI now auto-detects resource types. Much simpler.

PR: github.com/kasperjunge/agent-resources/pull/42
```

## Resources

### references/
- `writing-style.md` - User's personal writing style examples for tone matching
