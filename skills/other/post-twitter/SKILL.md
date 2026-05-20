---
name: post-twitter
description: |
  Create and post content on Twitter/X to generate business visibility and engagement.
  Drafts tweets based on business goals, creates approval requests, and publishes
  via Playwright browser automation after human approval. Also generates weekly
  engagement summaries from Twitter notifications in /Needs_Action.
  Use when scheduled to post, when the user requests a tweet, or for
  generating a summary of Twitter activity.
---

# Post to Twitter (X) / Generate Twitter Summary

Create and publish tweets, or summarize Twitter activity for business intelligence.

## Workflow A: Post to Twitter

### 1. Generate Tweet Content
Read `vault/Business_Goals.md` to understand current business objectives.
Draft a tweet that:
- Is concise and impactful (max 280 characters)
- Uses 2-4 relevant hashtags
- Includes a clear value proposition or call-to-action
- Stays professional and on-brand
- Thread format for longer announcements (number each tweet 1/N)

### 2. Create Approval Request
**All tweets require human approval before publishing.**

Create an approval file in `vault/Pending_Approval/`:
```markdown
---
type: approval_request
request_id: "YYYYMMDD_HHMMSS_twitter_post"
action: twitter_post
priority: medium
created: ISO-8601
expires: ISO-8601 (24 hours from creation)
status: pending
details:
  platform: "twitter"
  content_preview: "First 100 chars of tweet..."
  character_count: "0"
---

# Approval Required: Twitter Post

## Proposed Tweet
[Full tweet text here — max 280 characters]

## Hashtags
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

2. Navigate to Twitter/X:
   ```bash
   python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
     -u http://localhost:8808 -t browser_navigate \
     -p '{"url": "https://x.com/compose/tweet"}'
   ```

3. Type the tweet content and click Post.

4. Verify success by checking for confirmation.

### 4. Log the Action
```json
{
  "timestamp": "ISO-8601",
  "action_type": "twitter_post_published",
  "actor": "claude_code",
  "platform": "twitter",
  "content_preview": "First 100 chars...",
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

---

## Workflow B: Generate Twitter Activity Summary

### 1. Scan /Needs_Action
Read all `TWITTER_*.md` files in `vault/Needs_Action/`.

### 2. Categorize Notifications
Group by type:
- Direct messages (high priority)
- Mentions and replies (high priority)
- Follow notifications (medium priority)
- Engagement: likes, retweets, quotes (low priority)
- Business/analytics notifications (medium priority)

### 3. Write Summary
Create a summary in `vault/Briefings/TWITTER_Summary_YYYYMMDD.md` with:
- Total notification count
- DMs and mentions requiring response
- Engagement metrics (likes, retweets, impressions)
- Top performing content
- Recommended actions

### 4. Log the Action
```json
{
  "timestamp": "ISO-8601",
  "action_type": "twitter_summary_generated",
  "actor": "claude_code",
  "result": "success"
}
```
