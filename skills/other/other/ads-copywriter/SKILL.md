---
name: ads-copywriter
description: "Multi-platform ad copy generation for Google Ads, Meta/Facebook, TikTok, LinkedIn with A/B testing variants"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: marketing
tags:
  - advertising
  - copywriting
  - google-ads
  - facebook-ads
  - tiktok
department: Marketing

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - gpt-4
    - gpt-4o

capabilities:
  - ad_copy_generation
  - headline_variants
  - platform_optimization
  - ab_testing
  - cta_optimization

languages:
  - en
  - zh

related_skills:
  - tiktok-marketing
  - content-writer
  - landing-page
---

# Ads Copywriter

Generate high-converting ad copy for Google Ads, Meta/Facebook, TikTok, and LinkedIn with platform-specific optimization and A/B testing variants.

## Platform Specifications

### Google Ads

```yaml
google_ads_formats:
  responsive_search_ad:
    headlines:
      count: 15 (min 3)
      max_chars: 30
      requirements:
        - Include keyword in 3+ headlines
        - Include brand name in 2+ headlines
        - Include CTA in 2+ headlines
        - Include numbers/stats in 2+ headlines
    
    descriptions:
      count: 4 (min 2)
      max_chars: 90
      requirements:
        - Expand on headline promise
        - Include benefits
        - Include CTA
        - Include trust signals
  
  performance_max:
    headlines: 5 (30 chars each)
    long_headlines: 5 (90 chars each)
    descriptions: 5 (90 chars each)
    
  display_ad:
    short_headline: 25 chars
    long_headline: 90 chars
    description: 90 chars
```

### Meta/Facebook Ads

```yaml
meta_ads_formats:
  feed_ad:
    primary_text: 125 chars (visible), 500 max
    headline: 40 chars
    description: 30 chars
    cta_options: [Learn More, Shop Now, Sign Up, Get Offer, Book Now]
  
  stories_ad:
    text_overlay: 125 chars
    headline: 40 chars
    
  reels_ad:
    caption: 2200 chars max
    first_line_visible: ~100 chars
```

### TikTok Ads

```yaml
tiktok_ads:
  in_feed:
    ad_text: 100 chars max
    display_name: 40 chars
    
  spark_ads:
    caption: 150 chars recommended
    hashtags: 3-5
```

### LinkedIn Ads

```yaml
linkedin_ads:
  sponsored_content:
    intro_text: 150 chars (mobile visible)
    headline: 70 chars
    description: 100 chars
    
  message_ad:
    subject: 60 chars
    message: 500 chars
    cta: 20 chars
```

---

## Ad Copy Frameworks

### AIDA Framework
```
Attention → Interest → Desire → Action

Example:
A: "Struggling with [problem]?"
I: "Our [product] helps [target] achieve [benefit]"
D: "[Social proof] + [Unique value]"
A: "[CTA] - [Urgency/Offer]"
```

### PAS Framework
```
Problem → Agitation → Solution

Example:
P: "Tired of [pain point]?"
A: "Every day, [worse scenario]. [Emotional impact]."
S: "[Product] solves this by [mechanism]. [CTA]"
```

### BAB Framework
```
Before → After → Bridge

Example:
B: "Before: [current state]"
A: "After: [desired state]"
B: "Bridge: [your product] makes it possible. [CTA]"
```

---

## Ad Copy Templates

### Google Ads Headlines (30 chars)

```yaml
headline_templates:
  keyword_focused:
    - "[Keyword] - Save 20% Today"
    - "Best [Keyword] of 2026"
    - "[Keyword] Starting at $X"
    - "Top-Rated [Keyword]"
  
  benefit_focused:
    - "Save X Hours Per Week"
    - "Boost [Metric] by X%"
    - "Get Results in X Days"
    - "No [Pain Point] Ever Again"
  
  urgency_focused:
    - "Limited Time Offer"
    - "Only X Spots Left"
    - "Sale Ends [Date]"
    - "Don't Miss Out"
  
  trust_focused:
    - "X+ Happy Customers"
    - "★★★★★ Rated"
    - "As Seen in [Publication]"
    - "Trusted by [Brands]"
  
  cta_focused:
    - "Get Your Free Trial"
    - "Start Now - It's Free"
    - "Book a Demo Today"
    - "Download Free Guide"
```

### Facebook Ad Templates

**Template 1: Problem-Solution**
```
🚨 Still struggling with [problem]?

You're not alone. [X%] of [target audience] face this every day.

Here's the thing: [brief insight about why old solutions fail]

That's why we created [Product] – the only [category] that:
✅ [Benefit 1]
✅ [Benefit 2]  
✅ [Benefit 3]

[Social proof: "X customers have already [achieved result]"]

👉 [CTA] and see the difference for yourself.

[Offer/Urgency if applicable]
```

**Template 2: Story-Based**
```
I used to [relatable struggle]...

Then I discovered [insight/product] and everything changed.

In just [timeframe], I was able to:
• [Result 1]
• [Result 2]
• [Result 3]

If you're ready to [achieve goal], here's your chance.

🔗 [CTA] (Link in comments)
```

**Template 3: Direct Offer**
```
🎁 [Offer headline]

For a limited time, get [product/service] at [discount/special price].

What you get:
📦 [Item 1]
📦 [Item 2]
📦 [Item 3]

Total value: $XXX
Your price: $XX

⏰ Offer ends [date]

[CTA Button] 👆
```

---

## A/B Testing Variants

### Generating Test Variants

```yaml
ab_test_strategy:
  elements_to_test:
    - headlines: emotional vs rational
    - cta: soft vs hard
    - social_proof: numbers vs testimonial
    - urgency: scarcity vs deadline
    - benefit: primary vs secondary
  
  variant_generation:
    per_ad_group: 3-5 variants
    test_duration: 7-14 days minimum
    statistical_significance: 95%
    
  example_variants:
    headline_test:
      A: "Save 50% on Your First Order"  # Offer-focused
      B: "Join 10,000+ Happy Customers"   # Social proof
      C: "Stop Wasting Money on [X]"      # Problem-focused
    
    cta_test:
      A: "Get Started Free"               # Low commitment
      B: "Claim Your Discount"            # Urgency
      C: "See How It Works"               # Curiosity
```

---

## Output Example

**Request**: "Create Google Ads copy for a project management SaaS tool"

**Output**:

```markdown
# Google Ads Copy - Project Management Tool

## Responsive Search Ad

### Headlines (15 variants, 30 chars each)

**Keyword Headlines:**
1. "Project Management Made Easy"
2. "#1 Project Management Tool"
3. "Best PM Software 2026"

**Benefit Headlines:**
4. "Save 10 Hours Per Week"
5. "Boost Team Productivity 40%"
6. "Never Miss a Deadline Again"

**CTA Headlines:**
7. "Try Free for 14 Days"
8. "Start Your Free Trial"
9. "Get Started in 2 Minutes"

**Trust Headlines:**
10. "50,000+ Teams Trust Us"
11. "★★★★★ on G2 & Capterra"
12. "Used by Fortune 500"

**Urgency Headlines:**
13. "Limited: 30% Off Annual"
14. "Special Offer Ends Soon"

**Brand Headlines:**
15. "[BrandName] - Work Smarter"

### Descriptions (4 variants, 90 chars each)

1. "Manage projects, track time, and collaborate with your team in one powerful platform. Try free!"

2. "Trusted by 50,000+ teams worldwide. Kanban, Gantt, time tracking & more. No credit card required."

3. "Stop juggling apps. One tool for tasks, docs, and communication. Start your 14-day free trial today."

4. "Rated #1 for ease of use. Set up in minutes, not days. See why teams love [BrandName]. Try it free!"

---

## Facebook/Meta Ad

### Variant A: Problem-Solution

🤯 Still managing projects with spreadsheets and endless email threads?

You're not alone. 73% of teams say they waste 5+ hours/week on project chaos.

That's why 50,000+ teams switched to [BrandName]:

✅ All tasks, docs & chat in one place
✅ See who's doing what at a glance
✅ Never miss another deadline

"We cut meeting time by 40% in the first month" - Sarah, Marketing Director

👉 Start your free 14-day trial (no credit card needed)

### Variant B: Direct Offer

🎁 Get [BrandName] Pro FREE for 14 days

The all-in-one project management tool trusted by 50,000+ teams.

What you get:
📋 Unlimited projects & tasks
👥 Team collaboration tools
📊 Reports & dashboards
📱 Mobile apps included

No credit card required. Cancel anytime.

[Start Free Trial] 👆

---

## TikTok Ad

**Caption (100 chars):**
"POV: You finally have ONE app for all your projects 🙌 Link in bio for free trial #productivity #work"

**Spark Ad Caption:**
"We were drowning in spreadsheets until we found this... 50K+ teams can't be wrong. Try it free 🔗"

---

## LinkedIn Ad

**Intro Text (150 chars):**
"73% of project managers say tool overload hurts productivity. There's a better way. See how 50,000+ teams work smarter."

**Headline (70 chars):**
"The Project Management Tool Teams Actually Want to Use"

**Description:**
"All-in-one platform for tasks, docs, and team collaboration. Start free."
```

---

*Ads Copywriter Skill - Part of Claude Office Skills*
