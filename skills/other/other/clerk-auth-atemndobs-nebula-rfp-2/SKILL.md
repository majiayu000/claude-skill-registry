---
name: Clerk Authentication
description: Guidelines for integrating Clerk authentication into the RFP Discovery application with Convex
---

# Clerk Authentication Skill

This skill provides guidance for integrating Clerk as the authentication provider for the RFP Discovery application.

## Installation

```bash
npm install @clerk/clerk-react
```

## Environment Setup

Create environment variables:

```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
CLERK_SECRET_KEY=sk_test_xxxxx
```

## Provider Setup

Wrap your app in the Clerk provider (`index.tsx`):

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ClerkProvider } from '@clerk/clerk-react';
import App from './App';

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Publishable Key");
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <App />
    </ClerkProvider>
  </React.StrictMode>
);
```

## Integration with Convex

When using both Clerk and Convex, set up providers together:

```tsx
import { ClerkProvider, useAuth } from '@clerk/clerk-react';
import { ConvexProviderWithClerk } from 'convex/react-clerk';
import { ConvexReactClient } from 'convex/react';

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

function App() {
  return (
    <ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        <MainApp />
      </ConvexProviderWithClerk>
    </ClerkProvider>
  );
}
```

## Authentication Components

### Sign In/Sign Up Buttons

```tsx
import { SignInButton, SignUpButton, SignedIn, SignedOut, UserButton } from '@clerk/clerk-react';

function Header() {
  return (
    <header>
      <SignedOut>
        <SignInButton mode="modal" />
        <SignUpButton mode="modal" />
      </SignedOut>
      <SignedIn>
        <UserButton afterSignOutUrl="/" />
      </SignedIn>
    </header>
  );
}
```

### Protected Content

```tsx
import { SignedIn, SignedOut, RedirectToSignIn } from '@clerk/clerk-react';

function ProtectedPage() {
  return (
    <>
      <SignedIn>
        <AdminView />
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
}
```

## User Hooks

### Get Current User

```tsx
import { useUser, useAuth } from '@clerk/clerk-react';

function UserProfile() {
  const { user, isLoaded, isSignedIn } = useUser();
  const { userId, getToken } = useAuth();
  
  if (!isLoaded) return <div>Loading...</div>;
  if (!isSignedIn) return <div>Not signed in</div>;
  
  return (
    <div>
      <p>Welcome, {user.firstName}!</p>
      <p>Email: {user.primaryEmailAddress?.emailAddress}</p>
    </div>
  );
}
```

## Protected Routes Pattern

For this single-page app, protect specific views rather than routes:

```tsx
function App() {
  const [view, setView] = useState<'home' | 'rawData' | 'admin'>('home');
  const { isSignedIn, isLoaded } = useUser();
  
  // Redirect to sign-in for admin view if not authenticated
  if (view === 'admin' && isLoaded && !isSignedIn) {
    return <RedirectToSignIn />;
  }
  
  return (
    <>
      <ViewSwitcher currentView={view} onSwitchView={setView} />
      {view === 'home' && <HomeView />}
      {view === 'rawData' && <RawDataView />}
      {view === 'admin' && <AdminView />}
    </>
  );
}
```

## Access Control Patterns

### Admin-Only Features

```tsx
import { useUser } from '@clerk/clerk-react';

function AdminFeature() {
  const { user } = useUser();
  
  // Check for admin role (configure in Clerk Dashboard)
  const isAdmin = user?.publicMetadata?.role === 'admin';
  
  if (!isAdmin) {
    return <p>You don't have permission to access this feature.</p>;
  }
  
  return <AdminPanel />;
}
```

### Organization-Based Access

For multi-tenant scenarios (future consideration):

```tsx
import { useOrganization } from '@clerk/clerk-react';

function TeamDashboard() {
  const { organization } = useOrganization();
  
  if (!organization) {
    return <p>Please select a team.</p>;
  }
  
  return <Dashboard orgId={organization.id} />;
}
```

## Session Token for API Calls

When calling the FastAPI backend with auth:

```tsx
import { useAuth } from '@clerk/clerk-react';

function useAuthenticatedFetch() {
  const { getToken } = useAuth();
  
  const fetchWithAuth = async (url: string, options?: RequestInit) => {
    const token = await getToken();
    
    return fetch(url, {
      ...options,
      headers: {
        ...options?.headers,
        Authorization: `Bearer ${token}`,
      },
    });
  };
  
  return fetchWithAuth;
}
```

## Migration Strategy

### Phase 1: Add Clerk (Optional Auth)
1. Install Clerk packages
2. Add ClerkProvider wrapper
3. Add SignIn/SignUp buttons to header
4. Show UserButton when signed in
5. Continue allowing unauthenticated access to main features

### Phase 2: Protect Admin Features
1. Require authentication for Admin view
2. Store user preferences in Convex tied to userId
3. Add user-specific evaluation history

### Phase 3: Full Authentication
1. Require authentication for all features
2. Migrate localStorage settings to Convex per-user
3. Add organization/team support for shared access

## Styling Integration

Clerk components can be customized via the `appearance` prop:

```tsx
<ClerkProvider
  publishableKey={PUBLISHABLE_KEY}
  appearance={{
    elements: {
      formButtonPrimary: {
        backgroundColor: '#6366f1',
        '&:hover': { backgroundColor: '#4f46e5' },
      },
    },
    variables: {
      colorPrimary: '#6366f1',
    },
  }}
>
```
