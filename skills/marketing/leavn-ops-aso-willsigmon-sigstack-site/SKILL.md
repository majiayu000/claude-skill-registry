---
name: Leavn Ops: App Store Optimization Skill
description: Use this skill when optimizing Leavn's App Store presence, researching keywords, or responding to reviews.
allowed-tools: Grep
---

# Leavn Ops: App Store Optimization Skill

Use this skill when optimizing Leavn's App Store presence, researching keywords, or responding to reviews.

## CLI Commands Available

```bash
# Research keywords for topic
leavn-ops aso keywords "bible study app"

# Generate localized listings
leavn-ops aso localize --source en-US --targets es-ES,de-DE,fr-FR

# Draft review responses
leavn-ops aso reviews
```

## ASO Best Practices

### Keyword Strategy

#### Keyword Sources
1. **Competitor Analysis**: What keywords do YouVersion, Hallow, Pray.com rank for?
2. **Autocomplete**: Type in App Store search for suggestions
3. **Related Searches**: Bottom of search results
4. **Review Mining**: What words do users use to describe apps?

#### Keyword Placement Priority
1. **App Name** (30 chars) - Highest weight
2. **Subtitle** (30 chars) - High weight
3. **Keyword Field** (100 chars) - Medium weight
4. **Description** - Indexed for search

#### Leavn Keyword Categories
- **Primary**: bible, prayer, devotional, faith, christian
- **Secondary**: meditation, spiritual, wellness, daily, morning
- **Long-tail**: bible study app, daily devotional, prayer journal
- **Competitor**: alternatives to [competitor names]

### App Store Listing Optimization

#### Title Formula
`Leavn - [Primary Value Prop]`
Example: `Leavn - Bible & Daily Devotionals`

#### Subtitle Formula
`[Benefit] | [Feature] | [Feature]`
Example: `Prayer Journal | AI Devotions | Audio`

#### Description Structure
1. **Hook** (first 3 lines visible): Clear value proposition
2. **Features**: Bullet points with keywords naturally included
3. **Social Proof**: Ratings, testimonials
4. **CTA**: Download now

### Screenshot Optimization

#### Best Practices
1. **First Screenshot**: Show primary value (Bible + AI devotionals)
2. **Lifestyle Context**: Show app in real-world use
3. **Feature Callouts**: Text overlays explaining benefits
4. **Consistent Style**: Match brand colors and typography
5. **Device Frames**: Optional but professional

#### Screenshot Order Strategy
1. Hero shot (main value prop)
2. Bible reading feature
3. Devotional/AI feature
4. Prayer/community feature
5. Personalization/settings

### Review Response Framework

#### Positive Reviews (4-5 stars)
- Thank the user genuinely
- Highlight what they loved
- Invite them to try another feature
- Keep it brief (2-3 sentences)

```
Thank you so much for your kind words, [Name]! We're thrilled
that the daily devotionals have been meaningful for you.
Have you tried the prayer journal feature? We think you'd
love it!
```

#### Negative Reviews (1-2 stars)
- Acknowledge their frustration
- Apologize without being defensive
- Offer concrete solution
- Invite direct contact

```
We're sorry to hear about your experience, [Name]. That's
definitely not what we want for our users. We'd love to help
resolve this - could you email us at support@leavn.app with
more details? We'll prioritize your case.
```

#### Feature Requests
- Thank them for the idea
- Explain current status (if planned)
- Invite them to reach out

### Localization Priority

#### Tier 1 (High Priority)
- English (US)
- Spanish (ES, MX)
- Portuguese (BR)

#### Tier 2 (Medium Priority)
- German (DE)
- French (FR)
- Chinese Simplified (CN)

#### Tier 3 (Growth Markets)
- Korean (KR)
- Japanese (JP)
- Arabic (SA)
- Hebrew (IL)

### A/B Testing

#### What to Test
1. Icon variations
2. First screenshot
3. Subtitle wording
4. App preview video vs static

#### Testing Strategy
- Run each test for 7+ days
- Change one variable at a time
- Measure: Conversion rate, impressions, downloads

## Integration with Research

After running ASO commands:
1. Use `leavn-ops research competitors` to analyze competitor ASO
2. Use `leavn-ops research sentiment` to find user language
3. Update keywords monthly based on performance

## Output Location
All ASO content saved to: `~/.local/share/leavn-ops/outputs/`
