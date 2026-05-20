# post-to-social-media Skill

---
name: post-to-social-media
description: Manage Facebook and Instagram business presence. Create and schedule posts, generate platform-optimized content, track engagement. Handles both text and visual content for community building and brand awareness. Use when user mentions "post to facebook", "post to instagram", "social media", "facebook post", "instagram post", or when scheduling content across multiple platforms.
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
context: fork
---

## Purpose

Automate Facebook and Instagram content creation for multi-platform social media presence. This skill generates platform-optimized posts that maintain brand consistency, follow platform-specific best practices, and require human approval before publishing.

## When to Use This Skill

This skill activates when:
- User asks to "post to Facebook" or "post to Instagram"
- Creating content for community engagement
- Sharing business updates across multiple platforms
- Building brand awareness visually (Instagram) or through community (Facebook)
- Cross-posting content with platform optimization
- Scheduling regular social media updates
- Promoting services, achievements, or behind-the-scenes content

## Workflow Overview

```
Business_Goals.md → Platform Selection → Content Type
        ↓                    ↓                ↓
Platform Guidelines → Content Generation → Image Selection
        ↓                    ↓                ↓
Hashtag Strategy → Optimization → Approval Request
        ↓                    ↓                ↓
Human Approval → Multi-Platform Publishing → Engagement Tracking
```

## Platform Differences (Critical)

### Facebook
- **Optimal Length:** 40-80 words (can go longer for stories)
- **Hashtags:** 1-2 hashtags (low usage, not critical)
- **Focus:** Community engagement, conversation starters
- **Best Times:** Tuesday-Thursday 1-4 PM, Saturday 12-1 PM
- **Content Style:** Conversational, community-focused, discussion prompts
- **Character Limit:** 63,206 (but shorter performs better)

### Instagram
- **Optimal Length:** Short captions (125-150 characters for feeds) or longer storytelling
- **Hashtags:** 5-10 relevant hashtags (critical for discovery)
- **Focus:** Visual storytelling, aesthetic consistency
- **Best Times:** Monday/Wednesday 11 AM-1 PM, Friday 10-11 AM
- **Content Style:** Visual-first, aspirational, behind-the-scenes
- **Character Limit:** 2,200 for captions

**Key Insight:** NEVER create identical content for both platforms. Each requires platform-specific optimization.

---

## Step-by-Step Process

### Phase 1: Content Discovery & Platform Selection

**Objective:** Identify content-worthy activities and determine optimal platform(s).

1. **Read Business_Goals.md**
   ```bash
   # Location: Vault/Business_Goals.md
   # Look for: Active projects, target audience, content themes
   ```
   - Identify current business priorities
   - Check social media goals (engagement targets, brand awareness)
   - Note preferred content types

2. **Scan Recent Completed Tasks**
   ```bash
   # Location: Vault/Done/
   # Pattern: Visual-worthy achievements, team activities, client projects
   ```
   - Look for visually interesting content (Instagram)
   - Find conversation starters or community-relevant topics (Facebook)
   - Identify behind-the-scenes moments

3. **Check Explicit Content Requests**
   ```bash
   # Location: Vault/Needs_Action/
   # Pattern: Social media post requests
   ```
   - Extract platform preference (Facebook, Instagram, or both)
   - Note any specific images or angles requested

4. **Platform Selection Logic**

   Use [platform-selection.md](./reference/platform-selection.md):

   **Choose Facebook when:**
   - Content sparks discussion or community engagement
   - Sharing longer-form stories or updates
   - Targeting local community or specific groups
   - Text-heavy content with minimal visual requirements

   **Choose Instagram when:**
   - Content is highly visual (product shots, workspace, team photos)
   - Targeting younger or design-conscious audience
   - Building aesthetic brand consistency
   - Showcasing portfolio work or creative process

   **Choose Both when:**
   - Major announcements or milestones
   - Content works well visually AND as discussion starter
   - Maximizing reach across different audiences
   - *Note: MUST create platform-specific versions*

**Output:** Platform(s) selected, content theme identified

---

### Phase 2: Content Generation (Platform-Optimized)

**Objective:** Create engaging, platform-specific content.

#### For Facebook Posts

1. **Select Facebook Template**

   Refer to [facebook-guidelines.md](./reference/facebook-guidelines.md):

   - **Community Question:** Spark discussion with open-ended question
   - **Behind-the-Scenes:** Share process, team culture, work environment
   - **Milestone Celebration:** Achievements with community appreciation
   - **Value/Tip Share:** Helpful advice or industry insights
   - **Event/Announcement:** Business updates, launches, events

2. **Draft Facebook Content**

   Structure (40-80 words optimal):
   ```markdown
   [Hook - question or relatable statement]

   [Context - brief story or background]

   [Call-to-Action - encourage comments/shares]

   #hashtag1 #hashtag2 (optional, max 2)
   ```

   **Facebook Voice Guidelines:**
   - Conversational and friendly
   - Ask questions to encourage comments
   - Use personal pronouns (we, our, you)
   - Create sense of community
   - Authentic and approachable

#### For Instagram Posts

1. **Select Instagram Template**

   Refer to [instagram-guidelines.md](./reference/instagram-guidelines.md):

   - **Visual Showcase:** Portfolio work, product shots, design
   - **Carousel Story:** Multi-image narrative or tutorial
   - **Motivational Quote:** Branded quote graphic with caption
   - **Behind-the-Scenes:** Candid workspace, process shots
   - **User-Generated Content:** Client results, testimonials (with permission)

2. **Draft Instagram Caption**

   Structure (flexible length):
   ```markdown
   [Visual Description OR Hook] (emojis acceptable)

   [Story/Value - 2-4 sentences]

   [Call-to-Action - tag friends, save post, visit link in bio]

   •
   •
   •
   #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
   #hashtag6 #hashtag7 #hashtag8 (5-10 total)
   ```

   **Instagram Voice Guidelines:**
   - Visual-first (caption complements image)
   - Emojis acceptable and encouraged (2-5)
   - Line breaks for readability (use • • • separator before hashtags)
   - Storytelling or inspirational tone
   - Strategic hashtag use for discovery

3. **Hashtag Strategy**

   Use [hashtag-library.md](./reference/hashtag-library.md):

   **Facebook:** 1-2 broad hashtags (low priority)
   - Example: #SmallBusiness #Entrepreneurship

   **Instagram:** 5-10 mix of sizes (critical)
   - 2-3 niche hashtags (10K-100K posts) - your specific industry
   - 3-4 medium hashtags (100K-500K posts) - broader topics
   - 1-2 popular hashtags (1M+ posts) - discovery
   - Always include your branded hashtag
   - Example: #FreelanceDesigner #BrandIdentity #DesignProcess #CreativeStudio #SmallBusinessDesign #GraphicDesign

**Output:** Platform-specific drafted content with hashtags

---

### Phase 3: Visual Content Planning

**Objective:** Identify or specify required images/graphics.

1. **Image Requirements Check**

   **Facebook:**
   - Optional but recommended (2-3x higher engagement)
   - Recommended size: 1200x630px (link previews)
   - Formats: JPG, PNG, GIF

   **Instagram:**
   - REQUIRED (visual-first platform)
   - Feed post: 1080x1080px (square) or 1080x1350px (portrait)
   - Carousel: Multiple 1080x1080px images
   - Formats: JPG, PNG

2. **Image Source Identification**

   Check in priority order:
   ```bash
   # 1. Vault/Social_Media/Images/ - pre-approved images
   # 2. Vault/Projects/[project-name]/ - project screenshots
   # 3. Request from user - if no suitable image found
   ```

3. **Image Optimization**

   If image found, use image optimizer:
   ```bash
   python scripts/image_optimizer.py --input "path/to/image.jpg" --platform [facebook|instagram]
   ```

   The optimizer will:
   - Resize to platform-optimal dimensions
   - Compress for fast loading (< 1MB)
   - Add subtle branding if configured
   - Output to `/Vault/Social_Media/[Platform]/Ready/`

4. **Image Requirement Documentation**

   If no suitable image available:
   - Include in approval request: "IMAGE REQUIRED: [description]"
   - Suggest image type or content
   - Provide reference examples if applicable

**Output:** Image identified/optimized OR image requirement documented

---

### Phase 4: Quality Review & Validation

**Objective:** Ensure content meets platform and brand standards.

1. **Platform-Specific Checklist**

   **Facebook:**
   - [ ] Length: 40-80 words (can be longer if storytelling)
   - [ ] Includes question or call-to-action
   - [ ] Conversational and community-focused
   - [ ] Hashtags: 0-2 (not critical)
   - [ ] No excessive emojis (0-2)

   **Instagram:**
   - [ ] Caption complements visual content
   - [ ] Hashtags: 5-10 relevant tags
   - [ ] Line breaks for readability
   - [ ] Emojis used appropriately (2-5)
   - [ ] Image requirement specified OR image attached
   - [ ] Visual-first approach maintained

2. **Brand Compliance Check**

   Reference `Vault/Company_Handbook.md`:
   - [ ] Aligns with brand voice
   - [ ] No prohibited topics
   - [ ] Professional standards maintained
   - [ ] Client confidentiality respected
   - [ ] No negative commentary about competitors

3. **Engagement Optimization**

   Reference [engagement-rules.md](./reference/engagement-rules.md):
   - [ ] Clear call-to-action included
   - [ ] Encourages saves, shares, or comments
   - [ ] Optimal posting time considered
   - [ ] Platform best practices followed

**Output:** Validated content ready for approval request

---

### Phase 5: Approval Request Creation

**Objective:** Create formal approval request for human review.

1. **Integrate with handle-approval Skill**

   This skill MUST use the `handle-approval` skill for approval requests.

   Reference: [../../handle-approval/reference/approval-thresholds.md](../../handle-approval/reference/approval-thresholds.md)

2. **Create Approval File**

   ```markdown
   ---
   type: approval_request
   action: social_media_post
   platform: [facebook|instagram|both]
   created: [timestamp ISO 8601]
   expires: [72 hours from creation]
   priority: normal
   status: pending
   ---

   ## Action Summary
   Publish social media post: [One-line description]

   ## Platform
   **Target:** [Facebook / Instagram / Both (optimized separately)]

   ---

   ### Facebook Post Content
   [Full drafted Facebook post with minimal hashtags]

   **Metadata:**
   - Word Count: [X words]
   - Character Count: [X/63206]
   - Hashtags: [0-2]
   - Image: [Required/Optional/Attached]

   ---

   ### Instagram Post Content
   [Full drafted Instagram caption with hashtags]

   **Metadata:**
   - Caption Length: [X characters]
   - Hashtags: [5-10 listed]
   - Image: [Required - description OR attached path]
   - Format: [Square/Portrait/Carousel]

   ---

   ## Visual Content
   - **Status:** [Ready / Required / Pending]
   - **Image Path:** [If ready: path/to/optimized/image.jpg]
   - **Image Description:** [Brief description of visual content]
   - **Alt Text:** [Accessibility description]

   ## Context & Rationale
   - **Content Source:** [Project / Achievement / Daily Activity]
   - **Business Goal:** [Brand awareness / Engagement / Community building]
   - **Target Audience:** [Demographics and interests]

   ## Posting Schedule
   - **Facebook Optimal:** Tuesday-Thursday 1-4 PM, Saturday 12-1 PM
   - **Instagram Optimal:** Monday/Wednesday 11 AM-1 PM, Friday 10-11 AM
   - **Suggested Time:** [Specific time if scheduled]

   ## Risks & Considerations
   - Risk: Low (standard business update)
   - Compliance: Follows brand guidelines
   - Platform policies: Compliant

   ## To Approve
   Move this file to `/Approved` folder.

   ## To Reject
   Move this file to `/Rejected` folder and add reason at bottom.

   ---
   ## Human Edits (Optional)
   [Space for human to edit content or image selection before approval]
   ```

3. **File Naming Convention**
   ```
   APPROVAL_SOCIAL_[FB|IG|BOTH]_[description]_[YYYY-MM-DD].md

   Examples:
   - APPROVAL_SOCIAL_FB_TeamMilestone_2026-01-11.md
   - APPROVAL_SOCIAL_IG_ProductShowcase_2026-01-11.md
   - APPROVAL_SOCIAL_BOTH_MajorAnnouncement_2026-01-11.md
   ```

4. **Save to Pending Approval Folder**
   ```bash
   # Location: Vault/Pending_Approval/
   ```

**Output:** Approval request file created in /Pending_Approval

---

### Phase 6: Dashboard Logging

**Objective:** Maintain audit trail and activity log.

Update `Vault/Dashboard.md`:

```markdown
## Recent Activity

- [YYYY-MM-DD HH:MM:SS] **Social Media Post Created**
  - Platform: [Facebook / Instagram / Both]
  - Topic: [Brief description]
  - Image: [Ready / Required]
  - Status: Pending Approval
  - Approval File: APPROVAL_SOCIAL_[...]_[date].md
  - Action: Human review required in /Pending_Approval
```

**Output:** Dashboard updated with pending post status

---

### Phase 7: Post-Approval Execution

**Note:** Executes ONLY after human moves approval file to `/Approved` folder.

1. **Detect Approved Post**
   ```bash
   # Monitor: Vault/Approved/
   # Pattern: APPROVAL_SOCIAL_*.md
   ```

2. **Execute Platform Publishing**

   **For Facebook:**
   ```bash
   python scripts/facebook_api_helper.py --approval-file "Vault/Approved/APPROVAL_SOCIAL_FB_xxx.md"
   ```

   **For Instagram:**
   ```bash
   python scripts/instagram_api_helper.py --approval-file "Vault/Approved/APPROVAL_SOCIAL_IG_xxx.md"
   ```

   The scripts will:
   - Extract post content and image path
   - Authenticate with Facebook/Instagram Graph API
   - Publish the post(s)
   - Return post URLs and status

3. **Handle Execution Results**

   **If Success:**
   - Move approval file from `/Approved` to `/Done`
   - Update Dashboard with success log and post URLs
   - Initialize engagement tracking file in `/Social_Media/[Platform]/Analytics/`

   **If Failure:**
   - Keep file in `/Approved`
   - Log error to Dashboard with details
   - Create troubleshooting task in /Needs_Action

4. **Engagement Tracking Setup**

   Create tracking file:
   ```markdown
   # /Vault/Social_Media/[Platform]/Analytics/POST_[date]_[topic].md

   ---
   platform: [facebook|instagram]
   post_url: [URL]
   published: [timestamp]
   ---

   ## Initial Metrics (24h)
   - Likes: [TBD - check after 24h]
   - Comments: [TBD]
   - Shares/Saves: [TBD]
   - Reach: [TBD]

   ## Week Performance (7d)
   [To be updated after 7 days]
   ```

5. **Final Dashboard Update**
   ```markdown
   - [YYYY-MM-DD HH:MM:SS] **Social Media Post Published** ✓
     - Platform: [Facebook / Instagram / Both]
     - Topic: [Brief description]
     - Post URLs: [URLs]
     - Status: Complete
     - Tracking: /Social_Media/[Platform]/Analytics/POST_[date]_[topic].md
   ```

**Output:** Post(s) published and engagement tracking initiated

---

## Integration with Other Skills

### Required Dependencies

1. **handle-approval Skill** (Gold Branch 1)
   - MUST be used for all approval request creation
   - Enforces security thresholds
   - Manages expiration policies

### Optional Integrations

2. **create-plan Skill** (Silver Tier)
   - Use for content calendar planning
   - Schedule multi-platform campaigns

3. **process-tasks Skill** (Bronze Tier)
   - Process explicit social media requests from /Needs_Action

---

## Security & Safety Protocols

### Never Auto-Approve

- ALL social media posts REQUIRE human approval (zero exceptions)
- Public-facing content is permanent
- Brand reputation risk is HIGH
- Approval expiration: 72 hours (3 days)

### Content Validation Required

Before creating approval request:
- [ ] No confidential business information
- [ ] No client names/data without explicit permission
- [ ] No controversial, political, or divisive content
- [ ] No negative comments about competitors or industry peers
- [ ] Professional and inclusive language
- [ ] Image rights verified (own content or licensed)
- [ ] Platform community guidelines compliant

### Rate Limiting

From `Business_Goals.md` (adjust as needed):
- **Facebook:** 3-5 posts per week maximum
- **Instagram:** 4-7 posts per week maximum (daily acceptable)
- **Minimum Spacing:** 4 hours between posts on same platform
- **Cross-posting:** Stagger Facebook and Instagram by 2+ hours

---

## Error Handling

### Common Issues

1. **No Suitable Visual Content Found (Instagram)**
   - Action: Document image requirement in approval request
   - Provide: Suggested image type and references
   - User: Must provide image before approval

2. **Business_Goals.md Missing Social Media Section**
   - Action: Alert user to define social media strategy
   - Fallback: Use Company_Handbook brand themes
   - Default: Conservative posting frequency (2-3x/week)

3. **Facebook/Instagram API Authentication Failure**
   - Action: Log error with details
   - Alert: Create task in /Needs_Action for token refresh
   - Guidance: Link to OAuth troubleshooting guide

4. **Image Optimization Script Failure**
   - Action: Use original image if within size limits
   - Log: Warning about unoptimized image
   - Fallback: Request manual image preparation

5. **Hashtag Library Empty**
   - Facebook: Skip hashtags (not critical)
   - Instagram: Use generic industry hashtags
   - Alert: Recommend populating hashtag library

---

## Testing & Validation

### Dry-Run Mode

Both API helper scripts support dry-run:
```bash
python scripts/facebook_api_helper.py --dry-run --approval-file "path/to/file.md"
python scripts/instagram_api_helper.py --dry-run --approval-file "path/to/file.md"
```

This will:
- Parse approval file
- Validate content and image
- Show what would be posted
- NOT publish to platforms

### Success Criteria

- [ ] Platform-specific content generated correctly
- [ ] Hashtag strategy appropriate per platform
- [ ] Image requirements identified or images attached
- [ ] Approval request in correct format
- [ ] Dashboard logging complete
- [ ] Content passes quality checklist

---

## Trigger Phrases for Auto-Activation

This skill activates when user says:
- "post to facebook"
- "post to instagram"
- "share on social media"
- "create facebook post"
- "create instagram post"
- "post to facebook and instagram"
- "social media update"
- "schedule social post"
- "share [content] on instagram/facebook"

---

## Reference Files

- [Facebook Guidelines](./reference/facebook-guidelines.md) - FB-specific best practices, templates
- [Instagram Guidelines](./reference/instagram-guidelines.md) - IG-specific best practices, templates
- [Content Calendar](./reference/content-calendar.md) - Posting schedule and themes
- [Hashtag Library](./reference/hashtag-library.md) - Platform-specific hashtag collections
- [Engagement Rules](./reference/engagement-rules.md) - Optimization tactics for both platforms

---

## Examples

### Example 1: Instagram Product Showcase

```
User: "Post our new website design to Instagram"

Skill Actions:
1. Identifies content: Website project completion
2. Platform: Instagram (visual-first, portfolio content)
3. Checks for project screenshots in Vault/Projects/
4. Optimizes image to 1080x1080px
5. Generates caption with storytelling approach
6. Adds 8 relevant hashtags (#WebDesign #UIDesign #BrandIdentity...)
7. Creates APPROVAL_SOCIAL_IG_NewWebsiteLaunch_2026-01-11.md
8. Logs to Dashboard
9. Waits for human approval
```

### Example 2: Facebook Community Question

```
User: "Ask our Facebook community about their biggest business challenge"

Skill Actions:
1. Platform: Facebook (community engagement)
2. Selects "Community Question" template
3. Crafts 60-word post with open-ended question
4. Adds single hashtag #SmallBusiness (optional)
5. No image required (text-focused)
6. Creates APPROVAL_SOCIAL_FB_CommunityQuestion_2026-01-11.md
7. Human approves and responds to comments
8. Logs success to Dashboard
```

### Example 3: Cross-Platform Milestone (Both)

```
User: "Announce our 100th client milestone on social media"

Skill Actions:
1. Platform: Both (major announcement)
2. Creates TWO distinct posts:
   - Facebook: 75-word community appreciation with question
   - Instagram: Graphic + short caption + 10 hashtags
3. Identifies celebration image or requests custom graphic
4. Optimizes image separately for each platform
5. Creates APPROVAL_SOCIAL_BOTH_100ClientMilestone_2026-01-11.md
6. Waits for approval
7. Posts to both platforms (staggered by 2 hours)
8. Tracks engagement on both
```

---

## Notes

### Facebook Specifics
- Character limit: 63,206 (but 40-80 words optimal)
- Video performs exceptionally well
- Facebook Groups integration possible (future enhancement)
- Link sharing auto-generates previews

### Instagram Specifics
- Character limit: 2,200 for captions
- Story posting (future enhancement) - 24-hour content
- Reels (future enhancement) - short video content
- Link in bio is only clickable link location
- Carousel posts (up to 10 images) have higher engagement
- First comment can contain additional hashtags (common tactic)

---

*Skill Version: 1.0*
*Created: 2026-01-11*
*Branch: feat/gold-social-expansion*
*Dependencies: handle-approval (Gold Branch 1)*
