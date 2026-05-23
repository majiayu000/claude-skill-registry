---
name: gluestack-components
description: Use when building UI with gluestack-ui components. Covers component composition, variants, sizes, states, accessibility props, and platform-specific considerations for React and React Native.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# gluestack-ui - Components

Expert knowledge of gluestack-ui's universal component library for building accessible, performant UI across React and React Native platforms.

## Overview

gluestack-ui provides 50+ unstyled, accessible components that work seamlessly on web and mobile. Components are copy-pasteable into your project and styled with NativeWind (Tailwind CSS for React Native).

## Key Concepts

### Component Installation

Add components using the CLI:

```bash
# Initialize gluestack-ui in your project
npx gluestack-ui init

# Add individual components
npx gluestack-ui add button
npx gluestack-ui add input
npx gluestack-ui add modal

# Add multiple components
npx gluestack-ui add button input select modal

# Add all components
npx gluestack-ui add --all
```

### Component Anatomy

Every gluestack-ui component follows a consistent pattern:

```tsx
import { Button, ButtonText, ButtonSpinner, ButtonIcon } from '@/components/ui/button';

// Components are composable with sub-components
<Button size="md" variant="solid" action="primary">
  <ButtonIcon as={PlusIcon} />
  <ButtonText>Add Item</ButtonText>
  <ButtonSpinner />
</Button>
```

### Variants, Sizes, and Actions

Components support consistent prop APIs:

```tsx
// Button variants
<Button variant="solid">Solid</Button>
<Button variant="outline">Outline</Button>
<Button variant="link">Link</Button>

// Button sizes
<Button size="xs">Extra Small</Button>
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
<Button size="xl">Extra Large</Button>

// Button actions (semantic colors)
<Button action="primary">Primary</Button>
<Button action="secondary">Secondary</Button>
<Button action="positive">Positive</Button>
<Button action="negative">Negative</Button>
```

## Core Components

### Button

Interactive button with loading states and icons:

```tsx
import { Button, ButtonText, ButtonSpinner, ButtonIcon } from '@/components/ui/button';
import { SaveIcon } from 'lucide-react-native';

function SaveButton({ isLoading, onPress }: { isLoading: boolean; onPress: () => void }) {
  return (
    <Button
      size="md"
      variant="solid"
      action="primary"
      isDisabled={isLoading}
      onPress={onPress}
    >
      {isLoading ? (
        <ButtonSpinner />
      ) : (
        <ButtonIcon as={SaveIcon} />
      )}
      <ButtonText>{isLoading ? 'Saving...' : 'Save'}</ButtonText>
    </Button>
  );
}
```

### Input

Text input with labels and validation:

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
import { Input, InputField, InputSlot, InputIcon } from '@/components/ui/input';
import { AlertCircleIcon, MailIcon } from 'lucide-react-native';

function EmailInput({ value, onChange, error }: {
  value: string;
  onChange: (text: string) => void;
  error?: string;
}) {
  return (
    <FormControl isInvalid={!!error}>
      <FormControlLabel>
        <FormControlLabelText>Email</FormControlLabelText>
      </FormControlLabel>
      <Input variant="outline" size="md">
        <InputSlot pl="$3">
          <InputIcon as={MailIcon} />
        </InputSlot>
        <InputField
          placeholder="Enter your email"
          value={value}
          onChangeText={onChange}
          keyboardType="email-address"
          autoCapitalize="none"
        />
      </Input>
      {error ? (
        <FormControlError>
          <FormControlErrorIcon as={AlertCircleIcon} />
          <FormControlErrorText>{error}</FormControlErrorText>
        </FormControlError>
      ) : (
        <FormControlHelper>
          <FormControlHelperText>We'll never share your email</FormControlHelperText>
        </FormControlHelper>
      )}
    </FormControl>
  );
}
```

### Select

Dropdown selection component:

```tsx
import {
  Select,
  SelectTrigger,
  SelectInput,
  SelectIcon,
  SelectPortal,
  SelectBackdrop,
  SelectContent,
  SelectDragIndicatorWrapper,
  SelectDragIndicator,
  SelectItem,
} from '@/components/ui/select';
import { ChevronDownIcon } from 'lucide-react-native';

function CountrySelect({ value, onValueChange }: {
  value: string;
  onValueChange: (value: string) => void;
}) {
  return (
    <Select selectedValue={value} onValueChange={onValueChange}>
      <SelectTrigger variant="outline" size="md">
        <SelectInput placeholder="Select country" />
        <SelectIcon as={ChevronDownIcon} mr="$3" />
      </SelectTrigger>
      <SelectPortal>
        <SelectBackdrop />
        <SelectContent>
          <SelectDragIndicatorWrapper>
            <SelectDragIndicator />
          </SelectDragIndicatorWrapper>
          <SelectItem label="United States" value="us" />
          <SelectItem label="Canada" value="ca" />
          <SelectItem label="United Kingdom" value="uk" />
          <SelectItem label="Australia" value="au" />
        </SelectContent>
      </SelectPortal>
    </Select>
  );
}
```

### Modal

Dialog overlay component:

```tsx
import {
  Modal,
  ModalBackdrop,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
} from '@/components/ui/modal';
import { Heading } from '@/components/ui/heading';
import { Text } from '@/components/ui/text';
import { Button, ButtonText } from '@/components/ui/button';
import { CloseIcon, Icon } from '@/components/ui/icon';

function ConfirmModal({ isOpen, onClose, onConfirm, title, message }: {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
}) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} size="md">
      <ModalBackdrop />
      <ModalContent>
        <ModalHeader>
          <Heading size="lg">{title}</Heading>
          <ModalCloseButton>
            <Icon as={CloseIcon} />
          </ModalCloseButton>
        </ModalHeader>
        <ModalBody>
          <Text>{message}</Text>
        </ModalBody>
        <ModalFooter>
          <Button variant="outline" action="secondary" onPress={onClose}>
            <ButtonText>Cancel</ButtonText>
          </Button>
          <Button action="negative" onPress={onConfirm}>
            <ButtonText>Delete</ButtonText>
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
```

### Toast

Notification component:

```tsx
import {
  Toast,
  ToastTitle,
  ToastDescription,
  useToast,
} from '@/components/ui/toast';

function NotificationExample() {
  const toast = useToast();

  const showToast = () => {
    toast.show({
      placement: 'top',
      render: ({ id }) => (
        <Toast nativeID={`toast-${id}`} action="success" variant="solid">
          <ToastTitle>Success!</ToastTitle>
          <ToastDescription>Your changes have been saved.</ToastDescription>
        </Toast>
      ),
    });
  };

  return (
    <Button onPress={showToast}>
      <ButtonText>Show Toast</ButtonText>
    </Button>
  );
}
```

### Accordion

Expandable content sections:

```tsx
import {
  Accordion,
  AccordionItem,
  AccordionHeader,
  AccordionTrigger,
  AccordionTitleText,
  AccordionIcon,
  AccordionContent,
  AccordionContentText,
} from '@/components/ui/accordion';
import { ChevronDownIcon, ChevronUpIcon } from 'lucide-react-native';

function FAQAccordion({ items }: { items: { question: string; answer: string }[] }) {
  return (
    <Accordion type="multiple" defaultValue={['item-0']}>
      {items.map((item, index) => (
        <AccordionItem key={index} value={`item-${index}`}>
          <AccordionHeader>
            <AccordionTrigger>
              {({ isExpanded }) => (
                <>
                  <AccordionTitleText>{item.question}</AccordionTitleText>
                  <AccordionIcon as={isExpanded ? ChevronUpIcon : ChevronDownIcon} />
                </>
              )}
            </AccordionTrigger>
          </AccordionHeader>
          <AccordionContent>
            <AccordionContentText>{item.answer}</AccordionContentText>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
```

### Checkbox and Radio

Selection controls:

```tsx
import {
  Checkbox,
  CheckboxIndicator,
  CheckboxIcon,
  CheckboxLabel,
} from '@/components/ui/checkbox';
import {
  RadioGroup,
  Radio,
  RadioIndicator,
  RadioIcon,
  RadioLabel,
} from '@/components/ui/radio';
import { CheckIcon, CircleIcon } from 'lucide-react-native';

function TermsCheckbox({ isChecked, onChange }: {
  isChecked: boolean;
  onChange: (checked: boolean) => void;
}) {
  return (
    <Checkbox value="terms" isChecked={isChecked} onChange={onChange}>
      <CheckboxIndicator>
        <CheckboxIcon as={CheckIcon} />
      </CheckboxIndicator>
      <CheckboxLabel>I agree to the terms and conditions</CheckboxLabel>
    </Checkbox>
  );
}

function ShippingOptions({ value, onChange }: {
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <RadioGroup value={value} onChange={onChange}>
      <Radio value="standard">
        <RadioIndicator>
          <RadioIcon as={CircleIcon} />
        </RadioIndicator>
        <RadioLabel>Standard Shipping (5-7 days)</RadioLabel>
      </Radio>
      <Radio value="express">
        <RadioIndicator>
          <RadioIcon as={CircleIcon} />
        </RadioIndicator>
        <RadioLabel>Express Shipping (2-3 days)</RadioLabel>
      </Radio>
      <Radio value="overnight">
        <RadioIndicator>
          <RadioIcon as={CircleIcon} />
        </RadioIndicator>
        <RadioLabel>Overnight Shipping (1 day)</RadioLabel>
      </Radio>
    </RadioGroup>
  );
}
```

## Best Practices

### 1. Use Composition Over Configuration

Compose components with sub-components for flexibility:

```tsx
// Good: Composable structure
<Button>
  <ButtonIcon as={PlusIcon} />
  <ButtonText>Add</ButtonText>
</Button>

// Avoid: Prop-heavy configuration
<Button icon={PlusIcon} text="Add" iconPosition="left" />
```

### 2. Leverage FormControl for Form Fields

Wrap inputs in FormControl for consistent validation:

```tsx
<FormControl isRequired isInvalid={!!error}>
  <FormControlLabel>
    <FormControlLabelText>Password</FormControlLabelText>
  </FormControlLabel>
  <Input>
    <InputField type="password" />
  </Input>
  <FormControlError>
    <FormControlErrorText>{error}</FormControlErrorText>
  </FormControlError>
</FormControl>
```

### 3. Handle Platform Differences

Use platform-specific logic when needed:

```tsx
import { Platform } from 'react-native';

function ResponsiveModal({ children }: { children: React.ReactNode }) {
  return (
    <Modal size={Platform.OS === 'web' ? 'lg' : 'full'}>
      <ModalContent>
        {children}
      </ModalContent>
    </Modal>
  );
}
```

### 4. Use Proper Loading States

Show loading feedback for async operations:

```tsx
function SubmitButton({ isLoading, onPress }: {
  isLoading: boolean;
  onPress: () => void;
}) {
  return (
    <Button isDisabled={isLoading} onPress={onPress}>
      {isLoading && <ButtonSpinner mr="$2" />}
      <ButtonText>{isLoading ? 'Submitting...' : 'Submit'}</ButtonText>
    </Button>
  );
}
```

### 5. Create Reusable Component Wrappers

Build app-specific components on top of gluestack-ui:

```tsx
// components/app/PrimaryButton.tsx
import { Button, ButtonText, ButtonSpinner } from '@/components/ui/button';

interface PrimaryButtonProps {
  children: string;
  isLoading?: boolean;
  onPress: () => void;
}

export function PrimaryButton({ children, isLoading, onPress }: PrimaryButtonProps) {
  return (
    <Button
      size="lg"
      variant="solid"
      action="primary"
      isDisabled={isLoading}
      onPress={onPress}
      className="rounded-full"
    >
      {isLoading && <ButtonSpinner mr="$2" />}
      <ButtonText>{children}</ButtonText>
    </Button>
  );
}
```

## Common Patterns

### Form with Validation

```tsx
import { useState } from 'react';
import { VStack } from '@/components/ui/vstack';
import { Button, ButtonText } from '@/components/ui/button';
import { FormControl, FormControlError, FormControlErrorText } from '@/components/ui/form-control';
import { Input, InputField } from '@/components/ui/input';

interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

function LoginForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const [formData, setFormData] = useState<FormData>({ email: '', password: '' });
  const [errors, setErrors] = useState<FormErrors>({});

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <VStack space="md">
      <FormControl isInvalid={!!errors.email}>
        <Input>
          <InputField
            placeholder="Email"
            value={formData.email}
            onChangeText={(text) => setFormData({ ...formData, email: text })}
          />
        </Input>
        <FormControlError>
          <FormControlErrorText>{errors.email}</FormControlErrorText>
        </FormControlError>
      </FormControl>

      <FormControl isInvalid={!!errors.password}>
        <Input>
          <InputField
            placeholder="Password"
            type="password"
            value={formData.password}
            onChangeText={(text) => setFormData({ ...formData, password: text })}
          />
        </Input>
        <FormControlError>
          <FormControlErrorText>{errors.password}</FormControlErrorText>
        </FormControlError>
      </FormControl>

      <Button onPress={handleSubmit}>
        <ButtonText>Login</ButtonText>
      </Button>
    </VStack>
  );
}
```

### Data List with Actions

```tsx
import { HStack } from '@/components/ui/hstack';
import { VStack } from '@/components/ui/vstack';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { Button, ButtonIcon } from '@/components/ui/button';
import { Pressable } from '@/components/ui/pressable';
import { TrashIcon, EditIcon } from 'lucide-react-native';

interface Item {
  id: string;
  title: string;
  description: string;
}

function ItemList({ items, onEdit, onDelete }: {
  items: Item[];
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}) {
  return (
    <VStack space="sm">
      {items.map((item) => (
        <Box
          key={item.id}
          className="p-4 bg-background-50 rounded-lg border border-outline-200"
        >
          <HStack justifyContent="space-between" alignItems="center">
            <VStack space="xs" flex={1}>
              <Heading size="sm">{item.title}</Heading>
              <Text size="sm" className="text-typography-500">
                {item.description}
              </Text>
            </VStack>
            <HStack space="xs">
              <Button
                size="sm"
                variant="outline"
                action="secondary"
                onPress={() => onEdit(item.id)}
              >
                <ButtonIcon as={EditIcon} />
              </Button>
              <Button
                size="sm"
                variant="outline"
                action="negative"
                onPress={() => onDelete(item.id)}
              >
                <ButtonIcon as={TrashIcon} />
              </Button>
            </HStack>
          </HStack>
        </Box>
      ))}
    </VStack>
  );
}
```

## Anti-Patterns

### Do Not Mix Styling Approaches

```tsx
// Bad: Mixing inline styles with NativeWind
<Button style={{ backgroundColor: 'blue' }} className="p-4">
  <ButtonText>Click</ButtonText>
</Button>

// Good: Use NativeWind classes consistently
<Button className="bg-blue-500 p-4">
  <ButtonText>Click</ButtonText>
</Button>
```

### Do Not Skip Accessibility Props

```tsx
// Bad: Missing accessibility information
<Pressable onPress={handlePress}>
  <Icon as={MenuIcon} />
</Pressable>

// Good: Include accessibility props
<Pressable
  onPress={handlePress}
  accessibilityLabel="Open menu"
  accessibilityRole="button"
>
  <Icon as={MenuIcon} />
</Pressable>
```

### Do Not Ignore Platform Constraints

```tsx
// Bad: Using web-only APIs on native
<Modal>
  <ModalContent onClick={handleClick}> {/* onClick doesn't work on native */}
    ...
  </ModalContent>
</Modal>

// Good: Use cross-platform events
<Modal>
  <ModalContent>
    <Pressable onPress={handlePress}>
      ...
    </Pressable>
  </ModalContent>
</Modal>
```

### Do Not Hardcode Colors

```tsx
// Bad: Hardcoded colors
<Box className="bg-[#3B82F6]">
  <Text className="text-[#FFFFFF]">Hello</Text>
</Box>

// Good: Use theme tokens
<Box className="bg-primary-500">
  <Text className="text-typography-0">Hello</Text>
</Box>
```

## Related Skills

- **gluestack-theming**: Customizing themes and design tokens
- **gluestack-accessibility**: Ensuring accessible implementations
