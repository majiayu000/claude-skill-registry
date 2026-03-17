---
name: browser-extension
description: |
  Build browser extensions with WXT framework, Manifest V3, and TypeScript.
  Use when: creating Chrome extension, Firefox addon, browser plugin.
  Triggers: "extension", "browser extension", "chrome extension", "firefox addon", "manifest v3", "wxt".
---

# Browser Extension Development with WXT

## Quick Start

```bash
# Create new extension
npx wxt@latest init my-extension
cd my-extension

# Development (Chrome)
npm run dev

# Development (Firefox)
npm run dev:firefox

# Build for production
npm run build

# Create ZIP for store submission
npm run zip
```

---

## Project Structure

```
my-extension/
├── wxt.config.ts           # WXT configuration
├── entrypoints/
│   ├── background.ts       # Service worker
│   ├── content.ts          # Content script
│   ├── popup/
│   │   ├── index.html
│   │   ├── main.tsx
│   │   └── App.tsx
│   └── options/
│       ├── index.html
│       └── main.tsx
├── components/             # Shared React components
├── assets/
│   └── icon.png           # Auto-generates all sizes
├── public/                 # Static files
├── package.json
└── tsconfig.json
```

**Key difference from manual setup:** No `manifest.json` — WXT generates it automatically from entrypoints and config.

---

## WXT Configuration

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-react'],
  manifest: {
    name: 'My Extension',
    description: 'A browser extension built with WXT',
    permissions: ['storage', 'activeTab'],
    host_permissions: ['https://*.example.com/*'],
  },
});
```

---

## Background Script (Service Worker)

```typescript
// entrypoints/background.ts
export default defineBackground(() => {
  console.log('Extension installed', { id: browser.runtime.id });

  // Listen for messages
  browser.runtime.onMessage.addListener((message, sender) => {
    if (message.type === 'GET_DATA') {
      return fetchData(); // Return promise for async response
    }
  });

  // Context menu
  browser.contextMenus.create({
    id: 'my-action',
    title: 'Do Something',
    contexts: ['selection'],
  });

  browser.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'my-action') {
      console.log('Selected:', info.selectionText);
    }
  });
});
```

---

## Content Script

```typescript
// entrypoints/content.ts
export default defineContentScript({
  matches: ['https://*.example.com/*'],
  main() {
    console.log('Content script loaded');

    // DOM manipulation
    const button = document.createElement('button');
    button.textContent = 'My Extension';
    button.onclick = () => {
      browser.runtime.sendMessage({ type: 'BUTTON_CLICKED' });
    };
    document.body.appendChild(button);

    // Listen for messages from background
    browser.runtime.onMessage.addListener((message) => {
      if (message.type === 'HIGHLIGHT') {
        document.body.style.backgroundColor = 'yellow';
      }
    });
  },
});
```

### Content Script with UI (React)

```typescript
// entrypoints/content.tsx
import ReactDOM from 'react-dom/client';
import App from './App';

export default defineContentScript({
  matches: ['https://*.example.com/*'],
  cssInjectionMode: 'ui',

  main(ctx) {
    const ui = createIntegratedUi(ctx, {
      position: 'inline',
      anchor: 'body',
      onMount: (container) => {
        const root = ReactDOM.createRoot(container);
        root.render(<App />);
        return root;
      },
      onRemove: (root) => {
        root.unmount();
      },
    });
    ui.mount();
  },
});
```

---

## Popup (React)

```html
<!-- entrypoints/popup/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
</head>
<body>
  <div id="root"></div>
  <script type="module" src="./main.tsx"></script>
</body>
</html>
```

```tsx
// entrypoints/popup/main.tsx
import ReactDOM from 'react-dom/client';
import App from './App';
import './style.css';

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
```

```tsx
// entrypoints/popup/App.tsx
import { useState, useEffect } from 'react';
import { storage } from 'wxt/storage';

// Type-safe storage
const enabledStorage = storage.defineItem<boolean>('sync:enabled', {
  fallback: true,
});

export default function App() {
  const [enabled, setEnabled] = useState(true);

  useEffect(() => {
    enabledStorage.getValue().then(setEnabled);
  }, []);

  const toggle = async () => {
    const newValue = !enabled;
    await enabledStorage.setValue(newValue);
    setEnabled(newValue);
  };

  const handleAction = async () => {
    const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
    if (tab.id) {
      browser.tabs.sendMessage(tab.id, { type: 'HIGHLIGHT' });
    }
  };

  return (
    <div className="p-4 w-64">
      <h1 className="text-lg font-bold mb-4">My Extension</h1>
      <label className="flex items-center gap-2 mb-4">
        <input type="checkbox" checked={enabled} onChange={toggle} />
        Enabled
      </label>
      <button
        onClick={handleAction}
        className="w-full bg-blue-500 text-white py-2 rounded"
      >
        Do Something
      </button>
    </div>
  );
}
```

---

## Type-Safe Storage (WXT)

```typescript
// utils/storage.ts
import { storage } from 'wxt/storage';

// Define typed storage items
export const settings = storage.defineItem<{
  enabled: boolean;
  theme: 'light' | 'dark';
  apiKey?: string;
}>('sync:settings', {
  fallback: {
    enabled: true,
    theme: 'light',
  },
});

// Usage
const current = await settings.getValue();
await settings.setValue({ ...current, theme: 'dark' });

// Watch for changes
settings.watch((newValue) => {
  console.log('Settings changed:', newValue);
});
```

---

## Message Passing

```typescript
// Define message types
interface Messages {
  getData: { query: string };
  highlight: { color: string };
}

// Background
browser.runtime.onMessage.addListener((message: Messages[keyof Messages]) => {
  // Handle messages
});

// Content/Popup → Background
const response = await browser.runtime.sendMessage({ type: 'getData', query: 'test' });

// Background → Content
await browser.tabs.sendMessage(tabId, { type: 'highlight', color: 'yellow' });
```

---

## Permissions

```typescript
// wxt.config.ts
export default defineConfig({
  manifest: {
    // Required permissions (always active)
    permissions: ['storage', 'activeTab'],

    // Optional permissions (request at runtime)
    optional_permissions: ['tabs', 'history'],

    // Host permissions
    host_permissions: ['https://*.example.com/*'],
    optional_host_permissions: ['https://*/*'],
  },
});
```

```typescript
// Request optional permission
const granted = await browser.permissions.request({
  permissions: ['tabs'],
  origins: ['https://other-site.com/*'],
});
```

---

## Cross-Browser Support

WXT handles browser differences automatically:

```typescript
// Use `browser` namespace (works in all browsers)
browser.storage.sync.get(['key']);
browser.runtime.sendMessage({ type: 'test' });

// WXT polyfills Chrome's callback-based APIs to Promises
const tabs = await browser.tabs.query({ active: true });
```

Build for specific browser:
```bash
npm run build           # Chrome (default)
npm run build:firefox   # Firefox
npm run build:safari    # Safari
npm run build:edge      # Edge
```

---

## Testing

### Unit Tests (Vitest)

```typescript
// tests/storage.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fakeBrowser } from 'wxt/testing';

describe('Settings storage', () => {
  beforeEach(() => {
    fakeBrowser.reset();
  });

  it('saves and loads settings', async () => {
    const { settings } = await import('../utils/storage');

    await settings.setValue({ enabled: false, theme: 'dark' });
    const result = await settings.getValue();

    expect(result.enabled).toBe(false);
    expect(result.theme).toBe('dark');
  });
});
```

### E2E Tests (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('popup opens and toggles', async ({ page, context }) => {
  // Load extension
  const extensionId = // ... get from context

  await page.goto(`chrome-extension://${extensionId}/popup.html`);

  const checkbox = page.getByRole('checkbox');
  await expect(checkbox).toBeChecked();

  await checkbox.click();
  await expect(checkbox).not.toBeChecked();
});
```

---

## Common Patterns

### Inject CSS

```typescript
// entrypoints/content.ts
export default defineContentScript({
  matches: ['https://*.example.com/*'],
  css: ['./styles.css'], // Auto-injected
  main() {
    // ...
  },
});
```

### Run at Document Start

```typescript
export default defineContentScript({
  matches: ['*://*/*'],
  runAt: 'document_start', // Before page loads
  main() {
    // Block/modify requests early
  },
});
```

### Alarms (Scheduled Tasks)

```typescript
// entrypoints/background.ts
export default defineBackground(() => {
  browser.alarms.create('sync', { periodInMinutes: 30 });

  browser.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'sync') {
      syncData();
    }
  });
});
```

---

## Publishing

### Chrome Web Store

```bash
npm run zip              # Creates .output/my-extension-x.x.x-chrome.zip
# Upload to Chrome Web Store Developer Dashboard
```

**Required justifications for permissions:**

| Permission | Example Justification |
|------------|----------------------|
| `storage` | Stores user preferences locally: enabled state, settings. No data transmitted externally. |
| `activeTab` | Used to apply extension functionality to the current tab when user clicks extension icon. |
| `tabs` | Required to detect current website URL and determine if extension should activate based on user settings. |
| `host_permissions: <all_urls>` | Required to inject extension functionality on any website user adds to their list. Only activates on sites explicitly selected by user. |

**Warning:** Broad host permissions (`<all_urls>`) trigger in-depth review (1-2 weeks vs days). If you only need specific sites, list them explicitly.

**Store description template:**
```
Short tagline. Clear value proposition.

How it works:
Brief explanation of the mechanism.

Features:
• Feature 1 — short description
• Feature 2 — short description
• Feature 3 — short description

Privacy-first:
• No tracking
• No accounts
• All data stored locally

Call to action.
```

### Firefox Add-ons

```bash
npm run zip:firefox      # Creates .output/my-extension-x.x.x-firefox.zip
# Also creates .output/my-extension-x.x.x-sources.zip (required for review)
# Upload to Firefox Add-ons Developer Hub
```

**CRITICAL: Firefox Manifest Requirements (2024+)**

Firefox requires `browser_specific_settings.gecko.data_collection_permissions` for all new extensions:

```typescript
// wxt.config.ts
export default defineConfig({
  manifest: {
    // ... other config
    browser_specific_settings: {
      gecko: {
        id: 'your-extension@your-domain.com',
        strict_min_version: '142.0', // Required for data_collection_permissions
        data_collection_permissions: {
          // For extensions that DON'T collect data:
          required: ['none'],

          // For extensions that DO collect data, specify types:
          // required: ['browsingActivity', 'websiteContent'],
          // optional: ['locationInfo'],
        },
      },
    },
  },
});
```

**Valid data_collection_permissions values:**
- `'none'` — extension doesn't collect any data
- `'locationInfo'` — physical location
- `'healthInfo'` — health data
- `'financialAndPaymentInfo'` — payment info
- `'authenticationInfo'` — login credentials
- `'personalCommunications'` — messages, emails
- `'browsingActivity'` — browsing history
- `'websiteContent'` — page content
- `'websiteActivity'` — clicks, interactions
- `'searchTerms'` — search queries
- `'bookmarksInfo'` — bookmarks
- `'personallyIdentifyingInfo'` — PII

**Firefox submission notes template:**
```
Version notes:
Initial release of [Extension Name] - [brief description].

Notes for reviewer:
- No account required to test
- To test:
  1. Install extension
  2. [Step by step testing instructions]
- No external services or APIs used
- All data stored locally via browser.storage
```

### Edge Add-ons

```bash
# Use the same Chrome zip - Edge is Chromium-based
npm run zip              # Creates .output/my-extension-x.x.x-chrome.zip
# Upload to Edge Add-ons Developer Dashboard
```

### Naming Convention for ZIPs

```bash
# Rename for clarity
mv .output/my-extension-1.0.0-chrome.zip ./my-extension-v1.0.0-chrome.zip
mv .output/my-extension-1.0.0-firefox.zip ./my-extension-v1.0.0-firefox.zip
```

---

## Security Checklist

- [ ] Minimal permissions (request only what's needed)
- [ ] No `eval()` or inline scripts
- [ ] Validate all external data
- [ ] Use HTTPS only
- [ ] No API keys in source code
- [ ] Input sanitization in content scripts
- [ ] pre-commit hooks with gitleaks

---

## Resources

- [WXT Documentation](https://wxt.dev)
- [Chrome Extensions Docs](https://developer.chrome.com/docs/extensions)
- [Firefox Add-ons Docs](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions)
