---
name: react-native-web-core
description: Use when working with React Native Web projects. Provides core concepts, components, and cross-platform patterns for building web applications with React Native.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# React Native Web - Core Concepts

React Native Web enables React Native components and APIs to run on the web, providing a unified codebase for web and native platforms.

## Key Concepts

### Platform Abstraction

React Native Web provides a consistent API across web and native platforms:

```typescript
import { View, Text, StyleSheet } from 'react-native';

export function MyComponent() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Works on web and native!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: 16,
    color: '#333',
  },
});
```

### Core Components

Use React Native primitives instead of HTML elements:

- `<View>` instead of `<div>`
- `<Text>` instead of `<span>` or `<p>`
- `<Image>` instead of `<img>`
- `<TextInput>` instead of `<input>`
- `<ScrollView>` instead of scrollable `<div>`
- `<Pressable>` instead of `<button>`

### Platform-Specific Code

Use `Platform` module for platform-specific behavior:

```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    marginTop: Platform.select({
      web: 20,
      ios: 30,
      android: 25,
      default: 20,
    }),
  },
});

// Or use Platform.OS
if (Platform.OS === 'web') {
  // Web-specific code
}
```

## Best Practices

### Component Structure

✅ Use React Native primitives consistently:

```typescript
import { View, Text, Pressable } from 'react-native';

function Button({ onPress, title }: { onPress: () => void; title: string }) {
  return (
    <Pressable onPress={onPress}>
      <View style={styles.button}>
        <Text style={styles.buttonText}>{title}</Text>
      </View>
    </Pressable>
  );
}
```

### Type Safety

✅ Use TypeScript for prop types:

```typescript
import { ViewStyle, TextStyle, ImageStyle } from 'react-native';

interface Props {
  title: string;
  onPress: () => void;
  style?: ViewStyle;
  textStyle?: TextStyle;
  disabled?: boolean;
}

export function CustomButton({ title, onPress, style, textStyle, disabled }: Props) {
  // Implementation
}
```

### Accessibility

✅ Include accessibility props:

```typescript
<Pressable
  accessibilityRole="button"
  accessibilityLabel="Submit form"
  accessibilityState={{ disabled: isDisabled }}
  onPress={handleSubmit}
>
  <Text>Submit</Text>
</Pressable>
```

## Examples

### Basic Component

```typescript
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface CardProps {
  title: string;
  description: string;
}

export function Card({ title, description }: CardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: '#666',
  },
});
```

### Interactive Component with State

```typescript
import React, { useState } from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <View style={styles.container}>
      <Text style={styles.count}>{count}</Text>
      <View style={styles.buttons}>
        <Pressable style={styles.button} onPress={() => setCount(c => c - 1)}>
          <Text style={styles.buttonText}>-</Text>
        </Pressable>
        <Pressable style={styles.button} onPress={() => setCount(c => c + 1)}>
          <Text style={styles.buttonText}>+</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 20,
  },
  count: {
    fontSize: 48,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  buttons: {
    flexDirection: 'row',
    gap: 10,
  },
  button: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
});
```

## Common Patterns

### Layout with Flexbox

```typescript
const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },
  header: {
    height: 60,
    backgroundColor: '#f8f8f8',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  footer: {
    height: 50,
    backgroundColor: '#f8f8f8',
  },
});
```

### Conditional Rendering

```typescript
function UserProfile({ user }: { user?: User }) {
  if (!user) {
    return (
      <View style={styles.center}>
        <Text>Please log in</Text>
      </View>
    );
  }

  return (
    <View style={styles.profile}>
      <Text style={styles.name}>{user.name}</Text>
      <Text style={styles.email}>{user.email}</Text>
    </View>
  );
}
```

## Anti-Patterns

❌ Don't use HTML elements directly:

```typescript
// Bad
function Component() {
  return <div><span>Text</span></div>;
}

// Good
function Component() {
  return <View><Text>Text</Text></View>;
}
```

❌ Don't use CSS classes:

```typescript
// Bad
<div className="container">Content</div>

// Good
<View style={styles.container}>Content</View>
```

❌ Don't access DOM directly:

```typescript
// Bad
document.getElementById('my-element')

// Good - use refs
const ref = useRef<View>(null);
```

## Related Skills

- **react-native-web-styling**: Advanced styling patterns and responsive design
- **react-native-web-navigation**: Navigation setup and routing
- **react-native-web-performance**: Performance optimization techniques
- **react-native-web-testing**: Testing strategies for React Native Web
