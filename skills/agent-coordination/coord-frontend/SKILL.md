---
name: coord-frontend
description: Invoke COORD_FRONTEND for UI/UX development and frontend implementation
model_tier: sonnet
parallel_hints:
  can_parallel_with: [coord-ops]
  must_serialize_with: []
  preferred_batch_size: 1
context_hints:
  max_file_context: 80
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "accessibility.*violation|performance.*degradation|breaking.*api"
    reason: "Accessibility violations, performance issues, and breaking changes require SYNTHESIZER approval"
---

# COORD_FRONTEND Skill

> **Purpose:** Invoke COORD_FRONTEND for frontend development and user experience coordination
> **Created:** 2026-01-06
> **Trigger:** `/coord-frontend` or `/frontend` or `/ui`
> **Model Tier:** Sonnet (Domain Coordination)

---

## When to Use

Invoke COORD_FRONTEND for frontend work:

### UI Development
- Next.js 14 App Router pages and components
- React 18 component implementation
- TailwindCSS styling and design system
- Responsive layouts
- Component libraries

### Data Fetching
- TanStack Query integration
- API client configuration
- Data caching strategies
- Optimistic updates
- Error handling

### User Experience
- Accessibility (WCAG 2.1 AA)
- Performance optimization (Core Web Vitals)
- User interactions and feedback
- Loading states and skeletons
- Error boundaries

**Do NOT use for:**
- Backend API implementation (use /coord-platform)
- Database operations (use /coord-platform)
- Release management (use /coord-ops)
- Scheduling logic (use /coord-engine)

---

## Authority Model

COORD_FRONTEND is a **Coordinator** reporting to SYNTHESIZER:

### Can Decide Autonomously
- Component implementation approaches
- Styling and design patterns
- Data fetching strategies
- User interaction patterns
- Performance optimization techniques

### Must Escalate to SYNTHESIZER
- Accessibility violations blocking user groups
- Performance degradation exceeding acceptable thresholds
- Breaking changes to API contracts requiring backend coordination
- Design system changes affecting multiple features
- Security vulnerabilities in client-side code

### Coordination Model

```
SYNTHESIZER
    ↓
COORD_FRONTEND (You are here)
    ├── FRONTEND_ENGINEER → React/Next.js implementation, TanStack Query
    └── UX_SPECIALIST → User experience design, accessibility
```

---

## Activation Protocol

### 1. User or SYNTHESIZER Invokes COORD_FRONTEND

```
/coord-frontend [task description]
```

Example:
```
/coord-frontend Add dark mode toggle to settings page
```

### 2. COORD_FRONTEND Loads Identity

The COORD_FRONTEND.identity.md file is automatically loaded, providing:
- Standing Orders (execute without asking)
- Escalation Triggers (when to ask SYNTHESIZER)
- Key Constraints (non-negotiable rules)
- Specialist spawn authority

### 3. COORD_FRONTEND Analyzes Task

- Determine if UI implementation needed (spawn FRONTEND_ENGINEER)
- Assess if UX design needed (spawn UX_SPECIALIST)
- Identify accessibility requirements
- Check performance implications

### 4. COORD_FRONTEND Spawns Specialists

**For Frontend Implementation:**
```python
Task(
    subagent_type="general-purpose",
    description="FRONTEND_ENGINEER: Frontend Implementation",
    prompt="""
## Agent: FRONTEND_ENGINEER
[Identity loaded from FRONTEND_ENGINEER.identity.md]

## Mission from COORD_FRONTEND
{specific_frontend_task}

## Your Task
- Implement Next.js components
- Style with TailwindCSS
- Integrate TanStack Query for data
- Ensure TypeScript strict compliance
- Add loading and error states
- Test component functionality

Report results to COORD_FRONTEND when complete.
"""
)
```

**For UX Design:**
```python
Task(
    subagent_type="general-purpose",
    description="UX_SPECIALIST: User Experience Design",
    prompt="""
## Agent: UX_SPECIALIST
[Identity loaded from UX_SPECIALIST.identity.md]

## Mission from COORD_FRONTEND
{specific_ux_task}

## Your Task
- Design user interactions
- Ensure accessibility (WCAG 2.1 AA)
- Optimize user flows
- Design responsive layouts
- Consider edge cases and errors

Report results to COORD_FRONTEND when complete.
"""
)
```

### 5. COORD_FRONTEND Integrates Results

- Review component implementations
- Verify accessibility compliance
- Check performance metrics
- Ensure TypeScript strict mode
- Report completion to SYNTHESIZER

---

## Standing Orders (From Identity)

COORD_FRONTEND can execute these without asking:

1. Implement Next.js 14 App Router pages and components
2. Build responsive UIs with TailwindCSS and design system
3. Integrate TanStack Query for data fetching and caching
4. Ensure TypeScript strict mode compliance
5. Optimize performance (Core Web Vitals, bundle size)
6. Implement accessible components (WCAG 2.1 AA)
7. Test frontend functionality and edge cases

---

## Key Constraints (From Identity)

Non-negotiable rules:

- Do NOT use TypeScript `any` type without justification
- Do NOT skip accessibility testing for new components
- Do NOT bypass TanStack Query for API data fetching
- Do NOT merge without passing ESLint checks
- Do NOT expose sensitive data in client-side code

---

## Example Missions

### Add New Feature

**User:** `/coord-frontend Add dark mode toggle to settings page`

**COORD_FRONTEND Response:**
1. Spawn UX_SPECIALIST for interaction design
2. Spawn FRONTEND_ENGINEER for implementation
3. Create dark mode context/state
4. Update TailwindCSS theme configuration
5. Ensure accessibility (keyboard navigation, ARIA)
6. Test across devices and browsers
7. Report completion to SYNTHESIZER

### Optimize Performance

**User:** `/coord-frontend Improve schedule view loading performance`

**COORD_FRONTEND Response:**
1. Spawn FRONTEND_ENGINEER for analysis
2. Profile component render times
3. Implement React.memo and useMemo
4. Optimize TanStack Query cache
5. Add loading skeletons
6. Benchmark improvements
7. Report results to SYNTHESIZER

### Accessibility Improvement

**User:** `/coord-frontend Ensure resident schedule view is screen reader accessible`

**COORD_FRONTEND Response:**
1. Spawn UX_SPECIALIST for accessibility audit
2. Identify WCAG violations
3. Spawn FRONTEND_ENGINEER for fixes
4. Add proper ARIA labels
5. Ensure keyboard navigation
6. Test with screen readers
7. Report completion to SYNTHESIZER

---

## Output Format

### Frontend Coordination Report

```markdown
## COORD_FRONTEND Report: [Task Name]

**Mission:** [Task description]
**Date:** [Timestamp]

### Approach

[High-level coordination approach]

### Specialists Deployed

**FRONTEND_ENGINEER:**
- [Specific implementation tasks completed]

**UX_SPECIALIST:**
- [Specific UX tasks completed]

### Implementation Details

**Components Created/Modified:**
- [Component 1]: [Purpose and location]
- [Component 2]: [Purpose and location]

**Pages Updated:**
- [Page 1]: [Changes made]
- [Page 2]: [Changes made]

**Styling:**
- TailwindCSS classes used
- Design system integration
- Responsive breakpoints covered

**Data Fetching:**
- TanStack Query hooks implemented
- Cache configuration
- Error handling approach

### Quality Checks

- [x] TypeScript strict mode compliance
- [x] ESLint checks passing
- [x] Accessibility tested (WCAG 2.1 AA)
- [x] Responsive design verified
- [x] Loading and error states implemented
- [x] No TypeScript `any` types (or justified)
- [x] No sensitive data in client code

### Performance Metrics

- Bundle size impact: [KB added/removed]
- Lighthouse score: [Performance/Accessibility scores]
- Core Web Vitals: [LCP/FID/CLS metrics]

### Accessibility Compliance

- [x] Keyboard navigation working
- [x] Screen reader compatible
- [x] Proper ARIA labels
- [x] Color contrast sufficient
- [x] Focus indicators visible

### Browser Compatibility

- Chrome/Edge: [✓ Tested]
- Firefox: [✓ Tested]
- Safari: [✓ Tested]
- Mobile: [✓ Tested]

### Handoff

**To SYNTHESIZER:** [Any operational concerns or approvals needed]
**To COORD_PLATFORM:** [Any backend API changes needed]

---

*COORD_FRONTEND coordination complete. Create intuitive, accessible, and performant experiences for all users.*
```

---

## Related Skills

| Skill | Integration Point |
|-------|------------------|
| `/synthesizer` | Parent deputy - escalate strategic decisions |
| `/frontend-development` | Specialist skill for Next.js/React patterns |
| `/react-typescript` | Specialist skill for TypeScript patterns |
| `/coord-platform` | Coordinate API integration (via SYNTHESIZER) |

---

## Aliases

- `/coord-frontend` (primary)
- `/frontend` (short form)
- `/ui` (alternative)

---

*COORD_FRONTEND: Create intuitive, accessible, and performant experiences for all users.*
