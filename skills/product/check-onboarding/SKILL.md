---
name: check-onboarding
description: |
  Audit onboarding: first-run, time to aha, friction points, empty states.
  Outputs structured findings. Use log-onboarding-issues to create issues.
  Invoke for: onboarding review, new user experience, activation audit.
---

# /check-onboarding

Audit user onboarding experience. Output findings as structured report.

## What This Does

1. Check first-run experience
2. Measure time to "aha moment"
3. Identify friction points
4. Check empty states
5. Check progressive disclosure
6. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-onboarding-issues` to create GitHub issues or `/fix-onboarding` to fix.

## Process

### 1. First-Run Experience Check

```bash
# Onboarding flow exists?
find . -path "*onboarding*" -name "*.tsx" 2>/dev/null | head -5
find . -path "*welcome*" -name "*.tsx" 2>/dev/null | head -5

# New user detection?
grep -rE "isNewUser|firstVisit|hasCompletedOnboarding|onboardingComplete" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5

# Tour/walkthrough?
grep -rE "tour|Tour|walkthrough|Walkthrough|shepherd|driver\.js|intro\.js" --include="*.tsx" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5
```

### 2. Authentication Flow Check

```bash
# Auth callback handling?
find . -path "*callback*" -o -path "*auth*" -name "*.tsx" 2>/dev/null | head -5

# Post-signup redirect?
grep -rE "signUp.*redirect|afterSignUp|signUpUrl" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5

# Profile completion?
grep -rE "completeProfile|setupProfile|profile.*setup" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5
```

### 3. Empty States Check

```bash
# Empty state components?
grep -rE "empty|Empty|no.*found|NoResults|EmptyState" --include="*.tsx" components/ 2>/dev/null | head -5

# Placeholder content for new users?
grep -rE "placeholder|getStarted|Get Started|Create.*first" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5

# Loading states?
grep -rE "loading|Loading|skeleton|Skeleton|shimmer" --include="*.tsx" components/ 2>/dev/null | head -5
```

### 4. Friction Point Detection

```bash
# Required fields on first interaction?
grep -rE "required|isRequired|\*.*required" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -10

# Form complexity?
form_fields=$(grep -rE "<input|<Input|<TextField" --include="*.tsx" . 2>/dev/null | grep -v node_modules | wc -l | tr -d ' ')
echo "Form fields count: $form_fields"

# Payment wall before value?
grep -rE "subscribe.*before|payment.*required|upgrade.*to" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5
```

### 5. Progressive Disclosure Check

```bash
# Tooltips for guidance?
grep -rE "tooltip|Tooltip|hint|Hint" --include="*.tsx" components/ 2>/dev/null | head -5

# Feature discovery?
grep -rE "new.*feature|beta|coming.*soon|tip|Tip" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5

# Contextual help?
grep -rE "help|Help|info|Info|learn.*more|LearnMore" --include="*.tsx" components/ 2>/dev/null | head -5
```

### 6. Aha Moment Path

Analyze the path to core value:
```bash
# Main action identification
grep -rE "create|Create|add|Add|import|Import|generate|Generate" --include="*.tsx" app/ 2>/dev/null | head -10

# Steps to first success?
# Check for multi-step forms, wizards, or complex setup
grep -rE "step|Step|wizard|Wizard|progress|Progress" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5
```

### 7. Retention Hooks

```bash
# Notification permissions?
grep -rE "Notification|push|Push|notification" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5

# Email capture?
grep -rE "email|newsletter|subscribe" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5

# Save progress?
grep -rE "draft|Draft|autosave|Autosave|save.*progress" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -5
```

## Output Format

```markdown
## Onboarding Audit

### P0: Critical (Users Immediately Lost)
- No onboarding flow - Users dropped into empty app
- Auth callback broken - Users stuck after signup
- Required payment before seeing product value

### P1: Essential (Activation Blockers)
- No empty states - Blank screens confuse new users
- No guidance on first action
- Complex form on first interaction (15+ fields)
- No loading states (user thinks app is broken)

### P2: Important (Friction Reducers)
- No progressive disclosure (all features visible immediately)
- No tooltips/hints for new users
- No tour/walkthrough option
- Post-signup redirect goes to generic dashboard

### P3: Retention Enhancers
- No notification permission request
- No email capture for non-logged-in users
- No "save progress" for long workflows
- No "welcome back" experience

## Onboarding Metrics (Estimated)
- Steps to first value: 5+ (target: 2-3)
- Required fields before value: 8 (target: 0-2)
- Time to "aha": Unknown (add analytics)

## Current Status
- First-run flow: Missing
- Empty states: Partial
- Progressive disclosure: None
- Friction level: High

## Summary
- P0: 1 | P1: 4 | P2: 4 | P3: 3
- Recommendation: Add empty states and reduce first-action friction
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No onboarding flow | P0 |
| Broken auth callback | P0 |
| Paywall before value | P0 |
| No empty states | P1 |
| No first-action guidance | P1 |
| Complex initial forms | P1 |
| No loading states | P1 |
| No progressive disclosure | P2 |
| No tooltips/hints | P2 |
| No tour option | P2 |
| Notification capture | P3 |
| Email capture | P3 |

## Related

- `/log-onboarding-issues` - Create GitHub issues from findings
- `/fix-onboarding` - Fix onboarding issues
- `/cro` - Conversion rate optimization
