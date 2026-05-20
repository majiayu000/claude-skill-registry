---
name: react-native-app
description: Build cross-platform mobile apps with React Native. Covers navigation with React Navigation, state management with Redux/Context API, API integration, and platform-specific features.
---

# React Native App Development

## Overview

Create robust cross-platform mobile applications using React Native with modern development patterns including navigation, state management, API integration, and native module handling.

## When to Use

- Building iOS and Android apps from single codebase
- Rapid prototyping for mobile platforms
- Leveraging web development skills for mobile
- Sharing code between React Native and React Web
- Integrating with native modules and APIs

## Instructions

### 1. **Project Setup & Navigation**

```javascript
// Navigation with React Navigation
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function HomeStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: '#6200ee' },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' }
      }}
    >
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: 'Home Feed' }}
      />
      <Stack.Screen name="Details" component={DetailsScreen} />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const icons = {
            HomeTab: focused ? 'home' : 'home-outline',
            ProfileTab: focused ? 'person' : 'person-outline'
          };
          return <Ionicons name={icons[route.name]} size={size} color={color} />;
        }
      })}>
        <Tab.Screen name="HomeTab" component={HomeStack} />
        <Tab.Screen name="ProfileTab" component={ProfileScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

### 2. **State Management with Redux**

```javascript
import { createSlice, configureStore } from '@reduxjs/toolkit';
import { useSelector, useDispatch } from 'react-redux';

const itemsSlice = createSlice({
  name: 'items',
  initialState: { list: [], loading: false, error: null },
  reducers: {
    setItems: (state, action) => {
      state.list = action.payload;
      state.loading = false;
    },
    setLoading: (state) => { state.loading = true; },
    setError: (state, action) => {
      state.error = action.payload;
      state.loading = false;
    }
  }
});

export const store = configureStore({
  reducer: { items: itemsSlice.reducer }
});

export function HomeScreen() {
  const dispatch = useDispatch();
  const { list, loading, error } = useSelector(state => state.items);

  React.useEffect(() => {
    dispatch(setLoading());
    fetch('https://api.example.com/items')
      .then(r => r.json())
      .then(data => dispatch(setItems(data)))
      .catch(err => dispatch(setError(err.message)));
  }, [dispatch]);

  if (loading) return <ActivityIndicator size="large" />;
  if (error) return <Text>Error: {error}</Text>;

  return (
    <ScrollView>
      {list.map(item => <ItemCard key={item.id} item={item} />)}
    </ScrollView>
  );
}
```

### 3. **API Integration with Axios**

```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const apiClient = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = await AsyncStorage.getItem('refreshToken');
        const { data } = await axios.post(
          'https://api.example.com/auth/refresh',
          { refreshToken }
        );
        await AsyncStorage.setItem('authToken', data.accessToken);
        apiClient.defaults.headers.Authorization = `Bearer ${data.accessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const fetchUser = () => apiClient.get('/user/profile');
export const fetchItems = (page) => apiClient.get(`/items?page=${page}`);
export const createItem = (data) => apiClient.post('/items', data);
```

### 4. **Functional Component with Hooks**

```javascript
import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet, ActivityIndicator
} from 'react-native';

export function DetailsScreen({ route, navigation }) {
  const { itemId } = route.params;
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadItem();
  }, [itemId]);

  const loadItem = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(
        `https://api.example.com/items/${itemId}`
      );
      const data = await response.json();
      setItem(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [itemId]);

  if (loading) return <ActivityIndicator size="large" />;
  if (error) return <Text>Error: {error}</Text>;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{item?.title}</Text>
      <Text style={styles.description}>{item?.description}</Text>
      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Go Back</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, flex: 1 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
  description: { fontSize: 16, color: '#666', marginBottom: 16 },
  button: { backgroundColor: '#6200ee', padding: 12, borderRadius: 8 },
  buttonText: { color: '#fff', fontWeight: 'bold', textAlign: 'center' }
});
```

## Best Practices

### ✅ DO
- Use functional components with React Hooks
- Implement proper error handling and loading states
- Use Redux or Context API for state management
- Leverage React Navigation for routing
- Optimize list rendering with FlatList
- Handle platform-specific code elegantly
- Use TypeScript for type safety
- Test on both iOS and Android
- Use environment variables for API endpoints
- Implement proper memory management

### ❌ DON'T
- Use inline styles excessively (use StyleSheet)
- Make API calls without error handling
- Store sensitive data in plain text
- Ignore platform differences
- Create large monolithic components
- Use index as key in lists
- Make synchronous operations
- Ignore battery optimization
- Deploy without testing on real devices
- Forget to unsubscribe from listeners
