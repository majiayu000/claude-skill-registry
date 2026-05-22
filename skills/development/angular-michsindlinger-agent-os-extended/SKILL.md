---
description: Angular frontend development patterns for [PROJECT_NAME]
globs:
  - "src/app/**/*.ts"
  - "src/app/**/*.html"
  - "src/app/**/*.scss"
  - "src/app/**/*.css"
alwaysApply: false
---

# Angular Frontend Skill

> Project: [PROJECT_NAME]
> Framework: Angular [VERSION]
> Generated: [DATE]

## Quick Reference

### Components
- **Smart vs Dumb**: Container components handle logic, presentational components are pure
- **Change Detection**: Use `OnPush` by default for better performance
- **Signals**: Prefer signals over BehaviorSubject for reactive state (Angular 16+)

### State Management
- **Local State**: Use signals or component properties
- **Shared State**: Use services with signals or NgRx/Signals Store
- **Server State**: Consider TanStack Query or similar for caching

### API Integration
- **HttpClient**: Always use with interceptors for auth/error handling
- **Error Handling**: Use catchError operator, show user-friendly messages
- **Loading States**: Track loading state for better UX

### Forms
- **Reactive Forms**: Prefer over template-driven for complex forms
- **Validation**: Custom validators in separate files
- **Error Display**: Consistent error message components

### Testing
- **Unit Tests**: Use TestBed, mock dependencies
- **Component Tests**: Use ComponentFixture
- **E2E**: Cypress or Playwright

## Available Modules

| Module | File | Use When |
|--------|------|----------|
| Component Patterns | components.md | Creating/modifying components |
| State Management | state-management.md | Adding state, signals, stores |
| API Integration | api-integration.md | HTTP calls, services, interceptors |
| Forms & Validation | forms-validation.md | Forms, validators, error display |
| Dos and Don'ts | dos-and-donts.md | Project-specific learnings |

## How to Load Modules

When you need detailed patterns, read the specific module:
```
Read: .claude/skills/frontend-angular/[module].md
```

## Project Context

### Tech Stack
<!-- Extracted from agent-os/product/tech-stack.md -->
- **Framework:** Angular [ANGULAR_VERSION]
- **State Management:** [STATE_MANAGEMENT_LIBRARY]
- **UI Library:** [UI_LIBRARY]
- **Testing:** [TESTING_FRAMEWORK]
- **Build Tool:** [BUILD_TOOL]

### Architecture Patterns
<!-- Extracted from agent-os/product/architecture-decision.md -->
[ARCHITECTURE_PATTERNS]

### Project Structure
<!-- Extracted from agent-os/product/architecture-structure.md -->
```
[PROJECT_STRUCTURE]
```

---

## Design System
<!-- Extracted from agent-os/product/design-system.md -->

### Colors
[DESIGN_COLORS]

### Typography
[DESIGN_TYPOGRAPHY]

### Spacing
[DESIGN_SPACING]

### Components
[DESIGN_COMPONENTS]

**Reference:** `agent-os/product/design-system.md`

---

## UX Patterns
<!-- Extracted from agent-os/product/ux-patterns.md -->

### Navigation
[UX_NAVIGATION]

### User Flows
[UX_USER_FLOWS]

### Feedback States
[UX_FEEDBACK_STATES]

### Accessibility
[UX_ACCESSIBILITY]

**Reference:** `agent-os/product/ux-patterns.md`

---

## Self-Learning

Wenn du während der Implementierung etwas lernst:
- Unerwartetes Verhalten
- Besserer Ansatz gefunden
- Fehler der Zeit gekostet hat

**→ Füge es zu `dos-and-donts.md` in diesem Ordner hinzu.**
