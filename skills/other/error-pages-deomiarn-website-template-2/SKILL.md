---
name: error-pages
description: Create custom 404 and 500 error pages with brand styling. Use at project end before release. Triggers on "404", "error pages", "not found", "500 error".
---

# Error Pages

Create branded 404 and 500 error pages.

## Workflow

1. Create app/not-found.tsx (404)
2. Create app/error.tsx (500)
3. Match brand styling from globals.css
4. Add i18n support

## 404 Page (not-found.tsx)

Create at `app/not-found.tsx`:

```tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-svh flex items-center justify-center bg-background">
      <div className="container text-center">
        <h1 className="mb-4">404</h1>
        <p className="text-muted-foreground mb-8">
          Diese Seite wurde nicht gefunden.
        </p>
        <Link href="/" className="btn btn-primary">
          Zurück zur Startseite
        </Link>
      </div>
    </div>
  )
}
```

## 500 Page (error.tsx)

Create at `app/error.tsx`:

```tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="min-h-svh flex items-center justify-center bg-background">
      <div className="container text-center">
        <h1 className="mb-4">Fehler</h1>
        <p className="text-muted-foreground mb-8">
          Ein unerwarteter Fehler ist aufgetreten.
        </p>
        <button onClick={reset} className="btn btn-primary">
          Erneut versuchen
        </button>
      </div>
    </div>
  )
}
```

## i18n Support

Add to messages/de.json and messages/en.json:

```json
{
  "error": {
    "404": {
      "title": "404",
      "message": "Diese Seite wurde nicht gefunden.",
      "cta": "Zurück zur Startseite"
    },
    "500": {
      "title": "Fehler",
      "message": "Ein unerwarteter Fehler ist aufgetreten.",
      "cta": "Erneut versuchen"
    }
  }
}
```

## Checklist

- [ ] app/not-found.tsx created
- [ ] app/error.tsx created
- [ ] Brand styling applied
- [ ] i18n text added
- [ ] 404 page tested (visit /nonexistent-page)
