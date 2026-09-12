---
name: page-cro
description: |
  Audits existing landing pages for conversion rate optimization. Scores hero section, CTA placement, social proof, objection handling, and form friction on a 1-10 scale. Use when someone says 'audit my landing page', 'improve conversions', 'why isn't my page converting', 'CRO audit', 'landing page feedback', 'optimize my signup page', 'page review', 'conversion rate', 'bounce rate is high', 'nobody is signing up', or anything about improving an existing page's performance. Even if they just share a URL and say 'what do you think' or 'how can I improve this' — if there's a page involved and conversion matters, this is the skill. Always use this over generic advice when an actual page exists to audit.
allowed-tools: []
---

# Page CRO (Conversion Rate Optimization)

## Purpose

Take any landing page and audit it for conversion leaks. Score each element, prioritize fixes by impact, and provide ready-to-implement copy and layout changes. No vague advice — specific rewrites and structural fixes.

## Reads

- `brand/audience.md` — Target personas, pain points, buying triggers
- `brand/positioning.md` — Value props, differentiators, proof points
- `brand/voice-profile.md` — Brand voice for copy rewrites

## Brand Integration

- **audience.md** — Scoring thresholds shift by persona. A developer audience tolerates minimal social proof; a non-technical buyer needs more hand-holding. Pain points from audience.md inform which objections the page should address — unaddressed objections are the most common conversion killer.
- **positioning.md** — Every copy rewrite must reinforce the positioning angle. If the brand differentiates on speed, the hero rewrite should lead with speed. Proof points from positioning.md become the social proof recommendations.
- **voice-profile.md** — All before/after copy rewrites match the brand voice. A playful brand gets different CTA copy than a professional brand.

## Workflow

### Step 1: Capture the Page

Get the page content. Try these in order:
1. **User provides URL** — Use WebFetch or browser tool to get the rendered page
2. **User provides HTML/markdown** — Work with what's given
3. **User describes the page** — Ask for the actual page content before auditing; descriptions alone produce weak audits

If the page is behind authentication, ask the user to paste the HTML or provide screenshots.

Extract and map:
- Hero section (headline, subheadline, CTA)
- Navigation and header
- Each content section in scroll order
- All CTAs (primary, secondary, inline)
- Social proof elements (testimonials, logos, stats)
- Forms and their fields
- Footer and secondary navigation
- Page load performance indicators

### Step 2: Run the Audit

Score each element 1-10 with specific reasoning.

#### Hero Section Audit

| Check | What to look for |
|-------|-----------------|
| Headline clarity | Does it pass the 5-second test? Can a stranger understand what you do? |
| Specificity | Numbers, outcomes, timeframes > vague claims |
| Subheadline | Expands on HOW, not just restates the headline |
| Hero CTA | Single, clear, action-oriented. Not "Submit" or "Learn More" |
| Visual | Supports the message, not decorative stock photos |
| Above-fold completeness | Headline + value prop + CTA + credibility signal all visible without scrolling |

**5-Second Test:** If someone sees only the above-fold content for 5 seconds, can they answer:
1. What does this product do?
2. Who is it for?
3. Why should I care?
4. What do I do next?

#### CTA Audit

| Check | What to look for |
|-------|-----------------|
| Primary CTA count | One primary action per page. Multiple = decision paralysis |
| CTA copy | Action verb + outcome. "Start free trial" > "Sign up" > "Submit" |
| CTA contrast | Visually dominant, not competing with other elements |
| CTA frequency | Appears after every major content section |
| CTA anxiety reducers | "No credit card required", "Cancel anytime", "2-minute setup" |
| Secondary CTA | Lower-commitment alternative for not-ready visitors |

#### Social Proof Audit

| Check | What to look for |
|-------|-----------------|
| Testimonial specificity | Named person + role + company + specific result > anonymous quote |
| Logo bar | Recognizable brands, 5-8 logos, "Trusted by" framing |
| Stats | Specific numbers ("12,847 teams" not "thousands of teams") |
| Case studies | At least one detailed success story linked |
| Review scores | G2, Capterra, Product Hunt badges if applicable |
| Placement | Social proof appears before the main CTA, not buried at bottom |

#### Objection Handling Audit

| Check | What to look for |
|-------|-----------------|
| Price objection | ROI framing, comparison anchoring, money-back guarantee |
| Trust objection | Security badges, compliance logos, data handling statement |
| Effort objection | "Setup in 5 minutes", migration assistance, onboarding help |
| Switching objection | Import tools, comparison with current solution |
| FAQ section | Addresses top 5-7 real objections, not softballs |

#### Form Friction Audit

| Check | What to look for |
|-------|-----------------|
| Field count | Every field above 3 reduces conversion. Justify each field |
| Required vs optional | Mark optional fields or remove them |
| Field labels | Above the field, not placeholder text that disappears |
| Error handling | Inline validation, specific error messages |
| Multi-step | If >4 fields, break into steps with progress indicator |
| Social login | Google/GitHub/SSO options reduce friction |

### Step 3: Score and Prioritize

Generate a priority matrix. Score each of the 5 audit areas 1-10 (hero, CTA, social proof, objection handling, form friction). Sum them, multiply by 2 to get a /100 score. Then assign priority based on impact and effort:

```
## CRO Audit Score: [X]/100

| Element | Score | Impact | Effort | Priority |
|---------|-------|--------|--------|----------|
| Hero headline | 4/10 | High | Low | P0 |
| CTA copy | 3/10 | High | Low | P0 |
| Social proof | 5/10 | High | Medium | P1 |
| Form friction | 6/10 | Medium | Medium | P2 |
| Objection handling | 2/10 | High | Medium | P1 |

Priority ranking: High impact + Low effort = P0, High impact + Medium effort = P1, everything else = P2
```

### Step 4: Generate Recommendations

For each P0 and P1 issue, provide:

```markdown
### Issue: [Element] — Score [X/10]

**Problem:** [Specific description of what's wrong]

**Before:**
> [Exact current copy/structure]

**After:**
> [Rewritten copy/structure]

**Why this works:** [Psychology principle or data point backing the change]

**Expected impact:** [Estimated conversion lift range]
```

### Step 5: Provide Implementation Checklist

```markdown
## Implementation Priority

### This Week (P0 — High Impact, Low Effort)
- [ ] Rewrite hero headline to [specific suggestion]
- [ ] Change CTA from "[current]" to "[suggested]"
- [ ] Add anxiety reducer below primary CTA

### Next Sprint (P1 — High Impact, Medium Effort)
- [ ] Add 3 specific testimonials with results
- [ ] Create FAQ section addressing [top objections]
- [ ] Add logo bar above the fold

### Backlog (P2 — Medium Impact)
- [ ] Reduce form fields from [X] to [Y]
- [ ] Add secondary CTA for lower-commitment action
- [ ] Implement exit-intent offer
```

## Key Frameworks

### AIDA (Attention-Interest-Desire-Action)
- **Attention:** Headline that stops the scroll
- **Interest:** Subheadline that creates curiosity
- **Desire:** Benefits, social proof, and outcomes that build want
- **Action:** Clear, low-friction CTA

### PAS (Problem-Agitate-Solve)
- **Problem:** Name the specific pain point
- **Agitate:** Amplify the consequences of not solving it
- **Solve:** Present your product as the resolution

### Above-the-Fold Checklist
Everything visible without scrolling must include:
1. Clear headline (what you do)
2. Subheadline (how/why it matters)
3. Primary CTA (what to do next)
4. One credibility signal (logo bar, stat, or testimonial)
5. Relevant visual (product screenshot > stock photo)

## CTA Copy Formulas

| Pattern | Example |
|---------|---------|
| Action + Outcome | "Start saving 10 hours/week" |
| Action + Timeframe | "Get started in 2 minutes" |
| Action + Risk Reversal | "Try free for 14 days" |
| Action + Specificity | "Build your first workflow" |

## Worked Example

- **Hero: 7/10** — Headline is benefit-focused but subhead is too long. Recommend: cut to 8 words.
- **CTA: 5/10** — Generic 'Sign Up' button. Recommend: 'Start your free trial' with benefit reinforcement.
- **Social Proof: 3/10** — No testimonials above fold. Recommend: add 1-2 customer quotes near CTA.

## Anti-Patterns

- Don't suggest a complete page redesign — focus on conversion fixes within the existing structure
- Don't critique branding, aesthetics, or color choices unless they directly impact conversion (e.g., CTA blends into background)
- Don't provide vague advice ("improve the headline") — every recommendation must include specific rewrite copy
- Don't audit content/blog pages as if they were landing pages — different goals, different criteria
- Don't recommend tools or integrations the agent can't implement — stay within copy and structural changes
- Don't ignore mobile — flag any element that would break on small screens

## Edge Cases

- **Page behind auth:** Ask user to paste HTML or provide screenshots. Don't attempt to bypass login.
- **Blog/content page:** Shift criteria — evaluate for CTA to next step (newsletter, lead magnet), not for direct conversion. Skip form friction audit.
- **No clear CTA:** Flag as P0. The page needs a CTA before anything else matters.
- **Mobile-only page:** Prioritize tap target sizes, scroll depth, and thumb-zone placement in recommendations.

See `references/cro-benchmarks.md` for industry conversion rates, element-specific impact data, and A/B test planning benchmarks. Use these to ground scores and expected impact estimates in real numbers.

## Recommendation Psychology

Ground every recommendation in conversion psychology: social proof leverages conformity bias, anxiety reducers counter loss aversion, benefit-focused CTAs activate approach motivation. The 5-second test works because users form lasting first impressions in 50ms — if the value prop isn't instant, bounce rates spike.

## Output

The audit produces:
- Scored element breakdown with specific reasoning
- Prioritized recommendation list (P0/P1/P2)
- Before/after copy rewrites for every P0 and P1 item
- Implementation checklist ordered by impact/effort
- Framework references for each recommendation

## Quality Checks

- [ ] Every P0/P1 issue has a specific before/after rewrite, not vague advice
- [ ] Copy rewrites match brand voice (if voice-profile.md exists)
- [ ] Recommendations are achievable without a full redesign
- [ ] Mobile experience considered for all recommendations
- [ ] Prioritization reflects actual impact/effort, not just opinion
- [ ] Social proof recommendations reference specific proof types available to the brand
