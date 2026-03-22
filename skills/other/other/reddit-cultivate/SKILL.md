---
name: reddit-cultivate
description: Reddit account cultivation for indie developers. Uses AppleScript to control real Chrome — undetectable by anti-bot systems. Checks karma, finds rising posts, drafts comments, and posts directly. Triggers on "/reddit-cultivate", "check my reddit", "reddit maintenance", "find reddit opportunities", "build reddit karma".
---

# Reddit Cultivation Skill (AppleScript Chrome Control)

Build and maintain Reddit presence by controlling the user's real Chrome browser via AppleScript. No Playwright, no Selenium, no API tokens.

---

## How It Works

```
Claude Code → osascript → Chrome (real browser, logged in) → Reddit
```

- AppleScript executes JavaScript in Chrome's active tab
- Chrome is already logged into Reddit → cookies sent automatically
- Same-origin fetch → no CORS, no detection, no IP blocks
- Reddit cannot distinguish this from human browsing

---

## Prerequisites

- **macOS only** (AppleScript is a macOS technology)
- Chrome: View → Developer → Allow JavaScript from Apple Events ✓ (restart Chrome after enabling)
- User logged into Reddit in Chrome

---

## Method Detection (Run First)

Chrome multi-profile can cause AppleScript to not see windows. Always detect first:

```bash
WINDOWS=$(osascript -e 'tell application "Google Chrome" to return count of windows' 2>/dev/null)
if [ "$WINDOWS" = "0" ] || [ -z "$WINDOWS" ]; then
    echo "Use Method 2 (System Events + Console)"
else
    echo "Use Method 1 (execute javascript)"
fi
```

---

## Method 1: AppleScript Execute JavaScript (Preferred)

Works when `count of windows > 0`.

### Navigate

```bash
osascript -e 'tell application "Google Chrome" to tell active tab of first window to set URL to "https://www.reddit.com/r/SideProject/rising/"'
```

### Execute JS & Read Result (document.title trick)

```bash
# Run JS that writes result to document.title
osascript -e 'tell application "Google Chrome" to tell active tab of first window to execute javascript "fetch(\"/api/me.json\",{credentials:\"include\"}).then(r=>r.json()).then(d=>{document.title=\"R:\"+JSON.stringify({name:d.data.name,karma:d.data.total_karma})})"'

# Wait, then read title
sleep 2
osascript -e 'tell application "Google Chrome" to return title of active tab of first window'
```

### JXA for Complex JS (avoids escaping hell)

```bash
osascript -l JavaScript -e '
var chrome = Application("Google Chrome");
var tab = chrome.windows[0].activeTab;
tab.execute({javascript: "(" + function() {
    // Complex JS here — no escaping needed
    fetch("/r/SideProject/rising.json?limit=10", {credentials: "include"})
        .then(r => r.json())
        .then(d => {
            var posts = d.data.children.map(p => ({
                title: p.data.title.substring(0, 60),
                score: p.data.score,
                comments: p.data.num_comments,
                id: p.data.name,
                url: "https://reddit.com" + p.data.permalink
            }));
            document.title = "POSTS:" + JSON.stringify(posts);
        });
} + ")();"});
'
```

---

## Method 2: System Events + Console (Multi-Profile Fallback)

When AppleScript can't see Chrome windows (multi-profile bug), use keyboard automation.

### Step 1: Copy JS to Clipboard

```bash
python3 -c "
import subprocess
js = '''(async()=>{
    let resp = await fetch('/api/me.json', {credentials: 'include'});
    let data = await resp.json();
    document.title = 'R:' + JSON.stringify({name: data.data.name, karma: data.data.total_karma});
})()'''
subprocess.run(['pbcopy'], input=js.encode(), check=True)
"
```

### Step 2: Execute via Chrome Console Keyboard Shortcuts

```bash
osascript -e '
tell application "System Events"
    tell process "Google Chrome"
        set frontmost to true
        delay 0.3
        -- Cmd+Option+J = open/close Console
        key code 38 using {command down, option down}
        delay 1
        -- Select all + Paste + Enter
        keystroke "a" using {command down}
        delay 0.2
        keystroke "v" using {command down}
        delay 0.5
        key code 36
        delay 0.3
        -- Close Console
        key code 38 using {command down, option down}
    end tell
end tell'
```

### Step 3: Read Title via System Events

```bash
sleep 3
osascript -e '
tell application "System Events"
    tell process "Google Chrome"
        return name of window 1
    end tell
end tell'
```

---

## Workflow

### Step 1: Check Account Status

Get username, karma, verify login using `/api/me.json`.

### Step 2: Scan Rising Posts

For each target subreddit, fetch rising posts:

```
/r/{subreddit}/rising.json?limit=10
```

Look for:
- Rising posts with < 15 comments (early = more visibility)
- Score > 2 (some traction)
- Questions you can answer or discussions with genuine insight

### Step 3: Draft Comments

Rules:
- 2-4 sentences, natural tone
- Add genuine value (insights, experience, helpful info)
- No self-promotion, no links, no emojis
- Match the subreddit's culture
- Each comment must be unique

### Step 4: Post All Comments

Get modhash, then post each comment with 4s delay between posts.

```javascript
// Get modhash first
let me = await fetch("/api/me.json", {credentials: "include"}).then(r=>r.json());
let uh = me.data.modhash;

// Post comment
let body = new URLSearchParams({
    thing_id: "t3_xxxxx",  // post fullname
    text: "Your comment here",
    uh: uh,
    api_type: "json"
});
let resp = await fetch("/api/comment", {
    method: "POST",
    credentials: "include",
    headers: {"Content-Type": "application/x-www-form-urlencoded"},
    body: body.toString()
});
let result = await resp.json();
document.title = "POSTED:" + JSON.stringify(result);
```

Extract the comment ID from the response HTML: look for `id-t1_XXXXXXX` in the result.

### Step 5: Session Summary with Links

**ALWAYS end with a summary table containing direct links to every comment posted.**

The comment link format is:
```
https://www.reddit.com/r/{subreddit}/comments/{post_id}/comment/{comment_id}/
```

Where:
- `{subreddit}` = the subreddit name
- `{post_id}` = the post ID (from `thing_id` minus the `t3_` prefix)
- `{comment_id}` = extracted from the POST response (the `t1_XXXXXXX` value, minus `t1_` prefix)

**Example summary table:**

| # | Sub | Post | Comment Link |
|---|-----|------|-------------|
| 1 | r/SideProject | "Post title" | https://www.reddit.com/r/SideProject/comments/abc123/comment/xyz789/ |
| 2 | r/ClaudeAI | "Post title" | https://www.reddit.com/r/ClaudeAI/comments/def456/comment/uvw012/ |

This lets the user bookmark, follow up on replies, and track which comments got traction.

---

## Recommended Target Subreddits

| Priority | Subreddit | Why |
|----------|-----------|-----|
| High | r/SideProject | Project launches, very welcoming |
| High | r/indiehackers | Revenue/growth discussions |
| Medium | r/ClaudeAI | AI tooling audience |
| Medium | r/coolgithubprojects | Open source visibility |
| Medium | r/startups | Startup discussions |
| Medium | r/entrepreneur | Business insights |
| Medium | r/opensource | Technical audience |

---

## Comment Guidelines

- Add genuine value (insights, experience, helpful info)
- No self-promotion in comments
- Match the subreddit's tone
- Be specific, not generic
- 2-4 sentences, natural voice

---

## Rate Limiting

| Action | Limit |
|--------|-------|
| Between API calls | 2+ seconds |
| Between posts | 4+ seconds |
| Per session | Max 5 comments |
| Daily | 10-15 comments max |

---

## Karma Milestones

| Karma | Unlocks |
|-------|---------|
| 100+ | Can post in most subreddits |
| 500+ | Reduced spam filter triggers |
| 1000+ | Trusted contributor status |
| 5000+ | Community recognition |

---

## Algorithm Insights

- **First 30 minutes** determine if post reaches Hot page
- Early upvotes weighted 10x more than later ones
- 2 early comments > 20 passive upvotes
- **Best posting time**: Sunday 6-8 AM ET
- Upvote ratio matters: 100↑/10↓ (90%) beats 150↑/50↓ (75%)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `count of windows` = 0 | Chrome multi-profile bug → use Method 2 |
| "Allow JavaScript" not working | Restart Chrome after enabling |
| Modhash expired | Re-fetch from `/api/me.json` |
| 403 response | Rate limited, wait 5+ minutes |
| Comment not appearing | Check for shadowban: visit profile in incognito |

---

## Why AppleScript (Not Playwright/Selenium)

| Tool | Problem |
|------|---------|
| Playwright | Sets `navigator.webdriver=true`, detected instantly |
| Selenium | Same detection issue |
| Puppeteer | Same detection issue |
| curl + API | IP blocked by Reddit after few requests |
| **AppleScript** | Controls real Chrome, undetectable, cookies included |
