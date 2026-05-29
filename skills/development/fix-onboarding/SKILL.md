---
name: fix-onboarding
description: |
  Run /check-onboarding, then fix the highest priority onboarding issue.
  Creates one fix per invocation. Invoke again for next issue.
  Use /log-onboarding-issues to create issues without fixing.
---

# /fix-onboarding

Fix the highest priority onboarding issue.

## What This Does

1. Invoke `/check-onboarding` to audit new user experience
2. Identify highest priority issue
3. Fix that one issue
4. Verify the fix
5. Report what was done

**This is a fixer.** It fixes one issue at a time. Run again for next issue.

## Process

### 1. Run Primitive

Invoke `/check-onboarding` skill to get prioritized findings.

### 2. Fix Priority Order

Fix in this order:
1. **P0**: No onboarding flow, broken auth, paywall before value
2. **P1**: No empty states, no guidance, complex forms, no loading
3. **P2**: No progressive disclosure, no tooltips, no tour
4. **P3**: Retention hooks

### 3. Execute Fix

**No onboarding flow (P0):**
Create `app/onboarding/page.tsx`:
```tsx
export default function OnboardingPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md text-center">
        <h1 className="text-3xl font-bold mb-4">Welcome! 👋</h1>
        <p className="text-gray-600 mb-8">
          Let's get you started with your first [thing].
        </p>
        <a
          href="/create"
          className="bg-primary text-white px-6 py-3 rounded-lg"
        >
          Create your first [thing]
        </a>
      </div>
    </div>
  );
}
```

Add redirect for new users:
```tsx
// middleware.ts or layout check
const isNewUser = !user.hasCompletedOnboarding;
if (isNewUser) redirect('/onboarding');
```

**No empty states (P1):**
Create `components/empty-state.tsx`:
```tsx
export function EmptyState({
  title,
  description,
  action,
  actionHref,
}: {
  title: string;
  description: string;
  action: string;
  actionHref: string;
}) {
  return (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">📭</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 mb-6">{description}</p>
      <a href={actionHref} className="bg-primary text-white px-4 py-2 rounded">
        {action}
      </a>
    </div>
  );
}
```

Use in lists:
```tsx
{items.length === 0 ? (
  <EmptyState
    title="No projects yet"
    description="Create your first project to get started"
    action="Create Project"
    actionHref="/projects/new"
  />
) : (
  <ItemsList items={items} />
)}
```

**No first-action guidance (P1):**
Add inline hints:
```tsx
<div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
  <p className="text-blue-800">
    💡 <strong>Quick tip:</strong> Start by creating your first project.
    It only takes 30 seconds!
  </p>
</div>
```

**Complex initial forms (P1):**
Simplify to essential fields only:
```tsx
// Before: 10 required fields
// After: 2 required fields + "You can add more details later"

<form>
  <input name="name" required placeholder="Project name" />
  <button type="submit">Create</button>
  <p className="text-sm text-gray-500">
    You can add more details later
  </p>
</form>
```

**No loading states (P1):**
Add skeleton component:
```tsx
export function Skeleton({ className }: { className?: string }) {
  return (
    <div className={`animate-pulse bg-gray-200 rounded ${className}`} />
  );
}

// Usage
{isLoading ? (
  <div className="space-y-4">
    <Skeleton className="h-8 w-full" />
    <Skeleton className="h-8 w-full" />
    <Skeleton className="h-8 w-full" />
  </div>
) : (
  <ItemsList items={items} />
)}
```

### 4. Verify

After fix:
```bash
# New user gets onboarding
# Test: Create new account, verify redirect

# Empty state shows
# Test: Clear user data, check list renders empty state

# Loading state shows
# Test: Throttle network, verify skeleton visible
```

### 5. Report

```
Fixed: [P0] No onboarding flow

Created:
- app/onboarding/page.tsx (welcome screen)
- middleware.ts update (new user redirect)
- components/onboarding-complete-button.tsx

Flow:
1. New user signs up
2. Redirected to /onboarding
3. Single CTA to first action
4. Marked complete on first creation

Next highest priority: [P1] No empty states
Run /fix-onboarding again to continue.
```

## Branching

Before making changes:
```bash
git checkout -b feat/onboarding-$(date +%Y%m%d)
```

## Single-Issue Focus

Onboarding has many moving parts. Fix incrementally:
- Test each change with real new users
- Measure activation rate changes
- Easy to A/B test variations

Run `/fix-onboarding` repeatedly to improve activation.

## Related

- `/check-onboarding` - The primitive (audit only)
- `/log-onboarding-issues` - Create issues without fixing
- `/cro` - Conversion rate optimization
