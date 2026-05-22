---
name: jutsu-react-native:react-native-navigation
description: Use when implementing navigation in React Native apps with React Navigation. Covers stack, tab, drawer navigation, deep linking, and navigation patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# React Native Navigation

Use this skill when implementing navigation in React Native applications using React Navigation (the de facto standard navigation library).

## Key Concepts

### Installation

```bash
npm install @react-navigation/native
npm install react-native-screens react-native-safe-area-context

# For stack navigation
npm install @react-navigation/native-stack

# For tab navigation
npm install @react-navigation/bottom-tabs

# For drawer navigation
npm install @react-navigation/drawer react-native-gesture-handler react-native-reanimated
```

### Basic Setup

```tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Details: { itemId: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
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

### Stack Navigation

The most common navigation pattern:

```tsx
import React from 'react';
import { View, Text, Button } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Details: { itemId: string; title: string };
};

type HomeProps = NativeStackScreenProps<RootStackParamList, 'Home'>;
type DetailsProps = NativeStackScreenProps<RootStackParamList, 'Details'>;

function HomeScreen({ navigation }: HomeProps) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Home Screen</Text>
      <Button
        title="Go to Details"
        onPress={() =>
          navigation.navigate('Details', {
            itemId: '123',
            title: 'My Item',
          })
        }
      />
    </View>
  );
}

function DetailsScreen({ route, navigation }: DetailsProps) {
  const { itemId, title } = route.params;

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Details Screen</Text>
      <Text>Item ID: {itemId}</Text>
      <Text>Title: {title}</Text>
      <Button title="Go Back" onPress={() => navigation.goBack()} />
    </View>
  );
}
```

### Tab Navigation

Bottom tabs for primary navigation:

```tsx
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

type TabParamList = {
  Home: undefined;
  Search: undefined;
  Profile: undefined;
};

const Tab = createBottomTabNavigator<TabParamList>();

export default function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Search') {
            iconName = focused ? 'search' : 'search-outline';
          } else {
            iconName = focused ? 'person' : 'person-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

## Best Practices

### Type-Safe Navigation

Define navigation types for type safety:

```tsx
import { NativeStackScreenProps } from '@react-navigation/native-stack';

// Define param list
type RootStackParamList = {
  Home: undefined;
  Details: { itemId: string };
  UserProfile: { userId: string; name: string };
};

// Declare global types
declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}

// Use typed props
type DetailsProps = NativeStackScreenProps<RootStackParamList, 'Details'>;

function DetailsScreen({ route, navigation }: DetailsProps) {
  // route.params is fully typed
  const { itemId } = route.params;

  // navigation.navigate is type-safe
  navigation.navigate('UserProfile', {
    userId: '123',
    name: 'John',
  });

  return <View />;
}
```

### Header Customization

Customize navigation headers:

```tsx
<Stack.Navigator
  screenOptions={{
    headerStyle: {
      backgroundColor: '#007AFF',
    },
    headerTintColor: '#fff',
    headerTitleStyle: {
      fontWeight: 'bold',
    },
  }}
>
  <Stack.Screen
    name="Home"
    component={HomeScreen}
    options={{
      title: 'My Home',
      headerRight: () => (
        <Button
          onPress={() => console.log('Pressed')}
          title="Info"
          color="#fff"
        />
      ),
    }}
  />
</Stack.Navigator>
```

### Dynamic Header Options

Set header options from screen:

```tsx
import { useLayoutEffect } from 'react';

function DetailsScreen({ navigation, route }: DetailsProps) {
  useLayoutEffect(() => {
    navigation.setOptions({
      title: route.params.title,
      headerRight: () => (
        <Button title="Save" onPress={() => console.log('Save')} />
      ),
    });
  }, [navigation, route.params.title]);

  return <View />;
}
```

### Nested Navigators

Combine different navigation patterns:

```tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const HomeStack = createNativeStackNavigator();
const ProfileStack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function HomeStackScreen() {
  return (
    <HomeStack.Navigator>
      <HomeStack.Screen name="Home" component={HomeScreen} />
      <HomeStack.Screen name="Details" component={DetailsScreen} />
    </HomeStack.Navigator>
  );
}

function ProfileStackScreen() {
  return (
    <ProfileStack.Navigator>
      <ProfileStack.Screen name="Profile" component={ProfileScreen} />
      <ProfileStack.Screen name="Settings" component={SettingsScreen} />
    </ProfileStack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="HomeTab" component={HomeStackScreen} />
        <Tab.Screen name="ProfileTab" component={ProfileStackScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

## Common Patterns

### Authentication Flow

```tsx
import React, { useState } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

type RootStackParamList = {
  SignIn: undefined;
  SignUp: undefined;
  Home: undefined;
  Details: { itemId: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  const [isSignedIn, setIsSignedIn] = useState(false);

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {!isSignedIn ? (
          // Auth screens
          <>
            <Stack.Screen name="SignIn" component={SignInScreen} />
            <Stack.Screen name="SignUp" component={SignUpScreen} />
          </>
        ) : (
          // App screens
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Details" component={DetailsScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Deep Linking

Configure deep linking:

```tsx
import { NavigationContainer } from '@react-navigation/native';

const linking = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Home: 'home',
      Details: 'details/:itemId',
      UserProfile: 'user/:userId',
    },
  },
};

export default function App() {
  return (
    <NavigationContainer linking={linking}>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
        <Stack.Screen name="UserProfile" component={UserProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Modal Navigation

Present screens as modals:

```tsx
<Stack.Navigator>
  <Stack.Group>
    <Stack.Screen name="Home" component={HomeScreen} />
    <Stack.Screen name="Details" component={DetailsScreen} />
  </Stack.Group>
  <Stack.Group screenOptions={{ presentation: 'modal' }}>
    <Stack.Screen name="CreatePost" component={CreatePostScreen} />
    <Stack.Screen name="Settings" component={SettingsScreen} />
  </Stack.Group>
</Stack.Navigator>
```

### Navigation Guards

Protect routes with guards:

```tsx
import { useEffect } from 'react';

function ProtectedScreen({ navigation }: any) {
  const isAuthenticated = useAuth(); // Custom hook

  useEffect(() => {
    if (!isAuthenticated) {
      navigation.replace('SignIn');
    }
  }, [isAuthenticated, navigation]);

  if (!isAuthenticated) {
    return null; // Or loading screen
  }

  return <View>{/* Protected content */}</View>;
}
```

### Custom Tab Bar

Create custom tab bar:

```tsx
import { View, Text, TouchableOpacity } from 'react-native';

function CustomTabBar({ state, descriptors, navigation }: any) {
  return (
    <View style={{ flexDirection: 'row', height: 60 }}>
      {state.routes.map((route: any, index: number) => {
        const { options } = descriptors[route.key];
        const isFocused = state.index === index;

        const onPress = () => {
          const event = navigation.emit({
            type: 'tabPress',
            target: route.key,
            canPreventDefault: true,
          });

          if (!isFocused && !event.defaultPrevented) {
            navigation.navigate(route.name);
          }
        };

        return (
          <TouchableOpacity
            key={route.key}
            onPress={onPress}
            style={{
              flex: 1,
              justifyContent: 'center',
              alignItems: 'center',
              backgroundColor: isFocused ? '#007AFF' : '#fff',
            }}
          >
            <Text style={{ color: isFocused ? '#fff' : '#000' }}>
              {options.title || route.name}
            </Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

<Tab.Navigator tabBar={(props) => <CustomTabBar {...props} />}>
  <Tab.Screen name="Home" component={HomeScreen} />
  <Tab.Screen name="Profile" component={ProfileScreen} />
</Tab.Navigator>
```

## Anti-Patterns

### Don't Navigate in useEffect Without Dependencies

```tsx
// Bad - Infinite loop risk
useEffect(() => {
  navigation.navigate('Home');
});

// Good - Proper dependencies
useEffect(() => {
  if (shouldNavigate) {
    navigation.navigate('Home');
  }
}, [shouldNavigate, navigation]);
```

### Don't Use navigate() for Replacing Screens

```tsx
// Bad - Adds to navigation stack
navigation.navigate('SignIn');

// Good - Replaces current screen
navigation.replace('SignIn');
```

### Don't Access Navigation Without Type Safety

```tsx
// Bad - No type safety
function MyScreen({ navigation }: any) {
  navigation.navigate('Detials', { itemId: 123 }); // Typo won't be caught
}

// Good - Type-safe navigation
type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

function MyScreen({ navigation }: Props) {
  navigation.navigate('Details', { itemId: '123' }); // Type-checked
}
```

### Don't Forget to Handle Back Button on Android

```tsx
import { useEffect } from 'react';
import { BackHandler } from 'react-native';

function MyScreen({ navigation }: any) {
  useEffect(() => {
    const backHandler = BackHandler.addEventListener(
      'hardwareBackPress',
      () => {
        navigation.goBack();
        return true; // Prevent default behavior
      }
    );

    return () => backHandler.remove();
  }, [navigation]);

  return <View />;
}
```

## Related Skills

- **react-native-components**: Building UI components for screens
- **react-native-platform**: Platform-specific navigation behavior
- **react-native-performance**: Optimizing navigation performance
