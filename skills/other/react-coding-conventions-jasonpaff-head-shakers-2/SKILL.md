---
name: react-coding-conventions
description: Enforces project React coding conventions automatically when creating or modifying React components. This skill should be used proactively whenever working with .tsx/.jsx files to ensure consistent code style, naming conventions, component structure, and TypeScript patterns across the codebase.
---

# React Coding Conventions Enforcer

## Purpose

This skill enforces the project React coding conventions automatically during component development. It ensures consistent code quality, maintainable patterns, and adherence to project-specific standards for all React/TypeScript files.

## When to Use This Skill

Use this skill proactively in the following scenarios:

- Creating new React components (`.tsx` or `.jsx` files)
- Modifying existing React components
- Refactoring React code
- Reviewing or fixing React component issues
- Any task involving React/TSX file changes

**Important**: This skill should activate automatically without explicit user request whenever React component work is detected.

## How to Use This Skill

### 1. Load Conventions Reference

Before creating or modifying any React component, load the complete conventions document:

```
Read references/React-Coding-Conventions.md
```

This reference contains the authoritative coding standards including:

- Code style & formatting rules
- File organization patterns
- Component architecture guidelines
- Naming conventions
- TypeScript integration patterns
- State management approaches
- Event handling standards
- Conditional rendering rules
- Performance optimization guidelines
- Accessibility requirements

### 2. Apply Conventions During Development

When writing React code, ensure strict adherence to all conventions:

**Code Style**:

- Single quotes for all strings and imports
- JSX attributes must use curly braces with single quotes: `className={'btn-primary'}`
- Kebab-case for file names: `user-profile.tsx`
- Named exports only (no default exports)

**Component Structure**:

- Arrow function components with TypeScript interfaces
- Specific internal organization order:
  1. useState hooks
  2. Other hooks (useContext, useQuery, etc.)
  3. useMemo hooks
  4. useEffect hooks
  5. Utility functions
  6. Event handlers (prefixed with `handle`)
  7. Derived variables for conditional rendering (prefixed with `_`)

**Naming Conventions**:

- All boolean values must start with `is`: `isLoading`, `isVisible`, `isDisabled`
- Derived conditional variables must use `_` prefix: `_isDataReady`, `_hasNoResults`
- Event handlers use `handle` prefix: `handleSubmit`, `handleInputChange`
- Callback props use `on` prefix: `onSubmit`, `onInputChange`

**Conditional Rendering**:

- Use `<Conditional>` component for complex boolean conditions or multiple elements
- Use ternary operators for simple string values or single component swaps
- Extract complex conditions to meaningful `_` prefixed variable names
- Add UI block comments: `{/* Section Name */}`

**TypeScript**:

- Use `type` imports: `import type { ComponentProps } from 'react'`
- Props interfaces follow `ComponentNameProps` pattern
- Extend `ComponentPropsWithRef<'element'>` when appropriate
- Never use `any` type - use proper types, generics, or `unknown` with type narrowing

### 3. Automatic Convention Enforcement

After generating or modifying React code, immediately perform automatic validation and correction:

1. **Scan for violations**: Review the generated code against all conventions from the reference document
2. **Identify issues**: Create a mental checklist of any violations found:
   - Quote usage (strings, imports, JSX attributes)
   - Boolean naming (missing `is` prefix)
   - Derived variable naming (missing `_` prefix)
   - Component structure order
   - Conditional rendering patterns
   - Event handler naming
   - TypeScript patterns
   - Missing UI block comments

3. **Fix automatically**: Apply corrections immediately without asking for permission:
   - Correct quote usage throughout
   - Rename boolean variables to include `is` prefix
   - Rename derived variables to include `_` prefix
   - Reorder component internals to match standard structure
   - Replace inline conditions with extracted `_` variables
   - Add `{/* Section */}` comments to UI blocks
   - Convert default exports to named exports
   - Fix event handler naming
   - Improve TypeScript typing

4. **Verify completeness**: Ensure all conventions are satisfied before presenting code to user

### 4. Reporting

After automatically fixing violations, provide a brief summary:

```
✓ React conventions enforced:
  - Fixed quote usage in JSX attributes
  - Renamed boolean variables: loading → isLoading
  - Extracted derived conditions: _isFormValid
  - Reordered component hooks structure
  - Added UI section comments
```

**Do not ask for permission to apply fixes** - the skill's purpose is automatic enforcement.

## Convention Categories

The complete conventions are detailed in `references/React-Coding-Conventions.md`. Key categories include:

1. **Code Style & Formatting** - Quote usage, file naming, exports
2. **File Organization** - Folder structure, naming patterns
3. **Component Architecture** - Definition patterns, internal organization
4. **Naming Conventions** - Booleans, derived variables, functions
5. **TypeScript Integration** - Type imports, props interfaces
6. **State Management** - useState patterns, custom hooks
7. **Event Handling** - Handler naming and implementation
8. **Conditional Rendering** - Component vs ternary usage
9. **Performance Optimization** - Memoization guidelines
10. **Accessibility** - ARIA attributes, semantic HTML

## Important Notes

- **Automatic enforcement**: Apply fixes immediately without requesting permission
- **No compromises**: All conventions must be followed strictly
- **Reference first**: Always load the conventions reference before working with React code
- **Complete validation**: Check all aspects of the conventions, not just obvious violations
- **Proactive application**: Use this skill automatically when React work is detected, even if user doesn't mention conventions

## Workflow Summary

```
1. Detect React component work (create/modify .tsx/.jsx)
2. Load references/React-Coding-Conventions.md
3. Generate or modify component code following all conventions
4. Scan generated code for any violations
5. Automatically fix all violations found
6. Present corrected code to user with brief summary of fixes applied
```

This workflow ensures every React component in the project project maintains consistent, high-quality code that follows all established conventions.
