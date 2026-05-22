---
name: expo-workflow
description: Expo SDK 54+ workflows, EAS Build/Update, Expo Router v6, native tabs. Use for Expo development or OTA update strategies.
---

# Expo Workflow Expert (SDK 54+)

Comprehensive expertise in Expo SDK 54+ development workflows, EAS (Expo Application Services), and optimization strategies for rapid mobile development. Specializes in native tabs, Expo Router v6, iOS Liquid Glass, Android edge-to-edge, and modern deployment pipelines.

## What I Know

### Expo SDK 54 Features (August 2025)

**What's New in SDK 54**
- **Native Tab Bar Navigation**: True native tabs via React Navigation 7
- **iOS Liquid Glass Support**: Translucent glass effects (iOS 26+)
- **Android Edge-to-Edge**: Default immersive display
- **expo-video & expo-audio**: New media APIs replacing expo-av
- **expo-image v2**: useImage hook for imperative loading
- **React Native 0.81**: Foundation with New Architecture
- **Improved Developer Experience**: Faster builds, better error messages

**Breaking Changes from SDK 53**
- `expo-av` deprecated → use `expo-video` and `expo-audio`
- Tab navigation API changes for native tabs
- Android edge-to-edge now default (adjust padding)

### Expo Fundamentals

**Managed vs Bare Workflow**
- Managed workflow: Full Expo SDK, minimal native code
- Bare workflow: Full native code access with Expo modules
- **CNG (Continuous Native Generation)**: Best of both worlds
- Migration strategies between workflows

**Expo Go vs Development Builds**
- Expo Go: Quick testing, limited native modules
- Dev Client: Full native module support, custom builds
- When to switch from Expo Go to dev builds
- Creating custom dev clients with EAS Build

**Expo SDK & Modules**
- Core Expo modules (expo-camera, expo-location, expo-video, expo-audio)
- Third-party native module compatibility
- Module installation: `npx expo install <package>`
- Autolinking handles native setup automatically

### EAS Build (Cloud Builds)

**Build Profiles**
- Development builds: Fast iteration, dev client
- Preview builds: Internal testing, TestFlight/Internal Testing
- Production builds: App Store/Play Store submission
- Custom build profiles in eas.json

**Platform-Specific Configuration**
- iOS credentials management
- Android keystore handling
- Build caching strategies
- Environment variable injection

**Build Optimization**
- Caching node_modules and gradle dependencies
- Incremental builds
- Build machine types (M1, Ubuntu)
- Build time reduction strategies

### EAS Update (OTA Updates)

**Over-The-Air Updates**
- JavaScript bundle updates without app store submission
- Update channels and branches
- Rollout strategies (gradual rollout, instant rollout)
- Rollback capabilities

**Update Workflows**
- Development channel: Continuous updates
- Preview channel: QA testing
- Production channel: Staged rollouts
- Emergency hotfix workflows

**Update Best Practices**
- Version compatibility management
- Update frequency optimization
- Monitoring update adoption
- Handling update failures gracefully

### App Configuration

**app.json / app.config.js**
- App metadata (name, slug, version)
- Platform-specific configurations
- Asset and icon configuration
- Splash screen customization
- Deep linking setup (scheme, associated domains)
- Permissions configuration
- Build-time environment variables

**eas.json**
- Build profile configuration
- Submit profile setup
- Environment secrets management
- Platform-specific build settings

**Dynamic Configuration**
- Environment-specific configs (dev, staging, prod)
- Feature flags integration
- App variants (white-label apps)

### Development Workflow

**Fast Refresh & Hot Reloading**
- Understanding fast refresh behavior
- Troubleshooting fast refresh issues
- When to use full reload vs fast refresh

**Debugging Tools**
- React DevTools integration
- Remote debugging with Chrome DevTools
- Flipper for advanced debugging
- Network request inspection
- Performance profiling

**Local Development**
- Running on physical devices (QR code scanning)
- Running on simulators/emulators
- Offline development strategies
- Tunnel mode vs LAN mode

### Deployment & Distribution

**App Store Submission**
- iOS: TestFlight, App Store Connect integration
- Android: Internal testing, Play Store submission
- EAS Submit command automation
- Store metadata management

**Internal Distribution**
- Ad-hoc iOS builds
- Android APK distribution
- Enterprise distribution
- TestFlight external testing

**CI/CD Integration**
- GitHub Actions with EAS Build
- GitLab CI integration
- Automated build triggers
- Automated OTA updates on merge

## When to Use This Skill

Ask me when you need help with:
- Setting up Expo SDK 54+ development workflow
- Creating development builds with EAS Build
- Configuring app.json or eas.json
- Setting up over-the-air updates with EAS Update
- Troubleshooting Expo Go limitations
- Optimizing build times
- Managing app credentials and secrets
- Configuring deep linking and URL schemes
- Setting up CI/CD pipelines for Expo apps
- Deploying to App Store or Play Store
- Understanding Expo SDK 54 capabilities
- Migrating from Expo Go to dev client
- Handling native modules in Expo projects
- **Implementing native tab navigation**
- **Setting up iOS Liquid Glass effects**
- **Configuring Android edge-to-edge display**
- **Migrating from expo-av to expo-video/expo-audio**
- **Using Expo Router v6 file-based routing**

## Essential Expo Commands

### Project Setup
```bash
# Create new Expo project
npx create-expo-app@latest MyApp

# Navigate to project
cd MyApp

# Start development server
npx expo start

# Install Expo module
npx expo install expo-camera

# Check project health
npx expo-doctor
```

### Development
```bash
# Start with cache cleared
npx expo start -c

# Start with specific mode
npx expo start --dev-client  # Development build
npx expo start --go          # Expo Go

# Run on specific platform
npx expo run:ios
npx expo run:android

# Prebuild native projects (bare workflow)
npx expo prebuild
```

### EAS Build
```bash
# Login to EAS
eas login

# Configure EAS
eas build:configure

# Build for all platforms
eas build --platform all

# Build development version
eas build --profile development --platform ios

# Build for production
eas build --profile production --platform all

# Check build status
eas build:list
```

### EAS Update
```bash
# Configure EAS Update
eas update:configure

# Publish update to default channel
eas update --branch production --message "Fix critical bug"

# Publish to specific channel
eas update --channel preview --message "QA testing"

# List published updates
eas update:list

# Rollback update
eas update:rollback
```

### EAS Submit
```bash
# Submit to App Store
eas submit --platform ios

# Submit to Play Store
eas submit --platform android

# Submit specific build
eas submit --platform ios --id <build-id>
```

## Pro Tips & Tricks

### 1. Development Build Optimization

Create a reusable development build once, then use EAS Update for daily changes:

```json
// eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    }
  }
}
```

Build once:
```bash
eas build --profile development --platform all
```

Update JavaScript daily:
```bash
eas update --branch development --message "Daily changes"
```

### 2. Environment-Based Configuration

Use app.config.js for dynamic configuration:

```javascript
// app.config.js
export default ({ config }) => {
  const isProduction = process.env.APP_ENV === 'production';

  return {
    ...config,
    name: isProduction ? 'MyApp' : 'MyApp Dev',
    slug: 'myapp',
    extra: {
      apiUrl: isProduction
        ? 'https://api.myapp.com'
        : 'https://dev-api.myapp.com',
      analyticsKey: process.env.ANALYTICS_KEY,
    },
    updates: {
      url: 'https://u.expo.dev/your-project-id'
    }
  };
};
```

### 3. Fast Credential Setup

Let EAS manage credentials automatically:

```json
// eas.json
{
  "build": {
    "production": {
      "ios": {
        "credentialsSource": "remote"
      },
      "android": {
        "credentialsSource": "remote"
      }
    }
  }
}
```

### 4. Efficient Build Caching

Speed up builds by caching dependencies:

```json
// eas.json
{
  "build": {
    "production": {
      "cache": {
        "key": "myapp-v1",
        "paths": ["node_modules", "ios/Pods", "android/.gradle"]
      }
    }
  }
}
```

### 5. Gradual OTA Rollout

Safely deploy updates to production:

```bash
# Start with 10% rollout
eas update --branch production --message "New feature" --rollout-percentage 10

# Monitor metrics, then increase
eas update:configure-rollout --branch production --percentage 50

# Full rollout
eas update:configure-rollout --branch production --percentage 100
```

### 6. Quick Testing on Physical Devices

For Expo Go (quick testing):
```bash
# Start dev server
npx expo start

# Scan QR code with:
# - iOS: Camera app
# - Android: Expo Go app
```

For dev client (full features):
```bash
# Install dev client once
eas build --profile development --platform ios

# Daily JavaScript updates via EAS Update
eas update --branch development
```

### 7. Troubleshooting Common Issues

**"Unable to resolve module"**
```bash
# Clear Metro cache
npx expo start -c

# Reinstall dependencies
rm -rf node_modules && npm install
```

**"Build failed on EAS"**
```bash
# Check build logs
eas build:list
eas build:view <build-id>

# Run prebuild locally to catch issues early
npx expo prebuild
```

**"Update not appearing in app"**
```bash
# Check update channel matches app's channel
eas channel:list

# Verify update was published successfully
eas update:list --branch production

# Force reload in app (shake device → reload)
```

### 8. Native Module Integration

When you need a native module not in Expo SDK:

```bash
# Install the module
npm install react-native-awesome-module

# Prebuild to generate native projects
npx expo prebuild

# Rebuild dev client with new module
eas build --profile development --platform all

# Continue using EAS Update for JS changes
eas update --branch development
```

### 9. Native Tab Navigation (SDK 54+)

Enable true native tab bars with Expo Router v6:

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Platform } from 'react-native';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        // Enable native tabs (iOS has translucent effect by default)
        tabBarStyle: Platform.select({
          ios: { position: 'absolute' }, // For Liquid Glass
          default: {},
        }),
      }}
    >
      <Tabs.Screen
        name="index"
        options={{ title: 'Home', tabBarIcon: ({ color }) => <HomeIcon color={color} /> }}
      />
      <Tabs.Screen
        name="profile"
        options={{ title: 'Profile', tabBarIcon: ({ color }) => <ProfileIcon color={color} /> }}
      />
    </Tabs>
  );
}
```

### 10. iOS Liquid Glass (SDK 54+ / iOS 26+)

Create beautiful translucent effects:

```typescript
// components/GlassCard.tsx
import { View, StyleSheet, Platform } from 'react-native';
import { BlurView } from 'expo-blur';

export function GlassCard({ children }) {
  if (Platform.OS === 'ios' && parseInt(Platform.Version, 10) >= 26) {
    return (
      <BlurView
        style={styles.card}
        intensity={60}
        tint="systemMaterial" // Liquid Glass tint
      >
        {children}
      </BlurView>
    );
  }

  return <View style={[styles.card, styles.fallback]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  fallback: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
  },
});
```

### 11. Android Edge-to-Edge (SDK 54+)

Handle immersive display properly:

```typescript
// app/_layout.tsx
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { View, StyleSheet, Platform } from 'react-native';

export default function RootLayout() {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={[
        styles.container,
        {
          // Account for edge-to-edge on Android 15+
          paddingTop: insets.top,
          paddingBottom: insets.bottom,
        },
      ]}
    >
      <Slot />
    </View>
  );
}
```

```javascript
// app.json - enable edge-to-edge
{
  "expo": {
    "android": {
      "edgeToEdge": true  // SDK 54 default
    }
  }
}
```

### 12. expo-video (Replacing expo-av)

Modern video playback:

```typescript
// components/VideoPlayer.tsx
import { useVideoPlayer, VideoView } from 'expo-video';
import { useEvent } from 'expo';
import { StyleSheet, View } from 'react-native';

export function VideoPlayer({ source }: { source: string }) {
  const player = useVideoPlayer(source, (player) => {
    player.loop = true;
    player.play();
  });

  useEvent(player, 'statusChange', ({ status }) => {
    console.log('Player status:', status);
  });

  return (
    <View style={styles.container}>
      <VideoView
        style={styles.video}
        player={player}
        allowsFullscreen
        allowsPictureInPicture
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  video: { width: '100%', aspectRatio: 16 / 9 },
});
```

### 13. expo-audio (Replacing expo-av)

Modern audio handling:

```typescript
// hooks/useAudio.ts
import { useAudioPlayer, useAudioPlayerStatus } from 'expo-audio';

export function useAudio(source: string) {
  const player = useAudioPlayer(source);
  const status = useAudioPlayerStatus(player);

  return {
    play: () => player.play(),
    pause: () => player.pause(),
    seek: (position: number) => player.seekTo(position),
    isPlaying: status.playing,
    position: status.currentTime,
    duration: status.duration,
  };
}
```

### 14. expo-image v2 with useImage

Imperative image loading:

```typescript
import { useImage, Image } from 'expo-image';

export function PreloadedImage({ uri }: { uri: string }) {
  const image = useImage(uri, {
    onError: (error) => console.error('Failed to load image:', error),
  });

  if (!image) {
    return <ActivityIndicator />;
  }

  return (
    <Image
      source={image}
      style={{ width: image.width, height: image.height }}
      contentFit="cover"
    />
  );
}
```

## Integration with SpecWeave

**Increment Planning**
- Document Expo setup steps in `spec.md`
- Include EAS Build/Update configuration in `plan.md`
- Track build and deployment tasks in `tasks.md`

**Testing Strategy**
- Use dev builds for feature development
- Preview builds for QA testing
- Production builds for stakeholder demos

**Living Documentation**
- Document build profiles in `.specweave/docs/internal/operations/`
- Track deployment procedures in runbooks
- Maintain credential management procedures

**Cost Optimization**
- Use EAS Update instead of rebuilding for JS-only changes
- Cache dependencies to reduce build times
- Monitor EAS usage in increment reports
