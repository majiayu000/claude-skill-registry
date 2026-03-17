---
name: frontend-orchestrator
description: Master coordinator skill that diagnoses your application's design maturity level and sequences all 13 frontend design skills in the optimal order. Analyzes current state, identifies gaps, and creates a personalized implementation roadmap for transforming your MVP into a world-class experience.
---

# Frontend Design Orchestrator

## Overview

The Frontend Design Orchestrator is your strategic guide for applying the philosophy of "uncommon care" to your digital product. Rather than randomly applying design skills, this orchestrator helps you understand where your application stands, what matters most right now, and which skills to deploy in what sequence.

This skill embodies the principle: **"Reduce until it's clear, refine until it's right."** It helps you identify what's essential for your current stage and focuses your effort there first.

## The 13 Frontend Design Skills

Your complete design system includes:

**Foundation Layer:**
1. **design-foundation** — Design tokens, system structure, principles
2. **design-engineer-mindset** — Bridge design and implementation, code as material

**Visual Layer:**
3. **layout-system** — Responsive layouts, grids, flexbox, container queries
4. **typography-system** — Type scales, hierarchy, readability
5. **color-system** — Color theory, accessibility, theming
6. **visual-hierarchy-refactoring** — Size, weight, contrast, whitespace, Gestalt principles

**Component Layer:**
7. **component-architecture** — Atomic design, composition, variants, documentation

**Interaction Layer:**
8. **interaction-physics** — Momentum, gestures, animation principles, implicit input
9. **loading-states** — Skeleton screens, spinners, progress bars, empty states
10. **error-handling-recovery** — Error messages, recovery workflows, graceful degradation
11. **performance-optimization** — Perceived latency, optimistic UI, Core Web Vitals

**Quality Layer:**
12. **accessibility-excellence** — WCAG compliance, semantic HTML, inclusive design
13. **frontend-orchestrator** — This skill - strategic coordination and sequencing

## Core Methodology: Design Maturity Assessment

Every application exists at one of five design maturity levels. Understanding your level is the first step to improvement.

### The Five Maturity Levels

**Level 1: Functional MVP**
Your application works. Users can accomplish their core goals. But the experience feels rough, inconsistent, or confusing. Design feels like an afterthought. This is where most startups begin.

**Level 2: Consistent Foundation**
You've established basic consistency. Components look similar, colors are somewhat coordinated, spacing has some logic. But the system isn't documented, and new features often break the pattern. Accessibility is partial or missing.

**Level 3: System-Driven**
You have a documented design system with tokens, components, and clear patterns. New features follow the system. Accessibility is integrated. But the system might feel generic, lacking personality or delight. Interactions feel mechanical.

**Level 4: Refined Experience**
Your system is mature and well-executed. Every detail has been considered. Interactions feel smooth and intentional. Accessibility is excellent. Users notice the care. But the experience might not yet feel timeless or anticipatory.

**Level 5: Transcendent Design**
This is rare. Your product doesn't just work well—it feels loved. The experience anticipates user needs. Every interaction delights. The design feels timeless, not trendy. Users recommend it not because they have to, but because they want to.

## The Orchestrator's Diagnostic Process

### Step 1: Current State Assessment

Before recommending skills, the orchestrator asks these diagnostic questions:

**Foundation Questions:**
- What is your primary goal right now? (Shipping fast, improving retention, reducing support tickets, building brand love?)
- How many users are actively using your product?
- What's your team's design maturity? (No designer, junior designer, experienced designer, design team?)
- How much technical debt do you have in your UI/CSS?

**Design System Questions:**
- Do you have a documented design system?
- Are you using a CSS framework (Tailwind, CSS-in-JS, vanilla CSS)?
- How consistent is your current design across the application?
- Do you have design tokens or design system documentation?

**User Experience Questions:**
- What's your biggest user frustration right now?
- How many accessibility issues have been reported?
- What's your mobile experience like compared to desktop?
- Do users comment on the feel or polish of your product?

**Interaction Questions:**
- How much thought has gone into animations and transitions?
- Do users understand what actions are available to them?
- How clear is your error messaging and feedback?
- Do interactions feel responsive and intentional?

**Performance Questions:**
- How fast does your application feel?
- Do users complain about loading times?
- Are there perceived performance issues?
- Do you measure Core Web Vitals?

### Step 2: Gap Analysis

Based on the assessment, the orchestrator identifies which skills will have the highest impact on your specific situation.

| Current State | Highest Impact Skill | Why | Secondary Skills |
| :--- | :--- | :--- | :--- |
| Functional MVP, no system | design-foundation | Establishing a foundation prevents future technical debt and enables faster, more consistent development. | layout-system, typography-system, design-engineer-mindset |
| Inconsistent design, partial system | design-foundation | Documenting and formalizing what exists prevents regressions and enables team alignment. | component-architecture, color-system, visual-hierarchy-refactoring |
| System exists, but feels generic | interaction-physics | Adding intentionality to interactions transforms a functional product into one that feels loved. | typography-system, accessibility-excellence, performance-optimization |
| Good system, poor accessibility | accessibility-excellence | Accessibility is foundational and affects all other skills. Fixing it first ensures all future work is accessible. | component-architecture, interaction-physics, error-handling-recovery |
| Mature system, needs refinement | interaction-physics, visual-hierarchy-refactoring | Refinement happens at the margins—in the details of how things move, feel, and communicate. | performance-optimization, loading-states, design-engineer-mindset |
| Users confused by interactions | error-handling-recovery, loading-states | Clear feedback and error messages reduce support tickets and improve confidence. | interaction-physics, performance-optimization |
| Slow perceived performance | performance-optimization | Perceived speed dramatically affects user satisfaction and retention. | loading-states, interaction-physics, design-engineer-mindset |

### Step 3: Skill Sequencing

The orchestrator recommends one of five implementation paths based on your situation:

**Path A: Building from Scratch (Functional MVP → Refined Experience)**
1. design-foundation — Establish tokens, system structure, component library
2. design-engineer-mindset — Understand code as design material
3. layout-system — Create responsive, accessible layout patterns
4. typography-system — Define type scales and hierarchy
5. visual-hierarchy-refactoring — Establish clear visual hierarchy through size, weight, contrast
6. color-system — Establish color system with accessibility in mind
7. component-architecture — Build reusable, well-documented components
8. loading-states — Design loading and empty states
9. error-handling-recovery — Design error states and recovery
10. interaction-physics — Add intentionality to animations and transitions
11. performance-optimization — Optimize perceived performance
12. accessibility-excellence — Audit and improve accessibility across all layers

**Path B: Formalizing Existing Design (Inconsistent → System-Driven)**
1. design-foundation — Document and formalize existing patterns
2. visual-hierarchy-refactoring — Audit and improve visual hierarchy
3. component-architecture — Extract and document existing components
4. layout-system — Audit and standardize layout patterns
5. typography-system — Audit and standardize typography
6. color-system — Audit and standardize color usage
7. design-engineer-mindset — Establish design-code alignment
8. accessibility-excellence — Audit and improve accessibility
9. loading-states — Standardize loading and empty states
10. error-handling-recovery — Standardize error handling
11. interaction-physics — Add intentionality to interactions
12. performance-optimization — Optimize perceived performance

**Path C: Improving Mature System (System-Driven → Transcendent)**
1. design-engineer-mindset — Deepen implementation fidelity
2. interaction-physics — Add delight and intentionality
3. visual-hierarchy-refactoring — Refine visual hierarchy
4. performance-optimization — Optimize perceived performance
5. loading-states — Enhance loading state design
6. error-handling-recovery — Enhance error state design
7. accessibility-excellence — Audit and enhance accessibility
8. typography-system — Refine typography and readability
9. color-system — Refine color system and theming
10. component-architecture — Enhance component library

**Path D: Fixing Performance Issues (Slow → Responsive)**
1. performance-optimization — Measure and optimize perceived latency
2. design-engineer-mindset — Understand rendering pipeline
3. loading-states — Implement skeleton screens and progress bars
4. interaction-physics — Optimize animation performance
5. error-handling-recovery — Improve error feedback
6. accessibility-excellence — Ensure accessibility during optimization

**Path E: Improving Accessibility (Partial → Excellent)**
1. accessibility-excellence — Audit and establish accessibility baseline
2. error-handling-recovery — Ensure error messages are accessible
3. loading-states — Ensure loading states are accessible
4. component-architecture — Build accessible components
5. interaction-physics — Ensure animations respect prefers-reduced-motion
6. visual-hierarchy-refactoring — Ensure sufficient contrast and hierarchy
7. typography-system — Ensure readable typography
8. performance-optimization — Ensure performance doesn't impact accessibility

## How to Use the Orchestrator

### Step 1: Assess Your Current State

Ask yourself these questions:

1. **What's your design maturity level?** (1-5)
2. **What's your biggest pain point?** (Inconsistency, performance, accessibility, interactions, etc.)
3. **What's your primary goal?** (Ship fast, improve retention, build brand love, etc.)
4. **What's your team size and expertise?** (Solo developer, junior designer, experienced team, etc.)

### Step 2: Choose Your Path

Based on your assessment, select the path that matches your situation:
- **Path A** if you're building from scratch
- **Path B** if you have inconsistent design you want to formalize
- **Path C** if you have a mature system you want to refine
- **Path D** if performance is your main issue
- **Path E** if accessibility is your main issue

### Step 3: Follow the Sequence

Work through the skills in the recommended order. Each skill builds on the previous ones.

### Step 4: Iterate and Refine

After implementing each skill, assess your progress. You may need to revisit earlier skills or adjust your path based on what you learn.

## Integration Between Skills

### Foundation Skills Enable All Others
- **design-foundation** provides tokens used by all other skills
- **design-engineer-mindset** ensures fidelity across all implementations

### Visual Skills Work Together
- **layout-system** creates structure
- **typography-system** establishes hierarchy
- **color-system** adds visual interest
- **visual-hierarchy-refactoring** ties them together

### Interaction Skills Create Delight
- **interaction-physics** makes interactions feel natural
- **loading-states** maintain confidence during waits
- **error-handling-recovery** guide users to resolution
- **performance-optimization** make everything feel fast

### Quality Skills Ensure Excellence
- **accessibility-excellence** ensures everyone can use your product
- **frontend-orchestrator** ensures strategic coordination

## How to Use This Skill with Claude Code

### Automatic Skill Invocation

After assessing the user's situation and recommending a path, **ask the user if they want you to automatically invoke the recommended skills in sequence**. For example:

```
"Based on your assessment, I recommend Path B with these skills:
1. design-foundation
2. visual-hierarchy-refactoring
3. component-architecture
...

Would you like me to run these skills now? I'll invoke each one in sequence to analyze your codebase and provide specific recommendations."
```

If the user agrees, **invoke each recommended skill using the /skill-name command** (e.g., `/design-foundation`, `/interaction-physics`). Work through them in the recommended order, applying each skill's methodology to the user's specific codebase.

### Get a Personalized Roadmap

```
"I'm using the frontend-orchestrator skill. Can you help me:
- Assess my current design maturity
- Identify my biggest pain points
- Recommend a skill sequence
- Then run the recommended skills automatically"
```

### Diagnose Design Issues

```
"My users are complaining about [issue]. Using the orchestrator:
- What's the root cause?
- Which skills would help?
- What should I prioritize?"
```

### Plan a Design System

```
"Can you help me plan a design system using the orchestrator?
- Assess my current state
- Recommend a path
- Create a step-by-step guide
- Estimate effort for each skill"
```

## Key Principles

**1. Start Where You Are**
Don't try to implement all skills at once. Start with the highest-impact skill for your situation.

**2. Build Momentum**
Early wins create confidence and buy-in for continued improvement.

**3. Iterate, Don't Perfectionism**
Each skill can be refined later. Get the basics right first.

**4. Measure Progress**
Track improvements in user satisfaction, support tickets, and retention.

**5. Celebrate Refinement**
The journey from MVP to transcendent design is a marathon, not a sprint.

## Checklist: Are You Ready to Begin?

- [ ] I've assessed my current design maturity level
- [ ] I've identified my biggest pain point
- [ ] I've chosen my implementation path
- [ ] I understand the sequence of skills
- [ ] I know which skill to start with
- [ ] I have a team or resources to implement
- [ ] I'm ready to commit to the journey

The orchestrator's role is to guide you from where you are to where you want to be. Start with the next skill in your path.
