---
name: design-brief-generator
description: Generate comprehensive design briefs for design projects. Use this skill when designers ask to "create a design brief", "structure a design project", "define design requirements", or need help planning design work.
---

# Design Brief Generator

## Overview

Generate comprehensive, well-structured design briefs that align stakeholders and guide design projects. This skill helps designers create clear project briefs that define scope, goals, constraints, and success criteria.

**Built for:**
- UX/UI designers
- Product designers
- Design leads
- Design systems teams
- Brand designers

---

## Quick Start

### 1. Generate Design Brief

Run the interactive script:

```bash
scripts/generate_brief.sh
```

This will guide you through creating a comprehensive design brief covering:
- Project goals and objectives
- Target users and personas
- Design constraints
- Success criteria
- Timeline and deliverables

### 2. Validate Brief

Check brief completeness:

```bash
scripts/validate_brief.sh <brief_file.md>
```

Ensures all critical sections are included.

---

## Core Workflow

### When to Create a Design Brief

**Use a design brief for:**
- New product/feature design projects
- Design system initiatives
- Redesign projects
- Brand identity projects
- UX research initiatives

**Skip for:**
- Minor UI tweaks
- Bug fixes
- Small iterations on existing designs

---

## Design Brief Components

### 1. Project Overview

**What it includes:**
- Project name and description
- Background and context
- Why this project matters now
- Business objectives
- User problems being solved

**Example:**
```markdown
## Project Overview

**Project:** Mobile app redesign
**Background:** Current app has 2.8 star rating with users citing confusing navigation
**Business Goal:** Increase app retention from 15% to 40% (Day 30)
**User Problem:** Users can't find key features, leading to frustration and abandonment
```

---

### 2. Design Goals & Objectives

**Define what success looks like:**
- Primary design goal
- Secondary goals
- Success metrics
- Must-haves vs. nice-to-haves

**Example:**
```markdown
## Design Goals

**Primary Goal:** Create intuitive navigation that helps users complete core tasks in < 3 taps

**Secondary Goals:**
- Reduce visual clutter by 40%
- Improve accessibility (WCAG AA compliance)
- Establish reusable component library

**Success Metrics:**
- Task success rate: 90%+
- Time on task: -50%
- SUS score: 75+
```

---

### 3. Target Users & Personas

**Who are we designing for:**
- Primary user personas
- User needs and pain points
- User goals and motivations
- Technical proficiency
- Context of use

**Example:**
```markdown
## Target Users

**Primary Persona:** Sarah, Marketing Manager
- **Age:** 32-45
- **Tech Savvy:** Medium
- **Goals:** Create campaigns quickly, track performance
- **Pain Points:** Current tool too complex, takes too long
- **Context:** Uses on desktop during work hours, sometimes mobile
```

---

### 4. Design Principles & Direction

**Guiding principles for the project:**
- Core design principles
- Visual direction
- Interaction patterns
- Content strategy
- Accessibility requirements

**Example:**
```markdown
## Design Principles

1. **Clarity over cleverness** - Users should never wonder what to do next
2. **Progressive disclosure** - Show what's needed, hide complexity
3. **Consistent patterns** - Use established design system components
4. **Accessible by default** - WCAG AA minimum, aim for AAA
```

---

### 5. Scope & Constraints

**What's in and out of scope:**

**In Scope:**
- Screens/flows included
- Platforms (web, mobile, tablet)
- Devices and browsers
- Accessibility requirements

**Out of Scope:**
- What we're NOT designing
- Future considerations

**Constraints:**
- Technical limitations
- Timeline constraints
- Resource constraints
- Brand guidelines to follow

**Example:**
```markdown
## Scope

**In Scope:**
- Dashboard redesign (5 screens)
- Mobile responsive (iOS, Android)
- Dark mode support
- WCAG AA compliance

**Out of Scope:**
- Admin panel (separate project)
- Native mobile apps (web only)
- Marketing website

**Constraints:**
- Must use existing design system
- Launch deadline: 8 weeks
- Development team: 2 engineers
- No custom illustrations budget
```

---

### 6. User Flows & Journeys

**Key user paths to design:**
- Primary user flows
- Entry points
- Decision points
- Success states
- Error states

**Example:**
```markdown
## Key User Flows

**Flow 1: Create Campaign**
1. Land on dashboard
2. Click "New Campaign"
3. Choose template
4. Customize content
5. Preview
6. Publish
7. Success confirmation

**Flow 2: View Analytics**
[Define the flow]
```

---

### 7. Deliverables & Timeline

**What will be delivered:**

**Design Deliverables:**
- User research (if needed)
- Wireframes
- High-fidelity mockups
- Interactive prototype
- Design specifications
- Component documentation
- Accessibility annotations

**Timeline:**
- Week 1-2: Research & wireframes
- Week 3-4: High-fidelity designs
- Week 5-6: Prototype & testing
- Week 7-8: Refinement & handoff

---

### 8. Success Criteria

**How we'll measure success:**

**Qualitative:**
- User testing feedback
- Stakeholder approval
- Designer review
- Accessibility audit pass

**Quantitative:**
- Task success rate
- Time on task
- Error rate
- SUS score
- NPS

**Example:**
```markdown
## Success Criteria

**Usability Testing:**
- 8/10 users complete primary task without help
- Average SUS score: 75+
- Zero critical accessibility issues

**Business Metrics (post-launch):**
- 40% Day 30 retention (up from 15%)
- 90% task completion rate
- < 5% error rate
```

---

## Design Project Types

### 1. New Feature Design

**Focus areas:**
- User needs validation
- Integration with existing product
- Interaction patterns
- Edge cases

**Brief template:** Standard brief with emphasis on user flows

---

### 2. Redesign Project

**Focus areas:**
- Current state analysis
- What's working/not working
- Migration considerations
- Before/after comparisons

**Additional sections:**
- Current pain points
- Competitive analysis
- Design audit findings

---

### 3. Design System

**Focus areas:**
- Component inventory
- Design principles
- Usage guidelines
- Governance

**Additional sections:**
- Adoption strategy
- Documentation plan
- Maintenance plan

---

### 4. Brand/Visual Design

**Focus areas:**
- Brand attributes
- Visual language
- Mood boards
- Design explorations

**Additional sections:**
- Brand guidelines
- Application examples
- Asset deliverables

---

## Stakeholder Alignment

### Discovery Questions

**Ask before starting:**
1. What problem are we solving?
2. Who are the users?
3. What are the business goals?
4. What's the timeline?
5. What are the constraints?
6. How will we measure success?
7. Who needs to approve?

### Stakeholder Review Process

**Brief review checklist:**
- [ ] Product Manager reviewed
- [ ] Engineering lead reviewed (feasibility)
- [ ] Design lead approved
- [ ] Key stakeholders aligned
- [ ] Success metrics agreed upon
- [ ] Timeline confirmed
- [ ] Resources allocated

---

## Design Brief Best Practices

### DO:
- ✅ **Start with "why"** - Clearly state the problem
- ✅ **Define success** - Specific, measurable criteria
- ✅ **Include constraints** - Technical, time, resource
- ✅ **Show examples** - Inspiration, references
- ✅ **Get buy-in early** - Review draft with stakeholders
- ✅ **Keep it concise** - 2-3 pages maximum
- ✅ **Make it visual** - Include diagrams, mockups, references

### DON'T:
- ❌ **Jump to solutions** - Focus on problem first
- ❌ **Be vague** - "Make it better" isn't helpful
- ❌ **Ignore constraints** - They shape the solution
- ❌ **Work in isolation** - Involve PM, Engineering early
- ❌ **Skip research** - Base decisions on data
- ❌ **Forget accessibility** - Consider from the start

---

## Accessibility in Design Briefs

### Minimum Requirements

**Every design brief should include:**

**WCAG Compliance:**
- [ ] Target level (A, AA, AAA)
- [ ] Color contrast requirements (4.5:1 for text)
- [ ] Keyboard navigation support
- [ ] Screen reader compatibility
- [ ] Touch target sizes (44x44px minimum)

**Testing Plan:**
- [ ] Screen reader testing (NVDA, JAWS, VoiceOver)
- [ ] Keyboard-only navigation
- [ ] Color contrast validation
- [ ] Automated testing (axe, Lighthouse)

See `references/accessibility_guidelines.md` for complete checklist.

---

## Cross-Functional Collaboration

### Working with Product

**PM provides:**
- Business requirements
- User research
- Success metrics
- Timeline constraints

**Designer provides:**
- Design expertise
- User experience recommendations
- Feasibility feedback
- Design timeline

### Working with Engineering

**Engineering needs from brief:**
- Technical constraints acknowledged
- Interaction patterns defined
- Edge cases documented
- Component reuse identified

**Design provides to Engineering:**
- Design specifications
- Component documentation
- Interaction details
- Responsive breakpoints

---

## Design Tools & Templates

### Recommended Tools

**Design Briefs:**
- Notion (collaborative docs)
- Confluence
- Google Docs
- Figma FigJam (visual briefs)

**User Flows:**
- Figma
- Miro
- Whimsical
- FigJam

**Prototyping:**
- Figma
- Framer
- ProtoPie
- Principle

---

## Example Design Briefs

### Example 1: Mobile App Feature

```markdown
# Design Brief: In-App Messaging

## Project Overview
Add direct messaging between users within our fitness app.

**Business Goal:** Increase engagement, reduce churn
**User Problem:** Users want to connect with workout partners

## Design Goals
- Enable 1:1 messaging
- Keep it simple and focused
- Integrate with existing notifications

## Target Users
Primary: Sarah, fitness enthusiast, 28-45, uses app 4x/week

## Scope
**In:** 1:1 text messaging, read receipts, notifications
**Out:** Group chat, media sharing (future phase)

## Success Criteria
- 40% of users try messaging in first 30 days
- 20% become weekly active messagers
- No increase in support tickets

## Timeline
6 weeks: Research (1w), Design (3w), Prototype & Test (2w)
```

---

### Example 2: Dashboard Redesign

```markdown
# Design Brief: Analytics Dashboard Redesign

## Project Overview
Redesign analytics dashboard to improve data comprehension.

**Current Issues:**
- Users overwhelmed by data
- Key metrics buried
- Poor mobile experience

## Design Goals
1. Surface most important metrics first
2. Enable drill-down for details
3. Make it mobile-friendly

## Target Users
- Marketing managers (primary)
- Executives (secondary)
- Data analysts (tertiary)

## Success Criteria
- Users find key metric in < 10 seconds
- Mobile traffic increases 30%+
- SUS score: 75+

## Timeline
8 weeks (Research: 2w, Design: 4w, Testing: 2w)
```

---

## Resources

### Scripts

- **generate_brief.sh** - Interactive brief generation
- **validate_brief.sh** - Check brief completeness

### References

- **design_brief_template.md** - Comprehensive template
- **accessibility_guidelines.md** - WCAG checklist
- **design_principles.md** - Common design principles
- **user_research_methods.md** - Research guidance

---

## Tips for Designers

### Before Creating the Brief

1. **Talk to stakeholders** - Understand the real problem
2. **Review existing research** - Don't start from scratch
3. **Check technical constraints** - Talk to engineering
4. **Understand the timeline** - Be realistic

### During Brief Creation

1. **Start with template** - Don't reinvent the wheel
2. **Be specific** - Vague briefs lead to vague designs
3. **Include visuals** - Mood boards, references, examples
4. **Define success** - How will you know it worked?

### After Brief Creation

1. **Review with PM** - Align on goals and scope
2. **Review with Engineering** - Validate feasibility
3. **Get stakeholder sign-off** - Explicit approval
4. **Treat it as living doc** - Update as you learn

---

## Common Pitfalls

### Pitfall 1: Too Broad

**Problem:** "Redesign the entire app"
**Solution:** Break into phases, prioritize

### Pitfall 2: Solution-First

**Problem:** "Make it look like Apple"
**Solution:** Start with user problems, not aesthetics

### Pitfall 3: No Constraints

**Problem:** Ignoring technical/time limits
**Solution:** Document and respect constraints

### Pitfall 4: Skipping Research

**Problem:** Designing based on assumptions
**Solution:** At minimum, review existing data

### Pitfall 5: Vague Success Criteria

**Problem:** "Make it better" isn't measurable
**Solution:** Define specific, testable criteria

---

## Summary

A great design brief:

1. **Defines the problem** clearly
2. **Sets goals** and success criteria
3. **Identifies users** and their needs
4. **Documents constraints** (time, tech, budget)
5. **Aligns stakeholders** early
6. **Guides the work** without being prescriptive
7. **Evolves** as you learn

**Get started:**
```bash
scripts/generate_brief.sh
```

This creates a solid foundation for successful design projects.
