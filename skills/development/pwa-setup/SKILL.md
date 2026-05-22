---
name: pwa-setup
description: Progressive Web App setup with manifest, mobile meta tags, safe area handling for notched devices, and install prompts for app-like browser experience.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: frontend
  time: 2h
  source: drift-masterguide
---

# PWA Setup

Progressive Web App configuration for app-like browser experience.

## When to Use This Skill

- Users want to "install" your web app
- Mobile users want home screen access
- Need app-like behavior without native apps
- Supporting notched devices (iPhone, etc.)

## Core Concepts

PWA requires:
1. **Web App Manifest** - App metadata and icons
2. **Mobile meta tags** - Viewport and theme configuration
3. **Safe areas** - Handle notched devices
4. **Install prompt** - Custom install experience

## Implementation

### TypeScript (Next.js)

```typescript
// app/manifest.ts
import type { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "My SaaS App",
    short_name: "MySaaS",
    description: "Your app description here",
    start_url: '/dashboard',
    display: 'standalone',
    background_color: '#0f172a',
    theme_color: '#14b8a6',
    orientation: 'portrait-primary',
    
    icons: [
      {
        src: '/icons/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
        purpose: 'any',
      },
      {
        src: '/icons/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'any',
      },
      {
        src: '/icons/icon-maskable.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'maskable',
      },
    ],
    
    shortcuts: [
      { name: 'Dashboard', url: '/dashboard', description: 'Go to dashboard' },
      { name: 'Settings', url: '/settings', description: 'App settings' },
    ],
    
    categories: ['productivity', 'utilities'],
  };
}
```

### Root Layout Metadata

```typescript
// app/layout.tsx
import type { Metadata, Viewport } from 'next';

export const metadata: Metadata = {
  title: "My SaaS App",
  description: "Your app description",
  
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: "MySaaS",
  },
  
  applicationName: "MySaaS",
  
  openGraph: {
    title: "My SaaS App",
    description: "Your app description",
    type: 'website',
    siteName: "MySaaS",
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#14b8a6',
  viewportFit: 'cover',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-neutral-900 text-neutral-cream min-h-screen">
        {children}
      </body>
    </html>
  );
}
```

### Safe Area CSS

```css
/* globals.css */

/* Safe area for bottom navigation (notched devices) */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0);
}

/* Safe area for top header */
.safe-area-top {
  padding-top: env(safe-area-inset-top, 0);
}

/* Full safe area padding */
.safe-area-all {
  padding-top: env(safe-area-inset-top, 0);
  padding-right: env(safe-area-inset-right, 0);
  padding-bottom: env(safe-area-inset-bottom, 0);
  padding-left: env(safe-area-inset-left, 0);
}
```

### Install Prompt Hook

```typescript
// hooks/useInstallPrompt.ts
'use client';

import { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export function useInstallPrompt() {
  const [installPrompt, setInstallPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
      return;
    }

    const handler = (e: Event) => {
      e.preventDefault();
      setInstallPrompt(e as BeforeInstallPromptEvent);
    };

    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const promptInstall = async () => {
    if (!installPrompt) return false;

    await installPrompt.prompt();
    const { outcome } = await installPrompt.userChoice;

    if (outcome === 'accepted') {
      setIsInstalled(true);
      setInstallPrompt(null);
    }

    return outcome === 'accepted';
  };

  return {
    canInstall: !!installPrompt && !isInstalled,
    isInstalled,
    promptInstall,
  };
}
```

### Install Banner Component

```typescript
// components/InstallBanner.tsx
'use client';

import { useInstallPrompt } from '@/hooks/useInstallPrompt';

export function InstallBanner() {
  const { canInstall, promptInstall } = useInstallPrompt();

  if (!canInstall) return null;

  return (
    <div className="fixed bottom-20 left-4 right-4 bg-primary-600 text-white p-4 rounded-lg shadow-lg md:hidden">
      <p className="text-sm mb-2">Install our app for a better experience</p>
      <button
        onClick={promptInstall}
        className="w-full py-2 bg-white text-primary-600 rounded font-medium"
      >
        Install App
      </button>
    </div>
  );
}
```

### Mobile Navigation with Safe Area

```typescript
// components/MobileNav.tsx
export function MobileNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-neutral-800 border-t border-neutral-700 z-30 md:hidden safe-area-bottom">
      <div className="flex justify-around py-2">
        <NavItem href="/dashboard" icon={HomeIcon} label="Home" />
        <NavItem href="/search" icon={SearchIcon} label="Search" />
        <NavItem href="/settings" icon={SettingsIcon} label="Settings" />
      </div>
    </nav>
  );
}
```

## Icon Requirements

```
public/
├── icons/
│   ├── icon-192.png      # Standard icon
│   ├── icon-512.png      # Large icon
│   └── icon-maskable.png # Maskable (with safe zone padding)
├── favicon.ico
└── apple-touch-icon.png  # 180x180 for iOS
```

### Maskable Icon Safe Zone

```
┌─────────────────────┐
│                     │
│   ┌───────────┐     │
│   │   LOGO    │     │  ← Content in center 80%
│   └───────────┘     │
│                     │
└─────────────────────┘
```

## Usage Examples

### Testing PWA

1. Chrome DevTools → Application → Manifest
2. Lighthouse → PWA audit
3. Mobile → Add to Home Screen

### Detecting Standalone Mode

```typescript
function isStandalone(): boolean {
  return window.matchMedia('(display-mode: standalone)').matches ||
         (window.navigator as any).standalone === true;
}
```

## Best Practices

1. Use maskable icons with safe zone
2. Set theme_color to match your brand
3. Handle safe areas for notched devices
4. Provide install prompt at appropriate time
5. Test on actual mobile devices

## Common Mistakes

- Missing maskable icon (ugly on Android)
- No safe area handling (content under notch)
- Install prompt shown immediately (annoying)
- Wrong start_url (opens wrong page)
- Missing apple-touch-icon (iOS fallback)

## Related Patterns

- design-tokens - Consistent theming
- mobile-components - Responsive components
