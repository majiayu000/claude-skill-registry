---
name: gluestack-theming
description: Use when customizing gluestack-ui themes and design tokens. Covers theme provider setup, design tokens, dark mode, NativeWind integration, and extending themes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# gluestack-ui - Theming

Expert knowledge of gluestack-ui's theming system, design tokens, and NativeWind integration for creating consistent, customizable UI across React and React Native.

## Overview

gluestack-ui uses NativeWind (Tailwind CSS for React Native) for styling. The theming system provides design tokens, dark mode support, and customization through Tailwind configuration.

## Key Concepts

### Configuration File

gluestack-ui projects use `gluestack-ui.config.json` at the project root:

```json
{
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "global.css"
  },
  "components": {
    "path": "components/ui"
  },
  "typescript": true,
  "framework": "expo"
}
```

### Theme Provider Setup

Wrap your application with the GluestackUIProvider:

```tsx
// App.tsx
import { GluestackUIProvider } from '@/components/ui/gluestack-ui-provider';
import { config } from '@/components/ui/gluestack-ui-provider/config';

export default function App() {
  return (
    <GluestackUIProvider config={config}>
      <YourApp />
    </GluestackUIProvider>
  );
}
```

For dark mode support:

```tsx
import { useColorScheme } from 'react-native';
import { GluestackUIProvider } from '@/components/ui/gluestack-ui-provider';

export default function App() {
  const colorScheme = useColorScheme();

  return (
    <GluestackUIProvider mode={colorScheme === 'dark' ? 'dark' : 'light'}>
      <YourApp />
    </GluestackUIProvider>
  );
}
```

### NativeWind Configuration

Configure Tailwind CSS via `tailwind.config.js`:

```javascript
// tailwind.config.js
const { theme } = require('@gluestack-ui/nativewind-utils/theme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,jsx,ts,tsx}',
    './components/**/*.{js,jsx,ts,tsx}',
  ],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: theme.colors,
      fontFamily: theme.fontFamily,
      fontSize: theme.fontSize,
      borderRadius: theme.borderRadius,
      boxShadow: theme.boxShadow,
    },
  },
  plugins: [],
};
```

## Design Tokens

### Color Tokens

gluestack-ui provides semantic color tokens:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Primary colors
        primary: {
          0: '#E5F4FF',
          50: '#CCE9FF',
          100: '#B3DEFF',
          200: '#80C8FF',
          300: '#4DB3FF',
          400: '#1A9DFF',
          500: '#0077E6',
          600: '#005CB3',
          700: '#004080',
          800: '#00264D',
          900: '#000D1A',
          950: '#00060D',
        },
        // Secondary colors
        secondary: {
          0: '#F5F5F5',
          50: '#E6E6E6',
          // ... more shades
        },
        // Semantic colors
        success: {
          50: '#ECFDF5',
          500: '#22C55E',
          700: '#15803D',
        },
        warning: {
          50: '#FFFBEB',
          500: '#F59E0B',
          700: '#B45309',
        },
        error: {
          50: '#FEF2F2',
          500: '#EF4444',
          700: '#B91C1C',
        },
        info: {
          50: '#EFF6FF',
          500: '#3B82F6',
          700: '#1D4ED8',
        },
        // Typography colors
        typography: {
          0: '#FFFFFF',
          50: '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          900: '#111827',
          950: '#030712',
        },
        // Background colors
        background: {
          0: '#FFFFFF',
          50: '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          // Dark mode variants
          dark: '#0F172A',
        },
        // Outline/border colors
        outline: {
          0: '#FFFFFF',
          50: '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
        },
      },
    },
  },
};
```

### Typography Tokens

Configure font families and sizes:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        heading: ['Inter-Bold', 'sans-serif'],
        body: ['Inter-Regular', 'sans-serif'],
        mono: ['JetBrainsMono-Regular', 'monospace'],
      },
      fontSize: {
        '2xs': ['10px', { lineHeight: '14px' }],
        xs: ['12px', { lineHeight: '16px' }],
        sm: ['14px', { lineHeight: '20px' }],
        md: ['16px', { lineHeight: '24px' }],
        lg: ['18px', { lineHeight: '28px' }],
        xl: ['20px', { lineHeight: '28px' }],
        '2xl': ['24px', { lineHeight: '32px' }],
        '3xl': ['30px', { lineHeight: '36px' }],
        '4xl': ['36px', { lineHeight: '40px' }],
        '5xl': ['48px', { lineHeight: '1' }],
        '6xl': ['60px', { lineHeight: '1' }],
      },
    },
  },
};
```

### Spacing and Sizing

Consistent spacing scale:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        px: '1px',
        0: '0px',
        0.5: '2px',
        1: '4px',
        1.5: '6px',
        2: '8px',
        2.5: '10px',
        3: '12px',
        3.5: '14px',
        4: '16px',
        5: '20px',
        6: '24px',
        7: '28px',
        8: '32px',
        9: '36px',
        10: '40px',
        11: '44px',
        12: '48px',
        14: '56px',
        16: '64px',
        20: '80px',
        24: '96px',
        28: '112px',
        32: '128px',
      },
      borderRadius: {
        none: '0px',
        sm: '2px',
        DEFAULT: '4px',
        md: '6px',
        lg: '8px',
        xl: '12px',
        '2xl': '16px',
        '3xl': '24px',
        full: '9999px',
      },
    },
  },
};
```

## Dark Mode

### Automatic Dark Mode

Use system color scheme:

```tsx
import { useColorScheme } from 'react-native';
import { GluestackUIProvider } from '@/components/ui/gluestack-ui-provider';

function App() {
  const colorScheme = useColorScheme();

  return (
    <GluestackUIProvider mode={colorScheme === 'dark' ? 'dark' : 'light'}>
      <MainApp />
    </GluestackUIProvider>
  );
}
```

### Manual Dark Mode Toggle

Create a theme context for manual control:

```tsx
// contexts/ThemeContext.tsx
import { createContext, useContext, useState, useEffect } from 'react';
import { useColorScheme } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

type ThemeMode = 'light' | 'dark' | 'system';

interface ThemeContextType {
  mode: ThemeMode;
  resolvedMode: 'light' | 'dark';
  setMode: (mode: ThemeMode) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const systemColorScheme = useColorScheme();
  const [mode, setModeState] = useState<ThemeMode>('system');

  useEffect(() => {
    AsyncStorage.getItem('theme-mode').then((stored) => {
      if (stored) setModeState(stored as ThemeMode);
    });
  }, []);

  const setMode = (newMode: ThemeMode) => {
    setModeState(newMode);
    AsyncStorage.setItem('theme-mode', newMode);
  };

  const resolvedMode: 'light' | 'dark' =
    mode === 'system' ? (systemColorScheme ?? 'light') : mode;

  return (
    <ThemeContext.Provider value={{ mode, resolvedMode, setMode }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

Usage in App:

```tsx
// App.tsx
import { ThemeProvider, useTheme } from '@/contexts/ThemeContext';
import { GluestackUIProvider } from '@/components/ui/gluestack-ui-provider';

function ThemedApp() {
  const { resolvedMode } = useTheme();

  return (
    <GluestackUIProvider mode={resolvedMode}>
      <MainApp />
    </GluestackUIProvider>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <ThemedApp />
    </ThemeProvider>
  );
}
```

### Dark Mode Styling

Use dark: prefix for dark mode styles:

```tsx
<Box className="bg-background-0 dark:bg-background-dark">
  <Text className="text-typography-900 dark:text-typography-50">
    Hello World
  </Text>
</Box>
```

## Best Practices

### 1. Use Semantic Color Tokens

Use semantic tokens instead of literal colors:

```tsx
// Good: Semantic tokens
<Box className="bg-background-0 dark:bg-background-dark">
  <Text className="text-typography-900 dark:text-typography-0">Content</Text>
  <Button action="primary">
    <ButtonText>Action</ButtonText>
  </Button>
</Box>

// Avoid: Literal colors
<Box className="bg-white dark:bg-slate-900">
  <Text className="text-gray-900 dark:text-white">Content</Text>
</Box>
```

### 2. Create a Design System File

Centralize design decisions:

```typescript
// design-system/tokens.ts
export const tokens = {
  colors: {
    brand: {
      primary: 'primary-500',
      secondary: 'secondary-500',
      accent: 'info-500',
    },
    feedback: {
      success: 'success-500',
      warning: 'warning-500',
      error: 'error-500',
    },
  },
  spacing: {
    page: 'px-4 py-6',
    section: 'py-8',
    card: 'p-4',
  },
  radius: {
    card: 'rounded-xl',
    button: 'rounded-lg',
    input: 'rounded-md',
  },
} as const;

// Usage
import { tokens } from '@/design-system/tokens';

<Box className={`bg-${tokens.colors.brand.primary} ${tokens.spacing.card} ${tokens.radius.card}`}>
```

### 3. Extend Theme Properly

Extend rather than override the base theme:

```javascript
// tailwind.config.js
const { theme: gluestackTheme } = require('@gluestack-ui/nativewind-utils/theme');

module.exports = {
  theme: {
    extend: {
      // Extend colors, don't replace
      colors: {
        ...gluestackTheme.colors,
        // Add brand colors
        brand: {
          50: '#FFF5F7',
          100: '#FFEAEF',
          500: '#FF1493',
          600: '#DB1086',
          700: '#B80D6E',
        },
      },
    },
  },
};
```

### 4. Create Reusable Style Utilities

Build consistent style helpers:

```typescript
// utils/styles.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Card styles
export const cardStyles = cn(
  'bg-background-0 dark:bg-background-100',
  'border border-outline-200 dark:border-outline-700',
  'rounded-xl',
  'p-4'
);

// Interactive states
export const interactiveStyles = cn(
  'active:opacity-80',
  'focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
);
```

### 5. Handle Platform-Specific Theming

Account for platform differences:

```tsx
import { Platform } from 'react-native';

// Platform-specific shadows
const shadowClass = Platform.select({
  ios: 'shadow-md',
  android: 'elevation-4',
  web: 'shadow-lg',
});

<Box className={cn('bg-background-0 rounded-xl', shadowClass)}>
  <Text>Card content</Text>
</Box>
```

## Examples

### Custom Theme Configuration

Complete custom theme setup:

```javascript
// tailwind.config.js
const { theme: gluestackTheme } = require('@gluestack-ui/nativewind-utils/theme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,jsx,ts,tsx}',
    './components/**/*.{js,jsx,ts,tsx}',
  ],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        ...gluestackTheme.colors,
        // Custom brand palette
        brand: {
          50: '#F0F9FF',
          100: '#E0F2FE',
          200: '#BAE6FD',
          300: '#7DD3FC',
          400: '#38BDF8',
          500: '#0EA5E9',
          600: '#0284C7',
          700: '#0369A1',
          800: '#075985',
          900: '#0C4A6E',
          950: '#082F49',
        },
        // Override primary to use brand
        primary: {
          50: '#F0F9FF',
          100: '#E0F2FE',
          200: '#BAE6FD',
          300: '#7DD3FC',
          400: '#38BDF8',
          500: '#0EA5E9',
          600: '#0284C7',
          700: '#0369A1',
          800: '#075985',
          900: '#0C4A6E',
          950: '#082F49',
        },
      },
      fontFamily: {
        heading: ['Poppins-Bold', 'sans-serif'],
        body: ['Poppins-Regular', 'sans-serif'],
        mono: ['FiraCode-Regular', 'monospace'],
      },
      borderRadius: {
        ...gluestackTheme.borderRadius,
        card: '16px',
        button: '12px',
      },
    },
  },
  plugins: [],
};
```

### Theme Switcher Component

```tsx
import { useState } from 'react';
import { HStack } from '@/components/ui/hstack';
import { Button, ButtonText, ButtonIcon } from '@/components/ui/button';
import { SunIcon, MoonIcon, MonitorIcon } from 'lucide-react-native';
import { useTheme } from '@/contexts/ThemeContext';

type ThemeOption = 'light' | 'dark' | 'system';

export function ThemeSwitcher() {
  const { mode, setMode } = useTheme();

  const options: { value: ThemeOption; icon: typeof SunIcon; label: string }[] = [
    { value: 'light', icon: SunIcon, label: 'Light' },
    { value: 'dark', icon: MoonIcon, label: 'Dark' },
    { value: 'system', icon: MonitorIcon, label: 'System' },
  ];

  return (
    <HStack space="sm">
      {options.map((option) => (
        <Button
          key={option.value}
          variant={mode === option.value ? 'solid' : 'outline'}
          action={mode === option.value ? 'primary' : 'secondary'}
          size="sm"
          onPress={() => setMode(option.value)}
        >
          <ButtonIcon as={option.icon} />
          <ButtonText>{option.label}</ButtonText>
        </Button>
      ))}
    </HStack>
  );
}
```

### Themed Card Component

```tsx
import { Box } from '@/components/ui/box';
import { VStack } from '@/components/ui/vstack';
import { Heading } from '@/components/ui/heading';
import { Text } from '@/components/ui/text';
import { cn } from '@/utils/styles';

interface ThemedCardProps {
  title: string;
  description: string;
  variant?: 'default' | 'elevated' | 'outlined';
  children?: React.ReactNode;
}

export function ThemedCard({
  title,
  description,
  variant = 'default',
  children,
}: ThemedCardProps) {
  const variantStyles = {
    default: 'bg-background-0 dark:bg-background-100',
    elevated: cn(
      'bg-background-0 dark:bg-background-100',
      'shadow-lg dark:shadow-none',
      'dark:border dark:border-outline-700'
    ),
    outlined: cn(
      'bg-transparent',
      'border-2 border-outline-300 dark:border-outline-600'
    ),
  };

  return (
    <Box className={cn('rounded-xl p-4', variantStyles[variant])}>
      <VStack space="sm">
        <Heading size="md" className="text-typography-900 dark:text-typography-50">
          {title}
        </Heading>
        <Text size="sm" className="text-typography-500 dark:text-typography-400">
          {description}
        </Text>
        {children}
      </VStack>
    </Box>
  );
}
```

## Common Patterns

### Gradient Backgrounds

```tsx
import { LinearGradient } from 'expo-linear-gradient';
import { Box } from '@/components/ui/box';

function GradientCard({ children }: { children: React.ReactNode }) {
  return (
    <Box className="rounded-xl overflow-hidden">
      <LinearGradient
        colors={['#0EA5E9', '#6366F1']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={{ padding: 16 }}
      >
        {children}
      </LinearGradient>
    </Box>
  );
}
```

### Conditional Theme Styles

```tsx
import { useTheme } from '@/contexts/ThemeContext';

function AdaptiveImage() {
  const { resolvedMode } = useTheme();

  return (
    <Image
      source={
        resolvedMode === 'dark'
          ? require('@/assets/logo-dark.png')
          : require('@/assets/logo-light.png')
      }
      className="w-32 h-32"
    />
  );
}
```

## Anti-Patterns

### Do Not Use Hardcoded Colors

```tsx
// Bad: Hardcoded hex values
<Box className="bg-[#FFFFFF] dark:bg-[#1F2937]">
  <Text className="text-[#111827] dark:text-[#F9FAFB]">Hello</Text>
</Box>

// Good: Semantic tokens
<Box className="bg-background-0 dark:bg-background-dark">
  <Text className="text-typography-900 dark:text-typography-50">Hello</Text>
</Box>
```

### Do Not Mix Theming Systems

```tsx
// Bad: Mixing StyleSheet with NativeWind
const styles = StyleSheet.create({
  container: { backgroundColor: '#FFFFFF' },
});

<Box style={styles.container} className="p-4">
  <Text>Content</Text>
</Box>

// Good: Use NativeWind consistently
<Box className="bg-background-0 p-4">
  <Text>Content</Text>
</Box>
```

### Do Not Forget Dark Mode Variants

```tsx
// Bad: Missing dark mode
<Box className="bg-white border-gray-200">
  <Text className="text-gray-900">Content</Text>
</Box>

// Good: Include dark mode variants
<Box className="bg-background-0 dark:bg-background-dark border-outline-200 dark:border-outline-700">
  <Text className="text-typography-900 dark:text-typography-50">Content</Text>
</Box>
```

## Related Skills

- **gluestack-components**: Building UI with gluestack-ui components
- **gluestack-accessibility**: Ensuring accessible implementations
