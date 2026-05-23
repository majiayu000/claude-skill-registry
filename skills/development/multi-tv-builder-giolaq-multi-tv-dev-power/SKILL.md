---
name: multi-tv-builder
displayName: "Multi-TV Builder"
description: "Complete knowledge base for building production-ready cross-platform TV applications with React Native - supporting Android TV, Apple TV, Fire TV (Fire OS & Vega OS), and Web TV platforms with a single codebase. Use when implementing TV apps, monorepo architecture, spatial navigation, video playback, platform-specific optimizations, or migrating from Vega to multi-platform."
keywords: ["tv", "react-native", "android-tv", "apple-tv", "fire-tv", "vega", "tvos", "web-tv", "video", "streaming", "spatial-navigation", "monorepo", "expo", "migration", "typescript", "cross-platform", "remote-control", "focus-management"]
author: "Giovanni Laquidara"
---

# Multi-TV Builder - Complete Knowledge Base

Build production-ready cross-platform TV applications with React Native, supporting Android TV, Apple TV, Fire TV (Fire OS & Vega OS), and Web TV platforms with a single codebase.

## Quick Reference

- **Sample Repo**: https://github.com/AmazonAppDev/react-native-multi-tv-app-sample
- **Slash Commands**: `/multi-tv-help`, `/multi-tv-setup`, `/multi-tv-build`, `/multi-tv-platform`
- **Skills**: `multi-tv-builder`, `apple-tv-troubleshooter`, `tmdb-integration`
- **Author**: Giovanni Laquidara

## Core Capabilities

- **Cross-platform TV support** with single codebase for 5+ platforms
- **Monorepo architecture** with Yarn workspaces for apps and shared packages
- **Spatial navigation** optimized for TV remote controls and D-pad input
- **Video playback** with custom controls and remote integration
- **Platform-specific optimizations** using automatic file resolution
- **Shared UI library** with reusable TV-optimized components
- **TypeScript-first** with strict type safety across all packages

## Supported Platforms

| Platform | Technology | Output |
|----------|-----------|--------|
| Android TV | react-native-tvos | APK/AAB |
| Apple TV (tvOS) | react-native-tvos + Expo | IPA |
| Fire TV (Fire OS) | react-native-tvos | APK |
| Fire TV (Vega OS) | Amazon Vega SDK | Optimized VPKG |
| Web TV | React Native Web | HTML/JS Bundle |

---

# Product Overview

## React Native Multi-TV App Sample

A production-ready TV application template for building cross-platform TV apps with a single React Native codebase.

### Core Features

1. **Video Playback**
   - Integrated video player with react-native-video (universal) or W3C Media APIs (Vega)
   - Custom overlay controls with play/pause, seek bar, and time display
   - Remote control integration (play/pause, seek ±10s, exit)
   - Auto-hide controls after 5s of inactivity
   - Buffering indicators during loading

2. **Spatial Navigation**
   - React TV Space Navigation for focus management
   - D-pad/arrow key navigation optimized for TV remotes
   - Platform-specific remote control managers
   - Focus restoration when returning from player

3. **Content Discovery**
   - Dynamic content loading from external catalog API
   - Grid layouts optimized for TV screens
   - Detail screens with rich metadata (genre, rating, duration, year)
   - Dynamic hero banner based on focused content
   - Trending flags and content ratings

4. **Navigation**
   - Drawer navigation with left-side menu
   - Stack navigation for detail screens
   - Platform-specific navigation optimizations
   - Deep linking support (optional)

5. **Responsive Design**
   - Adaptive layouts for different TV screen sizes
   - Responsive scaling with useScale hook
   - Platform-specific layout adjustments
   - Safe zone handling for TV overscan

### App Variants

1. **expo-multi-tv** - Universal app supporting Android TV, Apple TV, Fire TV (Fire OS), and Web
2. **vega** - Fire TV Vega OS optimized build using Amazon Vega SDK

### Key Use Cases

- Streaming video applications
- Content discovery and browsing
- TV-optimized user interfaces
- Cross-platform TV development reference

---

# Architecture & Structure

## Monorepo Organization

```
project-root/
├── apps/                    # Application packages
│   ├── expo-multi-tv/      # Universal TV app
│   └── vega/               # Fire TV Vega optimized
├── packages/               # Shared packages
│   └── shared-ui/          # Shared components
├── package.json            # Workspace configuration
├── tsconfig.base.json      # Shared TypeScript config
├── babel.config.js         # Root babel configuration
└── yarn.lock               # Dependency lock file
```

## Apps Directory

### `apps/expo-multi-tv/`
Universal TV application built with Expo SDK.

**Key Files:**
- `App.tsx` - Main entry point
- `app.json` - Expo configuration
- `package.json` - App-specific dependencies
- `tsconfig.json` - TypeScript config extending base
- `metro.config.js` - Metro bundler configuration
- `ios/` - iOS/tvOS native code
- `android/` - Android TV native code

**Platforms Supported:**
- Android TV
- Apple TV (tvOS)
- Fire TV (Fire OS)
- Web (LG WebOS, Samsung Tizen)

### `apps/vega/`
Fire TV Vega OS optimized application using Amazon Vega SDK.

**Key Files:**
- `App.tsx` - Main entry point
- `package.json` - Vega-specific dependencies
- `tsconfig.json` - TypeScript config
- `metro.config.js` - Metro bundler configuration
- `android/` - Fire TV Vega native code

**Platform Supported:**
- Fire TV (Vega OS)

## Shared UI Package Structure

```
packages/shared-ui/src/
├── app/                           # App-level configuration
│   └── remote-control/           # Platform-specific remote managers
│       ├── RemoteControlManager.android.ts
│       ├── RemoteControlManager.ios.ts
│       └── RemoteControlManager.kepler.ts
├── assets/                        # Static assets (fonts, images, icons)
├── components/                    # Reusable UI components
│   ├── player/                   # Video player components
│   ├── CustomDrawerContent.tsx   # Drawer menu
│   ├── FocusablePressable.tsx    # TV-optimized pressable
│   ├── LoadingIndicator.tsx      # Loading spinner
│   ├── MenuContext.tsx           # Menu state management
│   └── PlatformLinearGradient.tsx # Cross-platform gradient
├── data/                          # Data and API
│   └── moviesData.ts             # Movie catalog API
├── hooks/                         # Custom React hooks
│   └── useScale.ts               # Responsive scaling
├── navigation/                    # Navigation configuration
│   ├── AppNavigator.tsx          # Main app navigator
│   ├── DrawerNavigator.tsx       # Drawer navigation
│   ├── RootNavigator.tsx         # Root wrapper
│   └── types.ts                  # Navigation types
├── screens/                       # Screen components
│   ├── DetailsScreen.tsx         # Content detail
│   ├── ExploreScreen.tsx         # Content exploration
│   ├── HomeScreen.tsx            # Home/landing
│   ├── PlayerScreen.tsx          # Video player
│   ├── PlayerScreen.vega.tsx     # Vega-specific player
│   ├── SettingsScreen.tsx        # Settings
│   └── TVScreen.tsx              # TV content
├── theme/                         # Design system
│   ├── colors.ts                 # Color palette
│   ├── spacing.ts                # Spacing scale
│   ├── typography.ts             # Font styles
│   ├── safeZones.ts              # TV safe zones
│   └── index.ts                  # Theme exports
├── utils/                         # Utility functions
└── index.ts                       # Package exports
```

## Platform-Specific File Resolution

Metro bundler automatically resolves platform files:
- `.kepler.ts/tsx` - Fire TV Vega OS (highest priority for Vega builds)
- `.android.ts/tsx` - Android TV & Fire TV Fire OS
- `.ios.ts/tsx` - Apple TV (tvOS)
- `.vega.tsx` - Vega-specific screens
- `.web.ts/tsx` - Web platforms (LG WebOS, Samsung Tizen)
- `.ts/tsx` - Default/shared implementation (lowest priority)

**Example:**
```
RemoteControlManager.android.ts  → Android TV
RemoteControlManager.ios.ts      → Apple TV
RemoteControlManager.kepler.ts   → Fire TV Vega
```

### Key Architectural Patterns

#### Shared UI Library Pattern
- All reusable components live in `@project/shared-ui` package
- Apps import from shared package, never local files
- Platform-specific implementations use file extensions
- Single source of truth for UI components and screens

#### TV-First Design
- **10-foot UI**: Larger touch targets, high-contrast colors, readable typography
- **Safe zones**: Content positioned within TV safe areas (see theme/safeZones.ts)
- **Focus management**: Clear visual focus indicators for all interactive elements
- **Remote control**: D-pad navigation with platform-specific key mappings

---

# Technology Stack

## Build System

- **Yarn Workspaces v4+**: Monorepo management
- **Metro Bundler**: Module bundling with platform-specific resolution
- **TypeScript v5.3+**: Strict mode enabled across all packages

## Core Technologies

- **React Native**: v0.74+ (react-native-tvos fork)
- **Expo SDK**: v51+ (for universal app)
- **React**: v18.2+
- **TypeScript**: v5.3+ with strict mode

## Navigation & Focus

- **React Navigation v6**: Drawer and stack navigators
- **React TV Space Navigation**: Spatial navigation for TV remotes
- **Platform Remote Managers**: Android (react-native-keyevent), iOS (TVEventHandler), Vega (Kepler SDK)

## Video Playback

- **react-native-video v6+**: Universal app video player
- **W3C Media APIs**: Native video for Vega OS
- Custom overlay controls with spatial navigation

## Platform-Specific SDKs

- **Amazon Vega SDK**: Fire TV Vega OS builds
- **@amazon-devices packages**: Kepler SDK components
- **react-native-tvos**: TV platform support (Android TV, Apple TV, Fire TV FOS)

## Development Tools

- **ESLint**: Code quality with TypeScript and React plugins
- **Prettier**: Code formatting (120 char width, single quotes)
- **Husky**: Git hooks for pre-commit checks
- **Commitlint**: Conventional commit enforcement
- **Jest**: Unit testing

---

# Implementation Patterns

## Workspace Configuration

**Root `package.json`:**
```json
{
  "name": "tv-app-project",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "packageManager": "yarn@4.5.0",
  "scripts": {
    "dev": "yarn workspace @project/expo-multi-tv start",
    "dev:android": "yarn workspace @project/expo-multi-tv android",
    "dev:ios": "yarn workspace @project/expo-multi-tv ios",
    "dev:web": "yarn workspace @project/expo-multi-tv web",
    "dev:vega": "yarn workspace @project/vega start",
    "build:vega": "yarn workspace @project/vega run build",
    "test:all": "yarn workspaces foreach -pt run test",
    "lint:all": "yarn workspaces foreach -pt run lint",
    "clean:all": "yarn workspaces foreach run clean"
  }
}
```

## Theme System

Centralized design tokens in `packages/shared-ui/src/theme/`:

**colors.ts:**
```typescript
export const colors = {
  primary: '#E50914',      // Netflix-style red
  background: '#141414',   // Dark background
  card: '#2F2F2F',        // Card background
  text: '#FFFFFF',        // Primary text
  textSecondary: '#B3B3B3' // Secondary text
};
```

**spacing.ts:**
```typescript
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48
};
```

**safeZones.ts:**
```typescript
export const safeZones = {
  horizontal: 48,  // Left/right margins for TV overscan
  vertical: 27     // Top/bottom margins
};
```

## Responsive Scaling

**useScale hook:**
```typescript
import { Dimensions } from 'react-native';

const BASE_WIDTH = 1920;
const BASE_HEIGHT = 1080;

export const useScale = () => {
  const { width, height } = Dimensions.get('window');

  const scaleWidth = width / BASE_WIDTH;
  const scaleHeight = height / BASE_HEIGHT;
  const scale = Math.min(scaleWidth, scaleHeight);

  return {
    scale: (size: number) => size * scale,
    width,
    height
  };
};
```

## Remote Control Manager Interface

All platform managers implement this interface:

```typescript
export interface RemoteControlManagerInterface {
  initialize(): void;
  cleanup(): void;
}
```

**Android/Fire TV FOS (`RemoteControlManager.android.ts`):**
```typescript
import ReactNativeKeyEvent from 'react-native-keyevent';

export class RemoteControlManager implements RemoteControlManagerInterface {
  initialize() {
    ReactNativeKeyEvent.onKeyDownListener((keyEvent) => {
      // Handle Android TV remote keys
    });
  }

  cleanup() {
    ReactNativeKeyEvent.removeKeyDownListener();
  }
}
```

**Apple TV (`RemoteControlManager.ios.ts`):**
```typescript
import { TVEventHandler } from 'react-native';

export class RemoteControlManager implements RemoteControlManagerInterface {
  private tvEventHandler: TVEventHandler | null = null;

  initialize() {
    this.tvEventHandler = new TVEventHandler();
    this.tvEventHandler.enable(this, (component, evt) => {
      // Handle tvOS remote events
    });
  }

  cleanup() {
    this.tvEventHandler?.disable();
  }
}
```

**Fire TV Vega (`RemoteControlManager.kepler.ts`):**
```typescript
import { TVEventHandler } from '@amazon-devices/react-native-kepler';

export class RemoteControlManager implements RemoteControlManagerInterface {
  private tvEventHandler: TVEventHandler | null = null;

  initialize() {
    this.tvEventHandler = new TVEventHandler();
    this.tvEventHandler.enable(this, (component, evt) => {
      // Handle Vega remote events
    });
  }

  cleanup() {
    this.tvEventHandler?.disable();
  }
}
```

## Spatial Navigation Setup

**Integration with React TV Space Navigation:**
```typescript
import { SpatialNavigation } from 'react-tv-space-navigation';

// Initialize in App.tsx
SpatialNavigation.init({
  debug: __DEV__,
  visualDebug: __DEV__
});

// Use in components
import { useFocusable } from 'react-tv-space-navigation';

const MyComponent = () => {
  const { ref, focused } = useFocusable();

  return (
    <View ref={ref} style={focused ? styles.focused : styles.default}>
      {/* Content */}
    </View>
  );
};
```

## Video Player Implementation

**Universal App (expo-multi-tv):**
```typescript
import Video from 'react-native-video';

<Video
  source={{ uri: videoUrl }}
  style={styles.video}
  controls={Platform.OS === 'ios'} // Native controls on iOS
  resizeMode="contain"
  onLoad={handleLoad}
  onProgress={handleProgress}
  ref={videoRef}
/>
```

**Vega App:**
```typescript
// Use W3C Media APIs through Kepler SDK
import { VideoView } from '@amazon-devices/react-native-kepler';

<VideoView
  source={{ uri: videoUrl }}
  style={styles.video}
  onLoad={handleLoad}
  ref={videoRef}
/>
```

## Dynamic Content Loading

**Catalog API Integration:**
```typescript
// packages/shared-ui/src/data/moviesData.ts
export interface Movie {
  id: string;
  title: string;
  genre: string;
  rating: number;
  contentRating: string;
  year: number;
  duration: number;
  videoUrl: string;
  imageUrl: string;
  trending: boolean;
}

export const fetchMovies = async (): Promise<Movie[]> => {
  const response = await fetch('https://api.example.com/catalog.json');
  const data = await response.json();
  return transformCatalogData(data);
};
```

---

# Common Commands

## Development

```bash
# Install all dependencies
yarn install

# Start Metro bundler for expo-multi-tv
yarn dev

# Run on specific platforms
yarn dev:android    # Android TV & Fire TV FOS
yarn dev:ios        # Apple TV
yarn dev:web        # Web TV platforms

# Start Metro bundler for vega
yarn dev:vega
```

## Building

**Expo Multi-TV App:**
```bash
# Build for all platforms
cd apps/expo-multi-tv

# Android TV / Fire TV (Fire OS)
npx expo build:android
# or: npx expo run:android

# Apple TV (tvOS)
npx expo build:ios
# or: npx expo run:ios

# Web TV platforms
npx expo export --platform web
```

**Fire TV Vega App:**
```bash
# From project root
yarn build:vega         # Build release VPKG
yarn build:vega:debug   # Build debug VPKG

# From apps/vega directory
cd apps/vega

# Build with npm (default from Vega CLI)
npm run build:app       # Builds for all architectures

# Build with Vega CLI (more control)
vega build --arch armv7 --buildType release    # Fire TV Stick
vega build --arch aarch64 --buildType release  # M-series Mac virtual devices
vega build --arch x86_64 --buildType release   # Intel virtual devices

# Clean build
rm -rf build && npm run build:app
```

## Testing & Linting

```bash
# Run tests across all workspaces
yarn test:all

# Lint all workspaces
yarn lint:all

# Type check
yarn typecheck

# Format code
yarn format
```

## Vega CLI Commands

**Project Management:**
```bash
# List available project templates
vega project list-templates

# Generate new Vega project (files are created in current directory)
# First create and cd into target directory, then generate:
mkdir -p myapp && cd myapp
vega project generate -n myapp --template helloWorld

# Verify Vega SDK installation
vega --version
```

**Building:**
```bash
# Build for specific architecture and build type
vega build --arch <armv7|aarch64|x86_64> --buildType <debug|release>

# Examples:
vega build --arch armv7 --buildType release     # Production Fire TV Stick build
vega build --arch aarch64 --buildType debug     # Debug build for M-series Mac
vega build --arch x86_64 --buildType debug      # Debug build for Intel virtual device
```

**Device Management:**
```bash
# List connected devices
vega device list

# Install VPKG on device
vega install --vpkg <path-to-vpkg-file>

# Run app on device
vega run --packageId com.company.myapp
```

---

# Getting Started

## Quick Start (Recommended)

The fastest way to get started is to clone the official React Native Multi-TV App Sample repository.

**Clone the Repository:**
```bash
# Clone the official sample repository
git clone https://github.com/AmazonAppDev/react-native-multi-tv-app-sample.git
cd react-native-multi-tv-app-sample

# Install dependencies
yarn install

# Bootstrap the monorepo
yarn bootstrap
```

**What's Included:**
- ✅ Pre-configured monorepo with Yarn workspaces
- ✅ expo-multi-tv app - Universal app for Android TV, Apple TV, Fire TV (Fire OS), and Web
- ✅ vega app - Fire TV Vega OS optimized app
- ✅ shared-ui package - Complete component library
- ✅ All configuration files

**Next Steps After Cloning:**
1. Review the codebase
2. Set up for Expo TV - Follow Expo TV documentation
3. Set up for Vega (optional) - Install Vega SDK
4. Run on platforms
5. Customize for your needs

## Alternative: Build from Scratch

### 1. Initialize Project Structure

```bash
# Create project directory
mkdir my-tv-app && cd my-tv-app

# Initialize package.json
yarn init -y

# Create directory structure
mkdir -p apps packages/shared-ui
```

### 2. Configure Shared TypeScript

Create `tsconfig.base.json`:
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "CommonJS",
    "lib": ["ES2021"],
    "jsx": "react-native",
    "strict": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

### 3. Set Up Shared UI Package

```bash
cd packages/shared-ui
yarn init -y

# Install dependencies
yarn add react react-native
yarn add -D typescript @types/react @types/react-native

# Create src directory structure
mkdir -p src/{components,screens,navigation,hooks,theme,app/remote-control,data,utils,assets}
```

### 4. Create Universal App (expo-multi-tv)

**IMPORTANT:** Follow the official Expo TV setup guide.

Option 1: Start with the basic TV template:
```bash
cd apps
npx create-expo-app@latest expo-multi-tv -e with-tv
```

Option 2: Start with the TV Router template (recommended):
```bash
cd apps
npx create-expo-app@latest expo-multi-tv -e with-router-tv
```

**After creating the app:**

1. Link shared-ui package by editing `apps/expo-multi-tv/package.json`
2. Install additional TV dependencies
3. Configure Metro bundler for monorepo

### 5. Create Vega App (Optional - Fire TV Vega OS Only)

**Prerequisites: Install Vega SDK**

**Required Dependencies (macOS):**
```bash
# For Apple Silicon Macs (includes Rosetta 2)
[[ $(arch) == "arm64" ]] && softwareupdate --install-rosetta --agree-to-license; brew update && brew install binutils coreutils gawk findutils grep jq lz4 gnu-sed watchman

# For Intel Macs
brew update && brew install binutils coreutils gawk findutils grep jq lz4 gnu-sed watchman
```

**Install Vega SDK:**
1. Close VS Code before installing
2. Download and run installer
3. Add export commands to shell config
4. Verify: `kepler --version`

**Create Vega Project:**
```bash
# Files are generated in current directory, so create and cd into target first
mkdir -p apps/vega
cd apps/vega

vega project generate -n vega --template helloWorld
```

### 6. Configure Metro Bundler

**metro.config.js** (in each app):
```javascript
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

// Add monorepo support
const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

module.exports = config;
```

---

# Vega to Multi-TV Migration Guide

## Prerequisites

- Node.js 18+
- Yarn 4.x (Berry)
- Java 17 (for Android builds)
- Android SDK with TV emulator
- Xcode (for Apple TV builds)

## Phase 1: Monorepo Setup

### 1.1 Initialize Yarn Workspaces

Create root `package.json`:

```json
{
  "name": "@mycompany/multi-tv",
  "version": "1.0.0",
  "private": true,
  "packageManager": "yarn@4.5.0",
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "resolutions": {
    "metro-source-map": "0.80.12"
  }
}
```

**CRITICAL**: The `metro-source-map` resolution is required to fix a babel plugin error. Without it, you'll get:
```
.plugins[0] must be a string, object, function
```

### 1.2 Create Root Babel Config

**CRITICAL**: Create `babel.config.js` at monorepo root. Metro looks for babel config starting from the project root.

```javascript
const path = require('path');

module.exports = function (api) {
  api.cache(true);

  // Try to resolve reanimated plugin from the universal TV app
  let reanimatedPlugin;
  try {
    reanimatedPlugin = require.resolve('react-native-reanimated/plugin', {
      paths: [path.join(__dirname, 'apps/universal-tv/node_modules')]
    });
  } catch (e) {
    try {
      reanimatedPlugin = require.resolve('react-native-reanimated/plugin');
    } catch (e2) {
      reanimatedPlugin = null;
    }
  }

  const plugins = reanimatedPlugin ? [reanimatedPlugin] : [];

  return {
    presets: ['babel-preset-expo'],
    plugins,
  };
};
```

## Phase 2: Shared UI Package Setup

### Platform-Specific File Resolution

| Extension | Platform | Description |
|-----------|----------|-------------|
| `.ts` / `.tsx` | All | Base/shared implementation |
| `.native.ts` | React Native | Android TV, Apple TV, Fire TV FOS |
| `.android.ts` | Android | Android TV, Fire TV FOS |
| `.ios.ts` | iOS/tvOS | Apple TV |
| `.kepler.ts` | Vega | Fire TV Vega OS specific |
| `.web.ts` | Web | Web TV specific |

**CRITICAL - Avoiding Circular Dependencies**:

When you have a base class that platform-specific files extend, Metro's platform resolution can create a circular dependency.

```
# BAD - Creates circular dependency
RemoteControlManager.ts        # Base class
RemoteControlManager.android.ts # Imports from RemoteControlManager.ts
```

**FIX**: Rename base files to use `.base.ts` extension:

```
# GOOD - No circular dependency
RemoteControlManager.base.ts    # Base class
RemoteControlManager.android.ts # Imports from RemoteControlManager.base.ts
RemoteControlManager.ios.ts     # Imports from RemoteControlManager.base.ts
```

## Phase 3: Universal TV App Setup (Expo)

### Fix HMRClient Error (CRITICAL)

**CRITICAL**: The `react-native-tvos` fork has an HMR (Hot Module Replacement) incompatibility.

**Fix**: Add HMRClient polyfill to `apps/universal-tv/index.js`:

```javascript
import { registerRootComponent } from 'expo';
import { AppRegistry } from 'react-native';
import App from './App';

// Polyfill for HMRClient to prevent "Module has not been registered as callable" error
if (!AppRegistry.getRunnable('HMRClient')) {
  AppRegistry.registerCallableModule('HMRClient', {
    setup: () => {},
    enable: () => {},
    disable: () => {},
  });
}

registerRootComponent(App);
```

### Configure app.json

```json
{
  "expo": {
    "name": "MyTVApp",
    "slug": "my-tv-app",
    "version": "1.0.0",
    "orientation": "landscape",
    "userInterfaceStyle": "dark",
    "plugins": [
      "@react-native-tvos/config-tv"
    ]
  }
}
```

## Phase 4: Platform Abstraction Layer

### Remote Control Manager Pattern

Create base class in `packages/shared-ui/src/app/remote-control/RemoteControlManager.base.ts`:

```typescript
export type RemoteKey =
  | 'up' | 'down' | 'left' | 'right'
  | 'select' | 'back'
  | 'play' | 'pause' | 'playPause'
  | 'fastForward' | 'rewind'
  | 'menu';

export interface RemoteKeyEvent {
  key: RemoteKey;
  action: 'keyDown' | 'keyUp';
  timestamp: number;
}

export type RemoteKeyHandler = (event: RemoteKeyEvent) => void;

export interface RemoteControlManagerInterface {
  initialize(): void;
  cleanup(): void;
  addKeyListener(handler: RemoteKeyHandler): () => void;
  removeKeyListener(handler: RemoteKeyHandler): void;
}

export class BaseRemoteControlManager implements RemoteControlManagerInterface {
  protected listeners: Set<RemoteKeyHandler> = new Set();

  initialize(): void {
    // Override in platform-specific implementation
  }

  cleanup(): void {
    this.listeners.clear();
  }

  addKeyListener(handler: RemoteKeyHandler): () => void {
    this.listeners.add(handler);
    return () => this.removeKeyListener(handler);
  }

  removeKeyListener(handler: RemoteKeyHandler): void {
    this.listeners.delete(handler);
  }

  protected notifyListeners(event: RemoteKeyEvent): void {
    this.listeners.forEach((handler) => handler(event));
  }
}
```

### Video Player Service Pattern

Create interface in `packages/shared-ui/src/services/videoPlayer/VideoPlayerService.ts`:

```typescript
export interface VideoSource {
  uri: string;
  type?: 'hls' | 'dash' | 'mp4';
  headers?: Record<string, string>;
  drm?: DRMConfig;
}

export interface DRMConfig {
  type: 'widevine' | 'fairplay' | 'playready';
  licenseServer: string;
  headers?: Record<string, string>;
}

export interface PlaybackState {
  isPlaying: boolean;
  isPaused: boolean;
  isBuffering: boolean;
  currentTime: number;
  duration: number;
}

export interface VideoPlayerService {
  initialize(): Promise<void>;
  load(source: VideoSource): Promise<void>;
  play(): Promise<void>;
  pause(): Promise<void>;
  seek(timeInSeconds: number): Promise<void>;
  destroy(): Promise<void>;
  getPlaybackState(): PlaybackState;
}

export const DEFAULT_SEEK_SECONDS = 10;
```

Create native implementation in `VideoPlayerService.native.ts` (uses react-native-video).
Create Vega implementation in `VideoPlayerService.kepler.ts` (uses Shaka/W3C Media).

## Migration Troubleshooting

### Error: `.plugins[0] must be a string, object, function`

**Cause**: `metro-source-map` version mismatch in monorepo
**Fix**: Add resolution in root `package.json`:
```json
"resolutions": {
  "metro-source-map": "0.80.12"
}
```

### Error: `Super expression must either be null or a function`

**Cause**: Circular dependency in class inheritance due to Metro's platform resolution
**Fix**: Rename base class files from `ClassName.ts` to `ClassName.base.ts`

### Error: `HMRClient.setup() Module has not been registered`

**Cause**: react-native-tvos HMR incompatibility with Expo
**Fix**: Add HMRClient polyfill in `index.js`

### Error: `Cannot find module '@mycompany/shared-ui'`

**Cause**: Metro not configured for monorepo workspace resolution
**Fix**:
1. Add `watchFolders` in metro.config.js
2. Add `extraNodeModules` mapping
3. Run `yarn install` from root

### Warning: `Require cycle: X.ts -> X.ts`

**Cause**: Platform-specific file importing itself due to Metro resolution
**Fix**: Rename base file to use `.base.ts` extension

## Version Compatibility Matrix

| Package | Version | Notes |
|---------|---------|-------|
| expo | ~51.0.0 | Required for TV support |
| react | 18.2.0 | Must match expo requirement |
| react-native-tvos | ~0.74.3-0 | Use instead of react-native |
| metro-source-map | 0.80.12 | Force via resolution |
| react-native-reanimated | ~3.10.1 | For animations |
| @react-native-tvos/config-tv | ^0.0.12 | Expo plugin for TV |
| react-tv-space-navigation | ^3.6.1 | Spatial navigation |
| Java | 17 | Required for Android Gradle |
| Node.js | 18+ | Required for Expo |
| Yarn | 4.x | Berry with workspaces |

---

# Best Practices

## TV-Specific Design

- Always test on actual TV hardware, not just emulators
- Maintain 10-foot UI standards (large text, high contrast)
- Position critical UI within safe zones (48px horizontal, 27px vertical)
- Provide clear focus indicators (borders, scale, highlights)
- Design for remote control first, touch second

## Focus Management

- Set default focus on screen mount
- Restore focus when returning from navigation
- Prevent focus traps (ensure all UI is reachable)
- Test navigation flow with D-pad only
- Handle edge cases (first/last item in grid)

## Performance

- Optimize image sizes for TV resolution (1920x1080)
- Use FlatList for long scrolling lists
- Implement image caching strategy
- Lazy load video content
- Monitor memory usage on low-end devices

## Platform-Specific Code

- Use file extensions for platform variants
- Keep shared logic in base files
- Document platform differences
- Test each platform independently
- Abstract platform APIs behind common interfaces

## Video Player

- Always show buffering state
- Handle network failures gracefully
- Implement playback controls with remote support
- Test with various video formats and codecs
- Support multiple video qualities/bitrates

## Content Loading

- Implement retry logic for failed requests
- Show loading states during fetch
- Cache catalog data locally
- Handle empty states gracefully
- Validate API response structure

---

# Testing

## Unit Tests

- Test business logic in shared-ui package
- Mock platform-specific modules
- Test remote control event handlers
- Validate navigation flows
- Test data transformations

## Integration Tests

- Test cross-platform file resolution
- Validate navigation between screens
- Test video player controls
- Verify focus management
- Test catalog API integration

## Platform Testing

- Test on Android TV emulator and device
- Test on Apple TV simulator and device
- Test on Fire TV device
- Test on web browser with keyboard navigation
- Verify remote control functionality per platform

---

# Troubleshooting

## Metro Bundler Issues

- Clear cache: `yarn start --reset-cache`
- Check for port conflicts (default 8081)
- Verify workspace resolution in metro.config.js

## Platform-Specific Build Failures

- **iOS/tvOS**: Check Node binary path in `.xcode.env.local`
- **Android TV**: Verify Android SDK and emulator setup
- **Vega**: See Vega-specific troubleshooting below

## Vega SDK Issues

### Installation Problems

**'Electron quit unexpectedly' during installation**
- This is expected if VS Code is running during installation
- Restart VS Code after installation completes

**Vega SDK not found / kepler command not available**
- Verify: `kepler --version`
- Check environment variables:
  ```bash
  echo $KEPLER_SDK_PATH
  echo $PATH | grep kepler
  ```
- Add exports to shell config if missing

**Development utilities missing (macOS)**
```bash
brew update && brew install binutils coreutils gawk findutils grep jq lz4 gnu-sed watchman
```

### Build Failures

**npm run build:app fails**
- Ensure dependencies installed: `npm install`
- Check Node.js version: `node --version` (requires 16.x or later)
- Verify package ID format (reverse DNS, no `com.amazon`)
- Check Metro not already running on port 8081

**VPKG file not generated**
- Check build output: `build/<architecture>-<buildType>/`
- Try clean build: `rm -rf build && npm run build:app`

### Runtime Issues

**App crashes on Vega device**
- Check device logs for errors
- Verify VPKG architecture matches device
- Test with debug build first
- Ensure native dependencies compatible with Vega SDK

**Metro bundler connection issues**
- Verify Metro is running: `yarn start`
- Check firewall settings
- Ensure device and dev machine on same network

## Navigation Issues

- Verify React Navigation installation
- Check focus restoration logic
- Test with D-pad/arrow keys only
- Enable spatial navigation debug mode

## Video Playback Issues

- Verify video URL accessibility
- Check video format compatibility (MP4 recommended)
- Test with different video codecs
- Monitor network bandwidth

---

# Additional Resources

## Sample Repositories

**React Native Multi-TV App Sample**
- Repository: https://github.com/AmazonAppDev/react-native-multi-tv-app-sample
- Complete monorepo setup
- Working implementations for all platforms
- Reference for best practices

## Official Documentation

**Expo TV Documentation**
- System requirements and prerequisites
- Quick start with TV templates
- EAS Build profiles for TV
- Platform-specific build instructions

**Vega SDK Documentation**
- Installation guide
- Vega CLI guide
- Device setup
- Deployment to Amazon Appstore

## External Resources

- [React Native TV (react-native-tvos)](https://github.com/react-native-tvos/react-native-tvos)
- [React TV Space Navigation](https://github.com/bamlab/react-tv-space-navigation)
- [Expo Examples - TV](https://github.com/expo/examples/tree/master/with-tv)
- [Expo Examples - TV Router](https://github.com/expo/examples/tree/master/with-router-tv)
- [React Navigation](https://reactnavigation.org/)
- [React Native Directory](https://reactnative.directory/?tvos=true)

---

# Adding New Features

## New Shared Component

1. Create in `packages/shared-ui/src/components/ComponentName.tsx`
2. Export from `packages/shared-ui/src/index.ts`
3. Import in apps: `import { ComponentName } from '@project/shared-ui'`

## Platform-Specific Implementation

1. Create base file: `Feature.base.ts`
2. Create platform files: `Feature.android.ts`, `Feature.ios.ts`, `Feature.kepler.ts`
3. Metro automatically resolves correct file at build time

## New Screen

1. Create in `packages/shared-ui/src/screens/ScreenName.tsx`
2. Add to navigation in `navigation/AppNavigator.tsx`
3. Export from `packages/shared-ui/src/index.ts`
4. Use in app's navigation configuration

---

# Vega App in Monorepo

## Critical Configuration

### 1. Prevent Dependency Hoisting

Add to `apps/vega/package.json`:
```json
{
  "installConfig": {
    "hoistingLimits": "dependencies"
  }
}
```

### 2. Fix Metro Source Map

Create `apps/vega/fix-metro.js`:
```javascript
const fs = require('fs');
const path = require('path');

const metroSourceMapPath = path.join(__dirname, 'node_modules/metro-source-map');
const packageJsonPath = path.join(metroSourceMapPath, 'package.json');

if (!fs.existsSync(packageJsonPath)) {
  console.log('⚠ metro-source-map not found');
  process.exit(0);
}

const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
pkg.exports = {
  ".": "./src/source-map.js",
  "./package.json": "./package.json",
  "./private/*": "./src/*.js",
  "./src/*": "./src/*.js"
};

fs.writeFileSync(packageJsonPath, JSON.stringify(pkg, null, 2));
console.log('✓ Patched metro-source-map exports for Vega');
```

### 3. Add Postinstall Script

In `apps/vega/package.json`:
```json
{
  "scripts": {
    "postinstall": "node fix-metro.js",
    "build:debug": "react-native build-kepler --build-type Debug",
    "build:release": "react-native build-kepler --build-type Release"
  }
}
```

**Note:** Use `build-kepler` command, not `build-vega`.

### 4. Manifest Configuration (CRITICAL)

The `manifest.toml` **MUST** include a `[processes]` section or the app will crash immediately on launch with no error message.

`apps/vega/manifest.toml`:
```toml
schema-version = 1

[package]
title = "My Vega App"
version = "0.1.0"
id = "com.mycompany.myapp"

[components]
[[components.interactive]]
id = "com.mycompany.myapp.main"
runtime-module = "/com.amazon.kepler.keplerscript.runtime.loader_2@IKeplerScript_2_0"
launch-type = "singleton"
categories = ["com.amazon.category.main"]

# CRITICAL: This section is REQUIRED or the app will crash on launch
[processes]
[[processes.group]]
component-ids = ["com.mycompany.myapp.main"]
```

**Common Symptom:** App installs successfully, shows "Successfully launched the app", but immediately crashes (black screen) with no visible error. The fix is adding the `[processes]` section.

### 5. Metro Configuration

`apps/vega/metro.config.js`:
```javascript
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');
const path = require('path');

const config = {
  watchFolders: [
    path.resolve(__dirname, '../../packages/shared-ui'),
  ],
  resolver: {
    unstable_enableSymlinks: true,
    sourceExts: ['kepler.tsx', 'kepler.ts', 'kepler.js', 'tsx', 'ts', 'jsx', 'js', 'json'],
    nodeModulesPaths: [
      path.resolve(__dirname, 'node_modules'),
      path.resolve(__dirname, '../../node_modules'),
    ],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

### 5. Required Dependencies

In `apps/vega/package.json`:
```json
{
  "dependencies": {
    "@amazon-devices/react-native-kepler": "^2.0.0",
    "@babel/runtime": "^7.28.6",
    "react": "18.2.0",
    "react-native": "0.72.0",
    "react-tv-space-navigation": "^6.0.0-beta1"
  },
  "devDependencies": {
    "@amazon-devices/kepler-cli-platform": "^0",
    "@amazon-devices/kepler-module-manifest-builder": "^0.1.0",
    "@react-native/metro-config": "^0.72.6",
    "jest-worker": "^28.0.0"
  }
}
```

### 6. Spatial Navigation with Vega (react-tv-space-navigation)

`react-tv-space-navigation` is compatible with Vega but requires a remote control configuration to map Vega's TVEventHandler to spatial navigation directions.

**Create `packages/shared-ui/src/app/remote-control/SupportedKeys.ts`:**
```typescript
export enum SupportedKeys {
  Up = 'up',
  Down = 'down',
  Left = 'left',
  Right = 'right',
  Enter = 'enter',
  Back = 'back',
  PlayPause = 'playPause',
  Rewind = 'rewind',
  FastForward = 'fastForward',
}
```

**Create `packages/shared-ui/src/app/remote-control/RemoteControlManager.kepler.ts`:**
```typescript
import { SupportedKeys } from './SupportedKeys';

type Listener = (event: SupportedKeys) => void;

const EVENT_TYPE_MAPPING: Record<string, SupportedKeys> = {
  left: SupportedKeys.Left,
  right: SupportedKeys.Right,
  down: SupportedKeys.Down,
  up: SupportedKeys.Up,
  select: SupportedKeys.Enter,
  back: SupportedKeys.Back,
  playpause: SupportedKeys.PlayPause,
  skip_backward: SupportedKeys.Rewind,
  skip_forward: SupportedKeys.FastForward,
};

class RemoteControlManager {
  private listeners: Set<Listener> = new Set();
  private tvEventHandler: any;

  constructor() {
    const { TVEventHandler } = require('react-native');
    this.tvEventHandler = new TVEventHandler();
    this.tvEventHandler.enable(this, this.handleHWEvent);
  }

  private handleHWEvent = (_component: any, event: any): void => {
    if (event.eventKeyAction === 0 || event.eventKeyAction === undefined) {
      const mappedKey = EVENT_TYPE_MAPPING[event.eventType];
      if (mappedKey) {
        this.listeners.forEach(listener => listener(mappedKey));
      }
    }
  };

  addKeydownListener = (listener: Listener) => {
    this.listeners.add(listener);
    return listener;
  };

  removeKeydownListener = (listener: Listener) => {
    this.listeners.delete(listener);
  };
}

export default new RemoteControlManager();
```

**Create `packages/shared-ui/src/app/configureRemoteControl.ts`:**
```typescript
import { Directions, SpatialNavigation } from 'react-tv-space-navigation';
import { SupportedKeys } from './remote-control/SupportedKeys';
import RemoteControlManager from './remote-control/RemoteControlManager';

SpatialNavigation.configureRemoteControl({
  remoteControlSubscriber: (callback) => {
    const mapping: { [key in SupportedKeys]: Directions | null } = {
      [SupportedKeys.Right]: Directions.RIGHT,
      [SupportedKeys.Left]: Directions.LEFT,
      [SupportedKeys.Up]: Directions.UP,
      [SupportedKeys.Down]: Directions.DOWN,
      [SupportedKeys.Enter]: Directions.ENTER,
      [SupportedKeys.Back]: null,
      [SupportedKeys.PlayPause]: null,
      [SupportedKeys.Rewind]: null,
      [SupportedKeys.FastForward]: null,
    };

    const remoteControlListener = (keyEvent: SupportedKeys) => {
      callback(mapping[keyEvent]);
    };

    return RemoteControlManager.addKeydownListener(remoteControlListener);
  },
  remoteControlUnsubscriber: (remoteControlListener) => {
    RemoteControlManager.removeKeydownListener(remoteControlListener);
  },
});
```

**Import in Vega App.tsx:**
```typescript
import '../../../packages/shared-ui/src/app/configureRemoteControl';
```

## Build Commands

```bash
# Install dependencies
yarn install

# Build JS bundle and VPKG (from root)
yarn workspace @your-app/vega run build:debug

# Or from vega directory
cd apps/vega
npm run build:debug

# Build VPKG separately
vega build -t armv7 -b Debug
```

## Why This Works

- **installConfig.hoistingLimits** - Forces Yarn to install dependencies locally instead of hoisting to monorepo root
- **Metro fix** - Patches package.json exports for Node.js 23+ compatibility with strict package exports
- **nodeModulesPaths** - Tells Metro to check local node_modules first, then fall back to root
- **Local dependencies** - `@babel/runtime` and `jest-worker` installed locally prevent monorepo version conflicts
- **kepler-module-manifest-builder** - Required Vega SDK tool for building VPKG

## Common Issues

**App crashes immediately on launch (black screen, no error)**
- Cause: Missing `[processes]` section in `manifest.toml`
- Fix: Add the following to your `manifest.toml`:
  ```toml
  [processes]
  [[processes.group]]
  component-ids = ["com.yourcompany.yourapp.main"]
  ```
- Note: The component-id must match the one defined in `[[components.interactive]]`

**Error: "Package subpath './src/DeltaBundler/Worker' not exported"**
- Cause: jest-worker loading metro from wrong location
- Fix: Install jest-worker locally + run postinstall script

**Error: "Unable to resolve @babel/runtime"**
- Cause: Yarn hoisted @babel/runtime to root
- Fix: Add installConfig.hoistingLimits + install @babel/runtime locally

**Error: "Could not find binary kepler-module-manifest-builder"**
- Cause: Missing Vega SDK tool
- Fix: Install @amazon-devices/kepler-module-manifest-builder

---

# Next Steps

## Recommended Path (Quick Start)

1. **Clone the repository** - `git clone https://github.com/AmazonAppDev/react-native-multi-tv-app-sample.git`
2. **Install dependencies** - `yarn install && yarn bootstrap`
3. **Review the codebase**
4. **Review documentation**
5. **Review steering files**
6. **Configure for Expo TV**
7. **Install Vega SDK** (optional)
8. **Test on platforms**
9. **Customize for your project**
10. **Deploy**

## Alternative Path (Build from Scratch)

Follow the step-by-step "Build from Scratch" guide above to understand:
- Monorepo setup with Yarn workspaces
- Expo TV configuration
- Vega SDK integration
- Shared component library architecture
- Platform-specific file resolution
- Theme system implementation
- Spatial navigation setup
- Remote control integration

---

**For detailed implementation guides, see:**
- `multi-tv-builder/POWER.md` - Complete implementation guide
- `multi-tv-builder/steering/product.md` - Product overview
- `multi-tv-builder/steering/structure.md` - Project structure details
- `multi-tv-builder/steering/tech.md` - Technology stack reference
- `multi-tv-builder/steering/VEGA_TO_MONOREPO_MIGRATION_GUIDE.md` - Migration guide


---

# Android TV / Fire TV Troubleshooting

## Common Runtime Errors

### TypeError: Cannot read property 'displayName' of undefined

**Symptoms:**
- App builds successfully but crashes immediately on launch
- Metro shows: `ERROR TypeError: Cannot read property 'displayName' of undefined, js engine: hermes`
- App returns to launcher after brief flash

**Common Causes & Fixes:**

1. **Wrong import in index.js** (Most Common)
   ```javascript
   // ❌ WRONG - Named import when App uses default export
   import { App } from './App';
   
   // ✅ CORRECT - Default import
   import App from './App';
   ```

2. **Metro cache corruption**
   ```bash
   # Clear all caches
   pkill -f "expo" 2>/dev/null || true
   pkill -f "metro" 2>/dev/null || true
   rm -rf node_modules/.cache
   rm -rf /tmp/metro-*
   rm -rf /tmp/haste-map-*
   npx expo start --clear
   ```

3. **react-tv-space-navigation v6 missing configuration**
   - v6 requires explicit remote control configuration
   - Create `src/configureRemoteControl.ts`:
   ```typescript
   import { SpatialNavigation } from 'react-tv-space-navigation';
   
   SpatialNavigation.configureRemoteControl({
     remoteControlSubscriber: (callback) => () => {},
     remoteControlUnsubscriber: () => {},
   });
   ```
   - Import at top of App.tsx: `import './src/configureRemoteControl';`

### App Launches But Shows Black Screen / Returns to Launcher

**Diagnostic Steps:**

1. **Check if app process is running:**
   ```bash
   adb shell "ps -A | grep <package_name>"
   ```

2. **Check Metro bundler connection:**
   ```bash
   # Verify Metro is running
   curl -s http://localhost:8081/status
   
   # Set up ADB reverse port forwarding
   adb reverse tcp:8081 tcp:8081
   ```

3. **Check device logs for JS errors:**
   ```bash
   adb logcat -d | grep -iE "(ReactNativeJS|ERROR|TypeError)" | tail -30
   ```

4. **Verify bundle is loading:**
   ```bash
   adb logcat -d | grep -i "bundled" | tail -5
   ```

### Metro Bundler Connection Issues

**Symptoms:**
- `Couldn't connect to "ws://localhost:8081/message..."`
- App shows loading screen indefinitely
- `ReactInstanceManager: Instance detached from instance manager`

**Fixes:**

1. **Set up ADB reverse port forwarding:**
   ```bash
   adb reverse tcp:8081 tcp:8081
   ```

2. **Verify emulator is connected:**
   ```bash
   adb devices -l
   ```

3. **Restart ADB if stale:**
   ```bash
   adb kill-server && adb start-server
   ```

4. **Use correct Metro start command:**
   ```bash
   # For development builds (not Expo Go)
   npx expo start --dev-client --clear
   
   # Or run directly
   npx expo run:android
   ```

## Android TV Emulator Setup

### Starting the Emulator

```bash
# List available emulators
emulator -list-avds

# Start Android TV emulator (cold boot recommended for stability)
emulator -avd Android_TV_720p -no-snapshot-load -gpu swiftshader_indirect &

# Wait for boot and verify
adb wait-for-device
adb devices -l
```

### Emulator Not Responding

```bash
# Kill stale processes
pkill -9 qemu-system 2>/dev/null || true
pkill -9 emulator 2>/dev/null || true
adb kill-server
sleep 1
adb start-server

# Start fresh
emulator -avd Android_TV_720p -no-snapshot-load &
```

### Fire TV Emulator Specific Issues

The Fire TV emulator (Android_TV_720p with Fire OS) may show system errors in logs like:
- `NEO_DIAL_SVC: DIAL_register_app error allocating memory`
- `libc++abi: terminating with uncaught exception`

**These are system service errors unrelated to your app** - ignore them and focus on `ReactNativeJS` or your package name in logs.

## Build & Launch Commands

### Quick Launch Sequence

```bash
# 1. Ensure emulator is running
adb devices

# 2. Set up port forwarding
adb reverse tcp:8081 tcp:8081

# 3. Build and run (from app directory)
cd apps/expo-multi-tv
yarn android
# or: npx expo run:android

# 4. If app crashes, force restart
adb shell am force-stop <package_name>
adb shell am start -n <package_name>/.MainActivity
```

### Debugging Workflow

```bash
# Clear logs before launch
adb logcat -c

# Launch app
adb shell am start -n com.example.app/.MainActivity

# Wait and capture logs
sleep 5
adb logcat -d | grep -iE "(ReactNativeJS|error|exception)" | tail -50
```

## Expo Go vs Development Builds

**Important:** TV apps should use **development builds**, not Expo Go.

- Expo Go has SDK version mismatches on TV emulators
- Use `npx expo run:android` or `npx expo start --dev-client`
- If prompted about Expo Go version, choose development build instead

```bash
# ❌ May cause issues on TV
npx expo start

# ✅ Correct for TV development
npx expo run:android
# or
npx expo start --dev-client
```


## Vega Virtual Device Notes

### `is-app-running` Command May Report False Negatives

The command `vega device is-app-running --appName <package>` may incorrectly report that an app is not running even when it's visible and functioning on the virtual device.

**Workaround:** Visually verify the app is running in the virtual device window rather than relying on the CLI command.

```bash
# This may report "not running" even when app is visible
vega device is-app-running --appName com.example.app

# Instead, just launch and visually verify
vega run-app <vpkg-path> <package-id>
# Check the virtual device window
```


---

# Monorepo React Version Conflict Resolution

## Problem: Expo + Vega in Same Monorepo

When running Expo (React 19) and Vega (React 18) apps in the same Yarn workspace, Metro bundles the wrong React version causing runtime crashes:

```
TypeError: Cannot read property 'ReactCurrentOwner' of undefined
TypeError: Cannot read property 'render' of undefined
```

### Root Cause

Yarn hoists dependencies to the workspace root. When Metro bundles the Vega app, it finds React 19 in the root `node_modules/` before finding React 18 in `apps/vega/node_modules/`.

### Solution: Move Root React Packages

Before running the Vega app, move the root React packages out of the way:

```bash
cd <workspace-root>
mv node_modules/react node_modules/react.bak
mv node_modules/react-native node_modules/react-native.bak
```

This forces Metro to use Vega's local React 18.2.0.

**Note:** After running `yarn install`, you'll need to move these packages again.

### Alternative Solutions

1. **Separate repositories** - Keep Expo and Vega apps in different repos
2. **Publish shared-ui** - Publish as npm package instead of workspace dependency
3. **Use consistent React versions** - Not always possible due to SDK requirements

---

# Node.js 23 Compatibility Issues

## Problem: Metro Package Exports

Node.js 23 enforces strict package exports. Metro packages don't export internal paths, causing errors:

```
Package subpath './src/Consumer/search' is not defined by "exports"
Package subpath './src/DeltaBundler/Worker' is not defined by "exports"
```

### Solution: Remove Exports Field

Create a script to remove the `exports` field from metro packages:

```javascript
// fix-metro-exports.js
const fs = require('fs');
const path = require('path');

const packages = [
  'node_modules/metro',
  'node_modules/metro-source-map',
  'node_modules/metro-transform-worker',
  'node_modules/metro-runtime',
];

packages.forEach(pkgPath => {
  const packageJsonPath = path.join(pkgPath, 'package.json');
  if (!fs.existsSync(packageJsonPath)) return;
  
  const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  delete pkg.exports;
  fs.writeFileSync(packageJsonPath, JSON.stringify(pkg, null, 2));
  console.log(`✓ Removed exports from ${path.basename(pkgPath)}`);
});
```

Run after `yarn install`:
```bash
node fix-metro-exports.js
```

### Best Practice

Add to `package.json` scripts:
```json
{
  "scripts": {
    "postinstall": "node fix-metro-exports.js"
  }
}
```

---

# Vega Development Workflow (Complete)

## Prerequisites

1. Vega SDK installed
2. Vega virtual device running: `vega virtual-device start`
3. Metro packages patched for Node 23 (if using Node 23)
4. Root React moved (if in Expo+Vega monorepo)

## Step-by-Step

### 1. Patch Metro (Node 23 only)
```bash
node fix-metro-exports.js
```

### 2. Move Root React (Monorepo only)
```bash
mv node_modules/react node_modules/react.bak
mv node_modules/react-native node_modules/react-native.bak
```

### 3. Start Metro
```bash
cd apps/vega
npm start
```

### 4. Set Up Port Forwarding
```bash
vega device start-port-forwarding --port 8081 --forward false
```

### 5. Launch App
```bash
vega device launch-app --appName <package-id>
```

### 6. Verify
```bash
vega device running-apps | grep <app-name>
```

## Troubleshooting Checklist

| Issue | Check | Fix |
|-------|-------|-----|
| Black screen | Metro running? | `npm start` in apps/vega |
| Black screen | Port forwarding? | `vega device start-port-forwarding --port 8081 --forward false` |
| ReactCurrentOwner error | Root React moved? | `mv node_modules/react node_modules/react.bak` |
| Package exports error | Metro patched? | Run `fix-metro-exports.js` |
| App not in running-apps | May be false negative | Visually verify in virtual device |

---

# Required Dependencies for Vega in Monorepo

When using Vega in a Yarn workspace, ensure these dependencies are installed locally in the Vega app:

```bash
cd apps/vega
npm install @babel/runtime --save
```

The `@babel/runtime` package is required for Babel transforms but may not be hoisted correctly in monorepos.
