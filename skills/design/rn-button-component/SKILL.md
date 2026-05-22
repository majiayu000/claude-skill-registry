---
name: rn-button-component
description: Ensures buttons use the unified Button component with proper state management, icon support, and glass effect integration. Apply when creating or modifying buttons in the app.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Button Component

Guide for using the unified `Button` component with state management, icon support, and glass effect integration.

## Overview

- **Location**: `@/components/Button`
- **Features**: State management, icon support, loading states, success/error states, glass effect on iOS
- **Design**: Rounded corners (borderRadius: 25), glass effect on iOS when available

## Basic Usage

```tsx
import { Button } from '@/components/Button';

<Button text="Click Me" onPress={() => console.log('Pressed')} />
```

## Props

### Required Props

- `text: string | React.ReactNode` - Button label text
- `onPress: () => void` - Press handler function

### Optional Props

- `variant?: 'primary' | 'secondary' | 'destructive'` - Button style variant (default: `'primary'`)
- `buttonState?: ButtonState` - Current button state (default: `'default'`)
- `loadingText?: string | React.ReactNode` - Text shown during loading state
- `successText?: string | React.ReactNode` - Text shown during success state
- `errorText?: string | React.ReactNode` - Text shown during error state
- `icon?: { name, size?, position? }` - Icon configuration
- `successIcon?: { name, size? }` - Icon shown in success state (default: `'checkmark'`)
- `reset?: boolean` - Auto-reset from success to default after 2 seconds (default: `false`)
- `setButtonState?: (state: ButtonState) => void` - External state control function
- `style?: StyleProp<ViewStyle>` - Additional styles

## Button States

```tsx
export type ButtonState = 'default' | 'disabled' | 'loading' | 'success' | 'error';
```

### State Behavior

- **`'default'`**: Normal interactive state
- **`'disabled'`**: Button is disabled and non-interactive
- **`'loading'`**: Shows loading spinner with optional `loadingText`
- **`'success'`**: Shows success icon with optional `successText`
- **`'error'`**: Shows error message with `errorText`

## Common Patterns

### Basic Button

```tsx
<Button text="Save" onPress={handleSave} />
```

### Button with Variant

```tsx
<Button text="Cancel" onPress={handleCancel} variant="secondary" />
<Button text="Delete" onPress={handleDelete} variant="destructive" />
```

### Loading State

```tsx
const [isSaving, setIsSaving] = useState(false);

<Button
  text="Save"
  onPress={handleSave}
  buttonState={isSaving ? 'loading' : 'default'}
  loadingText="Saving..."
/>
```

### Disabled State

```tsx
<Button
  text="Submit"
  onPress={handleSubmit}
  buttonState={!isValid ? 'disabled' : 'default'}
/>
```

### Button with Icon

```tsx
<Button
  text="Create Lesson"
  onPress={handleCreate}
  icon={{ name: 'add', size: 24, position: 'left' }}
  variant="secondary"
/>
```

### Success State with Auto-Reset

```tsx
const [buttonState, setButtonState] = useState<ButtonState>('default');

const handleSave = async () => {
  setButtonState('loading');
  try {
    await saveData();
    setButtonState('success');
  } catch (error) {
    setButtonState('error');
  }
};

<Button
  text="Save"
  onPress={handleSave}
  buttonState={buttonState}
  setButtonState={setButtonState}
  loadingText="Saving..."
  successText="Saved!"
  errorText="Failed to save"
  reset={true} // Auto-resets to 'default' after 2 seconds
/>
```

### Combined Loading and Disabled

```tsx
<Button
  text="Save Lesson"
  onPress={handleSave}
  buttonState={isSaving ? 'loading' : isLoading ? 'disabled' : 'default'}
  loadingText="Saving..."
/>
```

## Icon Configuration

### Icon Props

```tsx
icon?: {
  name: keyof typeof Ionicons.glyphMap;  // Required: Ionicons icon name
  size?: number;                          // Optional: Icon size (default: 24)
  position?: 'left' | 'right';            // Optional: Icon position (default: 'left')
}
```

### Examples

```tsx
// Left icon (default)
<Button
  text="Add Item"
  icon={{ name: 'add', position: 'left' }}
  onPress={handleAdd}
/>

// Right icon
<Button
  text="Next"
  icon={{ name: 'arrow-forward', position: 'right' }}
  onPress={handleNext}
/>

// Custom size
<Button
  text="Settings"
  icon={{ name: 'settings', size: 20 }}
  onPress={handleSettings}
/>
```

## State Management

### Internal State (Default)

The button manages its own state internally when `setButtonState` is not provided:

```tsx
<Button
  text="Click Me"
  onPress={handleClick}
  buttonState="loading" // State is managed internally
/>
```

### External State Control

Provide `setButtonState` to control state externally:

```tsx
const [state, setState] = useState<ButtonState>('default');

<Button
  text="Submit"
  onPress={handleSubmit}
  buttonState={state}
  setButtonState={setState}
  loadingText="Submitting..."
/>
```

## Auto-Reset Pattern

When `reset={true}` and button reaches `'success'` state, it automatically resets to `'default'` after 2 seconds:

```tsx
const [state, setState] = useState<ButtonState>('default');

<Button
  text="Save"
  onPress={async () => {
    setState('loading');
    await save();
    setState('success');
  }}
  buttonState={state}
  setButtonState={setState}
  reset={true}
  successText="Saved!"
/>
```

## Glass Effect

The button automatically uses glass effect on iOS when available:

- **iOS 26+**: Uses `GlassView` with liquid glass effect
- **Other platforms**: Falls back to regular `View` with background color
- **Automatic**: No configuration needed, handled internally

The glass effect respects:
- `variant` prop for tint color
- `buttonState` for disabled/loading tint
- Interactive glass effect enabled automatically

## Styling

### Default Styles

- `borderRadius: 25` - Fully rounded corners
- `paddingVertical: 14`
- `paddingHorizontal: 24`
- `minHeight: 48`

### Custom Styles

```tsx
<Button
  text="Custom Button"
  onPress={handlePress}
  style={{ marginTop: 16, width: '100%' }}
/>
```

## Complete Examples

### Form Submit Button

```tsx
const [isSubmitting, setIsSubmitting] = useState(false);
const [submitState, setSubmitState] = useState<ButtonState>('default');

const handleSubmit = async () => {
  setIsSubmitting(true);
  setSubmitState('loading');
  
  try {
    await submitForm();
    setSubmitState('success');
  } catch (error) {
    setSubmitState('error');
  } finally {
    setIsSubmitting(false);
  }
};

<Button
  text="Submit Form"
  onPress={handleSubmit}
  buttonState={submitState}
  setButtonState={setSubmitState}
  loadingText="Submitting..."
  successText="Submitted!"
  errorText="Submission failed"
  reset={true}
  disabled={!isFormValid}
/>
```

### Action Button with Icon

```tsx
<Button
  text="Create Lesson"
  onPress={openModal}
  icon={{ name: 'add', size: 24, position: 'left' }}
  variant="secondary"
/>
```

### Conditional Loading

```tsx
<Button
  text="Translate"
  onPress={handleTranslate}
  buttonState={isTranslating ? 'loading' : 'default'}
  loadingText="Translating..."
  variant="secondary"
/>
```

## Best Practices

1. **Always provide `loadingText`** when using loading state for better UX
2. **Use `setButtonState`** for complex state management scenarios
3. **Use `reset={true}`** for temporary success states (e.g., form submissions)
4. **Provide `errorText`** when handling error states
5. **Use icons sparingly** - only when they add clarity
6. **Choose appropriate variants** - use `destructive` only for destructive actions

## TypeScript

```tsx
import { Button, ButtonState } from '@/components/Button';

const [state, setState] = useState<ButtonState>('default');
```

## References

- Component location: `components/Button.tsx`
- Uses: `expo-glass-effect`, `@expo/vector-icons`, React Native `Pressable`
