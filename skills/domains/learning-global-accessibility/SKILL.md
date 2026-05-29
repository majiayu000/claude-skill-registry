---
name: learning-global-accessibility
description: Validate accessibility across international standards (WCAG, EN 301 549, Section 508), support diverse assistive technologies, address regional accessibility regulations, and design for global ability contexts. Use when ensuring worldwide accessibility. Activates on "global accessibility", "international WCAG", or "worldwide compliance".
---

# Learning Global Accessibility

Ensure educational content meets accessibility standards and supports assistive technologies across international contexts.

## When to Use

- Global learning platforms
- International accessibility compliance
- Multi-region course deployment
- Supporting diverse assistive technologies
- Meeting regional accessibility laws

## International Standards

### Core Standards

**WCAG (Web Content Accessibility Guidelines)**:
- Level A (minimum)
- Level AA (legally required in many regions)
- Level AAA (enhanced)
- Version: WCAG 2.1 (current), WCAG 2.2 (recent), WCAG 3.0 (future)

**EN 301 549 (European Standard)**:
- Based on WCAG 2.1
- Covers software, documents, hardware
- Required for EU public sector
- Referenced in Web Accessibility Directive

**Section 508 (United States)**:
- US federal accessibility standard
- Now harmonized with WCAG 2.0 AA
- Applies to federal agencies and contractors

### Regional Standards

**UK**: Equality Act 2010, Public Sector Bodies Regulations
**Canada**: AODA (Ontario), Accessible Canada Act
**Australia**: DDA (Disability Discrimination Act)
**Japan**: JIS X 8341
**India**: GIGW (Guidelines for Indian Government Websites)

## Regional Requirements

### European Union

**Web Accessibility Directive** (2016/2102):
- WCAG 2.1 AA required
- Public sector websites and apps
- Accessibility statement mandatory
- Monitoring and enforcement

**European Accessibility Act** (EAA):
- Products and services
- E-commerce, e-books, banking
- Implementation by 2025

### United States

**ADA (Americans with Disabilities Act)**:
- Applies to places of public accommodation
- Website accessibility increasingly required
- Title II (state/local government)
- Title III (private businesses)

**IDEA (Individuals with Disabilities Education Act)**:
- K-12 education
- Accessible educational materials
- Assistive technology requirements

### Other Regions

**Canada**:
- AODA (Accessibility for Ontarians with Disabilities Act)
- Accessible Canada Act (federal)

**Australia**:
- DDA standards
- Education standards

## Assistive Technology Support

### Screen Readers

**Major Screen Readers**:
- JAWS (Windows)
- NVDA (Windows, open source)
- VoiceOver (macOS, iOS)
- TalkBack (Android)
- ORCA (Linux)

**Requirements**:
- Semantic HTML
- ARIA labels and roles
- Logical heading structure
- Alt text for images
- Keyboard navigation

### Other Assistive Technologies

**Magnification**:
- ZoomText
- OS magnifiers
- Responsive text sizing

**Voice Control**:
- Dragon NaturallySpeaking
- OS voice control

**Switch Access**:
- Single-switch, multi-switch devices
- Keyboard-only navigation

## Global Considerations

### Language and Script

**RTL Languages**:
- Right-to-left navigation
- Screen reader support for Arabic, Hebrew
- Bidirectional text handling

**Complex Scripts**:
- Screen reader support varies
- Font and rendering requirements

### Cultural Context

**Disability Models**:
- Medical model vs. social model
- Cultural attitudes toward disability
- Access to assistive technology
- Economic factors

### Multimedia

**Captions and Subtitles**:
- SDH (Subtitles for Deaf and Hard of Hearing)
- Language translations
- Cultural caption differences

**Audio Descriptions**:
- Extended vs. standard descriptions
- Language and cultural context

## Testing Protocols

### Automated Testing

**Tools**:
- axe DevTools
- WAVE
- Lighthouse
- Pa11y

**Limitations**: Catches ~30-40% of issues

### Manual Testing

**Required Tests**:
- Keyboard navigation
- Screen reader testing (multiple readers)
- Color contrast
- Magnification/zoom
- Focus management

### User Testing

**With People with Disabilities**:
- Diverse disability types
- Varied assistive technologies
- Different experience levels
- Cultural contexts

## CLI Interface

```bash
# Global accessibility validation
/learning.global-accessibility --content "course/" --standards "WCAG-2.1-AA,EN-301-549,Section-508"

# Regional compliance check
/learning.global-accessibility --platform "lms/" --regions "EU,US,Canada,Australia"

# Assistive technology testing
/learning.global-accessibility --content "module/" --test-with "JAWS,NVDA,VoiceOver,TalkBack"

# Multi-language accessibility
/learning.global-accessibility --content "course/" --languages "en,ar,zh,es" --rtl-support
```

## Output

- Global accessibility compliance report
- Regional requirements checklist
- Assistive technology compatibility matrix
- Remediation recommendations
- Testing protocols
- Accessibility statement template

## Composition

**Input from**: `/curriculum.review-accessibility`, `/learning.multi-script-design`
**Works with**: `/learning.regional-compliance`, `/learning.multilingual-assessment`
**Output to**: Globally accessible learning materials

## Exit Codes

- **0**: Global accessibility validated
- **1**: Critical accessibility violations
- **2**: Regional standard not met
- **3**: Assistive technology incompatibility
