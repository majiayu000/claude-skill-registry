---
name: design-research
description: "Conduct foundational research to understand project context, user needs, business goals, and constraints before design begins. Use for: starting new projects, understanding requirements, defining scope, identifying constraints, and establishing design direction."
---

# Design Research

## Description

Design Research is the foundational skill for understanding project context, user needs, business goals, and constraints before any visual design begins. This skill ensures all subsequent design decisions are grounded in real understanding rather than assumptions.

## When to Use

- Starting any new design project
- Redesigning existing products
- Launching new features
- Pivoting design direction
- When requirements are unclear

---

## Instructions for AI Agents

### Step 1: Gather Project Requirements

**Prompt to extract requirements:**
```
Analyze the following project brief and extract:
1. Primary business goals (what success looks like)
2. Target audience description
3. Key features/functionality needed
4. Brand guidelines or constraints
5. Technical constraints (platforms, frameworks)
6. Timeline and budget considerations
7. Competitive landscape
8. Success metrics

Project brief: [INSERT BRIEF]
```

**Required information to collect:**

| Category | Questions to Answer |
|----------|--------------------|
| Business | What problem are we solving? What are the business objectives? |
| Users | Who will use this? What are their needs? |
| Scope | What pages/screens/features are needed? |
| Brand | Are there existing brand guidelines? Colors? Fonts? |
| Platform | Web only? Mobile app? Both? |
| Timeline | When is this needed? Are there milestones? |
| Competitors | Who are the main competitors? |

### Step 2: Analyze Target Audience

**Prompt for audience analysis:**
```
Based on the target audience of [AUDIENCE DESCRIPTION], identify:
1. Demographics (age, location, profession)
2. Technical proficiency level
3. Device preferences (mobile-first vs desktop)
4. Key pain points and motivations
5. Design expectations based on their industry
6. Accessibility considerations
```

### Step 3: Define Design Direction

**Prompt for design direction:**
```
Based on the following project requirements and audience:
[INSERT REQUIREMENTS AND AUDIENCE INFO]

Recommend:
1. Visual style direction (modern/minimal, bold/playful, corporate/professional, etc.)
2. Color mood (warm, cool, neutral, vibrant)
3. Typography character (elegant, friendly, technical, authoritative)
4. Layout approach (dense information, spacious, card-based, etc.)
5. Interaction level (simple, animated, highly interactive)

Provide reasoning for each recommendation.
```

### Step 4: Document Constraints

**Categories of constraints to identify:**

- **Technical**: Browser support, framework limitations, performance requirements
- **Brand**: Existing colors, fonts, logo usage rules
- **Content**: Text length limits, image availability, localization needs
- **Accessibility**: WCAG level required (AA minimum)
- **Legal**: Privacy policies, terms display requirements, cookie consent

---

## Example Input/Output

### Example Input

```markdown
**Project Brief:**
We need a landing page for our new SaaS product "TaskFlow" - a project 
management tool for small creative agencies. Target audience is creative 
directors and project managers at agencies with 5-20 employees. They're 
tech-savvy but time-poor. We want to feel modern and premium but approachable. 
We have a logo but no brand guidelines yet. Competitors include Monday.com, 
Asana, and Notion. Launch in 6 weeks.
```

### Example Output

```markdown
## TaskFlow Design Research Brief

### Business Goals
1. **Primary**: Generate sign-ups for free trial
2. **Secondary**: Establish brand recognition in creative agency market
3. **Success Metric**: 3% conversion rate from landing page visitors

### Target Audience Profile
- **Primary User**: Creative directors/project managers
- **Company Size**: 5-20 employees
- **Industry**: Creative agencies (design, advertising, marketing)
- **Tech Proficiency**: High - familiar with modern SaaS tools
- **Device**: Likely 60% desktop during work, 40% mobile for research
- **Pain Points**: Overwhelmed by complex tools, need simplicity
- **Motivations**: Look professional to clients, save time, reduce chaos

### Competitive Analysis Summary
| Competitor | Strength | Weakness | Opportunity |
|------------|----------|----------|-------------|
| Monday.com | Visual, colorful | Can feel overwhelming | More focused simplicity |
| Asana | Established trust | Corporate feeling | More creative personality |
| Notion | Flexible | Learning curve | Purpose-built for agencies |

### Design Direction Recommendation

**Visual Style**: Modern minimal with creative touches
- Clean layouts with generous whitespace
- Subtle playful elements (micro-interactions, illustrations)
- Premium feel without being cold

**Color Direction**: 
- Primary: Warm, approachable accent (coral, amber, or purple)
- Neutral base: Clean grays and whites
- Avoid: Bright primary colors (too corporate)

**Typography Direction**:
- Modern sans-serif for headings (geometric or humanist)
- Highly readable sans-serif for body
- Consider: Inter, Outfit, Satoshi

**Layout Approach**:
- Spacious, not cramped
- Card-based UI for features
- Progressive disclosure (don't overwhelm)

**Interaction Level**: 
- Subtle micro-interactions
- Smooth scroll animations
- Interactive demo/preview if possible

### Constraints Identified
- **Technical**: Web-first, must be responsive
- **Brand**: Logo exists, colors TBD
- **Content**: Need copywriting support
- **Accessibility**: WCAG AA minimum
- **Timeline**: 6 weeks to launch

### Next Steps
1. Gather inspiration from Dribbble (SaaS, project management, creative tools)
2. Conduct competitive visual analysis
3. Create user personas
4. Begin wireframing hero section
```

---

## Prompts Library

### Quick Requirements Extraction
```
From this project description, create a structured brief:
[PROJECT DESCRIPTION]

Format as:
- Project Type:
- Business Goal:
- Target Users:
- Key Features:
- Platforms:
- Design Constraints:
- Timeline:
```

### Audience Deep Dive
```
For an audience of [AUDIENCE TYPE] in [INDUSTRY]:
1. What design patterns are they familiar with?
2. What level of visual sophistication do they expect?
3. What are their accessibility needs?
4. Mobile or desktop primary?
5. What emotional tone resonates with them?
```

### Competitor Quick Analysis
```
Analyze the visual design approach of [COMPETITOR URL]:
1. Color palette used
2. Typography choices
3. Layout patterns
4. Unique design elements
5. Strengths to learn from
6. Weaknesses to avoid
```

### Design Direction Decision
```
Given these requirements: [REQUIREMENTS]

Choose between these design directions and explain why:
A) Minimal and professional
B) Bold and energetic
C) Warm and approachable
D) Technical and precise

Consider: audience expectations, competitive differentiation, brand personality
```

---

## Resources

### Research Templates
- Project brief template (create from example above)
- Competitive analysis matrix
- Audience profile template

### External Resources
- Nielsen Norman Group UX Research Methods: https://nngroup.com/articles/which-ux-research-methods/
- Google Design Sprint methodology: https://designsprintkit.withgoogle.com

---

## Success Criteria

### Minimum Requirements
- [ ] Business goals clearly defined
- [ ] Target audience identified and described
- [ ] Key features/pages listed
- [ ] Design direction recommended
- [ ] Constraints documented

### Quality Indicators
- [ ] Research informs all design decisions
- [ ] No major assumptions left unclarified
- [ ] Competitive context understood
- [ ] Clear actionable next steps defined

---

## Common Pitfalls

1. **Skipping research**: Leads to designs that miss the mark
2. **Too broad audience**: "Everyone" is not a target audience
3. **Ignoring constraints**: Technical limits discovered late cause rework
4. **Copying competitors**: Research to differentiate, not duplicate
5. **Analysis paralysis**: Research should inform, not delay indefinitely

---

## Related Skills

- **Next**: `inspiration_gathering.md` - Find visual references
- **Next**: `competitive_analysis.md` - Deep dive on competitors
- **Next**: `user_personas.md` - Create detailed user profiles
