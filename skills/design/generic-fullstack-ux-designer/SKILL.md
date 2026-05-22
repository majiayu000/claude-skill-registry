---
name: generic-fullstack-ux-designer
description: Professional UI/UX design expertise for full-stack applications. Covers design thinking, user psychology (Hick's/Fitts's/Jakob's Law), visual hierarchy, interaction patterns, accessibility, performance-driven design, and design critique. Use when designing features, improving UX, solving user problems, or conducting design reviews.
---

# Fullstack UX Designer

Professional UX expertise for Next.js/NestJS full-stack applications.

**Extends:** [Generic UX Designer](../generic-ux-designer/SKILL.md) - Read base skill for design thinking process, research methods, interaction patterns, and critique framework.

## Full-Stack UX Considerations

### Server-Side Rendering UX

| Scenario          | UX Pattern                                       |
| ----------------- | ------------------------------------------------ |
| Initial page load | Hydration-safe skeleton screens                  |
| Data fetching     | Server components for static, client for dynamic |
| Authentication    | Protected routes with redirect UX                |
| Form submission   | Progressive enhancement                          |

### Hydration-Safe Patterns

```tsx
// ✓ Avoid hydration mismatch
function Timestamp({ date }: { date: Date }) {
  const [formatted, setFormatted] = useState("");

  useEffect(() => {
    setFormatted(date.toLocaleString()); // Client-side only
  }, [date]);

  return <span>{formatted || "Loading..."}</span>;
}
```

## API Loading & Error States

### Loading State Hierarchy

| Duration   | Pattern         | Example      |
| ---------- | --------------- | ------------ |
| < 100ms    | No indicator    | Button click |
| 100ms - 1s | Subtle spinner  | Form submit  |
| 1s - 5s    | Skeleton screen | Page fetch   |
| > 5s       | Progress bar    | File upload  |

### Error State Design

```
API Error → Parse Error → User-Friendly Message → Recovery Action
```

| Error Type       | User Message           | Recovery          |
| ---------------- | ---------------------- | ----------------- |
| 400 Validation   | Show field errors      | Fix and retry     |
| 401 Unauthorized | "Please log in"        | Redirect to login |
| 404 Not Found    | "Item not found"       | Navigate back     |
| 500 Server Error | "Something went wrong" | Retry button      |

## Optimistic UI Pattern

```typescript
// Show immediate feedback, rollback on error
async function toggleLike(postId: string) {
  // 1. Update UI immediately
  setLiked(true);
  setLikeCount((c) => c + 1);

  try {
    // 2. Call API
    await api.like(postId);
  } catch {
    // 3. Rollback on failure
    setLiked(false);
    setLikeCount((c) => c - 1);
    showToast("Failed to like");
  }
}
```

### When to Use Optimistic UI

| Action        | Optimistic? | Why                        |
| ------------- | ----------- | -------------------------- |
| Like/favorite | Yes         | Low risk, common action    |
| Add comment   | Yes         | Can show pending state     |
| Delete item   | No          | Destructive, needs confirm |
| Payment       | No          | Critical, must verify      |
| Form submit   | Maybe       | Depends on complexity      |

## Form Submission UX

### Client → Server Flow

```
User Input → Client Validation → Submit → Server Validation → Response
     ↓              ↓              ↓              ↓              ↓
  Feedback    Inline errors   Loading...   Field errors    Success/Error
```

### Multi-Step Forms

```tsx
// Show progress and allow back navigation
<FormStepper
  steps={["Details", "Payment", "Confirm"]}
  currentStep={step}
  onBack={() => setStep((s) => s - 1)}
/>
```

## Authentication UX

### Login Flow Patterns

| State         | UX                           |
| ------------- | ---------------------------- |
| Loading auth  | Full-page skeleton           |
| Not logged in | Show login form              |
| Logging in    | Disable form, show spinner   |
| Success       | Redirect with toast          |
| Error         | Inline error, keep form data |

### Protected Route Pattern

```tsx
// Redirect unauthenticated users
if (!user && !loading) {
  return <Navigate to="/login" state={{ from: location }} />;
}
```

## Real-Time Updates

| Pattern   | Use Case                              |
| --------- | ------------------------------------- |
| Polling   | Low-frequency updates (notifications) |
| WebSocket | Chat, live collaboration              |
| SSE       | One-way server updates                |

### Presence Indicators

- Online status dots
- "User is typing..." indicators
- Collaborative cursors

## Full-Stack Design Critique

| Aspect           | Questions                        |
| ---------------- | -------------------------------- |
| Loading states   | What shows during API calls?     |
| Error recovery   | Can users recover from errors?   |
| Offline behavior | What happens without network?    |
| Auth transitions | Smooth login/logout experience?  |
| Data freshness   | Is stale data clearly indicated? |

## See Also

- [Generic UX Designer](../generic-ux-designer/SKILL.md) - Base methodology
- [UX Principles](../_shared/UX_PRINCIPLES.md) - Research methods, heuristics
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Visual patterns
