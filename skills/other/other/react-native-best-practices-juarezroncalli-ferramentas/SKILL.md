---
name: react-native-best-practices
description: React Native & Expo engineering standards.
category: development
version: 4.1.0-fractal
layer: master-skill
---

# React Native & Expo Best Practices

> **Goal**: Build "Write Once, Run Everywhere" mobile apps that feel 100% native.

## 1. Architecture: Expo Router

- **File-based Routing**: Use `app/` directory similar to Next.js.
- **Linking**: Define schemes in `app.json` for deep linking.
- **Layouts**: Use `_layout.tsx` for shared navigation wrappers (Stack, Tabs).

## 2. UI & Styling

- **NativeWind**: Use `nativewind` (Tailwind for RN) for styling. It's faster and more familiar.
- **FlashList**: Replace `FlatList` with Shopify's `FlashList` for 5x performance on long lists.
- **Safe Area**: Always wrap screen content in `SafeAreaView` (or use spacing tokens that account for insets).

## 3. Performance Optimization

- **Image Caching**: Use `expo-image` instead of React Native's `<Image />`.
    - Features: Blurhash, caching, preloading.
- **Reanimated**: Use `react-native-reanimated` for 60fps animations (runs on UI thread), avoiding the JS bridge.
- **Hermes**: Ensure Hermes engine is enabled in `app.json` for faster startup and smaller bundle size.

## 4. Data Management

- **TanStack Query (React Query)**: Standard for async server state. Handle `offline` status gracefully.
- **MMKV**: Use `react-native-mmkv` for synchronous local storage (replacing Async Storage). It is ~30x faster.

## 5. Debugging & Dev Experience

- **EAS Build**: Use Expo Application Services (EAS) for cloud builds.
- **Expo Go**: Use for rapid prototyping, but switch to "Development Build" (Prebuild) if adding native modules.

---

**Checklist**:
- [ ] Is Hermes enabled?
- [ ] Are images using `expo-image`?
- [ ] Is navigation handled by Expo Router?
- [ ] Are heavy computations moved off the JS thread?
