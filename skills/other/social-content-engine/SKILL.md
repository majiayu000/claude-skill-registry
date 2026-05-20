---
name: social-content-engine
description: Generates a 30-day "Warm Up" content calendar (Tweets, IG Reels ideas, LinkedIn posts).
---

# Social Content Engine

This skill generates a strategic 30-day content calendar to build an audience before launch.

## Input Variables
- [MDS] (Messaging Direction Summary)
- [PERSONA_DATA] (Buyer Persona)
- [PRE_LAUNCH_EMAILS] (Optional: to sync topics)

## The Protocol
1.  **Weekly Themes**: Assign a theme to each of the 4 weeks (e.g., Pain Awareness, Solution Education, Social Proof, Launch Hype).
2.  **Platform Strategy**: Adapt content for:
    - **Visual** (Instagram/TikTok): Reels ideas, carousels.
    - **Text** (Twitter/LinkedIn): Threads, thought leadership, questions.
3.  **Content Mix**: Ensure balance:
    - 40% Value (Education/Entertainment)
    - 30% Connection (Founder story/Behind the scenes)
    - 20% Engagement (Polls/Questions)
    - 10% Promotion (Signup CTA)
4.  **Daily Plan**: Generate specific post ideas with hooks and media descriptions for 30 days.

## Output Instructions
Render into `templates/social-content-calendar.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `social-content-engine`
- **Path**: `skills/social-content-engine/templates/social-content-calendar.md`
- **Context**: Part of *Social & Community*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `social-content-calendar.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate social-content-engine
```
