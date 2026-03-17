---
name: zafer-skills
description: Expo React Native mobile app development with RevenueCat payments, AdMob ads, i18n localization, onboarding flow, paywall, and NativeTabs navigation
---

# Expo Mobile Application Development Guide

> **IMPORTANT**: This is a SKILL file, NOT a project. NEVER run npm/bun install in this folder. NEVER create code files here. When creating a new project, ALWAYS ask the user for the project path first or create it in a separate directory (e.g., `~/Projects/app-name`).

This guide is created to provide context when working with Expo projects using Claude Code.

## MANDATORY REQUIREMENTS

When creating a new Expo project, you MUST include ALL of the following:

### Required Screens (ALWAYS CREATE)

- [ ] `src/app/onboarding.tsx` - Swipe-based onboarding with fullscreen background video and gradient overlay
- [ ] `src/app/paywall.tsx` - RevenueCat paywall screen (shown after onboarding)
- [ ] `src/app/settings.tsx` - Settings screen with language, theme, notifications, and reset onboarding options

### Onboarding Video Implementation (REQUIRED)

The onboarding screen MUST have a fullscreen background video. Use a URL, not a local file:

```tsx
import { useVideoPlayer, VideoView } from "expo-video";

const VIDEO_URL =
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";

const player = useVideoPlayer(VIDEO_URL, (player) => {
  player.loop = true;
  player.muted = true;
  player.play();
});

// In render:
<VideoView
  player={player}
  style={StyleSheet.absoluteFill}
  contentFit="cover"
  nativeControls={false}
/>;
```

Do NOT just import expo-video without actually using the VideoView component.

### Required Navigation (ALWAYS USE)

- [ ] Use `NativeTabs` from `expo-router/unstable-native-tabs` for tab navigation - NEVER use `@react-navigation/bottom-tabs` or `Tabs` from expo-router

### Required Context Providers (ALWAYS WRAP)

```tsx
import { ThemeProvider } from "@/context/theme-context";
import {
  DarkTheme,
  DefaultTheme,
  ThemeProvider as NavigationThemeProvider,
} from "@react-navigation/native";

<ThemeProvider>
  <OnboardingProvider>
    <AdsProvider>
      <NavigationThemeProvider
        value={colorScheme === "dark" ? DarkTheme : DefaultTheme}
      >
        <Stack />
      </NavigationThemeProvider>
    </AdsProvider>
  </OnboardingProvider>
</ThemeProvider>;
```

### Required Libraries (ALWAYS INSTALL)

Use `npx expo install` to install libraries (NOT npm/yarn/bun install):

```bash
npx expo install react-native-purchases react-native-google-mobile-ads expo-notifications i18next react-i18next expo-localization react-native-reanimated expo-video expo-audio expo-sqlite expo-linear-gradient
```

Libraries:

- `react-native-purchases` (RevenueCat)
- `react-native-google-mobile-ads` (AdMob)
- `expo-notifications`
- `i18next` + `react-i18next` + `expo-localization`
- `react-native-reanimated`
- `expo-video` + `expo-audio`
- `expo-sqlite` (for localStorage)
- `expo-linear-gradient` (for gradient overlays)

### AdMob Configuration (REQUIRED in app.json)

You MUST add this to `app.json` for AdMob to work:

```json
{
  "expo": {
    "plugins": [
      [
        "react-native-google-mobile-ads",
        {
          "androidAppId": "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy",
          "iosAppId": "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
        }
      ]
    ]
  }
}
```

For development/testing, use test App IDs:

- iOS: `ca-app-pub-3940256099942544~1458002511`
- Android: `ca-app-pub-3940256099942544~3347511713`

Do NOT skip this configuration or the app will crash with `GADInvalidInitializationException`.

### Banner Ad Implementation (REQUIRED)

You MUST implement banner ads in the Tab layout. Use this pattern:

```tsx
import { View, StyleSheet } from 'react-native';
import { NativeTabs } from 'expo-router/unstable-native-tabs';
import { useTranslation } from 'react-i18next';
import { BannerAd, BannerAdSize, TestIds } from 'react-native-google-mobile-ads';
import { useAds } from '@/context/ads-context';

const adUnitId = __DEV__
  ? TestIds.BANNER
  : 'ca-app-pub-xxxxxxxxxxxxxxxx/yyyyyyyyyy';

export default function TabLayout() {
  const { t } = useTranslation();
  const { shouldShowAds } = useAds();

  return (
    <View style={styles.container}>
      <NativeTabs>
        <NativeTabs.Trigger name="index">
          <NativeTabs.Trigger.Label>{t('tabs.home')}</NativeTabs.Trigger.Label>
          <NativeTabs.Trigger.Icon sf="house.fill" md="home" />
        </NativeTabs.Trigger>
        <NativeTabs.Trigger name="settings">
          <NativeTabs.Trigger.Label>{t('tabs.settings')}</NativeTabs.Trigger.Label>
          <NativeTabs.Trigger.Icon sf="gear" md="settings" />
        </NativeTabs.Trigger>
      </NativeTabs>

      {shouldShowAds && (
        <View style={styles.adContainer}>
          <BannerAd
            unitId={adUnitId}
            size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
            requestOptions={{
              requestNonPersonalizedAdsOnly: true,
            }}
          />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  adContainer: {
    alignItems: 'center',
    paddingBottom: 10,
  },
});
```

- ALWAYS use `TestIds.BANNER` in development
- Banner ad is placed below NativeTabs in the Tab layout
- Use `useAds` context to check `shouldShowAds` (hides for premium users)

### TURKISH LOCALIZATION (IMPORTANT)

When writing `tr.json`, you MUST use correct Turkish characters:

- ı (lowercase dotless i) - NOT i
- İ (uppercase dotted I) - NOT I
- ü, Ü, ö, Ö, ç, Ç, ş, Ş, ğ, Ğ

Example:

- ✅ "Ayarlar", "Giriş", "Çıkış", "Başla", "İleri", "Güncelle"
- ❌ "Ayarlar", "Giris", "Cikis", "Basla", "Ileri", "Guncelle"

### FORBIDDEN (NEVER USE)

- ❌ AsyncStorage - Use `expo-sqlite/localStorage/install` instead
- ❌ lineHeight style - Use padding/margin instead
- ❌ `Tabs` from expo-router - Use `NativeTabs` instead
- ❌ `@react-navigation/bottom-tabs` - Use `NativeTabs` instead
- ❌ `expo-av` - Use `expo-video` for video, `expo-audio` for audio instead
- ❌ `expo-ads-admob` - Use `react-native-google-mobile-ads` instead
- ❌ Any other ads library - ONLY use `react-native-google-mobile-ads`
- ❌ Reanimated hooks inside callbacks - Call at component top level

### Reanimated Usage (IMPORTANT)

NEVER call `useAnimatedStyle`, `useSharedValue`, or other reanimated hooks inside callbacks, loops, or conditions.

❌ WRONG:

```tsx
const renderItem = () => {
  const animatedStyle = useAnimatedStyle(() => ({ opacity: 1 })); // ERROR!
  return <Animated.View style={animatedStyle} />;
};
```

✅ CORRECT:

```tsx
function MyComponent() {
  const animatedStyle = useAnimatedStyle(() => ({ opacity: 1 })); // Top level
  return <Animated.View style={animatedStyle} />;
}
```

For lists, create a separate component for each item:

```tsx
function AnimatedItem({ item }) {
  const animatedStyle = useAnimatedStyle(() => ({ opacity: 1 }));
  return <Animated.View style={animatedStyle}>{item.name}</Animated.View>;
}

// In FlatList:
renderItem={({ item }) => <AnimatedItem item={item} />}
```

### POST-CREATION CLEANUP (ALWAYS DO)

After creating a new Expo project, you MUST:

1. If using `(tabs)` folder, DELETE `src/app/index.tsx` to avoid route conflicts:

```bash
rm src/app/index.tsx
```

2. Check and remove `lineHeight` from these files:

- `src/components/themed-text.tsx` (comes with lineHeight by default - REMOVE IT)
- Any other component using `lineHeight`

Search and remove all `lineHeight` occurrences:

```bash
grep -r "lineHeight" src/
```

Replace with padding or margin instead.

### AFTER COMPLETING CODE (ALWAYS RUN)

When you finish writing/modifying code, you MUST run these commands in order:

```bash
npx expo install --fix
npx expo prebuild --clean
```

1. `install --fix` fixes dependency version mismatches
2. `prebuild --clean` recreates ios and android folders

Do NOT skip these steps.

---

## Project Creation

When user asks to create an app, you MUST:

1. FIRST ask for the bundle ID (e.g., "What is the bundle ID? Example: com.company.appname")
2. Create the project in the CURRENT directory using:

```bash
bunx create-expo -t default@next app-name
```

3. Update `app.json` with the bundle ID:

```json
{
  "expo": {
    "ios": {
      "bundleIdentifier": "com.company.appname"
    },
    "android": {
      "package": "com.company.appname"
    }
  }
}
```

4. Then cd into the project and start implementing all required screens
5. Do NOT ask for project path - always use current directory

## Technology Stack

- **Framework**: Expo, React Native
- **Navigation**: Expo Router (file-based routing), NativeTabs
- **State Management**: React Context API
- **Translations**: i18next, react-i18next
- **Purchases**: RevenueCat (react-native-purchases)
- **Advertisements**: Google AdMob (react-native-google-mobile-ads)
- **Notifications**: expo-notifications
- **Animations**: react-native-reanimated
- **Storage**: localStorage via expo-sqlite polyfill

> **WARNING**: DO NOT USE AsyncStorage! Use expo-sqlite polyfill instead.

- Example usage

```js
import "expo-sqlite/localStorage/install";

globalThis.localStorage.setItem("key", "value");
console.log(globalThis.localStorage.getItem("key")); // 'value'
```

> **WARNING**: NEVER USE `lineHeight`! It causes layout issues in React Native. Use padding or margin instead.

## Project Structure

```
project-root/
├── src/
│   ├── app/
│   │   ├── _layout.tsx
│   │   ├── index.tsx
│   │   ├── explore.tsx
│   │   ├── settings.tsx
│   │   ├── paywall.tsx
│   │   └── onboarding.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── themed-text.tsx
│   │   └── themed-view.tsx
│   ├── constants/
│   │   ├── theme.ts
│   │   └── [data-files].ts
│   ├── context/
│   │   ├── onboarding-context.tsx
│   │   └── ads-context.tsx
│   ├── hooks/
│   │   ├── use-notifications.ts
│   │   └── use-color-scheme.ts
│   ├── lib/
│   │   ├── notifications.ts
│   │   ├── purchases.ts
│   │   ├── ads.ts
│   │   └── i18n.ts
│   └── locales/
│       ├── tr.json
│       └── en.json
├── assets/
│   └── images/
├── ios/
├── android/
├── app.json
├── eas.json
├── package.json
└── tsconfig.json
```

## Tab Navigation (NativeTabs)

Expo Router uses NativeTabs for native tab navigation:

```tsx
import { NativeTabs } from "expo-router/unstable-native-tabs";

export default function TabLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="house.fill" md="home" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="explore">
        <NativeTabs.Trigger.Label>Explore</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="compass.fill" md="explore" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="settings">
        <NativeTabs.Trigger.Label>Settings</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="gear" md="settings" />
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
```

### NativeTabs Properties

- **sf**: SF Symbols icon name (iOS)
- **md**: Material Design icon name (Android)
- **name**: Route file name
- Tab order follows trigger order

### Common Icons

| Purpose       | SF Symbol       | Material Icon |
| ------------- | --------------- | ------------- |
| Home          | house.fill      | home          |
| Explore       | compass.fill    | explore       |
| Settings      | gear            | settings      |
| Profile       | person.fill     | person        |
| Search        | magnifyingglass | search        |
| Favorites     | heart.fill      | favorite      |
| Notifications | bell.fill       | notifications |

## Development Commands

```bash
bun install
bun start
bun ios
bun android
bun lint
npx expo install --fix
npx expo prebuild --clean
```

## EAS Build Commands

```bash
eas build --profile development --platform ios
eas build --profile development --platform android
eas build --profile production --platform ios
eas build --profile production --platform android
eas submit --platform ios
eas submit --platform android
```

## Important Modules

### RevenueCat

- File: `lib/purchases.ts`
- Used for premium access
- Paywall: `app/paywall.tsx`

### AdMob

- File: `src/lib/ads.ts`
- Ads disabled for premium users
- Test IDs must be used in development

### Notifications

- Files: `src/lib/notifications.ts`, `src/hooks/use-notifications.ts`
- iOS requires push notification entitlement

### Onboarding & Paywall Flow (CRITICAL)

- Files: `src/app/onboarding.tsx`, `src/app/paywall.tsx`
- Swipe-based screens with fullscreen background video
- Gradient overlay on video
- **IMPORTANT**: Paywall MUST appear immediately after onboarding completes

```tsx
// In onboarding.tsx - when user completes onboarding:
const handleComplete = async () => {
  await setOnboardingCompleted(true);
  router.replace('/paywall'); // Navigate to paywall immediately
};
```

```tsx
// In paywall.tsx - after purchase or skip:
const handleContinue = () => {
  router.replace('/(tabs)'); // Navigate to main app
};
```

Flow: `Onboarding → Paywall → Main App (tabs)`

### Paywall Subscription Options (REQUIRED)

Paywall MUST have two subscription options:

1. **Weekly** - Default option
2. **Yearly** - With "50% OFF" badge (recommended, should be highlighted)

```tsx
// Subscription option component example:
const subscriptionOptions = [
  {
    id: 'weekly',
    title: t('paywall.weekly'),
    price: '$4.99/week',
    selected: selectedPlan === 'weekly',
  },
  {
    id: 'yearly',
    title: t('paywall.yearly'),
    price: '$129.99/year',
    badge: '50% OFF',
    selected: selectedPlan === 'yearly',
  },
];

// Yearly option should be visually highlighted as the best value
```

- Yearly option should show the discount badge prominently
- Default selection can be weekly, but yearly should be visually recommended
- Use RevenueCat package identifiers to match these options

### Settings Screen Options (REQUIRED)

Settings screen MUST include:

1. **Language** - Change app language
2. **Theme** - Light/Dark/System
3. **Notifications** - Enable/disable notifications
4. **Remove Ads** - Navigate to paywall (hidden if already premium)
5. **Reset Onboarding** - Restart onboarding flow (for testing/demo)

```tsx
const { isPremium } = usePurchases();

// Remove Ads - navigates to paywall
const handleRemoveAds = () => {
  router.push('/paywall');
};

// Reset onboarding
const handleResetOnboarding = async () => {
  await setOnboardingCompleted(false);
  router.replace('/onboarding');
};

// In settings list:
{!isPremium && (
  <SettingsItem
    title={t('settings.removeAds')}
    icon="crown.fill"
    onPress={handleRemoveAds}
  />
)}

<SettingsItem
  title={t('settings.resetOnboarding')}
  icon="arrow.counterclockwise"
  onPress={handleResetOnboarding}
/>
```

## Localization

- File: `lib/i18n.ts`
- Languages stored in `locales/`
- App restarts on language change

## Coding Standards

- Use functional components
- Strict TypeScript
- Avoid hardcoded strings
- Use padding instead of lineHeight
- Use memoization when necessary

## Context Providers

```tsx
<ThemeProvider>
  <OnboardingProvider>
    <AdsProvider>
      <Stack />
    </AdsProvider>
  </OnboardingProvider>
</ThemeProvider>
```

## useColorScheme Hook

File: `src/hooks/use-color-scheme.ts`

```tsx
import { useThemeContext } from '@/context/theme-context';

export function useColorScheme(): 'light' | 'dark' | 'unspecified' {
  const { isDark } = useThemeContext();
  return isDark ? 'dark' : 'light';
}
```

## Important Notes

1. iOS permissions are defined in `app.json`
2. Android permissions are defined in `app.json`
3. Enable new architecture via `newArchEnabled: true`
4. Enable typed routes via `experiments.typedRoutes`

## App Store & Play Store Notes

- iOS ATT permission required
- Restore purchases must work correctly
- Target SDK must be up to date

## Testing Checklist

- UI tested in all languages
- Dark / Light mode
- Notifications
- Premium flow
- Restore purchases
- Offline support
- Multiple screen sizes

## After Development

```bash
npx expo prebuild --clean
bun ios
bun android
```

> NOTE: `prebuild --clean` recreates ios and android folders. Run it after modifying native modules or app.json.
