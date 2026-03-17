---
name: component-generator
description: Generates new React Native components following Ishkul patterns. Creates component with proper TypeScript types, theme integration, variant support, accessibility, and matching test file. Use when creating reusable UI components.
---

# Component Generator

Creates new React Native components following Ishkul's established patterns.

## What Gets Created

When generating a new component, create:

1. **Component file**: `frontend/src/components/ComponentName.tsx`
2. **Test file**: `frontend/src/components/__tests__/ComponentName.test.tsx`

## Component Template

```typescript
import React, { useCallback } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ViewStyle,
  TextStyle,
  ActivityIndicator,
  AccessibilityProps,
} from 'react-native';

import { useTheme } from '../hooks/useTheme';
import { Spacing } from '../theme/spacing';
import { Typography } from '../theme/typography';

// =============================================================================
// Types
// =============================================================================

export type ComponentVariant = 'primary' | 'secondary' | 'outline' | 'ghost';
export type ComponentSize = 'small' | 'medium' | 'large';

export interface ComponentNameProps extends AccessibilityProps {
  /** Main title text */
  title: string;

  /** Optional subtitle text */
  subtitle?: string;

  /** Handler for press events */
  onPress?: () => void;

  /** Visual variant of the component */
  variant?: ComponentVariant;

  /** Size of the component */
  size?: ComponentSize;

  /** Show loading state */
  loading?: boolean;

  /** Disable interactions */
  disabled?: boolean;

  /** Custom container style */
  style?: ViewStyle;

  /** Custom title style */
  titleStyle?: TextStyle;

  /** Custom subtitle style */
  subtitleStyle?: TextStyle;

  /** Test ID for testing */
  testID?: string;
}

// =============================================================================
// Component
// =============================================================================

export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  subtitle,
  onPress,
  variant = 'primary',
  size = 'medium',
  loading = false,
  disabled = false,
  style,
  titleStyle,
  subtitleStyle,
  testID,
  accessibilityLabel,
  accessibilityHint,
  accessibilityRole = 'button',
  ...accessibilityProps
}) => {
  const { colors } = useTheme();

  // ==========================================================================
  // Computed Styles
  // ==========================================================================

  const getVariantStyle = useCallback((): ViewStyle => {
    switch (variant) {
      case 'secondary':
        return {
          backgroundColor: colors.gray100,
          borderWidth: 0,
        };
      case 'outline':
        return {
          backgroundColor: 'transparent',
          borderWidth: 1,
          borderColor: colors.gray300,
        };
      case 'ghost':
        return {
          backgroundColor: 'transparent',
          borderWidth: 0,
        };
      case 'primary':
      default:
        return {
          backgroundColor: colors.primary,
          borderWidth: 0,
        };
    }
  }, [variant, colors]);

  const getTextColor = useCallback((): string => {
    if (disabled) {
      return colors.gray400;
    }

    switch (variant) {
      case 'primary':
        return colors.white;
      case 'secondary':
      case 'outline':
      case 'ghost':
        return colors.text;
      default:
        return colors.text;
    }
  }, [variant, disabled, colors]);

  const getSizeStyle = useCallback((): ViewStyle => {
    switch (size) {
      case 'small':
        return {
          paddingVertical: Spacing.sm,
          paddingHorizontal: Spacing.md,
          minHeight: Spacing.buttonHeight.small,
        };
      case 'large':
        return {
          paddingVertical: Spacing.lg,
          paddingHorizontal: Spacing.xl,
          minHeight: Spacing.buttonHeight.large,
        };
      case 'medium':
      default:
        return {
          paddingVertical: Spacing.md,
          paddingHorizontal: Spacing.lg,
          minHeight: Spacing.buttonHeight.medium,
        };
    }
  }, [size]);

  const getTitleSize = useCallback((): TextStyle => {
    switch (size) {
      case 'small':
        return Typography.bodySmall;
      case 'large':
        return Typography.bodyLarge;
      case 'medium':
      default:
        return Typography.body;
    }
  }, [size]);

  // ==========================================================================
  // Handlers
  // ==========================================================================

  const handlePress = useCallback(() => {
    if (!disabled && !loading && onPress) {
      onPress();
    }
  }, [disabled, loading, onPress]);

  // ==========================================================================
  // Render
  // ==========================================================================

  const textColor = getTextColor();
  const isInteractive = !disabled && !loading && !!onPress;

  const content = (
    <View
      style={[
        styles.container,
        getVariantStyle(),
        getSizeStyle(),
        disabled && styles.disabled,
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator
          size="small"
          color={textColor}
          testID={`${testID}-loading`}
        />
      ) : (
        <>
          <Text
            style={[
              styles.title,
              getTitleSize(),
              { color: textColor },
              titleStyle,
            ]}
            numberOfLines={1}
          >
            {title}
          </Text>

          {subtitle && (
            <Text
              style={[
                styles.subtitle,
                { color: colors.textSecondary },
                subtitleStyle,
              ]}
              numberOfLines={2}
            >
              {subtitle}
            </Text>
          )}
        </>
      )}
    </View>
  );

  // Wrap in TouchableOpacity only if interactive
  if (isInteractive) {
    return (
      <TouchableOpacity
        onPress={handlePress}
        disabled={disabled || loading}
        activeOpacity={0.7}
        testID={testID}
        accessibilityLabel={accessibilityLabel || title}
        accessibilityHint={accessibilityHint}
        accessibilityRole={accessibilityRole}
        accessibilityState={{
          disabled: disabled,
          busy: loading,
        }}
        {...accessibilityProps}
      >
        {content}
      </TouchableOpacity>
    );
  }

  // Non-interactive: render as View
  return (
    <View
      testID={testID}
      accessibilityLabel={accessibilityLabel || title}
      {...accessibilityProps}
    >
      {content}
    </View>
  );
};

// =============================================================================
// Styles
// =============================================================================

const styles = StyleSheet.create({
  container: {
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: Spacing.borderRadius.md,
  },
  title: {
    fontWeight: '600',
    textAlign: 'center',
  },
  subtitle: {
    marginTop: Spacing.xs,
    textAlign: 'center',
    ...Typography.caption,
  },
  disabled: {
    opacity: 0.5,
  },
});
```

## Test File Template

Create `frontend/src/components/__tests__/ComponentName.test.tsx`:

```typescript
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { ComponentName, ComponentNameProps, ComponentVariant, ComponentSize } from '../ComponentName';

// Mock theme hook
jest.mock('../../hooks/useTheme', () => ({
  useTheme: () => ({
    colors: {
      primary: '#0066FF',
      white: '#FFFFFF',
      text: '#1A1A1A',
      textSecondary: '#666666',
      gray100: '#F5F5F5',
      gray300: '#D4D4D4',
      gray400: '#A3A3A3',
    },
  }),
}));

describe('ComponentName', () => {
  const defaultProps: ComponentNameProps = {
    title: 'Test Title',
    onPress: jest.fn(),
    testID: 'component-name',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render with title', () => {
      const { getByText } = render(<ComponentName {...defaultProps} />);
      expect(getByText('Test Title')).toBeTruthy();
    });

    it('should render with subtitle when provided', () => {
      const { getByText } = render(
        <ComponentName {...defaultProps} subtitle="Test Subtitle" />
      );
      expect(getByText('Test Subtitle')).toBeTruthy();
    });

    it('should not render subtitle when not provided', () => {
      const { queryByText } = render(<ComponentName {...defaultProps} />);
      expect(queryByText('Test Subtitle')).toBeNull();
    });

    it('should show loading indicator when loading', () => {
      const { getByTestId, queryByText } = render(
        <ComponentName {...defaultProps} loading />
      );
      expect(getByTestId('component-name-loading')).toBeTruthy();
      expect(queryByText('Test Title')).toBeNull();
    });

    it('should hide loading indicator when not loading', () => {
      const { queryByTestId } = render(<ComponentName {...defaultProps} />);
      expect(queryByTestId('component-name-loading')).toBeNull();
    });
  });

  describe('Variants', () => {
    const variants: ComponentVariant[] = ['primary', 'secondary', 'outline', 'ghost'];

    variants.forEach((variant) => {
      it(`should render ${variant} variant without crashing`, () => {
        const { getByText } = render(
          <ComponentName {...defaultProps} variant={variant} />
        );
        expect(getByText('Test Title')).toBeTruthy();
      });
    });
  });

  describe('Sizes', () => {
    const sizes: ComponentSize[] = ['small', 'medium', 'large'];

    sizes.forEach((size) => {
      it(`should render ${size} size without crashing`, () => {
        const { getByText } = render(
          <ComponentName {...defaultProps} size={size} />
        );
        expect(getByText('Test Title')).toBeTruthy();
      });
    });
  });

  describe('Interactions', () => {
    it('should call onPress when pressed', () => {
      const onPressMock = jest.fn();
      const { getByTestId } = render(
        <ComponentName {...defaultProps} onPress={onPressMock} />
      );

      fireEvent.press(getByTestId('component-name'));

      expect(onPressMock).toHaveBeenCalledTimes(1);
    });

    it('should not call onPress when disabled', () => {
      const onPressMock = jest.fn();
      const { getByTestId } = render(
        <ComponentName {...defaultProps} onPress={onPressMock} disabled />
      );

      fireEvent.press(getByTestId('component-name'));

      expect(onPressMock).not.toHaveBeenCalled();
    });

    it('should not call onPress when loading', () => {
      const onPressMock = jest.fn();
      const { getByTestId } = render(
        <ComponentName {...defaultProps} onPress={onPressMock} loading />
      );

      fireEvent.press(getByTestId('component-name'));

      expect(onPressMock).not.toHaveBeenCalled();
    });

    it('should not wrap in TouchableOpacity when no onPress', () => {
      const { getByText } = render(
        <ComponentName title="Static" testID="static-component" />
      );
      expect(getByText('Static')).toBeTruthy();
    });
  });

  describe('Accessibility', () => {
    it('should have correct accessibility label', () => {
      const { getByLabelText } = render(
        <ComponentName {...defaultProps} accessibilityLabel="Custom Label" />
      );
      expect(getByLabelText('Custom Label')).toBeTruthy();
    });

    it('should default accessibility label to title', () => {
      const { getByLabelText } = render(<ComponentName {...defaultProps} />);
      expect(getByLabelText('Test Title')).toBeTruthy();
    });

    it('should have correct accessibility role', () => {
      const { getByRole } = render(<ComponentName {...defaultProps} />);
      expect(getByRole('button')).toBeTruthy();
    });
  });

  describe('Custom Styles', () => {
    it('should apply custom container style', () => {
      const customStyle = { marginTop: 20 };
      const { getByTestId } = render(
        <ComponentName {...defaultProps} style={customStyle} />
      );
      expect(getByTestId('component-name')).toBeTruthy();
    });

    it('should apply custom title style', () => {
      const customTitleStyle = { fontWeight: 'bold' as const };
      const { getByText } = render(
        <ComponentName {...defaultProps} titleStyle={customTitleStyle} />
      );
      expect(getByText('Test Title')).toBeTruthy();
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty title', () => {
      const { container } = render(
        <ComponentName {...defaultProps} title="" />
      );
      expect(container).toBeTruthy();
    });

    it('should handle very long title', () => {
      const longTitle = 'A'.repeat(200);
      const { getByText } = render(
        <ComponentName {...defaultProps} title={longTitle} />
      );
      expect(getByText(longTitle)).toBeTruthy();
    });

    it('should handle undefined onPress', () => {
      const { getByText } = render(
        <ComponentName title="No Press Handler" />
      );
      expect(getByText('No Press Handler')).toBeTruthy();
    });
  });
});
```

## Component Categories

### Interactive Components
- Buttons, Cards, List Items
- Use TouchableOpacity/Pressable
- Handle loading/disabled states
- Include onPress handlers

### Display Components
- Text, Labels, Badges, Icons
- Pure presentation, no interaction
- Focus on styling variants

### Input Components
- TextInput, Checkbox, Radio, Switch
- Handle value/onChange
- Validation states (error, success)
- Controlled component pattern

### Layout Components
- Container, Row, Column, Spacer
- Composition-focused
- Accept children

## Design System Integration

### Theme Colors
```typescript
const { colors } = useTheme();
// Available: primary, background, text, textSecondary, error, success, warning, white, gray100-900
```

### Spacing
```typescript
import { Spacing } from '../theme/spacing';
// Available: xs (4), sm (8), md (16), lg (24), xl (32), xxl (48)
// Also: buttonHeight, borderRadius, icon, touchTarget
```

### Typography
```typescript
import { Typography } from '../theme/typography';
// Available: h1, h2, h3, body, bodySmall, bodyLarge, caption, button
```

## Checklist Before Completing

- [ ] Component file created with TypeScript types
- [ ] Props interface exported for consumers
- [ ] Theme integration (useTheme hook)
- [ ] Variant support (if applicable)
- [ ] Size support (if applicable)
- [ ] Loading state (if interactive)
- [ ] Disabled state (if interactive)
- [ ] Accessibility props included
- [ ] Custom style props for overrides
- [ ] Test file with comprehensive coverage
- [ ] TypeScript compiles: `npm run type-check`
- [ ] Tests pass: `npm test -- --testPathPattern="ComponentName"`

## When to Use

- When creating reusable UI elements
- When building design system components
- When abstracting repeated patterns
- When creating interactive controls
