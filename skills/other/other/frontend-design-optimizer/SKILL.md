---
name: frontend-design-optimizer
description: Find the best UI/UX design patterns and architectures using deep research. Use when user asks to "improve UI", "optimize UX", "best design for [feature]", or "modern UI patterns".
version: 1.0.0
agents: [codex-deep-research, gemini-research-analyst]
---

# Frontend UI/UX Design Optimizer

**Deep research-driven skill for finding optimal frontend design patterns.**

## When to Use

Invoke this skill when the user mentions:
- "What's the best UI pattern for..."
- "How should I design the frontend for..."
- "Improve the UX of..."
- "Modern design patterns for..."
- "Find examples of [component/feature] design"
- "Best practices for [UI element]"

## Research-First Methodology

This skill uses multi-agent deep research to find proven, production-ready design patterns.

### Step 1: Understand Context
```bash
# First, analyze the current codebase
- What framework are we using? (React, Vue, vanilla JS)
- What UI library is present? (Bootstrap, Tailwind, custom)
- What's the design system? (Material, custom, none)
- Who are the users? (internal tools, customer-facing, admin panels)
```

### Step 2: Launch Deep Research

**Use the codex-deep-research agent** to investigate:

```markdown
Invoke Task tool with subagent_type="codex-deep-research"

Prompt:
"Research the best UI/UX design patterns for [specific feature/component].

Context:
- Tech stack: [from Step 1]
- User type: [from Step 1]
- Requirements: [user's specific needs]

Please provide:
1. Top 3-5 proven design patterns with examples
2. Pros/cons of each approach
3. Real-world implementations (with links to examples)
4. Accessibility considerations (WCAG compliance)
5. Performance implications
6. Mobile responsiveness strategies
7. Recommendations ranked by: usability, accessibility, performance

Include code examples and visual descriptions where possible."
```

### Step 3: Compare with Modern Standards

**Use the gemini-research-analyst agent** (if Gemini-specific UI tools are relevant):

```markdown
Invoke Task tool with subagent_type="gemini-research-analyst"

Prompt:
"Research if Google's Gemini AI has any UI/UX design tools, guidelines, or recommended patterns for [specific feature].

Specifically check for:
1. Gemini-powered design assistants
2. Google's Material Design 3 updates
3. AI-assisted UI generation tools
4. Accessibility tools from Google AI
5. Any Gemini integrations for design workflows

If Gemini has relevant tools, explain how to integrate them."
```

### Step 4: Synthesize Recommendations

After agents return results:

1. **Compare patterns** from research
2. **Rank by criteria**:
   - User experience (most important)
   - Accessibility (WCAG AA minimum)
   - Performance (Lighthouse score impact)
   - Maintainability (code complexity)
   - Browser compatibility
   - Mobile-first design

3. **Provide decision matrix**:
```markdown
## Design Pattern Comparison

| Pattern | UX Score | A11y | Perf | Maintainability | Best For |
|---------|----------|------|------|----------------|----------|
| [Pattern 1] | ⭐⭐⭐⭐⭐ | WCAG AA | 95/100 | Low complexity | [Use case] |
| [Pattern 2] | ⭐⭐⭐⭐ | WCAG AAA | 88/100 | Medium | [Use case] |
```

4. **Recommend top choice** with justification

### Step 5: Provide Implementation Plan

```markdown
## Recommended: [Pattern Name]

### Why This Pattern?
- [Justification based on research]
- [Link to production examples]
- [Performance benchmarks]

### Implementation Steps
1. [Step 1 with code example]
2. [Step 2 with code example]
3. [Step 3 with code example]

### Accessibility Checklist
- [ ] Keyboard navigation
- [ ] Screen reader support (ARIA labels)
- [ ] Color contrast (4.5:1 minimum)
- [ ] Focus indicators
- [ ] Semantic HTML

### Testing Strategy
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsive testing (320px to 1920px)
- [ ] Lighthouse audit (>90 accessibility score)
- [ ] Screen reader testing (NVDA, JAWS, VoiceOver)

### Example Code
```javascript
// [Full working example from research]
```

### Live Examples
- [Link to CodeSandbox/CodePen]
- [Link to production site using this pattern]
- [Link to design system documentation]
```

## Validation Criteria

Before presenting recommendations, ensure:

- ✅ At least 3 different patterns researched
- ✅ Each pattern has production examples
- ✅ Accessibility compliance verified (WCAG AA minimum)
- ✅ Performance benchmarks included
- ✅ Mobile responsiveness addressed
- ✅ Code examples are complete and working
- ✅ Browser compatibility documented

## Anti-Patterns to Avoid

**NEVER recommend without research:**
- Trends without proven track record
- Patterns with poor accessibility
- Solutions that don't match tech stack
- Overcomplicated solutions for simple problems

**ALWAYS prioritize:**
- User experience over aesthetics
- Accessibility over visual flair
- Performance over feature bloat
- Maintainability over cleverness

## Example Invocation

```markdown
User: "What's the best way to design a real-time dashboard with live metrics?"