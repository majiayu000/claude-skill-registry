---
name: post-facebook
description: |
  Create and post content on Facebook to generate business visibility and leads.
  Drafts posts based on business goals, creates approval requests, and publishes
  via Playwright browser automation after human approval. Also generates weekly
  engagement summaries from Facebook notifications in /Needs_Action.
  Use when scheduled to post, when the user requests a Facebook post, or for
  generating a summary of Facebook activity.
---

# Post to Facebook / Generate Facebook Summary

Create and publish Facebook posts, or summarize Facebook activity for the CEO Briefing.

## Workflow A: Post to Facebook

### 1. Generate Post Content
Read `vault/Business_Goals.md` to understand current business objectives.
Draft a Facebook post that:
- Highlights business expertise or achievements
- Provides value to the target audience
- Includes a call-to-action when appropriate
- Stays professional and on-brand
- Is 100-250 words (optimal Facebook length for pages)

### 2. Create Approval Request
**All Facebook posts require human approval before publishing.**

Create an approval file in `vault/Pending_Approval/`:
```markdown
---
type: approval_request
request_id: "YYYYMMDD_HHMMSS_facebook_post"
action: facebook_post
priority: medium
created: ISO-8601
expires: ISO-8601 (24 hours from creation)
status: pending
details:
  platform: "facebook"
  content_preview: "First 100 chars of post..."
---

# Approval Required: Facebook Post

## Proposed Post Content
[Full post text here]

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

2. Navigate to Facebook:
   ```bash
   python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
     -u http://localhost:8808 -t browser_navigate \
     -p '{"url": "https://www.facebook.com/"}'
   ```

3. Click "What's on your mind" / create post button, type content, and post.

4. Verify success by checking for confirmation.

### 4. Log the Action
Write to `vault/Logs/YYYY-MM-DD.json`:
```json
{
  "timestamp": "ISO-8601",
  "action_type": "facebook_post_published",
  "actor": "claude_code",
  "platform": "facebook",
  "content_preview": "First 100 chars...",
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

---

## Workflow B: Generate Facebook Activity Summary

### 1. Scan /Needs_Action
Read all `FACEBOOK_*.md` files in `vault/Needs_Action/`.

### 2. Categorize Notifications
Group by type:
- Messages (high priority)
- Friend/Page requests (medium priority)
- Engagement: likes, comments, shares (low priority)
- Business/Page analytics (medium priority)

### 3. Write Summary
Create a summary in `vault/Briefings/FACEBOOK_Summary_YYYYMMDD.md` with:
- Total notification count
- Messages requiring response
- Engagement metrics
- Recommendations for follow-up

### 4. Log the Action
```json
{
  "timestamp": "ISO-8601",
  "action_type": "facebook_summary_generated",
  "actor": "claude_code",
  "result": "success"
}
```
