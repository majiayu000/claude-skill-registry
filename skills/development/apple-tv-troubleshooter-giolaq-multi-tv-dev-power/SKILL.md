---
name: apple-tv-troubleshooter
displayName: "Apple TV Troubleshooter"
description: "Expert troubleshooting for Apple TV (tvOS) React Native development. Use when users have issues with Siri Remote, focus management, TVEventHandler, TVFocusGuideView, ScrollView not scrolling, tvOS-specific problems, parallax animations, or tvOS vs Android TV differences."
keywords: ["apple-tv", "tvos", "siri-remote", "focus-management", "TVEventHandler", "TVFocusGuideView", "ScrollView", "parallax", "tv-focus", "expo-tv", "react-native-tvos", "navigation", "focus-trap"]
author: "Giovanni Laquidara"
---

# Apple TV Troubleshooter

You are an expert in Apple TV (tvOS) development with React Native. This skill activates when users encounter:

- Focus management issues on Apple TV
- Siri Remote event handling problems
- TVEventHandler not capturing events
- ScrollView/FlatList not scrolling
- TVFocusGuideView configuration
- tvOS vs Android TV differences
- Expo TV build issues
- Navigation and focus traps

## tvOS Focus Engine vs Android TV

**Critical Difference:** tvOS uses a **precision-based** focus engine while Android TV uses **proximity-based**.

| Aspect | Apple TV (tvOS) | Android TV |
|--------|-----------------|------------|
| Focus Engine | Precision-based (strict alignment) | Proximity-based (nearest element) |
| Remote Input | Siri Remote touchpad (swipe + click) | D-pad directional buttons |
| Focus Recovery | Attempts automatic (inconsistent) | Moves to top-left corner |
| Screen Resolution | 1920x1080 (native) | 960x540 (scaled) |

**Implication:** UI elements must be properly aligned on tvOS or focus won't move between them.

## Siri Remote Event Handling

### Using useTVEventHandler Hook (Recommended)

```typescript
import { useTVEventHandler } from 'react-native';

function MyComponent() {
  useTVEventHandler((evt) => {
    switch (evt.eventType) {
      case 'up':
      case 'down':
      case 'left':
      case 'right':
        // Handle navigation
        break;
      case 'select':
        // Center button pressed
        break;
      case 'playPause':
        // Play/Pause button
        break;
      case 'longPlayPause':
        // Long press play/pause (tvOS only)
        break;
    }
  });

  return <View>{/* content */}</View>;
}
```

### TVEventControl for Menu and Gestures

```typescript
import { TVEventControl } from 'react-native';

// Enable Menu button handling (for back navigation)
TVEventControl.enableTVMenuKey();

// Enable pan gesture detection on Siri Remote touchpad
TVEventControl.enableTVPanGesture();

// Disable when component unmounts
TVEventControl.disableTVMenuKey();
TVEventControl.disableTVPanGesture();
```

## Common Problems & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| **ScrollView won't scroll** | Regular ScrollView needs focusable items | Use `TVTextScrollView` for swipe-based scrolling |
| **TVEventHandler doesn't fire** | No focusable component on screen | Add `hasTVPreferredFocus={true}` to parent View or ensure a Touchable exists |
| **Event fires twice** | Press and release both trigger | Known behavior - debounce or track event state |
| **InputText can't receive focus** | tvOS limitation | Use native input alternatives or custom keyboards |
| **Focus leaves FlatList unexpectedly** | Virtualization removes focused item | VirtualizedList auto-wraps with TVFocusGuideView - ensure `trapFocus` enabled |
| **Menu button doesn't work** | Not enabled by default | Call `TVEventControl.enableTVMenuKey()` |
| **Pan/swipe not detected** | Disabled by default | Call `TVEventControl.enableTVPanGesture()` |
| **Expo prebuild fails after changing EXPO_TV** | Cached native config | Always run `npx expo prebuild --clean` |
| **Flipper causes build errors** | Incompatible with TV | Set Flipper to false in Podfile, run prebuild --clean |
| **Wrong screen dimensions** | Platform difference | Use platform-specific StyleSheets |
| **Focus doesn't move diagonally** | Precision engine limitation | Ensure UI elements are aligned vertically/horizontally |
| **BackHandler doesn't work** | Different API on tvOS | Use TVEventControl.enableTVMenuKey() for menu/back |
| **Parallax not working** | Missing props | Add `tvParallaxProperties` to TouchableHighlight |
| **removeClippedSubviews breaks focus** | Clipped items lose focus | Set `removeClippedSubviews={false}` |

## TVFocusGuideView Configuration

```typescript
import { TVFocusGuideView } from 'react-native';

// Basic usage with auto-focus memory
<TVFocusGuideView autoFocus>
  <TouchableOpacity>Item 1</TouchableOpacity>
  <TouchableOpacity>Item 2</TouchableOpacity>
</TVFocusGuideView>

// Trap focus within container
<TVFocusGuideView
  trapFocusUp
  trapFocusDown
  trapFocusLeft
  trapFocusRight
>
  {/* Focus cannot escape this container */}
</TVFocusGuideView>

// Custom focus destinations
<TVFocusGuideView destinations={[buttonRef.current]}>
  {/* Guides focus to specific elements */}
</TVFocusGuideView>
```

### Key Props

| Prop | Description |
|------|-------------|
| `autoFocus` | Remembers last focused child, restores on revisit |
| `trapFocusUp/Down/Left/Right` | Prevents focus from leaving in that direction |
| `destinations` | Array of refs to guide focus toward |
| `focusable` | When false, view and children not focusable |

## Platform-Specific Components

### TVTextScrollView (for scrolling content)

```typescript
import { TVTextScrollView } from 'react-native';

// Use instead of ScrollView for non-focusable content
<TVTextScrollView>
  <Text>Long text content that should scroll with swipe...</Text>
</TVTextScrollView>
```

### Parallax Animations

```typescript
<TouchableHighlight
  tvParallaxProperties={{
    enabled: true,
    magnification: 1.1,
    pressMagnification: 1.0,
    shiftDistanceX: 5,
    shiftDistanceY: 5,
  }}
>
  <Image source={poster} />
</TouchableHighlight>
```

### Unsupported Components on tvOS

These components are **disabled or suppressed** on Apple TV:
- `StatusBar`
- `Slider`
- `Switch`
- `WebView` (limited support)

## Focus Management Best Practices

### 1. Set Default Focus on Mount

```typescript
<TouchableOpacity hasTVPreferredFocus={true}>
  Default Focused Item
</TouchableOpacity>
```

### 2. Use nextFocus Props for Custom Navigation

```typescript
<TouchableOpacity
  ref={button1Ref}
  nextFocusRight={button2Ref.current}
  nextFocusDown={button3Ref.current}
>
  Button 1
</TouchableOpacity>
```

### 3. Capture Events at Top Level

```typescript
// Good: Capture at parent level
function Screen() {
  useTVEventHandler((evt) => {
    // Handle all events here, delegate to children
  });
  return <View>{/* children */}</View>;
}

// Bad: Each small component handles its own events
function SmallButton() {
  useTVEventHandler((evt) => { /* ... */ }); // Avoid this pattern
}
```

### 4. Use React Context for Focus State

```typescript
const FocusContext = createContext({ focusedId: null, setFocused: () => {} });

function FocusProvider({ children }) {
  const [focusedId, setFocused] = useState(null);
  return (
    <FocusContext.Provider value={{ focusedId, setFocused }}>
      {children}
    </FocusContext.Provider>
  );
}
```

## Expo TV Specific Issues

### Environment Variable

```bash
# Must be set BEFORE prebuild
export EXPO_TV=1

# Always clean when changing this variable
npx expo prebuild --clean
```

### Common Expo TV Errors

| Error | Solution |
|-------|----------|
| "EXPO_TV not recognized" | Ensure using Expo SDK 50+ |
| Build fails after toggling EXPO_TV | Run `npx expo prebuild --clean` |
| Flipper errors | Disable Flipper in ios/Podfile |
| Dev menu not showing | Use SDK 54+ with RNTV 0.81 for TV dev menu support |

## Platform Detection

```typescript
import { Platform } from 'react-native';

// Check if running on any TV
if (Platform.isTV) {
  // TV-specific code
}

// Check specifically for Apple TV (not Android TV)
if (Platform.isTVOS) {
  // Apple TV only code
}

// Platform-specific styles
const styles = StyleSheet.create({
  container: {
    padding: Platform.isTVOS ? 48 : 16,
  },
});
```

## Debugging Tips

1. **LogBox works on TV** - Error display supported after RN TV 0.76+
2. **Use console.log liberally** - Metro bundler shows logs
3. **Test on real device** - Simulator misses Siri Remote nuances
4. **Check focus state** - Add `onFocus`/`onBlur` handlers to debug focus flow

## Resources

- [react-native-tvos GitHub](https://github.com/react-native-tvos/react-native-tvos)
- [React Native TV Docs](https://reactnative.dev/docs/building-for-tv)
- [Expo TV Guide](https://docs.expo.dev/guides/building-for-tv/)
- [TVFocusGuideView Guide](https://dev.to/amazonappdev/tv-navigation-in-react-native-a-guide-to-using-tvfocusguideview-302i)


---

# Cross-Platform Troubleshooting (Also Applies to Apple TV)

## TypeError: Cannot read property 'displayName' of undefined

This error affects all TV platforms including Apple TV when using Expo.

**Symptoms:**
- App builds successfully but crashes immediately on launch
- Metro shows: `ERROR TypeError: Cannot read property 'displayName' of undefined`

**Common Causes & Fixes:**

1. **Wrong import in index.js** (Most Common)
   ```javascript
   // ❌ WRONG - Named import when App uses default export
   import { App } from './App';
   
   // ✅ CORRECT - Default import
   import App from './App';
   ```

2. **Metro cache corruption**
   ```bash
   pkill -f "expo" 2>/dev/null || true
   rm -rf node_modules/.cache /tmp/metro-* /tmp/haste-map-*
   npx expo start --clear
   ```

3. **react-tv-space-navigation v6 missing configuration**
   - v6.0.0+ requires explicit remote control configuration
   - Create `src/configureRemoteControl.ts`:
   ```typescript
   import { SpatialNavigation } from 'react-tv-space-navigation';
   
   SpatialNavigation.configureRemoteControl({
     remoteControlSubscriber: (callback) => () => {},
     remoteControlUnsubscriber: () => {},
   });
   ```
   - Import at top of App.tsx: `import './src/configureRemoteControl';`

## Expo TV Build & Run Issues

### Always Use Development Builds for TV

```bash
# ❌ May cause SDK version issues on TV simulators
npx expo start

# ✅ Correct for TV development
npx expo run:ios   # Apple TV
npx expo run:android  # Android TV
# or
npx expo start --dev-client
```

### Apple TV Simulator Quick Commands

```bash
# List available simulators
xcrun simctl list devices available | grep -i tv

# Boot Apple TV simulator
xcrun simctl boot "Apple TV"

# Run app
npx expo run:ios --device "Apple TV"
```
