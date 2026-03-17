---
name: Paperand Development
description: Guide for developing and maintaining the Paperand React Native manga reader application
---

# Paperand Development Skill

This skill provides comprehensive guidance for working with the **Paperand** project - an ad-free manga reader built with Expo and React Native, compatible with Paperback extensions.

## Project Overview

**Paperand** is a cross-platform manga reader app that:
- Provides an elegant, ad-free manga reading experience
- Is compatible with Paperback extension sources
- Supports both Android and iOS platforms
- Features a personal library, reading progress tracking, and multi-source search

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Expo SDK 54** | Development framework |
| **React Native 0.81** | Cross-platform mobile development |
| **TypeScript** | Type-safe JavaScript |
| **React Navigation 7** | Navigation library (stack + bottom tabs) |
| **AsyncStorage** | Persistent local storage |
| **expo-image** | Optimized image loading with caching |
| **WebView** | Extension runtime for Paperback sources |
| **i18n-js** | Internationalization |

## Project Structure

```
paperback-android/
├── App.tsx                    # Main app entry, providers setup
├── index.ts                   # Expo entry point
├── app.json                   # Expo configuration
├── package.json               # Dependencies
├── src/
│   ├── components/            # Reusable UI components
│   │   ├── MangaCard.tsx      # Manga cover card component
│   │   ├── ChapterListItem.tsx # Chapter list item
│   │   ├── ExtensionRunner.tsx # WebView extension runtime
│   │   ├── PickerModal.tsx    # Custom picker modal
│   │   └── ...
│   ├── context/               # React Context providers
│   │   ├── ThemeContext.tsx   # Theme management
│   │   └── LibraryContext.tsx # Library & progress state
│   ├── navigation/            # Navigation configuration
│   │   ├── AppNavigator.tsx   # Main stack navigator
│   │   └── BottomTabNavigator.tsx # Bottom tab navigation
│   ├── screens/               # App screens
│   │   ├── LibraryScreen.tsx  # User library
│   │   ├── DiscoverScreen.tsx # Browse sources
│   │   ├── SearchScreen.tsx   # Multi-source search
│   │   ├── MangaDetailScreen.tsx # Manga details & chapters
│   │   ├── ReaderScreen.tsx   # Manga reader (core feature)
│   │   ├── DownloadManagerScreen.tsx # Download management
│   │   ├── ExtensionsScreen.tsx # Manage extensions
│   │   └── ...
│   ├── services/              # Core business logic
│   │   ├── sourceService.ts   # Extension API bridge
│   │   ├── extensionService.ts # Extension management
│   │   ├── cacheService.ts    # Image caching
│   │   ├── downloadService.ts # Chapter downloads
│   │   ├── themeService.ts    # Theme file parsing
│   │   ├── i18nService.ts     # Internationalization
│   │   ├── updateService.ts   # App update checks
│   │   └── ...
│   ├── hooks/                 # Custom React hooks
│   ├── types/                 # TypeScript type definitions
│   ├── constants/             # App constants
│   └── locales/               # Translation files (17 languages)
├── android/                   # Android native code
├── assets/                    # Images, icons, fonts
├── plugins/                   # Custom Expo config plugins
└── credentials/               # Build credentials
```

## Development Commands

```bash
# Install dependencies
npm install
# or
bun install

# Start development server
npx expo start

# Run on Android
npm run android

# Run on iOS
npm run ios

# Run on web
npm run web
```

## Key Architectural Patterns

### 1. Extension System
The app uses a WebView-based extension runtime (`ExtensionRunner.tsx`) to execute Paperback-compatible extensions. Extensions are JavaScript bundles that provide manga source implementations.

### 2. Context Providers
- **ThemeContext**: Manages app theme (dark/light mode) and custom `.pbcolors` themes
- **LibraryContext**: Manages user library, favorites, reading progress, and history

### 3. Service Layer
All business logic is encapsulated in service files:
- `sourceService.ts` - Bridge between app and extensions
- `cacheService.ts` - Image caching with configurable limits
- `downloadService.ts` - Background chapter downloads
- `i18nService.ts` - Multi-language support

### 4. Navigation Structure
```
Stack Navigator (AppNavigator)
├── Bottom Tab Navigator
│   ├── Library
│   ├── Discover
│   ├── History
│   └── More
├── MangaDetail
├── Reader
├── Search
├── Extensions
├── Settings
└── ...
```

## Internationalization (i18n)

The app supports 17+ languages. Translation files are in `src/locales/` as JSON files.

**Adding a new translation:**
1. Create a new JSON file in `src/locales/` (e.g., `de.json`)
2. Copy the structure from `en.json`
3. Translate all strings
4. Register the language in `i18nService.ts`

## Theming

The app supports custom themes via `.pbcolors` files (Paperback theme format).

**Theme configuration:**
- System theme support (automatic dark/light mode)
- Custom color parsing in `themeService.ts`
- Theme application via `ThemeContext`

## Building for Production

### GitHub Actions (Automated)
On push to `main` or manual trigger:
1. Builds Android APK with signing
2. Builds iOS IPA
3. Creates GitHub Release with artifacts

### Local EAS Build
```bash
# Android APK
eas build --platform android --profile preview

# iOS
eas build --platform ios --profile preview
```

## Common Development Tasks

### Adding a New Screen
1. Create the screen component in `src/screens/`
2. Export it from `src/screens/index.ts`
3. Add the route in `src/navigation/AppNavigator.tsx`
4. Add navigation types if using TypeScript

### Adding a New Component
1. Create the component in `src/components/`
2. Export it from `src/components/index.ts`
3. Use the theme from `ThemeContext` for styling

### Adding a New Service
1. Create the service file in `src/services/`
2. Use AsyncStorage for persistent data
3. Follow existing patterns for async operations

## Code Style Guidelines

- Use TypeScript for all new files
- Use functional components with hooks
- Use the app's theme system for colors (`useTheme()`)
- Use `i18n.t('key')` for all user-facing strings
- Keep components focused and reusable
- Use services for business logic, not in components

## Testing & Debugging

- **Developer Menu**: Tap version number in More > About 7 times
- **Console Logging**: Use standard `console.log` (visible in Metro bundler)
- **React Native Debugger**: Connect via Expo dev tools

## Important Notes

- The app uses Expo managed workflow with custom native code via config plugins
- Background downloads require foreground service configuration (Android)
- Extension execution happens in an isolated WebView context
- Image caching is handled by expo-image with custom cache management

---

## Quick Reference

### Import Patterns
```typescript
// Theme & Styles
import { useTheme } from '../context/ThemeContext';

// Library & State
import { useLibrary } from '../context/LibraryContext';

// Navigation
import { useNavigation, useRoute } from '@react-navigation/native';

// Components
import { MangaCard, LoadingIndicator, EmptyState } from '../components';

// Services
import { sourceService } from '../services/sourceService';
import { cacheService } from '../services/cacheService';

// i18n
import { i18n } from '../services/i18nService';
```

### Screen Template
```typescript
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { useTheme } from '../context/ThemeContext';

export function NewScreen() {
  const { colors } = useTheme();
  
  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      {/* Content */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
});
```

### Navigation Params
```typescript
// Navigate with params
navigation.navigate('MangaDetail', { manga, sourceId });
navigation.navigate('Reader', { manga, chapter, sourceId });

// Get params
const { manga, sourceId } = useRoute().params;
```

---

## Styling Patterns

### Theme Colors
```typescript
const { colors, isDark } = useTheme();
// colors.background, colors.text, colors.primary, colors.card, colors.border
```

### Common Styles
```typescript
// Card style
{ backgroundColor: colors.card, borderRadius: 12, padding: 16 }

// Text styles
{ color: colors.text, fontSize: 16 }
{ color: colors.textSecondary, fontSize: 14 }

// Separator
{ height: 1, backgroundColor: colors.border }
```

---

## State Management

### Library Context Methods
```typescript
const { 
  library,           // Manga[] - saved manga
  favorites,         // string[] - favorite manga IDs
  readingProgress,   // { [mangaId]: { chapterId, page } }
  addToLibrary,      // (manga) => void
  removeFromLibrary, // (mangaId) => void
  toggleFavorite,    // (mangaId) => void
  updateProgress,    // (mangaId, chapterId, page) => void
} = useLibrary();
```

### AsyncStorage Keys
| Key | Type | Description |
|-----|------|-------------|
| `@library` | Manga[] | Saved manga |
| `@favorites` | string[] | Favorite IDs |
| `@reading_progress` | object | Reading positions |
| `@extensions` | Extension[] | Installed extensions |
| `@settings` | object | User settings |
| `@history` | HistoryItem[] | Reading history |

---

## Extension API

### Source Service Methods
```typescript
// Get manga list
await sourceService.getDiscoverSection(sourceId, sectionId);

// Search manga
await sourceService.searchManga(sourceId, query);

// Get manga details
await sourceService.getMangaDetails(sourceId, mangaId);

// Get chapters
await sourceService.getChapters(sourceId, mangaId);

// Get chapter pages
await sourceService.getChapterPages(sourceId, chapterId);
```

---

## Error Handling

```typescript
try {
  const data = await sourceService.getMangaDetails(sourceId, mangaId);
} catch (error) {
  console.error('Failed to load manga:', error);
  // Show error state or toast
}
```

---

## Performance Tips

1. **Images**: Use `expo-image` with `cachePolicy="memory-disk"`
2. **Lists**: Use `FlatList` with `keyExtractor` and `getItemLayout`
3. **Memoization**: Use `useMemo`/`useCallback` for expensive operations
4. **Lazy Loading**: Load chapters/pages on demand

---

## File Naming

| Type | Convention | Example |
|------|------------|---------|
| Screen | `*Screen.tsx` | `LibraryScreen.tsx` |
| Component | `PascalCase.tsx` | `MangaCard.tsx` |
| Service | `*Service.ts` | `cacheService.ts` |
| Hook | `use*.ts` | `useDebounce.ts` |
| Context | `*Context.tsx` | `ThemeContext.tsx` |
| Types | `index.ts` | `types/index.ts` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Extension not loading | Check WebView logs, verify extension URL |
| Images not caching | Check cache size limits in settings |
| Build fails | Run `npx expo prebuild --clean` |
| Metro bundler stuck | Clear cache: `npx expo start -c` |
| Android foreground service crash | Check `withBackgroundActionsServiceType` plugin |

---

## Android-Specific

- Foreground service type configured in `plugins/withBackgroundActionsServiceType.js`
- Permissions in `app.json` under `android.permissions`
- Deep links: `paperback://` and `paperand://` schemes

## iOS-Specific

- Background modes: `fetch` enabled
- Localization: 35+ locales in `CFBundleLocalizations`
- Bundle ID: `com.chiraitori.paperand.ios`
