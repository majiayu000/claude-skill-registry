---
name: react-native-app
description: React Native cross-platform mobile apps with navigation, state management, native features. Use for iOS/Android development, mobile prototyping, code sharing, or encountering bridge errors, platform-specific bugs, performance bottlenecks.
---

# React Native App Development

Build cross-platform mobile applications with modern React Native patterns.

## Project Structure

```
src/
├── components/     # Reusable UI components
├── screens/        # Screen components
├── navigation/     # React Navigation setup
├── services/       # API and business logic
├── store/          # State management
├── hooks/          # Custom hooks
└── utils/          # Helpers
```

## Navigation Setup

```javascript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Main" component={MainTabs} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

function MainTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

## State Management (Redux Toolkit)

```javascript
import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: { data: null, loading: false, error: null },
  reducers: {
    setUser: (state, action) => { state.data = action.payload; },
    setLoading: (state, action) => { state.loading = action.payload; },
    setError: (state, action) => { state.error = action.payload; }
  }
});
```

## API Client

```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({ baseURL: 'https://api.example.com' });

api.interceptors.request.use(async config => {
  const token = await AsyncStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

## Best Practices

- Use functional components with hooks
- Implement proper error boundaries
- Optimize FlatList with keyExtractor, getItemLayout
- Handle platform-specific code with Platform.select()
- Use TypeScript for type safety
- Test on both iOS and Android

## Avoid

- Inline styles (use StyleSheet)
- Index as list keys
- Storing sensitive data in AsyncStorage
- Ignoring platform differences
