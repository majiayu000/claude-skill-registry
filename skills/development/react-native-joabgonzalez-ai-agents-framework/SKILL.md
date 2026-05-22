---
name: react-native
description: React Native mobile development patterns and best practices. Platform-specific code, navigation, native modules, performance optimization. Trigger: When developing React Native mobile apps, implementing platform-specific features, or optimizing mobile performance.
skills:
  - conventions
  - a11y
  - react
  - typescript
  - architecture-patterns
  - humanizer
dependencies:
  react-native: ">=0.70.0 <1.0.0"
  react: ">=17.0.0 <19.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# React Native Skill

## Overview

Mobile development patterns with React Native for iOS and Android applications.

## Objective

Guide developers in building cross-platform mobile apps with React Native using proper patterns and performance optimization.

---

## Extended Mandatory Read Protocol

This skill uses the **Extended Mandatory Read Protocol** for complex React Native patterns (40+ patterns total).

### Reading Strategy

1. **ALWAYS read**: This main SKILL.md (covers 80% of common React Native cases)
2. **Read references/ when**:
   - Decision Tree indicates "**MUST read** {reference}"
   - Quick Reference Table marks it "Required Reading: ✅"
   - Critical Pattern says "**[CRITICAL] See** {reference} for..."
   - Working with advanced features (navigation, animations, native modules)

### When to Read References

| Situation                            | Read SKILL.md | Read references/ | Which References                    |
| ------------------------------------ | ------------- | ---------------- | ----------------------------------- |
| Basic React Native components        | ✅ Yes        | ❌ No            | SKILL.md covers all needed patterns |
| Navigation (Stack/Tab/Drawer)        | ✅ Yes        | ✅ Yes           | navigation-patterns.md (required)   |
| Gestures, animations                 | ✅ Yes        | ✅ Yes           | gestures-animations.md (required)   |
| Platform-specific code (iOS/Android) | ✅ Yes        | ✅ Yes           | platform-specific.md (required)     |
| Performance optimization             | ✅ Yes        | ✅ Yes           | performance-rn.md (required)        |
| Native modules integration           | ✅ Yes        | ✅ Yes           | native-modules.md (required)        |
| Multiple advanced features           | ✅ Yes        | ✅ Yes           | All relevant references             |

### Available References

All reference files located in `skills/react-native/references/`:

- **README.md**: Overview of all React Native references and navigation guide
- **navigation-patterns.md**: React Navigation Stack/Tab/Drawer, deep linking (required for navigation)
- **gestures-animations.md**: Gesture Handler, Animated API, Reanimated (required for animations)
- **platform-specific.md**: Platform.select, iOS/Android differences (required for platform code)
- **performance-rn.md**: FlatList optimization, memory management (required for optimization)
- **native-modules.md**: Linking native code, bridges (required for native integration)

### Conditional Language

- **"MUST read"** → **Obligatory** - Read immediately before proceeding
- **"CHECK"** or "Consider" → **Suggested** - Read if you need deeper understanding
- **"OPTIONAL"** → **Ignorable** - Read only for learning or edge cases

### Example: Navigation Task

```
1. User: "Set up Stack and Tab navigation"
2. Read: skills/react-native/SKILL.md (this file)
3. Check Decision Tree: "Navigation? → MUST read navigation-patterns.md"
4. Read: skills/react-native/references/navigation-patterns.md (REQUIRED)
5. Execute: Implement Stack and Tab navigators with React Navigation
```

---

## When to Use

Use this skill when:

- Building cross-platform mobile apps (iOS + Android)
- Using bare React Native (not Expo managed workflow)
- Implementing platform-specific features
- Optimizing mobile performance
- Integrating native modules

Don't use this skill for:

- Expo managed workflow (use expo skill)
- Web-only React apps (use react skill)
- Native iOS/Android development

---

## Critical Patterns

### ✅ REQUIRED: Use FlatList for Lists

```typescript
// ✅ CORRECT: Virtualized list
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <Item data={item} />}
/>

// ❌ WRONG: ScrollView with map (memory issues)
<ScrollView>
  {items.map(item => <Item key={item.id} data={item} />)}
</ScrollView>
```

### ✅ REQUIRED: Use Platform-Specific Code

```typescript
// ✅ CORRECT: Platform.select or Platform.OS
import { Platform } from "react-native";

const styles = StyleSheet.create({
  container: {
    padding: Platform.select({ ios: 10, android: 8 }),
  },
});

// Or separate files: Component.ios.tsx, Component.android.tsx
```

### ✅ REQUIRED: Handle Safe Areas

```typescript
// ✅ CORRECT: SafeAreaView
import { SafeAreaView } from 'react-native-safe-area-context';

<SafeAreaView>
  <App />
</SafeAreaView>

// ❌ WRONG: No safe area handling (notch issues)
<View>
  <App />
</View>
```

### ✅ REQUIRED: Optimize Images

```typescript
// ✅ CORRECT: Specify dimensions, use FastImage for remote images
<Image
  source={{ uri: url }}
  style={{ width: 200, height: 200 }}
  resizeMode="cover"
/>

// ❌ WRONG: No dimensions (layout thrashing)
<Image source={{ uri: url }} />
```

---

## Conventions

Refer to conventions for:

- Code organization

Refer to a11y for:

- Accessibility labels
- Screen reader support

Refer to react for:

- Component patterns
- Hooks usage

### React Native Specific

- Use Platform-specific code when necessary
- Implement proper list virtualization with FlatList
- Handle safe areas properly
- Optimize images and assets
- Use Hermes engine for better performance

---

## Decision Tree

**Long list?** → Use `FlatList` with `keyExtractor` and `getItemLayout` for optimization. **[CRITICAL] See** `references/performance-rn.md` for FlatList optimization.

**Platform-specific styling?** → Use `Platform.select()` or `Platform.OS === 'ios'`. **[CRITICAL] See** `references/platform-specific.md` for platform patterns.

**Navigation?** → Use React Navigation library. **[CRITICAL] See** `references/navigation-patterns.md` for Stack/Tab/Drawer setup.

**Gestures/Animations?** → Use Gesture Handler + Reanimated. **[CRITICAL] See** `references/gestures-animations.md` for gesture and animation patterns.

**Forms?** → Use controlled components, consider `react-hook-form` for complex forms.

**State management?** → Context for simple, Redux/Zustand for complex.

**Native feature needed?** → Check if React Native API exists, otherwise use native module or library. **[CRITICAL] See** `references/native-modules.md` for native integration.

**Performance issue?** → Enable Hermes, use `React.memo()`, avoid inline functions in renders, profile with Flipper. **[CRITICAL] See** `references/performance-rn.md` for optimization strategies.

**Testing?** → Use Jest + React Native Testing Library, test on real devices.

---

## Example

```typescript
import { View, Text, FlatList, Platform } from 'react-native';

const MyList = ({ items }) => (
  <FlatList
    data={items}
    keyExtractor={(item) => item.id}
    renderItem={({ item }) => (
      <View style={{ padding: Platform.OS === 'ios' ? 10 : 8 }}>
        <Text>{item.name}</Text>
      </View>
    )}
  />
);
```

---

## Advanced Architecture Patterns

**⚠️ Context Check**: Architecture patterns apply to React Native the same way as React. Mobile apps with business logic benefit from architecture patterns.

### When to Apply

- **AGENTS.md mentions architecture**: Project specifies "Clean Architecture", "SOLID", "DDD"
- **Enterprise mobile apps**: Banking, healthcare, fintech, ERP apps
- **Complex business logic**: Authentication, payments, offline sync, data transformations
- **Large teams**: >10 developers requiring consistent structure

### When NOT to Apply

- Simple apps (content display, basic forms)
- Prototypes or MVPs
- No mention in AGENTS.md

### Architecture Integration

**React Native uses same patterns as React**:

- **SOLID Principles** → Service classes, custom hooks, components
- **Clean Architecture** → `domain/`, `application/`, `infrastructure/`, `mobile/` (presentation)
- **Result Pattern** → Async operations, API calls, local storage
- **DIP** → Abstract services (API, storage, permissions) with adapters

**Mobile-specific architecture**:

```typescript
// domain/entities/User.ts (same as web)
export class User {
  constructor(
    public readonly id: string,
    public readonly email: string
  ) {}
}

// infrastructure/services/SecureStorageService.ts (mobile adapter)
export class SecureStorageService implements IStorageService {
  async save(key: string, value: string): Promise<Result<void>> {
    try {
      await SecureStore.setItemAsync(key, value); // Expo SecureStore
      return Result.ok(undefined);
    } catch (error) {
      return Result.fail('Storage error');
    }
  }
}

// mobile/screens/LoginScreen.tsx (presentation)
const LoginScreen = () => {
  const { execute, result } = useLoginUser(); // Clean Architecture use case

  return (
    <View>
      <TextInput onChangeText={setEmail} />
      <Button onPress={() => execute(email, password)} title="Login" />
      {result && !result.isSuccess && <Text>{result.error}</Text>}
    </View>
  );
};
```

### For Complete Guide

**MUST read** [architecture-patterns/references/frontend-integration.md](../architecture-patterns/references/frontend-integration.md) - React Native uses same patterns as React.

**Also see**: [architecture-patterns/SKILL.md](../architecture-patterns/SKILL.md) for pattern selection.

---

## Edge Cases

**Keyboard handling:** Use `KeyboardAvoidingView` or `react-native-keyboard-aware-scroll-view`.

**Android back button:** Handle with `BackHandler` API, especially for modals.

**Permissions:** Request runtime permissions on Android 6+, handle denied state gracefully.

**Deep linking:** Configure URL schemes for both iOS and Android, handle different app states.

**Offline support:** Use `NetInfo` to detect connectivity, queue operations when offline.

**Bundle size:** Use Hermes, enable ProGuard on Android, analyze bundle with Metro.

**Debugging:** Use Flipper for network/Redux inspection, React DevTools, Chrome debugger.

---

## References

- https://reactnative.dev/docs/getting-started
- https://reactnative.dev/docs/performance
