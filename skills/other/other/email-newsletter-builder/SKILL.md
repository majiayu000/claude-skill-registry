---
name: building-email-newsletters
description: Scaffolds email campaigns with content blocks and copy. Use when the user asks about email templates, newsletter content, subject lines, email marketing, or campaign copy.
---

# Email Newsletter Template Builder

## When to use this skill

- User asks to create a newsletter
- User needs email subject lines
- User wants email campaign templates
- User mentions email marketing copy
- User needs A/B testing variants

## Workflow

- [ ] Identify email type and goal
- [ ] Generate subject line variants
- [ ] Create preheader text
- [ ] Build email structure
- [ ] Write content blocks
- [ ] Add CTAs and footer

## Instructions

### Step 1: Identify Email Type

| Email Type    | Goal               | Structure                   |
| ------------- | ------------------ | --------------------------- |
| Newsletter    | Engagement, value  | Hero + 3-5 content blocks   |
| Promotional   | Sales, conversions | Hero + offer + CTA          |
| Welcome       | Onboarding         | Personal intro + next steps |
| Announcement  | Awareness          | News + details + CTA        |
| Re-engagement | Win-back           | Hook + incentive + CTA      |
| Transactional | Information        | Order details + support     |

### Step 2: Subject Line Generation

**Subject line formulas:**

| Formula          | Example                                     |
| ---------------- | ------------------------------------------- |
| Number + Benefit | "5 ways to speed up your website today"     |
| How to + Outcome | "How to double your open rates"             |
| Question         | "Is your portfolio costing you interviews?" |
| Curiosity gap    | "The one thing top developers never skip"   |
| Urgency          | "Last chance: 40% off ends tonight"         |
| Personal         | "John, your weekly digest is ready"         |
| FOMO             | "Everyone's talking about this new feature" |
| Direct benefit   | "Get 3 hours back every week"               |

**Subject line best practices:**

- 30-50 characters (mobile preview)
- Front-load key information
- Avoid spam triggers (FREE!!!, 💰💰💰)
- Test with/without emoji
- Match preheader text

**A/B test variants:**

```markdown
## Subject Line Variants

**Version A (Benefit-focused):**
Subject: 5 tools that cut my development time in half
Preheader: Plus the one tool I stopped using

**Version B (Curiosity):**
Subject: I stopped using this popular tool
Preheader: And my productivity doubled

**Version C (Question):**
Subject: Are you still using [Tool]?
Preheader: There's a faster alternative
```

### Step 3: Preheader Text

**Preheader guidelines:**

- 40-100 characters
- Complement (don't repeat) subject
- Add context or secondary hook
- Include CTA preview if relevant

| Subject                        | Poor Preheader              | Good Preheader                         |
| ------------------------------ | --------------------------- | -------------------------------------- |
| "5 ways to speed up your site" | "Read our latest blog post" | "Plus the #1 mistake slowing you down" |
| "Your order has shipped"       | "Order confirmation"        | "Arrives Thursday. Track it here →"    |

### Step 4: Email Structure Templates

**Newsletter template:**

```html
<!-- Preheader (hidden) -->
<span style="display:none;">[Preheader text here]</span>

<!-- Header -->
[Logo] [Navigation: Blog | Products | Contact]

<!-- Hero Section -->
[Featured image or heading] [Brief intro: 2-3 sentences] [Primary CTA button]

<!-- Content Block 1 -->
[H2: Section title] [Thumbnail image] [Summary: 2-3 sentences] [Read more link]

<!-- Content Block 2 -->
[H2: Section title] [Thumbnail image] [Summary: 2-3 sentences] [Read more link]

<!-- Content Block 3 -->
[H2: Section title] [Thumbnail image] [Summary: 2-3 sentences] [Read more link]

<!-- Secondary CTA -->
[H2: Call to action heading] [Brief value prop] [CTA button]

<!-- Footer -->
[Social icons] [Unsubscribe | Preferences | View in browser] [Company address]
[Copyright]
```

**Promotional template:**

```html
<!-- Preheader -->
<span style="display:none;">[Urgency or key offer]</span>

<!-- Header -->
[Logo]

<!-- Hero -->
[Bold headline with offer] [Hero image of product/service] [Key benefit: 1
sentence] [Primary CTA: "Shop Now" / "Get Started"]

<!-- Social Proof -->
[Testimonial or rating] [Customer logo bar]

<!-- Benefits -->
[Benefit 1 with icon] [Benefit 2 with icon] [Benefit 3 with icon]

<!-- Urgency -->
[Countdown or deadline] [Secondary CTA]

<!-- Footer -->
[Unsubscribe | View in browser] [Address]
```

**Welcome email template:**

```html
<!-- Preheader -->
<span style="display:none;">Here's what to do first...</span>

<!-- Header -->
[Logo]

<!-- Hero -->
[Personalized greeting: "Welcome, {first_name}!"] [What they signed up for /
what to expect] [Founder photo or brand image]

<!-- Quick Wins -->
[H2: Get started in 3 steps] [Step 1] [Icon + title + 1-sentence description]
[Step 2] [Icon + title + 1-sentence description] [Step 3] [Icon + title +
1-sentence description] [Primary CTA: "Complete your profile" / "Start
tutorial"]

<!-- Value Reminder -->
[H2: What you'll get] [Bullet list of benefits]

<!-- Personal Touch -->
[Sign-off from founder/team] [Photo + signature] [P.S. line with secondary offer
or tip]

<!-- Footer -->
[Support link] [Social icons] [Unsubscribe | Preferences]
```

### Step 5: Content Block Writing

**Block structure:**

```markdown
## [Compelling headline]

[1-2 sentences summarizing the value or key point]

[Optional: key stat or quote]

[CTA: "Read more →" or "Watch now →"]
```

**Block examples:**

```markdown
## Why Your Images Are Slowing Down Your Site

Large, unoptimized images are the #1 cause of slow page loads.
Here's how to fix it in under 10 minutes.

→ Read the full guide

---

## New Feature: Dark Mode Support

You asked, we delivered. Enable dark mode in your dashboard
settings for easier late-night work sessions.

→ Try it now

---

## Case Study: How Acme Corp Increased Conversions 47%

See exactly how they optimized their checkout flow and
the surprising change that made the biggest difference.

→ Read the case study
```

### Step 6: CTA Best Practices

**Button copy:**

| Weak       | Strong                 |
| ---------- | ---------------------- |
| Click here | Get your free guide    |
| Submit     | Start my trial         |
| Learn more | See how it works       |
| Buy now    | Add to cart - $29      |
| Download   | Download the checklist |

**CTA guidelines:**

- Action verb + benefit
- 2-5 words
- First person ("Get my..." vs "Get your...")
- Contrast color from email background
- Minimum 44x44px tap target

### Step 7: Footer Requirements

**Required elements:**

```html
<!-- Social Links -->
<a href="#">Twitter</a> | <a href="#">LinkedIn</a> | <a href="#">Instagram</a>

<!-- Legal -->
<p>You're receiving this because you signed up at [website].</p>

<a href="{unsubscribe_link}">Unsubscribe</a> |
<a href="{preferences_link}">Email preferences</a> |
<a href="{browser_link}">View in browser</a>

<!-- Address (CAN-SPAM required) -->
<p>
  [Company Name]<br />
  [Street Address]<br />
  [City, State ZIP]
</p>

<!-- Copyright -->
<p>© 2026 [Company Name]. All rights reserved.</p>
```

### Step 8: Mobile Optimization

**Mobile-first guidelines:**

| Element       | Mobile Spec                  |
| ------------- | ---------------------------- |
| Width         | 100%, max 600px              |
| Font size     | Body 16px+, headings 22px+   |
| Line height   | 1.5-1.6                      |
| Button size   | Full width, 48px height min  |
| Images        | 100% width, max-width set    |
| Padding       | 20px sides minimum           |
| Single column | Stack all content vertically |

**Responsive image:**

```html
<img
  src="image.jpg"
  alt="Description"
  width="600"
  style="max-width: 100%; height: auto; display: block;"
/>
```

### Step 9: Testing Checklist

Before sending:

- [ ] Subject line under 50 characters
- [ ] Preheader complements subject
- [ ] All links working
- [ ] Images have alt text
- [ ] Unsubscribe link present
- [ ] Physical address included
- [ ] Renders on mobile (test with Litmus/Email on Acid)
- [ ] Plain text version included
- [ ] Personalization tokens work ({first_name})
- [ ] Sent from recognizable sender name

## Output Format

```markdown
## Email Campaign: [Name]

**Type:** [Newsletter/Promotional/Welcome/etc.]
**Goal:** [Engagement/Sales/Onboarding/etc.]

---

### Subject Line Variants

**A:** [Subject line]
**B:** [Subject line variant]

**Preheader:** [Preheader text]

---

### Email Content

[Full email content with sections marked]

---

### Notes

- Send time: [Recommended day/time]
- Segment: [Target audience]
- A/B test: [What to test]
```

## Validation

Before completing:

- [ ] Subject line A/B variants provided
- [ ] Preheader text included
- [ ] Clear value in first paragraph
- [ ] CTAs are action-oriented
- [ ] Mobile-friendly structure
- [ ] Footer has required elements
- [ ] Consistent with brand voice

## Error Handling

- **No clear goal**: Ask for campaign objective (traffic, sales, engagement).
- **Too much content**: Limit to 3-5 content blocks; link to full articles.
- **Missing personalization**: Add {first_name} or segment-specific content.
- **Spam trigger words**: Avoid "FREE", "Act now", excessive caps/punctuation.
- **No mobile consideration**: Use single column, large fonts, stacked CTAs.

## Resources

- [Really Good Emails](https://reallygoodemails.com/) - Inspiration
- [Litmus](https://www.litmus.com/) - Email testing
- [Mail-Tester](https://www.mail-tester.com/) - Spam score check
- [Email on Acid](https://www.emailonacid.com/) - Cross-client testing
