---
name: Wireframing
description: Creating low-fidelity visual representations of website or application structure and layout to plan information architecture, user flows, and interface design before implementation.
---

# Wireframing

> **Current Level:** Intermediate  
> **Domain:** UX/UI Design / Planning

---

## Overview

Wireframes are low-fidelity visual representations of a website or application's structure and layout. Effective wireframes help teams plan information architecture, user flows, and interface design before investing in detailed design and development.

---

## Core Concepts

### 1. Wireframing Concepts

### What are Wireframes

```markdown
# Wireframing Concepts

## Definition

Wireframes are basic visual guides used in interface design to suggest the structure of an interface and relationships between its elements.

## Purpose

### 1. Structure
- Define layout
- Organize content
- Establish hierarchy
- Plan navigation

### 2. Communication
- Share ideas
- Get feedback
- Align stakeholders
- Document decisions

### 3. Exploration
- Try different layouts
- Explore options
- Test assumptions
- Iterate quickly

## Benefits

### 1. Speed
- Quick to create
- Easy to modify
- Fast iterations
- Rapid prototyping

### 2. Focus
- Structure over style
- Content over aesthetics
- Function over form
- User needs over designer preferences

### 3. Collaboration
- Easy to understand
- Non-designers can contribute
- Facilitates feedback
- Builds consensus

### 4. Cost-Effective
- Low investment
- Early feedback
- Reduces rework
- Saves time and money
```

---

## 2. Lo-Fi vs Hi-Fi Wireframes

### Fidelity Levels

```markdown
# Lo-Fi vs Hi-Fi Wireframes

## Low-Fidelity (Lo-Fi)

### Characteristics
- Basic shapes
- Simple lines
- Minimal detail
- Black and white
- Hand-drawn or simple digital

### When to Use
- Early exploration
- Brainstorming
- Quick iterations
- Stakeholder discussions
- User testing concepts

### Benefits
- Fast to create
- Easy to modify
- Focus on structure
- Low investment
- Encourages feedback

### Tools
- Pen and paper
- Whiteboard
- Balsamiq
- Sketch
- Simple drawing apps

## High-Fidelity (Hi-Fi)

### Characteristics
- Detailed elements
- Realistic proportions
- Color and typography
- Interactive elements
- Near-final appearance

### When to Use
- Finalizing design
- Developer handoff
- Stakeholder presentations
- User testing
- Documentation

### Benefits
- Clear communication
- Accurate representation
- Better understanding
- Ready for implementation
- Professional appearance

### Tools
- Figma
- Sketch
- Adobe XD
- InVision
- Principle
```

---

## 3. Wireframing Process

### Step-by-Step Process

```markdown
# Wireframing Process

## Step 1: Define Goals

### Objectives
- What are we building?
- Who is it for?
- What problem does it solve?
- What are the success criteria?

### Questions to Answer
- What's the primary user goal?
- What features are essential?
- What content is needed?
- What constraints exist?

## Step 2: Research

### Gather Information
- User research findings
- Competitive analysis
- Business requirements
- Technical constraints
- Brand guidelines

### Create Artifacts
- User personas
- User journeys
- Content inventory
- Feature list
- Requirements document

## Step 3: Sketch

### Quick Sketches
- Start with paper
- Explore multiple ideas
- Don't worry about details
- Focus on concepts
- Iterate rapidly

### Sketching Tips
- Use simple shapes
- Label elements clearly
- Focus on layout
- Show key interactions
- Annotate decisions

## Step 4: Create Lo-Fi Wireframes

### Digital Wireframes
- Convert sketches to digital
- Create multiple screens
- Show user flows
- Add basic annotations
- Get feedback

### Lo-Fi Best Practices
- Keep it simple
- Use consistent elements
- Show hierarchy
- Include key content
- Note interactions

## Step 5: Refine and Iterate

### Feedback Loop
- Share with stakeholders
- Gather feedback
- Make revisions
- Test with users
- Iterate based on feedback

### Refinement Focus
- Improve layout
- Adjust hierarchy
- Fix issues
- Add detail
- Polish interactions

## Step 6: Create Hi-Fi Wireframes

### Final Wireframes
- Add visual design
- Include real content
- Show interactions
- Create prototypes
- Prepare for handoff

### Hi-Fi Best Practices
- Follow design system
- Use real content
- Show all states
- Include annotations
- Test thoroughly
```

---

## 4. Information Architecture

### Organizing Content

```markdown
# Information Architecture

## 1. Content Inventory

### Purpose
- Understand what content exists
- Identify gaps
- Plan organization
- Prioritize content

### Process
1. Audit existing content
2. Categorize content
3. Identify relationships
4. Note content types
5. Document findings

### Template
| Content | Type | Priority | Status |
|---------|------|----------|--------|
| Home page | Page | High | Existing |
| About page | Page | Medium | New |
| Blog posts | Content | Medium | Existing |

## 2. Content Hierarchy

### Purpose
- Establish importance
- Guide user attention
- Create visual hierarchy
- Support scanning

### Techniques
- Size: Larger = more important
- Position: Top/left = more important
- Color: Bright/contrasting = more important
- Spacing: More space = more important
- Weight: Bold = more important

### Example
```
H1 - Main title (largest, boldest)
  H2 - Section title (smaller, lighter)
    H3 - Subsection title (smaller, lighter)
      Body text (smallest, lightest)
```

## 3. Navigation Structure

### Purpose
- Help users find content
- Support user goals
- Provide clear paths
- Enable exploration

### Types
- **Flat**: Single level
- **Hierarchical**: Multiple levels
- **Mixed**: Combination
- **Hub and Spoke**: Central hub with spokes

### Best Practices
- Keep it simple
- Use clear labels
- Show current location
- Provide breadcrumbs
- Include search
```

---

## 5. User Flows

### Flow Diagrams

```markdown
# User Flows

## 1. Flow Diagrams

### Purpose
- Map user journeys
- Identify decision points
- Show alternative paths
- Document interactions

### Elements
- **Start/End**: Begin and end points
- **Process**: Actions or steps
- **Decision**: Branching points
- **Connector**: Links between elements

### Example Flow
```
Start → Login → Dashboard → [Decision]
                    ↓ Yes      ↓ No
                View Profile    Create Profile
                    ↓              ↓
                End ← ← ← ← ← ← ←
```

## 2. Happy Path

### Purpose
- Show ideal user journey
- Focus on success scenario
- Identify key steps
- Optimize experience

### Example
```
User → Sign Up → Verify Email → Complete Profile → Welcome → Dashboard
```

## 3. Alternative Paths

### Purpose
- Show error scenarios
- Handle edge cases
- Provide fallbacks
- Ensure robustness

### Example
```
User → Sign Up → [Email Valid?] → Yes → Verify Email → Complete Profile
                    ↓ No
                    Show Error → Retry
```
```

---

## 6. Interactive Prototypes

### Creating Prototypes

```markdown
# Interactive Prototypes

## 1. Clickable Wireframes

### Purpose
- Test user flows
- Validate concepts
- Get feedback
- Communicate ideas

### Tools
- Figma
- Sketch
- Adobe XD
- InVision
- Principle

### Best Practices
- Link screens together
- Show key interactions
- Test on devices
- Get user feedback
- Iterate based on feedback

## 2. Annotated Wireframes

### Purpose
- Communicate behavior
- Document decisions
- Guide developers
- Provide context

### Annotations to Include
- Interaction behavior
- State changes
- Error conditions
- Loading states
- Responsive behavior

### Example
```
[Button: Primary]
- Clicks to next screen
- Shows loading state
- Disabled when form invalid
- Hover: Darker blue
- Active: Darker blue + scale
```

## 3. Interactive Components

### Purpose
- Test specific interactions
- Validate behavior
- Get detailed feedback
- Refine experience

### Components to Prototype
- Forms
- Navigation
- Modals
- Carousels
- Dropdowns
```

---

## 7. Tools

### Wireframing Tools

```markdown
# Wireframing Tools

## 1. Balsamiq

### Features
- Drag and drop
- Templates
- Collaboration
- Export options
- Simple interface

### Best For
- Lo-fi wireframes
- Quick iterations
- Beginners
- Teams

### Cost
- Freemium

## 2. Figma

### Features
- Vector editing
- Prototyping
- Collaboration
- Plugins
- Free tier

### Best For
- All fidelity levels
- Teams
- Design systems
- Handoff

### Cost
- Freemium

## 3. Sketch

### Features
- Vector editing
- Prototyping
- Libraries
- Collaboration
- Mac only

### Best For
- Mac users
- Designers
- Prototyping
- Handoff

### Cost
- Paid

## 4. Adobe XD

### Features
- Vector editing
- Prototyping
- Voice prototyping
- Auto-animate
- Adobe ecosystem

### Best For
- Adobe users
- Prototyping
- Animation
- Teams

### Cost
- Freemium

## 5. InVision

### Features
- Prototyping
- Collaboration
- User testing
- Design handoff
- Freehand

### Best For
- Prototyping
- User testing
- Teams
- Handoff

### Cost
- Freemium

## 6. Principle

### Features
- Advanced prototyping
- Micro-interactions
- Real-time collaboration
- Version history
- Mac/iOS only

### Best For
- High-fidelity prototypes
- Advanced interactions
- Mac users
- Designers

### Cost
- Paid

## 7. Whimsical

### Features
- Wireframing
- Flowcharts
- Mind maps
- Collaboration
- Simple interface

### Best For
- Wireframing
- Flowcharts
- Teams
- Quick sketches

### Cost
- Freemium
```

---

## 8. Annotations

### Wireframe Annotations

```markdown
# Wireframe Annotations

## What to Annotate

### 1. Content
- What content goes here?
- What's the purpose?
- Is it dynamic or static?
- What's the source?

### 2. Behavior
- What happens on click?
- What's the hover state?
- What's the active state?
- What happens on error?

### 3. States
- Loading state
- Empty state
- Error state
- Success state
- Disabled state

### 4. Responsive
- How does it adapt?
- What's mobile behavior?
- What's tablet behavior?
- What's desktop behavior?

### 5. Accessibility
- What's the ARIA role?
- What's the keyboard behavior?
- What's the screen reader behavior?
- What's the focus order?

## Annotation Format

### Example
```
[Component: Navigation Bar]

Purpose: Main site navigation

Content:
- Logo (links to home)
- Navigation links (Home, About, Services, Contact)
- Search icon (opens search)
- User menu (opens dropdown)

Behavior:
- Hover: Links highlight with underline
- Active: Current link has blue color
- Mobile: Collapses to hamburger menu
- Click: Navigates to page

States:
- Loading: N/A
- Empty: N/A
- Error: N/A

Responsive:
- Mobile: Hamburger menu
- Tablet: Full menu
- Desktop: Full menu

Accessibility:
- Role: navigation
- Label: Main navigation
- Keyboard: Tab through links
- Screen reader: Announces navigation
```
```

---

## 9. Responsive Wireframes

### Multi-Device Wireframes

```markdown
# Responsive Wireframes

## 1. Breakpoints

### Common Breakpoints
- **Mobile**: 320px - 480px
- **Small Tablet**: 481px - 768px
- **Tablet**: 769px - 1024px
- **Desktop**: 1025px - 1440px
- **Large Desktop**: 1441px+

## 2. Mobile-First Approach

### Process
1. Design for mobile first
2. Add breakpoints for larger screens
3. Enhance experience progressively
4. Test on all breakpoints

### Benefits
- Focus on essential content
- Better performance
- Progressive enhancement
- Easier to maintain

## 3. Responsive Patterns

### Column Drop
- Content drops to new columns as screen size increases

### Layout Shifter
- Layout changes completely at breakpoints

### Off Canvas
- Navigation slides in from off-screen

### Fluid Grid
- Grid uses flexible units

### Cards to List
- Cards become list items on mobile

## 4. Wireframe Templates

### Mobile Wireframe
- Single column layout
- Stacked content
- Touch-friendly targets
- Simplified navigation

### Tablet Wireframe
- Two column layout
- Side navigation
- More content visible
- Enhanced interactions

### Desktop Wireframe
- Multi-column layout
- Full navigation
- All content visible
- Rich interactions
```

---

## 10. User Testing with Prototypes

### Testing Wireframes

```markdown
# User Testing with Prototypes

## 1. Testing Methods

### Guerrilla Testing
- Quick, informal testing
- Test with available people
- Get immediate feedback
- Low cost
- Fast insights

### Remote Testing
- Test users remotely
- Use screen sharing
- Record sessions
- Reach diverse users
- Flexible scheduling

### Lab Testing
- Controlled environment
- Professional setup
- Detailed observations
- High-quality data
- More expensive

## 2. Testing Tasks

### Task Design
- Realistic tasks
- Clear instructions
- Measurable outcomes
- Time limits
- Success criteria

### Example Tasks
- "Find information about X"
- "Complete the sign-up process"
- "Purchase item Y"
- "Update your profile"
- "Contact customer support"

## 3. What to Observe

### Behaviors
- Where do they click?
- What do they read?
- What do they skip?
- Where do they get stuck?
- What confuses them?

### Feedback
- Ask for thoughts
- Probe on issues
- Note suggestions
- Record quotes
- Document emotions

## 4. Analysis

### Identify Patterns
- Common issues
- Success points
- Frustrations
- Opportunities
- Recommendations

### Prioritize Findings
- Impact vs effort
- Frequency of issue
- Severity of problem
- Number of users affected
- Business impact
```

---

## 11. Handoff to Developers

### Developer Handoff

```markdown
# Developer Handoff

## 1. Deliverables

### Wireframes
- Final wireframes
- All screens
- All states
- Responsive versions
- Annotated

### Specifications
- Component specs
- Interaction specs
- Responsive behavior
- Accessibility requirements
- Technical constraints

### Assets
- Images and icons
- Design tokens
- Style guide
- Component library
- Prototype links

## 2. Documentation

### Design Specifications
- Layout details
- Spacing and sizing
- Colors and typography
- Icons and images
- Animations and transitions

### Interaction Specifications
- Hover states
- Active states
- Focus states
- Error states
- Loading states

### Responsive Specifications
- Breakpoints
- Layout changes
- Component behavior
- Navigation changes
- Content priority

## 3. Communication

### Handoff Meeting
- Walk through designs
- Explain decisions
- Answer questions
- Discuss constraints
- Agree on approach

### Follow-up
- Available for questions
- Review implementation
- Provide feedback
- Make adjustments
- Finalize specs
```

---

## 12. Best Practices

### Wireframing Best Practices

```markdown
# Best Practices

## 1. Start Lo-Fi
- Sketch first
- Keep it simple
- Focus on structure
- Iterate quickly
- Get feedback early

## 2. Think Mobile-First
- Design for mobile
- Enhance for larger screens
- Focus on essentials
- Progressive enhancement

## 3. Use Grids
- Maintain consistency
- Align elements
- Create visual rhythm
- Use spacing systems
- Follow design system

## 4. Show Hierarchy
- Use size to show importance
- Use position strategically
- Use color sparingly
- Use weight effectively
- Create visual flow

## 5. Annotate Clearly
- Explain behavior
- Document decisions
- Provide context
- Note constraints
- Guide developers

## 6. Test Early
- Test with users
- Get feedback
- Iterate based on feedback
- Don't wait for perfection
- Fail fast, learn faster

## 7. Collaborate
- Share with team
- Get stakeholder input
- Incorporate feedback
- Build consensus
- Communicate clearly

## 8. Keep It Simple
- Focus on essentials
- Avoid complexity
- Don't over-design
- Solve real problems
- Meet user needs

## 9. Be Flexible
- Be open to changes
- Adapt to feedback
- Iterate based on learning
- Don't get attached
- Stay user-focused

## 10. Document Decisions
- Why decisions were made
- What alternatives were considered
- What constraints exist
- What assumptions were made
- What's the rationale
```

---

## Quick Reference

### Quick Tips

```markdown
# Quick Tips

## Do's
- ✓ Start with sketches
- ✓ Keep it simple
- ✓ Focus on structure
- ✓ Show hierarchy
- ✓ Annotate clearly
- ✓ Test early
- ✓ Iterate often
- ✓ Collaborate with team
- ✓ Get user feedback
- ✓ Document decisions

## Don'ts
- ✗ Start with high-fidelity
- ✗ Overcomplicate
- ✗ Focus on aesthetics
- ✗ Skip annotations
- ✗ Work in isolation
- ✗ Wait until perfect
- ✗ Ignore feedback
- ✗ Make assumptions
- ✗ Forget to test
- ✗ Skip documentation
```

### Wireframe Elements Quick Reference

```markdown
# Wireframe Elements

## Common Elements
- **Header**: Logo, navigation, user menu
- **Hero**: Main content, CTA
- **Cards**: Content containers
- **Forms**: Input fields, buttons
- **Navigation**: Links, menus
- **Footer**: Links, copyright, social

## Annotations
- **Content**: What goes here
- **Behavior**: What happens on interaction
- **States**: Loading, error, success
- **Responsive**: How it adapts
- **Accessibility**: ARIA, keyboard, screen reader

## Responsive Breakpoints
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+
```

---

## Quick Start

### Basic Wireframe Structure

```html
<!-- Low-fidelity wireframe structure -->
<div class="wireframe">
  <!-- Header -->
  <header>
    [Logo] [Navigation] [User Menu]
  </header>
  
  <!-- Main Content -->
  <main>
    <section class="hero">
      [Hero Image/Content]
      [CTA Button]
    </section>
    
    <section class="features">
      [Feature Card 1]
      [Feature Card 2]
      [Feature Card 3]
    </section>
  </main>
  
  <!-- Footer -->
  <footer>
    [Links] [Copyright]
  </footer>
</div>
```

### Wireframe Tools

```markdown
# Popular Wireframing Tools

## Free
- Figma (free tier)
- Draw.io
- Pencil Project

## Paid
- Sketch
- Adobe XD
- Balsamiq
```

---

## Production Checklist

- [ ] **User Flow**: Map user flows before wireframing
- [ ] **Information Architecture**: Plan content structure
- [ ] **Low-Fidelity First**: Start with low-fidelity wireframes
- [ ] **Annotations**: Add notes explaining behavior and states
- [ ] **Responsive**: Wireframe for mobile, tablet, desktop
- [ ] **User Testing**: Test wireframes with users
- [ ] **Iteration**: Iterate based on feedback
- [ ] **Handoff**: Prepare wireframes for design handoff
- [ ] **Documentation**: Document wireframe decisions
- [ ] **Version Control**: Version wireframes like code
- [ ] **Accessibility**: Consider accessibility in wireframes
- [ ] **Consistency**: Maintain consistent wireframe style

---

## Anti-patterns

### ❌ Don't: Too Much Detail Too Early

```html
<!-- ❌ Bad - High-fidelity wireframe too early -->
<div style="background: #f0f0f0; padding: 20px; border-radius: 8px;">
  <h2 style="color: #333; font-size: 24px;">Feature Title</h2>
  <!-- Too detailed for wireframe stage -->
</div>
```

```html
<!-- ✅ Good - Low-fidelity wireframe -->
<div class="wireframe-box">
  [Feature Title]
  [Description text]
  [Button]
</div>
```

### ❌ Don't: No Annotations

```html
<!-- ❌ Bad - No explanation -->
<div>[Button]</div>
```

```html
<!-- ✅ Good - Annotated -->
<div>
  [Button]
  <!-- Annotation: Opens modal with form -->
</div>
```

### ❌ Don't: Ignore Mobile

```html
<!-- ❌ Bad - Desktop only -->
<div class="desktop-layout">
  [Content]
</div>
```

```html
<!-- ✅ Good - Responsive wireframes -->
<!-- Mobile -->
<div class="mobile-layout">
  [Stacked content]
</div>

<!-- Desktop -->
<div class="desktop-layout">
  [Side-by-side content]
</div>
```

---

## Integration Points

- **User Research** (`22-ux-ui-design/user-research/`) - Test wireframes with users
- **Design Systems** (`22-ux-ui-design/design-systems/`) - Wireframe with design tokens
- **Responsive Design** (`22-ux-ui-design/responsive-design/`) - Responsive wireframes

---

## Further Reading

- [Wireframing Guide](https://www.interaction-design.org/literature/topics/wireframing)
- [Figma Wireframing](https://www.figma.com/resource-library/wireframing/)
- [Balsamiq Wireframing](https://balsamiq.com/learn/wireframing/)
- **Mobile**: 320px - 480px
- **Small Tablet**: 481px - 768px
- **Tablet**: 769px - 1024px
- **Desktop**: 1025px - 1440px
- **Large Desktop**: 1441px+
```
