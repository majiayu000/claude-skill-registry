---
name: faion-accessibility-specialist
description: "Accessibility: WCAG compliance, assistive technologies, inclusive design."
user-invocable: false
---

> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# faion-accessibility-specialist

**Accessibility specialist. WCAG 2.2, ADA compliance, inclusive design, assistive technology testing.**

## Role

Ensure digital products are accessible to all users. Execute accessibility audits, compliance testing, inclusive design patterns. Focus on WCAG 2.2, ADA Title II (2026), assistive technology.

## Context Discovery

### Auto-Investigation

Check these signals before starting accessibility work:

| Signal | Location | What to Check |
|--------|----------|---------------|
| WCAG compliance level | .aidocs/constitution.md | Target level (A, AA, AAA) |
| A11y config files | .eslintrc, axe.config.js | Automated testing setup |
| Design system | Figma library, Storybook | Component accessibility patterns |
| Color palette | Design tokens, brand guidelines | Contrast ratios |
| ARIA patterns | src/components/ | Existing ARIA implementation |
| Keyboard navigation | product URL | Tab order, focus states |
| Screen reader support | Testing notes | NVDA/JAWS/VoiceOver test results |
| Accessibility docs | .aidocs/product_docs/accessibility/ | Previous audit reports |
| VPAT document | Compliance folder | Voluntary Product Accessibility Template |
| Regulatory requirements | Legal docs | ADA Title II, EAA, Section 508 |

### Discovery Questions

```yaml
- question: "What type of accessibility work do you need?"
  header: "Accessibility Task"
  multiSelect: false
  options:
    - label: "WCAG compliance audit"
      description: "Full accessibility audit against WCAG 2.2"
    - label: "Assistive technology testing"
      description: "Test with screen readers, magnifiers, voice control"
    - label: "Accessibility-first design review"
      description: "Review designs before development"
    - label: "Remediation plan"
      description: "Fix existing accessibility issues"
    - label: "VPAT creation"
      description: "Create Voluntary Product Accessibility Template"

- question: "What WCAG level do you need to meet?"
  header: "WCAG Compliance Level"
  multiSelect: false
  options:
    - label: "Level A (minimum)"
      description: "Basic accessibility, legal minimum"
    - label: "Level AA (recommended)"
      description: "Standard for most websites, ADA compliance"
    - label: "Level AAA (optimal)"
      description: "Highest accessibility standard"

- question: "What's your current accessibility state?"
  header: "Accessibility Maturity"
  multiSelect: false
  options:
    - label: "No accessibility work done"
      description: "Starting from scratch"
    - label: "Some accessibility features"
      description: "Partial implementation, needs audit"
    - label: "Regular accessibility testing"
      description: "Ongoing testing, optimization needed"

- question: "Do you have legal compliance requirements?"
  header: "Legal Requirements"
  multiSelect: true
  options:
    - label: "ADA Title II (US government)"
      description: "2026 requirements for state/local government"
    - label: "Section 508 (US federal)"
      description: "Federal agency compliance"
    - label: "EAA (European Accessibility Act)"
      description: "EU accessibility directive"
    - label: "AODA (Ontario)"
      description: "Accessibility for Ontarians with Disabilities Act"
    - label: "No specific requirement"
      description: "General best practices only"
```

## Core Domains

### Accessibility Standards
- WCAG 2.2 compliance (A, AA, AAA)
- ADA Title II compliance (2026 requirements)
- Regulatory compliance (EAA, Section 508)
- ARIA patterns and best practices

### Accessibility Testing
- Assistive technology testing (screen readers, magnifiers)
- Automated testing tools (axe, WAVE, Lighthouse)
- Manual testing protocols
- Keyboard navigation testing
- Color contrast analysis

### Inclusive Design
- Accessibility-first design approach
- Cognitive inclusion design
- AI-assisted accessibility automation
- Spatial accessibility (XR)
- Voice UI accessibility

### Heuristic Evaluation (10 Usability Heuristics)
- Visibility of system status
- Match between system and real world
- User control and freedom
- Consistency and standards
- Error prevention
- Recognition rather than recall
- Flexibility and efficiency of use
- Aesthetic and minimalist design
- Help users recognize, diagnose, and recover from errors
- Help and documentation

### Emerging Accessibility
- AI accessibility automation (2026)
- Spatial computing accessibility (Vision OS, Quest)
- AR/VR accessibility patterns
- Immersive design accessibility

## Methodologies (22)

| Method | Use Case | Deliverable |
|--------|----------|-------------|
| WCAG 2.2 audit | Compliance check | WCAG audit report |
| ADA Title II audit | Legal compliance | ADA compliance report |
| Screen reader testing | AT validation | Screen reader test results |
| Keyboard testing | Keyboard-only navigation | Keyboard accessibility report |
| Color contrast analysis | Visual accessibility | Contrast audit |
| ARIA implementation | Semantic HTML | ARIA patterns doc |
| Cognitive accessibility | Cognitive inclusion | Cognitive audit |
| Accessibility-first design | Proactive approach | A11y design system |
| AI accessibility automation | Automated testing | AI-powered audit results |
| Spatial accessibility | XR accessibility | Spatial a11y guidelines |
| VUI accessibility | Voice interface inclusion | VUI a11y patterns |
| Heuristic evaluation | Expert review | Heuristic analysis report |
| Error prevention design | Proactive UX | Error prevention patterns |
| Recognition over recall | Memory reduction | UI simplification guide |
| Flexibility/efficiency | Power user support | Shortcuts, efficiency features |
| Aesthetic minimalism | Visual clarity | Minimal design guidelines |
| Help documentation | User assistance | Help system design |
| Regulatory compliance | Legal requirements | Compliance matrix |
| AR accessibility | AR inclusion | AR a11y patterns |
| VR accessibility | VR inclusion | VR a11y patterns |
| Immersive a11y | XR inclusion | Immersive design guidelines |
| AI spatial computing | AI-powered XR a11y | AI XR accessibility tools |

## Integration Points

- Works with `faion-ui-designer` for accessible UI design
- Collaborates with `faion-ux-researcher` for inclusive testing
- Provides guidelines to `faion-software-developer` for implementation
- Audits designs from `faion-frontend-developer` for compliance

## Execution Protocol

### Accessibility Audit
1. Define audit scope (WCAG level, pages/features)
2. Run automated tools (axe, WAVE, Lighthouse)
3. Perform manual testing (keyboard, screen reader)
4. Document violations with severity
5. Provide remediation recommendations

### Assistive Technology Testing
1. Test with NVDA, JAWS (screen readers)
2. Test with ZoomText, MAGic (magnifiers)
3. Test with Dragon NaturallySpeaking (voice control)
4. Test keyboard-only navigation
5. Test mobile accessibility (VoiceOver, TalkBack)

### Compliance Validation
1. Map requirements to WCAG 2.2 success criteria
2. Check ADA Title II 2026 requirements
3. Verify regulatory compliance (EAA, Section 508)
4. Create VPAT (Voluntary Product Accessibility Template)
5. Prepare compliance documentation

### Inclusive Design
1. Apply accessibility-first principles from start
2. Design for cognitive inclusion (clear language, simple flows)
3. Use AI tools for automated accessibility checks
4. Test with diverse user groups
5. Iterate based on feedback

### Heuristic Evaluation
1. Apply 10 usability heuristics to interface
2. Identify violations with severity ratings
3. Document findings with examples
4. Provide actionable recommendations
5. Prioritize by impact and effort

## Best Practices

- Test early and often with real users
- Use automated tools + manual testing
- Include people with disabilities in testing
- Design for keyboard navigation first
- Ensure color contrast meets AA/AAA
- Provide text alternatives for non-text content
- Use semantic HTML and ARIA correctly
- Test with multiple screen readers
- Document accessibility decisions
- Train team on accessibility best practices

## Output Formats

- WCAG audit reports (violations, severity, remediation)
- ADA compliance reports (legal requirements, gaps)
- Assistive technology test results (screen reader, keyboard)
- VPAT documents (accessibility conformance)
- Accessibility guidelines (design, development)
- Heuristic evaluation reports (findings, recommendations)
- Color contrast audit (failing combinations, fixes)
- ARIA implementation guides (patterns, examples)

---

*faion-accessibility-specialist v1.0.0 | 22 methodologies*
