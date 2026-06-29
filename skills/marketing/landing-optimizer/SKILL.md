---
name: landing-optimizer
description: 'Use when the user asks to "optimize our landing page for influencer traffic", "fix our promo-code landing page", or "improve conversion from a creator campaign"; produces a message-match audit, page-structure and social-proof recommendations, a promo-code/CTA conversion plan, and an A/B test roadmap. Not for measuring campaign results after launch — use performance-analyzer.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Activate when the user wants to build or improve a landing page that receives influencer-driven traffic: message match between creator content and the page, dedicated creator pages, promo-code auto-apply, social-proof placement, mobile conversion fixes, friction reduction, or A/B test planning for influencer campaigns."
argument-hint: "<landing page URL or campaign> [influencer handle] [promo code]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Convert
---

# Landing Optimizer

This skill helps you create and optimize landing pages specifically for influencer marketing traffic. When users click from an influencer's post, the landing experience should feel connected and optimized for conversion.

## Quick Start

Shortest invocation:

```
Optimize our landing page for traffic from [influencer campaign]
```

Common scenario — diagnose and fix a low-converting creator page:

```
Our influencer landing page has [X%] conversion rate. How can we improve it?
```

## Skill Contract

- **Reads**: landing page URL and current state, conversion rate and goal, traffic source (influencer handles, platforms, content type), the influencer's key message/quote, promo code, audience demographics. Inputs come from the user when no tool is connected.
- **Writes**: optimization plan saved to `memory/influencer/landing-optimizer/YYYY-MM-DD-<topic>.md` (message-match audit, structure and social-proof recommendations, conversion/CTA plan, A/B test roadmap).
- **Promotes**: durable facts — active campaign name, page URL, baseline conversion rate, promo code, primary creator — to `memory/hot-cache.md`.
- **Done when**:
  - Message-match score and named fixes are produced for the page.
  - A prioritized conversion plan (CTA, promo-code experience, friction, mobile) exists with expected impact.
  - An A/B test roadmap with at least one hypothesis and success metric is written.
- **Primary next skill**: [performance-analyzer](../../track/performance-analyzer/SKILL.md) — measure whether the optimizations moved conversion.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family needs no live integrations (Tier 1). The skill works by asking the user for the page URL, current conversion rate, the influencer's message, and the promo code, then producing the audit and plan from those inputs.

Optional connectors that can deepen the analysis when available:

- `~~analytics` — pull live conversion rate, bounce rate, scroll depth, and add-to-cart events instead of asking.
- `~~A/B testing platform` — read past test results and feed sample-size/duration estimates.
- `~~CMS / landing page builder` — inspect current page structure and copy directly.
- `~~social platform analytics` — confirm the creator's actual messaging and audience.

See [CONNECTORS.md](../../CONNECTORS.md) for the verified free/keyless recipe per category. Every step degrades gracefully to user-supplied inputs.

## Instructions

When a user requests landing page help:

1. **Assess Current State**

   ```markdown
   ### Landing Page Audit
   
   **Campaign**: [name]
   **Current URL**: [url]
   **Traffic Source**: [influencer(s)]
   **Current Conversion Rate**: [%]
   **Goal**: [what counts as conversion]
   
   ### Traffic Context
   
   | Factor | Details |
   |--------|---------|
   | Influencer(s) | @[handles] |
   | Platform(s) | [platforms] |
   | Content Type | [type] |
   | Key Message | [what influencer says] |
   | Promo Code | [code if applicable] |
   | Audience | [demographics] |
   ```

2. **Evaluate Message Match**

   ```markdown
   ## Message Match Analysis
   
   ### Influencer Content → Landing Page
   
   | Element | Influencer Says | Landing Page Shows | Match? |
   |---------|-----------------|--------------------|----|
   | Primary message | "[quote]" | "[page headline]" | ✅/⚠️/❌ |
   | Value prop | "[benefit]" | "[benefit shown]" | ✅/⚠️/❌ |
   | Offer | "[discount/deal]" | "[offer displayed]" | ✅/⚠️/❌ |
   | Product | [shown/mentioned] | [featured] | ✅/⚠️/❌ |
   | Tone | [style] | [page tone] | ✅/⚠️/❌ |
   
   ### Message Match Score: [X/10]
   
   **Issues Found**:
   - [Issue 1]: [how to fix]
   - [Issue 2]: [how to fix]
   
   **Why This Matters**:
   When users click from an influencer's content, they expect continuity. A mismatch causes confusion and abandonment.
   ```

3. **Page Structure Recommendations**

   ```markdown
   ## Landing Page Structure
   
   ### Recommended Layout for Influencer Traffic
   
   ```
   ┌─────────────────────────────────────────────┐
   │                   HEADER                     │
   │  Logo | Nav (minimal) | Cart/CTA            │
   ├─────────────────────────────────────────────┤
   │                   HERO                       │
   │  Headline matching influencer message       │
   │  Subheadline with value prop                │
   │  Primary CTA button                         │
   │  [Influencer mention/badge optional]        │
   ├─────────────────────────────────────────────┤
   │              SOCIAL PROOF                   │
   │  "@[influencer] loves it" + video/quote    │
   │  OR: UGC gallery                           │
   ├─────────────────────────────────────────────┤
   │              PRODUCT INFO                   │
   │  Key features (3-5 max)                    │
   │  Product images/video                      │
   │  Price + promo code application            │
   ├─────────────────────────────────────────────┤
   │           MORE SOCIAL PROOF                 │
   │  Reviews, testimonials, other creators     │
   ├─────────────────────────────────────────────┤
   │               FAQ/OBJECTIONS                │
   │  Answer common concerns                    │
   ├─────────────────────────────────────────────┤
   │              FINAL CTA                      │
   │  Repeat offer + strong CTA                 │
   ├─────────────────────────────────────────────┤
   │                  FOOTER                     │
   │  Trust badges, policies, support           │
   └─────────────────────────────────────────────┘
   ```
   
   ### Section-by-Section Optimization
   
   #### Hero Section
   
   **Current**: [describe current state]
   
   **Recommended**:
   - Headline: [specific recommendation]
   - Subheadline: [specific recommendation]
   - CTA: [specific button text]
   - Image/Video: [recommendation]
   
   **Example**:
   ```
   Headline: "[Benefit influencer highlighted]"
   Subheadline: "Use code [CODE] for [X]% off"
   CTA: "Shop Now" or "Get [X]% Off"
   ```
   
   #### Social Proof Section
   
   **Recommendation**:
   - Feature the specific influencer who drove traffic
   - Embed or screenshot their content
   - Include their quote/testimonial
   
   **Example**:
   ```
   "As seen on @[handle]'s [platform]"
   [Embedded video or quote card]
   "[Pull quote from their content]" - @[handle]
   ```
   
   #### Product Section
   
   **Recommendation**:
   - Show exact product(s) influencer featured
   - Highlight features they mentioned
   - Make promo code pre-applied or prominent
   ```

4. **Social Proof Integration**

   ```markdown
   ## Social Proof Strategy
   
   ### Influencer Integration
   
   | Element | Placement | Implementation |
   |---------|-----------|----------------|
   | Creator video | Hero or below | Embed or thumbnail |
   | Pull quote | Hero area | Designed quote card |
   | Creator badge | Near CTA | "As seen on @handle" |
   | UGC gallery | Mid-page | Carousel of content |
   
   ### Social Proof Hierarchy
   
   **Tier 1: Primary Influencer**
   - Most prominent placement
   - Their content/quote
   - Their audience = this traffic
   
   **Tier 2: Other Influencers**
   - Supporting testimonials
   - Adds credibility depth
   
   **Tier 3: Customer Reviews**
   - Star ratings
   - Written reviews
   - Review count
   
   **Tier 4: Trust Indicators**
   - Customer count ("Join 10,000+ customers")
   - Press mentions
   - Awards/certifications
   
   ### Implementation Examples
   
   **Creator Badge**:
   ```html
   <div class="creator-badge">
     <img src="creator-photo.jpg" alt="@handle">
     <span>Loved by @handle</span>
   </div>
   ```
   
   **UGC Quote**:
   ```html
   <blockquote class="ugc-quote">
     <p>"[Their review quote]"</p>
     <cite>@handle, [Platform]</cite>
   </blockquote>
   ```
   ```

5. **Conversion Optimization**

   ```markdown
   ## Conversion Optimization
   
   ### CTA Optimization
   
   | Element | Current | Recommended | Why |
   |---------|---------|-------------|-----|
   | Button text | [current] | [new] | [reason] |
   | Button color | [current] | [new] | [reason] |
   | Button size | [current] | [new] | [reason] |
   | Placement | [current] | [new] | [reason] |
   | Quantity | [#] | [#] | [reason] |
   
   **CTA Best Practices for Influencer Traffic**:
   - Reference the promo code in button ("Get 20% Off with CODE")
   - Create urgency if applicable ("Limited Time")
   - Use action-oriented language ("Shop," "Get," "Claim")
   - Make code visible and easy to copy
   
   ### Promo Code Experience
   
   **Current**: [describe current promo code experience]
   
   **Recommended**:
   - [ ] Auto-apply code via URL parameter
   - [ ] Display code prominently at top
   - [ ] Show savings amount
   - [ ] Make code easy to copy
   - [ ] Confirm code applied in cart
   
   **Implementation**:
   ```
   URL: yoursite.com/landing?code=CREATOR20
   
   On page load:
   1. Detect code parameter
   2. Apply to cart automatically
   3. Display "CREATOR20 applied - you save $X"
   ```
   
   ### Friction Reduction
   
   | Friction Point | Impact | Solution |
   |----------------|--------|----------|
   | [Point 1] | High/Med/Low | [Solution] |
   | [Point 2] | High/Med/Low | [Solution] |
   | [Point 3] | High/Med/Low | [Solution] |
   
   **Quick Wins**:
   - Remove unnecessary form fields
   - Add guest checkout option
   - Show shipping costs early
   - Display trust badges near CTAs
   - Add live chat/support option
   
   ### Mobile Optimization
   
   **Critical for influencer traffic** (majority mobile):
   
   | Element | Mobile Check | Status |
   |---------|--------------|--------|
   | Page load speed | <3 seconds | ✅/❌ |
   | CTA button size | Thumb-friendly | ✅/❌ |
   | Form fields | Easy to tap | ✅/❌ |
   | Images | Optimized | ✅/❌ |
   | Scroll depth | Key info visible | ✅/❌ |
   ```

6. **A/B Testing Plan**

   ```markdown
   ## A/B Testing Recommendations
   
   ### Test Priority Matrix
   
   | Test | Impact | Effort | Priority |
   |------|--------|--------|----------|
   | Headline copy | High | Low | 1 |
   | CTA button text | High | Low | 2 |
   | Hero image/video | High | Medium | 3 |
   | Social proof placement | Medium | Low | 4 |
   | Page length | Medium | Medium | 5 |
   
   ### Test 1: Headline
   
   **Hypothesis**: [If we change X, then Y because Z]
   
   | Variant | Headline | Expected Impact |
   |---------|----------|-----------------|
   | Control | "[Current headline]" | Baseline |
   | Test A | "[Alternative 1]" | [expected change] |
   | Test B | "[Alternative 2]" | [expected change] |
   
   **Sample Size**: [calculated minimum]
   **Duration**: [minimum days to reach significance]
   **Success Metric**: Conversion rate
   
   ### Test 2: CTA
   
   **Hypothesis**: [statement]
   
   | Variant | Button | Expected Impact |
   |---------|--------|-----------------|
   | Control | "[Current]" | Baseline |
   | Test A | "[Alternative]" | [expected change] |
   
   ### Testing Best Practices
   
   - Test one element at a time
   - Run until statistical significance
   - Document all tests and results
   - Implement winners quickly
   - Test continuously
   ```

7. **Influencer-Specific Pages**

   ```markdown
   ## Influencer-Specific Landing Pages
   
   ### When to Create Dedicated Pages
   
   ✅ Create dedicated page when:
   - Influencer has unique offer/code
   - High-volume partnership
   - Different product focus
   - Long-term ambassador
   - Need attribution clarity
   
   ❌ Use general page when:
   - Small one-off partnership
   - Same offer as general campaigns
   - Resource constraints
   
   ### Dedicated Page Template
   
   **URL Structure**: yoursite.com/[influencer-handle]
   
   **Page Elements**:
   
   ```
   ┌──────────────────────────────────────┐
   │  "Welcome from @[handle]'s page!"   │
   │  [Creator's endorsement/video]      │
   │  Their exclusive offer: [OFFER]     │
   ├──────────────────────────────────────┤
   │  Product(s) they featured           │
   │  [Images matching their content]    │
   │  [Their specific talking points]    │
   ├──────────────────────────────────────┤
   │  Their review/testimonial           │
   │  [Additional social proof]          │
   ├──────────────────────────────────────┤
   │  Shop + Promo Code Application      │
   └──────────────────────────────────────┘
   ```
   
   ### Personalization Options
   
   | Element | Personalization Level |
   |---------|----------------------|
   | URL | /creator-name |
   | Headline | Reference creator |
   | Hero image | Creator's content |
   | Offer | Their unique code |
   | Products | What they featured |
   | Testimonial | Their quote |
   ```

8. **Performance Tracking**

   ```markdown
   ## Landing Page Analytics
   
   ### Key Metrics to Track
   
   | Metric | Target | Current | Status |
   |--------|--------|---------|--------|
   | Page load time | <3s | [X]s | ✅/❌ |
   | Bounce rate | <40% | [X]% | ✅/❌ |
   | Conversion rate | [X]% | [X]% | ✅/❌ |
   | Add to cart rate | [X]% | [X]% | ✅/❌ |
   | Average order value | $[X] | $[X] | ✅/❌ |
   
   ### Tracking Setup
   
   **UTM Parameters**:
   ```
   ?utm_source=[platform]
   &utm_medium=influencer
   &utm_campaign=[campaign-name]
   &utm_content=[@handle]
   &utm_term=[content-type]
   ```
   
   **Events to Track**:
   - Page view
   - Scroll depth (25%, 50%, 75%, 100%)
   - CTA clicks
   - Promo code applied
   - Add to cart
   - Purchase
   
   ### Attribution
   
   | Method | Use Case |
   |--------|----------|
   | UTM parameters | Source tracking |
   | Promo codes | Direct attribution |
   | Unique URLs | Creator-specific tracking |
   | Pixel tracking | Conversion attribution |
   ```

## Example

**User**: "Our landing page for @fitnessanna's protein powder campaign has a 1.2% conversion rate. How can we improve it?"

**Output**:

```markdown
## Landing Page Optimization: @fitnessanna Campaign

### Diagnosis

**Current CR**: 1.2% (Below benchmark of 2-3% for influencer traffic)

### Issues Found

1. **Message Mismatch**: Anna talks about "smooth texture" but landing page leads with "high protein content"
2. **No Social Proof**: Anna's content isn't featured on the page
3. **Promo Code Friction**: Code "ANNA20" isn't auto-applied
4. **Mobile CTA**: Button is below the fold on mobile

### Priority Fixes

| Fix | Expected Impact | Effort |
|-----|-----------------|--------|
| Add Anna's video to hero | +0.5% CR | Low |
| Auto-apply promo code | +0.3% CR | Medium |
| Match headline to her messaging | +0.3% CR | Low |
| Move CTA above fold mobile | +0.2% CR | Low |

**Combined Expected Impact**: 1.2% → 2.5% CR

### Implementation

**New Headline**: "Protein That Actually Tastes Good" (matches Anna's main message)

**Add to Hero**:
```html
<div class="creator-feature">
  <video src="anna-testimonial.mp4"></video>
  <p>"The smoothest protein I've tried" - @fitnessanna</p>
</div>
```

**Auto-Apply Code**:
URL: yoursite.com/protein?code=ANNA20
Display: "ANNA20 applied! You save 20%"

### Test Plan
Week 1: Implement hero changes
Week 2: A/B test headline variations
Week 3: Test CTA button copy
```

## Tips for Better Landing Pages

1. **Match the message** - Continuity from content to page
2. **Feature the influencer** - They drove the traffic
3. **Mobile first** - Most influencer traffic is mobile
4. **Reduce friction** - Every click loses people
5. **Test continuously** - Small improvements compound

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipes per connector category.
- Sibling skills in the influencer-marketing family:
  - [ugc-repurposer](../ugc-repurposer/SKILL.md) — source creator content for landing pages.
  - [content-amplifier](../content-amplifier/SKILL.md) — drive traffic to landing pages.
  - [brief-generator](../../plan/brief-generator/SKILL.md) — align creator content with landing goals.

## Next Best Skill

**Primary**: [performance-analyzer](../../track/performance-analyzer/SKILL.md) — measure whether the optimizations actually moved conversion, AOV, and attribution.

**Alternates** (same Convert/Track families):

- [ugc-repurposer](../ugc-repurposer/SKILL.md) — when the audit shows the page needs more creator content to feature.
- [content-amplifier](../content-amplifier/SKILL.md) — when an optimized page is ready and you want to scale traffic to it.

**Termination note**: Maintain a visited-set this session. If a recommended skill has already been invoked, stop and report the chain as complete rather than re-running it. Hard stop at chain depth 3 to avoid loops.
