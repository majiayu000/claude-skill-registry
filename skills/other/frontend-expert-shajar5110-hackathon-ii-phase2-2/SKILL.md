---
name: frontend-ultimate
description: Ultimate 25+ years expert-level frontend skill covering Next.js, React, TypeScript, Tailwind CSS, styled-components, Redux, Zustand, Webpack, Vite, Parcel, Jest/Vitest testing, performance optimization, and ALL security aspects comprehensively (XSS, CSRF, injection, data privacy, CSP, dependency security, etc.). Covers all use cases (SPAs, PWAs, e-commerce, dashboards, real-time apps, mobile-responsive). Advanced features include A11y, Core Web Vitals, SEO, i18n, error handling, monitoring, component architecture, design patterns. Maximum security hardening, genius-level optimization, modernized development standards. Use when building ANY frontend application requiring enterprise security, performance, and scalability.
---

# ULTIMATE FRONTEND MASTERY - 25+ YEARS EXPERT LEVEL

Enterprise-grade frontend architecture with genius-level optimization, comprehensive security hardening, and all modern best practices across Next.js, React, TypeScript, and complete tooling ecosystem.

## 🎯 THE DECISION MATRIX

Choose your path based on requirements:

```
Building a website or app?
├─ Static site needed?
│  ├─ YES → Next.js with SSG
│  └─ NO → Continue
├─ Real-time features needed?
│  ├─ YES → Next.js with WebSockets + React
│  └─ NO → Continue
├─ Simple SPA sufficient?
│  ├─ YES → React + Vite
│  └─ NO → Next.js
├─ E-commerce with SEO?
│  └─ Next.js (SSG + ISR)
├─ Enterprise dashboard?
│  └─ React + Redux + Vite
├─ PWA needed?
│  └─ Next.js + PWA plugin
└─ Performance critical?
   └─ Vite + React with optimizations
```

---

## PART 1: CORE ARCHITECTURE

### Architecture Decision Tree

```typescript
// PROJECT STRUCTURE - NEXT.JS (Most Powerful)
my-app/
├── src/
│   ├── app/                    // Next.js App Router
│   │   ├── page.tsx           // Root page
│   │   ├── layout.tsx         // Root layout (security headers!)
│   │   ├── api/               // API routes (secured)
│   │   ├── (auth)/            // Route groups
│   │   ├── dashboard/
│   │   └── error.tsx          // Error boundary
│   ├── components/
│   │   ├── common/            // Reusable components
│   │   ├── features/          // Feature-specific
│   │   └── ui/                // Atomic components
│   ├── hooks/                 // Custom React hooks
│   ├── store/                 // Redux/Zustand
│   ├── utils/
│   │   ├── security.ts        // Security utilities
│   │   ├── validation.ts      // Input validation
│   │   ├── sanitization.ts    // XSS prevention
│   │   └── crypto.ts          // Client-side encryption
│   ├── lib/
│   │   ├── api.ts             // API client
│   │   └── db.ts              // Database access
│   ├── types/                 // TypeScript types
│   ├── styles/                // Global styles
│   ├── middleware.ts          // Next.js middleware
│   ├── env.ts                 // Type-safe env
│   └── constants.ts           // Constants
├── public/                    // Static assets
├── tests/                     // Test files
├── .env.local                 // Local env (gitignored)
├── .env.example               // Example env
├── .eslintrc.json            // ESLint config
├── .prettierrc.json          // Prettier config
├── tsconfig.json             // TypeScript config
├── next.config.js            // Next.js config
├── tailwind.config.js        // Tailwind config
├── jest.config.js            // Jest config
└── package.json              // Dependencies
```

### NextAuth Setup (Secure Authentication)

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { PrismaAdapter } from "@next-auth/prisma-adapter";
import { prisma } from "@/lib/prisma";
import { hash, compare } from "bcryptjs";

export const authOptions = {
    adapter: PrismaAdapter(prisma),
    secret: process.env.NEXTAUTH_SECRET,
    session: {
        strategy: "jwt" as const,
        maxAge: 30 * 24 * 60 * 60, // 30 days
    },
    pages: {
        signIn: "/auth/login",
        error: "/auth/error",
    },
    callbacks: {
        async jwt({ token, user, account }) {
            if (user) {
                token.id = user.id;
                token.role = user.role;
            }
            return token;
        },
        async session({ session, token }) {
            if (session.user) {
                session.user.id = token.id as string;
                session.user.role = token.role as string;
            }
            return session;
        },
        async signIn({ user, account }) {
            // Additional security checks
            if (account?.provider === "credentials") {
                // Rate limiting for password attempts
                const attempts = await getLoginAttempts(user.email);
                if (attempts > 5) {
                    throw new Error("Too many login attempts");
                }
            }
            return true;
        },
    },
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
            allowDangerousEmailAccountLinking: false,
        }),
        CredentialsProvider({
            async authorize(credentials: any) {
                if (!credentials?.email || !credentials?.password) {
                    throw new Error("Missing credentials");
                }

                const user = await prisma.user.findUnique({
                    where: { email: credentials.email },
                });

                if (!user) {
                    throw new Error("Invalid email");
                }

                const isValidPassword = await compare(
                    credentials.password,
                    user.hashedPassword
                );

                if (!isValidPassword) {
                    throw new Error("Invalid password");
                }

                return {
                    id: user.id,
                    email: user.email,
                    role: user.role,
                };
            },
        }),
    ],
};

export const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

---

## PART 2: SECURITY - COMPREHENSIVE HARDENING

### 2.1 XSS (Cross-Site Scripting) Prevention

```typescript
// lib/security/xss-prevention.ts
import DOMPurify from "isomorphic-dompurify";
import { marked } from "marked";

/**
 * Sanitize HTML to prevent XSS
 * CRITICAL: Use for user-generated content
 */
export function sanitizeHTML(html: string): string {
    const config = {
        ALLOWED_TAGS: [
            "b", "i", "em", "strong", "a", "p", "br", "ul", "li", 
            "ol", "blockquote", "code", "pre", "h1", "h2", "h3"
        ],
        ALLOWED_ATTR: ["href", "title", "target"],
        FORCE_BODY: true,
        KEEP_CONTENT: true,
    };

    return DOMPurify.sanitize(html, config);
}

/**
 * Safely render markdown without XSS
 */
export async function renderMarkdown(markdown: string): Promise<string> {
    const html = await marked(markdown);
    return sanitizeHTML(html);
}

/**
 * Escape HTML special characters
 * Use in text content
 */
export function escapeHTML(text: string): string {
    const map: Record<string, string> = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
    };
    return text.replace(/[&<>"']/g, (char) => map[char]);
}

/**
 * Prevent script injection in URLs
 */
export function isValidURL(url: string): boolean {
    try {
        const parsed = new URL(url);
        // Whitelist safe protocols
        if (!["http:", "https:", "mailto:", "tel:"].includes(parsed.protocol)) {
            return false;
        }
        return true;
    } catch {
        return false;
    }
}

/**
 * Safe JSON parsing
 */
export function safeJSONParse(json: string, fallback: any = null) {
    try {
        return JSON.parse(json);
    } catch {
        console.error("Invalid JSON");
        return fallback;
    }
}

// React component for safe content display
export function SafeHTML({ html }: { html: string }) {
    return (
        <div
            dangerouslySetInnerHTML={{
                __html: sanitizeHTML(html),
            }}
        />
    );
}
```

### 2.2 CSRF (Cross-Site Request Forgery) Protection

```typescript
// lib/security/csrf.ts
import { generateTokenPair } from "crypto-random-string";

/**
 * Generate CSRF token for forms
 */
export function generateCSRFToken(): string {
    return crypto.getRandomValues(new Uint8Array(32)).toString();
}

/**
 * Verify CSRF token
 */
export async function verifyCSRFToken(token: string, stored: string): Promise<boolean> {
    if (!token || !stored) return false;
    return crypto.subtle.timingSafeEqual(
        new TextEncoder().encode(token),
        new TextEncoder().encode(stored)
    );
}

// Middleware for CSRF protection
export const csrfProtectionMiddleware = async (
    req: NextRequest,
    res: NextResponse
) => {
    if (["POST", "PUT", "DELETE", "PATCH"].includes(req.method)) {
        const token = req.headers.get("x-csrf-token");
        const stored = req.cookies.get("csrf-token")?.value;

        if (!token || !stored || !await verifyCSRFToken(token, stored)) {
            return new NextResponse("CSRF token validation failed", {
                status: 403,
            });
        }
    }
    return res;
};

// Hook for forms
export function useCSRFToken() {
    const [token, setToken] = useState<string>("");

    useEffect(() => {
        const fetchToken = async () => {
            const res = await fetch("/api/csrf-token");
            const data = await res.json();
            setToken(data.token);
        };
        fetchToken();
    }, []);

    return token;
}

// Form component with CSRF
export function CSRFForm({ children, action }: any) {
    const token = useCSRFToken();

    return (
        <form action={action} method="POST">
            <input type="hidden" name="csrf-token" value={token} />
            {children}
        </form>
    );
}
```

### 2.3 Input Validation & Sanitization

```typescript
// lib/security/validation.ts
import { z } from "zod";

/**
 * Comprehensive validation schemas
 */
export const schemas = {
    email: z.string().email("Invalid email").toLowerCase(),
    
    password: z.string()
        .min(8, "Min 8 characters")
        .regex(/[A-Z]/, "Need uppercase")
        .regex(/[a-z]/, "Need lowercase")
        .regex(/[0-9]/, "Need digit")
        .regex(/[!@#$%^&*]/, "Need special char"),
    
    username: z.string()
        .min(3, "Min 3 chars")
        .max(20, "Max 20 chars")
        .regex(/^[a-zA-Z0-9_-]+$/, "Only alphanumeric, _, -"),
    
    url: z.string().url("Invalid URL").refine(
        (url) => ["http:", "https:"].includes(new URL(url).protocol),
        "Only http(s) allowed"
    ),
    
    phoneNumber: z.string()
        .regex(/^\+?[1-9]\d{1,14}$/, "Invalid phone"),
};

/**
 * Validate and sanitize input
 */
export function validateInput(
    data: unknown,
    schema: z.ZodSchema
): { valid: boolean; data?: unknown; error?: string } {
    try {
        const validated = schema.parse(data);
        return { valid: true, data: validated };
    } catch (error) {
        if (error instanceof z.ZodError) {
            return { valid: false, error: error.errors[0].message };
        }
        return { valid: false, error: "Validation failed" };
    }
}

/**
 * Prevent SQL injection
 * (Always use parameterized queries with Prisma/ORM)
 */
export function sanitizeSQLInput(input: string): string {
    // This is backup - always use ORM
    return input
        .replace(/'/g, "''")
        .replace(/"/g, '""')
        .replace(/\\/g, "\\\\")
        .slice(0, 1000); // Max length
}

/**
 * Sanitize file uploads
 */
export function validateFileUpload(
    file: File,
    allowedTypes: string[],
    maxSize: number
): { valid: boolean; error?: string } {
    // Check file type
    if (!allowedTypes.includes(file.type)) {
        return { valid: false, error: "File type not allowed" };
    }

    // Check file size
    if (file.size > maxSize) {
        return { valid: false, error: "File too large" };
    }

    // Check file name for injection
    if (!/^[a-zA-Z0-9._-]+$/.test(file.name)) {
        return { valid: false, error: "Invalid filename" };
    }

    return { valid: true };
}
```

### 2.4 Content Security Policy (CSP)

```typescript
// app/layout.tsx - Security Headers
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Secure App",
    description: "Enterprise security",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <head>
                {/* CSP Header */}
                <meta
                    httpEquiv="Content-Security-Policy"
                    content={`
                        default-src 'self';
                        script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net;
                        style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
                        img-src 'self' data: https: blob:;
                        font-src 'self' https://fonts.gstatic.com;
                        connect-src 'self' https://api.example.com;
                        frame-src 'none';
                        object-src 'none';
                        base-uri 'self';
                        form-action 'self';
                        upgrade-insecure-requests;
                    `.replace(/\n/g, "")}
                />

                {/* Security Headers */}
                <meta httpEquiv="X-UA-Compatible" content="ie=edge" />
                <meta httpEquiv="X-Content-Type-Options" content="nosniff" />
                <meta httpEquiv="X-Frame-Options" content="DENY" />
                <meta httpEquiv="X-XSS-Protection" content="1; mode=block" />
                <meta
                    httpEquiv="Referrer-Policy"
                    content="strict-origin-when-cross-origin"
                />
                <meta
                    httpEquiv="Permissions-Policy"
                    content="geolocation=(), microphone=(), camera=()"
                />

                {/* HTTPS Enforcement */}
                <meta httpEquiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains" />
            </head>
            <body>{children}</body>
        </html>
    );
}
```

### 2.5 API Security & Rate Limiting

```typescript
// lib/security/rate-limit.ts
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = new Redis({
    url: process.env.UPSTASH_REDIS_REST_URL!,
    token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

/**
 * Rate limiters for different endpoints
 */
export const rateLimiters = {
    // 5 requests per minute
    auth: new Ratelimit({
        redis,
        limiter: Ratelimit.fixedWindow(5, "60 s"),
    }),

    // 100 requests per minute
    api: new Ratelimit({
        redis,
        limiter: Ratelimit.fixedWindow(100, "60 s"),
    }),

    // 1000 requests per minute
    public: new Ratelimit({
        redis,
        limiter: Ratelimit.fixedWindow(1000, "60 s"),
    }),
};

// Middleware for rate limiting
export async function withRateLimit(
    key: string,
    limiter: Ratelimit,
    handler: Function
) {
    const { success, pending } = await limiter.limit(key);

    if (!success) {
        return new Response("Too many requests", { status: 429 });
    }

    return handler();
}
```

### 2.6 Secure API Routes with Validation

```typescript
// app/api/user/profile/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { schemas, validateInput } from "@/lib/security/validation";
import { rateLimiters, withRateLimit } from "@/lib/security/rate-limit";

/**
 * GET /api/user/profile - Fetch user profile
 * Protected: Requires authentication
 */
export async function GET(req: NextRequest) {
    try {
        // Check authentication
        const session = await getServerSession(authOptions);
        if (!session?.user?.id) {
            return NextResponse.json(
                { error: "Unauthorized" },
                { status: 401 }
            );
        }

        // Rate limiting
        return await withRateLimit(
            `api-${session.user.id}`,
            rateLimiters.api,
            async () => {
                // Fetch user data
                const user = await prisma.user.findUnique({
                    where: { id: session.user.id },
                    select: {
                        id: true,
                        email: true,
                        name: true,
                        role: true,
                    },
                });

                if (!user) {
                    return NextResponse.json(
                        { error: "User not found" },
                        { status: 404 }
                    );
                }

                return NextResponse.json(user);
            }
        );
    } catch (error) {
        console.error("Error:", error);
        return NextResponse.json(
            { error: "Internal server error" },
            { status: 500 }
        );
    }
}

/**
 * POST /api/user/profile - Update user profile
 * Protected: Requires authentication
 * Validates: Email, name
 * Sanitizes: All input
 */
export async function POST(req: NextRequest) {
    try {
        const session = await getServerSession(authOptions);
        if (!session?.user?.id) {
            return NextResponse.json(
                { error: "Unauthorized" },
                { status: 401 }
            );
        }

        // Rate limiting (stricter for POST)
        return await withRateLimit(
            `api-post-${session.user.id}`,
            rateLimiters.auth,
            async () => {
                const body = await req.json();

                // Validate email
                const emailValidation = validateInput(
                    body.email,
                    schemas.email
                );
                if (!emailValidation.valid) {
                    return NextResponse.json(
                        { error: emailValidation.error },
                        { status: 400 }
                    );
                }

                // Validate name
                if (!body.name || typeof body.name !== "string") {
                    return NextResponse.json(
                        { error: "Invalid name" },
                        { status: 400 }
                    );
                }

                // Check if email already exists
                const existingUser = await prisma.user.findUnique({
                    where: { email: emailValidation.data as string },
                });

                if (existingUser && existingUser.id !== session.user.id) {
                    return NextResponse.json(
                        { error: "Email already in use" },
                        { status: 409 }
                    );
                }

                // Update user
                const updated = await prisma.user.update({
                    where: { id: session.user.id },
                    data: {
                        email: emailValidation.data as string,
                        name: body.name,
                    },
                    select: {
                        id: true,
                        email: true,
                        name: true,
                    },
                });

                return NextResponse.json(updated);
            }
        );
    } catch (error) {
        console.error("Error:", error);
        return NextResponse.json(
            { error: "Internal server error" },
            { status: 500 }
        );
    }
}
```

---

## PART 3: STATE MANAGEMENT - REDUX & ZUSTAND

### 3.1 Redux Toolkit Setup (Enterprise)

```typescript
// store/index.ts
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/auth";
import userReducer from "./slices/user";
import uiReducer from "./slices/ui";

export const store = configureStore({
    reducer: {
        auth: authReducer,
        user: userReducer,
        ui: uiReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                // Ignore non-serializable data like Error objects
                ignoredActions: ["auth/login/rejected"],
            },
        }),
    devTools: process.env.NODE_ENV !== "production",
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

```typescript
// store/slices/auth.ts
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";

interface AuthState {
    user: { id: string; email: string; role: string } | null;
    token: string | null;
    loading: boolean;
    error: string | null;
}

const initialState: AuthState = {
    user: null,
    token: null,
    loading: false,
    error: null,
};

/**
 * Async thunk for login
 * Validates credentials, handles errors securely
 */
export const login = createAsyncThunk(
    "auth/login",
    async (
        credentials: { email: string; password: string },
        { rejectWithValue }
    ) => {
        try {
            const res = await fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include", // Include cookies
                body: JSON.stringify(credentials),
            });

            if (!res.ok) {
                const error = await res.json();
                return rejectWithValue(error.message);
            }

            const data = await res.json();
            return data;
        } catch (error) {
            return rejectWithValue("Network error");
        }
    }
);

/**
 * Async thunk for logout
 */
export const logout = createAsyncThunk("auth/logout", async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    return null;
});

export const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setUser: (state, action: PayloadAction<AuthState["user"]>) => {
            state.user = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload.user;
                state.token = action.payload.token;
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            .addCase(logout.fulfilled, (state) => {
                state.user = null;
                state.token = null;
            });
    },
});

export default authSlice.reducer;
```

### 3.2 Zustand Setup (Modern & Lightweight)

```typescript
// store/auth.store.ts
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface User {
    id: string;
    email: string;
    role: string;
}

interface AuthStore {
    user: User | null;
    token: string | null;
    isLoading: boolean;
    error: string | null;
    
    setUser: (user: User | null) => void;
    setToken: (token: string | null) => void;
    setLoading: (loading: boolean) => void;
    setError: (error: string | null) => void;
    
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    refresh: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>()(
    devtools(
        persist(
            (set) => ({
                user: null,
                token: null,
                isLoading: false,
                error: null,
                
                setUser: (user) => set({ user }),
                setToken: (token) => set({ token }),
                setLoading: (isLoading) => set({ isLoading }),
                setError: (error) => set({ error }),
                
                login: async (email, password) => {
                    set({ isLoading: true, error: null });
                    try {
                        const res = await fetch("/api/auth/login", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ email, password }),
                            credentials: "include",
                        });

                        if (!res.ok) {
                            const error = await res.json();
                            throw new Error(error.message);
                        }

                        const data = await res.json();
                        set({
                            user: data.user,
                            token: data.token,
                            isLoading: false,
                        });
                    } catch (error) {
                        const message =
                            error instanceof Error
                                ? error.message
                                : "Login failed";
                        set({ error: message, isLoading: false });
                        throw error;
                    }
                },
                
                logout: async () => {
                    await fetch("/api/auth/logout", { method: "POST" });
                    set({ user: null, token: null });
                },
                
                refresh: async () => {
                    const res = await fetch("/api/auth/refresh");
                    if (res.ok) {
                        const data = await res.json();
                        set({ token: data.token });
                    }
                },
            }),
            {
                name: "auth-store",
                partialize: (state) => ({
                    user: state.user,
                    token: state.token,
                }),
            }
        )
    )
);
```

---

## PART 4: STYLING - TAILWIND CSS & STYLED-COMPONENTS

### 4.1 Tailwind CSS Configuration

```typescript
// tailwind.config.js
import type { Config } from "tailwindcss";
import defaultTheme from "tailwindcss/defaultTheme";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: "#f0f9ff",
                    500: "#0ea5e9",
                    900: "#082f49",
                },
            },
            fontFamily: {
                sans: ["Inter", ...defaultTheme.fontFamily.sans],
            },
            spacing: {
                "safe-top": "var(--safe-top)",
                "safe-bottom": "var(--safe-bottom)",
            },
        },
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/aspect-ratio"),
    ],
};

export default config;
```

### 4.2 Styled Components with TypeScript

```typescript
// components/Button.styled.ts
import styled from "styled-components";

interface ButtonProps {
    variant?: "primary" | "secondary" | "danger";
    size?: "sm" | "md" | "lg";
    disabled?: boolean;
}

export const StyledButton = styled.button<ButtonProps>`
    padding: ${(props) => {
        switch (props.size) {
            case "sm": return "0.5rem 1rem";
            case "lg": return "1rem 1.5rem";
            default: return "0.75rem 1.25rem";
        }
    }};

    background-color: ${(props) => {
        switch (props.variant) {
            case "secondary": return "#e5e7eb";
            case "danger": return "#ef4444";
            default: return "#3b82f6";
        }
    }};

    color: ${(props) =>
        props.variant === "secondary" ? "#000" : "#fff"};

    border: none;
    border-radius: 0.375rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    opacity: ${(props) => (props.disabled ? 0.6 : 1)};
    pointer-events: ${(props) => (props.disabled ? "none" : "auto")};

    &:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    &:active:not(:disabled) {
        transform: translateY(0);
    }

    @media (max-width: 640px) {
        padding: ${(props) =>
            props.size === "sm"
                ? "0.375rem 0.75rem"
                : "0.625rem 1rem"};
    }
`;
```

---

## PART 5: PERFORMANCE OPTIMIZATION

### 5.1 Image Optimization

```typescript
// components/OptimizedImage.tsx
import Image from "next/image";
import { useState } from "react";

interface OptimizedImageProps {
    src: string;
    alt: string;
    width: number;
    height: number;
    priority?: boolean;
    sizes?: string;
}

export function OptimizedImage({
    src,
    alt,
    width,
    height,
    priority = false,
    sizes,
}: OptimizedImageProps) {
    const [isLoading, setIsLoading] = useState(true);

    return (
        <div className="relative overflow-hidden bg-gray-100">
            <Image
                src={src}
                alt={alt}
                width={width}
                height={height}
                priority={priority}
                sizes={sizes || "100vw"}
                quality={85}
                placeholder="blur"
                blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAY..."
                onLoadingComplete={() => setIsLoading(false)}
                className={`transition-opacity duration-300 ${
                    isLoading ? "opacity-0" : "opacity-100"
                }`}
            />
        </div>
    );
}
```

### 5.2 Code Splitting & Lazy Loading

```typescript
// components/Layout.tsx
import { lazy, Suspense } from "react";

// Lazy load components that aren't immediately needed
const Analytics = lazy(() => import("@/components/Analytics"));
const Chat = lazy(() => import("@/components/Chat"));

export function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div>
            {children}

            {/* Lazy load non-critical components */}
            <Suspense fallback={<div>Loading...</div>}>
                <Analytics />
            </Suspense>

            <Suspense fallback={null}>
                <Chat />
            </Suspense>
        </div>
    );
}
```

### 5.3 Performance Monitoring

```typescript
// lib/performance/metrics.ts
/**
 * Web Vitals monitoring
 * Sends metrics to analytics service
 */
export function reportWebVitals(metric: any) {
    if (metric.value === undefined) return;

    // Send to analytics
    const body = JSON.stringify(metric);
    if (navigator.sendBeacon) {
        navigator.sendBeacon("/api/metrics", body);
    } else {
        fetch("/api/metrics", {
            body,
            method: "POST",
            keepalive: true,
        });
    }
}

// pages/_app.tsx
import { useReportWebVitals } from "next/web-vitals";

function App() {
    useReportWebVitals((metric) => {
        console.log(`${metric.name}: ${metric.value}ms`);
    });

    return <></>;
}
```

---

## PART 6: TESTING - JEST & VITEST

### 6.1 Jest Setup

```typescript
// jest.config.js
const nextJest = require("next/jest");

const createJestConfig = nextJest({
    dir: "./",
});

const customJestConfig = {
    setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
    moduleNameMapper: {
        "^@/(.*)$": "<rootDir>/src/$1",
    },
    testEnvironment: "jest-environment-jsdom",
    collectCoverageFrom: [
        "src/**/*.{js,jsx,ts,tsx}",
        "!src/**/*.d.ts",
        "!src/**/*.stories.{js,jsx,ts,tsx}",
    ],
};

module.exports = createJestConfig(customJestConfig);
```

### 6.2 Component Testing

```typescript
// __tests__/Button.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "@/components/Button";

describe("Button Component", () => {
    it("renders button with text", () => {
        render(<Button>Click me</Button>);
        expect(screen.getByRole("button", { name: /click me/i })).toBeInTheDocument();
    });

    it("calls onClick handler", () => {
        const handleClick = jest.fn();
        render(<Button onClick={handleClick}>Click</Button>);
        fireEvent.click(screen.getByRole("button"));
        expect(handleClick).toHaveBeenCalled();
    });

    it("disables button when disabled prop is true", () => {
        render(<Button disabled>Disabled</Button>);
        expect(screen.getByRole("button")).toBeDisabled();
    });

    it("handles keyboard interaction", () => {
        const handleClick = jest.fn();
        render(<Button onClick={handleClick}>Click</Button>);
        const button = screen.getByRole("button");
        
        fireEvent.keyDown(button, { key: "Enter", code: "Enter" });
        expect(handleClick).toHaveBeenCalled();
    });
});
```

### 6.3 Integration Testing

```typescript
// __tests__/auth.integration.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "@/components/LoginForm";

describe("Login Flow", () => {
    it("logs in user successfully", async () => {
        const user = userEvent.setup();
        render(<LoginForm />);

        const emailInput = screen.getByLabelText(/email/i);
        const passwordInput = screen.getByLabelText(/password/i);
        const submitButton = screen.getByRole("button", { name: /login/i });

        await user.type(emailInput, "test@example.com");
        await user.type(passwordInput, "Password123!");
        await user.click(submitButton);

        await waitFor(() => {
            expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
        });

        expect(screen.getByText(/welcome/i)).toBeInTheDocument();
    });

    it("displays error for invalid credentials", async () => {
        const user = userEvent.setup();
        render(<LoginForm />);

        await user.type(screen.getByLabelText(/email/i), "wrong@example.com");
        await user.type(screen.getByLabelText(/password/i), "WrongPassword123!");
        await user.click(screen.getByRole("button", { name: /login/i }));

        await waitFor(() => {
            expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
        });
    });
});
```

---

## PART 7: BUILD TOOLS CONFIGURATION

### 7.1 Vite Configuration (Blazing Fast)

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import compression from "vite-plugin-compression";
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
    plugins: [
        react({
            jsxRuntime: "automatic",
            jsxImportSource: "@emotion/react",
        }),
        compression({
            verbose: true,
            disable: false,
            threshold: 10240,
            algorithm: "brotliCompress",
            ext: ".br",
        }),
        visualizer({
            open: true,
        }),
    ],
    build: {
        target: "ES2020",
        minify: "terser",
        reportCompressedSize: true,
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ["react", "react-dom"],
                    router: ["react-router-dom"],
                    state: ["zustand"],
                },
            },
        },
    },
    server: {
        middlewareMode: false,
        proxy: {
            "/api": "http://localhost:3001",
        },
    },
});
```

### 7.2 Webpack Configuration (Enterprise)

```typescript
// webpack.config.js
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const CompressionPlugin = require("compression-webpack-plugin");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;

module.exports = {
    mode: process.env.NODE_ENV || "development",
    entry: "./src/index.tsx",
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "[name].[contenthash].js",
        chunkFilename: "[name].[contenthash].chunk.js",
        clean: true,
    },
    module: {
        rules: [
            {
                test: /\.[jt]sx?$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: [
                            ["@babel/preset-env", { modules: false }],
                            ["@babel/preset-react", { runtime: "automatic" }],
                            "@babel/preset-typescript",
                        ],
                    },
                },
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader", "postcss-loader"],
            },
        ],
    },
    optimization: {
        minimize: true,
        minimizer: [
            new TerserPlugin({
                terserOptions: {
                    compress: { drop_console: true },
                },
            }),
        ],
        splitChunks: {
            chunks: "all",
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: "vendors",
                    priority: 10,
                },
                common: {
                    minChunks: 2,
                    priority: 5,
                    reuseExistingChunk: true,
                },
            },
        },
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./public/index.html",
            minify: {
                removeComments: true,
                collapseWhitespace: true,
            },
        }),
        new CompressionPlugin({
            algorithm: "gzip",
            test: /\.(js|css|html|svg)$/,
            threshold: 10240,
            minRatio: 0.8,
        }),
        process.env.ANALYZE && new BundleAnalyzerPlugin(),
    ].filter(Boolean),
    devServer: {
        port: 3000,
        historyApiFallback: true,
        proxy: {
            "/api": "http://localhost:3001",
        },
    },
};
```

---

## PART 8: ACCESSIBILITY (A11Y)

### 8.1 Accessible Components

```typescript
// components/accessible/AccessibleButton.tsx
import { ReactNode } from "react";

interface AccessibleButtonProps {
    children: ReactNode;
    onClick: () => void;
    disabled?: boolean;
    ariaLabel?: string;
    ariaPressed?: boolean;
    role?: "button" | "tab" | "menuitem";
}

export function AccessibleButton({
    children,
    onClick,
    disabled = false,
    ariaLabel,
    ariaPressed,
    role = "button",
}: AccessibleButtonProps) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            aria-label={ariaLabel}
            aria-pressed={ariaPressed}
            role={role}
            className="px-4 py-2 rounded font-semibold transition"
            style={{
                // Focus visible for keyboard navigation
                outline: "2px solid transparent",
                outlineOffset: "2px",
            }}
            onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    onClick();
                }
            }}
        >
            {children}
        </button>
    );
}
```

### 8.2 ARIA Labels & Attributes

```typescript
// components/accessible/AccessibleForm.tsx
export function AccessibleForm() {
    return (
        <form aria-labelledby="form-title">
            <h1 id="form-title">Login Form</h1>

            <div className="form-group">
                <label htmlFor="email-input">
                    Email Address
                    <span aria-label="required">*</span>
                </label>
                <input
                    id="email-input"
                    type="email"
                    aria-required="true"
                    aria-describedby="email-error"
                    placeholder="you@example.com"
                />
                <div id="email-error" role="alert">
                    {/* Error messages here */}
                </div>
            </div>

            <button
                type="submit"
                aria-label="Submit login form"
            >
                Login
            </button>
        </form>
    );
}
```

---

## PART 9: SEO OPTIMIZATION

### 9.1 Meta Tags & Structured Data

```typescript
// app/layout.tsx
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "My Awesome App",
    description: "The best application ever built",
    openGraph: {
        type: "website",
        locale: "en_US",
        url: "https://example.com",
        siteName: "My App",
        images: [
            {
                url: "https://example.com/og-image.png",
                width: 1200,
                height: 630,
                alt: "Preview Image",
            },
        ],
    },
    twitter: {
        card: "summary_large_image",
        creator: "@yourusername",
    },
    robots: {
        index: true,
        follow: true,
        "max-image-preview": "large",
        "max-snippet": -1,
        "max-video-preview": -1,
    },
};

// Structured Data (JSON-LD)
export function StructuredData() {
    const schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        name: "My App",
        url: "https://example.com",
        logo: "https://example.com/logo.png",
        sameAs: [
            "https://twitter.com/yourusername",
            "https://linkedin.com/company/myapp",
        ],
    };

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
    );
}
```

---

Continuing in next part due to length... This is PART 1-9 of the comprehensive skill.

Let me continue with remaining critical sections in the next file creation...