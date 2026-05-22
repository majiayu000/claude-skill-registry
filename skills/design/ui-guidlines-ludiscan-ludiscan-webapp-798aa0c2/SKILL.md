---
name: ui-guidelines
description: UIコンポーネントを新規作成・編集する際に使用。Emotion styled/テーマトークン/Atomic Designのルールを確認。
---

## Overview

This skill provides comprehensive UI development guidelines for the ludiscan-webapp project. Follow these guidelines to maintain consistency, code quality, and accessibility.

## Files in This Skill

- **SKILL.md** (this file) - Core principles and quick reference
- **reference.md** - Theme tokens, z-index, and component API reference
- **patterns.md** - React best practices, TypeScript patterns, and common pitfalls
- **examples.md** - Code examples for creating components

## Core Principles

### 1. Styling System

**ALWAYS use Emotion styled components - NEVER use inline HTML tags**
- ✅ Good: `const StyledDiv = styled.div`...` or `const StyledButton = styled(Component)`...`
- ❌ Bad: `<div style={{...}}>`

**Access theme via useSharedTheme() hook**
```tsx
import { useSharedTheme } from '@src/hooks/useSharedTheme';

const Component = () => {
  const { theme } = useSharedTheme();
  return <Text color={theme.colors.text.primary} />
}
```

**Use theme tokens, not hardcoded values**
- ✅ Good: `theme.colors.**`, `theme.spacing.md`, `theme.typography.fontSize.base`
- ❌ Bad: `#C41E3A`, `16px`, `1rem`

### 2. Component Architecture (Atomic Design)

```
src/component/
  ├── atoms/         # Basic building blocks (Button, Text, Flex, etc.)
  ├── molecules/     # Simple combinations (TextField, Modal, Menu, etc.)
  ├── organisms/     # Complex components (Sidebar, Toolbar, etc.)
  └── templates/     # Page layouts
```

**When to use each level:**
- **Atoms**: Single-purpose, no internal composition (Button, Text, Divider)
- **Molecules**: 2-3 atoms combined (TextField = Text label + input, Modal = header + content + footer)
- **Organisms**: Multiple molecules or complex logic (ProjectList, HeatmapViewer controls)
- **Templates**: Full page layouts with slots for content

### 3. Component File Pattern

```tsx
import styled from '@emotion/styled';
import type { FC } from 'react';

// 1. Type definitions
export type MyComponentProps = {
  className?: string;  // Always include!
  // ... other props
};

// 2. Base component - handles logic
const Component: FC<MyComponentProps> = ({ className, ...props }) => {
  return <div className={className}>...</div>;
};

// 3. Styled wrapper - handles styling
export const MyComponent = styled(Component)`
  color: ${({ theme }) => theme.colors.text.primary};
  padding: ${({ theme }) => theme.spacing.md};
`;
```

## Quick Reference

### Common Components

| Component | Import | Usage |
|-----------|--------|-------|
| Button | `@src/component/atoms/Button` | `<Button scheme="primary" onClick={...}>` |
| Text | `@src/component/atoms/Text` | `<Text text="..." fontSize={...} color={...} />` |
| FlexRow/FlexColumn | `@src/component/atoms/Flex` | `<FlexRow gap={16} align="center">` |
| Modal | `@src/component/molecules/Modal` | `<Modal isOpen={...} onClose={...}>` |
| TextField | `@src/component/molecules/TextField` | `<TextField value={...} onChange={...} />` |

### Theme Token Categories

| Category | Access | Example |
|----------|--------|---------|
| Colors | `theme.colors.*` | `theme.colors.primary.main` |
| Typography | `theme.typography.*` | `theme.typography.fontSize.lg` |
| Spacing | `theme.spacing.*` | `theme.spacing.md` (16px) |
| Borders | `theme.borders.*` | `theme.borders.radius.md` |
| Shadows | `theme.shadows.*` | `theme.shadows.md` |

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile`, `HeatmapViewer` |
| Props Types | `ComponentNameProps` | `ButtonProps`, `ModalProps` |
| Boolean vars | `is/has/should/can` prefix | `isLoading`, `hasError` |
| Event handlers | `handle` prefix | `handleClick`, `handleSubmit` |
| Custom hooks | `use` prefix | `useAuth`, `useHeatmapData` |

## Critical Rules (Never Violate)

1. ❌ **NEVER use `any` type** - use proper types or `unknown`
2. ❌ **NEVER use `dangerouslySetInnerHTML`** - XSS vulnerability
3. ❌ **NEVER use inline styles** - use Emotion styled components
4. ❌ **NEVER hardcode colors/spacing** - use theme tokens
5. ❌ **NEVER forget `className` prop** - required for styled component compatibility
6. ❌ **NEVER overuse useEffect** - derive state during render when possible
7. ❌ **NEVER create components inside components** - define outside
8. ❌ **NEVER forget cleanup in useEffect** - prevent memory leaks

## See Also

- **reference.md** - Complete theme tokens and API reference
- **patterns.md** - React best practices and TypeScript patterns
- **examples.md** - Full code examples for new components
