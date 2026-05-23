---
name: gluestack-accessibility
description: Use when ensuring accessible gluestack-ui implementations. Covers WAI-ARIA patterns, screen reader support, keyboard navigation, focus management, and WCAG 2.1 AA compliance.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# gluestack-ui - Accessibility

Expert knowledge of building accessible user interfaces with gluestack-ui, ensuring WCAG 2.1 AA compliance across React and React Native platforms.

## Overview

gluestack-ui components are built with accessibility in mind, following WAI-ARIA guidelines and providing built-in support for screen readers, keyboard navigation, and focus management. This skill covers best practices for maintaining and enhancing accessibility.

## Key Concepts

### Built-in Accessibility

gluestack-ui components include accessibility features out of the box:

```tsx
// Button automatically has role="button" and handles focus
<Button onPress={handlePress}>
  <ButtonText>Submit</ButtonText>
</Button>

// Modal manages focus trap and escape key handling
<Modal isOpen={isOpen} onClose={onClose}>
  <ModalContent>
    <ModalBody>Content</ModalBody>
  </ModalContent>
</Modal>

// Form controls link labels to inputs
<FormControl>
  <FormControlLabel>
    <FormControlLabelText>Email</FormControlLabelText>
  </FormControlLabel>
  <Input>
    <InputField />
  </Input>
</FormControl>
```

### Accessibility Props

React Native accessibility props supported by gluestack-ui:

```tsx
<Pressable
  accessibilityLabel="Close dialog"
  accessibilityHint="Closes the current dialog and returns to the previous screen"
  accessibilityRole="button"
  accessibilityState={{ disabled: isDisabled }}
  accessible={true}
  onPress={onClose}
>
  <Icon as={CloseIcon} />
</Pressable>
```

### ARIA Attributes for Web

For web platforms, use ARIA attributes:

```tsx
import { Platform } from 'react-native';

<Button
  {...(Platform.OS === 'web' && {
    'aria-label': 'Close dialog',
    'aria-describedby': 'dialog-description',
    'aria-expanded': isExpanded,
  })}
  onPress={handlePress}
>
  <ButtonText>Toggle</ButtonText>
</Button>
```

## Screen Reader Support

### Meaningful Labels

Provide descriptive labels for interactive elements:

```tsx
// Bad: No context for screen reader users
<Button onPress={handleDelete}>
  <ButtonIcon as={TrashIcon} />
</Button>

// Good: Clear accessibility label
<Button
  onPress={handleDelete}
  accessibilityLabel="Delete item"
  accessibilityHint="Permanently removes this item from your list"
>
  <ButtonIcon as={TrashIcon} />
</Button>
```

### Announcing Dynamic Changes

Use accessibility live regions for dynamic content:

```tsx
import { AccessibilityInfo } from 'react-native';

function SearchResults({ results, isLoading }: {
  results: Item[];
  isLoading: boolean;
}) {
  useEffect(() => {
    if (!isLoading) {
      AccessibilityInfo.announceForAccessibility(
        `${results.length} results found`
      );
    }
  }, [results, isLoading]);

  return (
    <VStack
      accessibilityRole="list"
      accessibilityLabel={`Search results, ${results.length} items`}
    >
      {results.map((item) => (
        <Box key={item.id} accessibilityRole="listitem">
          <Text>{item.name}</Text>
        </Box>
      ))}
    </VStack>
  );
}
```

### Image Accessibility

Always provide alt text for images:

```tsx
import { Image } from '@/components/ui/image';

// Informative image
<Image
  source={{ uri: product.imageUrl }}
  alt={`${product.name} - ${product.color} color option`}
  className="w-full h-48 rounded-lg"
/>

// Decorative image (hide from screen readers)
<Image
  source={require('@/assets/decorative-pattern.png')}
  alt=""
  accessibilityElementsHidden={true}
  importantForAccessibility="no-hide-descendants"
  className="absolute inset-0 opacity-10"
/>
```

## Keyboard Navigation

### Focus Management

Ensure proper focus order and visibility:

```tsx
import { useRef, useEffect } from 'react';
import { TextInput } from 'react-native';

function SearchModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const searchInputRef = useRef<TextInput>(null);

  useEffect(() => {
    if (isOpen) {
      // Focus the search input when modal opens
      searchInputRef.current?.focus();
    }
  }, [isOpen]);

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalContent>
        <ModalHeader>
          <Heading>Search</Heading>
          <ModalCloseButton />
        </ModalHeader>
        <ModalBody>
          <Input>
            <InputField
              ref={searchInputRef}
              placeholder="Search..."
              accessibilityLabel="Search input"
            />
          </Input>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
```

### Focus Trap in Modals

gluestack-ui Modal automatically traps focus, but you can enhance it:

```tsx
function AccessibleModal({ isOpen, onClose, children }: {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      closeOnOverlayClick={true}
      // Escape key closes modal (built-in)
    >
      <ModalBackdrop />
      <ModalContent
        accessibilityRole="dialog"
        accessibilityModal={true}
        accessibilityLabel="Dialog"
      >
        {children}
      </ModalContent>
    </Modal>
  );
}
```

### Keyboard Shortcuts

Implement keyboard shortcuts for web:

```tsx
import { useEffect } from 'react';
import { Platform } from 'react-native';

function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    if (Platform.OS !== 'web') return;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === key && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        callback();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [key, callback]);
}

// Usage
function SearchBar() {
  const inputRef = useRef<TextInput>(null);

  useKeyboardShortcut('k', () => {
    inputRef.current?.focus();
  });

  return (
    <Input>
      <InputField
        ref={inputRef}
        placeholder="Search (Cmd+K)"
        accessibilityKeyShortcuts={['cmd+k']}
      />
    </Input>
  );
}
```

## Form Accessibility

### Label Association

Properly associate labels with form controls:

```tsx
import {
  FormControl,
  FormControlLabel,
  FormControlLabelText,
  FormControlHelper,
  FormControlHelperText,
  FormControlError,
  FormControlErrorIcon,
  FormControlErrorText,
} from '@/components/ui/form-control';
import { Input, InputField } from '@/components/ui/input';
import { AlertCircleIcon } from 'lucide-react-native';

function AccessibleFormField({
  label,
  placeholder,
  helperText,
  error,
  isRequired,
  value,
  onChange,
}: {
  label: string;
  placeholder: string;
  helperText?: string;
  error?: string;
  isRequired?: boolean;
  value: string;
  onChange: (text: string) => void;
}) {
  return (
    <FormControl isRequired={isRequired} isInvalid={!!error}>
      <FormControlLabel>
        <FormControlLabelText>{label}</FormControlLabelText>
      </FormControlLabel>
      <Input>
        <InputField
          placeholder={placeholder}
          value={value}
          onChangeText={onChange}
          accessibilityLabel={label}
          accessibilityHint={helperText}
        />
      </Input>
      {error ? (
        <FormControlError>
          <FormControlErrorIcon as={AlertCircleIcon} />
          <FormControlErrorText>{error}</FormControlErrorText>
        </FormControlError>
      ) : helperText ? (
        <FormControlHelper>
          <FormControlHelperText>{helperText}</FormControlHelperText>
        </FormControlHelper>
      ) : null}
    </FormControl>
  );
}
```

### Error Announcement

Announce form errors to screen readers:

```tsx
import { AccessibilityInfo } from 'react-native';

function FormWithValidation() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateAndSubmit = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    }
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);

    const errorCount = Object.keys(newErrors).length;
    if (errorCount > 0) {
      // Announce errors to screen readers
      AccessibilityInfo.announceForAccessibility(
        `Form has ${errorCount} error${errorCount > 1 ? 's' : ''}. ${Object.values(newErrors).join('. ')}`
      );
      return;
    }

    submitForm();
  };

  return (
    <VStack space="md">
      <AccessibleFormField
        label="Email"
        error={errors.email}
        {...emailProps}
      />
      <AccessibleFormField
        label="Password"
        error={errors.password}
        {...passwordProps}
      />
      <Button onPress={validateAndSubmit}>
        <ButtonText>Submit</ButtonText>
      </Button>
    </VStack>
  );
}
```

### Required Field Indication

Clearly indicate required fields:

```tsx
function RequiredLabel({ label }: { label: string }) {
  return (
    <FormControlLabel>
      <FormControlLabelText>
        {label}
        <Text className="text-error-500" accessibilityLabel="required">
          {' *'}
        </Text>
      </FormControlLabelText>
    </FormControlLabel>
  );
}
```

## Best Practices

### 1. Use Semantic Components

Choose appropriate components for their semantic meaning:

```tsx
// Good: Semantic components
<Heading size="xl" accessibilityRole="header">Page Title</Heading>
<Button onPress={handleSubmit}>
  <ButtonText>Submit</ButtonText>
</Button>

// Bad: Generic elements for interactive content
<Text onPress={handleSubmit}>Submit</Text>
```

### 2. Provide Sufficient Color Contrast

Ensure text meets WCAG contrast requirements (4.5:1 for normal text, 3:1 for large text):

```tsx
// Good: High contrast
<Text className="text-typography-900 dark:text-typography-50">
  Readable text
</Text>

// Bad: Low contrast
<Text className="text-typography-300">
  Hard to read text
</Text>
```

### 3. Support Reduced Motion

Respect user preferences for reduced motion:

```tsx
import { useReducedMotion } from 'react-native-reanimated';

function AnimatedCard({ children }: { children: React.ReactNode }) {
  const reducedMotion = useReducedMotion();

  return (
    <Animated.View
      entering={reducedMotion ? undefined : FadeIn.duration(300)}
      exiting={reducedMotion ? undefined : FadeOut.duration(300)}
    >
      {children}
    </Animated.View>
  );
}
```

### 4. Handle Touch Target Sizes

Ensure touch targets are at least 44x44 points:

```tsx
// Good: Adequate touch target
<Button size="md" className="min-h-[44px] min-w-[44px]">
  <ButtonIcon as={MenuIcon} />
</Button>

// Or use Pressable with hitSlop
<Pressable
  onPress={handlePress}
  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
  className="p-2"
>
  <Icon as={CloseIcon} size="sm" />
</Pressable>
```

### 5. Group Related Elements

Use accessibility groups for related content:

```tsx
<Box
  accessibilityRole="group"
  accessibilityLabel="Product details"
>
  <Heading>{product.name}</Heading>
  <Text>{product.description}</Text>
  <Text>{formatPrice(product.price)}</Text>
</Box>
```

## Examples

### Accessible Navigation Menu

```tsx
import { useState } from 'react';
import { HStack } from '@/components/ui/hstack';
import { Pressable } from '@/components/ui/pressable';
import { Text } from '@/components/ui/text';

interface NavItem {
  id: string;
  label: string;
  href: string;
}

function AccessibleNav({ items, currentPath }: {
  items: NavItem[];
  currentPath: string;
}) {
  return (
    <HStack
      space="md"
      accessibilityRole="navigation"
      accessibilityLabel="Main navigation"
    >
      {items.map((item) => {
        const isActive = currentPath === item.href;

        return (
          <Pressable
            key={item.id}
            accessibilityRole="link"
            accessibilityLabel={item.label}
            accessibilityState={{ selected: isActive }}
            accessibilityCurrent={isActive ? 'page' : undefined}
            onPress={() => navigate(item.href)}
            className={cn(
              'px-4 py-2 rounded-lg',
              isActive
                ? 'bg-primary-500'
                : 'bg-transparent hover:bg-background-100'
            )}
          >
            <Text
              className={cn(
                isActive ? 'text-typography-0' : 'text-typography-700'
              )}
            >
              {item.label}
            </Text>
          </Pressable>
        );
      })}
    </HStack>
  );
}
```

### Accessible Data Table

```tsx
import { VStack } from '@/components/ui/vstack';
import { HStack } from '@/components/ui/hstack';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';

interface Column<T> {
  key: keyof T;
  header: string;
  accessibilityLabel?: string;
}

interface AccessibleTableProps<T> {
  columns: Column<T>[];
  data: T[];
  caption: string;
}

function AccessibleTable<T extends { id: string }>({
  columns,
  data,
  caption,
}: AccessibleTableProps<T>) {
  return (
    <VStack
      accessibilityRole="table"
      accessibilityLabel={caption}
    >
      {/* Caption for screen readers */}
      <Text
        accessibilityRole="summary"
        className="sr-only"
      >
        {caption}
      </Text>

      {/* Header Row */}
      <HStack
        accessibilityRole="row"
        className="bg-background-100 dark:bg-background-800 rounded-t-lg"
      >
        {columns.map((column) => (
          <Box
            key={String(column.key)}
            accessibilityRole="columnheader"
            className="flex-1 p-3"
          >
            <Text className="font-semibold text-typography-700 dark:text-typography-200">
              {column.header}
            </Text>
          </Box>
        ))}
      </HStack>

      {/* Data Rows */}
      {data.map((row, rowIndex) => (
        <HStack
          key={row.id}
          accessibilityRole="row"
          accessibilityLabel={`Row ${rowIndex + 1}`}
          className={cn(
            'border-b border-outline-200 dark:border-outline-700',
            rowIndex % 2 === 0 ? 'bg-background-0' : 'bg-background-50'
          )}
        >
          {columns.map((column) => (
            <Box
              key={String(column.key)}
              accessibilityRole="cell"
              accessibilityLabel={`${column.header}: ${String(row[column.key])}`}
              className="flex-1 p-3"
            >
              <Text className="text-typography-900 dark:text-typography-50">
                {String(row[column.key])}
              </Text>
            </Box>
          ))}
        </HStack>
      ))}
    </VStack>
  );
}
```

### Accessible Alert Component

```tsx
import { HStack } from '@/components/ui/hstack';
import { VStack } from '@/components/ui/vstack';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Icon } from '@/components/ui/icon';
import {
  AlertCircleIcon,
  CheckCircleIcon,
  InfoIcon,
  AlertTriangleIcon,
} from 'lucide-react-native';

type AlertType = 'info' | 'success' | 'warning' | 'error';

interface AccessibleAlertProps {
  type: AlertType;
  title: string;
  message: string;
}

const alertConfig: Record<AlertType, {
  icon: typeof InfoIcon;
  containerClass: string;
  iconClass: string;
  role: 'alert' | 'status';
}> = {
  info: {
    icon: InfoIcon,
    containerClass: 'bg-info-50 dark:bg-info-900 border-info-200',
    iconClass: 'text-info-500',
    role: 'status',
  },
  success: {
    icon: CheckCircleIcon,
    containerClass: 'bg-success-50 dark:bg-success-900 border-success-200',
    iconClass: 'text-success-500',
    role: 'status',
  },
  warning: {
    icon: AlertTriangleIcon,
    containerClass: 'bg-warning-50 dark:bg-warning-900 border-warning-200',
    iconClass: 'text-warning-500',
    role: 'alert',
  },
  error: {
    icon: AlertCircleIcon,
    containerClass: 'bg-error-50 dark:bg-error-900 border-error-200',
    iconClass: 'text-error-500',
    role: 'alert',
  },
};

export function AccessibleAlert({ type, title, message }: AccessibleAlertProps) {
  const config = alertConfig[type];

  return (
    <Box
      accessibilityRole={config.role}
      accessibilityLiveRegion={type === 'error' || type === 'warning' ? 'assertive' : 'polite'}
      accessibilityLabel={`${type} alert: ${title}. ${message}`}
      className={cn(
        'p-4 rounded-lg border',
        config.containerClass
      )}
    >
      <HStack space="sm" alignItems="flex-start">
        <Icon
          as={config.icon}
          className={cn('w-5 h-5 mt-0.5', config.iconClass)}
          accessibilityElementsHidden={true}
        />
        <VStack space="xs" flex={1}>
          <Text className="font-semibold text-typography-900 dark:text-typography-50">
            {title}
          </Text>
          <Text className="text-typography-700 dark:text-typography-200">
            {message}
          </Text>
        </VStack>
      </HStack>
    </Box>
  );
}
```

## Common Patterns

### Skip Navigation Link

```tsx
import { useState } from 'react';
import { Pressable } from '@/components/ui/pressable';
import { Text } from '@/components/ui/text';

function SkipLink() {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <Pressable
      onPress={() => {
        // Focus main content
        document.getElementById('main-content')?.focus();
      }}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
      accessibilityRole="link"
      accessibilityLabel="Skip to main content"
      className={cn(
        'absolute left-4 z-50 px-4 py-2 bg-primary-500 rounded-md',
        'transition-all duration-200',
        isFocused ? 'top-4' : '-top-20'
      )}
    >
      <Text className="text-typography-0 font-semibold">
        Skip to main content
      </Text>
    </Pressable>
  );
}
```

### Loading State Announcement

```tsx
import { useEffect } from 'react';
import { AccessibilityInfo } from 'react-native';
import { Spinner } from '@/components/ui/spinner';
import { Text } from '@/components/ui/text';
import { VStack } from '@/components/ui/vstack';

function LoadingState({ isLoading, loadingText = 'Loading...' }: {
  isLoading: boolean;
  loadingText?: string;
}) {
  useEffect(() => {
    if (isLoading) {
      AccessibilityInfo.announceForAccessibility(loadingText);
    }
  }, [isLoading, loadingText]);

  if (!isLoading) return null;

  return (
    <VStack
      space="sm"
      alignItems="center"
      accessibilityRole="progressbar"
      accessibilityLabel={loadingText}
      accessibilityLiveRegion="polite"
    >
      <Spinner size="large" />
      <Text className="text-typography-500">{loadingText}</Text>
    </VStack>
  );
}
```

## Anti-Patterns

### Do Not Hide Interactive Elements

```tsx
// Bad: Interactive element hidden from accessibility
<Pressable
  onPress={handlePress}
  importantForAccessibility="no"
>
  <Text>Click me</Text>
</Pressable>

// Good: Interactive element accessible
<Pressable
  onPress={handlePress}
  accessibilityRole="button"
  accessibilityLabel="Perform action"
>
  <Text>Click me</Text>
</Pressable>
```

### Do Not Use Color Alone to Convey Information

```tsx
// Bad: Only color indicates error
<Input>
  <InputField className="border-error-500" />
</Input>

// Good: Color plus icon and text
<FormControl isInvalid>
  <Input>
    <InputField />
  </Input>
  <FormControlError>
    <FormControlErrorIcon as={AlertCircleIcon} />
    <FormControlErrorText>This field is required</FormControlErrorText>
  </FormControlError>
</FormControl>
```

### Do Not Remove Focus Indicators

```tsx
// Bad: Removing focus outline
<Pressable className="focus:outline-none">
  <Text>Click</Text>
</Pressable>

// Good: Visible focus indicator
<Pressable className="focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-lg">
  <Text>Click</Text>
</Pressable>
```

### Do Not Use Placeholder as Label

```tsx
// Bad: Placeholder only
<Input>
  <InputField placeholder="Email" />
</Input>

// Good: Proper label
<FormControl>
  <FormControlLabel>
    <FormControlLabelText>Email</FormControlLabelText>
  </FormControlLabel>
  <Input>
    <InputField placeholder="name@example.com" />
  </Input>
</FormControl>
```

## WCAG 2.1 AA Checklist

### Perceivable

- [ ] Text has 4.5:1 contrast ratio (3:1 for large text)
- [ ] Images have alt text
- [ ] Form inputs have visible labels
- [ ] Content is readable when zoomed to 200%
- [ ] Color is not the only means of conveying information

### Operable

- [ ] All functionality available via keyboard
- [ ] Focus order is logical
- [ ] Focus indicators are visible
- [ ] Touch targets are at least 44x44 points
- [ ] Users have enough time to read and interact

### Understandable

- [ ] Language is specified
- [ ] Navigation is consistent
- [ ] Form errors are identified and described
- [ ] Labels and instructions are provided

### Robust

- [ ] Valid markup/component structure
- [ ] Name, role, and value are programmatically determined
- [ ] Status messages are announced to screen readers

## Related Skills

- **gluestack-components**: Building UI with gluestack-ui components
- **gluestack-theming**: Customizing themes and design tokens
