---
name: app
description: Use when working on the mobile app (packages/app). Covers Expo, React Native, expo-router navigation, NativeWind styling, React Query data fetching, translations, and mobile-specific patterns.
---

# Mobile App Development Guide

You are working on the **100cims mobile app** (`packages/app`), an Expo React Native application for mountaineering.

## Key Files

| File | Purpose |
| ---- | ------- |
| `app/_layout.tsx` | Root layout with providers |
| `app.config.ts` | Expo configuration, plugins, EAS project ID |
| `lib/api-client.ts` | openapi-fetch client with auth |
| `types/api.ts` | Generated OpenAPI types (DO NOT EDIT) |
| `domains/*/` | Feature-specific business logic |
| `components/ui/` | Reusable UI components |
| `translations/*.json` | i18n message files |

## Stack

- **Expo SDK 54** with React Native 0.81 (new architecture enabled)
- **expo-router 6** for file-based navigation
- **NativeWind 4** for styling (Tailwind CSS)
- **React Query 5** for server state
- **React Intl** for i18n (en, ca, es)

## Directory Structure

- `/app/`: expo-router screens (file-based routing)
- `/domains/`: Feature-specific business logic
- `/hooks/`: Shared React hooks
- `/lib/`: Utility functions (api-client, auth, dates, images, location, validation)
- `/components/`: Reusable UI components
- `/translations/`: i18n message files
- `/types/`: Shared TypeScript types (api.ts auto-generated, mountain.ts, etc.)

## Domain Pattern

Each domain folder typically contains:
- `*.api.ts`: React Query hooks for API calls
- `*.utils.ts`: Domain-specific utilities
- `*.types.ts`: TypeScript types (optional)

Example: `/domains/user/user.api.ts` exports `useUser()`, `useUpdateUser()`, etc.

## Shared Hooks

| Hook | Location | Purpose |
| ---- | -------- | ------- |
| `useImagePicker` | `hooks/use-image-picker.ts` | Pick and optimize images with state management |
| `useMountainSelection` | `hooks/use-mountain-selection.ts` | Manage mountain selection in challenge screens |
| `useLocation` | `hooks/use-location.ts` | Get user's current location |
| `useIsKeyboardVisible` | `hooks/use-is-keyboard-visible.ts` | Detect keyboard visibility |
| `useDistanceToTarget` | `hooks/use-distance-to-target.ts` | Calculate distance to coordinates |

## Shared Utilities

| Utility | Location | Purpose |
| ------- | -------- | ------- |
| `validateMountainForm` | `lib/mountain-validation.ts` | Validate mountain form fields |
| `getImageOptimized` | `lib/images.ts` | Optimize images for upload |
| `cleanText` | `lib/strings.ts` | Normalize text for search |
| `getDistanceInKm` | `lib/location.ts` | Calculate distance between coordinates |

## Shared Types

| Type | Location | Purpose |
| ---- | -------- | ------- |
| `MountainData` | `types/mountain.ts` | Base mountain data from API |
| `MountainWithChallengeCount` | `types/mountain.ts` | Mountain with challenge count |
| `NewMountainData` | `types/mountain.ts` | New mountain for local state |
| `MountainInfo` | `types/mountain.ts` | Minimal mountain info for display |

## Key Patterns

### Using Shared Hooks

```typescript
// Image picker with optimization
import { useImagePicker } from '@/hooks/use-image-picker';

const { imageUri, imageBase64, hasChanged, pickImage, reset } = useImagePicker({
  initialUri: existingImageUrl,
});

// Mountain selection state management
import { useMountainSelection } from '@/hooks/use-mountain-selection';

const {
  selectedMountainIds,
  newMountains,
  selectedMountainsForDisplay,
  totalMountainCount,
  handleSelectionChange,
  handleAddNewMountain,
  handleRemoveNewMountain,
} = useMountainSelection({ allMountains });
```

### Form Validation

```typescript
import { validateMountainForm } from '@/lib/mountain-validation';

const validation = validateMountainForm({ name, location, height, latitude, longitude }, intl);
if (!validation.valid) {
  return Alert.alert(validation.error);
}
// Use validation.data.name, validation.data.height (parsed numbers), etc.
```

### API Calls

```typescript
// Use openapi-fetch client from lib/api-client.ts
import apiClient from '@/lib/api-client';
import { useQuery } from '@tanstack/react-query';

export const useUser = (userId: string) => {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: async () => {
      const { data, error } = await apiClient.GET('/api/user/{id}', {
        params: { path: { id: userId } }
      });
      if (error) throw error;
      return data;
    }
  });
};
```

### Infinite Scroll with Pagination

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

export const useItemsList = () => {
  return useInfiniteQuery({
    queryKey: ['items', 'list'],
    initialPageParam: 1,
    queryFn: async ({ pageParam }) => {
      const { data, error } = await apiClient.GET('/api/items', {
        params: { query: { page: pageParam, limit: 50 } },
      });
      if (error) throw error;
      return data.message;
    },
    getNextPageParam: (lastPage) => {
      if (lastPage?.pagination?.hasMore) {
        return lastPage.pagination.page + 1;
      }
      return undefined;
    },
  });
};

// In component:
const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useItemsList();
const items = data?.pages?.flatMap((p) => p?.items ?? []) ?? [];

<FlatList
  data={items}
  onEndReached={() => hasNextPage && !isFetchingNextPage && fetchNextPage()}
  onEndReachedThreshold={0.5}
  ListFooterComponent={isFetchingNextPage ? <ActivityIndicator /> : null}
/>
```

### Authentication

- JWT stored in AsyncStorage
- `setAuthToken(token)` in lib/api-client.ts sets Authorization header
- Protected routes check auth state in _layout.tsx

### Styling with NativeWind

```typescript
<View className="flex-1 bg-white dark:bg-gray-900">
  <Text className="text-lg font-bold text-gray-900">Title</Text>
</View>
```

### Navigation

```typescript
import { router } from 'expo-router';

// Navigate
router.push('/user/123');

// With params
router.push({ pathname: '/mountain/[id]', params: { id: '456' } });
```

### Translations (CRITICAL)

**All user-facing strings MUST use `intl.formatMessage`** - never hardcode text.

```typescript
import { useIntl } from 'react-intl';

const { formatMessage } = useIntl();

// Simple string
const title = formatMessage({ defaultMessage: 'Settings' });

// In JSX
<ThemedText>{intl.formatMessage({ defaultMessage: "Save changes" })}</ThemedText>

// With FormattedMessage component
import { FormattedMessage } from 'react-intl';
<FormattedMessage defaultMessage="Welcome back" />
```

**Translation Workflow:**

1. Add strings in code using `defaultMessage` (English text)
2. Run extraction: `yarn translations:extract`
3. Run compilation: `yarn translations:generate`
4. English (`translations/en.json`) is auto-generated
5. **Manually copy new keys** to `translations/ca.json` (Catalan) and `translations/es.json` (Spanish)
6. Translate the values in ca.json and es.json

**Translation Files:**
- `translations/raw-en.json` - Extracted messages (intermediate)
- `translations/en.json` - Compiled English (used by app)
- `translations/ca.json` - Catalan translations (manual)
- `translations/es.json` - Spanish translations (manual)

## Common Tasks

### Add New Screen

1. Create file in `/app/` (e.g., `/app/settings.tsx`)
2. Export default React component
3. File name becomes route path

### Add API Integration

1. Ensure backend types are current: `yarn generate-api-types`
2. Create domain API file or add to existing
3. Use React Query for data fetching
4. Handle loading/error states

### Add/Update Translations

1. Use `intl.formatMessage({ defaultMessage: "English text" })` in code
2. Run `yarn translations:extract` to extract all messages
3. Run `yarn translations:generate` to compile English
4. Copy new keys from `en.json` to `ca.json` and `es.json`
5. Translate the values in ca.json and es.json

### Add Native Module

```bash
npx expo install <package-name>
```

May need to rebuild: `npx expo prebuild --clean`

## Environment Variables

Must prefix with `EXPO_PUBLIC_` to access in app:
- `EXPO_PUBLIC_API_URL`: Backend URL
- `EXPO_PUBLIC_REACT_ANALYTICS_KEY`: Analytics key
- OAuth client IDs for Google/Apple

## Debugging

### Common Issues

- **Type errors**: Regenerate API types with `yarn generate-api-types`
- **Navigation issues**: Check expo-router file structure
- **Styling not applying**: Verify NativeWind babel config, global.css import
- **OAuth not working**: Check google-services.json, Apple config in app.config.ts

### Helpful Commands

```bash
npx expo start --clear          # Clear cache
npx expo-doctor                 # Diagnose issues
npx uri-scheme list             # Check deep linking
```

## Build & Deploy

```bash
eas build --profile development  # Dev build with expo-dev-client
eas build --profile preview      # Internal preview
eas build --profile production   # Production release
```

See `eas.json` for build profiles.
