---
name: reddit-post
description: Post to Reddit using AppleScript Chrome control. Use when user wants to post to Reddit, share on subreddits, or promote open source projects on Reddit. Triggers on "post to reddit", "share on reddit", "reddit post", "submit to subreddit", or any Reddit posting request.
---

# Reddit Posting Skill (AppleScript Chrome Control)

Post to Reddit by controlling the user's real Chrome via AppleScript. No Playwright, no Selenium, no API tokens.

---

## How It Works

```
Claude Code → osascript → Chrome (real browser, logged in) → Reddit /api/submit
```

- Same-origin fetch with cookies → undetectable
- Reddit's `/api/submit` endpoint for text/link posts
- Modhash from `/api/me.json` for CSRF protection

---

## Prerequisites

- **macOS only** (AppleScript is a macOS technology)
- Chrome: View → Developer → Allow JavaScript from Apple Events (restart Chrome after enabling)
- User logged into Reddit in Chrome

---

## Method Detection (Run First)

```bash
WINDOWS=$(osascript -e 'tell application "Google Chrome" to return count of windows' 2>/dev/null)
if [ "$WINDOWS" = "0" ] || [ -z "$WINDOWS" ]; then
    echo "METHOD 2 (System Events + Console)"
else
    echo "METHOD 1 (execute javascript)"
fi
```

See `reddit-cultivate` skill for full Method 1 vs Method 2 details.

---

## Posting Workflow

### Step 1: Get Modhash

```bash
osascript -e 'tell application "Google Chrome" to tell active tab of first window to execute javascript "fetch(\"/api/me.json\",{credentials:\"include\"}).then(r=>r.json()).then(d=>{document.title=\"UH:\"+d.data.modhash})"'
sleep 2
osascript -e 'tell application "Google Chrome" to return title of active tab of first window'
```

### Step 2: Submit Post

Navigate Chrome to reddit.com first (same-origin requirement), then submit:

```javascript
(async()=>{
  try {
    let body = new URLSearchParams({
      sr: "SideProject",           // subreddit name (no r/ prefix)
      kind: "self",                // "self" for text, "link" for URL
      title: "Your post title",
      text: "Your post body with **markdown** support",
      uh: "MODHASH_HERE",
      api_type: "json",
      resubmit: "true"
    });
    let resp = await fetch("/api/submit", {
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: body.toString()
    });
    let result = await resp.json();
    document.title = "POSTED:" + JSON.stringify(result);
  } catch(e) {
    document.title = "ERR:" + e.message;
  }
})()
```

For **link posts**, change:
```javascript
kind: "link",
url: "https://github.com/your/repo",  // instead of text
```

### Step 3: Extract Post Link

The response contains `result.json.data.url` — the direct link to the new post.

### Step 4: Add Flair (if required)

Some subreddits require flair. After posting, use:

```javascript
(async()=>{
  try {
    // First get available flairs
    let resp = await fetch("/r/SUBREDDIT/api/link_flair_v2", {credentials: "include"});
    let flairs = await resp.json();
    document.title = "FLAIRS:" + JSON.stringify(flairs.map(f => ({id: f.id, text: f.text})));
  } catch(e) {
    document.title = "ERR:" + e.message;
  }
})()
```

Then apply flair:
```javascript
(async()=>{
  try {
    let body = new URLSearchParams({
      link: "t3_POST_ID",
      flair_template_id: "FLAIR_ID",
      uh: "MODHASH"
    });
    await fetch("/api/selectflair", {
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: body.toString()
    });
    document.title = "FLAIR_SET";
  } catch(e) {
    document.title = "ERR:" + e.message;
  }
})()
```

### Step 5: Session Summary

**Always end with the post link:**

| Sub | Title | Post Link |
|-----|-------|-----------|
| r/SideProject | "Your title" | https://www.reddit.com/r/SideProject/comments/abc123/... |

---

## Spam Filter Avoidance

### Words to AVOID in titles/body

| Avoid | Use Instead |
|-------|-------------|
| crawl, crawled, crawling | compiled, cataloged, indexed, collected |
| scrape, scraping | gathered, extracted, retrieved |
| bot, automated | tool, script, program |
| free (overused) | open source, MIT licensed |
| hack, hacks | tips, techniques, methods |

### Content Triggers to Avoid
- Multiple external links (max 1-2)
- URL shorteners (bit.ly, tinyurl)
- New account + promotional content
- Same content across multiple subreddits quickly
- Excessive self-promotion language

---

## Best Subreddits for Open Source Projects

| Subreddit | Members | Best For | Notes |
|-----------|---------|----------|-------|
| r/coolgithubprojects | 60K | GitHub repos | Designed for this! |
| r/SideProject | 453K | Side projects | Very welcoming |
| r/opensource | 100K+ | Open source tools | Technical audience |
| r/programming | 6M+ | Dev tools | High competition |
| r/Python | 1.5M+ | Python tools | Active community |
| r/webdev | 2M+ | Web tools | "Showoff Saturday" only |
| r/selfhosted | 400K+ | Self-hosted tools | Great engagement |

---

## Best Times to Post (US Eastern Time)

| Day | Best Time |
|-----|-----------|
| Monday | 6-8 AM |
| Tuesday | 7-9 AM |
| Wednesday | 8-10 AM |
| Thursday | 7-9 AM |
| Friday | 6-8 AM |
| Saturday | 7-9 AM |
| Sunday | 8-10 AM |

Post 30 minutes BEFORE peak times for momentum building.

---

## Post Templates

### Open Source Project Announcement
```
Title: I built [PROJECT_NAME] - [one-line description] (open source)

Body:
Hey everyone,

I created [PROJECT_NAME] to solve [PROBLEM].

**What it does:**
- Feature 1
- Feature 2
- Feature 3

**Tech stack:** [Languages/frameworks]

**Links:**
- GitHub: [single link]

Happy to answer any questions!
```

### Tool/Resource Share
```
Title: [TOOL_NAME]: [what it does] - free and open source

Body:
Built this because [reason/pain point].

**Features:**
- [List 3-5 key features]

**How to use:**
[Brief code example or instructions]

GitHub: [link]

Feedback welcome!
```

---

## Cross-Posting Strategy

Stagger posts across subreddits for maximum reach:

1. **Day 1**: Primary subreddit (most relevant)
2. **Day 2-3**: Secondary subreddit (different audience)
3. **Day 4-5**: General subreddit (r/SideProject, etc.)

**Never post to multiple subreddits on the same day** — triggers spam detection.

---

## Error Recovery

| Issue | Solution |
|-------|----------|
| "Post removed by filters" | Rewrite without trigger words, reduce links |
| "You're doing that too much" | Wait 10-15 min, need more karma |
| "This community requires flair" | Use /api/selectflair after posting |
| "Title too long" | Keep under 300 characters |
| Post not visible | Check if shadowbanned: profile in incognito |
| Modhash expired | Re-fetch from /api/me.json |

---

## Why AppleScript (Not Playwright)

| Tool | Problem |
|------|---------|
| Playwright | `navigator.webdriver=true`, detected by Reddit |
| Selenium | Same detection issue |
| curl + API | IP blocked after few requests |
| **AppleScript** | Controls real Chrome, undetectable, cookies included |
