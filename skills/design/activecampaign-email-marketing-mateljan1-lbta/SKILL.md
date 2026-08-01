---
name: activecampaign-email-marketing
description: 'Create, manage, and optimize email campaigns for Laguna Beach Tennis
  Academy using ActiveCampaign. Use when Claude needs to: (1) Create email campaigns
  for program launches, camps, or events, (2) Buil'
---

---
name: activecampaign-email-marketing
description: Create, manage, and optimize email campaigns for Laguna Beach Tennis Academy using ActiveCampaign. Use when Claude needs to: (1) Create email campaigns for program launches, camps, or events, (2) Build automation workflows and nurture sequences, (3) Manage contact lists and segmentation, (4) Design luxury-branded email templates following LBTA brand guidelines, (5) Set up triggered emails for registrations or trials, (6) Analyze campaign performance or optimize email strategy.
---

# ActiveCampaign Email Marketing

Create professional email campaigns for LBTA that drive registrations while maintaining the luxury brand aesthetic.

## Quick Start

### Creating a Campaign

1. **Choose campaign type** from `references/campaign-templates.md`
2. **Use HTML template** from `assets/templates/` matching campaign type
3. **Customize content** with program data from `/data/*.json`
4. **Create via API** using `scripts/create_campaign.py`

### Campaign Types

- **Season Launch** - Winter/Spring/Summer/Fall registration announcements
- **Program Spotlight** - JTT, camps, high-performance programs
- **Newsletter** - Monthly updates with tennis news and community stories
- **Nurture Sequence** - Trial follow-ups, re-engagement campaigns
- **Event Promotion** - Camps, clinics, special events

## Brand Guidelines for Emails

### Visual Standards
- **Typography**: Playfair Display (headlines) + Work Sans (body)
- **Colors**: Black/white primary, beige (#F8E6BB) accents, minimal orange (#F8A121)
- **Buttons**: Black background, white text, uppercase, 2.5px letter-spacing
- **Spacing**: 40%+ white space, generous padding
- **Images**: WebP format, editorial quality, no stock photos

### Copy Standards
- **Tone**: Calm, confident, authentic - never salesy
- **Voice**: Founder-led, personal, specific
- **Forbidden**: "Maximize", "elite", "world-class", exclamation points in headlines
- **Preferred**: "Book a Trial", "Start Training", "Join the Community"

### Technical Standards
- **Mobile-first**: Test at 320px, 375px, 768px
- **Accessibility**: 7:1 contrast, alt text on all images
- **Performance**: Images <350KB, inline critical CSS
- **Compatibility**: Test in Gmail, Apple Mail, Outlook

## Working with ActiveCampaign API

### Authentication
Set environment variable:
```bash
export ACTIVECAMPAIGN_API_KEY="your-api-key"
export ACTIVECAMPAIGN_URL="https://lbta.api-us1.com"
```

### Create Campaign
```python
python scripts/create_campaign.py \
  --name "Winter 2026 Registration Open" \
  --subject "Winter Classes Start January 5th" \
  --template "assets/templates/season-launch.html" \
  --list "All Contacts"
```

### Send Test Email
```python
python scripts/send_test.py \
  --campaign-id 123 \
  --email "andrew@lagunabeachtennisacademy.com"
```

## Campaign Strategy

### Segmentation
See `references/segmentation-guide.md` for detailed audience targeting:
- **Junior Parents** - Ages 3-17 programs
- **Adult Players** - Beginner/Intermediate/Advanced
- **High Performance** - Tournament players, college-bound
- **Trial Leads** - Booked but not registered
- **Past Students** - Re-engagement campaigns

### Timing
- **Season launches**: 4-6 weeks before start date
- **Early bird reminders**: 1 week before deadline
- **JTT registration**: 6 weeks before season
- **Camp promotions**: 8-12 weeks before camp dates
- **Newsletters**: Monthly, first Tuesday of month

### Email Sequences
See `references/campaign-templates.md` for pre-built sequences:
- **Welcome Series** (3 emails over 7 days)
- **Trial Follow-up** (4 emails over 14 days)
- **Registration Nurture** (5 emails over 21 days)
- **Re-engagement** (3 emails over 30 days)

## Templates

All templates in `assets/templates/` follow LBTA brand guidelines:

- `season-launch.html` - Winter/Spring/Summer/Fall registration
- `jtt-announcement.html` - Junior Team Tennis campaigns
- `camp-promotion.html` - Camp registration emails
- `newsletter.html` - Monthly newsletter template
- `trial-followup.html` - Post-trial nurture sequence
- `event-invitation.html` - Clinics, showcases, events

### Customizing Templates

1. **Update hero section** with season/program details
2. **Replace pricing** from `/data/*.json` (never hardcode)
3. **Update CTAs** to correct registration URLs
4. **Add program-specific** content blocks
5. **Test responsive** layout at all breakpoints

## Automation Workflows

Create automations using `scripts/create_automation.py`:

### Welcome Series
Triggered when: Contact subscribes to newsletter
- **Email 1** (Immediate): Welcome + academy overview
- **Email 2** (Day 3): Program options + trial booking
- **Email 3** (Day 7): Success stories + registration CTA

### Trial Follow-up
Triggered when: Contact books trial lesson
- **Email 1** (Day 1): Pre-trial preparation
- **Email 2** (Day 2): Post-trial thank you + feedback request
- **Email 3** (Day 5): Program recommendations
- **Email 4** (Day 10): Early bird deadline reminder

### Abandoned Registration
Triggered when: Contact starts but doesn't complete registration
- **Email 1** (1 hour): Cart abandonment reminder
- **Email 2** (24 hours): Testimonial + benefits
- **Email 3** (3 days): Scholarship info + final reminder

## Best Practices

### Subject Lines
- **Keep under 50 characters** for mobile
- **Use specific dates**: "Winter Classes Start January 5th"
- **Avoid spam triggers**: No ALL CAPS, excessive punctuation
- **Test A/B variants**: Question vs. statement, urgency vs. benefit

### Preview Text
- **50-100 characters** that complement subject line
- **Don't repeat** subject line
- **Include CTA** or key benefit

### Content Structure
1. **Hero section** - Visual + headline + subhead
2. **Primary message** - 2-3 paragraphs max
3. **Visual break** - Image or divider
4. **Supporting content** - Details, pricing, dates
5. **CTA section** - Primary + secondary buttons
6. **Footer** - Contact, social, unsubscribe

### Performance Optimization
- **Inline CSS** for email clients
- **Use tables** for layout (email HTML standard)
- **Optimize images** - WebP with JPEG fallback
- **Test deliverability** - Check spam score before sending

## Data Sources

Always pull dynamic data from single source of truth:

- **Programs/Pricing**: `/data/winter2026.json`, `/data/year2026.json`
- **Schedules**: `/data/schedule-2026.json`
- **Coaches**: `/app/coaches/` pages
- **Testimonials**: `/app/success-stories/` pages

Never hardcode prices, dates, or program details in email templates.

## Testing Checklist

Before sending any campaign:

- [ ] Mobile responsive (320px, 375px, 768px)
- [ ] Images have alt text
- [ ] All links work and use UTM parameters
- [ ] Prices match `/data/*.json` files
- [ ] CTAs point to correct URLs
- [ ] Unsubscribe link present
- [ ] Preview text set
- [ ] Test email sent and reviewed
- [ ] Spam score < 5
- [ ] Brand guidelines followed

## Advanced Features

### Personalization
Use ActiveCampaign merge tags:
- `%FIRSTNAME%` - First name
- `%LASTNAME%` - Last name
- `%CHILD_NAME%` - Custom field for junior programs
- `%CHILD_AGE%` - Custom field for age-appropriate programs
- `%LAST_PROGRAM%` - Custom field for returning students

### Dynamic Content
Show different content blocks based on:
- **Program interest** - Junior vs. Adult vs. High Performance
- **Engagement level** - New lead vs. trial booked vs. past student
- **Location** - Laguna Beach vs. nearby cities

### A/B Testing
Test variations of:
- **Subject lines** - Question vs. statement
- **CTA copy** - "Register Now" vs. "Book Your Spot"
- **Hero images** - Action shots vs. lifestyle
- **Pricing display** - Prominent vs. subtle

## Troubleshooting

### Low Open Rates (<20%)
- Improve subject line specificity
- Clean inactive contacts
- Test send time (Tue-Thu, 9-11am PST)
- Verify sender reputation

### Low Click Rates (<2%)
- Make CTAs more prominent
- Reduce content length
- Improve visual hierarchy
- Test CTA copy variations

### High Unsubscribe Rate (>0.5%)
- Reduce email frequency
- Improve content relevance
- Check segmentation accuracy
- Review tone/messaging fit

## Resources

- **API Documentation**: `references/activecampaign-api.md`
- **Campaign Templates**: `references/campaign-templates.md`
- **Segmentation Guide**: `references/segmentation-guide.md`
- **Email Best Practices**: `references/email-best-practices.md`

## Support

For ActiveCampaign account access:
- **Account**: lbta.activehosted.com
- **Support**: support@lagunabeachtennisacademy.com
- **Founder**: Andrew Mateljan

