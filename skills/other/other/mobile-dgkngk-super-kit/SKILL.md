---
name: mobile
description: React Native, Flutter, and mobile development best practices. Use when building mobile apps, handling platform-specific behavior, or optimizing mobile performance.
---

# Mobile Development Skill

## Overview
React Native, Flutter, and mobile development best practices.

## React Native Patterns

### 1. Project Structure
```
src/
├── components/       # Reusable UI components
│   ├── Button.tsx
│   └── Card.tsx
├── screens/          # Screen components
│   ├── Home.tsx
│   └── Profile.tsx
├── navigation/       # Navigation config
│   └── AppNavigator.tsx
├── hooks/            # Custom hooks
├── services/         # API calls
├── stores/           # State management
└── utils/            # Utilities
```

### 2. Navigation
```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### 3. Styling
```tsx
import { StyleSheet, View, Text } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 12,
  },
});

// Or use styled-components
import styled from 'styled-components/native';

const Container = styled.View`
  flex: 1;
  padding: 16px;
`;
```

## Performance Optimization

### FlatList Best Practices
```tsx
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={(item) => item.id}
  
  // Performance props
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
  initialNumToRender={10}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

### Memoization
```tsx
// Memoize expensive components
const MemoizedItem = React.memo(({ item }) => (
  <View>
    <Text>{item.title}</Text>
  </View>
));

// useCallback for event handlers
const handlePress = useCallback(() => {
  navigation.navigate('Details', { id: item.id });
}, [item.id]);
```

## Platform-Specific Code
```tsx
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.25,
    },
    android: {
      elevation: 5,
    },
  }),
});

// Or use file extensions
// Button.ios.tsx
// Button.android.tsx
```

## Testing
```typescript
import { render, fireEvent } from '@testing-library/react-native';

test('button press', () => {
  const onPress = jest.fn();
  const { getByText } = render(<Button onPress={onPress} title="Click" />);
  
  fireEvent.press(getByText('Click'));
  expect(onPress).toHaveBeenCalled();
});
```
