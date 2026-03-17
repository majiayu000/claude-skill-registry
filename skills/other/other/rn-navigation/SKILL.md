---
name: rn-navigation
description: Expo Router navigation patterns for React Native. Use when implementing navigation, routing, deep links, tab bars, modals, or handling navigation state in Expo apps.
---

# React Native Navigation (Expo Router)

## File-Based Routing Fundamentals

Expo Router uses file-system based routing. Files in `app/` become routes.

### Route Structure

```
app/
├── _layout.tsx          # Root layout (providers, global UI)
├── index.tsx            # "/" route
├── (tabs)/              # Tab group (parentheses = layout group)
│   ├── _layout.tsx      # Tab bar configuration
│   ├── home.tsx         # "/home" tab
│   └── profile.tsx      # "/profile" tab
├── (auth)/              # Auth flow group
│   ├── _layout.tsx      # Auth-specific layout
│   ├── login.tsx        # "/login"
│   └── register.tsx     # "/register"
├── settings/
│   ├── index.tsx        # "/settings"
│   └── [id].tsx         # "/settings/123" (dynamic)
└── [...missing].tsx     # Catch-all 404
```

### Layout Groups `(groupName)`

Parentheses create layout groups - they affect layout hierarchy but not URL:

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen 
        name="home" 
        options={{ 
          title: 'Home',
          tabBarIcon: ({ color }) => <HomeIcon color={color} />,
        }} 
      />
      <Tabs.Screen 
        name="profile" 
        options={{ title: 'Profile' }} 
      />
    </Tabs>
  );
}
```

### Dynamic Routes `[param]`

```typescript
// app/player/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function PlayerScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  
  return <PlayerProfile playerId={id} />;
}
```

### Catch-All Routes `[...slug]`

```typescript
// app/[...missing].tsx
import { Link, Stack } from 'expo-router';

export default function NotFound() {
  return (
    <>
      <Stack.Screen options={{ title: 'Not Found' }} />
      <Link href="/">Go home</Link>
    </>
  );
}
```

## Navigation Patterns

### Programmatic Navigation

```typescript
import { useRouter, Link } from 'expo-router';

function MyComponent() {
  const router = useRouter();
  
  // Navigate with push (adds to stack)
  router.push('/player/123');
  
  // Navigate with params
  router.push({
    pathname: '/player/[id]',
    params: { id: '123' },
  });
  
  // Replace current screen (no back)
  router.replace('/home');
  
  // Go back
  router.back();
  
  // Navigate to root
  router.navigate('/');
  
  // Dismiss modal
  router.dismiss();
}
```

### Link Component

```tsx
import { Link } from 'expo-router';

// Simple link
<Link href="/settings">Settings</Link>

// With params
<Link href={{ pathname: '/player/[id]', params: { id: '123' } }}>
  View Player
</Link>

// As button
<Link href="/schedule" asChild>
  <Pressable>
    <Text>View Schedule</Text>
  </Pressable>
</Link>

// Replace instead of push
<Link href="/home" replace>Home</Link>
```

## Stack Navigation

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen 
        name="modal" 
        options={{ presentation: 'modal' }} 
      />
      <Stack.Screen 
        name="player/[id]" 
        options={{ 
          headerTitle: 'Player',
          headerBackTitle: 'Back',
        }} 
      />
    </Stack>
  );
}
```

### Dynamic Header Options

```typescript
// app/player/[id].tsx
import { Stack, useLocalSearchParams } from 'expo-router';

export default function PlayerScreen() {
  const { id } = useLocalSearchParams();
  const player = usePlayer(id);
  
  return (
    <>
      <Stack.Screen 
        options={{ 
          headerTitle: player?.name ?? 'Loading...',
          headerRight: () => (
            <EditButton playerId={id} />
          ),
        }} 
      />
      <PlayerProfile player={player} />
    </>
  );
}
```

## Modals

```typescript
// Present as modal from anywhere
router.push('/booking-modal');

// app/booking-modal.tsx
import { Stack, useRouter } from 'expo-router';

export default function BookingModal() {
  const router = useRouter();
  
  const handleComplete = () => {
    router.dismiss(); // or router.back()
  };
  
  return (
    <>
      <Stack.Screen 
        options={{ 
          presentation: 'modal',
          headerLeft: () => (
            <Button title="Cancel" onPress={() => router.dismiss()} />
          ),
        }} 
      />
      <BookingForm onComplete={handleComplete} />
    </>
  );
}

// In _layout.tsx, configure the modal screen
<Stack.Screen 
  name="booking-modal" 
  options={{ 
    presentation: 'modal',
    headerShown: true,
  }} 
/>
```

## Deep Linking

### Configure scheme in app.json

```json
{
  "expo": {
    "scheme": "myapp",
    "ios": {
      "bundleIdentifier": "com.yourcompany.myapp",
      "associatedDomains": ["applinks:yourdomain.com"]
    }
  }
}
```

### Test deep links

```bash
# iOS Simulator
npx uri-scheme open "myapp://player/123" --ios

# Physical device
npx expo start --dev-client
# Then open myapp://player/123 in Safari
```

### Universal Links (iOS)

1. Add `associatedDomains` to app.json
2. Host `apple-app-site-association` file at `https://yourdomain.com/.well-known/apple-app-site-association`:

```json
{
  "applinks": {
    "apps": [],
    "details": [{
      "appID": "TEAMID.com.yourcompany.myapp",
      "paths": ["/player/*", "/schedule/*"]
    }]
  }
}
```

### Handle incoming links

```typescript
// app/_layout.tsx
import { useEffect } from 'react';
import * as Linking from 'expo-linking';
import { useRouter } from 'expo-router';

export default function RootLayout() {
  const router = useRouter();
  
  useEffect(() => {
    // Handle link that opened the app
    Linking.getInitialURL().then((url) => {
      if (url) handleDeepLink(url);
    });
    
    // Handle links while app is open
    const subscription = Linking.addEventListener('url', ({ url }) => {
      handleDeepLink(url);
    });
    
    return () => subscription.remove();
  }, []);
  
  function handleDeepLink(url: string) {
    const { path, queryParams } = Linking.parse(url);
    // Expo Router handles most cases automatically
    // Custom logic here for special cases
  }
  
  return <Stack />;
}
```

## Common Patterns

### Auth-Protected Routes

See `rn-auth` skill for full auth context pattern. Key navigation piece:

```typescript
// app/_layout.tsx
export default function RootLayout() {
  const { token, isLoading } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;
    
    const inAuthGroup = segments[0] === '(auth)';
    
    if (!token && !inAuthGroup) {
      router.replace('/(auth)/login');
    } else if (token && inAuthGroup) {
      router.replace('/(tabs)/home');
    }
  }, [token, isLoading]);

  return (
    <Stack>
      <Stack.Screen name="(auth)" options={{ headerShown: false }} />
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
  );
}
```

### Preventing Back Navigation

```typescript
// After login success, replace to prevent back to login
router.replace('/(tabs)/home');

// For onboarding completion
router.replace('/home');

// In screen options
<Stack.Screen 
  name="checkout-complete" 
  options={{ 
    headerBackVisible: false,
    gestureEnabled: false, // Prevent swipe back
  }} 
/>
```

### Passing Data Between Screens

```typescript
// Option 1: URL params (simple data, survives refresh)
router.push({
  pathname: '/confirm',
  params: { date: '2025-01-15', courtId: '5' },
});

// Reading
const { date, courtId } = useLocalSearchParams();

// Option 2: Global state for complex data (doesn't survive refresh)
// Use context, zustand, or similar
```

## Debugging Navigation

### Log current route

```typescript
import { usePathname, useSegments } from 'expo-router';

function DebugNav() {
  const pathname = usePathname();
  const segments = useSegments();
  
  console.log('Current path:', pathname);
  console.log('Segments:', segments);
  
  return null;
}
```

### Common issues

| Issue | Solution |
|-------|----------|
| Screen not found | Check file name matches route, check `_layout.tsx` includes screen |
| Tabs not showing | Ensure tab screens are direct children of tab `_layout.tsx` |
| Back button missing | Check `headerShown` in parent and child layouts |
| Deep link not working | Verify scheme in app.json, test with `uri-scheme` CLI |
| Params undefined | Use `useLocalSearchParams` not `useSearchParams` |
