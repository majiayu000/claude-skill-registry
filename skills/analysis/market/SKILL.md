---
name: market
description: Internationalization and accessibility audit - scan for hardcoded text, check i18n coverage, run WCAG 2.1 accessibility audit. Use when user says "go to market", "i18n check", "accessibility audit", "translation check", or wants to prepare app for international users.
allowed-tools: Read, Edit, Glob, Grep, Task
---

# Market Skill

Prepare the application for international markets with i18n and accessibility checks.

## When to Use
- Preparing for international launch
- Adding new language support
- Accessibility compliance check
- Before major releases

## Workflow

### Step 1: i18n Scan
1. Search for hardcoded text in components:
   - JSX text content
   - Placeholder attributes
   - Title attributes
   - Alt text (check if translatable)

2. Check for i18n usage patterns:
   - `t()` or `useTranslation` hooks
   - Translation file coverage
   - Missing translation keys

3. Report hardcoded strings that need i18n

### Step 2: Launch i18n Translator Agent
Spawn `i18n-locale-translator` agent to:
- Extract hardcoded text
- Create translation keys
- Generate locale files (en, jp, etc.)
- Update components with translation hooks

### Step 3: Accessibility Audit
Launch `accessibility-auditor` agent for WCAG 2.1 Level AA:
- Alt text on images
- Color contrast ratios
- Keyboard navigation
- ARIA labels and roles
- Form accessibility
- Focus management

### Step 4: Update Audit Documents
Update `_AUDIT/ACCESSIBILITY.md` with findings.

## Output Format
```
## Market Readiness Check

### i18n Status
- Hardcoded strings found: X
- Translation coverage: X%
- Missing translations: [list]

### Accessibility (WCAG 2.1 AA)
Score: X/10
- Critical issues: X
- High priority: X
- Medium priority: X

### Recommendations
- [Action items]

Updated: _AUDIT/ACCESSIBILITY.md
```
