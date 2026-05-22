---
name: Mobile App Distribution and Deployment
description: Submitting, testing, and releasing mobile apps to app stores including App Store and Google Play submission, beta testing, OTA updates, and release management.
---

# Mobile App Distribution and Deployment

> **Current Level:** Intermediate  
> **Domain:** Mobile Development / DevOps

---

## Overview

App distribution covers the process of submitting, testing, and releasing mobile apps to app stores. This guide covers App Store and Google Play submission, beta testing, OTA updates, and release management for successful app launches and updates.

---

## Core Concepts

### Table of Contents

1. [App Store Submission](#app-store-submission)
2. [App Metadata](#app-metadata)
3. [Screenshots and Previews](#screenshots-and-previews)
4. [App Store Optimization (ASO)](#app-store-optimization-aso)
5. [Beta Testing](#beta-testing)
6. [OTA Updates](#ota-updates)
7. [Release Management](#release-management)
8. [Versioning Strategy](#versioning-strategy)
9. [Staged Rollout](#staged-rollout)
10. [Best Practices](#best-practices)

---

## App Store Submission

### iOS App Store Submission

```typescript
// Fastlane configuration for iOS
// fastlane/Fastfile

platform :ios do
  desc "Submit to TestFlight"
  lane :testflight do
    increment_build_number

    match(
      type: "appstore",
      readonly: true
    )

    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )

    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      changelog: "Bug fixes and improvements"
    )
  end

  desc "Submit to App Store"
  lane :release do
    increment_build_number

    match(
      type: "appstore",
      readonly: true
    )

    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )

    upload_to_app_store(
      submit_for_review: true,
      automatic_release: false,
      force: true,
      submission_information: {
        add_id_info_uses_idfa: false
      },
      app_rating_config_path: "./fastlane/metadata/app_rating_config.json"
    )
  end
end
```

### Google Play Store Submission

```ruby
# fastlane/Fastfile

platform :android do
  desc "Submit to Google Play Internal Testing"
  lane :internal do
    gradle(
      task: "assemble",
      build_type: "Release",
      project_dir: "android/"
    )

    upload_to_play_store(
      track: "internal",
      aab: "./android/app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: false,
      skip_upload_images: false,
      skip_upload_screenshots: false,
      skip_upload_changelogs: false
    )
  end

  desc "Submit to Google Play Production"
  lane :release do
    gradle(
      task: "bundle",
      build_type: "Release",
      project_dir: "android/"
    )

    upload_to_play_store(
      track: "production",
      aab: "./android/app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: false,
      skip_upload_images: false,
      skip_upload_screenshots: false,
      skip_upload_changelogs: false,
      release_status: "completed",
      rollout: "0.1" # 10% staged rollout
    )
  end
end
```

---

## App Metadata

### iOS App Metadata

```json
// fastlane/metadata/en-US/whats_new.txt
- Bug fixes and performance improvements
- New feature: Dark mode support
- Improved user experience

// fastlane/metadata/en-US/description.txt
MyApp is the best app for managing your daily tasks. With intuitive design and powerful features, you can stay organized and productive.

Features:
- Create and manage tasks
- Set reminders and notifications
- Sync across devices
- Beautiful dark mode
- Customizable themes

// fastlane/metadata/en-US/keywords.txt
task,manager,productivity,organize,reminders

// fastlane/metadata/en-US/name.txt
MyApp

// fastlane/metadata/en-US/short_description.txt
The best task manager app
```

### Android App Metadata

```xml
<!-- android/app/src/main/res/values/strings.xml -->
<resources>
  <string name="app_name">MyApp</string>
  <string name="app_description">The best task manager app for staying organized and productive.</string>
  <string name="app_short_desc">Manage your tasks efficiently</string>
</resources>
```

---

## Screenshots and Previews

### iOS Screenshots

```ruby
# fastlane/Fastfile

desc "Generate screenshots"
lane :screenshots do
  capture_screenshots(
    scheme: "MyApp",
    devices: [
      "iPhone 14 Pro Max",
      "iPhone 14 Pro",
      "iPhone 14",
      "iPad Pro (12.9-inch) (6th generation)"
    ],
    languages: ["en-US", "es-ES", "fr-FR"],
    clear_previous_screenshots: true
  )

  frame_screenshots(
    white: true
  )
end
```

### Android Screenshots

```ruby
# fastlane/Fastfile

desc "Generate Android screenshots"
lane :android_screenshots do
  capture_android_screenshots(
    locales: ["en-US", "es-ES", "fr-FR"],
    clear_previous_screenshots: true
  )
end
```

---

## App Store Optimization (ASO)

### ASO Checklist

```typescript
// ASO Configuration
interface ASOConfig {
  title: string;
  subtitle: string;
  keywords: string[];
  description: string;
  promotionalText: string;
  screenshots: string[];
  previewVideo?: string;
}

const asoConfig: ASOConfig = {
  title: "MyApp - Task Manager",
  subtitle: "Organize your life",
  keywords: [
    "task",
    "manager",
    "productivity",
    "organize",
    "reminders",
    "to-do",
    "planner",
    "schedule"
  ],
  description: `
    MyApp is the best app for managing your daily tasks. With intuitive design and powerful features, you can stay organized and productive.

    Features:
    - Create and manage tasks
    - Set reminders and notifications
    - Sync across devices
    - Beautiful dark mode
    - Customizable themes
    - Priority levels
    - Due dates
    - Categories and tags
    - Search and filter
    - Export and share

    Download MyApp today and take control of your tasks!
  `,
  promotionalText: "New: Dark mode support!",
  screenshots: [
    "screenshots/iphone-1.png",
    "screenshots/iphone-2.png",
    "screenshots/iphone-3.png",
    "screenshots/iphone-4.png",
    "screenshots/iphone-5.png",
    "screenshots/iphone-6.png",
  ],
  previewVideo: "videos/app-preview.mp4",
};
```

### ASO Best Practices

```typescript
// ASO Analyzer
class ASOAnalyzer {
  /**
   * Analyze ASO score
   */
  analyzeASO(config: ASOConfig): {
    score: number;
    suggestions: string[];
  } {
    const suggestions: string[] = [];
    let score = 0;

    // Title analysis
    if (config.title.length >= 10 && config.title.length <= 30) {
      score += 20;
    } else {
      suggestions.push("Title should be between 10-30 characters");
    }

    // Subtitle analysis
    if (config.subtitle.length >= 10 && config.subtitle.length <= 30) {
      score += 20;
    } else {
      suggestions.push("Subtitle should be between 10-30 characters");
    }

    // Keywords analysis
    if (config.keywords.length >= 5 && config.keywords.length <= 10) {
      score += 20;
    } else {
      suggestions.push("Use 5-10 relevant keywords");
    }

    // Description analysis
    if (config.description.length >= 100 && config.description.length <= 4000) {
      score += 20;
    } else {
      suggestions.push("Description should be between 100-4000 characters");
    }

    // Screenshots analysis
    if (config.screenshots.length >= 5 && config.screenshots.length <= 10) {
      score += 20;
    } else {
      suggestions.push("Include 5-10 screenshots");
    }

    return { score, suggestions };
  }

  /**
   * Generate keywords
   */
  generateKeywords(description: string): string[] {
    const words = description
      .toLowerCase()
      .replace(/[^\w\s]/g, '')
      .split(/\s+/);

    const stopWords = new Set([
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
      'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through',
      'during', 'before', 'after', 'above', 'below', 'between', 'under',
      'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
      'why', 'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some',
      'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
      'too', 'very', 'can', 'will', 'just', 'should', 'now'
    ]);

    const wordCount = new Map<string, number>();

    for (const word of words) {
      if (!stopWords.has(word) && word.length > 2) {
        wordCount.set(word, (wordCount.get(word) || 0) + 1);
      }
    }

    return Array.from(wordCount.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);
  }
}
```

---

## Beta Testing

### TestFlight Setup

```ruby
# fastlane/Fastfile

desc "Add beta testers"
lane :add_testers do
  testflight(
    api_key_path: "./fastlane/api_key.json",
    skip_waiting_for_build_processing: true,
    changelog: "Bug fixes and improvements",
    groups: ["Internal Testers", "External Testers"],
    distribute_external: true,
    notify_external_testers: true
  )
end

desc "Add tester"
lane :add_tester do
  testflight_add_tester(
    email: "tester@example.com",
    first_name: "John",
    last_name: "Doe",
    groups: ["External Testers"]
  )
end
```

### Google Play Internal Testing

```ruby
# fastlane/Fastfile

desc "Add internal testers"
lane :add_internal_testers do
  upload_to_play_store(
    track: "internal",
    aab: "./android/app/build/outputs/bundle/release/app-release.aab",
    skip_upload_metadata: true,
    skip_upload_images: true,
    skip_upload_screenshots: true,
    skip_upload_changelogs: true
  )
end

desc "Add closed testers"
lane :add_closed_testers do
  upload_to_play_store(
    track: "beta",
    aab: "./android/app/build/outputs/bundle/release/app-release.aab",
    skip_upload_metadata: false,
    skip_upload_images: false,
    skip_upload_screenshots: false,
    skip_upload_changelogs: false
  )
end
```

---

## OTA Updates

### CodePush Integration

```typescript
// npm install react-native-code-push

import CodePush from 'react-native-code-push';

// Wrap your root component
const App = () => {
  return (
    <YourApp />
  );
};

// Configure CodePush
const codePushOptions = {
  checkFrequency: CodePush.CheckFrequency.ON_APP_RESUME,
  installMode: CodePush.InstallMode.IMMEDIATE,
  updateDialog: {
    appendReleaseDescription: true,
    descriptionPrefix: "\n\nChange log:\n",
    title: 'A new update is available!',
    mandatoryUpdateMessage: 'A mandatory update is available.',
    optionalIgnoreButtonLabel: 'Later',
    optionalInstallButtonLabel: 'Install',
    optionalUpdateMessage: 'An update is available. Would you like to install it?',
    mandatoryContinueButtonLabel: 'Continue',
  },
};

export default CodePush(codePushOptions)(App);
```

### Expo Updates

```typescript
// app.json
{
  "expo": {
    "updates": {
      "url": "https://u.expo.dev/YOUR_PROJECT_ID"
    },
    "runtimeVersion": {
      "policy": "appVersion"
    }
  }
}

// app.config.ts
import { ExpoConfig, ConfigContext } from '@expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  updates: {
    url: 'https://u.expo.dev/YOUR_PROJECT_ID',
  },
  runtimeVersion: {
    policy: 'appVersion',
  },
});
```

---

## Release Management

### Release Workflow

```typescript
// Release Manager
class ReleaseManager {
  /**
   * Create release
   */
  async createRelease(params: {
    version: string;
    buildNumber: number;
    platform: 'ios' | 'android';
    environment: 'testflight' | 'beta' | 'production';
    changelog: string;
  }): Promise<void> {
    // 1. Increment version
    await this.incrementVersion(params.version, params.buildNumber);

    // 2. Build app
    await this.buildApp(params.platform, params.environment);

    // 3. Upload to store
    await this.uploadToStore(params.platform, params.environment, params.changelog);

    // 4. Create release notes
    await this.createReleaseNotes(params.version, params.changelog);
  }

  /**
   * Increment version
   */
  private async incrementVersion(
    version: string,
    buildNumber: number
  ): Promise<void> {
    // Update version in package.json
    const packageJson = await fs.readJson('package.json');
    packageJson.version = version;

    await fs.writeJson('package.json', packageJson, { spaces: 2 });

    // Update iOS version
    if (Platform.OS === 'ios') {
      const plistPath = 'ios/MyApp/Info.plist';
      const plist = await fs.readXml(plistPath);
      plist.plist.dict[0].string[1] = version; // CFBundleShortVersionString
      plist.plist.dict[0].integer[0] = buildNumber; // CFBundleVersion
      await fs.writeXml(plistPath, plist);
    }

    // Update Android version
    if (Platform.OS === 'android') {
      const gradlePath = 'android/app/build.gradle';
      let gradle = await fs.readFile(gradlePath, 'utf-8');

      gradle = gradle.replace(
        /versionName ".*"/,
        `versionName "${version}"`
      );
      gradle = gradle.replace(
        /versionCode \d+/,
        `versionCode ${buildNumber}`
      );

      await fs.writeFile(gradlePath, gradle);
    }
  }

  /**
   * Build app
   */
  private async buildApp(
    platform: 'ios' | 'android',
    environment: 'testflight' | 'beta' | 'production'
  ): Promise<void> {
    if (platform === 'ios') {
      await exec('fastlane ios build');
    } else {
      await exec('fastlane android build');
    }
  }

  /**
   * Upload to store
   */
  private async uploadToStore(
    platform: 'ios' | 'android',
    environment: 'testflight' | 'beta' | 'production',
    changelog: string
  ): Promise<void> {
    if (platform === 'ios') {
      if (environment === 'testflight') {
        await exec('fastlane ios testflight');
      } else {
        await exec('fastlane ios release');
      }
    } else {
      if (environment === 'beta') {
        await exec('fastlane android internal');
      } else {
        await exec('fastlane android release');
      }
    }
  }

  /**
   * Create release notes
   */
  private async createReleaseNotes(
    version: string,
    changelog: string
  ): Promise<void> {
    const releaseNotes = `
# Release ${version}

## Changes
${changelog}

## Date
${new Date().toISOString()}
    `;

    await fs.writeFile(`RELEASE_NOTES/${version}.md`, releaseNotes);
  }
}
```

---

## Versioning Strategy

### Semantic Versioning

```typescript
// Version Manager
class VersionManager {
  /**
   * Bump version
   */
  bumpVersion(
    currentVersion: string,
    type: 'major' | 'minor' | 'patch'
  ): string {
    const [major, minor, patch] = currentVersion.split('.').map(Number);

    switch (type) {
      case 'major':
        return `${major + 1}.0.0`;
      case 'minor':
        return `${major}.${minor + 1}.0`;
      case 'patch':
        return `${major}.${minor}.${patch + 1}`;
      default:
        return currentVersion;
    }
  }

  /**
   * Get next version
   */
  getNextVersion(
    currentVersion: string,
    changes: {
      breaking: number;
      features: number;
      fixes: number;
    }
  ): string {
    if (changes.breaking > 0) {
      return this.bumpVersion(currentVersion, 'major');
    } else if (changes.features > 0) {
      return this.bumpVersion(currentVersion, 'minor');
    } else if (changes.fixes > 0) {
      return this.bumpVersion(currentVersion, 'patch');
    }

    return currentVersion;
  }

  /**
   * Compare versions
   */
  compareVersions(v1: string, v2: string): number {
    const [major1, minor1, patch1] = v1.split('.').map(Number);
    const [major2, minor2, patch2] = v2.split('.').map(Number);

    if (major1 !== major2) {
      return major1 - major2;
    } else if (minor1 !== minor2) {
      return minor1 - minor2;
    } else {
      return patch1 - patch2;
    }
  }
}
```

---

## Staged Rollout

### Staged Rollout Strategy

```typescript
// Rollout Manager
class RolloutManager {
  /**
   * Create staged rollout
   */
  async createStagedRollout(params: {
    version: string;
    platform: 'ios' | 'android';
    initialPercentage: number;
    rolloutSchedule: Array<{
      percentage: number;
      delay: number; // in hours
    }>;
  }): Promise<void> {
    // 1. Initial rollout
    await this.rollout(params.platform, params.initialPercentage);

    // 2. Schedule subsequent rollouts
    for (const schedule of params.rolloutSchedule) {
      setTimeout(() => {
        this.rollout(params.platform, schedule.percentage);
      }, schedule.delay * 60 * 60 * 1000);
    }
  }

  /**
   * Rollout to percentage
   */
  async rollout(
    platform: 'ios' | 'android',
    percentage: number
  ): Promise<void> {
    if (platform === 'android') {
      await exec(`fastlane android rollout rollout:${percentage / 100}`);
    } else {
      // iOS doesn't support staged rollouts
      console.log('iOS staged rollout not supported');
    }
  }

  /**
   * Monitor rollout
   */
  async monitorRollout(params: {
    version: string;
    platform: 'ios' | 'android';
  }): Promise<{
    crashRate: number;
    userRating: number;
    activeUsers: number;
  }> {
    // Fetch metrics from analytics
    const metrics = await this.fetchMetrics(params);

    return metrics;
  }

  /**
   * Rollback if needed
   */
  async rollback(params: {
    version: string;
    platform: 'ios' | 'android';
  }): Promise<void> {
    if (platform === 'android') {
      await exec('fastlane android rollback');
    } else {
      // iOS rollback requires app rejection
      console.log('iOS rollback requires app rejection');
    }
  }

  /**
   * Fetch metrics
   */
  private async fetchMetrics(params: {
    version: string;
    platform: 'ios' | 'android';
  }): Promise<{
    crashRate: number;
    userRating: number;
    activeUsers: number;
  }> {
    // Implement metrics fetching
    return {
      crashRate: 0.01,
      userRating: 4.5,
      activeUsers: 1000,
    };
  }
}
```

---

## Best Practices

### App Distribution Checklist

```typescript
// Pre-Release Checklist
const preReleaseChecklist = [
  {
    task: 'Test on all supported devices',
    category: 'Testing',
    required: true,
  },
  {
    task: 'Test on all supported OS versions',
    category: 'Testing',
    required: true,
  },
  {
    task: 'Run automated tests',
    category: 'Testing',
    required: true,
  },
  {
    task: 'Perform manual testing',
    category: 'Testing',
    required: true,
  },
  {
    task: 'Review app metadata',
    category: 'Metadata',
    required: true,
  },
  {
    task: 'Review screenshots',
    category: 'Metadata',
    required: true,
  },
  {
    task: 'Update changelog',
    category: 'Metadata',
    required: true,
  },
  {
    task: 'Check app size',
    category: 'Performance',
    required: false,
  },
  {
    task: 'Check battery usage',
    category: 'Performance',
    required: false,
  },
  {
    task: 'Check memory usage',
    category: 'Performance',
    required: false,
  },
  {
    task: 'Review privacy policy',
    category: 'Compliance',
    required: true,
  },
  {
    task: 'Check permissions',
    category: 'Compliance',
    required: true,
  },
  {
    task: 'Review terms of service',
    category: 'Compliance',
    required: true,
  },
  {
    task: 'Test with beta testers',
    category: 'Beta Testing',
    required: true,
  },
  {
    task: 'Review feedback',
    category: 'Beta Testing',
    required: false,
  },
];

// Release Checklist
const releaseChecklist = [
  {
    task: 'Increment version number',
    category: 'Versioning',
    required: true,
  },
  {
    task: 'Update build number',
    category: 'Versioning',
    required: true,
  },
  {
    task: 'Build production bundle',
    category: 'Build',
    required: true,
  },
  {
    task: 'Sign with production certificate',
    category: 'Build',
    required: true,
  },
  {
    task: 'Upload to app store',
    category: 'Distribution',
    required: true,
  },
  {
    task: 'Submit for review',
    category: 'Distribution',
    required: true,
  },
  {
    task: 'Monitor review status',
    category: 'Distribution',
    required: true,
  },
  {
    task: 'Monitor crash rates',
    category: 'Monitoring',
    required: true,
  },
  {
    task: 'Monitor user feedback',
    category: 'Monitoring',
    required: true,
  },
  {
    task: 'Prepare rollback plan',
    category: 'Monitoring',
    required: false,
  },
];

// Post-Release Checklist
const postReleaseChecklist = [
  {
    task: 'Monitor crash reports',
    category: 'Monitoring',
    required: true,
  },
  {
    task: 'Monitor user feedback',
    category: 'Monitoring',
    required: true,
  },
  {
    task: 'Monitor app ratings',
    category: 'Monitoring',
    required: true,
  },
  {
    task: 'Monitor download numbers',
    category: 'Monitoring',
    required: true,
  },
  {
    task: 'Review analytics',
    category: 'Analytics',
    required: true,
  },
  {
    task: 'Address critical issues',
    category: 'Support',
    required: true,
  },
  {
    task: 'Plan next release',
    category: 'Planning',
    required: false,
  },
];
```

---

---

## Quick Start

### App Store Submission

```bash
# Build iOS app
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -archivePath MyApp.xcarchive \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath MyApp.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist ExportOptions.plist
```

### Google Play Submission

```bash
# Build Android app bundle
./gradlew bundleRelease

# Upload to Play Console
# Use Google Play Console web interface or API
```

---

## Production Checklist

- [ ] **App Store Setup**: App Store Connect account configured
- [ ] **Google Play Setup**: Google Play Console account configured
- [ ] **App Metadata**: Complete app metadata (name, description, screenshots)
- [ ] **Screenshots**: Screenshots for all device sizes
- [ ] **App Icon**: App icon in all required sizes
- [ ] **Privacy Policy**: Privacy policy URL
- [ ] **Versioning**: Semantic versioning strategy
- [ ] **Beta Testing**: Beta testing setup (TestFlight, Internal Testing)
- [ ] **OTA Updates**: OTA update mechanism (for React Native)
- [ ] **Staged Rollout**: Staged rollout strategy
- [ ] **Monitoring**: Monitor app performance post-release
- [ ] **ASO**: App Store Optimization

---

## Anti-patterns

### ❌ Don't: No Beta Testing

```markdown
# ❌ Bad - Direct to production
Build → Submit → Release
# No testing!
```

```markdown
# ✅ Good - Beta testing first
Build → TestFlight/Internal Testing → Fix issues → Release
```

### ❌ Don't: Poor Metadata

```markdown
# ❌ Bad - Incomplete metadata
Name: "My App"
Description: "App"
# No screenshots, no keywords
```

```markdown
# ✅ Good - Complete metadata
Name: "My App - Task Manager"
Description: "Powerful task management app..."
Keywords: "task, todo, productivity"
Screenshots: All device sizes
```

---

## Integration Points

- **Mobile CI/CD** (`31-mobile-development/mobile-ci-cd/`) - Automated builds
- **React Native Patterns** (`31-mobile-development/react-native-patterns/`) - App patterns
- **Versioning** (`01-foundations/versioning/`) - Version strategy

---

## Further Reading

- [App Store Connect](https://appstoreconnect.apple.com/)
- [Google Play Console](https://play.google.com/console)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Google Play Policies](https://play.google.com/about/developer-content-policy/)
- [Fastlane Documentation](https://docs.fastlane.tools/)
- [CodePush Documentation](https://microsoft.github.io/code-push/)
- [Expo Updates](https://docs.expo.dev/eas-update/introduction/)
