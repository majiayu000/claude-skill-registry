---
name: react-native-patterns
description: React Native component and interaction patterns. Use when building Pressable components, ScrollViews, lists, bottom sheets, accessibility, navigation, or handling RN-specific requirements like Text wrapping and touch targets.
---

# React Native Patterns

## Overview

Patterns for building maintainable React Native components. Covers touch interactions (Pressable), list rendering (FlashList), modal patterns (bottom sheets), accessibility, navigation, and RN-specific requirements that differ from web React.

> For React web patterns (hooks, context, composition), see the **react-patterns** skill.

## Workflows

**Building an interactive screen:**
1. [ ] Set up SafeAreaView or apply safe area insets
2. [ ] Use Pressable for all interactive elements (44pt minimum)
3. [ ] Add haptic feedback on primary actions
4. [ ] Use FlashList for lists, ScrollView for fixed content
5. [ ] Implement bottom sheet for detail/modal views
6. [ ] Add accessibility labels to all interactive elements
7. [ ] Test on device for touch targets and scroll performance

## Guidance

### Pressable (not TouchableOpacity)

`Pressable` is the standard touch component. `TouchableOpacity` is deprecated.

Key principles:
- **44pt minimum touch target** on all interactive elements
- Use `hitSlop` to expand touch area beyond visual bounds: `hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}`
- Style feedback via `style` function: `style={({ pressed }) => [pressed && { opacity: 0.7 }]}`
- Or use NativeWind: `className="active:opacity-70"`
- Add haptics on press for primary actions: `onPress={() => { Haptics.impactAsync(); doAction(); }}`

### Text-Only Strings Rule

React Native requires all visible text to be wrapped in `<Text>`:

```
✅ <View><Text>Hello</Text></View>
❌ <View>Hello</View>  // Crashes at runtime
```

This applies to conditional renders, string interpolation, and JSX expressions. Always wrap strings in Text.

### ScrollView Patterns

Two className targets:
- `className` — outer container (flex, background)
- `contentContainerClassName` — inner content (padding, gap, alignment)

Use `ScrollView` for screens with fixed, non-dynamic content. Use `FlashList` for dynamic lists.

`showsVerticalScrollIndicator={false}` for cleaner visual when custom scroll indicators are used.

### FlashList Patterns

High-performance list rendering:
- `estimatedItemSize` is **required** — estimate average item height in points
- `renderItem` receives `{ item, index }` — keep render function pure
- `keyExtractor` — use unique string ID from data
- `contentContainerClassName` — NativeWind styling for inner content
- `ItemSeparatorComponent` — consistent spacing between items
- `ListEmptyComponent` — graceful empty state

### Bottom Sheet as Modal

`@gorhom/bottom-sheet` replaces web modal dialogs:

- Define `snapPoints` array: `['25%', '50%', '90%']`
- Use `BottomSheetModal` with `BottomSheetModalProvider` for imperative control
- `BottomSheetScrollView` for scrollable sheet content
- `BottomSheetBackdrop` for press-to-dismiss overlay
- Present: `bottomSheetRef.current?.present()`
- Dismiss: `bottomSheetRef.current?.dismiss()`

### expo-image Patterns

Use for all image display:
- Remote images: `source={{ uri: 'https://...' }}`
- Local images: `source={require('../assets/image.png')}`
- Blurhash placeholder: `placeholder="LKO2?U%2Tw=w]~RBVZRi}"` for loading state
- `contentFit="cover"` for card thumbnails, `"contain"` for full images
- `transition={300}` for smooth fade-in on load

### Accessibility

Required accessibility props for interactive elements:

| Prop | Purpose | Example |
|------|---------|---------|
| `accessibilityRole` | Semantic role | `"button"`, `"link"`, `"image"` |
| `accessibilityLabel` | Screen reader text | `"Open settings"` |
| `accessibilityHint` | Action description | `"Opens the settings screen"` |
| `accessibilityState` | Dynamic state | `{ selected: true, disabled: false }` |
| `accessible` | Marks as accessible | Default `true` for Pressable |

Guidelines:
- All Pressable elements need `accessibilityLabel`
- Images need `accessibilityLabel` describing content
- Use `accessibilityRole="header"` for screen titles
- Toggle/checkbox: set `accessibilityState={{ checked: isChecked }}`
- Disabled elements: `accessibilityState={{ disabled: true }}`

### Chat-Forward Component Patterns

Demos use a chat-forward interface where the conversation thread is the primary UI.

#### Chat Screen Layout

Three zones:
- **Header**: Minimal — title, back nav, optional status. Uses safe area top inset.
- **Message stream**: FlashList or inverted ScrollView for the conversation. Agent and user messages alternate. Rich content is embedded within agent message components.
- **Input bar**: Text input pinned to bottom. Uses `KeyboardAvoidingView` (iOS) or `android:windowSoftInputMode="adjustResize"`. Safe area bottom inset for home indicator. Optional quick-action chips above the text field.

#### Message Bubble

Agent and user bubbles have distinct styling (alignment, color, shape):
- **Agent bubble**: Left-aligned, neutral background, can contain child components (cards, summaries, action buttons)
- **User bubble**: Right-aligned, accent background, text only
- Bubbles animate in with `FadeInDown.duration(300)` on append

#### Inline Rich Card

Compact data card rendered as a child of an agent message bubble:
- Photo thumbnail (expo-image) + title + key metric + status badge
- Tappable — opens bottom sheet with full detail
- For card sets: horizontal `ScrollView` within the message, or vertical stack
- Stagger animation: `FadeInDown.delay(index * 50).duration(300)`

#### Summary Card

Running totals/status that updates as the conversation progresses:
- Shows aggregated state: Keep ($X), Sell ($Y), Donate ($Z), Progress (N%)
- Can be rendered as a sticky element above the input bar for persistent visibility
- Content crossfades on update (150ms timing)

#### Prompt Card

Agent suggestion with embedded action buttons:
- Text prompt + 1-3 action buttons inline
- Buttons are Pressable with 44pt targets, haptic on press
- After tap, the prompt card updates to show the confirmed action
- E.g., *"Want me to find pickup options?"* → [Yes] [Not now]

#### Comparison View

Before/after or side-by-side content within a message:
- Two expo-image instances with labels (Before / After)
- Optional delta annotation (e.g., "New scratch detected")

#### Timeline View

Chronological event list rendered inline within an agent message:
- Compact: date + title + icon per event
- Expandable: tap to show detail (inline expand or bottom sheet)
- Vertical line connector between events

#### Notification Message

Proactive agent alert that appears as a new message in the thread:
- Distinctive styling (icon + emphasis color) to differentiate from regular agent messages
- Can contain inline action buttons
- E.g., *"Storm season starts in 6 weeks. Your basement still shows moisture risk."*

### Navigation from Components

Use Expo Router's `useRouter()` hook:

- `router.push('/path')` — navigate forward (adds to stack)
- `router.replace('/path')` — replace current screen
- `router.back()` — go back
- `router.canGoBack()` — check if back navigation possible
- Pass params: `router.push({ pathname: '/detail/[id]', params: { id: '123' } })`

## Best Practices

- Always use `Pressable` over `TouchableOpacity` or `TouchableHighlight`
- Enforce 44pt minimum touch targets — use `hitSlop` when visual is smaller
- Wrap every visible string in `<Text>` — no bare strings in JSX
- Use `expo-image` for all images (never RN `Image`)
- Add `accessibilityLabel` to every interactive element
- Use `FlashList` with `estimatedItemSize` for any list with >10 items
- Use `contentContainerClassName` for ScrollView/FlashList inner styling
- Add haptic feedback sparingly — primary actions only
- Test touch targets on real device (simulator touch is imprecise)

## Anti-Patterns

- Using `TouchableOpacity` (deprecated — use Pressable)
- Touch targets smaller than 44pt without `hitSlop` compensation
- Bare strings without `<Text>` wrapper (runtime crash)
- Using RN `Image` instead of `expo-image` (no caching, no blurhash)
- Forgetting `estimatedItemSize` on FlashList
- Using `FlatList` for large datasets (FlashList is faster)
- Missing `accessibilityLabel` on interactive elements
- Using `Alert.alert()` for complex choices (use bottom sheet instead)
- Padding on `className` of ScrollView (use `contentContainerClassName`)
- Inline anonymous functions in FlashList `renderItem` (causes re-renders — extract component)
