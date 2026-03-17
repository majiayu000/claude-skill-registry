---
name: generating-webinar-slide-decks
description: Creates structured presentation slides with speaker notes, visual suggestions, and engagement elements for webinars. Use when the user asks about webinar slides, presentation decks, slide content, speaker notes, or virtual event presentations.
---

# Webinar Slide Deck Generator

## When to use this skill

- User asks to create webinar slides
- User needs presentation content
- User wants slide deck structure
- User mentions speaker notes
- User needs virtual event presentations

## Workflow

- [ ] Define webinar objectives
- [ ] Create slide structure
- [ ] Write slide content
- [ ] Add speaker notes
- [ ] Suggest visuals
- [ ] Include engagement elements

## Instructions

### Step 1: Webinar Brief

Gather: title, duration, date/time, platform, presenters, target audience, experience level, webinar type (educational/demo/panel), primary goal, 3-5 key takeaways, and call-to-action.

### Step 2: Slide Structure by Duration

| Duration | Total Slides | Content Slides | Q&A Time |
| -------- | ------------ | -------------- | -------- |
| 30 min   | 15-20        | 8-10           | 5 min    |
| 45 min   | 20-25        | 12-15          | 7 min    |
| 60 min   | 25-35        | 15-20          | 9 min    |

**Standard segments:** Welcome/intro → Agenda → Core content → Summary → Q&A → CTA/close

### Step 3: Slide Content

Each slide needs:

- **Content**: Headline + max 6 bullets (6 words each)
- **Visual**: Suggested image, chart, or icon
- **Speaker Notes**: 30-60 seconds of talking points

**Slide types:** Title, welcome/housekeeping, agenda, content (text or visual), quote/stat, poll/engagement, summary, CTA, Q&A, thank you.

See [examples/slide-templates.md](examples/slide-templates.md) for complete slide templates.

### Step 4: Content Patterns

**Problem → Solution:** Present challenge, then introduce approach
**Before → After:** Show transformation
**Framework/Model:** Introduce 3-5 element framework with diagram
**Demo:** Screenshot or "DEMO" placeholder with walkthrough notes

### Step 5: Speaker Notes

For each slide include:

- Transition from previous slide
- Key points to cover (1-2 sentences each)
- Timing (seconds/minutes)
- Engagement prompt if applicable
- Transition to next slide

### Step 6: Visual Guidelines

| Principle   | Guideline                       |
| ----------- | ------------------------------- |
| Text limit  | Max 6 bullets, max 6 words each |
| Font size   | Headlines: 36pt+, Body: 24pt+   |
| Colors      | Max 3 colors from brand palette |
| White space | 30-40% of slide should be empty |

### Step 7: Engagement Elements

Schedule engagement every 10-15 minutes:

- **Polls**: Gauge knowledge/opinion
- **Chat prompts**: Generate discussion
- **Hand raise**: Quick consensus
- **Quiz**: Test understanding

See [examples/engagement-templates.md](examples/engagement-templates.md) for engagement schedule and examples.

### Step 8: Webinar Type Structures

**Educational:** Intro → Agenda → Why this matters → Step-by-step content → Mistakes to avoid → Summary → Q&A → CTA

**Product Demo:** Intro → Customer challenge → Our approach → Demo → Customer success → Q&A → Offer/CTA

**Panel:** Intro → Topic intro → Panelist intros → Discussion topics → Audience Q&A → Closing thoughts

### Step 9: Accessibility

- Alt text for all images
- 4.5:1 minimum text contrast
- Minimum 24pt body text
- Avoid auto-play animations
- Enable captions for video/audio

## Output Format

```markdown
# [Webinar Title] - Slide Deck

**Duration:** [X minutes]
**Slides:** [X total]
**Presenter:** [Name]

---

## Slide 1: Title

**Content:** [Slide content]
**Visual:** [Description]
**Speaker Notes:** [Notes]

---

[Continue for all slides]

---

## Engagement Plan

[Poll and interaction schedule]

---

## Timing Runsheet

| Slide | Topic | Time | Cumulative |
| ----- | ----- | ---- | ---------- |
```

## Validation

Before completing:

- [ ] Slide count matches duration
- [ ] One key message per slide
- [ ] Speaker notes for every slide
- [ ] Engagement every 10-15 minutes
- [ ] Clear CTA included
- [ ] Visual suggestions provided
- [ ] Timing adds up correctly

## Error Handling

- **Topic too broad**: Help narrow to 3-5 key points for the duration.
- **No clear goal**: Ask for desired attendee action post-webinar.
- **Too much content**: Prioritize; suggest follow-up content for extras.
- **No visuals available**: Provide detailed descriptions for designer.
- **First-time presenter**: Add more detailed speaker notes and timing cues.

## Resources

- [Canva Presentations](https://www.canva.com/) - Quick slide design
- [Beautiful.ai](https://www.beautiful.ai/) - AI-powered slides
- [Pitch](https://pitch.com/) - Collaborative presentations
- [Mentimeter](https://www.mentimeter.com/) - Live polling
