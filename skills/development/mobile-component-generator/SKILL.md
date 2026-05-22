---
name: mobile-component-generator
description: Generates React Native components following GradientPeak mobile patterns with NativeWind styling, React Native Reusables, and proper hooks.
---

# Mobile Component Generator Skill

## When to Use

- User asks to create a new mobile component
- User wants to add a new screen/modal
- User needs a list component with data fetching
- User asks to generate UI for a feature

## What This Skill Does

1. Analyzes component requirements from user request
2. Determines component type (smart vs presentational)
3. Generates component with proper patterns:
   - NativeWind styling (every Text styled directly)
   - React Native Reusables UI components
   - Proper imports and exports
   - TypeScript types
   - Error boundaries if needed
4. Adds to proper directory structure
5. Generates basic tests if requested

## Component Types Generated

### 1. List Component

FlashList/FlatList with loading, empty, and error states

### 2. Card Component

Presentational component with props, React.memo for performance

### 3. Modal Component

With form integration using React Native Reusables

### 4. Screen Component

With navigation (Expo Router) and data fetching

## Styling Patterns

### Every Text Must Be Styled

```tsx
// WRONG - Text won't have color
<View className="text-foreground">
  <Text>This has no color!</Text>
</View>

// CORRECT - Direct styling
<View>
  <Text className="text-foreground">This has color!</Text>
</View>
```

### Semantic Colors

```tsx
<View className="bg-background border-border">
  <Text className="text-foreground font-semibold">Title</Text>
  <Text className="text-muted-foreground">Subtitle</Text>
  <Button className="bg-primary">
    <Text className="text-primary-foreground">Action</Text>
  </Button>
</View>
```

### Platform-Specific

```tsx
<View className="ios:pt-12 android:pt-6">
  <Text className="text-foreground">Platform-aware padding</Text>
</View>
```

## Directory Structure

```
components/
├── ui/               # React Native Reusables
├── shared/           # Cross-domain shared components
├── activity/         # Activity-specific components
├── recording/        # Recording-specific components
└── training-plan/    # Training plan components
```

## Critical Patterns

- Style every `<Text>` component directly
- Use React Native Reusables from `@/components/ui/`
- Use `activitySelectionStore` for cross-screen state
- Add `React.memo` for list items
- Include accessibility props
- Use TypeScript strict types
- Handle loading, error, and empty states
