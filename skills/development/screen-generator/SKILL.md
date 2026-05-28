---
name: screen-generator
description: Generates new React Native screens following Ishkul patterns. Creates screen component with proper hooks ordering, state management, loading/error/success states, navigation setup, and matching test file. Use when adding new screens to the app.
---

# Screen Generator

Creates new React Native screens following Ishkul's established patterns.

## What Gets Created

When generating a new screen, create:

1. **Screen component**: `frontend/src/screens/ScreenName.tsx`
2. **Test file**: `frontend/src/screens/__tests__/ScreenName.test.tsx`
3. **Navigation update**: Add to `frontend/src/types/navigation.ts`
4. **Navigator update**: Add to `frontend/src/navigation/AppNavigator.tsx`

## Screen Template

```typescript
import React, { useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';

// State management
import { useScreenNameStore } from '../state/screenNameStore';

// Custom hooks
import { useTheme } from '../hooks/useTheme';

// Components
import { Button } from '../components/Button';
import { ErrorBanner } from '../components/ErrorBanner';
import { LearningLayout } from '../components/LearningLayout';

// Types
import { RootStackParamList } from '../types/navigation';

// Theme
import { Spacing } from '../theme/spacing';
import { Typography } from '../theme/typography';

type ScreenNameProps = NativeStackScreenProps<RootStackParamList, 'ScreenName'>;

export const ScreenName: React.FC<ScreenNameProps> = ({ navigation, route }) => {
  // ==========================================================================
  // HOOKS SECTION - All hooks MUST be called at the top, before any conditionals
  // This prevents React Rules of Hooks violations (React error #310)
  // ==========================================================================

  // 1. Zustand store hooks first
  const {
    data,
    isLoading,
    error,
    fetchData,
    clearError,
  } = useScreenNameStore();

  // 2. Theme and navigation hooks
  const { colors } = useTheme();

  // 3. Route params extraction
  const { id } = route.params;

  // 4. Refs (if needed)
  // const scrollViewRef = useRef<ScrollView>(null);

  // 5. Extract state used in multiple render paths BEFORE conditionals
  const hasData = data !== null;
  const dataItems = data?.items ?? [];

  // 6. Callbacks with useCallback BEFORE conditionals
  const handleRefresh = useCallback(() => {
    fetchData(id);
  }, [fetchData, id]);

  const handleRetry = useCallback(() => {
    clearError();
    fetchData(id);
  }, [clearError, fetchData, id]);

  const handleItemPress = useCallback((itemId: string) => {
    navigation.navigate('ItemDetail', { itemId });
  }, [navigation]);

  // 7. Effects after hooks
  useEffect(() => {
    fetchData(id);
  }, [fetchData, id]);

  // ==========================================================================
  // CONDITIONAL RETURNS - Safe after all hooks are called
  // ==========================================================================

  // Loading state
  if (isLoading && !hasData) {
    return (
      <LearningLayout
        title="Loading..."
        onBackPress={() => navigation.goBack()}
        showProgress={false}
      >
        <View style={styles.centerContainer} testID="loading-indicator">
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={[styles.loadingText, { color: colors.textSecondary }]}>
            Loading content...
          </Text>
        </View>
      </LearningLayout>
    );
  }

  // Error state
  if (error && !hasData) {
    return (
      <LearningLayout
        title="Error"
        onBackPress={() => navigation.goBack()}
        showProgress={false}
      >
        <View style={styles.centerContainer} testID="error-container">
          <ErrorBanner message={error} onDismiss={clearError} />
          <Button
            title="Retry"
            onPress={handleRetry}
            variant="primary"
            style={styles.retryButton}
          />
        </View>
      </LearningLayout>
    );
  }

  // Empty state
  if (!hasData) {
    return (
      <LearningLayout
        title="Not Found"
        onBackPress={() => navigation.goBack()}
        showProgress={false}
      >
        <View style={styles.centerContainer} testID="empty-container">
          <Text style={[styles.emptyText, { color: colors.textSecondary }]}>
            No content found
          </Text>
          <Button
            title="Go Back"
            onPress={() => navigation.goBack()}
            variant="outline"
            style={styles.retryButton}
          />
        </View>
      </LearningLayout>
    );
  }

  // ==========================================================================
  // SUCCESS STATE - Main content
  // ==========================================================================

  return (
    <LearningLayout
      title={data.title}
      onBackPress={() => navigation.goBack()}
      showProgress={true}
      progress={0.5}
    >
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}
        refreshControl={
          <RefreshControl
            refreshing={isLoading}
            onRefresh={handleRefresh}
            colors={[colors.primary]}
          />
        }
        testID="content-container"
      >
        {/* Error banner for non-blocking errors */}
        {error && (
          <ErrorBanner
            message={error}
            onDismiss={clearError}
            style={styles.errorBanner}
          />
        )}

        {/* Main content */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>
            Content Section
          </Text>

          {dataItems.map((item) => (
            <View key={item.id} style={styles.itemContainer}>
              <Text style={[styles.itemText, { color: colors.text }]}>
                {item.title}
              </Text>
              <Button
                title="View"
                onPress={() => handleItemPress(item.id)}
                variant="outline"
                size="small"
              />
            </View>
          ))}
        </View>
      </ScrollView>
    </LearningLayout>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  contentContainer: {
    padding: Spacing.md,
    paddingBottom: Spacing.xxl,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.xl,
  },
  loadingText: {
    marginTop: Spacing.md,
    ...Typography.body,
  },
  emptyText: {
    ...Typography.body,
    textAlign: 'center',
    marginBottom: Spacing.lg,
  },
  retryButton: {
    marginTop: Spacing.lg,
  },
  errorBanner: {
    marginBottom: Spacing.md,
  },
  section: {
    marginBottom: Spacing.lg,
  },
  sectionTitle: {
    ...Typography.h2,
    marginBottom: Spacing.md,
  },
  itemContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: Spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
  },
  itemText: {
    ...Typography.body,
    flex: 1,
  },
});
```

## Navigation Type Update

Add to `frontend/src/types/navigation.ts`:

```typescript
export type RootStackParamList = {
  // ... existing routes
  ScreenName: { id: string };
  // Add any new routes the screen navigates to
  ItemDetail: { itemId: string };
};
```

## Navigator Update

Add to `frontend/src/navigation/AppNavigator.tsx`:

```typescript
import { ScreenName } from '../screens/ScreenName';

// In the navigator:
<Stack.Screen
  name="ScreenName"
  component={ScreenName}
  options={{
    headerShown: false, // Using LearningLayout
  }}
/>
```

## Zustand Store Template

If a new store is needed, create `frontend/src/state/screenNameStore.ts`:

```typescript
import { create } from 'zustand';
import { apiClient } from '../services/api/client';

interface DataItem {
  id: string;
  title: string;
}

interface ScreenData {
  id: string;
  title: string;
  items: DataItem[];
}

interface ScreenNameState {
  // State
  data: ScreenData | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchData: (id: string) => Promise<ScreenData | null>;
  clearError: () => void;
  reset: () => void;
}

export const useScreenNameStore = create<ScreenNameState>((set, get) => ({
  data: null,
  isLoading: false,
  error: null,

  fetchData: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get<ScreenData>(`/api/resource/${id}`);
      set({ data: response, isLoading: false });
      return response;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to load';
      set({ error: message, isLoading: false });
      return null;
    }
  },

  clearError: () => set({ error: null }),

  reset: () => set({ data: null, isLoading: false, error: null }),
}));
```

## Test File Template

Create `frontend/src/screens/__tests__/ScreenName.test.tsx` - see test-generator skill for full template.

Key test sections:
1. Loading State
2. Error State
3. Empty State
4. Success State
5. State Transitions (Critical!)
6. User Interactions

## Checklist Before Completing

- [ ] Screen component created with proper hooks ordering
- [ ] All hooks called BEFORE conditional returns
- [ ] Loading, error, empty, success states handled
- [ ] Navigation types updated
- [ ] Navigator updated
- [ ] Zustand store created (if needed)
- [ ] Test file created with state transition tests
- [ ] TypeScript compiles: `npm run type-check`
- [ ] Tests pass: `npm test -- --testPathPattern="ScreenName"`

## When to Use

- When adding a new feature that needs its own screen
- When creating list/detail views
- When building forms or interactive pages
- When adding settings or profile pages
