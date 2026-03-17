---
name: ux-review
description: Multi-perspective UX review combining usability, accessibility, and interaction design analysis.
keywords:
  - ux
  - usability
  - user experience
  - design review
  - heuristics
triggers:
  - ux review
  - usability review
  - design critique
  - user experience analysis
  - heuristic evaluation
---

# UX Review Skill

Comprehensive user experience review that coordinates multiple UX perspectives for thorough analysis of components, flows, or features.

## When to Use This Skill

- Reviewing new components or features before release
- Evaluating existing flows for usability issues
- PR reviews that touch UI/UX
- Design system component reviews
- Onboarding flow optimization
- Form and checkout flow analysis

## Review Framework

### Phase 1: Initial Assessment

**Context Gathering**:
1. What is the user trying to accomplish?
2. What is the component's role in the larger flow?
3. Who are the target users?
4. What are the success criteria?

**Heuristic Scan** (Nielsen's 10):
- Visibility of system status
- Match between system and real world
- User control and freedom
- Consistency and standards
- Error prevention
- Recognition rather than recall
- Flexibility and efficiency of use
- Aesthetic and minimalist design
- Help users recognize and recover from errors
- Help and documentation

### Phase 2: Multi-Perspective Analysis

#### UX Designer Perspective

| Category | Key Questions |
|----------|---------------|
| User Flow | Is the path to completion clear and efficient? |
| Information Architecture | Is content organized logically? |
| Cognitive Load | Is the interface overwhelming? |
| Error Prevention | Are mistakes prevented before they happen? |
| Mental Models | Does it work like users expect? |

#### Accessibility Expert Perspective

| Category | Key Questions |
|----------|---------------|
| WCAG 2.1 AA | Does it meet basic compliance? |
| Keyboard Navigation | Can everything be done without a mouse? |
| Screen Reader | Is the experience equivalent? |
| Color Contrast | Are all text/UI elements visible? |
| Focus Management | Is focus handled correctly? |

#### Interaction Designer Perspective

| Category | Key Questions |
|----------|---------------|
| State Coverage | Are all states handled (loading, empty, error, success)? |
| Feedback | Does the user know their action worked? |
| Micro-interactions | Are small details polished? |
| Transitions | Are animations purposeful and smooth? |
| Progressive Disclosure | Is complexity revealed appropriately? |

### Phase 3: Synthesis & Recommendations

Categorize findings by priority:

1. **Critical Issues**: Must fix for usability/accessibility
2. **High Priority**: Significantly impacts user experience
3. **Enhancements**: Would improve delight and efficiency
4. **Future Considerations**: Long-term improvements

## Output Template

```markdown
## UX Review: [Component/Flow Name]

### Summary
[2-3 sentence executive summary of overall UX quality and key findings]

### Critical Issues
- [ ] Issue 1: [Description and impact]
- [ ] Issue 2: [Description and impact]

### Recommendations by Category

#### Usability
| Finding | Impact | Recommendation |
|---------|--------|----------------|
| [Issue] | [High/Medium/Low] | [Fix] |

#### Accessibility
| Finding | WCAG Criterion | Recommendation |
|---------|----------------|----------------|
| [Issue] | [2.x.x Level] | [Fix] |

#### Interaction Design
| Finding | Impact | Recommendation |
|---------|--------|----------------|
| [Issue] | [High/Medium/Low] | [Fix] |

### Implementation Priority
1. **Critical fixes** (do first): [List]
2. **High-priority improvements**: [List]
3. **Enhancement opportunities**: [List]

### Next Steps
1. Create issues/tasks for critical findings
2. Add accessibility requirements to acceptance criteria
3. Update component documentation with UX guidelines
4. Schedule follow-up review after fixes
```

## Focus Area Deep Dives

### Usability Focus (`--focus=ux`)
- User flow mapping and optimization
- Task completion efficiency
- Error recovery patterns
- Learnability assessment
- Memory load reduction

### Accessibility Focus (`--focus=a11y`)
- WCAG 2.1 AA compliance audit
- Keyboard navigation testing
- Screen reader compatibility
- Color contrast verification
- Focus management review

### Interaction Focus (`--focus=interaction`)
- State coverage audit
- Feedback timing analysis
- Micro-interaction opportunities
- Animation review
- Progressive disclosure evaluation

## Success Indicators

- All critical usability issues identified
- Accessibility compliance gaps documented
- Interaction design improvements suggested
- Clear prioritization of fixes
- Actionable recommendations provided
