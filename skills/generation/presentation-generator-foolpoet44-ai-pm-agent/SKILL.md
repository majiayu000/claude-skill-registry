---
name: presentation-generator
description: Google Slides presentation creation for PM deliverables. Use when creating presentations from PRDs, pitching ideas, stakeholder updates, or product roadmaps. Triggers on "presentation", "slides", "pitch deck", "stakeholder meeting", "Google Slides".
allowed-tools: Read, Write, Edit
model: inherit
---

# Presentation Generator Skill - PM Presentation Creation

This Skill helps create compelling Google Slides presentations from PM documents for stakeholder meetings, product pitches, and roadmap reviews.

## When to Use This Skill

Use this Skill when you need to:
- Create product pitch decks from idea validation
- Present PRDs to stakeholders
- Build roadmap presentations
- Prepare sprint reviews or demos
- Generate executive updates
- Create customer-facing presentations

## Core Process

### Step 1: Input Analysis

**Required Inputs:**
- Source document (PRD, User Stories, Idea Report)
- Presentation type (pitch, review, update, roadmap)
- Target audience (executives, team, customers, investors)
- Time limit (5min, 15min, 30min, 1hr)

**Determine Slide Count:**
- 5 min presentation: 5-7 slides
- 15 min presentation: 10-12 slides
- 30 min presentation: 15-20 slides
- 1 hour presentation: 25-30 slides

### Step 2: Presentation Templates

#### Product Pitch Deck (Idea → Stakeholders)

**Slide Structure (12 slides, 15-20 minutes):**

1. **Cover Slide**
   - Product name (large, bold)
   - Tagline (one-line value prop)
   - Presenter name & date
   - Company logo

2. **Problem Slide**
   - Title: "The Problem"
   - 3 key pain points (bullet points)
   - Customer quote or stat
   - Visuals: Icon or photo representing problem

3. **Solution Slide**
   - Title: "Our Solution"
   - Core solution (2-3 sentences)
   - Key differentiation
   - Visual: Product screenshot or mockup

4. **How It Works**
   - Title: "How It Works"
   - 3-4 step process with icons
   - Simple, visual flow
   - Minimal text

5. **Market Opportunity**
   - Title: "Market Opportunity"
   - TAM/SAM/SOM (visual chart)
   - Market growth trends
   - Key stats (large numbers)

6. **Competition**
   - Title: "Competitive Landscape"
   - 2x2 matrix or comparison table
   - "Our unique advantage" callout
   - Positioning statement

7. **Target Customer**
   - Title: "Who It's For"
   - Primary persona (name, photo, quote)
   - Demographics & behaviors
   - Jobs-to-be-Done

8. **Business Model**
   - Title: "Business Model"
   - Revenue streams
   - Pricing strategy
   - Unit economics (LTV, CAC)

9. **Product Roadmap**
   - Title: "Roadmap"
   - Now-Next-Later timeline
   - Key milestones
   - MVP features highlighted

10. **Go-to-Market**
    - Title: "Go-to-Market Strategy"
    - Launch plan (phases)
    - Marketing channels
    - Success metrics

11. **Team**
    - Title: "The Team"
    - Key team members (photos, titles)
    - Relevant experience
    - Advisors (if applicable)

12. **Ask/Next Steps**
    - Title: "Next Steps"
    - Clear ask (approval, funding, resources)
    - Timeline
    - Contact information

#### PRD Review Presentation (PRD → Stakeholders)

**Slide Structure (15 slides, 30 minutes):**

1. **Cover**
   - Product/Feature name
   - Version & date
   - PM name

2. **Agenda**
   - Overview
   - Goals & Success Metrics
   - Features
   - Timeline
   - Q&A

3. **Executive Summary**
   - Problem statement
   - Solution overview
   - Expected impact

4. **Goals & Objectives**
   - Business goals
   - User goals
   - OKRs (table format)

5. **Target Users**
   - Primary persona
   - Use cases
   - Pain points addressed

6. **Key Features (Overview)**
   - Top 5 features (icons + descriptions)
   - MVP scope highlighted

7-11. **Feature Details** (1 slide per major feature)
   - Feature name
   - User value
   - Acceptance criteria (key points)
   - Mockup/wireframe

12. **Technical Approach**
   - High-level architecture
   - Key integrations
   - Technical dependencies

13. **Success Metrics**
   - KPIs table
   - Target values
   - How we'll measure

14. **Timeline & Milestones**
   - Gantt chart or timeline
   - Key dates
   - Dependencies

15. **Next Steps & Q&A**
   - Approval needed
   - Open questions
   - Contact for follow-up

#### Sprint Review Presentation (User Stories → Team)

**Slide Structure (8 slides, 15 minutes):**

1. **Cover**
   - Sprint number
   - Date range
   - Team name

2. **Sprint Goal**
   - What we committed to
   - Why it matters

3. **Completed Stories**
   - List with checkmarks
   - Story points completed
   - Velocity

4-6. **Demo Slides** (1 per major feature)
   - Feature name
   - Before/After screenshots
   - Key functionality

7. **Metrics**
   - Sprint burndown chart
   - Velocity trend
   - Quality metrics (bugs, test coverage)

8. **Retrospective & Next Sprint**
   - What went well
   - What to improve
   - Next sprint preview

#### Roadmap Presentation (Strategy → Stakeholders)

**Slide Structure (10 slides, 20 minutes):**

1. **Cover**
   - Product name
   - Roadmap period (Q1-Q4 2024)

2. **Product Vision**
   - Where we're going
   - Strategic priorities

3. **Now (Current Quarter)**
   - Features in development
   - Expected completion dates

4. **Next (Next 1-2 Quarters)**
   - Planned features
   - Dependencies

5. **Later (6+ Months)**
   - Future vision
   - Research & exploration

6. **Themes**
   - Theme 1: Customer onboarding
   - Theme 2: Power user features
   - Theme 3: Enterprise capabilities

7. **Success Metrics**
   - How we'll track progress
   - Target KPIs per quarter

8. **Resource Needs**
   - Team capacity
   - Hiring plans
   - Budget requirements

9. **Risks & Mitigations**
   - Key risks
   - Mitigation strategies

10. **Q&A**
    - Discussion
    - Feedback welcome

### Step 3: Slide Design Principles

#### Visual Hierarchy
- **Title:** 44pt, Bold
- **Heading:** 32pt, Bold
- **Body:** 20-24pt, Regular
- **Captions:** 16pt, Light

#### Color Scheme
**Primary Palette:**
- Primary: #1976D2 (Blue)
- Secondary: #FFC107 (Amber)
- Accent: #4CAF50 (Green)
- Background: #FFFFFF (White)
- Text: #212121 (Dark Gray)

**Semantic Colors:**
- Success: #4CAF50 (Green)
- Warning: #FF9800 (Orange)
- Error: #F44336 (Red)
- Info: #2196F3 (Blue)

#### Layout Rules
- **6x6 Rule**: Max 6 bullets, max 6 words per bullet
- **White Space**: 30-40% of slide should be empty
- **Alignment**: Left-align text, center images
- **Consistency**: Same font, colors, layout throughout

#### Typography
- **Headings**: Sans-serif (Roboto, Open Sans, Arial)
- **Body**: Sans-serif
- **Data**: Monospace for numbers (if tables)
- **No more than 2 fonts** per presentation

#### Imagery
- **High Quality**: Min 1920x1080px
- **Relevant**: Support the message
- **Consistent Style**: Photos or illustrations, not mixed
- **Icons**: Simple, one color, same style set

### Step 4: Slide Content Guidelines

#### Title Slides
```
[Large Product Name]
[Tagline in smaller text]

[Presenter Name]
[Date]
[Company Logo]
```

#### Content Slides
```
[Slide Title]

• [Key Point 1]
  • Supporting detail (if needed)

• [Key Point 2]

• [Key Point 3]

[Visual: Chart, Image, or Diagram]
```

#### Data Slides
```
[Slide Title]

[Large Key Metric: 150K Users]
↑ 35% from last quarter

[Supporting Chart or Graph]

Key Insight: [One-sentence takeaway]
```

#### Quote Slides
```
"[Powerful customer quote or testimonial]"

— [Name, Title]
[Photo of person]
```

### Step 5: Presentation Types

#### For Executives
- Focus on business impact
- Use large numbers and clear charts
- Minimize technical details
- Highlight ROI and risk mitigation
- Keep slides simple and visual
- Anticipate tough questions

#### For Technical Teams
- Include architecture diagrams
- Show technical dependencies
- Detail implementation approach
- Discuss trade-offs
- Be precise with requirements
- Allow for deep Q&A

#### For Customers
- Focus on benefits, not features
- Use real-world scenarios
- Show product in action (screenshots, demo)
- Include testimonials
- Clear call-to-action
- Avoid jargon

#### For Investors
- Market opportunity (TAM/SAM/SOM)
- Traction and metrics
- Competitive advantage
- Team credentials
- Financial projections
- Clear ask (funding amount, use of funds)

## Workaround (Until Google Drive MCP Available)

**Current Approach:**

### Generate Slide-by-Slide Markdown

```markdown
---
PRESENTATION METADATA:
- Type: [Product Pitch | PRD Review | Sprint Review | Roadmap]
- Title: [Presentation Title]
- Audience: [Executives | Team | Customers | Investors]
- Duration: [15 minutes]
- Slide Count: [12 slides]
- Date: [YYYY-MM-DD]
---

# Slide 1: Cover

**Layout:** Title Slide

**Title:**
[Product Name]

**Subtitle:**
[One-line value proposition]

**Footer:**
[Presenter Name] | [Date] | [Company]

**Design Notes:**
- Large, bold title (60pt)
- Company logo top-right
- Clean, minimal design

---

# Slide 2: Problem

**Layout:** Content with Icon

**Title:**
The Problem

**Content:**
• [Pain Point 1 - 6 words max]

• [Pain Point 2 - 6 words max]

• [Pain Point 3 - 6 words max]

**Visual:**
[Icon or image representing the problem]

**Speaker Notes:**
[Detailed explanation to elaborate during presentation]

---

# Slide 3: Solution

**Layout:** Content with Screenshot

**Title:**
Our Solution

**Content:**
[2-3 sentence description of core solution]

**Key Differentiation:**
• [Unique aspect 1]
• [Unique aspect 2]

**Visual:**
[Product screenshot or mockup]

**Speaker Notes:**
[How this solves the problem, why it's better]

---

[Continue for all slides...]

---

## Conversion Instructions

To create Google Slides from this content:

**Option 1: Manual Creation**
1. Open Google Slides
2. Choose a template or start blank
3. Create slides following the structure above
4. Apply consistent formatting
5. Add visuals as indicated

**Option 2: Use Slides API (when MCP available)**
1. Authenticate with Google Slides API
2. Run automated script
3. Review and adjust

**Option 3: Export to PowerPoint**
1. Create in PowerPoint first
2. Import to Google Slides
3. Adjust formatting

## Design Checklist

- [ ] Consistent fonts throughout (max 2 fonts)
- [ ] Color scheme applied consistently
- [ ] High-quality images (min 1920x1080)
- [ ] Icons in consistent style
- [ ] Text follows 6x6 rule
- [ ] Adequate white space (30-40%)
- [ ] Slide numbers added
- [ ] Company branding applied
- [ ] Speaker notes included
- [ ] Spell-check completed
- [ ] Accessibility checked (contrast, alt text)
```

### Include Visual Guidance

For each slide, specify:
- **Layout Type**: Title, Content, Two-Column, etc.
- **Visual Element**: Chart type, icon, image description
- **Color Emphasis**: Which elements should stand out
- **Animation** (optional): Fade in, appear, none

## Best Practices

### Content
✅ **Do:**
- One main idea per slide
- Use visuals to support, not decorate
- Tell a story (problem → solution → impact)
- Include concrete examples
- End with clear call-to-action

❌ **Don't:**
- Overcrowd slides with text
- Use bullet points as script
- Include every detail from PRD
- Use low-quality images
- Forget speaker notes

### Design
✅ **Do:**
- Use high contrast (dark text on light background)
- Align elements consistently
- Use brand colors
- Keep it simple and clean
- Test readability from distance

❌ **Don't:**
- Use more than 3 colors per slide
- Mix too many fonts
- Use distracting animations
- Ignore white space
- Sacrifice readability for style

### Delivery
✅ **Do:**
- Practice timing (1-2 min per slide)
- Prepare for questions
- Have backup slides (appendix)
- Test tech before presenting
- Bring printouts as backup

❌ **Don't:**
- Read slides verbatim
- Turn back to audience
- Rush through data slides
- Skip rehearsal
- Forget to pause for questions

## Output Template

```markdown
# [Presentation Title]

**Metadata:**
- Type: [Type]
- Audience: [Audience]
- Duration: [X minutes]
- Slides: [Y slides]

---

## Slide Outline

1. Cover
2. [Slide title]
3. [Slide title]
4. [Slide title]
...
N. Next Steps / Q&A

---

## Slide-by-Slide Content

[Detailed content for each slide as shown above]

---

## Appendix (Backup Slides)

[Additional slides for potential questions]

---

## Speaker Notes

[Overall presentation flow and key talking points]
```

## Integration Points

This Skill works with:
- **idea-agent**: Creates pitch decks from idea validation
- **prd-agent**: Creates PRD review presentations
- **userstory-agent**: Creates sprint review presentations
- **google-docs-writer**: Shares document formatting principles

## Success Criteria

Presentations should:
- [ ] Tell a clear, compelling story
- [ ] Be visually appealing and professional
- [ ] Fit within time constraints
- [ ] Engage the target audience
- [ ] Drive desired action (approval, funding, buy-in)
- [ ] Be accessible (readable, high contrast)
- [ ] Include speaker notes for delivery
- [ ] Have backup slides for Q&A

---

Use this Skill to create persuasive, professional presentations that effectively communicate PM insights and drive stakeholder decisions.
