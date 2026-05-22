---
name: website-ux-audit
description: This skill should be used when the user asks to "audit this website", "UX review", "analyze user experience", "website modernization report", "evaluate website design", "improve website UX", or provides a URL for comprehensive UX/UI analysis. Produces actionable modernization reports structured for design and implementation handoff.
version: 1.2
title: "Website Ux Audit"
status: active
---

# Website UX Audit Skill

## Overview

Conduct systematic analysis of a website's user experience and interface design, producing structured reports that feed directly into design and implementation workflows.

The output consists of:
1. A **main report** with overall findings, cross-cutting issues, and prioritized recommendations
2. **Section-specific reports** for each major area of the site, with detailed analysis and implementation guidance

**Key principle:** All recommendations are categorized by implementation readiness to enable immediate action on what's possible without waiting for additional inputs.

---

## Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Homepage URL | User provides | Entry point for exploration |
| Screenshots | User provides OR captured via browser tools | Visual analysis of actual rendering |
| Site purpose/context | User provides (optional) | Understanding business goals |

---

## Recommendation Tiers

All recommendations MUST be categorized into one of three tiers:

### Tier 1: Implement Now
Recommendations that can be actioned immediately using:
- Existing site content (text, images, data)
- Publicly observable structure and functionality
- Standard UX patterns and best practices

**No additional information required from site owner.**

Examples:
- Reorganizing existing navigation items
- Simplifying category labels using existing terminology
- Creating wireframes based on current content
- Fixing broken images/links that are observable
- Adding search functionality to existing content
- Improving layout and visual hierarchy
- Mobile optimization of existing pages

### Tier 2: Requires Information
Recommendations that need input from the site owner before implementation:
- Business rules or logic not apparent from the site
- Access to backend systems or data
- Brand guidelines or design assets
- Content that doesn't exist on the current site
- Metrics, statistics, or claims to be displayed
- Pricing or product information
- Legal/compliance requirements

**Document specifically what information is needed.**

Examples:
- Adding audience metrics (need actual numbers)
- Testimonials (need permission and content)
- Integration with external systems (need access)
- New content sections (need subject matter)
- Pricing display (need current rates)

### Tier 3: Future Enhancements
Strategic improvements that require:
- Significant new functionality development
- Content creation beyond reorganization
- Third-party integrations
- Ongoing operational commitments
- Major architectural changes

**These inform the product roadmap but aren't immediate implementation candidates.**

Examples:
- User review/rating systems
- Personalization engines
- Advanced search with ML
- Community features
- New content programs

---

## Process

### Phase 1: Discovery & Data Gathering

#### 1.1 Explore Site Structure

Start by fetching the homepage:

```
web_fetch(url=homepage_url)
```

Then systematically explore:
- Main navigation sections
- Footer links
- Key landing pages
- Representative subpages (1-2 per section)

Document the site map as discovered.

#### 1.2 Capture Screenshots

Use browser automation tools to capture:
- Homepage (desktop and mobile)
- Mobile navigation (open state)
- Each major section landing page
- Key interactive elements (forms, search, filters)
- Any areas of specific user concern

#### 1.3 Run Performance Analysis

Execute PageSpeed Insights checks:
```
https://pagespeed.web.dev/analysis?url={homepage_url}
```

Record:
- Core Web Vitals scores
- Performance opportunities
- Diagnostic findings
- Mobile vs desktop differences

### Phase 2: Analysis

Analyze across these dimensions:

#### 2.1 Visual Design
- Typography (fonts, hierarchy, readability)
- Color palette (cohesion, contrast, accessibility)
- Layout (whitespace, density, grid usage)
- Imagery (quality, loading, relevance)
- Consistency across pages

#### 2.2 Information Architecture
- Navigation systems (primary, secondary, footer)
- Content hierarchy and organization
- Labeling clarity
- Search and findability
- Duplicate or conflicting paths

#### 2.3 Content Quality
- Messaging clarity and tone
- Value proposition communication
- Call-to-action effectiveness
- Content freshness and relevance
- Grammar, spelling, consistency

#### 2.4 Interaction Design
- Form design and usability
- Interactive element clarity
- Feedback mechanisms
- Error handling
- Loading states

#### 2.5 Mobile Experience
- Responsive design quality
- Touch target sizing
- Mobile navigation patterns
- Content prioritization
- Performance on mobile

#### 2.6 Accessibility
- Semantic HTML usage
- Keyboard navigation
- Screen reader compatibility
- Color contrast ratios
- Alternative text for images

#### 2.7 Performance
- Page load times
- Resource optimization
- Render-blocking resources
- Image optimization
- Code efficiency

### Phase 3: Report Generation

#### 3.1 Main Report Structure

Create comprehensive main report with:

**Executive Summary**
- Overall site assessment (2-3 paragraphs)
- Most critical issues (top 3-5)
- Quick wins available
- Estimated impact of improvements

**Cross-Cutting Issues**
Issues affecting multiple sections:
- Pattern-level problems
- Systemic usability issues
- Technical debt
- Brand inconsistencies

**Prioritized Recommendations**
Group by tier:
1. **Tier 1 (Implement Now)** - Action immediately
2. **Tier 2 (Requires Information)** - Note what's needed
3. **Tier 3 (Future Enhancements)** - Strategic roadmap

For each recommendation:
- **Issue:** What's wrong
- **Impact:** User/business consequence
- **Solution:** Specific fix
- **Tier:** Implementation category
- **Effort:** Rough estimate (S/M/L)

**Performance Summary**
- Core Web Vitals breakdown
- Top performance issues
- Quick optimization opportunities

**Next Steps**
Clear action items:
- Immediate implementations (Tier 1)
- Information to gather (Tier 2)
- Strategic planning items (Tier 3)

#### 3.2 Section-Specific Reports

For each major site section, create focused report:

**Section Overview**
- Purpose and goals
- Current state assessment
- User journey analysis

**Visual Design Assessment**
- Section-specific visual issues
- Consistency with site standards
- Recommendations

**Content & IA Assessment**
- Content effectiveness
- Navigation and structure
- Findability issues
- Recommendations

**Interaction Design Assessment**
- Key interactions review
- Usability issues
- Recommendations

**Implementation Guidance**
Tier 1 recommendations only:
- Specific changes to make
- Wireframes or mockups (if helpful)
- Content reorganization specifics
- Priority order

---

## Quality Standards

### Recommendations Must Be:
- **Specific**: Clear, actionable instructions
- **Justified**: Explain impact and reasoning
- **Tiered**: Correctly categorized for implementation
- **Prioritized**: Relative importance clear
- **Measurable**: Success criteria defined where possible

### Reports Must Include:
- Evidence from actual site (screenshots, URLs)
- Comparative examples (good vs current)
- Performance data (when relevant)
- Accessibility issues (WCAG violations)
- Mobile-specific concerns

### Avoid:
- Generic advice applicable to any site
- Recommendations without justification
- Mixing tiers (keep clear separation)
- Assumptions about unavailable information
- Subjective opinions without UX principles

---

## Output Format

### File Structure

Create organized deliverables:

```
ux-audit-{site-name}/
├── 00-main-report.md
├── 01-homepage.md
├── 02-section-name.md
├── 03-section-name.md
├── screenshots/
│   ├── homepage-desktop.png
│   ├── homepage-mobile.png
│   └── ...
└── performance/
    ├── pagespeed-mobile.png
    └── pagespeed-desktop.png
```

### Report Formatting

Use consistent markdown structure:
- H1 for report title
- H2 for major sections
- H3 for subsections
- Tables for structured data
- Code blocks for specific implementations
- Bullet lists for recommendations
- Numbered lists for step-by-step processes

---

## Browser Automation Integration

When browser tools are available, leverage them for:

### Screenshot Capture
```
computer(action="screenshot", tabId=tab_id)
```

### Mobile Viewport Testing
```
resize_window(width=375, height=667)  # iPhone SE
resize_window(width=414, height=896)  # iPhone 11 Pro Max
```

### Interactive Element Testing
```
navigate(url=page_url)
find(query="search button")
computer(action="left_click", coordinate=[x, y])
```

### Console Error Checking
```
read_console_messages(pattern="error|warning")
```

### Network Performance Analysis
```
read_network_requests()
```

---

## Additional Resources

### Reference Files

For detailed workflows and standards:
- **`references/CHECKLIST.md`** - Comprehensive audit checklist for thorough coverage

### Example Files

Working examples in `examples/`:
- **`EXAMPLES.md`** - Sample audit reports and recommendation formats

---

## Best Practices

### During Discovery
- Capture evidence systematically
- Document navigation paths taken
- Note observable user friction
- Screenshot liberally
- Record performance metrics

### During Analysis
- Apply recognized UX principles
- Reference WCAG standards
- Compare against modern patterns
- Prioritize user impact
- Consider implementation feasibility

### During Reporting
- Lead with high-impact items
- Provide clear visual examples
- Separate what's possible now vs later
- Make recommendations actionable
- Include success metrics

### Communication
- Write for multiple audiences (designers, developers, stakeholders)
- Balance technical detail with accessibility
- Use visual aids effectively
- Organize for easy navigation
- Enable quick reference

---

## Common Patterns

### Navigation Issues
- Over-complex menu structures
- Unclear labeling
- Inconsistent navigation across sections
- Missing breadcrumbs
- Poor mobile navigation

**Solution Pattern:** Simplify, clarify labels, add consistent navigation cues

### Content Issues
- Unclear value propositions
- Weak calls-to-action
- Outdated information
- Inconsistent tone
- Poor content hierarchy

**Solution Pattern:** Refine messaging, strengthen CTAs, reorganize hierarchy

### Visual Issues
- Inconsistent styling
- Poor typography hierarchy
- Low contrast
- Cluttered layouts
- Inconsistent spacing

**Solution Pattern:** Create consistent design system, improve visual hierarchy

### Mobile Issues
- Non-responsive elements
- Small touch targets
- Horizontal scrolling
- Poor mobile navigation
- Slow mobile performance

**Solution Pattern:** Implement responsive patterns, optimize mobile experience

### Performance Issues
- Large unoptimized images
- Render-blocking resources
- Excessive JavaScript
- Slow server response
- No caching strategy

**Solution Pattern:** Optimize assets, defer non-critical resources, implement caching

---

## Success Criteria

Effective audit delivers:
- ✅ Clear, prioritized action items
- ✅ Tier 1 recommendations ready for immediate implementation
- ✅ Evidence-based findings with screenshots
- ✅ Specific solutions, not just problems
- ✅ Section-specific implementation guidance
- ✅ Performance improvement opportunities
- ✅ Accessibility issue identification
- ✅ Mobile experience evaluation
- ✅ Strategic roadmap (Tier 2 & 3)
