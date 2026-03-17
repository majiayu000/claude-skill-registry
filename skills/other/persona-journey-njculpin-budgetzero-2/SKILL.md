---
name: persona-journey
description: Comprehensive persona journey testing and UX verification across all personas
---

# Game Loopers Product & UX Verification Skill

## Skill Name
**user-journey-verification**

## Purpose
Comprehensively test and verify all persona journeys across Game Loopers personas, leveraging the project-product-manager and ux-flow-designer agents to identify friction points, ensure consistency, and generate actionable improvement recommendations.

This skill produces a detailed `REPORT.md` in the root directory documenting findings, prioritized recommendations, and implementation roadmap.

---

## Scope

### Personas Covered (MVP Phase)
This skill tests user journeys for all current personas defined in `PERSONAS.md`:

1. **Game Designer** - Creates products by combining assets, manages royalties
2. **3D Modeler** - Publishes embeddable STL products, earns royalties
3. **Illustrator/Artist** - Licenses artwork via embeddable products
4. **Consumer/Buyer** - Purchases complete game packages

### Future Personas (Deferred)
Documented but not tested until Phase 3:
- Printer (3D printing service provider)
- Painter (miniature painting service provider)

---

## Verification Framework

### 1. User Journey Testing

For each persona, the skill will:

**A. Map Complete User Flows**
- Account creation and onboarding
- Primary goal achievement (create/publish/purchase)
- Secondary interactions (collaboration, discovery, community)
- Edge cases and error states

**B. Identify Friction Points**
Using the **ux-flow-designer** agent to analyze:
- Cognitive load at each step
- Decision fatigue and confusion points
- Missing feedback or unclear states
- Excessive clicks or form fields
- Mobile responsiveness issues

**C. Verify Business Rules**
Using the **project-product-manager** agent to ensure:
- Product status system (draft, private, public, archived)
- Embeddability rules (is_embeddable flag, royalty configuration)
- Publishing validation (products need files OR components)
- Revenue distribution (10% platform fee, owner share, royalties)
- RLS security policies

**D. Check Consistency**
Cross-persona consistency verification:
- UI patterns (BEM CSS, design tokens)
- Form validation messaging
- Error handling and recovery
- Success state feedback
- Navigation patterns

---

### 2. UX Best Practices Audit

The skill applies industry-standard UX principles:

**Progressive Disclosure**
- Are complex features revealed gradually?
- Do first-time users see appropriate guidance?
- Are power users able to access advanced features?

**Error Prevention & Recovery**
- Are destructive actions confirmed?
- Do forms validate in real-time?
- Are error messages actionable with recovery paths?
- Can users undo or go back?

**Feedback & Affordance**
- Do buttons clearly indicate their purpose?
- Is loading state visible for async operations?
- Are success/failure states communicated clearly?
- Does the UI respond immediately to interactions?

**Accessibility (WCAG 2.1 Level AA)**
- Keyboard navigation support
- Focus indicators visible and clear
- Screen reader compatibility (ARIA labels)
- Color contrast ratios
- Touch target sizes (mobile)

**Conversion Optimization**
- Is the primary CTA obvious on each page?
- Are form fields minimized to essentials?
- Is trust established (transparent pricing, clear policies)?
- Are abandonment points minimized?

---

### 3. Agent Orchestration

The skill coordinates multiple specialized agents:

#### Phase 1: Strategic Analysis (project-product-manager)
- Review current implementation against product goals
- Identify scope creep or missing requirements
- Validate business rule enforcement
- Check code quality (no unused vars/imports/any types)
- Assess technical debt and scalability

**Deliverable**: Strategic assessment document

#### Phase 2: Flow Design Review (ux-flow-designer)
- Analyze all critical user flows per persona
- Map entry points, decision points, exit states
- Identify friction and suggest improvements
- Recommend component patterns (aligned with BEM)
- Provide accessibility recommendations

**Deliverable**: Flow analysis with diagrams and recommendations

#### Phase 3: Synthesis & Reporting
Combine findings into prioritized report:
- **P0 Critical Issues** (blocking launch/sales)
- **P1 High Impact** (significant UX friction or inconsistency)
- **P2 Medium Impact** (nice-to-have improvements)
- **P3 Future Enhancements** (deferred to post-MVP)

---

## Execution Process

When invoked, this skill will:

### Step 1: Context Gathering
```
1. Read PERSONAS.md for all persona definitions
2. Read .claude/skills/CSS/DESIGN_SYSTEM.md for UI standards
3. Read CLAUDE.md for architecture rules
4. Read ROADMAP.md for current phase and priorities
```

### Step 2: Agent Invocation (Sequential)

**2A. Launch project-product-manager agent**
```
Task: Strategic Product Review
- Verify product status system implementation
- Check embeddability and royalty logic
- Review publishing validation rules
- Assess code quality (unused imports, any types)
- Validate consistency across components
- Identify technical debt or architectural issues
```

**2B. Launch ux-flow-designer agent (per persona)**

For each persona, launch separate flow analysis:

**Game Designer Journey:**
```
Flow 1: Create first product
  Entry: Dashboard → "Create Product" button
  Steps: Title/description → Upload files → Set price → Embed products → Configure royalties → Publish
  Exit: Product live in marketplace

Flow 2: Embed community product for royalty sharing
  Entry: Product editor → "Embed Products" tab
  Steps: Search embeddable products → Select product → Configure royalty → Save
  Exit: Product updated with component royalties

Flow 3: Monitor revenue breakdown
  Entry: Product detail page (owner view)
  Steps: View revenue preview → Understand splits → See contributor list
  Exit: Confident in revenue distribution
```

**3D Modeler Journey:**
```
Flow 1: Publish embeddable STL product
  Entry: Create → "Create Product" button
  Steps: Upload STL files → Mark as embeddable → Set direct sale price → Set royalty rate → Publish
  Exit: Product visible in marketplace + embeddable for others

Flow 2: Track royalty earnings from embedded products
  Entry: Dashboard → "Royalty Earnings"
  Steps: View products embedding their work → See earnings per parent product → Track total royalties
  Exit: Understand passive income stream
```

**Illustrator Journey:**
```
Flow 1: License artwork via embeddable product
  Entry: Create → "Create Product" button
  Steps: Upload art files (PNG/PDF) → Mark embeddable → Set royalty rate → Publish
  Exit: Art available for licensing

Flow 2: Get credited on parent products
  Entry: Notification: "Your art was embedded in [Product]"
  Steps: View parent product page → See attribution → View royalty amount
  Exit: Confident work is credited and compensated
```

**Consumer Journey:**
```
Flow 1: Discover and purchase complete game package
  Entry: Browse products page
  Steps: Search/filter → View product detail → See what's included → See price breakdown → Add to cart → Checkout → Download files
  Exit: Product files downloaded, creators paid

Flow 2: Understand who gets paid (transparency)
  Entry: Product detail page
  Steps: View "Revenue Breakdown" section → See owner share → See contributor royalties → See platform fee
  Exit: Trust established through transparency
```

### Step 3: Cross-Persona Analysis
```
- Compare flows for consistency
- Identify shared components needing standardization
- Verify design system adherence across personas
- Check for conflicting patterns or messaging
```

### Step 4: Generate REPORT.md
```
Output structure:
- Executive Summary
- Methodology
- Findings by Persona (each persona gets dedicated section)
- Cross-Cutting Issues (affects multiple personas)
- Prioritized Recommendations (P0, P1, P2, P3)
- Implementation Roadmap
- Success Metrics for Improvements
```

---

## Report Template

The generated `REPORT.md` will follow this structure:

```markdown
# Game Loopers User Journey Verification Report

**Generated:** [Date]
**Scope:** MVP Personas (Game Designer, 3D Modeler, Illustrator, Consumer)
**Phase:** Pre-Launch Verification

---

## Executive Summary

[High-level findings, critical issues count, overall UX health score]

---

## Methodology

- Agents used: project-product-manager, ux-flow-designer
- Personas tested: 4 current MVP personas
- Flows analyzed: [Number] user journeys
- Standards applied: WCAG 2.1 AA, BEM CSS, Game Loopers design system

---

## Findings by Persona

### 1. Game Designer

**Primary Journey: Create and Publish Product**

✅ **What Works:**
- [List strengths]

❌ **Friction Points:**
- [Specific issues with location references]

🔧 **Recommendations:**
- [Actionable improvements with priority]

**Secondary Journey: Embed Community Products**

[Same structure]

---

### 2. 3D Modeler

[Same structure as Game Designer]

---

### 3. Illustrator

[Same structure]

---

### 4. Consumer/Buyer

[Same structure]

---

## Cross-Cutting Issues

### Design System Consistency
[Issues affecting multiple personas]

### Component Reusability
[Opportunities to DRY up code]

### Accessibility Gaps
[WCAG violations or keyboard navigation issues]

### Mobile Responsiveness
[Breakpoint issues, touch target sizes]

---

## Prioritized Recommendations

### P0: Critical (Blocking Launch)
1. [Issue] - **Impact:** [Description] - **Location:** [File/Component]
   - **Fix:** [Specific solution]
   - **Effort:** [Hours/Days]

### P1: High Impact (Launch Blockers or Major UX Friction)
[Same format]

### P2: Medium Impact (Post-Launch Improvements)
[Same format]

### P3: Future Enhancements (Phase 2+)
[Same format]

---

## Implementation Roadmap

### Week 1 (Pre-Launch)
- [ ] Fix P0 critical issues
- [ ] Address P1 high-impact items

### Week 2-4 (Post-Launch)
- [ ] Implement P2 medium-impact improvements
- [ ] Monitor metrics for validation

### Month 2+ (Growth Phase)
- [ ] Consider P3 enhancements based on user feedback

---

## Success Metrics

### Pre-Launch Targets
- 0 P0 critical issues
- <3 P1 high-impact issues
- WCAG 2.1 AA compliance: 100%
- Mobile responsiveness: All breakpoints tested

### Post-Launch Metrics (to validate improvements)
- Product publish success rate: >90%
- Checkout completion rate: >75%
- Average time to first sale: <7 days
- User support tickets: <5% of users

---

## Appendix

### A. Agent Outputs
[Links to detailed agent reports]

### B. Flow Diagrams
[Text-based flow diagrams for each persona]

### C. Component Audit
[BEM compliance, design token usage, accessibility]

### D. Code Quality Report
[Unused imports/vars, any types, architectural issues]
```

---

## Invocation Examples

### Example 1: Full Pre-Launch Audit
```
User: "Run the user journey verification for all personas"

Skill executes:
1. Reads PERSONAS.md, DESIGN_SYSTEM.md, CLAUDE.md
2. Invokes project-product-manager for strategic review
3. Invokes ux-flow-designer for each persona flow
4. Synthesizes findings
5. Writes REPORT.md to root directory
6. Outputs: "✅ Verification complete. See /REPORT.md for detailed findings and recommendations."
```

### Example 2: Single Persona Deep Dive
```
User: "Verify the 3D Modeler journey in detail"

Skill executes:
1. Reads PERSONAS.md (3D Modeler section only)
2. Invokes ux-flow-designer for modeler-specific flows
3. Invokes project-product-manager for consistency check
4. Generates focused report section
5. Appends to REPORT.md or creates MODELER_REPORT.md
```

### Example 3: Specific Flow Verification
```
User: "Test the product publishing flow for Game Designers"

Skill executes:
1. Maps publishing flow from product editor to marketplace
2. Invokes ux-flow-designer for friction analysis
3. Invokes project-product-manager for validation rule check
4. Generates focused recommendations
5. Outputs inline report or appends to REPORT.md
```

---

## Quality Assurance Checklist

Before generating final report, verify:

- [ ] All 4 MVP personas have been analyzed
- [ ] Each persona has at least 2 primary flows tested
- [ ] Accessibility standards checked (WCAG 2.1 AA)
- [ ] Design system compliance verified (BEM, tokens)
- [ ] Business rules validated (status, embeddability, royalties)
- [ ] Code quality reviewed (no unused code, no any types)
- [ ] Cross-persona consistency checked
- [ ] Recommendations are actionable with clear next steps
- [ ] Priorities assigned (P0, P1, P2, P3)
- [ ] Implementation effort estimated
- [ ] Success metrics defined

---

## Success Criteria

This skill succeeds when:

✅ **Comprehensive Coverage**
- All MVP personas analyzed
- Primary and secondary flows mapped
- Edge cases and error states considered

✅ **Actionable Recommendations**
- Each issue has clear location (file:line)
- Specific fixes provided, not just observations
- Prioritization helps focus effort (P0 → P3)
- Effort estimates guide planning

✅ **Strategic Alignment**
- Recommendations align with ROADMAP.md priorities
- MVP scope respected (no scope creep)
- Phase 2/3 ideas captured but deferred

✅ **Quality Standards**
- WCAG 2.1 AA compliance verified
- BEM CSS methodology enforced
- Design token usage checked
- Code quality rules applied

✅ **Measurable Outcomes**
- Success metrics defined for improvements
- Baseline current-state documented
- Target post-improvement state specified

---

## Agent Communication Protocol

### To project-product-manager:
```
Context: We're conducting pre-launch user journey verification
Task: Strategic product review covering:
  1. Product status system (draft, private, public, archived) - verify implementation
  2. Embeddability rules (is_embeddable flag, royalty config) - check consistency
  3. Publishing validation (products need files OR components) - test edge cases
  4. Revenue distribution (10% platform fee, owner share, royalties) - validate calculations
  5. Code quality (unused imports, variables, any types) - enforce rules
  6. Cross-persona consistency (components, patterns, messaging)

Output: Strategic assessment with prioritized issues (P0-P3)
```

### To ux-flow-designer (per persona):
```
Context: Testing [PERSONA] user journey for Game Loopers MVP
Persona: [Full persona details from PERSONAS.md]
Primary Flow: [Flow description]
Task: Analyze this flow for:
  1. Friction points (confusion, extra clicks, unclear states)
  2. Progressive disclosure (is complexity revealed gradually?)
  3. Error prevention & recovery (validations, confirmations, undo)
  4. Feedback & affordance (loading states, success messages)
  5. Accessibility (keyboard nav, ARIA, focus management)
  6. Conversion optimization (clear CTAs, minimal fields, trust signals)

Output: Flow diagram + friction analysis + recommendations
```

---

## Maintenance & Updates

**When to Re-Run:**
- Pre-launch (final verification before beta)
- After major feature additions
- When new personas are added (Phase 2, 3)
- Quarterly UX health checks
- After user feedback indicates friction

**How to Update This Skill:**
- Add new personas to PERSONAS.md
- Update agent orchestration for new flows
- Refine report template based on stakeholder feedback
- Adjust priority definitions (P0-P3) as project matures

---

## Summary

This skill is the comprehensive UX and product verification system for Game Loopers. By orchestrating specialized agents and applying rigorous testing frameworks, it ensures that all user journeys are friction-free, consistent, accessible, and aligned with business goals.

The resulting REPORT.md becomes the source of truth for pre-launch polish and post-launch improvement prioritization, driving product excellence through data-driven, persona-centric analysis.
