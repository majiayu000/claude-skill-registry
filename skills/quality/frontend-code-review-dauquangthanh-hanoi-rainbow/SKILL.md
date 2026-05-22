---
name: frontend-code-review
description: Conducts comprehensive frontend code reviews including React/Vue/Angular component analysis, TypeScript/JavaScript quality assessment, CSS/styling review, performance optimization, accessibility compliance, security vulnerabilities, and best practices validation. Produces detailed review reports with specific issues, severity ratings, and actionable recommendations. Use when reviewing frontend code, analyzing React/Vue/Angular components, checking JavaScript/TypeScript quality, validating CSS/SCSS, assessing web performance, or when users mention "review frontend code", "check React components", "analyze JavaScript", "review TypeScript", "validate accessibility", or "frontend code quality".
---

# Frontend Code Review

Systematically review frontend code to identify issues, ensure quality, and provide actionable improvement recommendations across code quality, performance, accessibility, and security dimensions.

## Review Workflow

## 1. Initial Assessment

Gather context about the project and identify review scope:

**Project Context:**

- Framework and version (React, Vue, Angular, vanilla JS)
- Build tools and dependencies
- Target browsers/devices
- Accessibility requirements (WCAG level)
- Performance targets (Core Web Vitals)

**Review Scope:**

- New features vs. refactoring vs. bug fixes
- Component complexity level
- Critical user paths
- Security-sensitive areas

### 2. Code Quality Analysis

Evaluate component structure, code patterns, and maintainability:

**Key Areas:**

- Component architecture (single responsibility, composition patterns)
- JavaScript/TypeScript quality (type safety, naming, complexity)
- State management decisions (local vs. global, immutability)
- Error handling and edge cases
- Code duplication and DRY violations

> **Load references/code-quality-checklist.md** for detailed quality criteria, common issues, and fixes with code examples

### 3. Performance Review

Assess rendering efficiency, resource loading, and Core Web Vitals:

**Focus Areas:**

- Rendering optimization (React.memo, useMemo, useCallback, keys)
- Resource loading (images, fonts, scripts, lazy loading)
- Bundle size and code splitting
- Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- Memory leaks and cleanup

> **Load references/performance-checklist.md** for detailed optimization techniques and Web Vitals guidelines with code examples

### 4. Accessibility Assessment

Evaluate WCAG 2.1 compliance and inclusive design:

**Key Areas:**

- Semantic HTML (proper headings, landmarks, lists)
- ARIA implementation (labels, roles, live regions)
- Keyboard navigation and focus management
- Screen reader support (alt text, labels, announcements)
- Color contrast ratios

> **Load references/accessibility-checklist.md** for WCAG 2.1 AA/AAA compliance criteria with detailed examples

### 5. Security Review

Identify vulnerabilities and security best practices:

**Common Vulnerabilities:**

- XSS (input sanitization, safe HTML rendering)
- CSRF protection
- Authentication token handling
- Sensitive data exposure
- Dependency vulnerabilities

**Security Controls:**

- Content Security Policy (CSP)
- HTTPS enforcement
- Secure cookies
- Input validation and output encoding

> **Load references/security-checklist.md** for comprehensive frontend security guidelines and vulnerability prevention

### 6. CSS/Styling Review

Assess architecture, responsiveness, and maintainability:

**Key Areas:**

- CSS methodology (BEM, OOCSS, CSS-in-JS, Tailwind)
- Responsive design (mobile-first, breakpoints, flexible layouts)
- Design tokens and variables
- Specificity management
- Unused CSS detection

### 7. Testing Coverage

Evaluate test completeness and quality:

**Test Types:**

- Unit tests (component logic, utilities, edge cases)
- Integration tests (component interaction, API integration, state flows)
- E2E tests (critical user journeys, cross-browser compatibility)
- Accessibility automated tests

### 8. Generate Review Report

Create structured report with findings and recommendations:

**Report Structure:**

- Executive Summary (quality rating, critical issues, recommendation)
- Detailed Findings (by category with severity: Critical/Major/Minor)
- Action Items (prioritized with file/line references and specific fixes)

> **Load references/report-templates.md** for full review report formats and examples

## Review Process Guidelines

**Review Timing:**

- **Pre-Commit**: Automated linting and formatting
- **Pre-PR**: Self-review using this workflow
- **PR Review**: Peer review with comprehensive analysis
- **Pre-Deployment**: Final quality gate

**Severity Definitions:**

- **Critical**: Blocks deployment (security issues, breaking bugs, accessibility blockers)
- **Major**: Should fix before merge (performance issues, poor patterns, maintainability concerns)
- **Minor**: Nice to improve (style suggestions, micro-optimizations, documentation)

## Common Anti-Patterns

**React/Component Patterns:**

- Prop drilling through multiple levels
- God components doing too much
- Missing error boundaries
- Mutating state directly
- Inline functions causing unnecessary re-renders

**JavaScript/TypeScript:**

- Using `any` type in TypeScript
- Console.log in production code
- Deeply nested callbacks
- Global variables
- Unhandled promises

**CSS/Styling:**

- !important overuse
- Inline styles instead of classes
- Fixed pixels instead of relative units
- High specificity wars

**Performance:**

- Synchronous expensive operations in render
- Large unoptimized bundles (>500KB)
- Missing code splitting and lazy loading
- Unoptimized images

**Accessibility:**

- Non-semantic div/span buttons
- Missing alt attributes
- Color-only information
- Keyboard traps
- Missing focus management in modals

## Key Review Checkpoints

**Code Quality:**

- [ ] Components follow single responsibility
- [ ] Functions < 50 lines, complexity < 10
- [ ] TypeScript strict mode enabled
- [ ] Meaningful naming conventions
- [ ] Error handling present

**Performance:**

- [ ] Appropriate use of React.memo/useMemo/useCallback
- [ ] Images optimized (WebP/AVIF)
- [ ] Code splitting implemented
- [ ] Core Web Vitals within targets

**Accessibility:**

- [ ] Semantic HTML used
- [ ] All images have alt text
- [ ] Keyboard navigable
- [ ] Color contrast compliant (≥4.5:1)

**Security:**

- [ ] User input sanitized
- [ ] XSS prevention in place
- [ ] No sensitive data in localStorage
- [ ] Dependencies up to date

## Reference Files

Load these files when detailed guidance is needed:

- **references/code-quality-checklist.md**: Component patterns, code smells, fixes with examples (693 lines)
- **references/performance-checklist.md**: Web Vitals optimization, rendering performance (891 lines)
- **references/accessibility-checklist.md**: WCAG 2.1 compliance with detailed examples (1045 lines)
- **references/security-checklist.md**: XSS, CSRF, authentication, CSP guidelines (969 lines)
- **references/report-templates.md**: Review report formats and examples (1203 lines)
