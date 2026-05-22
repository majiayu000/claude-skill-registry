---
name: metro-bundler
description: Metro bundler configuration, optimization, and troubleshooting. Use for bundle errors, "unable to resolve module", or caching issues.
---

# Metro Bundler Expert

Comprehensive expertise in React Native's Metro bundler, including configuration, optimization, custom transformers, caching strategies, and troubleshooting common bundling issues.

## What I Know

### Metro Fundamentals

**What is Metro?**
- JavaScript bundler for React Native
- Transforms and bundles JavaScript modules
- Handles assets (images, fonts, etc.)
- Provides fast refresh for development
- Generates source maps for debugging

**Key Concepts**
- **Transformer**: Converts source code (TypeScript, JSX) to JavaScript
- **Resolver**: Locates modules in the file system
- **Serializer**: Combines modules into bundles
- **Cache**: Speeds up subsequent builds

### Metro Configuration

**Basic metro.config.js**
```javascript
const { getDefaultConfig } = require('expo/metro-config');

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

module.exports = config;
```

**Custom Configuration**
```javascript
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const defaultConfig = getDefaultConfig(__dirname);

const config = {
  transformer: {
    // Enable Babel transformer
    babelTransformerPath: require.resolve('react-native-svg-transformer'),

    // Source map options
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
  },

  resolver: {
    // Custom asset extensions
    assetExts: defaultConfig.resolver.assetExts.filter(ext => ext !== 'svg'),

    // Custom source extensions
    sourceExts: [...defaultConfig.resolver.sourceExts, 'svg', 'cjs'],

    // Node module resolution
    nodeModulesPaths: [
      './node_modules',
      '../../node_modules',  // For monorepos
    ],

    // Custom platform-specific extensions
    platforms: ['ios', 'android', 'native'],
  },

  server: {
    // Custom port
    port: 8081,

    // Enhanced logging
    enhanceMiddleware: (middleware) => {
      return (req, res, next) => {
        console.log(`Metro request: ${req.url}`);
        return middleware(req, res, next);
      };
    },
  },

  watchFolders: [
    // Watch external folders (monorepos)
    path.resolve(__dirname, '..', 'shared-library'),
  ],

  resetCache: true,  // Reset cache on start (dev only)
};

module.exports = mergeConfig(defaultConfig, config);
```

### Optimization Strategies

**Inline Requires**
```javascript
// metro.config.js
module.exports = {
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        inlineRequires: true,  // Lazy load modules (faster startup)
      },
    }),
  },
};

// Before (eager loading)
import UserProfile from './UserProfile';
import Settings from './Settings';

function App() {
  return (
    <View>
      {showProfile ? <UserProfile /> : <Settings />}
    </View>
  );
}

// After inline requires (lazy loading)
function App() {
  return (
    <View>
      {showProfile ?
        <require('./UserProfile').default /> :
        <require('./Settings').default />
      }
    </View>
  );
}
```

**Bundle Splitting (Experimental)**
```javascript
// metro.config.js
module.exports = {
  serializer: {
    createModuleIdFactory: () => {
      // Generate stable module IDs for better caching
      return (path) => {
        return require('crypto')
          .createHash('sha1')
          .update(path)
          .digest('hex')
          .substring(0, 8);
      };
    },
  },
};
```

**Asset Optimization**
```javascript
// metro.config.js
module.exports = {
  transformer: {
    // Minify assets
    minifierPath: require.resolve('metro-minify-terser'),
    minifierConfig: {
      compress: {
        drop_console: true,  // Remove console.log in production
        drop_debugger: true,
      },
      output: {
        comments: false,
      },
    },
  },

  resolver: {
    // Optimize asset resolution
    assetExts: [
      'png', 'jpg', 'jpeg', 'gif', 'webp',  // Images
      'mp3', 'wav', 'm4a', 'aac',           // Audio
      'mp4', 'mov',                          // Video
      'ttf', 'otf', 'woff', 'woff2',        // Fonts
    ],
  },
};
```

### Custom Transformers

**SVG Transformer**
```bash
# Install
npm install react-native-svg react-native-svg-transformer

# metro.config.js
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

config.transformer = {
  ...config.transformer,
  babelTransformerPath: require.resolve('react-native-svg-transformer'),
};

config.resolver = {
  ...config.resolver,
  assetExts: config.resolver.assetExts.filter(ext => ext !== 'svg'),
  sourceExts: [...config.resolver.sourceExts, 'svg'],
};

module.exports = config;
```

```javascript
// Usage in code
import Logo from './assets/logo.svg';

function App() {
  return <Logo width={120} height={40} />;
}
```

**Multiple File Extensions**
```javascript
// metro.config.js
module.exports = {
  resolver: {
    // Add .web.js, .native.js for platform-specific code
    sourceExts: ['js', 'json', 'ts', 'tsx', 'jsx', 'web.js', 'native.js'],

    // Custom resolution logic
    resolveRequest: (context, moduleName, platform) => {
      if (moduleName === 'my-module') {
        // Custom module resolution
        return {
          filePath: '/custom/path/to/module.js',
          type: 'sourceFile',
        };
      }

      return context.resolveRequest(context, moduleName, platform);
    },
  },
};
```

### Caching Strategies

**Cache Management**
```bash
# Clear Metro cache
npx react-native start --reset-cache
npm start -- --reset-cache  # Expo

# Or manually
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*

# Clear watchman cache
watchman watch-del-all

# Clear all caches (nuclear option)
npm run clear  # If configured in package.json
```

**Cache Configuration**
```javascript
// metro.config.js
const path = require('path');

module.exports = {
  cacheStores: [
    // Custom cache directory
    {
      get: (key) => {
        const cachePath = path.join(__dirname, '.metro-cache', key);
        // Implement custom cache retrieval
      },
      set: (key, value) => {
        const cachePath = path.join(__dirname, '.metro-cache', key);
        // Implement custom cache storage
      },
    },
  ],

  // Reset cache on config changes
  resetCache: process.env.RESET_CACHE === 'true',
};
```

### Monorepo Setup

**Workspaces Configuration**
```javascript
// metro.config.js (in app directory)
const path = require('path');
const { getDefaultConfig } = require('@react-native/metro-config');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);

// Watch workspace directories
config.watchFolders = [workspaceRoot];

// Resolve modules from workspace
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

// Avoid hoisting issues
config.resolver.disableHierarchicalLookup = false;

module.exports = config;
```

**Symlink Handling**
```javascript
// metro.config.js
module.exports = {
  resolver: {
    // Enable symlink support
    unstable_enableSymlinks: true,

    // Resolve symlinked packages
    resolveRequest: (context, moduleName, platform) => {
      const resolution = context.resolveRequest(context, moduleName, platform);

      if (resolution && resolution.type === 'sourceFile') {
        // Resolve real path for symlinks
        const realPath = require('fs').realpathSync(resolution.filePath);
        return {
          ...resolution,
          filePath: realPath,
        };
      }

      return resolution;
    },
  },
};
```

### Common Issues & Solutions

**"Unable to resolve module"**
```bash
# Solution 1: Clear cache
npx react-native start --reset-cache

# Solution 2: Reinstall dependencies
rm -rf node_modules
npm install

# Solution 3: Check import paths
# Ensure case-sensitive imports match file names
import UserProfile from './userProfile';  # ❌ Wrong case
import UserProfile from './UserProfile';  # ✅ Correct

# Solution 4: Add to metro.config.js
module.exports = {
  resolver: {
    extraNodeModules: {
      'my-module': path.resolve(__dirname, 'node_modules/my-module'),
    },
  },
};
```

**"Port 8081 already in use"**
```bash
# Find and kill process
lsof -ti:8081 | xargs kill -9

# Or start on different port
npx react-native start --port 8082

# Update code to use new port
adb reverse tcp:8082 tcp:8082  # Android
```

**"Invariant Violation: Module AppRegistry is not a registered callable module"**
```bash
# Clear all caches
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*
watchman watch-del-all
rm -rf node_modules
npm install
npx react-native start --reset-cache
```

**"TransformError: ... SyntaxError"**
```javascript
// Add Babel plugin to metro.config.js
module.exports = {
  transformer: {
    babelTransformerPath: require.resolve('./customBabelTransformer.js'),
  },
};

// customBabelTransformer.js
module.exports = require('metro-react-native-babel-preset');
```

## When to Use This Skill

Ask me when you need help with:
- Configuring Metro bundler
- Custom transformers (SVG, images, etc.)
- Optimizing bundle size and startup time
- Setting up monorepo with Metro
- Troubleshooting "Unable to resolve module" errors
- Clearing Metro cache effectively
- Configuring source maps
- Platform-specific file resolution
- Debugging bundling performance
- Custom asset handling
- Port conflicts (8081)
- Symlink resolution in monorepos

## Essential Commands

### Development
```bash
# Start Metro bundler
npx react-native start

# Start with cache cleared
npx react-native start --reset-cache

# Start with custom port
npx react-native start --port 8082

# Start with verbose logging
npx react-native start --verbose

# Expo dev server
npx expo start

# Expo with cache cleared
npx expo start -c
```

### Debugging
```bash
# Check Metro status
curl http://localhost:8081/status

# Get bundle (for debugging)
curl http://localhost:8081/index.bundle?platform=ios > bundle.js

# Check source map
curl http://localhost:8081/index.map?platform=ios > bundle.map

# List all modules in bundle
curl http://localhost:8081/index.bundle?platform=ios&dev=false&minify=false
```

### Cache Management
```bash
# Clear Metro cache
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*

# Clear watchman
watchman watch-del-all

# Clear all (comprehensive)
npm run clear  # Custom script
# Or manually:
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*
watchman watch-del-all
rm -rf node_modules
npm install
```

## Pro Tips & Tricks

### 1. Bundle Analysis

Analyze bundle size to find optimization opportunities:

```bash
# Generate bundle with source map
npx react-native bundle \
  --platform ios \
  --dev false \
  --entry-file index.js \
  --bundle-output ./bundle.js \
  --sourcemap-output ./bundle.map

# Analyze with source-map-explorer
npm install -g source-map-explorer
source-map-explorer bundle.js bundle.map
```

### 2. Environment-Specific Configuration

```javascript
// metro.config.js
const isDev = process.env.NODE_ENV !== 'production';

module.exports = {
  transformer: {
    minifierConfig: {
      compress: {
        drop_console: !isDev,  // Remove console.log in production
      },
    },
  },

  serializer: {
    getModulesRunBeforeMainModule: () => [
      // Polyfills for production
      ...(!isDev ? [require.resolve('./polyfills.js')] : []),
    ],
  },
};
```

### 3. Custom Asset Pipeline

```javascript
// metro.config.js
module.exports = {
  transformer: {
    // Optimize images during bundling
    assetPlugins: ['expo-asset/tools/hashAssetFiles'],
  },

  resolver: {
    assetExts: ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'],

    // Custom asset resolution
    resolveAsset: (dirPath, assetName, extension) => {
      const basePath = `${dirPath}/${assetName}`;

      // Try @2x, @3x variants
      const variants = ['@3x', '@2x', ''];
      for (const variant of variants) {
        const path = `${basePath}${variant}.${extension}`;
        if (require('fs').existsSync(path)) {
          return path;
        }
      }

      return null;
    },
  },
};
```

### 4. Preloading Heavy Modules

```javascript
// index.js
import { AppRegistry } from 'react-native';
import App from './App';

// Preload heavy modules
import('./src/heavyModule').then(() => {
  console.log('Heavy module preloaded');
});

AppRegistry.registerComponent('MyApp', () => App);
```

### 5. Development Performance Boost

```javascript
// metro.config.js
const isDev = process.env.NODE_ENV !== 'production';

module.exports = {
  transformer: {
    // Skip minification in dev
    minifierPath: isDev ? undefined : require.resolve('metro-minify-terser'),

    // Faster source maps in dev
    getTransformOptions: async () => ({
      transform: {
        inlineRequires: !isDev,  // Only in production
      },
    }),
  },

  server: {
    // Increase file watching performance
    watchFolders: isDev ? [] : undefined,
  },
};
```

## Integration with SpecWeave

**Configuration Management**
- Document Metro configuration in `docs/internal/architecture/`
- Track bundle size across increments
- Include bundling optimization in `tasks.md`

**Performance Monitoring**
- Set bundle size thresholds
- Track startup time improvements
- Document optimization strategies

**Troubleshooting**
- Maintain runbook for common Metro issues
- Document cache clearing procedures
- Track bundling errors in increment reports
