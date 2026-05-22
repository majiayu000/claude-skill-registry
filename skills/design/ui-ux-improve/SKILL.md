---
name: ui-ux-improve
description: Research UI/UX improvements with trend analysis and generate actionable recommendations. Use when you need comprehensive UI/UX analysis and improvement suggestions.
context: fork
agent: general-purpose
---

# UI/UX Improvement Research Command

## User Input

```text
$ARGUMENTS
```

Parse user input for:

- **Focus Area**: Specific component, page, or feature to improve (optional)
- **Mode**: `research` (default) or `implement` (immediate action)
- **Scope**: `full` (entire app) or `targeted` (specific area)

If empty, analyze entire application with research mode.

---

## Overview

This command combines AI-powered UI/UX analysis with real-time trend research to generate actionable improvement recommendations.

### Key Features

- 🎨 **UI/UX Designer Agent**: Specialized analysis via ui-ux-designer agent
- 🛠️ **Tech Stack Advisor Agent**: Library/framework recommendations via tech-stack-advisor agent
- 🔍 **Trend Research**: Web search for current UI/UX trends (2024-2025)
- 📊 **Gap Analysis**: Compare current state vs best practices
- 📝 **Actionable Report**: Generate improvement roadmap in markdown
- 🚀 **Optional Implementation**: Execute improvements on demand

---

## Execution Steps

### 1. Context Gathering

#### Analyze Project Structure

**Detect Frontend Framework**:

- Check `package.json` for: React, Next.js, Vue, Svelte, Angular
- Identify styling approach: Tailwind, CSS Modules, styled-components, CSS-in-JS
- Find component library: shadcn/ui, MUI, Chakra, Radix

**Explore UI Components**:

- Use Glob to find component files (`**/*.tsx`, `**/components/**/*`)
- Identify layout components (Header, Footer, Sidebar, Navigation)
- Map page structure and routing

**Analyze Current Design System**:

- Color palette (CSS variables, theme config)
- Typography (fonts, sizes, weights)
- Spacing and layout patterns
- Component consistency

### 2. Invoke UI/UX Designer Agent

**REQUIRED**: Use Task tool with `subagent_type: "ui-ux-designer"` to perform:

- User experience evaluation
- Accessibility assessment (WCAG guidelines)
- Information architecture review
- Component usability analysis
- Mobile responsiveness check

**Agent Prompt Template**:

```
Analyze the UI/UX of this project focusing on:
1. User journey and flow optimization
2. Visual hierarchy and information architecture
3. Accessibility compliance (WCAG 2.1 AA)
4. Component reusability and consistency
5. Responsive design patterns
6. User interaction feedback patterns

Project context:
- Framework: {detected framework}
- Styling: {styling approach}
- Component library: {if any}
- Focus area: {from user input or "entire application"}

Provide specific, actionable recommendations with priority levels.
```

### 3. Invoke Tech Stack Advisor Agent

**REQUIRED**: Use Task tool with `subagent_type: "tech-stack-advisor"` when:

- Recommending new UI component libraries
- Evaluating animation/interaction libraries
- Comparing styling solutions
- Suggesting accessibility tooling
- Recommending state management for UI

**Agent Prompt Template**:

```
Evaluate UI/UX related technologies for this project:

Current stack:
- Framework: {detected framework}
- Styling: {styling approach}
- Component library: {if any}

Evaluate these categories based on project needs:
1. Component libraries (shadcn/ui, Radix, Headless UI, etc.)
2. Animation libraries (Framer Motion, React Spring, GSAP)
3. Accessibility tools (axe-core, react-aria, etc.)
4. Icon libraries (Lucide, Heroicons, Phosphor)
5. Form libraries (React Hook Form, Formik, etc.)

For each recommendation:
- Modernity score (0-10)
- Stability score (0-10)
- Bundle size impact
- Migration complexity
- Learning curve

Focus on: {user focus area or "general UI/UX improvement"}
```

### 4. Trend Research (Web Search)

**Search Queries** (use WebSearch tool):

1. `"UI/UX trends 2025" best practices`
2. `"{framework} UI design patterns 2025"` (e.g., "React UI design patterns 2025")
3. `"modern web design trends" accessibility`
4. `"{component type} UX best practices"` (if specific focus area)
5. `"best {library type} library 2025"` (e.g., "best React animation library 2025")

**Information to Gather**:

- Current design trends (micro-interactions, glassmorphism, etc.)
- Accessibility improvements
- Performance optimization patterns
- User engagement techniques
- Mobile-first strategies
- Emerging UI libraries and tools
- Bundle size optimization techniques

### 5. Gap Analysis

**Compare and Identify**:

- Current design vs trend recommendations
- Missing accessibility features
- Outdated patterns to modernize
- Quick wins vs major refactors
- Priority based on impact/effort ratio
- Library/tool upgrades or additions needed

### 6. Generate Report

**Create**: `UI-UX-IMPROVEMENTS.md` at project root

**Structure**:

```markdown
# UI/UX Improvement Recommendations

> **Generated**: {YYYY-MM-DD HH:mm}
> **Scope**: {full/targeted: specific area}
> **Mode**: {research/implement}

---

## 📊 Current State Analysis

### Framework & Stack

- **Framework**: {detected}
- **Styling**: {approach}
- **Component Library**: {if any}

### Strengths

- {what's working well}

### Areas for Improvement

- {identified issues}

---

## 🎯 Trend Insights (2024-2025)

### Design Trends

- {trend 1}: {how it applies}
- {trend 2}: {how it applies}

### Accessibility Standards

- {WCAG requirements}
- {current compliance status}

### UX Best Practices

- {practice 1}
- {practice 2}

---

## 🛠️ Technology Recommendations

### Recommended Libraries

| Category   | Library   | Score  | Bundle Size | Why      |
| ---------- | --------- | ------ | ----------- | -------- |
| {category} | {library} | {X}/10 | {size}      | {reason} |

### Migration Considerations

- {library 1}: {migration notes}
- {library 2}: {migration notes}

---

## 🚀 Recommendations

### Critical Priority

#### 1. {Recommendation Title}

**Problem**: {what's wrong}
**Solution**: {how to fix}
**Impact**: {user benefit}
**Effort**: {Low/Medium/High}
**Files**: {affected files}

### High Priority

#### 2. {Recommendation Title}

{same structure}

### Medium Priority

#### 3. {Recommendation Title}

{same structure}

---

## 📋 Implementation Roadmap

### Phase 1: Quick Wins (1-2 days)

- [ ] {task 1}
- [ ] {task 2}

### Phase 2: Core Improvements (1-2 weeks)

- [ ] {task 3}
- [ ] {task 4}

### Phase 3: Advanced Enhancements (2-4 weeks)

- [ ] {task 5}
- [ ] {task 6}

---

## 🔗 Resources

- {relevant documentation links}
- {trend articles referenced}
- {component library docs}
```

### 7. Implementation Mode (if requested)

If user specified `implement` mode or requests immediate action:

1. Confirm scope with user before proceeding
2. Start with Critical Priority items
3. Make incremental changes with clear commits
4. Verify each change doesn't break existing functionality
5. Update report with completed items

---

## Key Rules

### ✅ MUST DO

- **Always invoke ui-ux-designer agent** for expert analysis
- **Always invoke tech-stack-advisor agent** for library/tool recommendations
- **Perform web search** for current trends and library comparisons
- **Analyze actual project code** (not assumptions)
- **Provide specific file paths** in recommendations
- **Include effort estimates** for each recommendation
- **Evaluate bundle size impact** for library recommendations
- **Generate report at project root** (`UI-UX-IMPROVEMENTS.md`)
- **Consider accessibility** in all recommendations
- **Prioritize by impact/effort ratio**

### ❌ NEVER DO

- Skip ui-ux-designer or tech-stack-advisor agent invocation
- Make recommendations without code analysis
- Suggest breaking changes without migration path
- Ignore mobile/responsive considerations
- Recommend trends that conflict with project constraints
- Implement without user confirmation (in implement mode)
- Generate vague or non-actionable recommendations
- Recommend libraries without bundle size consideration
- Suggest libraries with poor stability scores (<6/10)

### 🎯 Quality Standards

Each recommendation must include:

1. **Clear Problem Statement**: What's wrong and why it matters
2. **Specific Solution**: How to fix with code examples if applicable
3. **User Impact**: How it improves user experience
4. **Effort Estimate**: Implementation complexity (Low/Medium/High)
5. **File References**: Which files need changes

---

## Completion Report

After execution, provide summary:

```markdown
## UI/UX Improvement Research Complete

### 📊 Analysis Summary

- **Components Analyzed**: {X}
- **Pages Reviewed**: {Y}
- **Trends Researched**: {Z}
- **Libraries Evaluated**: {W}

### 🎯 Recommendations

- **Critical**: {N}
- **High**: {M}
- **Medium**: {K}

### 📄 Generated Report

`UI-UX-IMPROVEMENTS.md` created at project root.

### Next Steps

{Based on mode}:

- **Research mode**: Review recommendations and run with `implement` to proceed
- **Implement mode**: {X} improvements applied, {Y} remaining
```

---

## Execute

Start the UI/UX improvement research following the guidelines above.
