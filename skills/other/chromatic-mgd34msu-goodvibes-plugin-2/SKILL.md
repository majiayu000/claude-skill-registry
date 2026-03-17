---
name: chromatic
description: Automates visual regression testing for Storybook components using cloud-based snapshot comparison. Use when setting up visual testing, catching UI regressions, or reviewing component changes.
---

# Chromatic Visual Testing

Cloud-based visual testing platform that captures screenshots of every Storybook story and detects visual changes.

## Quick Start

```bash
# Install Chromatic
npx storybook add chromatic

# Or install manually
npm install --save-dev chromatic

# Run visual tests (first time creates baselines)
npx chromatic --project-token=<token>
```

## How It Works

1. **Cloud Rendering**: Chromatic renders components in cloud browsers
2. **Snapshot Capture**: Takes screenshot of each story
3. **Automated Diffing**: Compares new snapshots to baselines
4. **Review & Verify**: Approve or reject visual changes

## Configuration

### chromatic.config.json

```json
{
  "projectToken": "chpt_xxxxxxxxxxxx",
  "buildScriptName": "build-storybook",
  "storybookBuildDir": "storybook-static",
  "zip": true,
  "autoAcceptChanges": "main",
  "exitOnceUploaded": false,
  "exitZeroOnChanges": false,
  "onlyChanged": true,
  "externals": ["public/**"],
  "skip": "dependabot/**"
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "chromatic": "chromatic --exit-zero-on-changes",
    "chromatic:ci": "chromatic --auto-accept-changes=main"
  }
}
```

## Story-Level Configuration

### Disable Snapshots

```tsx
// Skip specific story
export const Loading: Story = {
  parameters: {
    chromatic: { disableSnapshot: true }
  }
};

// Skip all stories in file
export default {
  title: 'Components/Spinner',
  parameters: {
    chromatic: { disableSnapshot: true }
  }
};
```

### Viewport Testing

```tsx
export const Responsive: Story = {
  parameters: {
    chromatic: {
      viewports: [320, 768, 1200]
    }
  }
};
```

### Delay for Animations

```tsx
export const Animated: Story = {
  parameters: {
    chromatic: {
      delay: 300, // Wait 300ms before snapshot
      pauseAnimationAtEnd: true
    }
  }
};
```

### Diff Threshold

```tsx
export const SubtleChanges: Story = {
  parameters: {
    chromatic: {
      diffThreshold: 0.2 // 0-1, higher = more tolerant
    }
  }
};
```

## Multi-Browser Testing

```tsx
// Test in multiple browsers
export default {
  title: 'Components/Button',
  parameters: {
    chromatic: {
      modes: {
        chrome: { viewport: 1200 },
        firefox: { viewport: 1200 },
        safari: { viewport: 1200 },
        edge: { viewport: 1200 }
      }
    }
  }
};
```

## Modes for Theme/Locale Testing

```tsx
// .storybook/modes.ts
export const allModes = {
  light: { theme: 'light' },
  dark: { theme: 'dark' },
  mobile: { viewport: { width: 375, height: 667 } },
  desktop: { viewport: { width: 1200, height: 800 } }
};

// Component story
export const Button: Story = {
  parameters: {
    chromatic: {
      modes: {
        'light desktop': allModes['light'],
        'dark desktop': { ...allModes['dark'], ...allModes['desktop'] },
        'light mobile': { ...allModes['light'], ...allModes['mobile'] }
      }
    }
  }
};
```

## CI Integration

### GitHub Actions

```yaml
name: Chromatic

on: push

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Required for accurate baselines

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci

      - uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          autoAcceptChanges: main
          onlyChanged: true
```

### GitLab CI

```yaml
chromatic:
  stage: test
  image: node:20
  script:
    - npm ci
    - npx chromatic --project-token=$CHROMATIC_PROJECT_TOKEN
  only:
    - merge_requests
    - main
```

## TurboSnap (Incremental Testing)

Only test stories affected by code changes:

```bash
npx chromatic --only-changed
```

Configure in CI:

```yaml
- uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    onlyChanged: true
    traceChanged: expanded # Track changes across files
```

## Handling Dynamic Content

### Ignore DOM Elements

```tsx
export const WithTimestamp: Story = {
  parameters: {
    chromatic: {
      diffIncludeAntiAliasing: false
    }
  },
  decorators: [
    (Story) => (
      <>
        <Story />
        <span data-chromatic="ignore">
          {new Date().toISOString()}
        </span>
      </>
    )
  ]
};
```

### Mock Data

```tsx
export const UserProfile: Story = {
  parameters: {
    chromatic: { delay: 500 }
  },
  loaders: [
    async () => ({
      user: { name: 'Test User', avatar: '/mock-avatar.png' }
    })
  ]
};
```

## Review Workflow

### Accept Changes

```bash
# Auto-accept on main branch
npx chromatic --auto-accept-changes=main

# Accept specific branches
npx chromatic --auto-accept-changes="main|release/*"
```

### Skip Builds

```bash
# Skip CI for specific patterns
npx chromatic --skip="dependabot/**"

# Skip with commit message
git commit -m "docs: update readme [skip chromatic]"
```

## Troubleshooting

### Flaky Tests

```tsx
// Increase delay for async content
parameters: {
  chromatic: {
    delay: 1000,
    diffThreshold: 0.1
  }
}
```

### Font Loading Issues

```tsx
// Wait for fonts in preview.js
export const decorators = [
  (Story) => {
    const [fontsLoaded, setFontsLoaded] = useState(false);

    useEffect(() => {
      document.fonts.ready.then(() => setFontsLoaded(true));
    }, []);

    return fontsLoaded ? <Story /> : null;
  }
];
```

### External Resources

```json
{
  "externals": [
    "public/fonts/**",
    "public/images/**"
  ]
}
```

See [references/configuration.md](references/configuration.md) for complete CLI options and [references/ci-integration.md](references/ci-integration.md) for advanced CI setups.
