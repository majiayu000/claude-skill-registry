---
name: tradeoff-evaluation
description: Use when metrics conflict or feature has mixed results - evaluates short-term vs long-term impact, segments by user lifecycle, aligns with strategic positioning, and explores mitigation strategies before binary rollback decisions
---

# Trade-off Evaluation

## Purpose

Make informed decisions when improving one metric harms another, or when A/B test results are mixed. Avoids binary thinking (ship vs. rollback) by exploring nuanced approaches that preserve gains while addressing losses.

## When to Use This Skill

Activate automatically when:
- A/B test shows some metrics up, others down
- Feature launched with mixed performance
- Optimizing for one goal reduces another
- Stakeholders disagree on ship/no-ship decision
- Redesign shifted user behavior unexpectedly
- `tradeoff-decision` workflow evaluates mixed results
- `metrics-definition` workflow identifies counter-metrics
- Need to choose between competing priorities

**When NOT to use:**
- All metrics clearly positive (ship it)
- All metrics clearly negative (don't ship)
- Harm is minor and acceptable (make call quickly)
- Decision is time-sensitive and stakes are low

## Core Principles

### 1. Default to "It Depends"

**Avoid binary yes/no thinking:**
- ❌ "Should we ship this? Yes or No"
- ✓ "Should we ship this to everyone, some segments, or iterate first?"

**Segmentation thinking:**
- New users vs. established users
- Power users vs. casual users
- Free tier vs. paid tier
- Geographic segments
- Use case segments

### 2. Long-Term Strategic Value > Short-Term Gains

**When in doubt, choose the option that:**
- Aligns with company strategic positioning
- Builds sustainable competitive advantages
- Strengthens core value proposition
- Supports mission beyond just revenue

**Example (Snapchat):**
- Short-term: Time on site ↑ (good for ads)
- Long-term: Messages sent ↓, stories shared ↓ (breaks social flywheel)
- Decision: Long-term strategic value (social/camera app) > short-term time-on-site gains

### 3. Mitigation Before Rollback

**Avoid immediate reversions:**
- Understand WHY metrics moved
- Identify which specific changes caused issues
- Explore partial fixes that preserve gains
- Test iterations before full rollback

**Staged problem-solving:**
1. Analyze: Which parts of change are beneficial vs. harmful?
2. Hypothesize: What modifications could fix the harm?
3. Test: Try mitigation strategies
4. Only then: Consider full rollback if mitigation fails

## Decision Frameworks

### Framework 1: User Lifecycle Segmentation

**Principle:** Different metrics matter at different user stages

**Example: Facebook News Feed**

**Question:** Show ad after every 10th post OR show "People You May Know" widget?

**Answer: It depends on user lifecycle stage**

**New Users (< 50 friends):**
- Priority: Build friend network for long-term retention
- Decision: Show "People You May Know"
- Rationale: Need friends to find value; too early to monetize
- Trade-off: Sacrifice short-term ad revenue for long-term user retention

**Established Users (> 2000 friends):**
- Priority: Monetization (already retained)
- Decision: Show ads
- Rationale: Friend suggestions have diminishing returns; time to generate revenue
- Trade-off: Already has network, ad value exceeds friend value

**Gradient Approach:**
- 0-50 friends: 100% PYMK
- 50-500 friends: 70% PYMK, 30% ads
- 500-2000 friends: 30% PYMK, 70% ads
- 2000+ friends: 10% PYMK, 90% ads

### Framework 2: Strategic Positioning Alignment

**Principle:** Choose option that reinforces company's core identity

**Example: Snapchat Redesign**

**Situation:**
- Time on site: ↑ 15% (good for ads)
- Messages sent: ↓ 12% (bad for social engagement)
- Stories shared: ↓ 8% (bad for social engagement)

**Strategic Question:** Is Snapchat a social/camera app or content consumption app?

**Analysis:**
- **Content consumption positioning:**
  - Competes with TikTok, YouTube, Instagram Reels
  - Market saturated with strong players
  - Not Snapchat's core competency
  - Time-on-site gains are short-term

- **Social/camera app positioning:**
  - Unique value proposition in market
  - Peer-to-peer engagement drives retention flywheel
  - Messages/stories create notifications → app opens
  - Sustainable long-term competitive advantage

**Decision:** Prioritize messaging/stories over time-on-site
- Reason: Aligns with core strategic positioning
- Trade-off: Accept lower time-on-site to strengthen social flywheel
- Mitigation: Explore ways to integrate creator content without harming peer-to-peer

### Framework 3: Flywheel Impact Analysis

**Principle:** Preserve metrics that drive virtuous cycles

**Identify flywheel components:**
1. What user behavior creates notifications/triggers?
2. What brings users back to the product?
3. What creates value for other users (network effects)?
4. What reinforces habit formation?

**Example: Snapchat Social Flywheel**

```
Stories shared → Friends receive notifications → Friends open app → 
Friends send messages → Original user gets notification → Opens app → 
Shares more stories → [LOOP]
```

**Breaking the flywheel:**
- Reduced story sharing = Fewer notifications sent
- Fewer notifications = Less app opening
- Less opening = Less engagement
- Less engagement = Reduced retention

**Preservation priority:**
- Stories shared: CRITICAL (triggers loop)
- Messages sent: CRITICAL (reciprocal engagement)
- Time on content: NICE-TO-HAVE (doesn't drive loop)

**Decision:** Protect flywheel metrics even at cost of other metrics

### Framework 4: Revenue Impact (Short vs. Long-Term)

**Principle:** Evaluate both immediate and future revenue implications

**Short-term revenue metrics:**
- Immediate ad impressions
- This quarter's subscription conversions
- Current transaction volume

**Long-term revenue metrics:**
- User retention (LTV)
- Network effects (platform value)
- Brand strength
- Competitive positioning

**Example: Facebook Dating**

**Scenario:** Dating feature increases MAU but reduces News Feed engagement

**Short-term analysis:**
- News Feed ads: Slightly down (users spending time in dating)
- Immediate revenue: Minor negative

**Long-term analysis:**
- Overall platform value: Up (new use case)
- User retention: Up (more reasons to use Facebook)
- Competitive positioning: Better (catch up to Tinder/Bumble)
- LTV: Up (stronger platform lock-in)

**Decision:** Ship dating feature despite News Feed cannibalization
- Long-term strategic value > short-term ad revenue
- Counter-metric (News Feed engagement) acceptable trade-off

## Mitigation Strategies Catalog

### Strategy 1: Segmented Rollout

**When to use:** Impact varies by user type

**Approach:**
- Ship to segments where metrics are net positive
- Don't ship to segments where metrics are net negative
- Iterate on problematic segments separately

**Example:**
- Feature works for power users, not casual users
- Ship to power users immediately
- Redesign for casual users based on learnings

### Strategy 2: Targeted Modifications

**When to use:** Specific element causing harm

**Approach:**
- Analyze which specific change caused negative impact
- Keep beneficial parts, modify harmful parts
- Test modified version

**Example (Snapchat):**
- Problem: Creator content tab reducing peer engagement
- Keep: Creator content (time-on-site benefit)
- Modify: Re-integrate friend stories in main tab
- Add: Prompts to message friends after viewing content

### Strategy 3: Compensation Mechanisms

**When to use:** Trade-off is necessary but painful

**Approach:**
- Accept metric decline in one area
- Boost complementary features to compensate
- Create new paths to value

**Example:**
- Feature reduces click rate but improves user satisfaction
- Accept: Lower clicks (engagement metric)
- Compensate: Better retention (satisfaction metric)
- Net result: Lower short-term engagement, higher long-term LTV

### Strategy 4: Gradual Rollout with Monitoring

**When to use:** Uncertain about long-term effects

**Approach:**
- 10% rollout → Monitor for 2 weeks
- 25% rollout → Monitor for 2 weeks  
- 50% rollout → Monitor for 1 month
- Maintain holdback group indefinitely

**Watch for:**
- Delayed negative effects (retention drops after initial boost)
- Segment-specific issues that emerge at scale
- Interaction effects with other features

### Strategy 5: A/B/C Testing

**When to use:** Multiple approaches possible

**Approach:**
- Test original (A) vs. full change (B) vs. modified version (C)
- Evaluate trade-offs across all three
- Choose best balance

**Example:**
- A: Current experience
- B: New design with creator content prominent
- C: New design with balanced creator/peer content
- Evaluate: Time-on-site, messages, stories across all three

## Workflow Steps

### 1. Identify the Conflict

Ask:
- Which metrics went up?
- Which metrics went down?
- What's the magnitude of each change?
- Are changes statistically significant?

Document the trade-off clearly.

### 2. Apply Strategic Lens

Ask:
- Which metric aligns with company strategic positioning?
- Which metric drives long-term competitive advantage?
- Which metric supports the core value proposition?
- Which metric feeds important flywheels?

Rank metrics by strategic importance.

### 3. Segment the Analysis

Ask:
- Does trade-off vary by user segment?
- Are some segments net positive, others net negative?
- Which segments are most valuable long-term?

Analyze trade-offs by segment.

### 4. Identify Mitigation Options

Brainstorm:
- Can we modify to reduce harm?
- Can we segment the rollout?
- Can we compensate with other features?
- What's the best of both worlds approach?

List 3-5 mitigation strategies.

### 5. Make Recommendation

Choose:
- **Ship fully:** Net positive across segments, aligned with strategy
- **Ship to segments:** Positive for some users, not others
- **Iterate first:** Promising but needs modification
- **Rollback:** Net negative, no clear mitigation path

Document rationale and risks.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Binary thinking (ship vs. rollback only) | Explore segmented rollout and mitigation |
| Optimizing for wrong metric | Use strategic alignment as tie-breaker |
| Ignoring long-term flywheel effects | Analyze how metrics drive retention loops |
| Not segmenting by user lifecycle | New vs. established users need different things |
| Immediate rollback without diagnosis | Understand cause before reversing |
| Prioritizing short-term revenue over LTV | Calculate long-term customer value impact |

## Anti-Rationalization Blocks

| Rationalization | Reality |
|-----------------|---------|
| "All metrics must go up" | Trade-offs are normal; choose strategically |
| "Short-term revenue is most important" | Long-term LTV usually matters more |
| "We can't ship if anything goes down" | Strategic metrics matter more than vanity metrics |
| "Let's just rollback to be safe" | Understand why before reversing |
| "This is too complex to analyze" | Use systematic frameworks to decide |
| "Everyone should get same experience" | Segmentation often creates better outcomes |

## Success Criteria

Trade-off evaluation succeeds when:
- Conflicting metrics clearly identified and quantified
- Strategic importance of each metric assessed
- User segments analyzed for differential impact
- 3-5 mitigation strategies brainstormed
- Decision framework applied (lifecycle, strategic, flywheel, revenue)
- Recommendation made with clear rationale
- Risks of chosen path documented
- Plan for monitoring outcomes established

## Real-World Examples

### Example 1: Snapchat Redesign - Time vs. Social

**Situation:**
- Redesign launched: Separate social from media
- Time on site: ↑ 15% (watching creator content)
- Messages sent: ↓ 12%
- Stories shared: ↓ 8%

**Initial question:** Net positive or net negative?

**Strategic analysis:**
- **Content app positioning:** Time-on-site gains matter
  - But: Saturated market (TikTok, YouTube, Instagram)
  - Snapchat not core competency

- **Camera/social app positioning:** Messaging/stories matter
  - Unique value proposition
  - Flywheel: Stories → Notifications → Messages → Retention
  - Sustainable competitive advantage

**Decision: Net negative despite time-on-site gains**

**Rationale:**
- Social flywheel breaking outweighs time-on-site benefit
- Long-term retention risk from reduced peer engagement
- Strategic positioning as camera/social app is core identity

**Mitigation approach (not immediate rollback):**
1. Analyze traffic distribution: Where are users spending time?
2. Test modifications: Can we show friend stories in creator tab?
3. Add prompts: Encourage messaging after content viewing
4. Monitor: Track if mitigation restores messaging/stories

**Only if mitigation fails:** Consider full rollback

### Example 2: Facebook Dating Cannibalization

**Situation:**
- Dating feature launched
- Weekly active dating users: ↑ (new feature adoption)
- News Feed engagement: ↓ 2% (time shifting to dating)
- Overall Facebook MAU: → (no change)

**Trade-off:** Dating adoption vs. News Feed engagement

**Strategic analysis:**

**Short-term:**
- Ad impressions: Slightly down (less News Feed time)
- Revenue: Minor negative

**Long-term:**
- Platform value: Up (new use case, competitive with dating apps)
- User retention: Up (more reasons to use Facebook)
- Strategic positioning: Better (full-service social platform)
- LTV: Up (dating users more engaged overall)

**Segmentation analysis:**
- New users: Dating is additional value (no cannibalization)
- Established users: Some shift from Feed to Dating (acceptable trade-off)
- Dating-age demographic: Much higher engagement overall

**Decision: Ship dating feature widely**

**Rationale:**
- Long-term strategic value > short-term ad revenue
- Counter-metric (Feed engagement) within acceptable range
- Dating-age users show net positive engagement
- Competitive necessity (catch up to Tinder/Bumble)

**Mitigation:**
- Show dating profile prompts in News Feed (drive discovery)
- Dating → Feed suggestions (create cross-product engagement)
- Monitor for further cannibalization (have thresholds for concern)

### Example 3: Facebook Feed - Ads vs. Friend Building

**Situation:**
- Feed space allocation decision
- Option A: Show ad after every 10th post
- Option B: Show "People You May Know" widget

**Trade-off:** Immediate revenue vs. long-term network building

**User lifecycle segmentation approach:**

| User Stage | Friends | Decision | Rationale |
|------------|---------|----------|-----------|
| New | 0-50 | 100% PYMK | Need friends to find value; monetization can wait |
| Growing | 50-500 | 70% PYMK, 30% ads | Still building network, some monetization OK |
| Established | 500-2000 | 30% PYMK, 70% ads | Good network, ready for monetization |
| Saturated | 2000+ | 10% PYMK, 90% ads | Friend suggestions have diminishing returns |

**Implementation:**
- Dynamic per-user allocation based on friend count
- Maximize LTV by balancing retention (friends) and revenue (ads)

**Monitoring:**
- New user retention rates by PYMK exposure
- Revenue per user by PYMK/ad mix
- Friend connection rates by allocation

### Example 4: Uber Driver Quality vs. Availability

**Situation:**
- Strict driver quality standards proposed (4.8+ rating required)
- Driver quality: ↑ (removing low-rated drivers)
- Driver availability: ↓ (fewer drivers in network)
- Wait times: ↑ (supply reduction)

**Trade-off:** Quality experience vs. availability

**Strategic analysis:**

**Option A: Strict standards (4.8+ only)**
- Pro: Premium experience, higher rider satisfaction
- Con: Longer wait times, reduced coverage
- Risk: Riders switch to Lyft due to availability

**Option B: Moderate standards (4.5+ rating)**
- Pro: Good quality, maintained availability
- Con: Some poor experiences persist
- Balance: Acceptable quality + good availability

**Option C: Segmented approach**
- Premium tier: 4.8+ only (UberBlack)
- Standard tier: 4.5+ (UberX)
- Pro: Choice for customers
- Complex: More tiers to manage

**Decision: Option B with active quality improvement**

**Rationale:**
- 4.5-4.8 drivers often improvable with training
- Availability is competitive necessity
- Quality can improve through coaching, not just removal

**Mitigation:**
- Driver quality program: Training for 4.5-4.8 drivers
- Real-time feedback: Help drivers improve
- Graduated warnings before deactivation
- Monitor: Track if 4.5-4.8 drivers improve to 4.8+

### Example 5: YouTube Homepage Redesign

**Situation:**
- New homepage emphasizes algorithm recommendations
- Video clicks from homepage: ↑ 20%
- New genre discovery: ↑ 15%
- Time spent per video: ↓ 10% (more browsing, less watching)

**Trade-off:** Discovery/clicks vs. watch time depth

**Strategic analysis:**

**Primary North Star:** Total watch time (ad impressions)
- More clicks but less time per video
- Net impact: Need to calculate (clicks × time per video)

**Mission alignment:** "Organize world's information" / "Broaden interests"
- New genre discovery: ✓ Supports mission
- Suggests users finding valuable content

**Flywheel impact:**
- More discovery → More interests → More returning
- Could be positive for long-term retention

**Decision: Keep redesign but monitor retention**

**Rationale:**
- Discovery aligns with mission
- May improve long-term engagement (more interests = more reasons to return)
- Time-per-video could stabilize as users settle on new content

**Mitigation:**
- Optimize recommendation quality (prevent spam clicks)
- Balance familiar vs. new content
- Monitor: 30-day retention and long-term watch time trends

**Success criteria:**
- 30-day retention ↑ (discovery driving habit)
- Total watch time stable or ↑ (volume compensates)
- User satisfaction surveys positive

## Related Skills

- **north-star-alignment**: Identifies which metric aligns with company strategy
- **funnel-metric-mapping**: Identifies where in funnel the trade-off occurs
- **proxy-metric-selection**: Creates counter-metrics to detect trade-offs
- **root-cause-diagnosis**: Diagnoses why metrics moved before deciding
- **tradeoff-decision** (workflow): Orchestrates systematic trade-off evaluation
- **metrics-definition** (workflow): Uses trade-off evaluation to identify counter-metrics

## Integration Points

**Called by workflows:**
- `metrics-definition` - Step 4: Identify counter-metrics and trade-offs
- `tradeoff-decision` - Steps 2-3: Evaluate mixed A/B test results
- `dashboard-design` - Step 4: Include counter-metrics to detect trade-offs
- `goal-setting` - Step 3: Evaluate cost of aggressive vs. conservative targets

**May call:**
- `north-star-alignment` to assess strategic importance
- `funnel-metric-mapping` to understand where trade-off occurs
- `root-cause-diagnosis` to understand why metrics moved

