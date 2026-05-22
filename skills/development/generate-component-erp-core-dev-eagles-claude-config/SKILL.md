---
name: generate-component
description: Generate React component with TypeScript, tests, and styles
argument-hint: "<component-name> [--type=page|form|list|detail]"
tags: [codegen, react, frontend, component]
user-invocable: true
---

# Generate React Component

Generate a typed React component with Ant Design, Redux integration, and tests.

## What To Do

1. **Generate component file** with proper TypeScript types
2. **Generate test file** using React Testing Library
3. **Add Redux slice** if stateful component
4. **Register route** if page component

## Component Types
- `page`: Full page with layout, breadcrumb, data fetching
- `form`: Ant Design Form with validation, submit handler
- `list`: Table with pagination, search, filters
- `detail`: Detail view with tabs and action buttons

## Arguments
- `<component-name>`: Component name in PascalCase
- `--type=<page|form|list|detail>`: Component template