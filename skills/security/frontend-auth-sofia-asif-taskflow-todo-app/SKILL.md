# Frontend Authentication Skill

**Purpose**: Guidance for implementing authentication flows using Better Auth and JWT token management.

## Overview

Authentication uses Better Auth library with JWT plugin enabled. JWT tokens are stored in localStorage and automatically attached to API requests. Session management handles token expiration and refresh.

## Better Auth Configuration

### Pattern from `frontend/lib/auth.ts`

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",

  // Session configuration
  session: {
    cookieName: "better-auth.session",
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // Update session every 24 hours
  },

  // Storage configuration (for client-side token management)
  storage: typeof window !== "undefined" ? localStorage : undefined,
});
```

**Pattern**:
- Use environment variable `NEXT_PUBLIC_BETTER_AUTH_URL` with fallback
- Session expires in 7 days
- Session updates every 24 hours
- Use localStorage for client-side storage
- Check for `window` before accessing localStorage

## Authentication Functions

### 1. Sign Up

```typescript
export async function signUp(email: string, password: string, name: string) {
  try {
    const response = await authClient.signUp.email({
      email,
      password,
      name,
    });

    return response;
  } catch (error: any) {
    throw new Error(error.message || "Signup failed");
  }
}
```

**Pattern**:
- Use `authClient.signUp.email()` method
- Pass email, password, and name
- Handle errors with try-catch
- Throw user-friendly error messages

### 2. Sign In

```typescript
export async function signIn(email: string, password: string) {
  try {
    const response = await authClient.signIn.email({
      email,
      password,
    });

    return response;
  } catch (error: any) {
    throw new Error(error.message || "Signin failed");
  }
}
```

**Pattern**:
- Use `authClient.signIn.email()` method
- Pass email and password
- Handle errors with try-catch

### 3. Sign Out

```typescript
export async function signOut() {
  try {
    await authClient.signOut();

    // Clear auth token from localStorage
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
    }
  } catch (error) {
    console.error("Signout error:", error);
    throw error;
  }
}
```

**Pattern**:
- Call `authClient.signOut()`
- Remove token from localStorage
- Check for `window` before accessing localStorage

### 4. Check Authentication

```typescript
export async function isAuthenticated(): Promise<boolean> {
  const session = await getSession();
  return session !== null && session.user !== null;
}
```

**Pattern**:
- Get session using `getSession()`
- Check if session and user exist
- Return boolean

### 5. Get Current User

```typescript
export async function getCurrentUser() {
  const session = await getSession();
  return session?.user || null;
}
```

**Pattern**:
- Get session using `getSession()`
- Return user from session or null

### 6. Get Session

```typescript
export async function getSession() {
  try {
    const session = await authClient.getSession();
    return session;
  } catch (error) {
    console.error("Failed to get session:", error);
    return null;
  }
}
```

**Pattern**:
- Use `authClient.getSession()`
- Handle errors gracefully
- Return null on error

## JWT Token Management (from `frontend/lib/api.ts`)

### 1. Token Storage After Successful Auth

```typescript
async signup(userData: UserSignupData): Promise<ApiResponse<AuthResponse>> {
  const response = await apiFetch<AuthResponse>("/api/auth/signup", {
    method: "POST",
    body: JSON.stringify(userData),
  });

  // Store token if signup successful
  if (response.success && response.data?.token) {
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", response.data.token);
    }
  }

  return response;
}
```

**Pattern**:
- Check `response.success` and `response.data?.token`
- Store token in localStorage with key `"auth_token"`
- Check for `window` before accessing localStorage

### 2. Token Retrieval

```typescript
const getAuthToken = (): string | null => {
  if (typeof window === "undefined") return null;
  const token = localStorage.getItem("auth_token");
  return token;
};
```

**Pattern**:
- Check for `window` to ensure client-side
- Retrieve token from localStorage
- Return null if token doesn't exist

### 3. Token Attachment to API Requests

```typescript
const headers: HeadersInit = {
  "Content-Type": "application/json",
  ...options.headers,
};

// Attach JWT token if available
if (token) {
  headers["Authorization"] = `Bearer ${token}`;
}
```

**Pattern**:
- Get token using `getAuthToken()`
- Add `Authorization: Bearer ${token}` header if token exists
- Use in all API requests

### 4. Token Removal on Signout

```typescript
async signout(): Promise<ApiResponse<void>> {
  const response = await apiFetch<void>("/api/auth/signout", {
    method: "POST",
  });

  // Remove token on signout
  if (typeof window !== "undefined") {
    localStorage.removeItem("auth_token");
  }

  return response;
}
```

**Pattern**:
- Remove token from localStorage on signout
- Check for `window` before accessing localStorage

### 5. 401 Error Handling

```typescript
const handleApiError = (error: any, statusCode?: number): never => {
  // Redirect to login on 401 Unauthorized
  if (statusCode === 401) {
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
      window.location.href = "/signin";
    }
  }

  throw {
    message: error.message || "An error occurred",
    code: error.code || "UNKNOWN_ERROR",
    statusCode: statusCode || 500,
  };
};
```

**Pattern**:
- Check for 401 status code
- Remove token from localStorage
- Redirect to `/signin` page
- Throw structured error

## Protected Route Pattern

**From**: `frontend/components/ProtectedRoute.tsx`

```typescript
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";
import LoadingSpinner from "./LoadingSpinner";

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter();
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    async function checkAuth() {
      try {
        const authenticated = await isAuthenticated();

        if (!authenticated) {
          // Store the intended destination for redirect after login
          const currentPath = window.location.pathname;
          if (currentPath !== "/signin") {
            sessionStorage.setItem("redirectAfterLogin", currentPath);
          }

          router.push("/signin");
        } else {
          setIsAuthorized(true);
        }
      } catch (error) {
        console.error("Auth check failed:", error);
        router.push("/signin");
      } finally {
        setIsChecking(false);
      }
    }

    checkAuth();
  }, [router]);

  if (isChecking) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  if (!isAuthorized) {
    return null;
  }

  return <>{children}</>;
}
```

**Pattern**:
- Check authentication on mount
- Show loading spinner during check
- Store intended destination in `sessionStorage` with key `"redirectAfterLogin"`
- Redirect to `/signin` if not authenticated
- Only render children if authorized

## Form Validation Pattern

**From**: `frontend/app/signup/page.tsx`

### Email Validation

```typescript
import { isValidEmail } from "@/lib/utils";

if (!formData.email.trim()) {
  errors.email = "Email is required";
} else if (!isValidEmail(formData.email)) {
  errors.email = "Please enter a valid email address";
}
```

**Pattern**:
- Use `isValidEmail()` utility from `@/lib/utils`
- Check for empty email
- Validate email format

### Password Validation

```typescript
import { getPasswordStrength } from "@/lib/utils";

const { strength, message } = getPasswordStrength(formData.password);
if (strength === "weak") {
  errors.password = message || "Password is too weak";
}
```

**Pattern**:
- Use `getPasswordStrength()` utility
- Check password strength
- Show strength message to user

### Form Submission with Auth

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setApiError("");

  if (!validateForm()) {
    return;
  }

  setIsLoading(true);

  try {
    const response = await api.signup({
      name: formData.name.trim(),
      email: formData.email.trim().toLowerCase(),
      password: formData.password,
    });

    if (response.success) {
      // Redirect to dashboard or intended destination
      const redirectPath = sessionStorage.getItem("redirectAfterLogin") || "/dashboard";
      sessionStorage.removeItem("redirectAfterLogin");
      router.push(redirectPath);
    } else {
      setApiError(response.message || "Signup failed");
    }
  } catch (error: any) {
    setApiError(error.message || "An error occurred");
  } finally {
    setIsLoading(false);
  }
};
```

**Pattern**:
- Validate form before submission
- Call API method (`api.signup()` or `api.signin()`)
- Check `response.success`
- Redirect to intended destination or dashboard
- Handle errors with user-friendly messages

## Constitution Requirements

- **FR-001**: User account creation ✅
- **FR-002**: User authentication with JWT ✅
- **FR-026**: Better Auth with JWT plugin ✅
- **FR-028**: Auto-attach JWT token ✅
- **FR-029**: Handle 401 errors ✅

## MCP Server Usage

- **Better Auth MCP Server**: Use for Better Auth configuration patterns and best practices

## References

- **Specification**: `specs/002-frontend-todo-app/spec.md` - Authentication requirements
- **Better Auth Config**: `frontend/lib/auth.ts` - Better Auth implementation
- **API Client**: `frontend/lib/api.ts` - JWT token handling
- **Protected Route**: `frontend/components/ProtectedRoute.tsx` - Protected route pattern
- **Signup Page**: `frontend/app/signup/page.tsx` - Signup form pattern
- **Signin Page**: `frontend/app/signin/page.tsx` - Signin form pattern

## Common Patterns Summary

1. ✅ Use Better Auth `createAuthClient()` for configuration
2. ✅ Store JWT token in localStorage with key `"auth_token"`
3. ✅ Attach token to API requests via `Authorization: Bearer ${token}` header
4. ✅ Remove token on signout
5. ✅ Handle 401 errors with redirect to `/signin`
6. ✅ Check authentication before rendering protected routes
7. ✅ Store intended destination in sessionStorage for redirect after login
8. ✅ Validate email with `isValidEmail()` utility
9. ✅ Validate password with `getPasswordStrength()` utility
10. ✅ Always check for `window` before accessing localStorage

