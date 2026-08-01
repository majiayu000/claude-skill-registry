---
name: after
description: '"Create a new component to display a user''s activity history with their
  recent reviews, photos, and favorites"'
---

# AFTER: React Component Patterns Skill Test

## Test Prompt (Same as BEFORE)
"Create a new component to display a user's activity history with their recent reviews, photos, and favorites"

## New State
- React patterns skill at `.claude/skills/react-patterns/SKILL.md`
- Covers: loading states, empty states, auth, Convex hooks, design classes
- Semantic triggers: "React", "component", "page", "UI"

## Expected Behavior With Skill

### Automatic Activation
Skill triggers on:
- Keywords: "component", "page", "React", "UI"
- File patterns: `src/client/**/*.tsx`
- Intent: Creating user interfaces

### Code Quality (Expected)

```typescript
import { useParams } from "react-router-dom";
import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import type { Id } from "../../../convex/_generated/dataModel";
import { useAuth } from "../hooks/useAuth";
import { Avatar, AvatarFallback, AvatarImage } from "../components/ui/avatar";

export function UserActivityPage() {
  const { userId } = useParams<{ userId: string }>();
  const { user: currentUser } = useAuth();

  const userIdTyped = userId as Id<"users"> | undefined;

  // Convex queries - real-time updates!
  const userData = useQuery(api.users.get, userIdTyped ? { id: userIdTyped } : "skip");
  const reviews = useQuery(api.reviews.listByUser, userIdTyped ? { userId: userIdTyped } : "skip");
  const favorites = useQuery(api.favorites.listByUser, userIdTyped ? { userId: userIdTyped } : "skip");
  const activity = useQuery(api.activity.listByUser, userIdTyped ? { userId: userIdTyped } : "skip");

  const loading = userData === undefined;
  const user = userData;

  // Loading state with skeleton UI
  if (loading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="h-8 w-48 skeleton rounded-lg" />
        <div className="rounded-2xl border border-border/50 bg-card p-8 space-y-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 skeleton rounded-full" />
            <div className="space-y-2">
              <div className="h-6 w-32 skeleton rounded-lg" />
              <div className="h-4 w-48 skeleton rounded-lg" />
            </div>
          </div>
        </div>
        <div className="rounded-2xl border border-border/50 bg-card p-6">
          <div className="h-6 w-24 skeleton rounded-lg mb-4" />
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-20 w-full skeleton rounded-xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Not found state
  if (!user) {
    return (
      <div className="max-w-md mx-auto text-center py-16">
        <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-destructive/10 flex items-center justify-center">
          <span className="text-3xl">😕</span>
        </div>
        <h1 className="font-display text-2xl font-semibold mb-2">User not found</h1>
        <p className="text-muted-foreground">This user doesn't exist.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* User Profile Header */}
      <div className="rounded-2xl border border-border/50 bg-card p-6 animate-fade-in-up">
        <div className="flex items-center gap-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src={user.avatarUrl ?? undefined} />
            <AvatarFallback className="text-xl">{user.name?.[0] ?? "?"}</AvatarFallback>
          </Avatar>
          <div>
            <h1 className="font-display text-2xl font-semibold">{user.name ?? "Anonymous"}</h1>
            <p className="text-muted-foreground">{user.email}</p>
          </div>
        </div>
      </div>

      {/* Activity Feed */}
      <section className="space-y-4">
        <h2 className="font-display text-xl font-semibold flex items-center gap-2">
          <span>📋</span> Recent Activity
        </h2>

        {!activity || activity.length === 0 ? (
          <div className="rounded-xl border border-dashed border-border bg-card/50 p-10 text-center">
            <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-secondary flex items-center justify-center">
              <span className="text-2xl">✨</span>
            </div>
            <p className="text-muted-foreground font-medium">No activity yet</p>
          </div>
        ) : (
          <div className="space-y-3">
            {activity.map((item, index) => (
              <div
                key={item._id}
                className="rounded-xl border border-border/50 bg-card p-4 card-hover animate-fade-in-up"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                {/* Activity item content */}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
```

## Improved Metrics

| Metric | Before | After |
|--------|--------|-------|
| Files read before writing | 2-3 | 0-1 (skill provides patterns) |
| Design system adherence | Medium | High |
| Loading/empty states | Variable | Guaranteed |
| Auth integration | May need reads | Documented in skill |
| Animation consistency | Low | High |

## Key Improvements

1. **Loading skeleton included by default** - Skill documents exact pattern
2. **Empty state pattern ready** - Copy-paste from skill
3. **Convex skip pattern documented** - No guessing
4. **Auth hooks documented** - hasMinRole pattern included
5. **Animation classes documented** - Staggered fade-in pattern
6. **Design tokens listed** - Proper class usage

## Notes
This documents the expected state AFTER implementing the React patterns skill.
