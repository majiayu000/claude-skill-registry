---
name: cross-platform-compatibility
description: This skill enforces cross-platform compatibility best practices for Expo apps targeting iOS, Android, and web. It should be used when creating new features, components, or screens to ensure they work correctly on all platforms. Use this skill when writing platform-specific code, using Platform.OS checks, creating platform-specific files (.web.tsx, .native.tsx, .ios.tsx, .android.tsx), or reviewing code for cross-platform issues.
---

# Cross-Platform Compatibility

This skill provides guidance for writing code that works correctly on iOS, Android, and web platforms in Expo applications.

## Core Principle

Every feature must work on **all three platforms** (iOS, Android, web) unless explicitly documented otherwise. Test on all platforms before considering a feature complete.

## Platform-Specific Approaches

There are two primary ways to handle platform differences:

### 1. Platform Module (Runtime Checks)

Use `Platform.OS` for small, inline differences within a single component.

```tsx
import { Platform } from "react-native";

// Simple conditional
if (Platform.OS === "web") {
  // Web-specific code
}

// Platform.select for multiple platforms
const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { shadowColor: "#000" },
      android: { elevation: 4 },
      web: { boxShadow: "0 2px 4px rgba(0,0,0,0.1)" },
    }),
  },
});
```

### 2. Platform-Specific File Extensions

Use file extensions when entire components or modules differ significantly between platforms.

| Extension      | Platforms     | Use Case                        |
| -------------- | ------------- | ------------------------------- |
| `.web.tsx`     | Web only      | Web-specific implementation     |
| `.native.tsx`  | iOS + Android | Shared native implementation    |
| `.ios.tsx`     | iOS only      | iOS-specific implementation     |
| `.android.tsx` | Android only  | Android-specific implementation |

**Resolution Priority**: Metro bundler resolves in this order:

1. `.ios.tsx` / `.android.tsx` (most specific)
2. `.native.tsx` (native platforms)
3. `.web.tsx` (web platform)
4. `.tsx` (universal fallback)

## Decision Tree: When to Use Each Approach

```
Need platform-specific behavior?
├── Small differences (styles, one-liner logic)?
│   └── Use Platform.OS or Platform.select()
├── Moderate differences (conditional rendering blocks)?
│   └── Use Platform.OS with clear separation
└── Significant differences (entire component logic)?
    └── Use platform-specific file extensions
```

### Use Platform.OS When:

- Differences are 1-5 lines of code
- Only styles differ between platforms
- Logic is mostly shared with minor variations
- You need to check platform at runtime dynamically

### Use File Extensions When:

- Components have fundamentally different implementations
- Different libraries are needed per platform (e.g., `dom-to-image` for web vs `react-native-view-shot` for native)
- Layout structure differs significantly
- You want cleaner separation of concerns

## File Extension Rules

### Within `app/` Directory (Expo Router)

Platform-specific extensions in the `app/` directory **require a base version** for route universality:

```
app/
├── _layout.tsx          # Required base version
├── _layout.web.tsx      # Optional web override
├── index.tsx            # Required base version
├── about.tsx            # Required base version
└── about.web.tsx        # Optional web override
```

### Outside `app/` Directory

Platform-specific files outside `app/` do not require a base version:

```
components/
├── DatePicker/
│   ├── DatePickerContainer.tsx      # Container (shared logic)
│   ├── DatePickerView.tsx           # Default view
│   ├── DatePickerView.web.tsx       # Web-specific view
│   └── index.tsx                    # Exports container
```

### Re-exporting Pattern

To use platform-specific components in routes:

```tsx
// components/about/index.tsx (or about.native.tsx + about.web.tsx)
// Platform-specific implementations

// app/about.tsx
export { default } from "../components/about";
```

## Common Cross-Platform Issues

### 1. Web-Incompatible APIs

These APIs require Platform.OS checks or alternatives on web:

| API                               | Issue on Web      | Solution                         |
| --------------------------------- | ----------------- | -------------------------------- |
| `MediaLibrary.saveToLibraryAsync` | Not supported     | Use download link on web         |
| `Share.share()`                   | Limited support   | Use Web Share API or clipboard   |
| `Haptics.*`                       | Not supported     | Skip or use CSS animations       |
| `captureRef()`                    | Not supported     | Use `dom-to-image` on web        |
| `Linking.openURL()`               | Works but differs | Consider `window.open()` for web |

### 2. Style Differences

```tsx
// Platform-specific shadows
const shadowStyles = Platform.select({
  ios: {
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  android: {
    elevation: 5,
  },
  web: {
    boxShadow: "0 2px 4px rgba(0,0,0,0.25)",
  },
});
```

### 3. Layout Differences

- Bottom tabs work differently on web vs native
- Drawer navigation may need different treatment
- Touch vs mouse interactions differ

### 4. Gesture Handling

```tsx
// Web may need different gesture handlers
const gestureConfig = Platform.select({
  web: { enabled: false }, // Disable on web if using mouse
  default: { enabled: true },
});
```

## Implementation Patterns

### Pattern 1: Platform-Specific Hook

```tsx
// hooks/useSaveImage.ts
import { Platform } from "react-native";

/**
 * Hook for saving images with platform-specific implementations.
 */
export const useSaveImage = () => {
  const saveImage = useCallback(async (imageRef: React.RefObject<View>) => {
    if (Platform.OS === "web") {
      // Web implementation using dom-to-image
      const dataUrl = await domtoimage.toJpeg(imageRef.current);
      const link = document.createElement("a");
      link.download = "image.jpeg";
      link.href = dataUrl;
      link.click();
    } else {
      // Native implementation using view-shot
      const uri = await captureRef(imageRef);
      await MediaLibrary.saveToLibraryAsync(uri);
    }
  }, []);

  return { saveImage };
};
```

### Pattern 2: Platform-Specific Component Files

```tsx
// components/Modal/ModalView.native.tsx
import { Modal as RNModal } from "react-native";

const ModalView = ({ visible, children }: ModalViewProps) => (
  <RNModal visible={visible} animationType="slide">
    {children}
  </RNModal>
);

// components/Modal/ModalView.web.tsx
const ModalView = ({ visible, children }: ModalViewProps) =>
  visible ? (
    <div className="modal-overlay">
      <div className="modal-content">{children}</div>
    </div>
  ) : null;
```

### Pattern 3: Conditional Feature Loading

```tsx
// Only import heavy libraries on platforms that need them
const loadPlatformModule = async () => {
  if (Platform.OS === "web") {
    return await import("dom-to-image");
  }
  return await import("react-native-view-shot");
};
```

## Validation Checklist

Before submitting code, verify:

- [ ] Component renders correctly on iOS
- [ ] Component renders correctly on Android
- [ ] Component renders correctly on web
- [ ] Platform-specific files in `app/` have base versions
- [ ] All Platform.OS checks handle all three platforms (or use `default`)
- [ ] No web-incompatible APIs are called without Platform checks
- [ ] Styles work on all platforms (shadows, layouts)
- [ ] Touch/gesture handlers work on all platforms
- [ ] No hardcoded platform assumptions

## Running Validation

To validate cross-platform compliance:

```bash
python3 .claude/skills/cross-platform-compatibility/scripts/validate_cross_platform.py [path]
```

## Reference Documentation

For detailed patterns and examples:

- `references/platform-api.md` - Platform module API reference
- `references/file-extensions.md` - File extension patterns and resolution
- `references/common-issues.md` - Platform-specific issues and solutions
