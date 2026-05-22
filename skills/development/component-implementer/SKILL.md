---
name: component-implementer
description: Implements UI components from design specifications. Use when implementing frontend components, pages, or UI elements. Follows design specs from ui-ux-designer, implements responsive design, and ensures accessibility.
---

# Component Implementer Skill

## Instructions

1. Analyze component requirements from task
2. Review design specifications from ui-ux-designer
3. Implement component structure (HTML/JSX)
4. Apply styling according to design specs
5. Implement component states (default, hover, active, etc.)
6. Add interactions and animations
7. Ensure accessibility compliance
8. Make component responsive
9. Return implementation with:
   - Component code
   - Styling (CSS/SCSS)
   - State management
   - Accessibility features
   - Responsive design

## Examples

**Input:** "Implement submit button with design specs"
**Output:**
```jsx
// components/Button.jsx
function Button({ children, variant = 'primary', size = 'medium', disabled, onClick }) {
    return (
        <button
            className={`btn btn-${variant} btn-${size}`}
            disabled={disabled}
            onClick={onClick}
            aria-label={children}
        >
            {children}
        </button>
    );
}

// styles/Button.css
.btn {
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: all 150ms ease-in-out;
}

.btn-primary {
    background-color: #007bff;
    color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
    background-color: #0056b3;
    transform: scale(1.02);
}

.btn-primary:focus {
    outline: 2px solid #007bff;
    outline-offset: 2px;
}

.btn-primary:disabled {
    background-color: #6c757d;
    opacity: 0.6;
    cursor: not-allowed;
}
```

## Component Implementation Areas

- **Component Structure**: HTML/JSX structure
- **Styling**: CSS according to design specs
- **States**: Default, hover, active, focus, disabled, loading
- **Interactions**: Click handlers, animations, transitions
- **Accessibility**: ARIA labels, keyboard navigation, focus management
- **Responsive Design**: Mobile/tablet/desktop adaptations
- **Props/Props Interface**: Component API and props
- **State Management**: Component state, props, context

## Design Spec Compliance

- **Colors**: Use exact colors from design specs
- **Spacing**: Use spacing values from design system
- **Typography**: Follow typography system
- **Layout**: Follow layout specifications
- **Interactions**: Implement interactions as specified
- **Responsive**: Follow responsive breakpoints

## Best Practices

- **Follow Design Specs**: Implement exactly as designed
- **Accessibility First**: Ensure WCAG compliance
- **Responsive**: Mobile-first approach
- **Reusable**: Make components reusable when appropriate
- **Performance**: Optimize rendering and interactions
- **Documentation**: Document component props and usage
