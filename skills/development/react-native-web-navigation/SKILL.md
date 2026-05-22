---
name: react-native-web-navigation
description: Use when implementing navigation in React Native Web projects. Provides patterns for React Navigation, deep linking, and web-specific routing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# React Native Web - Navigation

Navigation patterns for React Native Web using React Navigation, supporting both native and web platforms with a unified API.

## Key Concepts

### React Navigation

React Navigation is the standard navigation library for React Native and React Native Web:

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Type-Safe Navigation

Define navigation types for type safety:

```typescript
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Details: { id: string; title: string };
  Profile: { userId: string };
};

type HomeProps = NativeStackScreenProps<RootStackParamList, 'Home'>;
type DetailsProps = NativeStackScreenProps<RootStackParamList, 'Details'>;

function HomeScreen({ navigation }: HomeProps) {
  return (
    <Button
      title="Go to Details"
      onPress={() => navigation.navigate('Details', { id: '123', title: 'Item' })}
    />
  );
}
```

### Web URLs

React Navigation automatically handles URLs on web:

```typescript
import { LinkingOptions } from '@react-navigation/native';

const linking: LinkingOptions<RootStackParamList> = {
  prefixes: ['https://myapp.com', 'myapp://'],
  config: {
    screens: {
      Home: '',
      Details: 'details/:id',
      Profile: 'profile/:userId',
    },
  },
};

<NavigationContainer linking={linking}>
  {/* Navigator */}
</NavigationContainer>
```

## Best Practices

### Stack Navigator

✅ Use for screen-to-screen navigation:

```typescript
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator<RootStackParamList>();

function RootNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        headerStyle: {
          backgroundColor: '#007AFF',
        },
        headerTintColor: '#fff',
      }}
    >
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: 'Home' }}
      />
      <Stack.Screen
        name="Details"
        component={DetailsScreen}
        options={({ route }) => ({ title: route.params.title })}
      />
    </Stack.Navigator>
  );
}
```

### Tab Navigator

✅ Use for main app sections:

```typescript
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

const Tab = createBottomTabNavigator<TabParamList>();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const iconName = route.name === 'Home' ? 'home' : 'person';
          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

### Drawer Navigator (Web)

✅ Use for sidebar navigation on web:

```typescript
import { createDrawerNavigator } from '@react-navigation/drawer';
import { useWindowDimensions } from 'react-native';

const Drawer = createDrawerNavigator();

function DrawerNavigator() {
  const { width } = useWindowDimensions();
  const isLargeScreen = width >= 768;

  return (
    <Drawer.Navigator
      screenOptions={{
        drawerType: isLargeScreen ? 'permanent' : 'front',
        drawerStyle: {
          width: 240,
        },
      }}
    >
      <Drawer.Screen name="Home" component={HomeScreen} />
      <Drawer.Screen name="Settings" component={SettingsScreen} />
    </Drawer.Navigator>
  );
}
```

## Examples

### Complete Navigation Setup

```typescript
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

type RootStackParamList = {
  Tabs: undefined;
  Details: { id: string };
  Modal: undefined;
};

type TabParamList = {
  Home: undefined;
  Search: undefined;
  Profile: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

function TabNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

export function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Tabs"
          component={TabNavigator}
          options={{ headerShown: false }}
        />
        <Stack.Screen name="Details" component={DetailsScreen} />
        <Stack.Screen
          name="Modal"
          component={ModalScreen}
          options={{ presentation: 'modal' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Navigation with Hooks

```typescript
import { useNavigation, useRoute } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RouteProp } from '@react-navigation/native';

type DetailsScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  'Details'
>;
type DetailsScreenRouteProp = RouteProp<RootStackParamList, 'Details'>;

function DetailsScreen() {
  const navigation = useNavigation<DetailsScreenNavigationProp>();
  const route = useRoute<DetailsScreenRouteProp>();

  const { id, title } = route.params;

  return (
    <View>
      <Text>{title}</Text>
      <Button title="Go Back" onPress={() => navigation.goBack()} />
      <Button
        title="Go to Profile"
        onPress={() => navigation.navigate('Profile', { userId: id })}
      />
    </View>
  );
}
```

### Deep Linking Configuration

```typescript
import { LinkingOptions } from '@react-navigation/native';

const linking: LinkingOptions<RootStackParamList> = {
  prefixes: ['https://myapp.com', 'myapp://'],
  config: {
    screens: {
      Tabs: {
        screens: {
          Home: '',
          Search: 'search',
          Profile: 'profile',
        },
      },
      Details: 'details/:id',
      Modal: 'modal',
    },
  },
};

export function App() {
  return (
    <NavigationContainer linking={linking} fallback={<LoadingScreen />}>
      {/* Navigator */}
    </NavigationContainer>
  );
}
```

## Common Patterns

### Protected Routes

```typescript
import { useAuth } from './auth-context';

function RootNavigator() {
  const { isAuthenticated } = useAuth();

  return (
    <Stack.Navigator>
      {isAuthenticated ? (
        <>
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Profile" component={ProfileScreen} />
        </>
      ) : (
        <>
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Register" component={RegisterScreen} />
        </>
      )}
    </Stack.Navigator>
  );
}
```

### Navigation Guards

```typescript
import { useNavigation } from '@react-navigation/native';
import { useEffect } from 'react';

function ProtectedScreen() {
  const navigation = useNavigation();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      navigation.navigate('Login');
    }
  }, [isAuthenticated, navigation]);

  if (!isAuthenticated) {
    return null;
  }

  return <View>{/* Protected content */}</View>;
}
```

### Programmatic Navigation

```typescript
import { createNavigationContainerRef } from '@react-navigation/native';

// Create ref outside component
export const navigationRef = createNavigationContainerRef<RootStackParamList>();

// Use in App component
export function App() {
  return (
    <NavigationContainer ref={navigationRef}>
      {/* Navigator */}
    </NavigationContainer>
  );
}

// Navigate from anywhere
export function navigateToDetails(id: string) {
  if (navigationRef.isReady()) {
    navigationRef.navigate('Details', { id });
  }
}
```

## Anti-Patterns

❌ Don't use React Router directly (use React Navigation):

```typescript
// Bad - React Router is web-only
import { BrowserRouter, Route } from 'react-router-dom';

// Good - React Navigation works everywhere
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
```

❌ Don't pass navigation prop manually:

```typescript
// Bad
<ChildComponent navigation={navigation} />

// Good - use useNavigation hook
function ChildComponent() {
  const navigation = useNavigation();
  // ...
}
```

❌ Don't store navigation state in Redux/Context:

```typescript
// Bad - navigation state should be managed by React Navigation
const [currentScreen, setCurrentScreen] = useState('Home');

// Good - let React Navigation manage state
// Use navigation listeners if you need to react to changes
```

## Related Skills

- **react-native-web-core**: Core React Native Web concepts
- **react-native-web-styling**: Styling navigation components
- **react-native-web-testing**: Testing navigation flows
