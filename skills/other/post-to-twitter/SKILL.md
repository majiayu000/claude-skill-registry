# post-to-twitter Skill

---
name: post-to-twitter
description: Manage Twitter/X presence with tweets and threads. Create concise, engaging content optimized for Twitter's format. Support single tweets (280 chars) and multi-tweet threads. Track engagement and build thought leadership. Use when user mentions "post to twitter", "tweet", "create thread", "share on x", "twitter post".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
context: fork
---

## Purpose

Automate Twitter/X content creation for professional thought leadership and engagement. This skill generates platform-optimized tweets and threads that maintain brand voice, follow Twitter best practices, and require human approval before publishing.

## When to Use This Skill

This skill activates when:
- User asks to "post to Twitter" or "tweet this"
- Creating thread content for deeper insights
- Sharing quick updates or industry commentary
- Building thought leadership on Twitter
- Engaging with tech/business Twitter community
- User mentions "twitter", "tweet", "x post", "thread"

## Workflow Overview

```
Business_Goals.md → Content Type Selection → Tweet vs Thread
        ↓                    ↓                      ↓
Twitter Guidelines → Drafting → Optimization (280 char)
        ↓                    ↓                      ↓
Hashtag Strategy → Final Tweet(s) → Approval Request
        ↓                    ↓                      ↓
Human Approval → Twitter Publishing → Engagement Tracking
```

## Twitter Platform Characteristics

### Key Differences from Other Platforms
- **Character Limit:** 280 characters (brevity is critical)
- **Optimal Length:** 71-100 characters (highest engagement)
- **Hashtags:** 1-2 maximum (unlike Instagram's 5-10)
- **Threading:** Multi-tweet threads for longer content
- **Speed:** Real-time, fast-paced, conversational
- **Audience:** Tech-savvy, professional, fast scrollers

### Content Performance Insights
- **Tweets:** Short, punchy tweets (< 100 chars) perform best
- **Threads:** Deep-dive content gets more engagement than links
- **Visual Tweets:** Images/GIFs increase engagement 35%
- **Questions:** Direct questions get 3x more replies
- **Timing:** Weekday mornings and early afternoons peak

---

## Step-by-Step Process

### Phase 1: Content Discovery & Format Selection

**Objective:** Identify content and determine if single tweet or thread.

1. **Read Business_Goals.md**
   ```bash
   # Location: Vault/Business_Goals.md
   # Look for: Twitter strategy, content themes, target audience
   ```
   - Identify current business priorities
   - Check Twitter-specific goals (follower growth, engagement targets)
   - Note voice/tone preferences

2. **Scan Recent Completed Tasks**
   ```bash
   # Location: Vault/Done/
   # Pattern: Quick wins, insights, interesting learnings
   ```
   - Look for tweetable moments (quick insights)
   - Find thread-worthy topics (complex ideas)
   - Identify controversial or hot takes

3. **Check Explicit Content Requests**
   ```bash
   # Location: Vault/Needs_Action/
   # Pattern: Twitter post requests
   ```
   - Extract specific topic or angle
   - Note if user requested tweet or thread
   - Identify any linked resources

4. **Format Decision Logic**

   Use [twitter-guidelines.md](./reference/twitter-guidelines.md):

   **Choose Single Tweet when:**
   - Content is simple, one clear idea
   - Quick insight, tip, or observation
   - Sharing a link with commentary
   - Engaging with trending topic
   - Maximum 280 characters sufficient

   **Choose Thread when:**
   - Complex idea requiring multiple points
   - Step-by-step tutorial or guide
   - Storytelling with narrative arc
   - In-depth analysis or commentary
   - Content exceeds 280 characters meaningfully

**Output:** Format selected (tweet or thread), content theme identified

---

### Phase 2: Content Generation (Twitter-Optimized)

**Objective:** Create engaging, concise content within Twitter constraints.

#### For Single Tweets

1. **Select Tweet Template**

   Refer to [twitter-guidelines.md](./reference/twitter-guidelines.md):

   - **Insight/Tip:** Share valuable knowledge in < 100 chars
   - **Hot Take:** Controversial but defensible opinion
   - **Question:** Spark conversation with direct question
   - **Announcement:** Brief update or news
   - **Quote + Commentary:** Share quote with your take

2. **Draft Tweet Content**

   **Optimal Structure (71-100 characters):**
   ```
   [Hook or statement]

   [Optional: Link or CTA]
   [Optional: 1-2 hashtags]
   ```

   **Extended Structure (100-280 characters):**
   ```
   [Hook or opening statement]

   [Elaboration or context]

   [Call-to-action or link]
   [Optional: 1-2 hashtags]
   ```

   **Twitter Voice Guidelines:**
   - Direct and conversational
   - No fluff or filler words
   - Active voice preferred
   - Sentence fragments acceptable
   - Personality over polish

3. **Character Count Optimization**

   **Priority:**
   1. Core message: 50-100 chars
   2. Link (if needed): 23 chars (auto-shortened)
   3. Hashtags (1-2): 10-20 chars
   4. **Total Target:** 71-100 chars (sweet spot)

   **If over 280 chars:** Convert to thread (Phase 2B)

#### For Tweet Threads

1. **Select Thread Template**

   Refer to [thread-templates.md](./reference/thread-templates.md):

   - **Tutorial/How-To:** Step-by-step guide (3-7 tweets)
   - **Storytelling:** Narrative with beginning, middle, end (4-10 tweets)
   - **Listicle:** Numbered list of insights (5-10 tweets)
   - **Deep Dive:** In-depth analysis (5-12 tweets)
   - **Hot Take + Justification:** Opinion + supporting points (3-5 tweets)

2. **Draft Thread Structure**

   **Tweet 1 (Hook Thread):**
   ```
   [Attention-grabbing hook]

   [Brief preview of what's coming]

   [Optional: "A thread 🧵" or "Let me explain 👇"]
   ```

   **Tweets 2-N (Content Tweets):**
   ```
   [Point/step with clear value]

   [Brief elaboration if needed]

   [Natural transition to next tweet]
   ```

   **Final Tweet (CTA/Conclusion):**
   ```
   [Summary or key takeaway]

   [Call-to-action: Follow, Retweet, Comment]

   [Optional: Link to related resource]
   ```

3. **Thread Best Practices**

   - **Length:** 3-10 tweets optimal (over 15 loses readers)
   - **Numbering:** Use "1/" "2/" etc. for clarity
   - **Flow:** Each tweet must make sense standalone
   - **Pacing:** Vary tweet length (some short, some longer)
   - **Hook Strong:** First tweet determines if thread gets read

4. **Hashtag Strategy**

   Use [hashtag-strategy.md](./reference/hashtag-strategy.md):

   **Twitter-Specific Rules:**
   - **Maximum:** 1-2 hashtags per tweet
   - **Placement:** End of tweet only
   - **Selection:** Broad, trending, or branded only
   - **Thread Placement:** Only on first or last tweet, not all

   **Examples:**
   - #AI #ProductivityTips
   - #Startups #EntrepreneursLife
   - #TechTwitter #BuildInPublic

   **Note:** Twitter hashtags are less critical than Instagram. Focus on content quality over hashtag quantity.

**Output:** Tweet or thread drafted, character counts verified

---

### Phase 3: Quality Review & Validation

**Objective:** Ensure content meets Twitter and brand standards.

1. **Twitter-Specific Checklist**

   **Single Tweet:**
   - [ ] Character count: 71-280 (optimal: 71-100)
   - [ ] Clear message without jargon
   - [ ] No typos or errors
   - [ ] Links shortened (if applicable)
   - [ ] Hashtags: 0-2 maximum
   - [ ] Engaging (question, insight, or call-to-action)

   **Thread:**
   - [ ] First tweet hooks attention
   - [ ] 3-10 tweets total (not too long)
   - [ ] Each tweet standalone makes sense
   - [ ] Numbered clearly (1/7, 2/7, etc.)
   - [ ] Natural flow between tweets
   - [ ] Strong conclusion with CTA
   - [ ] Hashtags only on first/last tweet

2. **Brand Compliance Check**

   Reference `Vault/Company_Handbook.md`:
   - [ ] Aligns with brand voice
   - [ ] No prohibited topics
   - [ ] Professional but conversational
   - [ ] No offensive language
   - [ ] Respectful of others

3. **Engagement Optimization**

   Reference [engagement-tactics.md](./reference/engagement-tactics.md):
   - [ ] Includes question or conversation starter (if applicable)
   - [ ] Personality or opinion evident
   - [ ] Value-driven (insight, tip, story)
   - [ ] Optimal posting time considered
   - [ ] No excessive self-promotion

**Output:** Validated tweet/thread ready for approval

---

### Phase 4: Approval Request Creation

**Objective:** Create formal approval request for human review.

1. **Integrate with handle-approval Skill**

   This skill MUST use the `handle-approval` skill for approval requests.

   Reference: [../../handle-approval/reference/approval-thresholds.md](../../handle-approval/reference/approval-thresholds.md)

2. **Create Approval File**

   ```markdown
   ---
   type: approval_request
   action: social_media_post
   platform: twitter
   content_type: [tweet|thread]
   created: [timestamp ISO 8601]
   expires: [72 hours from creation]
   priority: normal
   status: pending
   ---

   ## Action Summary
   Publish Twitter [tweet/thread]: [One-line description]

   ## Twitter Content

   ### [Single Tweet] OR [Thread]

   **Tweet 1:**
   [Tweet content]
   Character count: [X/280]

   [If thread, continue:]
   **Tweet 2:**
   [Tweet content]
   Character count: [X/280]

   **Tweet 3:**
   [Tweet content]
   Character count: [X/280]

   [... additional tweets ...]

   **Tweet N (Final):**
   [Tweet content]
   Character count: [X/280]

   ---

   ## Metadata
   - **Platform:** Twitter/X
   - **Type:** [Single Tweet / Thread]
   - **Thread Length:** [If thread: X tweets]
   - **Total Character Count:** [Sum of all tweets]
   - **Hashtags:** [List hashtags used]
   - **Mentions:** [Any @mentions]
   - **Links:** [Any URLs included]

   ## Context & Rationale
   - **Content Source:** [Insight / Project / Industry commentary]
   - **Business Goal:** [Thought leadership / Engagement / Brand awareness]
   - **Target Audience:** [Tech community / Entrepreneurs / Industry peers]
   - **Inspiration:** [What prompted this tweet/thread]

   ## Posting Schedule
   - **Optimal Times:** Weekdays 8-10 AM, 12-1 PM, 5-6 PM
   - **Suggested Time:** [Specific time if scheduled]

   ## Risks & Considerations
   - Risk: Low (standard business content)
   - Compliance: Follows Twitter guidelines and brand voice
   - Controversy: [None / Low / Intentional hot take - explain]

   ## To Approve
   Move this file to `/Approved` folder.

   ## To Reject
   Move this file to `/Rejected` folder and add reason at bottom.

   ---
   ## Human Edits (Optional)
   [Space for human to edit tweet content before approval]
   ```

3. **File Naming Convention**
   ```
   APPROVAL_TWITTER_[TWEET|THREAD]_[description]_[YYYY-MM-DD].md

   Examples:
   - APPROVAL_TWITTER_TWEET_AIProductivityTip_2026-01-11.md
   - APPROVAL_TWITTER_THREAD_AutomationTutorial_2026-01-11.md
   - APPROVAL_TWITTER_TWEET_WeeklyInsight_2026-01-11.md
   ```

4. **Save to Pending Approval Folder**
   ```bash
   # Location: Vault/Pending_Approval/
   ```

**Output:** Approval request file created in /Pending_Approval

---

### Phase 5: Dashboard Logging

**Objective:** Maintain audit trail and activity log.

Update `Vault/Dashboard.md`:

```markdown
## Recent Activity

- [YYYY-MM-DD HH:MM:SS] **Twitter [Tweet/Thread] Created**
  - Type: [Single Tweet / Thread (X tweets)]
  - Topic: [Brief description]
  - Character Count: [Total characters]
  - Status: Pending Approval
  - Approval File: APPROVAL_TWITTER_[...]_[date].md
  - Action: Human review required in /Pending_Approval
```

**Output:** Dashboard updated with pending post status

---

### Phase 6: Post-Approval Execution

**Note:** Executes ONLY after human moves approval file to `/Approved` folder.

1. **Detect Approved Post**
   ```bash
   # Monitor: Vault/Approved/
   # Pattern: APPROVAL_TWITTER_*.md
   ```

2. **Execute Twitter Publishing**

   ```bash
   python scripts/twitter_api_helper.py --approval-file "Vault/Approved/APPROVAL_TWITTER_xxx.md"
   ```

   The script will:
   - Extract tweet/thread content
   - Authenticate with Twitter API v2
   - Publish tweet(s) in sequence (for threads)
   - Return tweet URL(s) and status

3. **Handle Execution Results**

   **If Success:**
   - Move approval file from `/Approved` to `/Done`
   - Update Dashboard with success log and tweet URL(s)
   - Initialize engagement tracking file

   **If Failure:**
   - Keep file in `/Approved`
   - Log error to Dashboard with details
   - Create troubleshooting task in /Needs_Action

4. **Engagement Tracking Setup**

   Create tracking file:
   ```markdown
   # /Vault/Social_Media/Twitter/Analytics/TWEET_[date]_[topic].md

   ---
   platform: twitter
   type: [tweet|thread]
   tweet_url: [Primary tweet URL]
   published: [timestamp]
   ---

   ## Initial Metrics (24h)
   - Impressions: [TBD]
   - Engagements: [TBD]
   - Retweets: [TBD]
   - Likes: [TBD]
   - Replies: [TBD]
   - Profile Clicks: [TBD]

   ## Week Performance (7d)
   [To be updated after 7 days]
   ```

5. **Final Dashboard Update**
   ```markdown
   - [YYYY-MM-DD HH:MM:SS] **Twitter [Tweet/Thread] Published** ✓
     - Type: [Single Tweet / Thread (X tweets)]
     - Topic: [Brief description]
     - Tweet URL: [URL]
     - Status: Complete
     - Tracking: /Social_Media/Twitter/Analytics/TWEET_[date]_[topic].md
   ```

**Output:** Tweet/thread published and engagement tracking initiated

---

## Integration with Other Skills

### Required Dependencies

1. **handle-approval Skill** (Gold Branch 1)
   - MUST be used for all approval request creation
   - Enforces security thresholds
   - Manages expiration policies

### Optional Integrations

2. **create-plan Skill** (Silver Tier)
   - Use for thread planning and structuring
   - Break down complex topics into thread format

3. **process-tasks Skill** (Bronze Tier)
   - Process explicit Twitter post requests from /Needs_Action

---

## Security & Safety Protocols

### Never Auto-Approve

- ALL Twitter posts REQUIRE human approval (zero exceptions)
- Twitter is public, permanent, and highly visible
- Brand reputation risk is HIGH
- Threads especially need review (longer content = more risk)
- Approval expiration: 72 hours (3 days)

### Content Validation Required

Before creating approval request:
- [ ] No confidential business information
- [ ] No client names without permission
- [ ] No controversial content unless intentional (and approved strategy)
- [ ] No negative comments about competitors
- [ ] Professional and respectful language
- [ ] No excessive self-promotion (80/20 rule: 80% value, 20% promo)
- [ ] Twitter community guidelines compliant

### Rate Limiting

From `Business_Goals.md` (adjust as needed):
- **Single Tweets:** 3-5 per week maximum
- **Threads:** 1-2 per week maximum (more effort to read)
- **Minimum Spacing:** 4-6 hours between tweets
- **Optimal Frequency:** Daily or every other day

---

## Error Handling

### Common Issues

1. **Character Count Exceeds 280**
   - Action: Either shorten or convert to thread
   - Template: Use thread template
   - Ask: User preference on shortening vs threading

2. **Business_Goals.md Missing Twitter Strategy**
   - Action: Alert user to define Twitter goals
   - Fallback: Use general tech/business audience assumptions
   - Default: Conservative posting frequency (2-3x/week)

3. **Twitter API Authentication Failure**
   - Action: Log error with details
   - Alert: Create task in /Needs_Action for token refresh
   - Guidance: Link to Twitter Developer Console

4. **Thread Too Long (> 15 tweets)**
   - Action: Suggest shortening or splitting into multiple threads
   - Reason: Long threads lose readers
   - Optimal: 5-7 tweets per thread

---

## Testing & Validation

### Dry-Run Mode

The Twitter API helper script supports dry-run:
```bash
python scripts/twitter_api_helper.py --dry-run --approval-file "path/to/file.md"
```

This will:
- Parse approval file
- Validate character counts
- Show what would be posted
- NOT publish to Twitter

### Success Criteria

- [ ] Tweet(s) drafted correctly
- [ ] Character counts within limits (280 per tweet)
- [ ] Hashtag strategy appropriate (1-2 max)
- [ ] Thread flow logical (if thread)
- [ ] Approval request in correct format
- [ ] Dashboard logging complete
- [ ] Content passes quality checklist

---

## Trigger Phrases for Auto-Activation

This skill activates when user says:
- "post to twitter"
- "tweet this"
- "share on twitter"
- "create a tweet"
- "create a thread"
- "twitter thread about [topic]"
- "post on x"
- "tweet about [topic]"

---

## Reference Files

- [Twitter Guidelines](./reference/twitter-guidelines.md) - Platform best practices, tweet templates
- [Thread Templates](./reference/thread-templates.md) - Multi-tweet thread structures
- [Hashtag Strategy](./reference/hashtag-strategy.md) - Twitter-specific hashtag usage
- [Engagement Tactics](./reference/engagement-tactics.md) - Optimization for replies and engagement

---

## Examples

### Example 1: Single Tweet (Quick Tip)

```
User: "Tweet about the productivity hack I discovered today"

Skill Actions:
1. Reviews recent Done/ tasks for productivity-related content
2. Selects "Insight/Tip" tweet template
3. Drafts concise tweet (85 characters):
   "Automation isn't lazy. It's choosing to solve a problem once instead of daily."
4. Adds 1 hashtag: #ProductivityTips
5. Creates APPROVAL_TWITTER_TWEET_AutomationInsight_2026-01-11.md
6. Logs to Dashboard
7. Waits for human approval
8. Posts to Twitter after approval
```

### Example 2: Thread (Tutorial)

```
User: "Create a Twitter thread explaining how to set up Claude Code automation"

Skill Actions:
1. Selects "Tutorial/How-To" thread template
2. Structures 7-tweet thread:
   - Tweet 1: Hook + promise
   - Tweets 2-6: Step-by-step instructions
   - Tweet 7: Conclusion + CTA
3. Numbers tweets (1/7, 2/7, etc.)
4. Keeps each tweet 150-250 characters
5. Adds #ClaudeCode #Automation to first tweet only
6. Creates APPROVAL_TWITTER_THREAD_ClaudeCodeSetup_2026-01-11.md
7. Human reviews, makes minor edits, approves
8. Posts thread to Twitter (with 5-second delay between tweets)
9. Tracks engagement
```

### Example 3: Hot Take (Controversial Opinion)

```
User: "Tweet my opinion that most SaaS tools are over-engineered"

Skill Actions:
1. Recognizes controversial/opinion content
2. Selects "Hot Take" template
3. Drafts tweet (142 characters):
   "Unpopular opinion: 90% of SaaS tools are over-engineered. Most businesses need 10% of the features they pay for.

   Simplicity > feature bloat."
4. No hashtags (hot takes work better without)
5. Creates approval request with "Risk: Medium - Intentional hot take" note
6. Human reviews, confirms stance, approves
7. Posts and monitors replies for engagement
```

---

## Notes

### Twitter Character Limits
- **Single Tweet:** 280 characters
- **Username Mentions:** Count toward 280
- **Links:** Auto-shortened to 23 characters (t.co)
- **Images/GIFs:** Don't count toward character limit
- **Polls:** Separate format, not covered in this skill yet

### Thread Best Practices
- Hook within first 5 words
- Use line breaks for readability (double return)
- Vary tweet length (some short, some longer)
- Number clearly (1/7, 2/7, etc.)
- Strong CTA in final tweet
- Engage with replies quickly

### Engagement Tips
- Ask questions (gets 3x more replies)
- Reply to all comments within first hour
- Retweet relevant replies
- Quote tweet for commentary
- Use Twitter Lists to monitor industry conversations

---

*Skill Version: 1.0*
*Created: 2026-01-11*
*Branch: feat/gold-social-expansion*
*Dependencies: handle-approval (Gold Branch 1)*
