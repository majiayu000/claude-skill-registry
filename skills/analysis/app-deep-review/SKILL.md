---
name: app-deep-review
description: Deep analysis of an AinexSuite app with 6 parallel review agents. Use when you want comprehensive modernization recommendations for backend, frontend, UX, UI, AI enhancement, and security/performance. Includes severity ratings, code examples, and auto-fix suggestions.
argument-hint: "[app-name] [--auto-fix]"
model: claude-opus-4-5-20251101
allowed-tools:
  - Read
  - Grep
  - Glob
  - Task
  - Edit
  - Write
  - Bash(ls:*)
  - Bash(wc:*)
  - Bash(find:*)
  - Bash(jq:*)
  - Bash(cat:*)
---

# App Deep Review Skill

## Overview

This skill performs comprehensive deep analysis of any app in the AinexSuite monorepo. It uses extended thinking (ultrathink) and spawns 6 parallel sub-agents to review different aspects of the codebase, providing severity-rated findings with before/after code examples.

## Arguments

- `app-name` (required): The name of the app to analyze (e.g., `notes`, `main`, `journal`)
- `--auto-fix` (optional): Enable automatic fixing of safe, low-risk issues

## Available Apps

| App      | Port | Purpose               |
| -------- | ---- | --------------------- |
| main     | 3000 | Central dashboard     |
| notes    | 3001 | Colorful notes        |
| journal  | 3002 | Mood/reflections      |
| todo     | 3003 | Task management       |
| health   | 3004 | Body metrics          |
| album    | 3005 | Memory curation       |
| habits   | 3006 | Personal development  |
| mosaic   | 3007 | Dashboard display     |
| fit      | 3008 | Workout tracking      |
| projects | 3009 | Project management    |
| flow     | 3010 | Visual automation     |
| subs     | 3011 | Subscription tracking |
| docs     | 3012 | Rich documents        |
| tables   | 3013 | Spreadsheets          |
| calendar | 3014 | Scheduling            |
| admin    | 3020 | Admin dashboard       |

---

## Execution Instructions

### Step 1: Parse Arguments

Extract the app name and check for `--auto-fix` flag from the user's input.

```
User input: "/app-deep-review notes --auto-fix"
→ app_name = "notes"
→ auto_fix = true

User input: "/app-deep-review main"
→ app_name = "main"
→ auto_fix = false
```

**Validation:**

1. Verify the app exists in `apps/{app_name}/`
2. If app doesn't exist, list available apps and ask user to choose

---

### Step 2: Collect Pre-Analysis Metrics

Before spawning review agents, gather concrete data about the app. Run these commands to establish a metrics baseline:

```bash
# App structure metrics
find apps/{app}/src -name "*.tsx" 2>/dev/null | wc -l           # Total TSX files
find apps/{app}/src -name "*.ts" 2>/dev/null | wc -l            # Total TS files
find apps/{app}/src/components -name "*.tsx" 2>/dev/null | wc -l # Component count
find apps/{app}/src/hooks -name "*.ts" 2>/dev/null | wc -l       # Custom hooks count
find apps/{app}/src/app/api -type d 2>/dev/null | wc -l          # API route count

# Code volume (lines of code)
find apps/{app}/src -type f \( -name "*.ts" -o -name "*.tsx" \) -exec wc -l {} + 2>/dev/null | tail -1

# Dependencies count
jq '.dependencies | length' apps/{app}/package.json 2>/dev/null
jq '.devDependencies | length' apps/{app}/package.json 2>/dev/null

# Package usage - imports from shared packages
grep -r "@ainexsuite/ui" apps/{app}/src --include="*.tsx" --include="*.ts" 2>/dev/null | wc -l
grep -r "@ainexsuite/firebase" apps/{app}/src --include="*.tsx" --include="*.ts" 2>/dev/null | wc -l
grep -r "@ainexsuite/auth" apps/{app}/src --include="*.tsx" --include="*.ts" 2>/dev/null | wc -l
grep -r "@ainexsuite/types" apps/{app}/src --include="*.tsx" --include="*.ts" 2>/dev/null | wc -l

# Check for key patterns
grep -r "use client" apps/{app}/src --include="*.tsx" 2>/dev/null | wc -l      # Client components
grep -r "use server" apps/{app}/src --include="*.tsx" 2>/dev/null | wc -l      # Server actions
grep -r "useState" apps/{app}/src --include="*.tsx" 2>/dev/null | wc -l        # State usage
grep -r "useEffect" apps/{app}/src --include="*.tsx" 2>/dev/null | wc -l       # Effect usage
grep -r "useMemo\|useCallback" apps/{app}/src --include="*.tsx" 2>/dev/null | wc -l  # Memoization
```

**Format metrics as a baseline table:**

```markdown
## Metrics Baseline for {app_name}

| Metric                           | Value |
| -------------------------------- | ----- |
| Total TSX Files                  | X     |
| Total TS Files                   | X     |
| Components                       | X     |
| Custom Hooks                     | X     |
| API Routes                       | X     |
| Lines of Code                    | X     |
| Dependencies                     | X     |
| DevDependencies                  | X     |
| @ainexsuite/ui imports           | X     |
| @ainexsuite/firebase imports     | X     |
| Client Components ("use client") | X     |
| useState calls                   | X     |
| useEffect calls                  | X     |
| useMemo/useCallback calls        | X     |
```

---

### Step 3: Spawn 6 Parallel Review Agents

Use the Task tool to launch 6 Explore agents IN PARALLEL. Each agent focuses on a specific review dimension.

**CRITICAL: Launch all 6 agents in a SINGLE message with multiple Task tool calls.**

#### Agent 1: Backend Modernization

```
Prompt for Agent 1:
---
You are reviewing the BACKEND architecture of the {app_name} app in the AinexSuite monorepo.

**Metrics Baseline:**
{Insert metrics table from Step 2}

**Focus Areas:**
- apps/{app}/src/app/api/ - API route handlers
- apps/{app}/src/lib/ - Service layer, utilities, Firebase interactions

**Review Criteria:**
1. API Design Patterns
   - Route organization (RESTful conventions)
   - Request/response typing
   - Error handling consistency
   - HTTP method appropriateness

2. Firebase Usage
   - Firestore query optimization
   - Real-time listener patterns
   - Security rule alignment
   - Admin SDK vs client SDK usage

3. Error Handling
   - Try/catch consistency
   - Error types and messages
   - Client-friendly error responses
   - Logging strategy

4. Type Safety
   - Strict TypeScript usage
   - Zod/Yup validation
   - Type inference vs explicit types
   - Any/unknown usage

5. Caching Strategies
   - React Query / SWR usage
   - Cache invalidation patterns
   - Optimistic updates

**Reference:**
- packages/firebase patterns for Firestore best practices

**Output Format:**
For each finding, provide:
- Severity: 🔴 Critical / 🟠 Important / 🟡 Suggested / 🟢 Positive
- Location: File path and line numbers
- Description: What the issue is
- Before code snippet (if applicable)
- After code snippet (recommended fix)
- Why: Explanation of impact
---
```

#### Agent 2: Frontend Modernization

```
Prompt for Agent 2:
---
You are reviewing the FRONTEND architecture of the {app_name} app in the AinexSuite monorepo.

**Metrics Baseline:**
{Insert metrics table from Step 2}

**Focus Areas:**
- apps/{app}/src/components/ - React components
- apps/{app}/src/hooks/ - Custom hooks
- apps/{app}/src/app/ - Page components and layouts

**Review Criteria:**
1. React 19 Patterns
   - Server Components vs Client Components
   - "use client" directive placement
   - Server Actions usage
   - Suspense boundaries

2. Component Composition
   - Single responsibility
   - Prop drilling depth
   - Component size (lines)
   - Render prop vs hooks

3. Hook Extraction
   - Logic in components that should be hooks
   - Hook composition patterns
   - Custom hook naming (use* prefix)
   - Hook dependencies

4. State Management
   - Local vs global state
   - Context usage
   - State lifting patterns
   - Derived state vs computed

5. Performance Patterns
   - Memoization (useMemo, useCallback, memo)
   - List virtualization
   - Code splitting / lazy loading
   - Re-render optimization

**Reference:**
- packages/ui component patterns for shared component best practices

**Output Format:**
For each finding, provide:
- Severity: 🔴 Critical / 🟠 Important / 🟡 Suggested / 🟢 Positive
- Location: File path and line numbers
- Description: What the issue is
- Before code snippet (if applicable)
- After code snippet (recommended fix)
- Why: Explanation of impact
---
```

#### Agent 3: UX Review

```
Prompt for Agent 3:
---
You are reviewing the USER EXPERIENCE of the {app_name} app in the AinexSuite monorepo.

**Metrics Baseline:**
{Insert metrics table from Step 2}

**Focus Areas:**
- User flows and interactions
- Loading and error states
- Accessibility (a11y)
- Responsive behavior

**Review Criteria:**
1. Loading States
   - Skeleton components
   - Progressive loading
   - Optimistic UI updates
   - Loading indicators placement

2. Error Feedback
   - Error message clarity
   - Recovery options
   - Form validation feedback
   - Network error handling

3. Empty States
   - First-time user experience
   - No data scenarios
   - Call-to-action clarity
   - Helpful guidance

4. Navigation Flow
   - Breadcrumbs / back navigation
   - Deep linking support
   - Page transition smoothness
   - Browser history handling

5. Accessibility
   - ARIA labels and roles
   - Keyboard navigation
   - Focus management
   - Screen reader compatibility
   - Color contrast
   - Touch targets size

6. Progressive Disclosure
   - Information hierarchy
   - Overwhelming content
   - Expandable sections
   - Tooltip usage

**Output Format:**
For each finding, provide:
- Severity: 🔴 Critical / 🟠 Important / 🟡 Suggested / 🟢 Positive
- Location: File path and line numbers (or component name)
- Description: What the UX issue is
- Current behavior
- Recommended behavior
- Why: User impact explanation
---
```

#### Agent 4: UI Review

```
Prompt for Agent 4:
---
You are reviewing the UI DESIGN IMPLEMENTATION of the {app_name} app in the AinexSuite monorepo.

**Metrics Baseline:**
{Insert metrics table from Step 2}

**Focus Areas:**
- Tailwind CSS usage
- Design system consistency
- Visual styling patterns

**Review Criteria:**
1. Tailwind Usage
   - Arbitrary values vs design tokens
   - Class organization
   - @apply vs inline classes
   - Dark mode implementation

2. Design Token Consistency
   - packages/ui/src/config/tokens.ts usage
   - Color palette adherence
   - Spacing scale (4px base)
   - Typography scale

3. Component Styling
   - Consistent border radius
   - Shadow usage patterns
   - Animation/transition consistency
   - Hover/active state consistency

4. Responsive Design
   - Breakpoint usage (sm, md, lg, xl)
   - Mobile-first approach
   - Container widths
   - Touch-friendly sizing

5. Dark Mode
   - Complete dark mode support
   - Contrast ratios
   - Color variable usage
   - Theme switching behavior

6. Visual Consistency
   - Button styles match across app
   - Input field styling
   - Card/panel styling
   - Icon usage consistency

**Reference:**
- packages/ui/src/config/tokens.ts for design tokens
- packages/ui/src/config/tailwind-presets.ts for Tailwind config

**Output Format:**
For each finding, provide:
- Severity: 🔴 Critical / 🟠 Important / 🟡 Suggested / 🟢 Positive
- Location: File path and line numbers
- Description: What the styling issue is
- Before code snippet (current Tailwind classes)
- After code snippet (recommended classes)
- Why: Visual/UX impact
---
```

#### Agent 5: AI Enhancement Opportunities

```
Prompt for Agent 5:
---
You are reviewing AI INTEGRATION OPPORTUNITIES for the {app_name} app in the AinexSuite monorepo.

**Metrics Baseline:**
{Insert metrics table from Step 2}

**Focus Areas:**
- Current AI usage patterns
- Opportunities for AI enhancement
- packages/ai integration potential

**Review Criteria:**
1. Current AI Usage
   - Gemini integration
   - GPT-4 integration
   - Claude integration
   - Grok integration
   - Prompt patterns

2. Prompt Engineering
   - System prompt quality
   - Few-shot examples
   - Chain-of-thought patterns
   - Output format specification

3. AI Feature Opportunities
   - Content generation potential
   - Smart suggestions
   - Summarization features
   - Search enhancement
   - Auto-categorization
   - Predictive features

4. Streaming & UX
   - Streaming response handling
   - Loading states for AI
   - Error handling for AI failures
   - Rate limiting handling

5. Cost Optimization
   - Model selection appropriateness
   - Token usage efficiency
   - Caching AI responses
   - Batching requests

**Reference:**
- packages/ai for shared AI utilities and best practices
- apps/{app}/src/lib/ai for app-specific AI implementation (if exists)

**Output Format:**
For each opportunity, provide:
- Type: Current Issue / Enhancement Opportunity
- Severity: 🔴 Critical / 🟠 Important / 🟡 Suggested / 🟢 Positive
- Location: Where to implement (file/component)
- Description: What AI feature could be added/improved
- Implementation sketch: High-level approach
- Why: User value explanation
---
```

#### Agent 6: Security & Performance

```
Prompt for Agent 6:
---
You are reviewing SECURITY and PERFORMANCE of the {app_name} app in the AinexSuite monorepo.

**Metrics Baseline:**
{Insert metrics table from Step 2}

**Focus Areas:**
- Authentication patterns
- API security
- Input validation
- Bundle size
- Render performance

**Review Criteria:**
1. Authentication
   - Auth check consistency
   - Session handling
   - Protected route patterns
   - Token management

2. API Security
   - Input validation (Zod/Yup)
   - Rate limiting
   - CORS configuration
   - Sensitive data exposure

3. XSS Prevention
   - Raw HTML insertion patterns
   - User content sanitization
   - URL parameter handling
   - Content Security Policy

4. CSRF Protection
   - Form submission security
   - State-changing GET requests
   - Token validation

5. Bundle Performance
   - Bundle size analysis
   - Tree shaking effectiveness
   - Dynamic imports
   - Image optimization

6. Render Performance
   - Re-render frequency
   - Large list handling
   - Expensive computations
   - Memory leaks (effect cleanup)

7. Data Security
   - Sensitive data in localStorage
   - Console.log with sensitive data
   - Error messages exposing internals
   - API response data filtering

**Output Format:**
For each finding, provide:
- Severity: 🔴 Critical / 🟠 Important / 🟡 Suggested / 🟢 Positive
- Location: File path and line numbers
- Description: What the security/performance issue is
- Before code snippet (if applicable)
- After code snippet (recommended fix)
- Why: Risk/impact explanation
- CVSS-like rating for security issues (Low/Medium/High/Critical)
---
```

---

### Step 4: Synthesize Agent Findings

After all 6 agents complete, synthesize their findings into a unified report.

**Severity Definitions:**

| Level        | Icon         | Criteria                                                     | Action      |
| ------------ | ------------ | ------------------------------------------------------------ | ----------- |
| 🔴 Critical  | Must fix     | Security vulnerabilities, data loss risks, breaking bugs     | Immediate   |
| 🟠 Important | Should fix   | Performance issues, maintainability debt, accessibility gaps | This sprint |
| 🟡 Suggested | Nice to have | Code style, minor optimizations, enhanced UX                 | Backlog     |
| 🟢 Positive  | Keep doing   | Good patterns to preserve and potentially share              | Document    |

**Priority Matrix:**

Group findings by severity and create actionable checklists:

```markdown
### 🔴 Critical (Fix Immediately)

- [ ] [Security] Finding description - `path/to/file.tsx:123`

### 🟠 Important (This Sprint)

- [ ] [Performance] Finding description - `path/to/file.tsx:45`
- [ ] [Accessibility] Finding description - `path/to/component.tsx:89`

### 🟡 Suggested (Backlog)

- [ ] [Code Quality] Finding description - `path/to/file.ts:34`

### 🟢 Positive Patterns (Preserve)

- ✅ Good pattern description - `path/to/file.tsx`
```

---

### Step 5: Identify Package Extraction Candidates

Based on agent findings, identify code that should move to shared packages:

```markdown
## Package Extraction Opportunities

### → packages/ui

| Component       | Current Location              | Reason               |
| --------------- | ----------------------------- | -------------------- |
| `ComponentName` | apps/{app}/src/components/... | Reusable across apps |

### → packages/hooks

| Hook          | Current Location         | Reason                   |
| ------------- | ------------------------ | ------------------------ |
| `useHookName` | apps/{app}/src/hooks/... | Utility hook, duplicated |

### → packages/utils

| Utility        | Current Location       | Reason         |
| -------------- | ---------------------- | -------------- |
| `utilFunction` | apps/{app}/src/lib/... | Common utility |

### → packages/types

| Type       | Current Location         | Reason             |
| ---------- | ------------------------ | ------------------ |
| `TypeName` | apps/{app}/src/types/... | Shared domain type |
```

---

### Step 6: Handle Auto-Fix Mode (if --auto-fix flag present)

If `--auto-fix` was passed, identify and offer to apply safe fixes:

**Safe Auto-Fix Categories:**

1. **Missing "use client" directives**
   - Components using hooks without directive
   - Pattern: Add `"use client";` at file start

2. **Unused imports**
   - Imports that are never used
   - Pattern: Remove import line

3. **Missing TypeScript return types**
   - Functions without explicit return types
   - Pattern: Add `: ReturnType` annotation

4. **Console.log statements**
   - Development logging left in code
   - Pattern: Remove console.log lines

5. **Inconsistent Tailwind class ordering**
   - Unordered utility classes
   - Pattern: Apply prettier-plugin-tailwindcss ordering

**Auto-Fix Prompt:**

```markdown
## Auto-Fixable Issues Found

The following issues can be automatically fixed:

| #   | Issue                           | Files Affected | Risk |
| --- | ------------------------------- | -------------- | ---- |
| 1   | Missing "use client" directives | 8 files        | Low  |
| 2   | Unused imports                  | 23 files       | Low  |
| 3   | Console.log statements          | 7 files        | Low  |

**Options:**

- `[A]` Apply all auto-fixes
- `[S]` Select which fixes to apply
- `[N]` Skip auto-fix, show report only

Which option would you like?
```

**After user selection, apply fixes using Edit tool and show summary:**

```markdown
## Auto-Fix Results

✅ Applied 38 fixes across 15 files:

- Added "use client" to 8 files
- Removed 23 unused imports
- Removed 7 console.log statements

No errors encountered.
```

---

### Step 7: Generate Final Report

**Output Format Template:**

```markdown
# Deep Review: {app_name}

_Generated: {timestamp} | Model: Opus 4.5 | Agents: 6_

---

## 📊 Metrics Baseline

| Metric        | Value |
| ------------- | ----- |
| Total Files   | X     |
| Components    | X     |
| Custom Hooks  | X     |
| API Routes    | X     |
| Lines of Code | X     |
| Dependencies  | X     |

---

## 📋 Executive Summary

{2-3 sentence overview highlighting key strengths and priority improvement areas}

**Health Score: X/100**

- Backend: X/100
- Frontend: X/100
- UX: X/100
- UI: X/100
- AI Integration: X/100
- Security/Performance: X/100

---

## 🎯 Priority Matrix

### 🔴 Critical (Fix Immediately)

{List of critical findings with checkboxes}

### 🟠 Important (This Sprint)

{List of important findings with checkboxes}

### 🟡 Suggested (Backlog)

{List of suggested findings with checkboxes}

### 🟢 Positive Patterns (Preserve)

{List of good patterns to document and share}

---

## 🔍 Detailed Findings

### 1. Backend Modernization

{Agent 1 findings with full detail}

#### Finding 1.1: {Title}

**Severity:** 🟠 Important
**Location:** `apps/{app}/src/app/api/route.ts:45-67`

**Before:**
\`\`\`typescript
// Current problematic code
\`\`\`

**After:**
\`\`\`typescript
// Recommended fix
\`\`\`

**Why:** {Explanation of impact and benefit}

---

### 2. Frontend Modernization

{Agent 2 findings with full detail}

---

### 3. UX Improvements

{Agent 3 findings with full detail}

---

### 4. UI Enhancements

{Agent 4 findings with full detail}

---

### 5. AI Enhancement Opportunities

{Agent 5 findings with full detail}

---

### 6. Security & Performance

{Agent 6 findings with full detail}

---

## 📦 Package Extraction Opportunities

### → packages/ui

| Component | Current Location | Reason |
| --------- | ---------------- | ------ |
| ...       | ...              | ...    |

### → packages/hooks

| Hook | Current Location | Reason |
| ---- | ---------------- | ------ |
| ...  | ...              | ...    |

---

## 🔧 Auto-Fix Summary

{If --auto-fix was used: Show what was fixed}
{If not: Show what COULD be auto-fixed}

**Auto-fixable issues:**

- X missing "use client" directives
- X unused imports
- X console.log statements

_Run `/app-deep-review {app_name} --auto-fix` to automatically apply safe fixes_

---

## 🚀 Recommended Next Steps

1. **Immediate (Today):**
   - {Critical fix 1}
   - {Critical fix 2}

2. **This Week:**
   - {Important improvement 1}
   - {Important improvement 2}

3. **This Month:**
   - {Strategic improvement 1}
   - {Package extraction task}

---

_Report generated by `/app-deep-review` skill using Opus 4.5 with extended thinking_
```

---

## Extended Thinking Triggers

To activate extended thinking (ultrathink), include these phrases in agent prompts:

- "Think deeply about..."
- "Carefully analyze..."
- "Consider all aspects..."
- "Thoroughly examine..."

---

## Error Handling

**App not found:**

```markdown
❌ App "{app_name}" not found.

Available apps:

- main, notes, journal, todo, health, album
- habits, mosaic, fit, projects, flow, subs
- docs, tables, calendar, admin

Usage: /app-deep-review [app-name] [--auto-fix]
Example: /app-deep-review notes --auto-fix
```

**Agent failure:**
If any agent fails to complete, report partial results and note which review dimension is missing.

---

## See Also

- [review-criteria.md](review-criteria.md) - Detailed review criteria for each dimension
- [metrics-collector.md](metrics-collector.md) - Pre-analysis metrics collection guide
- [auto-fixes.md](auto-fixes.md) - Auto-fix pattern definitions and safety criteria
