---
description: "Conventions and patterns for React Native/Expo mobile development including component structure, styling with NativeWind, hooks, testing, and Storybook"
---

# React Native Component Guidelines

This skill provides conventions for React Native/Expo mobile development.

## Directory Structure

```
apps/mobile/src/
├── components/
│   ├── ui/                     # Design system primitives (Button, Input, Card, etc.)
│   │   └── [ComponentName]/
│   │       ├── [ComponentName].tsx
│   │       ├── [ComponentName].test.tsx
│   │       ├── [ComponentName].stories.tsx
│   │       └── index.ts
│   └── common/                 # Shared business components (Avatar, MessageBubble, etc.)
├── features/                   # Feature-specific code
│   └── [feature-name]/
│       ├── components/
│       ├── hooks/
│       └── screens/
├── hooks/                      # App-wide shared hooks
├── screens/                    # Top-level screens (navigation entry points)
└── lib/                        # Utilities, constants, types
```

## Component Structure

Every component **must** be a folder with:
- `ComponentName.tsx` - Implementation
- `ComponentName.test.tsx` - Unit tests (required)
- `ComponentName.stories.tsx` - Storybook story (required for ui/common)
- `index.ts` - Barrel export

### Component Pattern

```tsx
import { View, Text, Pressable } from 'react-native';

export interface ButtonProps {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export function Button({ label, onPress, variant = 'primary', disabled = false }: ButtonProps) {
  return (
    <Pressable
      className={`px-4 py-2 rounded-lg ${variant === 'primary' ? 'bg-accent' : 'bg-background'} ${disabled ? 'opacity-50' : ''}`}
      onPress={onPress}
      disabled={disabled}
    >
      <Text className={`text-center font-medium ${variant === 'primary' ? 'text-background' : 'text-foreground'}`}>
        {label}
      </Text>
    </Pressable>
  );
}
```

### Barrel File (`index.ts`)

```ts
export { Button } from './Button';
export type { ButtonProps } from './Button';
```

## Rules

- **Named exports only** (no default exports)
- **Props interface** named `[ComponentName]Props` and exported
- Keep components focused on presentation; extract logic to hooks

## Styling

**Use uniwind (NativeWind) classes only. StyleSheet.create() is FORBIDDEN.**

| Rule | Status |
|------|--------|
| Use uniwind className prop | Required |
| Inline classNames | Required |
| Use theme colors | Required |
| StyleSheet.create() | Forbidden |
| Inline style prop | Forbidden (except dynamic values) |
| Hardcoded color values | Forbidden |

### Theme Colors

Colors **must** come from theme in `global.css`:

| Class | Usage |
|-------|-------|
| `bg-background` / `text-background` | Main background |
| `bg-foreground` / `text-foreground` | Main text |
| `bg-accent` / `text-accent` | Accent/highlight |

**Never use hardcoded colors** like `bg-white`, `text-black`, `bg-blue-500`.

### Correct

```tsx
<View className="flex-1 bg-background p-4">
  <Text className="text-lg font-bold text-foreground">Title</Text>
</View>
```

### Incorrect

```tsx
// Hardcoded colors
<View className="bg-white">

// StyleSheet.create
const styles = StyleSheet.create({ container: { flex: 1 } });

// Inline style
<View style={{ flex: 1, backgroundColor: 'white' }} />
```

## Hooks

| Hook Type | Location |
|-----------|----------|
| Component-specific | Inside component folder |
| Feature-shared | `features/[feature]/hooks/` |
| App-wide | `hooks/` |

### Pattern

```ts
export interface UseAuthReturn {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  isLoading: boolean;
}

export function useAuth(): UseAuthReturn {
  // implementation
}
```

## Screens

- Orchestrate components, no business logic
- Data fetching in hooks, not screens
- NO Storybook stories (use Maestro E2E)

## Testing

### Unit Tests (Required)

```tsx
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

describe('Button', () => {
  it('renders label correctly', () => {
    render(<Button label="Click me" onPress={() => {}} />);
    expect(screen.getByText('Click me')).toBeOnTheScreen();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    render(<Button label="Click me" onPress={onPress} />);
    fireEvent.press(screen.getByText('Click me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

### E2E Tests (Maestro)

```yaml
# .maestro/flows/auth/login.yaml
appId: com.sunsay.attune
---
- launchApp
- tapOn: "Email"
- inputText: "test@example.com"
- tapOn: "Sign In"
- assertVisible: "Welcome"
```

## Storybook

Required for `ui/` and `common/` components:

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'ui/Button',
  component: Button,
  args: {
    label: 'Button',
    onPress: () => console.log('pressed'),
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = { args: { variant: 'primary' } };
export const Disabled: Story = { args: { disabled: true } };
```

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Component folder | PascalCase | `Button/` |
| Component file | PascalCase | `Button.tsx` |
| Hook file | camelCase | `useAuth.ts` |
| Feature folder | kebab-case | `features/user-profile/` |

## Checklist

- [ ] Component in correct location
- [ ] All required files present
- [ ] Props interface exported
- [ ] Styled with uniwind only
- [ ] Theme colors only (no hardcoded)
- [ ] Unit tests cover main functionality
- [ ] Storybook story (for ui/common)
- [ ] testID for interactive elements
