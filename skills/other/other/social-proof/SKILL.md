---
name: social-proof
description: Design and implement social proof elements including testimonials, logo bars, stats counters, reviews, and trust signals to increase credibility and conversion.
---

# Social Proof Skill

Design authentic, compelling social proof elements that build trust and credibility throughout the buyer journey.

## When to Use

Use `/social-proof` when you need to:
- Add testimonials to landing pages
- Create logo/trust bars
- Display usage statistics
- Implement review/rating displays
- Add case study previews
- Create "as seen in" press mentions
- Place social proof strategically

## Instructions

### Phase 1: Identify Available Social Proof

**Goal**: Gather all credibility signals to display

**I will inventory:**

1. **Customer Testimonials**
   - Direct quotes from satisfied customers
   - Full names, photos, job titles, companies
   - Specific results or outcomes
   - Video testimonials available?

2. **Company Logos**
   - Recognizable brands using your product
   - Industry leaders or aspirational brands
   - Diversity of industries

3. **Usage Statistics**
   - Number of customers ("10,000+ users")
   - Volume metrics ("1M+ tasks completed")
   - Growth metrics ("Growing 50% MoM")
   - Time-based ("Trusted since 2015")

4. **Reviews & Ratings**
   - Star ratings (aggregate score)
   - Review platform mentions (G2, Capterra, Trustpilot)
   - Number of reviews ("2,000+ reviews")

5. **Case Studies**
   - Detailed success stories
   - Quantifiable results
   - Before/after narratives

6. **Press & Awards**
   - Media mentions (TechCrunch, Forbes)
   - Industry awards
   - Certifications

7. **Expert Endorsements**
   - Industry thought leaders
   - Celebrity endorsements
   - Professional certifications

---

### Phase 2: Select Appropriate Patterns

**Goal**: Match social proof types to page context

### Social Proof Pattern Matrix

| Page Type | Primary Social Proof | Secondary |
|-----------|---------------------|-----------|
| **Homepage** | Logo bar, Stats counter | Hero testimonial |
| **Features** | Feature-specific testimonials | Stats related to features |
| **Pricing** | Reviews, testimonials | Money-back guarantee |
| **Case Studies** | Full case study | Related testimonials |
| **Signup/Form** | Trust badges, security | Quick testimonial |
| **Product Page** | Reviews, ratings | Usage stats |

### Placement Strategy

**Logo Bar**: Immediately after hero
**Hero Testimonial**: In hero section or just after
**Mid-Page Testimonials**: After feature sections
**Review Widgets**: On pricing pages
**Trust Badges**: Near forms and payment
**Final Testimonial**: Before closing CTA

---

### Phase 3: Implement Social Proof Components

**Goal**: Create authentic, visually appealing social proof elements

### Component 1: Logo Trust Bar

```css
.logoBar {
  padding: 32px 24px;
  background: var(--color-bg-subtle);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.logoBarHeading {
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}

.logoGrid {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48px;
  flex-wrap: wrap;
}

.logoItem {
  height: 40px;
  opacity: 0.6;
  transition: opacity 0.2s ease;
  filter: grayscale(100%);
}

.logoItem:hover {
  opacity: 1;
  filter: grayscale(0%);
}

@media (max-width: 640px) {
  .logoGrid {
    gap: 32px;
  }

  .logoItem {
    height: 32px;
  }
}
```

```html
<div class="logoBar">
  <p class="logoBarHeading">Trusted by industry leaders</p>
  <div class="logoGrid">
    <img src="/logos/google.svg" alt="Google" class="logoItem" />
    <img src="/logos/microsoft.svg" alt="Microsoft" class="logoItem" />
    <img src="/logos/salesforce.svg" alt="Salesforce" class="logoItem" />
    <img src="/logos/shopify.svg" alt="Shopify" class="logoItem" />
  </div>
</div>
```

---

### Component 2: Testimonial Card

```css
.testimonialCard {
  background: var(--color-bg-elevated);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.testimonialQuote {
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-text);
}

.testimonialQuote::before {
  content: '"';
  font-size: 36px;
  line-height: 0;
  color: var(--color-primary);
  opacity: 0.3;
}

.testimonialAuthor {
  display: flex;
  align-items: center;
  gap: 12px;
}

.testimonialAvatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.testimonialInfo {
  flex: 1;
}

.testimonialName {
  font-weight: 600;
  font-size: 15px;
  color: var(--color-text);
  margin-bottom: 2px;
}

.testimonialRole {
  font-size: 14px;
  color: var(--color-text-secondary);
}

/* Variant: With company logo */
.testimonialCard.withLogo .testimonialAuthor {
  justify-content: space-between;
}

.testimonialCompanyLogo {
  height: 24px;
  opacity: 0.6;
}
```

```html
<!-- Minimal Testimonial -->
<div class="testimonialCard">
  <div class="testimonialQuote">
    This tool saved our team 10 hours per week. The automation features are incredible and actually work as promised.
  </div>
  <div class="testimonialAuthor">
    <img src="/avatars/sarah.jpg" alt="Sarah Chen" class="testimonialAvatar" />
    <div class="testimonialInfo">
      <div class="testimonialName">Sarah Chen</div>
      <div class="testimonialRole">Head of Marketing, Acme Corp</div>
    </div>
  </div>
</div>

<!-- With company logo -->
<div class="testimonialCard withLogo">
  <div class="testimonialQuote">
    We tried 5 different tools. This is the only one our entire team actually uses daily.
  </div>
  <div class="testimonialAuthor">
    <div class="testimonialInfo">
      <div class="testimonialName">Marcus Rodriguez</div>
      <div class="testimonialRole">VP of Sales</div>
    </div>
    <img src="/logos/salesforce.svg" alt="Salesforce" class="testimonialCompanyLogo" />
  </div>
</div>
```

---

### Component 3: Stats Counter

```css
.statsSection {
  padding: 64px 24px;
  background: var(--color-bg-subtle);
}

.statsGrid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 48px;
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}

.statItem {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.statNumber {
  font-size: 48px;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1;
}

.statLabel {
  font-size: 16px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

/* Animated counter */
.statNumber.counting {
  animation: countUp 2s ease-out forwards;
}

@keyframes countUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

```html
<section class="statsSection">
  <div class="statsGrid">
    <div class="statItem">
      <div class="statNumber">10,000+</div>
      <div class="statLabel">Active Teams</div>
    </div>
    <div class="statItem">
      <div class="statNumber">1M+</div>
      <div class="statLabel">Tasks Completed</div>
    </div>
    <div class="statItem">
      <div class="statNumber">99.9%</div>
      <div class="statLabel">Uptime</div>
    </div>
    <div class="statItem">
      <div class="statNumber">4.9/5</div>
      <div class="statLabel">Customer Rating</div>
    </div>
  </div>
</section>
```

---

### Component 4: Review Widget

```css
.reviewWidget {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--color-bg-elevated);
  border-radius: 8px;
}

.reviewStars {
  display: flex;
  gap: 2px;
  color: #fbbf24; /* Yellow */
  font-size: 20px;
}

.reviewScore {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
}

.reviewCount {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.reviewPlatform {
  margin-left: auto;
  height: 20px;
  opacity: 0.6;
}
```

```html
<div class="reviewWidget">
  <div class="reviewStars">
    ★★★★★
  </div>
  <div class="reviewScore">4.9</div>
  <div class="reviewCount">from 2,000+ reviews</div>
  <img src="/logos/g2.svg" alt="G2" class="reviewPlatform" />
</div>
```

---

### Component 5: Trust Badge Bar

```css
.trustBadges {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  padding: 16px;
  flex-wrap: wrap;
}

.trustBadge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.trustBadge svg,
.trustBadge img {
  width: 20px;
  height: 20px;
  color: var(--color-success);
}
```

```html
<div class="trustBadges">
  <div class="trustBadge">
    <svg><!-- Checkmark icon --></svg>
    <span>256-bit SSL Encryption</span>
  </div>
  <div class="trustBadge">
    <svg><!-- Shield icon --></svg>
    <span>GDPR Compliant</span>
  </div>
  <div class="trustBadge">
    <svg><!-- Lock icon --></svg>
    <span>SOC 2 Type II Certified</span>
  </div>
  <div class="trustBadge">
    <img src="/badges/stripe.svg" alt="Stripe" />
    <span>Secured by Stripe</span>
  </div>
</div>
```

---

### Component 6: "As Seen In" Press Bar

```css
.pressBar {
  padding: 32px 24px;
  text-align: center;
}

.pressHeading {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}

.pressLogos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48px;
  flex-wrap: wrap;
}

.pressLogo {
  height: 32px;
  opacity: 0.5;
  filter: grayscale(100%);
  transition: all 0.2s ease;
}

.pressLogo:hover {
  opacity: 0.8;
  filter: grayscale(0%);
}
```

```html
<div class="pressBar">
  <p class="pressHeading">As Featured In</p>
  <div class="pressLogos">
    <img src="/press/techcrunch.svg" alt="TechCrunch" class="pressLogo" />
    <img src="/press/forbes.svg" alt="Forbes" class="pressLogo" />
    <img src="/press/wired.svg" alt="Wired" class="pressLogo" />
    <img src="/press/nyt.svg" alt="New York Times" class="pressLogo" />
  </div>
</div>
```

---

### Component 7: Real-Time Activity Feed

```css
.activityFeed {
  position: fixed;
  bottom: 24px;
  left: 24px;
  max-width: 320px;
  background: var(--color-bg-elevated);
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  animation: slideIn 0.3s ease;
  z-index: 1000;
}

@keyframes slideIn {
  from {
    transform: translateY(100px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.activityDot {
  width: 8px;
  height: 8px;
  background: var(--color-success);
  border-radius: 50%;
  animation: pulse 2s ease infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

.activityMessage {
  flex: 1;
  font-size: 14px;
  color: var(--color-text);
}

.activityTime {
  font-size: 12px;
  color: var(--color-text-secondary);
}
```

```html
<div class="activityFeed">
  <div class="activityDot"></div>
  <div class="activityMessage">
    <strong>Sarah from Chicago</strong> just signed up
  </div>
  <div class="activityTime">2m ago</div>
</div>
```

---

## Social Proof Checklist

### Authenticity
- [ ] Real photos (not stock images)?
- [ ] Full names and roles provided?
- [ ] Specific companies mentioned?
- [ ] Verifiable claims (numbers, outcomes)?
- [ ] Recent testimonials (not from 2015)?
- [ ] Diverse range of customers?

### Relevance
- [ ] Testimonials match page context?
- [ ] Customer profiles match target audience?
- [ ] Stats relate to value proposition?
- [ ] Industry-relevant logos?
- [ ] Results are meaningful to prospects?

### Placement
- [ ] Logo bar immediately after hero?
- [ ] Testimonials after value propositions?
- [ ] Trust badges near forms/payment?
- [ ] Reviews on pricing pages?
- [ ] Final testimonial before closing CTA?

### Design
- [ ] Social proof doesn't overpower message?
- [ ] Consistent visual style?
- [ ] Readable on mobile?
- [ ] High-quality images?
- [ ] Proper contrast and spacing?

### Content Quality
- [ ] Testimonials are specific, not generic?
- [ ] Stats are impressive and current?
- [ ] No superlatives without proof?
- [ ] Company logos are recognizable?
- [ ] Press mentions are credible?

---

## Output Format

```markdown
## Social Proof Implementation

### Inventory
**Available Social Proof**:
- 15 customer testimonials (with photos)
- 8 recognizable company logos
- 10,000+ active users
- 4.9/5 star rating from 2,000+ reviews
- 3 press mentions (TechCrunch, Forbes, Wired)
- 2 industry certifications

### Components Created

**1. Logo Trust Bar**
- Placement: Below hero section
- Logos: Google, Microsoft, Salesforce, Shopify
- File: `[filepath]`

**2. Hero Testimonial**
- Quote from Sarah Chen (Head of Marketing, Acme Corp)
- Placement: Hero section, right column
- File: `[filepath]`

**3. Stats Counter**
- Metrics: 10,000+ teams, 1M+ tasks, 99.9% uptime, 4.9/5 rating
- Placement: Mid-page after features
- File: `[filepath]`

**4. Review Widget**
- 4.9/5 stars from 2,000+ G2 reviews
- Placement: Pricing page sidebar
- File: `[filepath]`

**5. Trust Badges**
- SSL, GDPR, SOC 2, Stripe
- Placement: Near signup form
- File: `[filepath]`

**6. Press Bar**
- TechCrunch, Forbes, Wired logos
- Placement: Above footer
- File: `[filepath]`

### Strategic Placement
✅ Logo bar immediately after hero
✅ Testimonials after each feature section
✅ Trust badges near form
✅ Reviews on pricing page
✅ Final testimonial before closing CTA

### Files Modified
- `[filepath]` - Hero section with testimonial
- `[filepath]` - Logo trust bar component
- `[filepath]` - Stats section
- `[filepath]` - Review widget
- `[filepath]` - Trust badges

### Authenticity Checklist
✅ Real customer photos used
✅ Full names and companies provided
✅ Specific, quantifiable results mentioned
✅ Current testimonials (last 6 months)
✅ Diverse customer profiles represented
```

---

## Integration with Other Skills

- **/conversion-audit** - Ensure social proof addresses objections
- **/cta-optimizer** - Place CTAs near social proof
- **/copywriting-guide** - Write compelling testimonial copy
- **/component-states** - Add hover states to logos
- **/enhance-project** - Add social proof to existing projects

---

## Notes

- Authenticity beats perfection - real customers > stock photos
- Specific testimonials convert better ("saved 10 hours/week" > "great tool")
- Logo bar works even with lesser-known companies if they're relevant
- Update stats regularly - "10,000+ users" from 2020 looks stale
- Video testimonials can increase conversion by 20-30% but are harder to produce
- Too much social proof can feel desperate - use strategically
- Always verify you have permission to use company logos and testimonials
- Real-time activity feeds should be real (fake ones damage trust)