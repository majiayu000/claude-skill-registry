---
name: ugc-repurposer
description: 'Use when the user asks to "repurpose influencer content", "turn one video into multiple ads", or "build a UGC asset library"; produces a content inventory with rights, a multi-channel repurposing map (1 video to 10+ assets), per-format transformation specs, and a 30-day distribution plan. Not for paid amplification spend planning — use content-amplifier.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when a brand has influencer or user-generated content (videos, reels, reviews, images) and wants to extract more value by adapting it across paid ads, website, email, and organic social. Triggers include maximizing ROI on existing UGC, generating ad variations from organic clips, building a searchable content library, populating product pages with social proof, or planning a multi-channel rollout from a small set of source assets."
argument-hint: "<campaign or content set> [target channels]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Convert
---

# UGC Repurposer

This skill helps you extract maximum value from influencer-generated content by repurposing it across multiple channels and formats. One great piece of content can become many assets.

## Quick Start

Shortest invocation:

```
How can we repurpose this influencer content across channels?
```

Common scenario — turn a small set of clips into a multi-channel plan:

```
We have 3 great TikTok videos from our campaign. Build a repurposing plan and a 30-day distribution calendar.
```

## Skill Contract

- **Reads**: source UGC assets (videos, reels, reviews, images), creator handles and platforms, usage rights per asset, original performance metrics, target channels. Pulls prior campaign context from `memory/hot-cache.md` when `memory-management` is active.
- **Writes**: content inventory, repurposing opportunity map, 30-day distribution plan, format transformation specs, and a rights tracker to `memory/influencer/ugc-repurposer/YYYY-MM-DD-<topic>.md`.
- **Promotes**: durable facts (rights levels, expiration dates, library naming convention, top-performing source assets) to `memory/hot-cache.md`.
- **Done when**:
  - Every source asset has a rights level and expiration recorded.
  - At least one source asset is mapped to 3+ distinct output formats across 2+ channels.
  - A dated distribution plan with an asset checklist exists.
- **Primary next skill**: [landing-optimizer](../../convert/landing-optimizer/SKILL.md) — place the repurposed social-proof assets where they convert.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family needs no live integrations (Tier 1) — it works by asking you for inputs: the asset list, creator handles, rights terms, and original metrics. Provide those and the skill produces the full plan.

Where a tool could speed up or enrich the work, use a `~~` connector placeholder:

- `~~influencer database` — pull creator handles, platforms, and contract rights terms.
- `~~social platform analytics` — original view/engagement metrics to rank repurpose priority.
- `~~DAM / asset library` — store and tag processed assets; enforce the naming convention.
- `~~CRM` — reconcile creator records with usage-rights expirations.

No connector is required. See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless recipe per category.

## Instructions

When a user requests repurposing help:

1. **Audit Available Content**

   ```markdown
   ### Content Inventory
   
   **Campaign**: [name]
   **Total Content Pieces**: [#]
   **Content Types**: [videos, images, reviews, etc.]
   
   | ID | Creator | Platform | Type | Duration/Format | Rights | Status |
   |----|---------|----------|------|-----------------|--------|--------|
   | 001 | @[handle] | TikTok | Video | 45s | Perpetual | Available |
   | 002 | @[handle] | Instagram | Reel | 30s | 12 months | Available |
   | 003 | @[handle] | Instagram | Carousel | 5 images | Campaign only | Limited |
   
   ### Rights Summary
   
   | Rights Type | Content Count | Expiration |
   |-------------|---------------|------------|
   | Perpetual | [#] | Never |
   | 12 months | [#] | [date] |
   | Campaign only | [#] | [date] |
   | Organic only | [#] | N/A - no paid use |
   ```

2. **Map Repurposing Opportunities**

   ```markdown
   ## Repurposing Opportunity Map
   
   ### Original Content: @[handle] TikTok Video
   
   **Original**: 45-second product review video
   
   ### Repurposing Options
   
   | New Format | Channel | Modifications Needed | Effort |
   |------------|---------|---------------------|--------|
   | Spark Ad | TikTok Ads | None (native) | Low |
   | Instagram Reel | Instagram | Aspect ratio adjust | Low |
   | Facebook Ad | Facebook | Caption + CTA overlay | Medium |
   | YouTube Short | YouTube | Minor edits | Low |
   | Website testimonial | Website | Extract quote + thumbnail | Medium |
   | Email GIF | Email | Convert to GIF, 5-10s | Medium |
   | Still images | Multiple | Screenshot key moments | Low |
   | Quote cards | Social | Pull text, design graphic | Medium |
   | Landing page | Website | Embed or screenshot | Low |
   | Sales deck | Presentations | Screenshots + stats | Medium |
   
   ### Content Multiplication
   
   ```
   1 Original Video → 10+ Assets
   
   ┌─────────────────────────────────────────────┐
   │         Original: 45s TikTok Video          │
   └─────────────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      [Paid Ads]    [Social]     [Website/Email]
          │              │              │
    ┌─────┴─────┐   ┌────┴────┐   ┌────┴────┐
    │           │   │         │   │         │
   Spark   FB   IG  Stories Quote Website  Email
    Ad    Video Reel Clips  Cards Banner   Hero
   ```
   ```

3. **Create Repurposing Plan**

   ```markdown
   ## Content Repurposing Plan
   
   ### Priority Content
   
   Based on performance and rights, prioritize:
   
   | Rank | Content | Original Performance | Repurpose Priority |
   |------|---------|---------------------|-------------------|
   | 1 | @[handle1] video | [metrics] | Maximize - full rights |
   | 2 | @[handle2] reel | [metrics] | High - strong content |
   | 3 | @[handle3] post | [metrics] | Medium - limited rights |
   
   ### Channel Distribution Plan
   
   #### Paid Advertising
   
   | Platform | Content to Use | Format | Timeline |
   |----------|---------------|--------|----------|
   | TikTok Ads | [content IDs] | Spark Ads | Immediate |
   | Meta Ads | [content IDs] | Video/Carousel | Week 1 |
   | YouTube | [content IDs] | Shorts/Pre-roll | Week 2 |
   
   #### Owned Channels
   
   | Channel | Content to Use | Format | Timeline |
   |---------|---------------|--------|----------|
   | Website | [content IDs] | Embedded/Screenshots | Week 1 |
   | Email | [content IDs] | GIF/Images | Week 2 |
   | Blog | [content IDs] | Embedded + quotes | Week 3 |
   
   #### Social Media
   
   | Platform | Content to Use | Format | Timeline |
   |----------|---------------|--------|----------|
   | Instagram | [content IDs] | Repost/Stories | Ongoing |
   | TikTok | [content IDs] | Stitch/Duet | Ongoing |
   | Twitter | [content IDs] | Quote + link | Ongoing |
   
   #### Sales & Marketing
   
   | Use Case | Content to Use | Format | Timeline |
   |----------|---------------|--------|----------|
   | Sales deck | [content IDs] | Screenshots | Week 1 |
   | Case study | [content IDs] | Quotes + metrics | Month 2 |
   | Trade show | [content IDs] | Loop video | As needed |
   ```

4. **Format Transformation Guide**

   ```markdown
   ## Format Transformation Specifications
   
   ### Video to Multiple Formats
   
   #### Full Video Variations
   
   | Target | Aspect Ratio | Duration | Modifications |
   |--------|--------------|----------|---------------|
   | TikTok/Reels | 9:16 | 15-60s | Native or trim |
   | Instagram Feed | 1:1 or 4:5 | 15-60s | Crop/letterbox |
   | Facebook Feed | 1:1 or 16:9 | 15-60s | CTA overlay |
   | YouTube Shorts | 9:16 | <60s | YouTube branding |
   | YouTube Pre-roll | 16:9 | 15-30s | Front-load message |
   | Stories | 9:16 | 15s max | Split into segments |
   
   #### Video to Static
   
   | Asset Type | Source | Specifications |
   |------------|--------|----------------|
   | Thumbnail | Key frame | 1080x1080 or 1080x1920 |
   | Quote card | Pull text | Brand template |
   | Product shot | Frame grab | High-res moment |
   | GIF | 5-10s clip | <5MB, loop |
   
   ### Quote/Review Transformations
   
   | Format | Specifications | Use Case |
   |--------|----------------|----------|
   | Website testimonial | Photo + quote + name | Product pages |
   | Social quote card | Designed graphic | Organic posts |
   | Email testimonial | Quote + thumbnail | Campaigns |
   | Ad copy | Pull key phrases | Ad headlines |
   
   ### Image Transformations
   
   | From | To | Specifications |
   |------|----|----------------|
   | Carousel | Individual posts | Separate each image |
   | High-res image | Multiple crops | 1:1, 4:5, 9:16 |
   | Photo | Ad creative | Add copy overlay |
   | Photo | Website banner | Crop to banner ratio |
   ```

5. **Channel-Specific Guidelines**

   ```markdown
   ## Channel Repurposing Guidelines
   
   ### Website Usage
   
   **Product Pages**
   - Embed video reviews
   - Pull quote testimonials with creator photo
   - "As seen on @handle" badges
   
   **Homepage**
   - UGC carousel/gallery
   - Video testimonial section
   - Social proof counter
   
   **Landing Pages**
   - Hero video from top creator
   - Testimonial quotes throughout
   - Creator endorsement badges
   
   **Implementation**:
   ```html
   <!-- Embedded UGC Example -->
   <div class="ugc-testimonial">
     <video src="[creator-video]" controls></video>
     <p class="quote">"[Pull quote]"</p>
     <p class="attribution">@[handle], [platform]</p>
   </div>
   ```
   
   ### Email Marketing
   
   **Best Practices**:
   - Use GIFs (under 5MB) for video content
   - Include static fallback
   - Pull compelling quotes
   - Link to full content
   
   **Content Types**:
   | Email Type | UGC Usage |
   |------------|-----------|
   | Welcome series | Testimonial quote |
   | Promotional | Product demo GIF |
   | Newsletter | "What creators say" section |
   | Abandoned cart | Social proof quote |
   
   ### Paid Advertising
   
   **Creative Variations**:
   
   For each video, create:
   - Original (no changes)
   - Hook variation (different first 3 seconds)
   - CTA variation (different end card)
   - Length variations (15s, 30s, full)
   - Text overlay variation
   
   **Testing Matrix**:
   | Version | Hook | Body | CTA | Overlay |
   |---------|------|------|-----|---------|
   | A | Original | Original | Original | None |
   | B | New hook | Original | Original | None |
   | C | Original | Trimmed | Strong CTA | Brand |
   | D | New hook | Trimmed | Strong CTA | Brand |
   
   ### Social Media Organic
   
   **Reposting Best Practices**:
   - Always credit creator
   - Ask permission even if contractual
   - Add brand commentary
   - Use platform repost features when available
   
   **Content Calendar Integration**:
   | Day | Content Type | Source |
   |-----|--------------|--------|
   | Mon | Original brand content | Brand |
   | Tue | UGC repost | @[creator1] |
   | Wed | Original brand content | Brand |
   | Thu | UGC Stories | @[creator2] |
   | Fri | UGC repost | @[creator3] |
   ```

6. **Build Content Library**

   ```markdown
   ## UGC Content Library Structure
   
   ### Folder Organization
   
   ```
   /ugc-library/
   ├── /raw/
   │   ├── /videos/
   │   ├── /images/
   │   └── /audio/
   ├── /processed/
   │   ├── /ads/
   │   │   ├── /tiktok/
   │   │   ├── /meta/
   │   │   └── /youtube/
   │   ├── /website/
   │   ├── /email/
   │   └── /social/
   ├── /creators/
   │   ├── /@handle1/
   │   ├── /@handle2/
   │   └── /@handle3/
   └── /campaigns/
       ├── /campaign-name-1/
       └── /campaign-name-2/
   ```
   
   ### Asset Naming Convention
   
   `[campaign]_[creator]_[platform]_[type]_[variation]_[date]`
   
   Examples:
   - `summer2024_sarahfit_tiktok_video_original_20240615`
   - `summer2024_sarahfit_tiktok_video_15s_20240615`
   - `summer2024_sarahfit_ig_thumbnail_01_20240615`
   
   ### Metadata Tracking
   
   | Field | Description | Example |
   |-------|-------------|---------|
   | Asset ID | Unique identifier | UGC-2024-001 |
   | Creator | @handle | @sarahfit |
   | Original Platform | Where created | TikTok |
   | Content Type | Format | Video |
   | Duration | Length | 45s |
   | Usage Rights | License type | Perpetual |
   | Rights Expiration | If applicable | N/A |
   | Approved Uses | Where can use | All channels |
   | Performance | Original metrics | 250K views, 8% ER |
   | Tags | Searchable keywords | Product, review, demo |
   ```

7. **Rights Tracking**

   ```markdown
   ## Usage Rights Tracker
   
   ### Rights by Content
   
   | Content ID | Creator | Rights Level | Paid Use | Website | Email | Expires |
   |------------|---------|--------------|----------|---------|-------|---------|
   | UGC-001 | @handle1 | Full | ✅ | ✅ | ✅ | Never |
   | UGC-002 | @handle2 | Limited | ✅ | ✅ | ❌ | Dec 2024 |
   | UGC-003 | @handle3 | Organic only | ❌ | ❌ | ❌ | N/A |
   
   ### Expiring Rights Alert
   
   | Content | Creator | Rights Expire | Action Needed |
   |---------|---------|---------------|---------------|
   | UGC-002 | @handle2 | Dec 15, 2024 | Renew or remove |
   | UGC-005 | @handle5 | Jan 30, 2025 | Renew or remove |
   
   ### Rights Expansion Opportunities
   
   | Content | Current Rights | Potential Upgrade | Est. Cost |
   |---------|----------------|-------------------|-----------|
   | UGC-003 | Organic only | Add paid rights | $[X] |
   | UGC-002 | 12 months | Perpetual | $[X] |
   ```

## Example

**User**: "We have 3 great TikTok videos from our campaign. How should we repurpose them?"

**Output**:

```markdown
## Repurposing Plan: 3 TikTok Videos

### Content Overview
1. @creator1: 45s product demo (best performer)
2. @creator2: 30s before/after
3. @creator3: 60s day-in-the-life

### Immediate Actions (Week 1)

**From @creator1 video (45s demo):**
- ✅ TikTok Spark Ad (original)
- ✅ Instagram Reel (repost)
- ✅ Website product page embed
- ✅ 3 still images for ads/social
- ✅ 15s cut for Stories

**Total: 1 video → 6 assets**

### 30-Day Repurposing Calendar

| Week | Channel | Content | Asset Type |
|------|---------|---------|------------|
| 1 | TikTok Ads | @creator1 | Spark Ad |
| 1 | Instagram | @creator2 | Reel repost |
| 1 | Website | @creator1 | Embed |
| 2 | Meta Ads | @creator1 | Video ad |
| 2 | Email | @creator3 | GIF + quote |
| 3 | YouTube | @creator2 | Short |
| 4 | Landing page | All | Testimonials |

### Asset Checklist
- [ ] Create 15s cuts from all 3
- [ ] Pull 2 quote cards from @creator3
- [ ] Design 3 thumbnail images
- [ ] Convert @creator2 to GIF for email
- [ ] Add CTA overlay to @creator1 for Meta
```

## Tips for Maximum Value

1. **Plan repurposing before shooting** - Capture with multiple uses in mind
2. **Negotiate rights upfront** - Cheaper than adding later
3. **Create a system** - Organize for easy access
4. **Track everything** - Know what you can use where
5. **Refresh regularly** - Don't overuse the same content

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipe per connector category.
- [content-reviewer](../../activate/content-reviewer/SKILL.md) — ensure source content quality before repurposing.
- [content-amplifier](../../convert/content-amplifier/SKILL.md) — paid amplification of the repurposed UGC.
- [contract-helper](../../activate/contract-helper/SKILL.md) — secure or expand usage rights.
- [performance-analyzer](../../track/performance-analyzer/SKILL.md) — track how repurposed assets perform.

## Next Best Skill

**Primary**: [landing-optimizer](../../convert/landing-optimizer/SKILL.md) — drop the repurposed testimonials, hero videos, and quote cards onto the pages that convert.

**Alternates** (same Convert family):

- [content-amplifier](../../convert/content-amplifier/SKILL.md) — when the repurposed ad variations are ready for paid spend.

Termination note: track a visited-set. If a skill has already run this session, stop and report chain-complete instead of re-invoking it. Max chain depth is 3 hops.

## Related Skills

- [content-reviewer](../../activate/content-reviewer/SKILL.md) - Ensure content quality
- [content-amplifier](../../convert/content-amplifier/SKILL.md) - Paid amplification of UGC
- [contract-helper](../../activate/contract-helper/SKILL.md) - Secure usage rights
- [performance-analyzer](../../track/performance-analyzer/SKILL.md) - Track UGC performance
