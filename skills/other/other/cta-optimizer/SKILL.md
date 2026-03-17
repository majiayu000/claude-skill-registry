---
name: cta-optimizer
description: Design and optimize call-to-action buttons for maximum conversion. Covers copy psychology, visual design, placement strategy, and A/B testing guidance.
---

# CTA Optimizer Skill

Design call-to-action buttons and sections that drive action through psychology-driven copy, strategic placement, and visual prominence.

## When to Use

Use `/cta-optimizer` when you need to:
- Audit existing CTAs for effectiveness
- Write better CTA button copy
- Design visually prominent CTAs
- Determine optimal CTA placement
- Create CTA sections with supporting copy
- Plan A/B tests for CTAs

## Instructions

### Phase 1: Audit Existing CTAs

**Goal**: Identify weaknesses in current CTAs

**I will evaluate:**

1. **Visibility**
   - Color contrast ratio (≥ 4.5:1)?
   - Large enough (min 48x48px for mobile)?
   - Enough white space around it?
   - Stands out from page content?

2. **Copy**
   - Action-oriented verb?
   - States what user gets?
   - Specific vs vague?
   - Creates urgency (without manipulation)?

3. **Placement**
   - Above the fold?
   - After value demonstration?
   - Repeated at logical intervals?
   - Not competing with other CTAs?

4. **Visual Hierarchy**
   - Primary CTA most prominent?
   - Secondary CTAs clearly secondary?
   - Tertiary actions de-emphasized?

**Audit Checklist:**
```markdown
- [ ] Visible above fold?
- [ ] High contrast (primary color)?
- [ ] Large enough (48px+ height)?
- [ ] Copy is action-oriented ("Get", "Start", "Download")?
- [ ] States value ("Start Free Trial" not "Submit")?
- [ ] Reduces friction ("No Credit Card" disclaimer)?
- [ ] Mobile-friendly (thumb-reachable)?
- [ ] Only one primary CTA per screen?
```

---

### Phase 2: Optimize CTA Copy

**Goal**: Write compelling, action-driving CTA copy

### CTA Copy Formula

**Structure**: [Action Verb] + [What They Get] + [Friction Reducer]

**Examples:**

| ❌ Generic | ✅ Optimized |
|-----------|-------------|
| Submit | Start Free Trial - No Credit Card |
| Learn More | See How It Works |
| Sign Up | Get Instant Access |
| Download | Download the Free Guide |
| Click Here | Show Me the Playbook |
| Continue | Yes, Send Me Tips |
| Register | Join 10,000+ Marketers |
| Buy Now | Get Lifetime Access Today |

### Action Verbs by Goal

**Trial Signups:**
- Start, Begin, Try, Test, Explore, Experience

**Downloads:**
- Download, Get, Grab, Access, Claim

**Purchases:**
- Buy, Get, Unlock, Secure, Upgrade

**Email/Newsletter:**
- Subscribe, Join, Get, Receive, Send

**Demos/Calls:**
- Schedule, Book, Request, See, Watch

### Value Statements

**What user receives (not what they do):**
```markdown
❌ "Create Account" (what they do)
✅ "Get Free Access" (what they receive)

❌ "Enter Email" (what they do)
✅ "Send Me the Guide" (what they receive)

❌ "Submit Form" (what they do)
✅ "Get My Custom Quote" (what they receive)
```

### Friction Reducers

**Remove objections inline:**
```markdown
- "No Credit Card Required"
- "Free Forever"
- "Cancel Anytime"
- "Takes 2 Minutes"
- "No Spam, Ever"
- "Instant Access"
- "100% Free"
```

### Urgency (Ethical)

**Only use if true:**
```markdown
✅ Ethical urgency:
- "Limited Spots Available" (if truly limited)
- "Sale Ends Friday" (with real deadline)
- "Early Bird Pricing" (time-based)

❌ Fake urgency:
- "Only 2 left!" (always says 2)
- "Flash sale!" (runs every day)
- "Act now!" (no real urgency)
```

---

### Phase 3: Optimize CTA Design

**Goal**: Make CTAs visually prominent and appealing

### Color Psychology

**Best Practice**: Contrast > Specific Color

```css
/* ✅ Good - high contrast against background */
.ctaPrimary {
  background: #2563eb; /* Blue */
  color: #ffffff;
  /* Contrast ratio: 8.59:1 (AAA) */
}

/* ❌ Bad - low contrast */
.ctaBad {
  background: #93c5fd; /* Light blue */
  color: #ffffff;
  /* Contrast ratio: 1.93:1 (Fails WCAG) */
}
```

**Color Associations** (context-dependent):
- **Blue**: Trust, safety, professionalism
- **Green**: Success, go, positive action
- **Orange**: Friendly, energetic, call-to-action
- **Red**: Urgency, bold action, stop
- **Purple**: Premium, luxury, creativity

**Primary CTA Template:**

```css
.ctaPrimary {
  /* Size */
  min-height: 48px;
  padding: 14px 28px;
  min-width: 200px;

  /* Typography */
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  text-align: center;

  /* Visual */
  background: var(--color-primary, #2563eb);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);

  /* Interaction */
  cursor: pointer;
  transition: all 0.2s ease;
  -webkit-tap-highlight-color: transparent;
}

.ctaPrimary:hover {
  background: var(--color-primary-dark, #1d4ed8);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}

.ctaPrimary:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(37, 99, 235, 0.3);
}

.ctaPrimary:focus-visible {
  outline: 3px solid var(--color-primary-light, #60a5fa);
  outline-offset: 2px;
}

/* Mobile optimization */
@media (max-width: 640px) {
  .ctaPrimary {
    width: 100%;
    padding: 16px 24px;
    font-size: 17px; /* iOS prevents zoom at 16px+ */
  }
}
```

**Secondary CTA:**

```css
.ctaSecondary {
  min-height: 48px;
  padding: 14px 28px;

  font-size: 16px;
  font-weight: 600;

  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: 8px;

  cursor: pointer;
  transition: all 0.2s ease;
}

.ctaSecondary:hover {
  background: var(--color-primary);
  color: #ffffff;
}
```

**Ghost/Tertiary CTA:**

```css
.ctaTertiary {
  min-height: 48px;
  padding: 14px 20px;

  font-size: 16px;
  font-weight: 500;
  color: var(--color-text-secondary);

  background: transparent;
  border: none;

  text-decoration: underline;
  cursor: pointer;
  transition: color 0.2s ease;
}

.ctaTertiary:hover {
  color: var(--color-text);
}
```

### White Space

**Give CTAs room to breathe:**

```css
.ctaSection {
  padding: 48px 24px;
  text-align: center;
}

.ctaHeadline {
  margin-bottom: 16px;
  font-size: 32px;
  font-weight: 700;
}

.ctaSubtext {
  margin-bottom: 32px;
  font-size: 18px;
  color: var(--color-text-secondary);
}

.ctaButton {
  /* Isolated with white space */
  margin: 24px 0;
}

.ctaDisclaimer {
  margin-top: 12px;
  font-size: 14px;
  color: var(--color-text-muted);
}
```

---

### Phase 4: Optimize CTA Placement

**Goal**: Position CTAs where users are ready to act

### Placement Strategy

**Hero Section (Above Fold):**
```html
<section class="hero">
  <h1>Close deals 3x faster with AI-powered sales tools</h1>
  <p>Stop losing deals to slow follow-ups. Automate your outreach and focus on closing.</p>

  <div class="heroCtaGroup">
    <button class="ctaPrimary">Start Free Trial</button>
    <button class="ctaSecondary">Watch 2-Min Demo</button>
  </div>

  <p class="disclaimer">No credit card required • 14-day trial</p>
</section>
```

**After Value Demonstration:**
```html
<section class="features">
  <h2>Everything you need to scale sales</h2>

  <!-- Feature blocks -->
  <div class="featureGrid">
    <div class="feature">...</div>
    <div class="feature">...</div>
    <div class="feature">...</div>
  </div>

  <!-- CTA after showing value -->
  <div class="ctaSection">
    <h3>Ready to 3x your deals?</h3>
    <button class="ctaPrimary">Get Started Free</button>
  </div>
</section>
```

**Sticky Bottom Bar (Mobile):**

```css
.stickyCtaMobile {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

@media (min-width: 768px) {
  .stickyCtaMobile {
    display: none; /* Desktop has inline CTAs */
  }
}
```

**Before Footer:**
```html
<section class="finalCta">
  <h2>Join 10,000+ sales teams closing more deals</h2>
  <p>Start your free trial today - no credit card required</p>
  <button class="ctaPrimary">Get Started Free</button>

  <div class="socialProof">
    <div class="stars">★★★★★</div>
    <p>4.9/5 from 2,000+ reviews</p>
  </div>
</section>

<footer>
  <!-- Footer content -->
</footer>
```

### Placement Rules

**DO:**
- ✅ Place primary CTA above the fold
- ✅ Repeat CTA after value demonstrations
- ✅ Include CTA before footer
- ✅ Use sticky mobile CTA for long pages
- ✅ Place CTA near social proof

**DON'T:**
- ❌ Multiple primary CTAs on same screen
- ❌ CTA before explaining value
- ❌ Competing CTAs next to each other
- ❌ CTA in middle of reading flow

---

### Phase 5: CTA Sections with Supporting Copy

**Goal**: Frame CTAs with compelling context

### CTA Section Patterns

**Pattern 1: Question + Answer + CTA**
```html
<div class="ctaSection">
  <h3>Ready to close more deals with less effort?</h3>
  <p>Join 10,000+ sales teams who've 3x'd their pipeline</p>
  <button class="ctaPrimary">Start Free Trial</button>
  <p class="disclaimer">No credit card • Cancel anytime</p>
</div>
```

**Pattern 2: Social Proof + CTA**
```html
<div class="ctaSection">
  <div class="logoBar">
    <img src="google.svg" alt="Google" />
    <img src="microsoft.svg" alt="Microsoft" />
    <img src="salesforce.svg" alt="Salesforce" />
  </div>
  <h3>Join top companies using our platform</h3>
  <button class="ctaPrimary">Get Started Free</button>
</div>
```

**Pattern 3: Benefit List + CTA**
```html
<div class="ctaSection">
  <h3>Start your free trial and get:</h3>
  <ul class="benefits">
    <li>✓ Full access to all features</li>
    <li>✓ Personal onboarding session</li>
    <li>✓ Cancel anytime, no questions asked</li>
  </ul>
  <button class="ctaPrimary">Start Free Trial</button>
</div>
```

**Pattern 4: Urgency + CTA**
```html
<div class="ctaSection">
  <div class="urgencyBadge">Limited Time Offer</div>
  <h3>Get 50% off your first year</h3>
  <p>Offer ends Friday, May 31st</p>
  <button class="ctaPrimary">Claim Your Discount</button>
  <p class="countdown">Ends in 2 days, 14 hours</p>
</div>
```

---

## CTA Optimization Checklist

### Copy
- [ ] Uses action verb (Get, Start, Download, Join)?
- [ ] States what user receives (not what they do)?
- [ ] Specific vs vague ("Start Free Trial" not "Sign Up")?
- [ ] Includes friction reducer if needed?
- [ ] Creates urgency (only if ethical/true)?
- [ ] Consistent across page?

### Design
- [ ] High contrast against background (≥ 4.5:1)?
- [ ] Large enough for mobile (≥ 48px height)?
- [ ] Stands out visually (color, size, shadow)?
- [ ] Adequate white space around it?
- [ ] Clear hover/active states?
- [ ] Focus indicator visible?

### Placement
- [ ] Primary CTA above the fold?
- [ ] Repeated after value demos?
- [ ] Included before footer?
- [ ] Only one primary CTA per screen?
- [ ] Near social proof when possible?
- [ ] Sticky bar on mobile for long pages?

### Hierarchy
- [ ] Primary CTA most prominent?
- [ ] Secondary CTA clearly less prominent?
- [ ] Tertiary actions de-emphasized (text links)?
- [ ] No competing CTAs side-by-side?

### Mobile
- [ ] Touch target ≥ 48x48px?
- [ ] Full-width or centered appropriately?
- [ ] Text size prevents zoom (≥ 16px)?
- [ ] Thumb-reachable (bottom half preferred)?

---

## A/B Testing Guidance

### What to Test First (Highest Impact)

**1. CTA Copy** (Easiest, highest ROI)
- Test: "Get Started" vs "Start Free Trial"
- Test: With/without friction reducer
- Test: Benefit-focused vs action-focused

**2. CTA Color** (Easy, moderate ROI)
- Test: Primary brand color vs high-contrast alternative
- Test: Solid vs gradient backgrounds
- Must maintain contrast ratio

**3. CTA Placement** (Moderate difficulty, high ROI)
- Test: Above fold only vs repeated throughout
- Test: Sticky mobile bar vs inline only
- Test: Before vs after social proof

**4. CTA Size** (Easy, moderate ROI)
- Test: Standard (48px) vs large (60px)
- Test: Padding variations
- Test: Full-width vs auto-width

**5. Supporting Copy** (Moderate, moderate ROI)
- Test: With vs without subtext
- Test: Urgency messaging variations
- Test: Social proof placement

### Sample Hypothesis

```markdown
**Hypothesis**: Adding "No Credit Card Required" to CTA will increase trial signups by 15-25%

**Rationale**: Credit card requirement is #1 objection in surveys

**Test**:
- Control: "Start Free Trial"
- Variant: "Start Free Trial - No Credit Card Required"

**Success Metric**: Trial signup conversion rate
**Duration**: 2 weeks or 1,000 conversions
**Statistical Significance**: 95% confidence
```

---

## Output Format

```markdown
## CTA Optimization Report

### Current State
**Primary CTA**: "Submit"
**Issues Identified**:
- Generic copy ("Submit" doesn't state value)
- Low contrast (3.2:1, below WCAG AA)
- Below fold on mobile
- No friction reducer

### Optimized CTAs

**Primary CTA**:
- Copy: "Start Free Trial - No Credit Card"
- Color: #2563eb (8.59:1 contrast ratio)
- Size: 48px height, full-width on mobile
- Placement: Hero (above fold), after features, before footer

**Secondary CTA**:
- Copy: "Watch 2-Min Demo"
- Style: Outlined button
- Placement: Hero (next to primary)

**Tertiary CTA**:
- Copy: "See Pricing"
- Style: Text link
- Placement: Navigation

### CTA Sections Added
1. Hero section CTA with social proof
2. Post-feature CTA with benefit list
3. Final CTA before footer
4. Sticky mobile bar for long-scroll pages

### Files Modified
- `[filepath]` - Hero CTA
- `[filepath]` - CTA button styles
- `[filepath]` - CTA sections
- `[filepath]` - Mobile sticky bar

### A/B Test Recommendations
**Test 1**: CTA copy
- Control: "Start Free Trial"
- Variant: "Get Instant Access"
- Expected lift: +10-15%

**Test 2**: CTA placement
- Control: Hero only
- Variant: Hero + repeated throughout
- Expected lift: +20-30%
```

---

## Integration with Other Skills

- **/conversion-audit** - Use to identify CTA issues
- **/copywriting-guide** - Create compelling CTA copy
- **/social-proof** - Place CTAs near social proof
- **/mobile-patterns** - Optimize CTA placement for mobile

---

## Notes

- Test on real devices - mobile CTA experience differs from desktop
- Contrast ratio tools: WebAIM, Coolors, Stark
- One primary CTA per page/screen - don't confuse users
- Urgency works but only if ethical (real deadlines only)
- Friction reducers can increase conversions by 10-30%
- CTA copy matters more than color (test copy first)
- Mobile users often need CTAs repeated (sticky bar helps)