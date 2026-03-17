---
name: reddit-commenter
description: A skill for writing natural and valuable comments on Reddit communities. Includes the complete workflow from subreddit exploration, comment writing, review, posting, to tracking.
license: MIT
---

# Reddit Commenter Skill

> Reddit Comment Automation - From Exploration to Posting and Tracking

---

## Required Tool: Playwright MCP

This skill uses **Playwright MCP** to interact with Reddit.

### Main MCP Tools
| MCP Tool | Purpose |
|----------|---------|
| `browser_navigate` | Navigate to Reddit pages |
| `browser_snapshot` | Capture page structure (accessibility tree) |
| `browser_click` | Click elements (comment box, buttons, etc.) |
| `browser_type` | Input text (comment content) |
| `browser_wait_for` | Wait for page loading |

### ⚠️ Important Notes When Using Playwright MCP
- **Minimize tokens**: When calling MCP, don't pass entire conversation context—only concisely summarize the essential information needed for that action
- **Direct navigation**: Navigate directly to URLs with `browser_navigate` rather than clicking elements (prevents click errors, saves tokens)
- **Concise instructions**: Pass only minimal instructions like "Navigate to [URL]", "Click [element]", "Type: [text]"
- **⚠️ No screenshots**: Do NOT use `browser_take_screenshot`. Always use only `browser_snapshot` for page verification (accessibility tree is sufficient and doesn't save files)

---

## Execution Workflow

### Step 1: Check Activity Status and Select Subreddit

```
1. Check today's date file in tracking/reddit/ folder
   → File name: YYYY-MM-DD.md (e.g., 2026-01-12.md)
   → If file doesn't exist, create new one referencing template.md

2. Check activity status table by subreddit:
   - How many comments posted in each subreddit today
   - Check subreddits under daily limit (3)
   - Check last comment time (minimum 5-10 minute intervals)

3. Select next subreddit for commenting:
   - Prioritize subreddits with no activity today or under limit
   - Prioritize subreddits with oldest last activity time

4. Check subreddit specifics in resources/subreddits.md:
   - Core community rules
   - Community nature
   - Good topics to answer
   → Reflect this information when selecting posts
```

### Step 2: Access Reddit and Explore Posts

```
1. Access Reddit with Playwright MCP
   → browser_navigate("https://www.reddit.com/r/{selected_subreddit}/new/")
   or
   → browser_navigate("https://www.reddit.com/r/{selected_subreddit}/rising/")

2. Page snapshot
   → browser_snapshot()

3. Criteria for selecting posts to comment on:
   • Posts where you can share insights or provide feedback
   • ⚠️ CRITICAL: Posts you haven't commented on today
     - Check activity log in tracking/reddit/today's-date.md file
     - Extract list of post URLs from today's comments
     - Verify selected post URL is NOT in that list
     - Absolutely NO duplicate comments on same post
   • OK even if not related to your service/field
   • Relevance to "good topics to answer" from Step 1
   • Avoid posts with already hundreds of comments

4. Secure URL of selected post
   → Check and record post link in snapshot
   → Navigate directly to this URL in next Step
```

### Step 3: Deep Analysis of Post Content and Existing Comments

```
⚠️ CRITICAL: Must perform this step before writing comment

0. Navigate directly to post
   → browser_navigate(post URL secured in Step 2)
   → Navigate directly to URL, don't click on post (prevents click errors)
   → browser_snapshot()

1. Read post content accurately:
   - Understand what OP is actually asking
   - Don't react only to keywords—understand full context
   - Distinguish between hypothetical questions and actual problem complaints

2. Understand OP's intent:
   - Seeking specific help? (problem solving)
   - Seeking opinions/discussion? (hypothetical scenario)
   - Information sharing? (experience story)

3. Analyze existing comments:
   - Check how others interpreted
   - Understand how community is receiving this post
   - Check tone and answering style

4. Decide comment direction:
   - Is this post worth answering?
   - From what angle should I answer?
   - Can I naturally answer in my style?

5. ⚠️ CRITICAL: Determine if site/link verification needed:
   - Did OP provide website/app link?
   - Are there expressions like "feedback requested", "honest feedback", "looking for feedback"?
   - Is feedback requested on UX, design, performance that requires actual verification?

   → If YES:
     • Visit actual site with browser_navigate(provided link)
     • Check UI/UX with browser_snapshot()
     • Write feedback based ONLY on what you actually saw
     • Absolutely NO speculative feedback on things you didn't see

   → If NO:
     • Can answer from post content alone
     • General advice or experience sharing

⚠️ Proceed to Step 4 only after clearly verifying analysis results
```

### Step 4: Write Comment

```
1. Draft comment based on Step 3 analysis results:
   - Answer matching OP's actual question
   - Practically helpful content
   - Match subreddit tone
   - Focus on 1-2 points (don't try to explain everything)
```

### Step 5: Personalization Review (Loop)

```
1. Check resources/personalization_reddit.md file
   → Sequentially check 16 personalization checklist items based on actual comment style
   → Especially important: #4 personal experience, #13 experience pattern, #15 question intent understanding, #16 site verification

2. Check style patterns:
   • Which pattern (1-8) is it closest to?
   • Does it capture that pattern's characteristics well?
   • Does it look like you wrote it?

3. Review process:
   • All items PASS → Proceed to Step 6
   • Any violation → Revise comment and re-review from Step 5 beginning

```

**Detailed personalization guide**: See `resources/personalization_reddit.md`

### Step 6: Post Comment

```
1. Click comment input box
   → Check comment input element after browser_snapshot()
   → browser_click(comment box ref)

2. Input comment content
   → browser_type(reviewed comment)

3. Click post button
   → browser_click(post button ref)

4. Secure comment URL
   → Copy comment permalink after posting
```

### Step 7: Judge Potential Customer (Optional)

```
⚠️ CRITICAL: Judge accurately by referring to Step 3 analysis again

→ Refer to "Lead Selection Criteria" in leads/reddit.md
→ Classify as lead only users with actual problems (not hypothetical questions)

When lead discovered, update leads/reddit.md:
  - Username, subreddit, post URL
  - Post summary, selection reason, relevance
```

### Step 8: Update Tracking

```
Update tracking/reddit/[today's-date].md file:

1. Activity status table by subreddit:
   - Increment comment count for that subreddit by +1
   - Update last comment time

2. Add to activity log:
   ### [HH:MM] r/subreddit
   - **Post**: [Title](URL)
   - **Topic Summary**: One-line summary of post content
   - **Comment Link**: [Comment URL]
   - **Comment Content**:
   ```
   Full comment written
   ```

3. When potential customer discovered:
   - Update 'leads/reddit.md' when potential customer discovered
```

---

## File Reference Rules (Token Savings)

| File | Reference Timing |
|------|------------------|
| `resources/subreddits.md` | Step 1 (subreddit selection) |
| `resources/personalization_reddit.md` | Step 5 (review) |
| `resources/product.md` | Step 7 (potential customer judgment) |
| `leads/reddit.md` | Step 7 (lead criteria check) |

→ Reference only at relevant Step, don't read in advance

---

## Cautions

1. **Login Required**: Check Reddit account login status
2. **Rate Limiting**: Too fast activity risks account restrictions
3. **Community Rules**: Must follow each subreddit's rules
4. **Spam Prevention**: Absolutely NO copy-pasting same content
5. **Review Required**: Rewrite if any checklist item violated
6. **⚠️ Step 3 Required**: NEVER write comment without analyzing post content. Judging only by keywords can cause serious errors
7. **⚠️ Minimize Playwright MCP tokens**:
   - Don't pass entire context when calling Playwright MCP
   - Concisely summarize only essential information needed for each MCP call
   - E.g.: Only minimal instructions like "Navigate to [URL]", "Click comment box", "Type: [text]"
   - Prevent errors from excessive input tokens
8. **⚠️ Post Navigation**: Use browser_navigate directly with URL instead of clicking post (prevents click errors)
