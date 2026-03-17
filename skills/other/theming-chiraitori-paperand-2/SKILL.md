---
name: Theming System
description: Theme management with dark mode and custom .pbcolors themes
---

# Theming System

## Theme Context

```typescript
import { useTheme } from '../context/ThemeContext';

function MyComponent() {
  const { colors, isDark, setTheme } = useTheme();

  return (
    <View style={{ backgroundColor: colors.background }}>
      <Text style={{ color: colors.text }}>Hello</Text>
    </View>
  );
}
```

## Color Palette

| Color Key | Light | Dark | Usage |
|-----------|-------|------|-------|
| `background` | #FFFFFF | #1a1a2e | Screen background |
| `card` | #F5F5F5 | #2d2d44 | Cards, modals |
| `text` | #000000 | #FFFFFF | Primary text |
| `textSecondary` | #666666 | #AAAAAA | Secondary text |
| `primary` | #FA6432 | #FA6432 | Accent color |
| `border` | #E0E0E0 | #404040 | Borders, separators |

## Theme Provider Setup

```typescript
// App.tsx
import { ThemeProvider } from './src/context/ThemeContext';

export default function App() {
  return (
    <ThemeProvider>
      <NavigationContainer>
        <AppNavigator />
      </NavigationContainer>
    </ThemeProvider>
  );
}
```

## Styled Components Pattern

```typescript
function Card({ children }) {
  const { colors } = useTheme();

  return (
    <View style={[
      styles.card,
      { backgroundColor: colors.card, borderColor: colors.border }
    ]}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
  },
});
```

## .pbcolors Theme Format

Paperback theme files (`.pbcolors`) are parsed by `themeService.ts`:

```typescript
interface PBColors {
  primary: string;
  background: string;
  card: string;
  text: string;
  // ... other colors
}

// Import custom theme
import { parseThemeFile } from '../services/themeService';

const customTheme = await parseThemeFile(fileUri);
setTheme(customTheme);
```

## System Theme Detection

```typescript
import { useColorScheme } from 'react-native';

function ThemeProvider({ children }) {
  const systemScheme = useColorScheme(); // 'light' | 'dark'
  const [userPreference, setUserPreference] = useState('system');

  const isDark = userPreference === 'system' 
    ? systemScheme === 'dark'
    : userPreference === 'dark';

  const colors = isDark ? darkColors : lightColors;

  return (
    <ThemeContext.Provider value={{ colors, isDark, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

## Status Bar

```typescript
import { StatusBar } from 'expo-status-bar';

function App() {
  const { isDark } = useTheme();

  return (
    <>
      <StatusBar style={isDark ? 'light' : 'dark'} />
      {/* App content */}
    </>
  );
}
```

## Navigation Theme

```typescript
import { NavigationContainer, DefaultTheme, DarkTheme } from '@react-navigation/native';

function App() {
  const { colors, isDark } = useTheme();

  const navTheme = {
    ...(isDark ? DarkTheme : DefaultTheme),
    colors: {
      ...(isDark ? DarkTheme.colors : DefaultTheme.colors),
      background: colors.background,
      card: colors.card,
      primary: colors.primary,
      text: colors.text,
      border: colors.border,
    },
  };

  return (
    <NavigationContainer theme={navTheme}>
      <AppNavigator />
    </NavigationContainer>
  );
}
```
