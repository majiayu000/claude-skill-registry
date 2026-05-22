---
name: react-native-navigation-builder
description: Creates navigation structures following the app's nested navigator pattern. Handles type-safe navigation, stack and tab setup, and screen parameter management in Fitness Tracker App.
---

# React Native Navigation Builder

This skill helps create and maintain the navigation structure of the Fitness Tracker App, ensuring type safety and consistency across nested navigators.

## When to Use This Skill

Use this skill when you need to:
- Add a new screen to the `AppStack` or `MainTabs`
- Create a new nested navigator (e.g., a sub-stack or tabs)
- Define navigation types for new routes
- Set up screen props for components
- Configure navigation options (headers, tab bar, presentation modes)

## Navigation Structure

The app uses a nested navigation structure:
1. **AppNavigator**: The top-level `NavigationContainer`.
2. **AppStack**: A `NativeStack` containing global screens (Welcome, Legal, Modals) and the `MainTabs`.
3. **MainTabs**: A `BottomTab` navigator for the primary app features (Home, Capture, Map, Profile).

## Type Safety

### Defining Parameters
```typescript
// app/navigators/navigationTypes.ts
export type AppStackParamList = {
  Welcome: undefined
  MainTabs: NavigatorScreenParams<MainTabParamList>
  RoutineDetail: { routineId: string }
  // ...
}
```

### Screen Props
```typescript
export type AppStackScreenProps<T extends keyof AppStackParamList> = 
  NativeStackScreenProps<AppStackParamList, T>

export type MainTabScreenProps<T extends keyof MainTabParamList> = 
  CompositeScreenProps<
    BottomTabScreenProps<MainTabParamList, T>,
    AppStackScreenProps<keyof AppStackParamList>
  >
```

## Adding a New Screen

### 1. Update Param List
Add the screen name and its parameters to `navigationTypes.ts`.

### 2. Update Navigator
Add a `<Stack.Screen>` or `<Tab.Screen>` to the appropriate navigator file.

### 3. Implement Component
Use the defined props in your screen component:
```tsx
export const MyNewScreen = (props: AppStackScreenProps<"MyNewScreen">) => {
  const { navigation, route } = props
  // ...
}
```

## Common Patterns

### Modal Presentation
```tsx
<Stack.Screen
  name="RoutineEdit"
  component={RoutineEditScreen}
  options={{ presentation: "modal" }}
/>
```

### Tab Bar Icons
```tsx
<Tab.Screen
  name="Home"
  component={HomeScreen}
  options={{
    tabBarLabel: "Home",
    tabBarIcon: ({ color }) => <Home size={24} color={color} />,
  }}
/>
```

## References

See [NAVIGATION_TYPES.md](references/NAVIGATION_TYPES.md) for detailed type patterns.

See [NAVIGATOR_SETUP.md](references/NAVIGATOR_SETUP.md) for stack and tab configuration examples.
