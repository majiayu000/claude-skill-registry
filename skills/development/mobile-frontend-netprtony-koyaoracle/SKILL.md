---
name: mobile-frontend
description: React Native patterns, NativeWind styling, React Native Reusables components, mobile-specific patterns
---

# Mobile Frontend Skill

## Core Principles

1. **Every Text Must Be Styled** - React Native doesn't cascade styles; every Text component needs direct className
2. **Event-Driven Hooks** - Subscribe to specific events only, not all events
3. **Shared Service Instances** - Use ActivityRecorderProvider for single service instance across components
4. **Semantic Colors** - Always use design tokens (text-foreground, bg-background, etc.)
5. **Consume-Once Navigation** - Use activitySelectionStore for complex object navigation instead of URL params
6. **Platform-Specific Code** - Use NativeWind classes (ios:pt-12 android:pt-6) for platform differences

## Patterns to Follow

### Pattern 1: Text Styling (CRITICAL)

**When to use**: Every single Text component in the app
**Why**: React Native has no style inheritance

```tsx
// ❌ BAD - Text inherits nothing
<View className="text-foreground">
  <Text>This text has no color!</Text>
</View>

// ✅ GOOD - Direct styling on every Text
<View className="bg-background">
  <Text className="text-foreground font-semibold">Title</Text>
  <Text className="text-muted-foreground text-sm">Subtitle</Text>
</View>

// ✅ GOOD - Semantic color variants
<Text variant="h1" className="text-foreground">Heading</Text>
<Text variant="p" className="text-foreground">Paragraph</Text>
<Text variant="muted" className="text-muted-foreground">Secondary</Text>
```

**Key Points**:

- Style every Text element explicitly
- Use semantic color classes: `text-foreground`, `text-muted-foreground`, `text-destructive`
- Use variant prop when available on Text component
- TextClassContext can provide default styling in custom components

### Pattern 2: React Native Reusables Icon Usage

**When to use**: Any time you need an icon
**Why**: Provides consistent styling and theming

```tsx
import { Icon } from '@/components/ui/icon';
import { Home, Activity, Settings } from 'lucide-react-native';

// ✅ CORRECT - Icon wrapper component
<Icon as={Home} size={24} className="text-foreground" />

// ✅ CORRECT - In Button
<Button variant="default">
  <Icon as={Activity} size={18} />
  <Text className="text-primary-foreground">Start</Text>
</Button>

// ❌ WRONG - Direct icon usage
<Home size={24} /> {/* No styling context */
```

**Key Points**:

- Always use `<Icon as={IconComponent} />` pattern
- Icons automatically get theme colors
- Can override with className
- Works inside Button/Card components

### Pattern 3: Shared Service via Provider

**When to use**: ActivityRecorder service across multiple screens
**Why**: Ensures single service instance, prevents state fragmentation

```tsx
// ✅ GOOD - Single shared instance
// In recording layout (_layout.tsx)
<ActivityRecorderProvider profile={profile}>
  <Stack />
</ActivityRecorderProvider>;

// In any screen
function RecordScreen() {
  const service = useSharedActivityRecorder(); // Same instance everywhere
  const state = useRecordingState(service);
  // ...
}

// ❌ BAD - Multiple instances
function Screen1() {
  const service = useActivityRecorder(profile); // Different instance
}
function Screen2() {
  const service = useActivityRecorder(profile); // Different instance
}
```

**Key Points**:

- Wrap recording screens with ActivityRecorderProvider
- Use `useSharedActivityRecorder()` to access service
- Service state persists across navigation
- Automatic cleanup on unmount

### Pattern 4: Event-Driven Hook Subscriptions

**When to use**: Subscribing to ActivityRecorder events
**Why**: Prevents unnecessary re-renders, optimizes performance

```tsx
// ✅ GOOD - Subscribe to specific event
export function useRecordingState(
  service: ActivityRecorderService | null,
): RecordingState {
  const [state, setState] = useState<RecordingState>(
    service?.state ?? "pending",
  );

  useEffect(() => {
    if (!service) return;

    setState(service.state);

    const subscription = service.addListener("stateChanged", (newState) => {
      setState(newState);
    });

    return () => subscription.remove(); // Always clean up
  }, [service]);

  return state;
}

// ❌ BAD - Subscribe to all events
useEffect(() => {
  const sub = service.onAnyEvent(() => {
    setNeedsUpdate(true); // Re-render entire component on any event
  });
  return () => sub.remove();
}, [service]);
```

**Key Points**:

- Use specific hooks: `useRecordingState`, `useCurrentReadings`, `useSessionStats`
- Each hook subscribes to specific events only
- Always return cleanup function
- Component only re-renders when subscribed values change

### Pattern 5: Consume-Once Navigation Store

**When to use**: Navigating with complex objects (activity plans, activity selection)
**Why**: URL params can't encode complex objects

```tsx
// ✅ GOOD - Use selection store
// In source screen
activitySelectionStore.setSelection({ category: "run", location: "outdoor" });
router.push("/(internal)/record");

// In destination screen
const selection = activitySelectionStore.peekSelection();
if (selection) {
  service.selectActivityFromPayload(selection);
  activitySelectionStore.consumeSelection(); // Clear after use
}

// ❌ BAD - URL params for complex objects
router.push({
  pathname: "/record",
  params: { plan: activityPlan }, // Serialization fails
});
```

**Key Points**:

- Store complex objects before navigation
- Consume once in destination screen
- Clear selection after reading
- Handles navigation back gracefully

### Pattern 6: NativeWind Platform-Specific Styling

**When to use**: Different styling for iOS vs Android
**Why**: Platform-specific design guidelines

```tsx
// ✅ GOOD - Platform variants
<View className="ios:pt-12 android:pt-6 bg-background">
  <Text className="ios:text-lg android:text-base text-foreground">
    Platform Text
  </Text>
</View>;

// ✅ GOOD - Safe area handling
import { useSafeAreaInsets } from "react-native-safe-area-context";

function Screen() {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ paddingTop: insets.top }} className="flex-1 bg-background">
      {/* Content */}
    </View>
  );
}
```

**Key Points**:

- Use `ios:` and `android:` prefixes
- Combine with safe area insets for notch handling
- Platform.select() for complex conditional logic

### Pattern 7: Form Mutation with Retry

**When to use**: Creating/updating data with forms
**Why**: Automatic retry, error handling, field error mapping

```tsx
import { useFormMutation } from "@/lib/hooks/useFormMutation";

const mutation = useFormMutation({
  mutationFn: async (data) => trpc.activities.create.mutate(data),
  form, // React Hook Form instance (optional)
  invalidateQueries: [["activities"]],
  successMessage: "Activity created!",
  retryAttempts: 2,
  onSuccess: () => router.back(),
  onError: (error) => {
    // Field errors automatically mapped to form
    toast.error(error.message);
  },
});

<Button
  onPress={form.handleSubmit(mutation.mutate)}
  disabled={mutation.isLoading}
>
  <Text className="text-primary-foreground">
    {mutation.isLoading ? "Creating..." : "Create"}
  </Text>
</Button>;
```

**Key Points**:

- Automatic network error retry with exponential backoff
- Field errors mapped to React Hook Form
- Cache invalidation on success
- Loading/success/error states built-in

### Pattern 8: Memoized List Items

**When to use**: FlatList with many items
**Why**: Prevents unnecessary re-renders

```tsx
import { memo } from "react";

export const ActivityListItem = memo(
  ({ activity, onPress }: Props) => {
    return (
      <TouchableOpacity onPress={onPress}>
        <Text className="text-foreground">{activity.name}</Text>
      </TouchableOpacity>
    );
  },
  (prev, next) => {
    // Custom comparison - return true if equal (DON'T re-render)
    return (
      prev.activity.id === next.activity.id &&
      prev.activity.name === next.activity.name &&
      prev.activity.distance_meters === next.activity.distance_meters
    );
  },
);

ActivityListItem.displayName = "ActivityListItem";

// Usage in FlatList
<FlatList
  data={activities}
  renderItem={({ item }) => (
    <ActivityListItem activity={item} onPress={handlePress} />
  )}
  keyExtractor={(item) => item.id}
/>;
```

**Key Points**:

- Use React.memo with custom comparison
- Compare only fields that affect rendering
- Set displayName for debugging
- Use with FlatList for best performance

## Anti-Patterns to Avoid

### Anti-Pattern 1: Multiple Service Instances

**Problem**: Each component gets different service, sensors not shared

```tsx
// ❌ BAD
function Screen1() {
  const service = useActivityRecorder(profile); // Instance A
}
function Screen2() {
  const service = useActivityRecorder(profile); // Instance B - different!
}

// ✅ CORRECT
<ActivityRecorderProvider profile={profile}>
  <Screen1 />
  <Screen2 />
</ActivityRecorderProvider>;

function Screen1() {
  const service = useSharedActivityRecorder(); // Same instance
}
function Screen2() {
  const service = useSharedActivityRecorder(); // Same instance
}
```

### Anti-Pattern 2: Forgetting Subscription Cleanup

**Problem**: Memory leaks from event listeners

```tsx
// ❌ BAD
useEffect(() => {
  service.addListener("stateChanged", handleStateChange);
  // Missing cleanup!
}, [service]);

// ✅ CORRECT
useEffect(() => {
  const subscription = service.addListener("stateChanged", handleStateChange);
  return () => subscription.remove(); // Always clean up
}, [service]);
```

### Anti-Pattern 3: Over-Subscribing to Events

**Problem**: Component re-renders on every event

```tsx
// ❌ BAD
useEffect(() => {
  const sub = service.onAnyEvent(() => {
    setNeedsUpdate(true); // Re-render on ANY event
  });
  return () => sub.remove();
}, [service]);

// ✅ CORRECT
const readings = useCurrentReadings(service); // Only re-renders on sensor updates
const stats = useSessionStats(service); // Only re-renders on stat changes
```

### Anti-Pattern 4: Missing TextClassContext in Custom Components

**Problem**: Text inside custom button has no styling

```tsx
// ❌ BAD
function CustomButton({ children }) {
  return (
    <Pressable>
      <Text>{children}</Text> {/* No styling context */}
    </Pressable>
  );
}

// ✅ CORRECT
function CustomButton({ children, textClassName }) {
  return (
    <TextClassContext.Provider value={textClassName}>
      <Pressable>
        <Text>{children}</Text> {/* Gets context styling */}
      </Pressable>
    </TextClassContext.Provider>
  );
}
```

## File Organization

```
apps/mobile/
├── app/                        # Expo Router screens
│   ├── (external)/            # Public routes
│   ├── (internal)/
│   │   ├── (tabs)/           # Tab navigation
│   │   ├── (standard)/       # Stack navigation
│   │   └── record/           # Recording flow
├── components/
│   ├── ui/                    # React Native Reusables
│   ├── recording/             # Recording UI
│   ├── activity/              # Activity components
│   └── shared/                # Shared components
├── lib/
│   ├── hooks/                 # Custom hooks
│   │   └── useActivityRecorder.ts  # 8 specialized hooks
│   ├── stores/                # Zustand stores
│   ├── services/              # Business logic
│   └── providers/             # React Context providers
└── assets/
```

## Naming Conventions

- **Components**: `PascalCase` → `ActivityCard.tsx`, `RecordingFooter.tsx`
- **Hooks**: `camelCase` with `use` prefix → `useActivityRecorder.ts`, `useFormMutation.ts`
- **Stores**: `camelCase` with `Store` suffix → `authStore.ts`, `activitySelectionStore.ts`
- **Utilities**: `camelCase` → `formatDuration.ts`
- **Constants**: `SCREAMING_SNAKE_CASE` → `MAX_HEART_RATE = 220`

## Common Scenarios

### Scenario 1: Creating a New Recording Screen Component

**Approach**:

1. Import service from provider
2. Use specific hooks for data needs
3. Style all Text elements
4. Handle loading/error states
5. Wrap with ErrorBoundary

**Example**:

```tsx
import { useSharedActivityRecorder } from "@/lib/providers/ActivityRecorderProvider";
import {
  useRecordingState,
  useCurrentReadings,
} from "@/lib/hooks/useActivityRecorder";
import { ErrorBoundary, ScreenErrorFallback } from "@/components/ErrorBoundary";

function RecordingMetrics() {
  const service = useSharedActivityRecorder();
  const state = useRecordingState(service);
  const readings = useCurrentReadings(service);

  if (!service) {
    return <Text className="text-muted-foreground">Loading...</Text>;
  }

  return (
    <View className="p-4 bg-card">
      <Text className="text-foreground text-lg font-semibold">
        {readings.heartRate ? `${readings.heartRate} bpm` : "--"}
      </Text>
    </View>
  );
}

export default function RecordingMetricsWithErrorBoundary() {
  return (
    <ErrorBoundary fallback={ScreenErrorFallback}>
      <RecordingMetrics />
    </ErrorBoundary>
  );
}
```

### Scenario 2: Form with Validation and Submission

**Approach**:

1. Use React Hook Form + Zod
2. Use useFormMutation for submission
3. Handle field errors automatically
4. Show loading state on button

**Example**:

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { activitySchema } from "@repo/core/schemas";
import { useFormMutation } from "@/lib/hooks/useFormMutation";
import { trpc } from "@/lib/trpc";

function CreateActivityForm() {
  const form = useForm({
    resolver: zodResolver(activitySchema),
    defaultValues: { name: "", type: "run", distance: 0 },
  });

  const mutation = useFormMutation({
    mutationFn: async (data) => trpc.activities.create.mutate(data),
    form,
    invalidateQueries: [["activities"]],
    successMessage: "Activity created!",
    onSuccess: () => router.back(),
  });

  return (
    <View className="p-4">
      <Input
        {...form.register("name")}
        placeholder="Activity name"
        className="bg-background"
      />
      {form.formState.errors.name && (
        <Text className="text-destructive text-sm">
          {form.formState.errors.name.message}
        </Text>
      )}

      <Button
        onPress={form.handleSubmit(mutation.mutate)}
        disabled={mutation.isLoading}
        className="mt-4"
      >
        <Text className="text-primary-foreground">
          {mutation.isLoading ? "Creating..." : "Create"}
        </Text>
      </Button>
    </View>
  );
}
```

## Dependencies

**Required**:

- `expo` v54+
- `expo-router` v6+
- `react-native-reusables` (shadcn-inspired components)
- `nativewind` v4
- `lucide-react-native` (icons)
- `@tanstack/react-query` v5
- `zustand` (state management)

**Optional**:

- `react-hook-form` + `@hookform/resolvers` (complex forms)
- `expo-location` (GPS tracking)
- `expo-sensors` (device sensors)

**Forbidden**:

- Never import from `@repo/supabase` directly (use tRPC)
- Never import database clients in mobile app

## Testing Requirements

- Test component rendering with React Native Testing Library
- Test hooks with renderHook from testing library
- Mock services/stores for isolated testing
- Test event handler callbacks with jest.fn()
- Test navigation with mocked router

## Checklist

Quick reference for mobile implementation:

- [ ] Every Text component has className with color
- [ ] Icons use `<Icon as={Component} />` pattern
- [ ] Service accessed via useSharedActivityRecorder
- [ ] Event subscriptions cleaned up in useEffect
- [ ] Complex navigation uses selection store
- [ ] Platform-specific styles use ios:/android: prefixes
- [ ] Forms use useFormMutation for submissions
- [ ] List items memoized with custom comparison
- [ ] Error boundaries wrap screens
- [ ] Safe area insets handled for notches

## Related Skills

- [Core Package Skill](./core-package-skill.md) - Pure function patterns
- [Backend Skill](./backend-skill.md) - tRPC integration
- [Testing Skill](./testing-skill.md) - Mobile testing patterns

## Version History

- **1.0.0** (2026-01-21): Initial version based on codebase analysis

---

**Next Review**: 2026-02-21
