---
name: implementing-navigation
description: Implements navigation patterns and routing for both frontend (React/TS) and backend (Python) including menus, tabs, breadcrumbs, client-side routing, and server-side route configuration. Use when building navigation systems or setting up routing.
---

# Navigation Patterns & Routing Implementation

## Purpose

This skill provides comprehensive guidance for implementing navigation systems across both frontend and backend applications. It covers client-side navigation patterns (menus, tabs, breadcrumbs) and routing (React Router, Next.js) as well as server-side route configuration (Flask, Django, FastAPI).

## When to Use

Use this skill when:
- Building primary navigation (top, side, mega menus)
- Implementing secondary navigation (breadcrumbs, tabs, pagination)
- Setting up client-side routing (React Router, Next.js)
- Configuring server-side routes (Flask, Django, FastAPI)
- Creating mobile navigation patterns (hamburger, bottom nav)
- Implementing keyboard-accessible navigation
- Building command palettes or search-driven navigation
- Creating multi-step wizards or steppers
- Ensuring WCAG 2.1 AA compliance for navigation

## Navigation Decision Framework

```
Information Architecture → Navigation Pattern

Flat (1-2 levels)      → Top Navigation
Deep (3+ levels)       → Side Navigation
E-commerce/Large       → Mega Menu
Linear Process         → Stepper/Wizard
Long Content          → Table of Contents
Power Users           → Command Palette
Multi-section Page    → Tabs
Large Data Sets       → Pagination
```

## Frontend Navigation Components

### Primary Navigation Patterns

**Top Navigation (Horizontal)**
- Best for shallow hierarchies, marketing sites
- 5-7 primary links maximum for cognitive load
- See `references/menu-patterns.md` for implementation

**Side Navigation (Vertical)**
- Best for deep hierarchies, admin panels, dashboards
- Supports multi-level nesting and collapsible sections
- See `references/menu-patterns.md` for sidebar patterns

**Mega Menu**
- Best for e-commerce, content-heavy sites
- Rich content with images and descriptions
- See `references/menu-patterns.md` for mega menu structure

### Secondary Navigation Components

**Breadcrumbs**
- Shows hierarchical path and current location
- Essential for deep sites and e-commerce
- See `references/navigation-components.md` for breadcrumb patterns

**Tabs**
- Content switching without page reload
- URL synchronization for bookmarking
- See `references/navigation-components.md` for tab implementation

**Pagination**
- For search results, product lists, articles
- Consider virtualization for performance
- See `references/navigation-components.md` for pagination patterns

### Client-Side Routing

**React Router (Industry Standard)**
- Type-safe routing with loader patterns
- Nested routes and lazy loading support
- See `references/client-routing.md` for React Router patterns

**Next.js App Router**
- File-based routing with RSC support
- Parallel and intercepting routes
- See `references/client-routing.md` for Next.js routing

## Backend Routing Patterns

### Python Web Frameworks

**Flask**
- Blueprint-based organization
- Route decorators and URL rules
- See `references/flask-routing.md` for Flask patterns

**Django**
- URL configuration with namespaces
- Path converters and regex patterns
- See `references/django-urls.md` for Django URL conf

**FastAPI**
- Router-based organization
- Path operations and dependencies
- See `references/fastapi-routing.md` for FastAPI routers

## Mobile Navigation

### Patterns for Touch Devices

**Hamburger Menu**
- Slide-out drawer for primary navigation
- See `references/menu-patterns.md` for mobile drawer

**Bottom Navigation**
- 3-5 primary actions, thumb-friendly
- See `references/menu-patterns.md` for bottom nav

**Tab Bar**
- Horizontal scrollable tabs with swipe
- Natural for mobile-first applications

## Accessibility Requirements

### Keyboard Navigation

```
Tab       → Move forward through links
Shift+Tab → Move backward through links
Enter     → Activate link/button
Space     → Activate button
Arrow keys → Navigate within menus
Escape    → Close dropdowns/modals
```

### ARIA Patterns

Essential ARIA attributes for accessible navigation:
- See `references/accessibility-navigation.md` for complete ARIA patterns
- Includes landmark roles, states, and properties
- Screen reader optimization techniques

### Focus Management

- Visible focus indicators (2px minimum, 3:1 contrast)
- Focus trap for modals and dropdowns
- Skip navigation link for keyboard users
- See `references/accessibility-navigation.md` for focus patterns

## Implementation Utilities

### Navigation Structure Management

Generate and validate navigation trees:
```bash
# Validate navigation structure
node scripts/validate_navigation_tree.js nav-config.json

# Generate breadcrumb trails
node scripts/calculate_breadcrumbs.js current-path
```

### Route Generation (Python)

Generate route configurations:
```bash
# Generate Flask/Django/FastAPI routes
python scripts/generate_routes.py --framework flask --config routes.yaml
```

## Code Examples

### Frontend Examples

For working navigation implementations:
- `examples/horizontal-menu.tsx` - Responsive top navigation
- `examples/tab-navigation.tsx` - Tabs with URL sync
- `examples/mobile-navigation.tsx` - Hamburger and drawer

### Backend Examples

For routing configuration:
- `examples/flask_routes.py` - Flask blueprint setup
- `examples/django_urls.py` - Django URL patterns
- `examples/fastapi_routes.py` - FastAPI router organization

## Navigation Configuration

For complex navigation structures, use the configuration schema:
- `assets/navigation-config-schema.json` - Navigation tree schema
- `assets/route-templates.json` - Common route patterns

Validate configurations before implementation using the validation script.

## Library Recommendations

### Frontend Routing

**React Router** is the recommended solution for React applications:
- Industry standard with excellent TypeScript support
- Built-in accessibility with NavLink active states
- See `references/library-comparison.md` for alternatives

### Component Libraries

For rapid development, consider:
- Headless UI libraries (Radix UI, React Aria)
- Accessible by default
- Work with any styling approach

## Progressive Enhancement

Build navigation that works without JavaScript:
- Server-rendered HTML navigation
- Progressive enhancement with client-side routing
- Fallback for JavaScript failures

## Performance Considerations

- Lazy load route components
- Prefetch navigation targets
- Use route-based code splitting
- Implement loading states for navigation

## Testing Navigation

Essential navigation tests:
- Keyboard navigation flow
- Screen reader announcements
- Mobile touch interactions
- Route parameter validation
- Deep linking functionality

## Next Steps

1. Analyze the information architecture
2. Select appropriate navigation pattern
3. Implement with accessibility first
4. Add progressive enhancement
5. Test across devices and assistive technologies

For detailed implementation guides, explore the referenced documentation files based on specific requirements.