---
name: theone-react-native-standards
description: Enforces TheOne Studio React Native development standards including TypeScript patterns, React/Hooks best practices, React Native architecture (Zustand/Jotai, Expo Router), and mobile performance optimization. Triggers when writing, reviewing, or refactoring React Native code, implementing mobile features, working with state management/navigation, or reviewing pull requests.
---

# TheOne Studio React Native Development Standards

⚠️ **React Native Latest + TypeScript:** All patterns use latest React Native with TypeScript strict mode, Expo SDK 51+, and modern React 18+ patterns.

## Skill Purpose

This skill enforces TheOne Studio's comprehensive React Native development standards with **CODE QUALITY FIRST**:

**Priority 1: Code Quality & Hygiene** (MOST IMPORTANT)
- TypeScript strict mode, ESLint + Prettier enforcement
- Path aliases (@/), throw errors (never suppress), structured logging
- No any types, proper error boundaries, consistent imports
- File naming conventions, no inline styles in JSX

**Priority 2: Modern React & TypeScript**
- Functional components with Hooks (NO class components)
- Custom hooks for logic reuse, proper memoization
- Type-safe props, generics, discriminated unions
- useCallback/useMemo for performance

**Priority 3: React Native Architecture**
- Zustand/Jotai for state (document both, require consistency per project)
- Expo Router (file-based) OR React Navigation 7
- FlatList optimization (NEVER ScrollView + map)
- Platform-specific code (.ios.tsx/.android.tsx)

**Priority 4: Mobile Performance**
- List rendering optimization (getItemLayout, keyExtractor)
- Prevent unnecessary rerenders (React.memo, shouldComponentUpdate)
- Lazy loading, code splitting, bundle optimization
- Memory leak prevention (cleanup effects)

## When This Skill Triggers

- Writing or refactoring React Native TypeScript code
- Implementing mobile UI components or features
- Working with state management (Zustand/Jotai)
- Implementing navigation flows (Expo Router/React Navigation)
- Optimizing list rendering or app performance
- Reviewing React Native pull requests
- Setting up project architecture or conventions

## Quick Reference Guide

### What Do You Need Help With?

| Priority | Task | Reference |
|----------|------|-----------|
| **🔴 PRIORITY 1: Code Quality (Check FIRST)** | | |
| 1 | TypeScript strict, ESLint, Prettier, no any types | [Quality & Hygiene](references/language/quality-hygiene.md) ⭐ |
| 1 | Path aliases (@/), structured logging, error handling | [Quality & Hygiene](references/language/quality-hygiene.md) ⭐ |
| 1 | File naming, no inline styles, consistent imports | [Quality & Hygiene](references/language/quality-hygiene.md) ⭐ |
| **🟡 PRIORITY 2: Modern React/TypeScript** | | |
| 2 | Functional components, Hooks rules, custom hooks | [Modern React](references/language/modern-react.md) |
| 2 | useCallback, useMemo, React.memo optimization | [Modern React](references/language/modern-react.md) |
| 2 | Type-safe props, generics, utility types | [TypeScript Patterns](references/language/typescript-patterns.md) |
| 2 | Discriminated unions, type guards, inference | [TypeScript Patterns](references/language/typescript-patterns.md) |
| **🟢 PRIORITY 3: React Native Architecture** | | |
| 3 | Functional components, composition, HOCs | [Component Patterns](references/framework/component-patterns.md) |
| 3 | Zustand patterns, Jotai atoms, persistence | [State Management](references/framework/state-management.md) |
| 3 | Expo Router (file-based), React Navigation setup | [Navigation](references/framework/navigation-patterns.md) |
| 3 | Platform checks, .ios/.android files, Platform module | [Platform-Specific](references/framework/platform-specific.md) |
| **🔵 PRIORITY 4: Performance** | | |
| 4 | FlatList optimization, getItemLayout, keyExtractor | [Performance](references/framework/performance-patterns.md) |
| 4 | Rerender prevention, React.memo, useMemo | [Performance](references/framework/performance-patterns.md) |
| 4 | Architecture violations (components, state, navigation) | [Architecture Review](references/review/architecture-review.md) |
| 4 | TypeScript quality, hooks violations, ESLint | [Quality Review](references/review/quality-review.md) |
| 4 | List optimization, memory leaks, unnecessary rerenders | [Performance Review](references/review/performance-review.md) |

## 🔴 CRITICAL: Code Quality Rules (CHECK FIRST!)

### ⚠️ MANDATORY QUALITY STANDARDS

**ALWAYS enforce these BEFORE writing any code:**

1. **TypeScript strict mode** - Enable all strict compiler options
2. **ESLint + Prettier** - Enforce linting and formatting
3. **No any types** - Use proper types or unknown
4. **Path aliases** - Use @/ for src/ imports
5. **Throw errors** - NEVER suppress errors with try/catch + console.log
6. **Structured logging** - Use logger utility, not raw console.log
7. **Error boundaries** - Wrap components with ErrorBoundary
8. **Consistent imports** - React first, then libraries, then local
9. **File naming** - kebab-case for files, PascalCase for components
10. **No inline styles in JSX** - Define styles outside component or use StyleSheet

**Example: Enforce Quality First**

```typescript
// ✅ EXCELLENT: All quality rules enforced

// 1. TypeScript strict mode in tsconfig.json
// {
//   "compilerOptions": {
//     "strict": true,
//     "noImplicitAny": true,
//     "strictNullChecks": true
//   }
// }

// 2. Import order: React → libraries → local
import React, { useCallback, useMemo } from 'react'; // React first
import { View, Text, StyleSheet } from 'react-native'; // Libraries
import { useStore } from '@/stores/user-store'; // Local with path alias

// 3. Type-safe props (no any)
interface UserProfileProps {
  userId: string;
  onPress?: () => void;
}

// 4. Functional component with typed props
export const UserProfile: React.FC<UserProfileProps> = ({ userId, onPress }) => {
  const user = useStore((state) => state.users[userId]);

  // 5. Throw errors (not console.log)
  if (!user) {
    throw new Error(`User not found: ${userId}`);
  }

  // 6. Structured logging
  const handlePress = useCallback(() => {
    logger.info('User profile pressed', { userId });
    onPress?.();
  }, [userId, onPress]);

  return (
    <View style={styles.container}>
      <Text style={styles.name}>{user.name}</Text>
    </View>
  );
};

// 7. No inline styles - use StyleSheet
const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  name: {
    fontSize: 18,
    fontWeight: 'bold',
  },
});
```

## ⚠️ React Native Architecture Rules (AFTER Quality)

### Choose Consistent State Management

**Choose ONE state management solution per project:**

**Option 1: Zustand (Recommended for Simple State)**
- ✅ Minimal boilerplate, hooks-based
- ✅ Perfect for app-level state (user, settings)
- ✅ Easy to test, TypeScript-friendly

**Option 2: Jotai (Recommended for Atomic State)**
- ✅ Atomic state management
- ✅ Perfect for complex derived state
- ✅ Better for fine-grained reactivity

**Universal Rules (Both Solutions):**
- ✅ Use selectors to prevent unnecessary rerenders
- ✅ Keep state normalized (no nested objects)
- ✅ Persist state with async storage adapters
- ✅ NEVER use Redux (too much boilerplate)

### Choose ONE Navigation Solution

**Option 1: Expo Router (Recommended)**
- ✅ File-based routing (app/ directory)
- ✅ Built-in TypeScript support
- ✅ Automatic deep linking

**Option 2: React Navigation 7**
- ✅ More control over navigation structure
- ✅ Better for complex navigation flows
- ✅ Proven stability

### ALWAYS Use FlatList for Lists

**NEVER use ScrollView + map for lists:**

```typescript
// ❌ BAD: ScrollView + map (terrible performance)
<ScrollView>
  {items.map(item => <Item key={item.id} {...item} />)}
</ScrollView>

// ✅ GOOD: FlatList with proper optimization
<FlatList
  data={items}
  renderItem={({ item }) => <Item {...item} />}
  keyExtractor={(item) => item.id}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  removeClippedSubviews
  maxToRenderPerBatch={10}
  windowSize={11}
/>
```

## Quick Examples: ❌ BAD vs ✅ GOOD

### Example 1: Component Structure

```typescript
// ❌ BAD: Class component, inline styles, no types
class UserCard extends React.Component {
  render() {
    return (
      <View style={{ padding: 10 }}>
        <Text>{this.props.name}</Text>
      </View>
    );
  }
}

// ✅ GOOD: Functional component, typed props, StyleSheet
interface UserCardProps {
  name: string;
  onPress?: () => void;
}

export const UserCard: React.FC<UserCardProps> = ({ name, onPress }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.name}>{name}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { padding: 10 },
  name: { fontSize: 16 },
});
```

### Example 2: State Management

```typescript
// ❌ BAD: useState for app-level state
function App() {
  const [user, setUser] = useState(null);
  const [settings, setSettings] = useState({});

  return <AppContent user={user} settings={settings} />;
}

// ✅ GOOD: Zustand for app-level state
import { create } from 'zustand';

interface AppState {
  user: User | null;
  settings: Settings;
  setUser: (user: User | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  settings: {},
  setUser: (user) => set({ user }),
}));

function App() {
  const user = useAppStore((state) => state.user);
  return <AppContent />;
}
```

### Example 3: List Rendering

```typescript
// ❌ BAD: ScrollView + map
<ScrollView>
  {users.map(user => (
    <UserCard key={user.id} user={user} />
  ))}
</ScrollView>

// ✅ GOOD: FlatList with optimization
const ITEM_HEIGHT = 80;

<FlatList
  data={users}
  renderItem={({ item }) => <UserCard user={item} />}
  keyExtractor={(item) => item.id}
  getItemLayout={(_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

## Common Mistakes to Avoid

### 🔴 Critical Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Using class components | Outdated, verbose, no hooks | Use functional components |
| Using `any` type | Defeats TypeScript safety | Use proper types or `unknown` |
| Inline styles in JSX | Poor performance, not reusable | Use `StyleSheet.create()` |
| ScrollView + map for long lists | Memory issues, poor performance | Use `FlatList` with optimization |
| Direct console.log | Not structured, no filtering | Use logger utility |

### 🟡 Warning-Level Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Not using path aliases | Ugly relative imports | Configure @/ alias |
| Missing keyExtractor | Poor list performance | Always provide keyExtractor |
| Not memoizing callbacks | Causes unnecessary rerenders | Use `useCallback` |
| Platform checks in render | Duplicated logic | Use Platform-specific files |
| Not cleaning up effects | Memory leaks | Return cleanup function |

### 🟢 Optimization Opportunities

| Pattern | Issue | Optimization |
|---------|-------|--------------|
| Expensive calculations in render | Recalculates every render | Use `useMemo` |
| Props causing child rerenders | Child rerenders unnecessarily | Use `React.memo` |
| Large lists without optimization | Slow scrolling | Add `getItemLayout` |
| Deep object comparisons | Expensive checks | Use shallow equality |
| Large bundles | Slow app startup | Code splitting, lazy loading |

## Code Review Checklist

Use this checklist when reviewing React Native code:

### 🔴 Critical Issues (Block Merge)

- [ ] TypeScript strict mode enabled
- [ ] No `any` types used
- [ ] ESLint + Prettier passing
- [ ] Path aliases (@/) configured and used
- [ ] Errors are thrown (not suppressed)
- [ ] Error boundaries wrap components
- [ ] FlatList used for lists (not ScrollView + map)
- [ ] File naming follows conventions (kebab-case)

### 🟡 Important Issues (Request Changes)

- [ ] Functional components used (no class components)
- [ ] Props are properly typed
- [ ] Hooks rules followed (no conditionals, no loops)
- [ ] useCallback/useMemo used appropriately
- [ ] Styles use StyleSheet (no inline styles)
- [ ] State management is consistent (Zustand OR Jotai)
- [ ] Navigation is consistent (Expo Router OR React Navigation)
- [ ] Platform-specific code properly handled

### 🟢 Suggestions (Non-Blocking)

- [ ] Custom hooks extract reusable logic
- [ ] React.memo used for expensive components
- [ ] getItemLayout provided for FlatList
- [ ] Effect cleanup functions provided
- [ ] Code splitting for large screens
- [ ] Images optimized and lazy loaded
- [ ] Accessibility props added (accessibilityLabel)

## Framework Versions

**Recommended Stack:**
- React Native: 0.74+ (latest stable)
- Expo SDK: 51+ (if using Expo)
- TypeScript: 5.4+
- React: 18.2+
- Zustand: 4.5+ OR Jotai: 2.8+
- Expo Router: 3.5+ OR React Navigation: 7+

**Development Tools:**
- ESLint: 8.57+ with @react-native-community plugin
- Prettier: 3.2+
- Metro bundler (built-in)
- React DevTools: Latest

## Reference Files Structure

All detailed patterns and examples are in reference files:

### Language Patterns (TypeScript + React)
- **[Quality & Hygiene](references/language/quality-hygiene.md)** - TypeScript strict, ESLint, path aliases, error handling
- **[Modern React](references/language/modern-react.md)** - Hooks, functional components, memoization
- **[TypeScript Patterns](references/language/typescript-patterns.md)** - Type-safe props, generics, utility types

### Framework Patterns (React Native)
- **[Component Patterns](references/framework/component-patterns.md)** - Functional components, composition, HOCs
- **[State Management](references/framework/state-management.md)** - Zustand, Jotai, persistence
- **[Navigation Patterns](references/framework/navigation-patterns.md)** - Expo Router, React Navigation, deep linking
- **[Platform-Specific](references/framework/platform-specific.md)** - iOS/Android differences, platform files
- **[Performance Patterns](references/framework/performance-patterns.md)** - FlatList optimization, rerender prevention

### Code Review Guidelines
- **[Architecture Review](references/review/architecture-review.md)** - Component violations, state issues
- **[Quality Review](references/review/quality-review.md)** - TypeScript quality, hooks violations
- **[Performance Review](references/review/performance-review.md)** - List optimization, memory leaks
