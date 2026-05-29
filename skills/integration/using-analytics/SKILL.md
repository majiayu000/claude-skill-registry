---
name: using-analytics
description: Track custom events and conversions with Vercel Web Analytics. Covers common events, form tracking, and development testing.
---

# Working with Analytics

Track custom events and conversions with Vercel Web Analytics. Covers common events, form tracking, and development testing.

## Implement Working with Analytics

Track custom events and conversions with Vercel Web Analytics. Covers common events, form tracking, and development testing.

**See:**

- Resource: `using-analytics` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/using-analytics

---

### Tracking Custom Events

Track user actions and conversions:

```typescript
import { track } from "@vercel/analytics";

// Basic event
track("signup_clicked");

// Event with properties
track("purchase_completed", {
  plan: "pro",
  price: 29,
  currency: "USD",
});
```

### Common Events to Track

Track meaningful user actions:

```typescript
// Authentication
track("signup_completed", { method: "email" });
track("signin_completed", { method: "google" });

// Feature usage
track("chat_started");
track("chat_completed", { messageCount: 5 });
track("file_uploaded", { type: "pdf", size: 1024 });

// Conversions
track("trial_started");
track("subscription_created", { plan: "pro" });
track("upgrade_completed", { from: "free", to: "pro" });
```

### Tracking in Components

```tsx
import { track } from "@vercel/analytics";

function UpgradeButton() {
  const handleClick = () => {
    track("upgrade_button_clicked", { location: "header" });
    // Navigate to upgrade page...
  };

  return <button onClick={handleClick}>Upgrade</button>;
}
```

### Tracking Form Submissions

```tsx
import { track } from "@vercel/analytics";

function ContactForm() {
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    track("contact_form_submitted", { source: "footer" });

    // Submit form...
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### Testing in Development

Analytics only send in production by default. For development testing:

```tsx
// In layout.tsx
<Analytics mode="development" />

// Or just log to console
<Analytics debug />
```

### Viewing Analytics

View analytics in the Vercel dashboard:

1. Go to your project in [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Analytics" in the sidebar
3. View page views, visitors, and custom events

---

## References

- [Vercel Web Analytics](https://vercel.com/docs/analytics)
- [Custom Events](https://vercel.com/docs/analytics/custom-events)
