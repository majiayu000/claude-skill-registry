---
name: cookies-analytics
description: Set up Google Analytics 4 with DSGVO-compliant cookie consent banner. Use when analytics tracking is needed. Triggers on "analytics", "GA4", "Google Analytics", "cookie consent", "tracking".
---

# Cookies & Analytics

Set up GA4 with DSGVO-compliant cookie consent.

## Overview

1. Create cookie consent banner component
2. Set up Google Analytics 4
3. Only load GA after consent
4. Store consent in localStorage

## Cookie Consent Banner

Create `components/cookie-consent.tsx`:

```tsx
'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'

export function CookieConsent() {
  const [showBanner, setShowBanner] = useState(false)

  useEffect(() => {
    const consent = localStorage.getItem('cookie-consent')
    if (!consent) setShowBanner(true)
  }, [])

  const acceptAll = () => {
    localStorage.setItem('cookie-consent', 'all')
    setShowBanner(false)
    loadAnalytics()
  }

  const acceptEssential = () => {
    localStorage.setItem('cookie-consent', 'essential')
    setShowBanner(false)
  }

  if (!showBanner) return null

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-background border-t p-4 z-50">
      <div className="container flex flex-col md:flex-row items-center justify-between gap-4">
        <p className="text-sm text-muted-foreground">
          Wir verwenden Cookies, um Ihre Erfahrung zu verbessern.{' '}
          <a href="/datenschutz" className="underline">Mehr erfahren</a>
        </p>
        <div className="flex gap-2">
          <Button variant="outline" onClick={acceptEssential}>
            Nur notwendige
          </Button>
          <Button onClick={acceptAll}>
            Alle akzeptieren
          </Button>
        </div>
      </div>
    </div>
  )
}

function loadAnalytics() {
  // Load GA4 script dynamically
  const script = document.createElement('script')
  script.src = `https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`
  script.async = true
  document.head.appendChild(script)

  window.dataLayer = window.dataLayer || []
  function gtag(...args: any[]) { window.dataLayer.push(args) }
  gtag('js', new Date())
  gtag('config', process.env.NEXT_PUBLIC_GA_ID)
}
```

## Environment Variables

Add to `.env.local`:

```
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

## Layout Integration

Add to `app/layout.tsx`:

```tsx
import { CookieConsent } from '@/components/cookie-consent'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <CookieConsent />
      </body>
    </html>
  )
}
```

## Check Existing Consent on Load

Add to layout or a provider:

```tsx
'use client'

import { useEffect } from 'react'

export function AnalyticsProvider({ children }) {
  useEffect(() => {
    const consent = localStorage.getItem('cookie-consent')
    if (consent === 'all') {
      loadAnalytics()
    }
  }, [])

  return <>{children}</>
}
```

## Datenschutz Update

Add to Datenschutz page:

```markdown
### Google Analytics

Diese Website verwendet Google Analytics 4, einen Webanalysedienst der Google LLC.
Die Nutzung erfolgt nur nach Ihrer ausdrücklichen Einwilligung.

**Verarbeitete Daten:**
- IP-Adresse (anonymisiert)
- Besuchte Seiten
- Verweildauer
- Geräte- und Browserinformationen

**Rechtsgrundlage:** Art. 6 Abs. 1 lit. a DSGVO (Einwilligung)

Sie können Ihre Einwilligung jederzeit widerrufen, indem Sie die Cookies in Ihrem Browser löschen.
```

## Checklist

- [ ] Cookie consent component created
- [ ] GA4 only loads after consent
- [ ] Consent stored in localStorage
- [ ] Datenschutz updated with GA info
- [ ] Environment variable set
- [ ] Banner displays on first visit
- [ ] "Nur notwendige" doesn't load GA
- [ ] "Alle akzeptieren" loads GA
