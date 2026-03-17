---
name: linkedin-personal-branding
description: Comprehensive LinkedIn personal branding analysis, profile optimization, and visibility improvement skill using Claude for Chrome browser tools. Use when users request LinkedIn profile analysis, personal branding audit, profile optimization recommendations, LinkedIn visibility improvement, headline optimization, About section review, content strategy guidance, engagement analysis, or Social Selling Index improvement. Works with Claude for Chrome to analyze profile photos, banners, headlines, About sections, experience, skills, recommendations, featured content, activity/posts, and network engagement directly from the user's browser.
---

# LinkedIn Personal Branding Skill

## ⚠️ CRITICAL: Mandatory Requirements

**Every audit MUST include these elements - no exceptions:**

| Requirement | What | Why |
|-------------|------|-----|
| **Industry Classification** | Identify user's industry/sector | Determines which benchmarks to apply |
| **Profile Type** | Employee / Consultant / Freelancer / Entrepreneur / Job Seeker | Affects recommendations (e.g., Services section) |
| **Target Audience** | Recruiters / Clients / Peers / Investors / Partners | Shapes content and positioning strategy |
| **Engagement Rate** | CALCULATED: (R+C+S)/Impressions×100 | Raw numbers alone are meaningless |
| **SSI Score** | Actual score OR estimation with note | Key performance indicator |

**These fields appear in the report header and metrics section. Do not skip them.**

---

## Overview

This skill enables comprehensive LinkedIn profile analysis, personal branding assessment, and actionable optimization recommendations using **Claude for Chrome** browser automation. It helps professionals improve their visibility, engagement, and professional positioning on LinkedIn.

**Works for ANY industry:** Tech, Finance, Healthcare, Legal, Marketing, HR, Consulting, Creative, Nonprofit, and more. See `references/metrics_benchmarks.md` for industry-specific benchmarks.

**Requirements:**
- Claude for Chrome extension installed and connected
- User has LinkedIn profile open in their browser
- User is logged into LinkedIn (for access to private metrics like profile views)

## Core Workflow

### Step 1: Determine Analysis Type

Identify what type of LinkedIn work is needed:

**A. Full Profile Audit**
- Comprehensive analysis of all profile elements
- Output: Complete audit report with scores and recommendations

**B. Quick Profile Review**
- Fast assessment of key profile elements
- Output: Priority action items and quick wins

**C. Content Strategy Analysis**
- Focus on posts, engagement, and content performance
- Output: Content recommendations and posting strategy

**D. Visibility Optimization**
- Focus on discoverability and search appearances
- Output: Keyword and SEO optimization recommendations

### Step 1b: MANDATORY - Profile Classification

**⚠️ REQUIRED: Before any analysis, you MUST identify and document:**

| Field | How to Determine | Example Values |
|-------|------------------|----------------|
| **Industry/Sector** | Job titles, company types, content topics | Tech, Finance, Healthcare, Consulting, etc. |
| **Profile Type** | Current role structure | Employee, Consultant/Freelancer, Entrepreneur, Job Seeker |
| **Target Audience** | Who they want to reach | Recruiters, Clients, Peers, Investors, Partners |
| **Geographic Focus** | Location + language | Local, Regional, Global |

**Classification Questions to Answer:**
1. What industry does this person work in? (Check job titles, skills, content)
2. Are they an employee, consultant, freelancer, or entrepreneur?
3. Who is their target audience on LinkedIn?
4. What is their primary language/market?

**This information MUST appear in the audit report header:**
```
**Industry/Sector:** [IDENTIFIED INDUSTRY]
**Profile Type:** [Employee / Consultant / Freelancer / Entrepreneur / Job Seeker]
**Target Audience:** [Recruiters / Clients / Peers / Investors / Partners]
```

**Why This Matters:**
- Benchmarks vary significantly by industry (see metrics_benchmarks.md)
- Recommendations differ for employees vs. consultants
- Content strategy depends on target audience

### Step 2: Gather Profile Information

Use **Claude for Chrome** browser tools to access the LinkedIn profile. The user should have LinkedIn open in their browser.

**Chrome DevTools MCP Tools for LinkedIn Analysis:**

| Tool | MCP Tool Name | Use For |
|------|---------------|---------|
| List Pages | `mcp__chrome-devtools__list_pages` | Get browser tabs, find LinkedIn tab by URL |
| Select Page | `mcp__chrome-devtools__select_page` | Select LinkedIn tab for operations |
| Snapshot | `mcp__chrome-devtools__take_snapshot` | Extract accessibility tree with element UIDs |
| Screenshot | `mcp__chrome-devtools__take_screenshot` | Capture visual elements (photo, banner) |
| Navigate | `mcp__chrome-devtools__navigate_page` | Navigate to URLs or back/forward |
| Click | `mcp__chrome-devtools__click` | Click elements using UID from snapshot |
| Wait For | `mcp__chrome-devtools__wait_for` | Wait for text to appear (lazy content) |
| Hover | `mcp__chrome-devtools__hover` | Scroll element into view |

**Workflow:**
1. Call `mcp__chrome-devtools__list_pages` → find pageId where URL contains "linkedin.com/in/"
2. Call `mcp__chrome-devtools__select_page` with the pageId to focus LinkedIn tab
3. Call `mcp__chrome-devtools__take_snapshot` → returns accessibility tree with UIDs (e.g., `[uid1]`, `[uid2]`)
4. Call `mcp__chrome-devtools__take_screenshot` → analyze profile photo and banner quality
5. For lazy-loaded sections: `mcp__chrome-devtools__hover` to scroll → re-snapshot to get new content

Key sections to analyze:

**Profile Foundation**
- Profile photo (quality, professionalism, approachability)
- Banner/background image (branded, relevant, memorable)
- Headline (value proposition, keywords, impact)
- About section (storytelling, keywords, call-to-action)
- Custom URL (clean, professional)

**Professional Story**
- Experience section (completeness, achievements, metrics)
- Education (relevance, completeness)
- Skills (relevance, endorsements count, top 3 pinned)
- Certifications (industry relevance, credibility)
- Recommendations (quantity, quality, recency)

**Visibility & Engagement**
- Featured section (portfolio, links, media)
- Activity/posts (frequency, engagement rates)
- Followers count
- Connections (500+ indicator)
- Publications and articles

**Network Signals**
- Groups membership
- Newsletter subscriptions
- Interests followed

### Step 3: Score Profile Elements

Use the scoring framework from `references/scoring_framework.md` to evaluate each element.

**Scoring Categories (1-10 scale):**

| Category | Weight | Key Factors |
|----------|--------|-------------|
| Visual Identity | 15% | Photo quality, banner relevance, visual consistency |
| Headline | 15% | Value proposition, keywords, memorability |
| About Section | 15% | Story structure, keywords, CTA |
| Experience | 20% | Completeness, achievements, metrics |
| Skills & Endorsements | 10% | Relevance, endorsement count |
| Recommendations | 10% | Quality, diversity, recency |
| Activity & Content | 15% | Posting frequency, engagement rate |

**Overall Score Interpretation:**
- 90-100: Elite (Top 1% of LinkedIn profiles)
- 80-89: Excellent (Strong personal brand)
- 70-79: Good (Solid foundation, room for improvement)
- 60-69: Average (Missing key optimizations)
- Below 60: Needs Work (Significant improvements required)

### Step 4: Analyze Key Metrics

Track and benchmark these metrics (see `references/metrics_benchmarks.md`):

**Visibility Metrics**
- Profile views (weekly/monthly trend)
- Search appearances
- Post impressions

**Engagement Metrics**
- Engagement rate (target: 2-8% for B2B)
- Comments per post
- Share rate

**⚠️ MANDATORY: Calculate Actual Engagement Rate**

You MUST calculate and report the engagement rate, not just show raw numbers:

```
Engagement Rate = (Reactions + Comments + Shares) / Impressions × 100
```

**Example Calculation:**
```
Post data: 1,376 impressions, 15 reactions, 1 comment, 0 shares
Engagement Rate = (15 + 1 + 0) / 1,376 × 100 = 1.16%

Interpretation: 🟡 Average (1-2%) - needs improvement
Target: 3%+ for good engagement
```

**Always include in the report:**
| Metric | Raw Value | Calculated | Benchmark | Status |
|--------|-----------|------------|-----------|--------|
| Engagement Rate | 16 interactions / 1,376 impressions | **1.16%** | 3%+ | 🟡 Below target |

**Growth Metrics**
- Follower growth rate (target: 10%+ monthly)
- Connection acceptance rate (target: 40%+)

**⚠️ MANDATORY: Social Selling Index (SSI)**

The SSI score is critical for measuring LinkedIn effectiveness. You MUST either:

**Option A - User provides SSI:**
Ask user to visit `linkedin.com/sales/ssi` and share their score, then document:
```
| SSI Component | Score | Target |
|---------------|-------|--------|
| Establish professional brand | X/25 | 20+ |
| Find the right people | X/25 | 15+ |
| Engage with insights | X/25 | 18+ |
| Build relationships | X/25 | 18+ |
| **TOTAL SSI** | **X/100** | **70+** |
```

**Option B - SSI not available:**
If user cannot access SSI, document in report:
```
**SSI Score:** Not available (user should visit linkedin.com/sales/ssi to check)
**Estimated SSI Range:** [X-Y] based on profile completeness and activity
```

**SSI Estimation Guide (when actual score unavailable):**
| Profile Characteristics | Estimated SSI |
|------------------------|---------------|
| All-Star profile + active posting + engaged network | 70-85 |
| Complete profile + regular posting | 55-70 |
| Basic profile + occasional activity | 40-55 |
| Incomplete profile + minimal activity | Below 40 |

### Step 4b: Advanced Analysis Areas

**Keyword/SEO Analysis**
- Identify target keywords for user's industry/role
- Check keyword presence in: Headline, About, Experience, Skills
- Assess search visibility for target terms
- Recommend keyword additions for discoverability

**Profile Completeness Check**
- [ ] Profile photo uploaded
- [ ] Custom banner image
- [ ] Headline customized (not just job title)
- [ ] About section filled (500+ characters)
- [ ] Current position with description
- [ ] 2+ past positions
- [ ] Education listed
- [ ] 5+ skills added
- [ ] Location set
- [ ] Industry selected
→ All checked = LinkedIn "All-Star" profile status

**Multilingual Profile Analysis** (if applicable)
- Primary language alignment with target audience
- Secondary language profile completeness
- Consistency across language versions
- Keyword optimization in both languages
- Recommendation: Keep both versions equally updated

**LinkedIn Features Assessment**
| Feature | Status | Recommendation |
|---------|--------|----------------|
| Creator Mode | On/Off | Enable if posting 3+/week |
| Open to Work | On/Off | Enable if job seeking (visible to recruiters only) |
| Providing Services | On/Off | Enable if freelancer/consultant |
| Newsletter | On/Off | Consider if 1000+ followers |
| Custom URL | Set/Default | Always customize |
| Verification Badge | Yes/No | Add if available |

**Network Quality Assessment**
- Connection diversity (industries, roles, seniority)
- Percentage of 1st-degree connections in target audience
- Key influencers/decision-makers in network
- Group membership relevance

### Step 5: Generate Recommendations

Provide actionable recommendations using the priority framework:

**Priority Matrix:**
- **Quick Wins** (High impact, Low effort): Do immediately
- **Strategic Initiatives** (High impact, High effort): Plan carefully
- **Nice-to-haves** (Low impact, Low effort): Do when possible
- **Avoid** (Low impact, High effort): Not worth resources

**Recommendation Categories:**

1. **Profile Optimization**
   - Photo and banner improvements
   - Headline rewriting
   - About section restructuring
   - Skills reorganization

2. **Content Strategy**
   - Posting frequency (target: 3x/week minimum)
   - Content pillars definition
   - Best posting times
   - Content formats (carousels, videos, polls)

3. **Engagement Strategy**
   - Comment engagement tactics
   - Network growth approaches
   - Recommendation requests
   - Group participation

4. **Visibility Enhancement**
   - Keyword optimization
   - Featured section curation
   - Publication strategy
   - Creator mode activation

### Step 6: Create Actionable Report

**⚠️ MANDATORY: Pre-Report Validation Checklist**

Before generating any audit report, verify ALL mandatory fields are completed:

```
□ Industry/Sector identified and documented
□ Profile Type classified (Employee/Consultant/Freelancer/Entrepreneur/Job Seeker)
□ Target Audience identified (Recruiters/Clients/Peers/Investors/Partners)
□ Engagement Rate CALCULATED (not just raw numbers)
□ SSI Score captured OR noted as unavailable with estimation
□ Industry-specific benchmarks applied (from metrics_benchmarks.md)
```

**If any field is missing, go back and complete it before proceeding.**

Generate output using templates from `assets/`:

**Report Sections:**
1. Executive Summary
2. **Mandatory Classification (Industry, Profile Type, Target Audience)**
3. Profile Score Card
4. **Mandatory Calculated Metrics (Engagement Rate, SSI)**
5. Element-by-Element Analysis
6. Quick Wins (Immediate Actions)
7. Strategic Recommendations
8. 30-60-90 Day Action Plan

## Profile Element Best Practices

### Profile Photo
- High-quality headshot (400x400px minimum)
- Professional attire appropriate to industry
- Friendly, approachable expression
- Clean, neutral background
- Face occupies 60-70% of frame
- Good lighting (natural preferred)

### Banner Image (1584x396px)
- Branded or industry-relevant imagery
- Include value proposition or tagline
- Showcase expertise or work
- Use brand colors if applicable
- Avoid clutter and small text

### Headline (220 characters max)
**Formula:** Who you are + What problems you solve + Benefits you provide

**Bad:** "Marketing Manager"
**Good:** "Marketing Manager | Helping B2B Companies Grow Through Data-Driven Strategies | 45% Revenue Increase Specialist"

**Industry-Specific Examples:**

| Industry | Example Headline |
|----------|------------------|
| **Tech** | "Senior Software Engineer | Building Scalable Systems at Fortune 500s | Python, AWS, Distributed Systems" |
| **Finance** | "Investment Analyst | Helping Family Offices Navigate Alternative Investments | CFA Charterholder" |
| **Healthcare** | "Nurse Practitioner | Improving Patient Outcomes Through Preventive Care | 15+ Years Emergency Medicine" |
| **Legal** | "Corporate Attorney | M&A and Securities for Growth-Stage Companies | Former BigLaw, Now Founder-Friendly" |
| **HR** | "Talent Acquisition Leader | Building World-Class Engineering Teams | Hired 200+ Engineers at Scale-Ups" |
| **Sales** | "Enterprise Account Executive | Helping CFOs Reduce Costs by 30% | $5M+ Annual Quota Achiever" |
| **Creative** | "UX Designer | Making Complex Products Simple | Design Systems, User Research, Accessibility" |
| **Consulting** | "Strategy Consultant | Helping Retailers Increase Revenue 25%+ | Former McKinsey, Now Independent" |
| **Nonprofit** | "Development Director | Raising $10M+ Annually for Education Equity | Grant Writing, Major Gifts" |
| **Startup** | "Founder & CEO @ [Company] | Helping SMBs Automate Operations | Ex-Google, 2x Founder" |

**Include:**
- Primary role/expertise
- Target audience
- Key differentiator or result
- Relevant keywords

### About Section (2,600 characters max)
**Structure (Problem-Solution-Proof-CTA):**
1. Hook (first 2-3 lines visible before "see more")
2. Your story/journey
3. What you do and who you help
4. Key achievements with metrics
5. Skills and expertise
6. Call-to-action

**Tips:**
- Write in first person
- Use short paragraphs
- Include relevant keywords
- Add emojis sparingly for visual breaks
- End with clear CTA

### Experience Section
For each role include:
- Quantified achievements (%, $, #)
- Scope of responsibility
- Key projects and outcomes
- Skills demonstrated
- Media attachments if relevant

### Skills Section
- List 50+ relevant skills
- Pin top 3 most important skills
- Request endorsements from colleagues
- Align with target job keywords

### Featured Section
Curate 3-6 items:
- Portfolio pieces
- Case studies
- Articles/publications
- Media appearances
- Key achievements
- Lead magnets or "work with me" links

### Services Section (for Consultants/Freelancers)
If user offers services:
- List 3-5 core service offerings
- Use keyword-rich service names
- Ensure services align with headline positioning
- Link to service page if available

### Content Performance Patterns
Analyze the user's posting history to identify:
- **Best-performing content types** (text, carousel, video, poll)
- **Optimal posting times** based on their engagement data
- **Topic resonance** - which subjects get most engagement
- **Hook effectiveness** - first-line patterns that work
- **CTA performance** - which calls-to-action drive action

Calculate actual engagement rate:
```
Engagement Rate = (Total Reactions + Comments + Shares) / Impressions × 100
```

Benchmark: 2-5% is good, 5-8% is excellent, 8%+ is exceptional

## Reference Files

### `references/scoring_framework.md`
Detailed scoring criteria for each profile element with examples and benchmarks.

**When to load**: For any profile audit or analysis requiring detailed scoring.

### `references/metrics_benchmarks.md`
Industry benchmarks for LinkedIn metrics including SSI scores, engagement rates, and growth targets.

**When to load**: When analyzing metrics or setting targets for improvement.

### `references/content_strategy.md`
Content pillars, posting schedules, format recommendations, and engagement tactics.

**When to load**: When developing content strategy or analyzing posting performance.

## Asset Templates

### `assets/profile_audit_template.md`
Complete profile audit report template with scoring cards and recommendations.

### `assets/quick_review_template.md`
Rapid assessment checklist with priority actions.

### `assets/action_plan_template.md`
30-60-90 day improvement roadmap template.

## Usage Examples

### Example 1: Full Profile Audit
**User:** "Analyze my LinkedIn profile and give me recommendations"
**Steps:**
1. User has their LinkedIn profile open in Chrome
2. Call `mcp__chrome-devtools__list_pages` → find pageId for LinkedIn tab
3. Call `mcp__chrome-devtools__select_page` with pageId
4. Call `mcp__chrome-devtools__take_snapshot` → extract profile structure with UIDs
5. Call `mcp__chrome-devtools__take_screenshot` → analyze photo and banner visually
6. Load `references/scoring_framework.md` for scoring criteria
7. Score each profile element (Visual, Headline, About, Experience, Skills, etc.)
8. Load `references/metrics_benchmarks.md` for industry comparison
9. Use `assets/profile_audit_template.md` for report format
10. Provide prioritized recommendations with quick wins first

### Example 2: Headline Optimization
**User:** "Help me improve my LinkedIn headline"
**Steps:**
1. Call `mcp__chrome-devtools__take_snapshot` → find headline in accessibility tree
2. Extract current headline text from snapshot
3. Identify target audience and value proposition from profile context
4. Apply headline formula from SKILL.md (Who + Problems Solved + Benefits)
5. Provide 3-5 optimized alternatives with keywords
6. Include industry-specific examples

### Example 3: Content Strategy
**User:** "Help me create a LinkedIn content strategy"
**Steps:**
1. Call `mcp__chrome-devtools__navigate_page` (url: linkedin.com/in/[user]/recent-activity/)
2. Call `mcp__chrome-devtools__wait_for` (text: "reactions") → wait for posts to load
3. Call `mcp__chrome-devtools__take_snapshot` → extract recent posts data
4. Analyze posting patterns and engagement metrics
5. Load `references/content_strategy.md` for strategy framework
6. Define content pillars based on expertise
7. Create posting schedule with optimal times
8. Set engagement targets based on industry benchmarks

### Example 4: Quick Profile Check
**User:** "Take a quick look at my LinkedIn profile"
**Steps:**
1. Call `mcp__chrome-devtools__list_pages` → find LinkedIn tab
2. Call `mcp__chrome-devtools__select_page` → focus the tab
3. Call `mcp__chrome-devtools__take_snapshot` → quick structure scan
4. Check key elements (photo, headline, about, experience) in snapshot
5. Use `assets/quick_review_template.md` for rapid assessment
6. Provide top 5 quick wins with specific actions

### Example 5: Deep Analytics Review
**User:** "Analyze my LinkedIn analytics and engagement metrics"
**Steps:**
1. Call `mcp__chrome-devtools__navigate_page` (url: "https://www.linkedin.com/analytics/")
2. Call `mcp__chrome-devtools__wait_for` (text: "Profile viewers") → verify dashboard loads
3. Call `mcp__chrome-devtools__take_snapshot` → capture analytics overview
4. Navigate to SSI: `mcp__chrome-devtools__navigate_page` (url: "https://www.linkedin.com/sales/ssi")
5. Call `mcp__chrome-devtools__wait_for` (text: "Social Selling Index") → check access
6. Call `mcp__chrome-devtools__take_snapshot` → capture SSI scores (or note unavailable)
7. Navigate back to Activity to analyze recent posts
8. Calculate engagement rate from visible metrics using formula
9. Compare against industry benchmarks from `references/metrics_benchmarks.md`
10. Provide improvement recommendations with specific targets

## Chrome DevTools MCP Workflows

### Step-by-Step: Extracting Profile Data

```
Step 1: Get browser tabs
→ mcp__chrome-devtools__list_pages
→ Response includes array of pages with: pageId, url, title
→ Find page where url contains "linkedin.com/in/"

Step 2: Select LinkedIn tab
→ mcp__chrome-devtools__select_page (pageId: [found_id])
→ Page is now the active context for subsequent operations

Step 3: Take accessibility snapshot
→ mcp__chrome-devtools__take_snapshot
→ Returns text representation of page with element UIDs like [uid1], [uid2]
→ UIDs are used for click, hover, and other interactions

Step 4: Take screenshot for visual analysis
→ mcp__chrome-devtools__take_screenshot
→ Returns image of current viewport
→ Analyze profile photo quality, banner design, visual branding

Step 5: Extract specific text (optional)
→ mcp__chrome-devtools__evaluate_script
→ function: "() => document.body.innerText"
→ Returns all visible text on page
```

### Step-by-Step: Navigating Profile Sections

LinkedIn lazy-loads content. To access sections below the fold:

```
Step 1: Take initial snapshot
→ mcp__chrome-devtools__take_snapshot
→ Identify UID for section you need (e.g., "Skills" heading)

Step 2: Scroll to section
→ mcp__chrome-devtools__hover (uid: "[skills_uid]")
→ OR mcp__chrome-devtools__click (uid: "[show_more_uid]")
→ Element scrolls into view

Step 3: Wait for content to load
→ mcp__chrome-devtools__wait_for (text: "Show all", timeout: 5000)
→ LinkedIn AJAX content finishes loading

Step 4: Re-snapshot for new content
→ mcp__chrome-devtools__take_snapshot
→ Now includes previously hidden elements
```

### Step-by-Step: Analyzing Activity/Posts

```
Step 1: Navigate to Activity section
→ From profile, find "Activity" or "Posts" link UID in snapshot
→ mcp__chrome-devtools__click (uid: "[activity_uid]")
→ OR mcp__chrome-devtools__navigate_page (url: "linkedin.com/in/[username]/recent-activity/")

Step 2: Wait for posts to load
→ mcp__chrome-devtools__wait_for (text: "reactions", timeout: 5000)

Step 3: Snapshot activity page
→ mcp__chrome-devtools__take_snapshot
→ Extract post content, reaction counts, comment counts

Step 4: Calculate engagement metrics
→ For each visible post: (reactions + comments + reposts) / impressions × 100
→ Note: Impressions may not be visible to non-authors
```

### Step-by-Step: Accessing LinkedIn Analytics Dashboard

LinkedIn Analytics provides key metrics only visible to the profile owner.

```
Step 1: Navigate to Analytics
→ mcp__chrome-devtools__navigate_page (url: "https://www.linkedin.com/analytics/")

Step 2: Wait for dashboard to load
→ mcp__chrome-devtools__wait_for (text: "Profile viewers", timeout: 10000)
→ If timeout: User may not have analytics access - ask them to navigate manually

Step 3: Capture analytics snapshot
→ mcp__chrome-devtools__take_snapshot
→ Extract: Profile views (7d, 90d), Post impressions, Search appearances, Follower count

Step 4: Navigate to detailed views (optional)
→ Click "Profile viewers" UID for viewer demographics
→ Click "Post impressions" UID for content performance breakdown
→ Click "Search appearances" UID for keyword visibility
```

### Step-by-Step: Capturing SSI Score

The Social Selling Index is a key LinkedIn metric (mandatory in audits).

```
Step 1: Navigate to SSI page
→ mcp__chrome-devtools__navigate_page (url: "https://www.linkedin.com/sales/ssi")

Step 2: Check for access
→ mcp__chrome-devtools__wait_for (text: "Social Selling Index", timeout: 5000)
→ If timeout: SSI may require Sales Navigator - document as unavailable

Step 3: Capture SSI data
→ mcp__chrome-devtools__take_snapshot
→ Extract: Overall score (/100), 4 component scores (/25 each)
→ Components: Professional Brand, Find Right People, Engage Insights, Build Relationships

Step 4: Capture rankings (if visible)
→ Industry rank, Network rank (percentile position)
```

### Step-by-Step: Individual Post Analytics

For detailed engagement data on specific posts (author-only view).

```
Step 1: From Activity page, find target post
→ mcp__chrome-devtools__take_snapshot
→ Locate post by content or date in the snapshot

Step 2: Click to view post details
→ mcp__chrome-devtools__click (uid: "[post_uid]")
→ OR click "View analytics" link UID if visible

Step 3: Wait for analytics overlay
→ mcp__chrome-devtools__wait_for (text: "impressions", timeout: 5000)

Step 4: Capture post-level metrics
→ mcp__chrome-devtools__take_snapshot
→ Extract: Impressions, Unique views, Reactions (by type), Comments, Reposts
→ Extract: Top companies, Top job titles (viewer demographics)
```

### Step-by-Step: Follower Analytics

For audience understanding and growth tracking.

```
Step 1: Navigate to Follower Analytics
→ mcp__chrome-devtools__navigate_page (url: "https://www.linkedin.com/analytics/profile-viewers/followers/")
→ OR from Analytics dashboard, click "Followers" tab UID

Step 2: Wait for data to load
→ mcp__chrome-devtools__wait_for (text: "followers", timeout: 5000)

Step 3: Capture follower data
→ mcp__chrome-devtools__take_snapshot
→ Extract: Total followers, Growth (7d, 30d), Top companies, Top job titles, Top locations

Step 4: Scroll for historical data (if needed)
→ mcp__chrome-devtools__hover (uid: "[chart_uid]") to scroll down
→ Re-snapshot to capture growth chart data
```

### Playwright MCP Fallback

If Chrome DevTools MCP is unavailable, use Playwright MCP:

| Chrome DevTools | Playwright Equivalent |
|-----------------|----------------------|
| `mcp__chrome-devtools__list_pages` | `mcp__playwright__browser_tabs` action: "list" |
| `mcp__chrome-devtools__select_page` | `mcp__playwright__browser_tabs` action: "select" |
| `mcp__chrome-devtools__take_snapshot` | `mcp__playwright__browser_snapshot` |
| `mcp__chrome-devtools__take_screenshot` | `mcp__playwright__browser_take_screenshot` |
| `mcp__chrome-devtools__navigate_page` | `mcp__playwright__browser_navigate` |
| `mcp__chrome-devtools__click` | `mcp__playwright__browser_click` |
| `mcp__chrome-devtools__hover` | `mcp__playwright__browser_hover` |
| `mcp__chrome-devtools__wait_for` | `mcp__playwright__browser_wait_for` |

### Error Handling Patterns

| Error | Detection | Recovery |
|-------|-----------|----------|
| LinkedIn tab not found | `list_pages` returns no matching URL | Ask user: "Please open your LinkedIn profile in Chrome" |
| Element UID not in snapshot | Click/hover fails with invalid UID | Re-take snapshot, search for alternative element |
| Content not loading | `wait_for` times out | Scroll manually, increase timeout, try page refresh |
| Rate limited by LinkedIn | Page shows CAPTCHA or error | Pause 30+ seconds, inform user, proceed slowly |
| SSI page requires Sales Navigator | linkedin.com/sales/ssi shows paywall | Note as "SSI unavailable" and provide estimation based on profile |
| Profile is private | Snapshot shows limited content | Document as "Limited visibility - private profile" |
| Analytics page access denied | Page shows "upgrade" or paywall | Note limited metrics access, use visible profile data only |
| Post analytics not available | No "View analytics" option on post | User is not post author - can only see public engagement counts |
| Follower data unavailable | Analytics follower tab empty or restricted | Use visible follower count from profile, note demographics unavailable |

## Tips for Effective Analysis

1. **Use Chrome DevTools MCP**: Ensure the user has LinkedIn open in Chrome before starting analysis
2. **List Pages First**: Always call `mcp__chrome-devtools__list_pages` to verify LinkedIn tab exists
3. **Snapshot Before Actions**: Always `take_snapshot` before clicking or hovering - you need UIDs
4. **Visual + Text Analysis**: Combine `take_screenshot` for visual analysis with `take_snapshot` for text
5. **Handle Lazy Loading**: LinkedIn loads content on scroll - use `hover` to scroll, then re-snapshot
6. **Consider Industry Context**: Benchmarks vary by industry and role - always classify first
7. **Focus on Quick Wins**: Prioritize high-impact, low-effort improvements first
8. **Be Specific**: Provide concrete examples and rewrites, not just general advice
9. **Set Measurable Goals**: Include specific targets for metrics improvement
10. **Handle Private Metrics**: Some metrics (profile views, SSI) are only visible to profile owner
11. **Respect Rate Limits**: Avoid rapid navigation that might trigger LinkedIn's bot detection
12. **Use Playwright Fallback**: If Chrome DevTools MCP fails, fall back to `mcp__playwright__*` tools

## Industry-Specific Guidance

**This skill works for ANY professional profile.** Always identify the user's industry context first to apply relevant benchmarks.

### Step 1: Identify Industry Context

Ask or infer from the profile:
- What industry/sector?
- B2B, B2C, or internal-facing?
- Employee, consultant/freelancer, or entrepreneur?
- Target audience (recruiters, clients, peers, investors)?

### Step 2: Apply Relevant Benchmarks

The `references/metrics_benchmarks.md` file contains benchmarks for 15+ industries:

| Category | Industries Covered |
|----------|-------------------|
| Technology | Software, Web3/Blockchain, Data Science |
| Business | Finance, Consulting, Sales, Marketing |
| Professional | Legal, Healthcare, HR, Education |
| Creative | Design, Creative, Media |
| Other | Manufacturing, Nonprofit, Real Estate, Startups |

### Step 3: Adjust Recommendations

Different industries have different norms:

| Factor | Conservative Industries | Progressive Industries |
|--------|------------------------|------------------------|
| **Tone** | Formal, reserved | Casual, personable |
| **Photo** | Traditional headshot | Can be more creative |
| **Content** | Thought leadership, insights | Stories, behind-the-scenes |
| **Posting** | 2-3x/week | 4-5x/week |
| **Emojis** | Minimal | Acceptable |
| **Examples** | Legal, Finance, Healthcare | Tech, Marketing, Startups |

### Industry Detection Cues

Look for these signals in the profile:
- Job titles and company types
- Skills listed
- Content topics
- Industry groups
- Certifications
- Education background

## Competitor Analysis Workflow

When conducting competitive analysis for positioning:

### Step 1: Identify Aspirational Profiles
Ask user to provide 3-5 LinkedIn profiles of:
- Direct competitors
- Industry leaders they admire
- People in similar roles with strong presence

### Step 2: Analyze Each Profile
For each competitor, capture:
- Headline structure and keywords
- About section hook and CTA
- Content frequency and formats
- Engagement levels (reactions, comments)
- Follower count and growth

### Step 3: Gap Analysis
Create comparison table showing:
- Where user is stronger
- Where competitors excel
- Specific elements to replicate/adapt

### Step 4: Differentiation Strategy
Recommend how user can:
- Match competitor strengths
- Differentiate with unique positioning
- Capitalize on untapped opportunities

## Visual Analysis Criteria

When analyzing profile photos and banners:

### Profile Photo Scoring (0-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Professional headshot, perfect lighting, confident expression, clean background, face fills 60-70% of frame |
| 7-8 | Good quality, professional appearance, minor improvements possible |
| 5-6 | Acceptable but dated, lighting issues, or unprofessional background |
| 3-4 | Low quality, inappropriate setting, or face not clearly visible |
| 1-2 | No photo, logo instead of face, or severely inappropriate |

**Red Flags:**
- Cropped from group photos
- Sunglasses or obscured face
- Outdated (>5 years old)
- Poor lighting/resolution
- Distracting background

### Banner Image Scoring (0-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Custom branded banner with value proposition, professional design, proper dimensions (1584×396) |
| 7-8 | Custom image, relevant to role/industry, minor optimization possible |
| 5-6 | Generic image, somewhat relevant but no branding or messaging |
| 3-4 | Default LinkedIn background or low-quality image |
| 1-2 | Distracting, inappropriate, or broken/stretched image |

**Effective Banner Elements:**
- Clear value proposition text
- Brand colors if applicable
- Relevant imagery (industry, role, achievements)
- Contact info or CTA (optional)
- Professional design quality

## Handling Multilingual Profiles

When user has profiles in multiple languages:

### Analysis Approach
1. Identify primary language (where most connections are)
2. Analyze both versions for completeness
3. Check consistency across languages
4. Ensure keywords optimized for each language market

### Recommendations Format
Provide recommendations for:
- **Primary language profile**: Full optimization
- **Secondary language profile**: Key gaps to address
- **Content strategy**: Which language to post in (consider audience split)

### Common Multilingual Issues
- Secondary profile is outdated
- Keywords not localized
- About section only translated, not adapted
- Different positioning across languages (confusing)
