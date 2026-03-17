---
name: post-instagram
description: |
  Create and post content on Instagram to generate business visibility and leads.
  Drafts posts based on business goals, creates approval requests, and publishes
  via Playwright browser automation after human approval. Also generates weekly
  engagement summaries from Instagram notifications in /Needs_Action.
  Use when scheduled to post, when the user requests an Instagram post, or for
  generating a summary of Instagram activity.
---

# Post to Instagram / Generate Instagram Summary

Create and publish Instagram posts, or summarize Instagram activity.

## Workflow A: Post to Instagram

### 1. Generate Post Content
Read `vault/Business_Goals.md` to understand current business objectives.
Draft an Instagram post that:
- Is visually descriptive (mention what image/video to use)
- Uses 5-10 relevant hashtags
- Has a clear call-to-action
- Is 75-150 words for the caption
- Stays professional and on-brand

### 2. Create Approval Request
**All Instagram posts require human approval before publishing.**

Create an approval file in `vault/Pending_Approval/`:
```markdown
---
type: approval_request
request_id: "YYYYMMDD_HHMMSS_instagram_post"
action: instagram_post
priority: medium
created: ISO-8601
expires: ISO-8601 (24 hours from creation)
status: pending
details:
  platform: "instagram"
  content_preview: "First 100 chars of caption..."
  hashtags: "#business #ai"
---

# Approval Required: Instagram Post

## Proposed Post Caption
[Full caption text here]

## Suggested Hashtags
[Hashtags here]

## How to Respond
- **To Approve**: Move this file to the `/Approved` folder
- **To Reject**: Move this file to the `/Rejected` folder
```

### 3. Publish (After Approval)
Once the file appears in `vault/Approved/`:

1. Start Playwright MCP if not running:
   ```bash
   bash .claude/skills/browsing-with-playwright/scripts/start-server.sh
   ```

2. Navigate to Instagram web:
   ```bash
   python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
     -u http://localhost:8808 -t browser_navigate \
     -p '{"url": "https://www.instagram.com/"}'
   ```

3. Click the "+" create button, upload image (if applicable), add caption with hashtags, and post.

4. Verify success by checking for confirmation.

### 4. Log the Action
```json
{
  "timestamp": "ISO-8601",
  "action_type": "instagram_post_published",
  "actor": "claude_code",
  "platform": "instagram",
  "content_preview": "First 100 chars...",
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

---

## Workflow B: Generate Instagram Activity Summary

### 1. Scan /Needs_Action
Read all `INSTAGRAM_*.md` files in `vault/Needs_Action/`.

### 2. Categorize Notifications
Group by type:
- Direct messages (high priority)
- Follow requests (medium priority)
- Post engagement: likes, comments (low priority)
- Business/Creator analytics (medium priority)

### 3. Write Summary
Create a summary in `vault/Briefings/INSTAGRAM_Summary_YYYYMMDD.md` with:
- Total notification count
- DMs requiring response
- Engagement metrics (likes, comments, follows)
- Top performing content indicators
- Recommendations for follow-up

### 4. Log the Action
```json
{
  "timestamp": "ISO-8601",
  "action_type": "instagram_summary_generated",
  "actor": "claude_code",
  "result": "success"
}
```
