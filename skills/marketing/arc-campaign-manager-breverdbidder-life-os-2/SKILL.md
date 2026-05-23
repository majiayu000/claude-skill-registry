---
name: arc-campaign-manager
description: Manage Advance Review Copy (ARC) campaigns for book launches. Use when recruiting beta readers, distributing advance copies, tracking reviewer commitments, writing ARC recruitment emails, managing review team communications, or planning review acquisition strategies. Triggers on requests involving book reviews, ARC teams, beta readers, or review campaigns.
---

# ARC Campaign Manager

Build and manage review teams that deliver 25+ Day 1 reviews.

## ARC Campaign Timeline

| Phase | Timing | Goal |
|-------|--------|------|
| Recruitment | T-90 to T-60 | 50-100 signups |
| Distribution | T-60 to T-45 | ARCs delivered |
| Nurturing | T-45 to T-7 | Readers engaged |
| Activation | T-7 to T-0 | Reviews prepped |
| Launch | T-0 | Reviews posted |

## Target Metrics

```
ARC Signups: 100
ARC Downloads: 75 (75% conversion)
Readers Who Finish: 50 (67% of downloads)
Reviews Posted: 25-30 (50-60% of finishers)
Day 1 Reviews: 10-15
Week 1 Reviews: 20-25
```

## Recruitment Channels

### Tier 1: High Conversion (30-60%)

| Source | Conversion | Notes |
|--------|------------|-------|
| Email list | 40-60% | Warm audience, best quality |
| Past ARC readers | 50-70% | Proven reviewers |
| Social media followers | 20-40% | Engaged audience |

### Tier 2: Medium Conversion (10-30%)

| Source | Conversion | Notes |
|--------|------------|-------|
| BookFunnel groups | 15-25% | Genre-specific |
| StoryOrigin promos | 10-20% | Cross-promotion |
| Facebook reader groups | 10-25% | Active communities |

### Tier 3: Low Conversion (5-15%)

| Source | Conversion | Notes |
|--------|------------|-------|
| Goodreads giveaways | 5-10% | High volume, low quality |
| Twitter/X | 5-15% | Depends on following |
| Reddit communities | 5-10% | Must add value first |

### Paid Services

| Service | Cost | Expected Reviews |
|---------|------|-----------------|
| NetGalley | $450/listing | 20-50 |
| BookSirens | $99-299/mo | 15-40 |
| Pubby | $100-500 | 10-30 |
| Hidden Gems | Free-$299 | 10-25 |

## ARC Distribution Platforms

### BookFunnel (Recommended)

```
Cost: $20-150/year
Features:
- Multiple format delivery (EPUB, MOBI, PDF)
- Reader email capture
- Download tracking
- Automated delivery
```

**Setup Steps:**
1. Create account at bookfunnel.com
2. Upload manuscript files (EPUB required)
3. Set up landing page
4. Enable reader signup
5. Generate unique download link

### StoryOrigin

```
Cost: $70/year
Features:
- ARC management dashboard
- Reader tracking
- Review reminders
- Cross-promotion tools
```

### Direct Distribution

For small teams (<20 people):
- Email attachments (PDF/EPUB)
- Google Drive links
- Dropbox shared folders

## ARC Agreement Template

Include in signup confirmation:

```markdown
ARC READER AGREEMENT

By requesting an advance copy of [BOOK TITLE], you agree to:

1. Read the book (or as much as possible) before [LAUNCH DATE]
2. Post an honest review on Amazon within 48 hours of launch
3. Not share or distribute the ARC file
4. Disclose in your review if required by FTC guidelines*

In exchange, you receive:
- A free advance copy of the book
- [BONUS: exclusive content, etc.]
- Credit in the acknowledgments (optional)

*Note: Amazon's terms prohibit mentioning you received a free 
copy in exchange for a review. Simply post your honest opinion.
```

## Review Guidelines for ARC Readers

Send this with the ARC:

```markdown
HOW TO WRITE A GREAT AMAZON REVIEW

Your review helps readers decide if this book is right for them.
Here's what makes a review helpful:

STRUCTURE (2-5 sentences is fine):
1. Your overall impression
2. What you liked most
3. Who would enjoy this book

EXAMPLE:
"I found [BOOK] to be an insightful guide to [TOPIC]. 
The [specific element] was particularly helpful. 
If you're looking to [outcome], this book delivers."

TIPS:
✅ Be specific (mention chapters, examples, concepts)
✅ Be honest (critical reviews are okay!)
✅ Focus on the content, not delivery method
❌ Don't mention receiving a free copy
❌ Don't copy from other reviews
❌ Don't use phrases like "in exchange for"

POSTING YOUR REVIEW:
1. Go to the book's Amazon page
2. Scroll to "Customer Reviews"
3. Click "Write a customer review"
4. Select star rating
5. Write your review
6. Click Submit

Thank you for supporting this book launch!
```

## Email Sequence Framework

### Email 1: Recruitment (T-60)

**Subject lines that work:**
- "Be the first to read [BOOK]"
- "[NAME], I need your help with something"
- "Free book + your honest opinion?"

**Structure:**
- Personal greeting
- What the book is about (2-3 sentences)
- What you're asking (clear expectations)
- What they get (ARC + bonus)
- Simple CTA (reply or link)

### Email 2: Delivery (T-45)

**Subject:** "Your copy of [BOOK] is ready!"

**Include:**
- Download link (prominent)
- File format options
- Deadline reminder
- Quick reading tips

### Email 3: Check-in (T-30)

**Subject:** "How's the reading going?"

**Include:**
- Friendly check-in
- Answer any questions
- Request for typo reports
- Reminder of timeline

### Email 4: Pre-launch (T-7)

**Subject:** "One week to launch!"

**Include:**
- Countdown excitement
- Review writing tips
- What to expect on launch day
- Thank them for support

### Email 5: Launch day (T-0)

**Subject:** "It's live! Please post your review now"

**Include:**
- Direct Amazon review link
- Step-by-step instructions
- Urgency (first 24 hours matter)
- Gratitude

## Tracking Spreadsheet Template

Track each ARC reader:

| Name | Email | Signed Up | Downloaded | Read | Review Posted | Rating | Notes |
|------|-------|-----------|------------|------|---------------|--------|-------|
| [Name] | [email] | [date] | ✅/❌ | ✅/❌ | ✅/❌ | ⭐⭐⭐⭐⭐ | [notes] |

## Troubleshooting Low Conversions

### Problem: Low signup rate (<20%)

**Solutions:**
- Improve offer (add bonuses)
- Better targeting (right audience?)
- Stronger copy (clear benefits)
- Reduce friction (simpler signup)

### Problem: Low download rate (<60%)

**Solutions:**
- Send reminder emails
- Simplify download process
- Offer multiple formats
- Check for technical issues

### Problem: Low review rate (<40%)

**Solutions:**
- More follow-up emails
- Clearer instructions
- Earlier deadline
- Personal outreach
- Review writing tips

## Scripts

- **ARC tracker**: See `scripts/arc_tracker.py`
- **Email scheduler**: See `scripts/email_scheduler.py`
