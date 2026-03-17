---
name: clerk-auth
description: Clerk authentication patterns and integration with Convex. Use when implementing sign-in/sign-out, protected routes, user profile sync, or role-based access control.
allowed-tools: Read, Grep, Glob
---

# Clerk Authentication Skill

## Overview

This skill provides patterns for integrating Clerk authentication with the RFP Discovery platform and Convex backend.

## Setup

### Install Dependencies

```bash
npm install @clerk/clerk-react convex
```

### Environment Variables

```env
# .env.local (client-side)
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
VITE_CONVEX_URL=https://your-project.convex.cloud

# Convex Dashboard (server-side)
CLERK_ISSUER_URL=https://your-clerk-domain.clerk.accounts.dev
```

### Clerk Dashboard Configuration

1. Create application at https://dashboard.clerk.com
2. Configure sign-in methods (Email, Google, GitHub)
3. Create JWT template for Convex:
   - Name: `convex`
   - Claims:
     ```json
     {
       "aud": "convex",
       "sub": "{{user.id}}",
       "name": "{{user.full_name}}",
       "email": "{{user.primary_email_address}}",
       "picture": "{{user.image_url}}"
     }
     ```

### Convex Auth Config

```typescript
// convex/auth.config.ts
export default {
  providers: [
    {
      domain: process.env.CLERK_ISSUER_URL,
      applicationID: "convex",
    },
  ],
};
```

## Provider Setup

### App Entry Point

```tsx
// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { ClerkProvider, useAuth } from "@clerk/clerk-react";
import { ConvexProviderWithClerk } from "convex/react-clerk";
import { ConvexReactClient } from "convex/react";
import App from "./App";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        <App />
      </ConvexProviderWithClerk>
    </ClerkProvider>
  </React.StrictMode>
);
```

## Authentication Components

### Sign In/Out Buttons

```tsx
// components/AuthButtons.tsx
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/clerk-react";

export function AuthButtons() {
  return (
    <div className="flex items-center gap-4">
      <SignedOut>
        <SignInButton mode="modal">
          <button className="px-4 py-2 text-sm text-muted-foreground hover:text-foreground">
            Sign In
          </button>
        </SignInButton>
        <SignUpButton mode="modal">
          <button className="px-4 py-2 text-sm bg-primary text-primary-foreground rounded-lg hover:bg-primary/90">
            Sign Up
          </button>
        </SignUpButton>
      </SignedOut>
      <SignedIn>
        <UserButton
          afterSignOutUrl="/"
          appearance={{
            elements: {
              avatarBox: "w-10 h-10",
            },
          }}
        />
      </SignedIn>
    </div>
  );
}
```

### Protected Route Component

```tsx
// components/ProtectedRoute.tsx
import { useAuth } from "@clerk/clerk-react";
import { Navigate, useLocation } from "react-router-dom";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: "admin" | "user";
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { isLoaded, isSignedIn } = useAuth();
  const location = useLocation();

  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (!isSignedIn) {
    return <Navigate to="/sign-in" state={{ from: location }} replace />;
  }

  // Role check would use Convex query here
  return <>{children}</>;
}
```

### Auth Guard (Simple)

```tsx
// components/AuthGuard.tsx
import { SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SignedIn>{children}</SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
}
```

## Convex Auth Patterns

### User Identity in Mutations

```typescript
// convex/pursuits.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const create = mutation({
  args: { rfpId: v.id("rfps") },
  handler: async (ctx, args) => {
    // Always check auth first
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) {
      throw new Error("Not authenticated");
    }

    return await ctx.db.insert("pursuits", {
      rfpId: args.rfpId,
      userId: identity.subject, // Clerk user ID
      userName: identity.name ?? "Unknown",
      userEmail: identity.email ?? "",
      status: "new",
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });
  },
});
```

### User Sync on First Sign-In

```typescript
// convex/users.ts
import { mutation, query } from "./_generated/server";

export const syncUser = mutation({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const existing = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (existing) {
      // Update existing user
      await ctx.db.patch(existing._id, {
        name: identity.name ?? existing.name,
        email: identity.email ?? existing.email,
        imageUrl: identity.pictureUrl,
        updatedAt: Date.now(),
      });
      return existing._id;
    }

    // Create new user with default role
    return await ctx.db.insert("users", {
      clerkId: identity.subject,
      name: identity.name ?? "",
      email: identity.email ?? "",
      imageUrl: identity.pictureUrl,
      role: "user", // Default role
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });
  },
});

export const getCurrentUser = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return null;

    return await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
  },
});
```

### Auth Helper Functions

```typescript
// convex/lib/auth.ts
import { QueryCtx, MutationCtx } from "../_generated/server";

export async function requireAuth(ctx: QueryCtx | MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new Error("Not authenticated");
  }
  return identity;
}

export async function requireAdmin(ctx: QueryCtx | MutationCtx) {
  const identity = await requireAuth(ctx);

  const user = await ctx.db
    .query("users")
    .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
    .first();

  if (!user || user.role !== "admin") {
    throw new Error("Admin access required");
  }

  return { identity, user };
}

export async function getOptionalUser(ctx: QueryCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) return null;

  return await ctx.db
    .query("users")
    .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
    .first();
}
```

### Admin-Only Mutation

```typescript
// convex/admin.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";
import { requireAdmin } from "./lib/auth";

export const deleteRfp = mutation({
  args: { rfpId: v.id("rfps") },
  handler: async (ctx, args) => {
    await requireAdmin(ctx); // Throws if not admin

    await ctx.db.delete(args.rfpId);
    return { success: true };
  },
});

export const updateUserRole = mutation({
  args: {
    userId: v.id("users"),
    role: v.string(),
  },
  handler: async (ctx, args) => {
    const { user: adminUser } = await requireAdmin(ctx);

    // Prevent self-demotion
    if (args.userId === adminUser._id) {
      throw new Error("Cannot change your own role");
    }

    await ctx.db.patch(args.userId, {
      role: args.role,
      updatedAt: Date.now(),
    });

    return { success: true };
  },
});
```

## React Hooks

### useCurrentUser Hook

```tsx
// hooks/useCurrentUser.ts
import { useQuery } from "convex/react";
import { useUser, useAuth } from "@clerk/clerk-react";
import { api } from "../convex/_generated/api";

export function useCurrentUser() {
  const { user: clerkUser, isLoaded: clerkLoaded } = useUser();
  const { isSignedIn } = useAuth();
  const convexUser = useQuery(
    api.users.getCurrentUser,
    isSignedIn ? {} : "skip"
  );

  return {
    clerkUser,
    convexUser,
    isLoaded: clerkLoaded && (convexUser !== undefined || !isSignedIn),
    isSignedIn: !!clerkUser,
    isAdmin: convexUser?.role === "admin",
    userId: convexUser?._id,
  };
}
```

### Auto-Sync User Hook

```tsx
// hooks/useSyncUser.ts
import { useEffect } from "react";
import { useMutation } from "convex/react";
import { useAuth } from "@clerk/clerk-react";
import { api } from "../convex/_generated/api";

export function useSyncUser() {
  const { isSignedIn, isLoaded } = useAuth();
  const syncUser = useMutation(api.users.syncUser);

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      syncUser().catch(console.error);
    }
  }, [isLoaded, isSignedIn, syncUser]);
}

// Use in App.tsx
function App() {
  useSyncUser(); // Syncs user on sign-in

  return <AppContent />;
}
```

## Header Integration

```tsx
// components/Header.tsx
import { AuthButtons } from "./AuthButtons";
import { useCurrentUser } from "../hooks/useCurrentUser";

export function Header() {
  const { convexUser, isAdmin, isLoaded } = useCurrentUser();

  return (
    <header className="flex items-center justify-between p-4 border-b border-border">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-bold">RFP Discovery</h1>
        {isAdmin && (
          <span className="px-2 py-1 text-xs bg-primary/20 text-primary rounded">
            Admin
          </span>
        )}
      </div>
      <div className="flex items-center gap-4">
        {isLoaded && convexUser && (
          <span className="text-sm text-muted-foreground">
            {convexUser.name}
          </span>
        )}
        <AuthButtons />
      </div>
    </header>
  );
}
```

## Role-Based UI

```tsx
// components/AdminSection.tsx
import { useCurrentUser } from "../hooks/useCurrentUser";

export function AdminSection({ children }: { children: React.ReactNode }) {
  const { isAdmin, isLoaded } = useCurrentUser();

  if (!isLoaded) return null;
  if (!isAdmin) return null;

  return <>{children}</>;
}

// Usage
function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Visible to all */}
      <RfpList />

      {/* Admin only */}
      <AdminSection>
        <AdminControls />
      </AdminSection>
    </div>
  );
}
```

## Common Patterns Summary

| Pattern | Use Case |
|---------|----------|
| `SignedIn` / `SignedOut` | Conditional rendering based on auth |
| `useAuth().isSignedIn` | Check auth state in hooks |
| `ctx.auth.getUserIdentity()` | Get user in Convex functions |
| `requireAuth(ctx)` | Throw if not authenticated |
| `requireAdmin(ctx)` | Throw if not admin |
| User sync mutation | Keep Convex user in sync with Clerk |
