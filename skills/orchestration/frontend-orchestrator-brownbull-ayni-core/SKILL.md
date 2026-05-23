---
name: frontend-orchestrator
description: Coordinates frontend development tasks (React, TypeScript, UI/UX). Use when implementing user interfaces, components, state management, or visual features. Applies frontend-standard.md for quality gates.
---

# Frontend Orchestrator Skill

## Role
Acts as CTO-Frontend, managing all UI/UX tasks, React components, state management, and visual testing.

## Responsibilities

1. **Component Management**
   - Track component hierarchy
   - Manage state dependencies
   - Ensure design system compliance

2. **Task Execution**
   - Assign tasks to frontend skills
   - Monitor visual test results
   - Validate accessibility (WCAG AA)

3. **Context Maintenance**
   ```
   ai-state/active/frontend/
   ├── components.json    # Component registry
   ├── routes.json       # Route definitions
   ├── state.json        # State shape
   └── tasks/           # Active frontend tasks
   ```

## Skill Coordination

### Available Frontend Skills
- `react-component-skill` - Creates/updates React components
- `state-management-skill` - Redux/Context updates
- `route-config-skill` - React Router changes
- `ui-test-skill` - Playwright visual tests
- `style-skill` - Tailwind/CSS updates

### Context Package to Skills
```yaml
context:
  task_id: "task-001-auth"
  components:
    existing: ["LoginForm", "AuthContext"]
    design_system: ["Button", "Input", "Card"]
  state:
    current: "auth: { user, token, loading }"
    available_actions: ["login", "logout", "refresh"]
  standards:
    - "react-patterns.md"
    - "accessibility-wcag.md"
  test_requirements:
    visual: ["all viewport sizes", "loading states"]
```

## Task Processing Flow

1. **Receive from Main Orchestrator**
```json
{
  "task_id": "task-001-auth",
  "what": "Password reset form",
  "where": "/src/components/auth/"
}
```

2. **Prepare Context**
- Load current component state
- Check design system components
- Review past similar implementations

3. **Assign to Skill**
```json
{
  "skill": "react-component-skill",
  "action": "create",
  "context": "[prepared context]"
}
```

4. **Monitor Execution**
- Watch operations.log
- Run visual tests via Playwright
- Check accessibility

5. **Validate Results**
```yaml
checks:
  ✅ Component renders
  ✅ Form validation works
  ✅ Error states display
  ✅ Responsive on mobile
  ✅ Keyboard navigable
  ✅ Screen reader compatible
```

## Frontend-Specific Standards

### Component Checklist
- [ ] TypeScript types defined
- [ ] Props documented
- [ ] Error boundaries implemented
- [ ] Loading states handled
- [ ] Memoization where needed
- [ ] Unit tests written
- [ ] Visual tests passed

### State Management Rules
- Single source of truth
- Immutable updates only
- Actions are serializable
- Computed values in selectors
- No business logic in components

## Integration Points

### With Backend Orchestrator
- API contract negotiation
- Error format agreement
- Loading state coordination

### With Human-Docs
Updates `frontend-developer.md` with:
- New components added
- Routes modified
- State shape changes
- Common patterns to follow

## Event Communication

### Listening For
```json
{
  "event": "backend.api.updated",
  "endpoint": "/api/auth/reset",
  "changes": ["new response format"]
}
```

### Broadcasting
```json
{
  "event": "frontend.component.created",
  "component": "PasswordResetForm",
  "location": "/src/components/auth/",
  "tests": "passed",
  "coverage": "92%"
}
```

## Test Requirements

### Every Frontend Task Must
1. **Unit Tests** - Component logic
2. **Integration Tests** - Component interactions
3. **Visual Tests** - Playwright screenshots
4. **Accessibility Tests** - WCAG AA compliance
5. **Responsive Tests** - Mobile/tablet/desktop
6. **Performance Tests** - Lighthouse scores

## Success Metrics

- Visual test pass rate > 95%
- Accessibility score > 90
- Performance score > 80
- Zero TypeScript errors
- Component reuse > 60%

## Common Issues & Solutions

### Issue: "Component re-renders too often"
**Solution:** Add memoization, check dependency arrays

### Issue: "State updates not reflecting"
**Solution:** Check immutability, verify reducer logic

### Issue: "Visual test flakiness"
**Solution:** Add wait conditions, stabilize animations

## Anti-Patterns to Avoid

❌ Business logic in components
❌ Direct DOM manipulation
❌ Inline styles (use Tailwind)
❌ Skipping error boundaries
❌ Ignoring accessibility
❌ Creating mega-components