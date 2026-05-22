---
name: expo-llm-docs
description: Fetch Expo documentation via llms.txt for up-to-date React Native development references
agents: [tap, blaze]
triggers: [expo, expo router, eas build, eas update, expo sdk, development build]
llm_docs_url: https://docs.expo.dev/llms.txt
---

# Expo LLM Documentation

Expo provides extensive LLM-optimized documentation at `https://docs.expo.dev/llms.txt`.

## When to Use

Fetch this documentation when:
- Setting up a new Expo project or development build
- Configuring Expo Router for navigation
- Working with EAS Build, Submit, or Update
- Using Expo SDK modules (Camera, Location, Notifications, etc.)
- Creating native modules with Expo Modules API
- Deploying to app stores or using internal distribution

## Key Topics Covered

- **Get Started**: Project creation, environment setup, development builds
- **Expo Router**: File-based routing, layouts, navigation patterns, modals
- **EAS Services**: Build, Submit, Update, Metadata, Hosting, Workflows
- **SDK Modules**: Camera, FileSystem, Notifications, SQLite, Video, Audio
- **Native Development**: Config plugins, Expo Modules API, Swift/Kotlin
- **Deployment**: App stores, OTA updates, code signing, rollouts

## Quick Reference

```typescript
// Fetch Expo docs via Firecrawl
const docs = await firecrawl.scrape({
  url: "https://docs.expo.dev/llms.txt",
  formats: ["markdown"]
});
```

## Popular SDK Modules

| Module | Description |
|--------|-------------|
| `expo-router` | File-based routing |
| `expo-camera` | Camera access |
| `expo-notifications` | Push notifications |
| `expo-location` | Geolocation |
| `expo-sqlite` | SQLite database |
| `expo-secure-store` | Encrypted storage |
| `expo-file-system` | File operations |
| `expo-image` | Performant images |

## Related Skills

- `react-native-llm-docs` - React Native core documentation
- `better-auth-expo` - Better Auth for Expo
- `expo-patterns` - Expo development patterns
