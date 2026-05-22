---
name: authjs-skills
description: Auth.js v5 setup for Next.js authentication including Google OAuth, credentials provider, environment configuration, and core API integration
---

## Links

- Getting Started: https://authjs.dev/getting-started/installation?framework=Next.js
- Migrating to v5: https://authjs.dev/getting-started/migrating-to-v5
- Google Provider: https://authjs.dev/getting-started/providers/google
- Credentials Provider: https://authjs.dev/getting-started/providers/credentials
- Core API Reference: https://authjs.dev/reference/core
- Session Management: https://authjs.dev/getting-started/session-management
- Concepts: https://authjs.dev/concepts

## Installation

```sh
pnpm add next-auth@beta
```

**Note**: Auth.js v5 is currently in beta. Use `next-auth@beta` to install the latest v5 version.

## What's New in Auth.js v5?

### Key Changes from v4

- **Simplified Configuration**: More streamlined setup with better TypeScript support
- **Universal `auth()` Export**: Single function for authentication across all contexts
- **Enhanced Security**: Improved CSRF protection and session handling
- **Edge Runtime Support**: Full compatibility with Edge Runtime and middleware
- **Better Type Safety**: Improved TypeScript definitions throughout

## Environment Variables

### Required Environment Variables

```env
# Auth.js Configuration
AUTH_SECRET=your_secret_key_here

# Google OAuth (if using Google provider)
AUTH_GOOGLE_ID=your_google_client_id
AUTH_GOOGLE_SECRET=your_google_client_secret

# For production deployments
AUTH_URL=https://yourdomain.com

# For development (optional, defaults to http://localhost:3000)
# AUTH_URL=http://localhost:3000
```

### Generating AUTH_SECRET

```sh
# Generate a random secret (Unix/Linux/macOS)
openssl rand -base64 32

# Alternative using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# Using pnpm
pnpm dlx auth secret
```

**Important**: Never commit `AUTH_SECRET` to version control. Use `.env.local` for development.

## Basic Setup (Next.js App Router)

### 1. Create `auth.ts` Configuration File

Create `auth.ts` at the project root (next to `package.json`):

```typescript
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import Credentials from "next-auth/providers/credentials"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
    Credentials({
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      authorize: async (credentials) => {
        // TODO: Implement your authentication logic here
        // This is a basic example - see Credentials Provider section below for complete implementation
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        // Example: validate against database (placeholder)
        // See "Credentials Provider" section for full implementation with bcrypt
        const user = { id: "1", email: credentials.email, name: "User" } // Replace with actual DB lookup
        
        if (!user) {
          return null
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
        }
      },
    }),
  ],
  pages: {
    signIn: '/auth/signin',
  },
  callbacks: {
    authorized: async ({ auth }) => {
      // Return true if user is authenticated
      return !!auth
    },
  },
})
```

**Note**: This is a basic setup example. For production-ready credentials authentication, see the "Credentials Provider" section below which includes proper password hashing with bcrypt and database integration.

### 2. Create API Route Handler

Create `app/api/auth/[...nextauth]/route.ts`:

```typescript
import { handlers } from "@/auth"

export const { GET, POST } = handlers
```

### 3. Add Middleware (Optional but Recommended)

Create `middleware.ts` at the project root:

```typescript
export { auth as middleware } from "@/auth"

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
```

For more control:

```typescript
import { auth } from "@/auth"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard')
  
  if (isOnDashboard && !isLoggedIn) {
    return Response.redirect(new URL('/auth/signin', req.url))
  }
})

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*'],
}
```

## Google OAuth Provider

### 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs:
     - Development: `http://localhost:3000/api/auth/callback/google`
     - Production: `https://yourdomain.com/api/auth/callback/google`
5. Copy Client ID and Client Secret to `.env.local`

### 2. Configuration

```typescript
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code"
        }
      }
    }),
  ],
})
```

### 3. Google Provider Options

```typescript
Google({
  clientId: process.env.AUTH_GOOGLE_ID,
  clientSecret: process.env.AUTH_GOOGLE_SECRET,
  // Request additional scopes
  authorization: {
    params: {
      scope: "openid email profile",
      prompt: "select_account", // Force account selection
    }
  },
  // Allow specific domains only
  allowDangerousEmailAccountLinking: false,
})
```

## Credentials Provider (Username/Password)

### Required Dependencies

```sh
# Install required packages for credentials provider
pnpm add bcryptjs zod
pnpm add -D @types/bcryptjs
```

### 1. Basic Configuration

```typescript
import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import { z } from "zod"
import bcrypt from "bcryptjs"
import { prisma } from "@/lib/prisma"

const credentialsSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      credentials: {
        email: { label: "Email", type: "email", placeholder: "user@example.com" },
        password: { label: "Password", type: "password" },
      },
      authorize: async (credentials) => {
        try {
          const { email, password } = credentialsSchema.parse(credentials)
          
          // Fetch user from database
          const user = await prisma.user.findUnique({
            where: { email },
          })

          if (!user) {
            throw new Error("User not found")
          }

          // Verify password
          const isValidPassword = await bcrypt.compare(password, user.hashedPassword)
          
          if (!isValidPassword) {
            throw new Error("Invalid password")
          }

          // Return user object (must include id)
          return {
            id: user.id,
            email: user.email,
            name: user.name,
            image: user.image,
          }
        } catch (error) {
          console.error("Authentication error:", error)
          return null
        }
      },
    }),
  ],
  session: {
    strategy: "jwt", // Required for credentials provider
  },
})
```

### 2. User Registration Example

```typescript
// app/api/auth/register/route.ts
import { NextResponse } from "next/server"
import bcrypt from "bcryptjs"
import { z } from "zod"
import { prisma } from "@/lib/prisma"

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2),
})

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const { email, password, name } = registerSchema.parse(body)

    // Check if user exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    })

    if (existingUser) {
      return NextResponse.json(
        { error: "User already exists" },
        { status: 400 }
      )
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10)

    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        name,
        hashedPassword,
      },
    })

    return NextResponse.json(
      { message: "User created successfully", userId: user.id },
      { status: 201 }
    )
  } catch (error) {
    console.error("Registration error:", error)
    return NextResponse.json(
      { error: "Failed to register user" },
      { status: 500 }
    )
  }
}
```

## Using Auth in Components

### Server Components

```typescript
import { auth } from "@/auth"

export default async function ProfilePage() {
  const session = await auth()

  if (!session?.user) {
    return <div>Not authenticated</div>
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>Email: {session.user.email}</p>
    </div>
  )
}
```

### Server Actions

```typescript
"use server"

import { auth } from "@/auth"
import { revalidatePath } from "next/cache"
import { prisma } from "@/lib/prisma"

export async function updateProfile(formData: FormData) {
  const session = await auth()

  if (!session?.user) {
    throw new Error("Not authenticated")
  }

  const name = formData.get("name") as string

  // Update database
  await prisma.user.update({
    where: { id: session.user.id },
    data: { name },
  })

  revalidatePath("/profile")
}
```

### Client Components (with SessionProvider)

```typescript
// app/providers.tsx
"use client"

import { SessionProvider } from "next-auth/react"

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>
}
```

```typescript
// app/layout.tsx
import { Providers } from "./providers"

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

```typescript
// app/components/user-profile.tsx
"use client"

import { useSession, signIn, signOut } from "next-auth/react"

export function UserProfile() {
  const { data: session, status } = useSession()

  if (status === "loading") {
    return <div>Loading...</div>
  }

  if (!session) {
    return (
      <button onClick={() => signIn()}>
        Sign In
      </button>
    )
  }

  return (
    <div>
      <p>Signed in as {session.user?.email}</p>
      <button onClick={() => signOut()}>
        Sign Out
      </button>
    </div>
  )
}
```

## Sign In/Out Actions

### Programmatic Sign In

```typescript
import { signIn } from "@/auth"

// Server Action
export async function handleSignIn(provider: string) {
  "use server"
  await signIn(provider)
}

// With credentials
export async function handleCredentialsSignIn(formData: FormData) {
  "use server"
  await signIn("credentials", formData)
}

// With redirect
export async function handleGoogleSignIn() {
  "use server"
  await signIn("google", { redirectTo: "/dashboard" })
}
```

### Sign In Form Component

```typescript
// app/auth/signin/page.tsx
import { signIn } from "@/auth"

export default function SignInPage() {
  return (
    <div>
      <h1>Sign In</h1>
      
      {/* Google OAuth */}
      <form
        action={async () => {
          "use server"
          await signIn("google")
        }}
      >
        <button type="submit">Sign in with Google</button>
      </form>

      {/* Credentials */}
      <form
        action={async (formData) => {
          "use server"
          await signIn("credentials", formData)
        }}
      >
        <input name="email" type="email" placeholder="Email" required />
        <input name="password" type="password" placeholder="Password" required />
        <button type="submit">Sign In</button>
      </form>
    </div>
  )
}
```

### Sign Out

```typescript
import { signOut } from "@/auth"

export default function SignOutButton() {
  return (
    <form
      action={async () => {
        "use server"
        await signOut()
      }}
    >
      <button type="submit">Sign Out</button>
    </form>
  )
}
```

## Session Management

### Session Strategy

Auth.js v5 supports two session strategies:

1. **JWT (Default)**: Stores session in encrypted JWT token
2. **Database**: Stores session in database

```typescript
export const { handlers, signIn, signOut, auth } = NextAuth({
  session: {
    strategy: "jwt", // or "database"
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
})
```

### Extending the Session

```typescript
import NextAuth from "next-auth"
import type { DefaultSession } from "next-auth"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      role: string
    } & DefaultSession["user"]
  }
}

export const { handlers, signIn, signOut, auth } = NextAuth({
  callbacks: {
    jwt({ token, user }) {
      if (user) {
        token.id = user.id
        token.role = user.role
      }
      return token
    },
    session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
        session.user.role = token.role as string
      }
      return session
    },
  },
})
```

## Callbacks

### Essential Callbacks

```typescript
export const { handlers, signIn, signOut, auth } = NextAuth({
  callbacks: {
    // Called when user signs in
    async signIn({ user, account, profile }) {
      // Return true to allow sign in, false to deny
      // Example: Check if email is verified
      if (account?.provider === "google") {
        return profile?.email_verified === true
      }
      return true
    },

    // Called whenever a JWT is created or updated
    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id
      }
      if (account) {
        token.accessToken = account.access_token
      }
      return token
    },

    // Called whenever a session is checked
    async session({ session, token }) {
      session.user.id = token.id as string
      session.accessToken = token.accessToken as string
      return session
    },

    // Called on middleware and server-side auth checks
    async authorized({ auth, request }) {
      const isLoggedIn = !!auth?.user
      const isOnDashboard = request.nextUrl.pathname.startsWith("/dashboard")
      
      if (isOnDashboard) {
        return isLoggedIn
      }
      
      return true
    },

    // Called when user is redirected
    async redirect({ url, baseUrl }) {
      // Allows relative callback URLs
      if (url.startsWith("/")) return `${baseUrl}${url}`
      // Allows callback URLs on the same origin
      else if (new URL(url).origin === baseUrl) return url
      return baseUrl
    },
  },
})
```

## Database Adapter (Optional)

For persisting users, accounts, and sessions in a database, install the Prisma adapter:

```sh
pnpm add @auth/prisma-adapter
```

Then configure it in your `auth.ts`:

```typescript
import NextAuth from "next-auth"
import { PrismaAdapter } from "@auth/prisma-adapter"
import { prisma } from "@/lib/prisma"

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: {
    strategy: "database",
  },
  providers: [
    // ... providers
  ],
})
```

Required Prisma schema:

```prisma
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  accounts      Account[]
  sessions      Session[]
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String?
  access_token      String?
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String?
  session_state     String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

## API Routes

### Custom API Endpoints

```typescript
// app/api/user/route.ts
import { auth } from "@/auth"
import { NextResponse } from "next/server"

export async function GET() {
  const session = await auth()

  if (!session?.user) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    )
  }

  return NextResponse.json({
    user: session.user,
  })
}
```

### Protected Route Helper

```typescript
// lib/auth-helpers.ts
import { auth } from "@/auth"
import { NextResponse } from "next/server"
import type { Session } from "next-auth"

export async function withAuth(
  handler: (session: Session) => Promise<NextResponse>
) {
  const session = await auth()

  if (!session?.user) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    )
  }

  return handler(session)
}

// Usage
export async function GET() {
  return withAuth(async (session) => {
    return NextResponse.json({ userId: session.user.id })
  })
}
```

## Best Practices

### Security

- **Always hash passwords**: Use bcrypt, argon2, or similar
- **Use HTTPS in production**: Required for secure cookie transmission
- **Validate environment variables**: Check AUTH_SECRET and provider credentials
- **Set secure cookie options**:
  ```typescript
  cookies: {
    sessionToken: {
      name: `__Secure-next-auth.session-token`,
      options: {
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
        secure: process.env.NODE_ENV === 'production',
      },
    },
  }
  ```
- **Implement rate limiting**: Protect sign-in endpoints
- **Use CSRF protection**: Enabled by default in v5
- **Validate redirects**: Use the `redirect` callback to prevent open redirects

### Session Management

- **Use appropriate maxAge**: Default 30 days, adjust based on security requirements
- **Update sessions regularly**: Use `updateAge` to refresh session data
- **Handle session expiry gracefully**: Provide clear UI feedback
- **Secure session storage**: Use database strategy for sensitive applications

### Provider Configuration

- **Google OAuth**: Request minimum required scopes
- **Credentials**: Always validate input with zod or similar
- **Multiple providers**: Allow account linking carefully
- **Provider-specific logic**: Use callbacks to handle provider differences

### Performance

- **Cache session checks**: Use middleware for route protection
- **Minimize database calls**: Use JWT strategy when appropriate
- **Optimize database queries**: Add indexes on frequently queried fields
- **Use Edge Runtime**: For faster authentication checks in middleware

### Type Safety

- **Extend types properly**: Use module augmentation for custom session fields
- **Validate inputs**: Use zod for runtime type checking
- **TypeScript strict mode**: Enable for better type safety

## Common Patterns

### Protected Pages with Middleware

```typescript
import { auth } from "@/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const { pathname } = req.nextUrl

  // Public routes
  const publicRoutes = ['/auth/signin', '/auth/register', '/']
  if (publicRoutes.includes(pathname)) {
    return NextResponse.next()
  }

  // Protected routes
  if (!isLoggedIn) {
    const signInUrl = new URL('/auth/signin', req.url)
    signInUrl.searchParams.set('callbackUrl', pathname)
    return NextResponse.redirect(signInUrl)
  }

  // Role-based access
  const adminRoutes = ['/admin']
  if (adminRoutes.some(route => pathname.startsWith(route))) {
    if (req.auth.user.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', req.url))
    }
  }

  return NextResponse.next()
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
```

### Multi-Provider Setup

```typescript
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import GitHub from "next-auth/providers/github"
import Credentials from "next-auth/providers/credentials"
import { prisma } from "@/lib/prisma"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
    Credentials({
      // ... credentials config
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      // Link accounts with same email
      if (account?.provider !== "credentials") {
        const existingUser = await prisma.user.findUnique({
          where: { email: user.email },
        })
        
        if (existingUser) {
          // Link account to existing user
          await prisma.account.create({
            data: {
              userId: existingUser.id,
              type: account.type,
              provider: account.provider,
              providerAccountId: account.providerAccountId,
              access_token: account.access_token,
              refresh_token: account.refresh_token,
            },
          })
        }
      }
      return true
    },
  },
})
```

### Custom Sign In Page

```typescript
// app/auth/signin/page.tsx
import { signIn } from "@/auth"
import { redirect } from "next/navigation"

export default function SignInPage({
  searchParams,
}: {
  searchParams: { callbackUrl?: string }
}) {
  const callbackUrl = searchParams.callbackUrl || "/dashboard"

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-8">
        <h1 className="text-2xl font-bold text-center">Sign In</h1>
        
        {/* OAuth Providers */}
        <div className="space-y-4">
          <form
            action={async () => {
              "use server"
              await signIn("google", { redirectTo: callbackUrl })
            }}
          >
            <button 
              type="submit"
              className="w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded hover:bg-gray-50"
            >
              Continue with Google
            </button>
          </form>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="bg-white px-2 text-gray-500">Or</span>
          </div>
        </div>

        {/* Credentials Form */}
        <form
          action={async (formData) => {
            "use server"
            try {
              await signIn("credentials", {
                email: formData.get("email"),
                password: formData.get("password"),
                redirectTo: callbackUrl,
              })
            } catch (error) {
              redirect(`/auth/signin?error=CredentialsSignin&callbackUrl=${callbackUrl}`)
            }
          }}
          className="space-y-4"
        >
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  )
}
```

### Role-Based Access Control (RBAC)

```typescript
// lib/auth-rbac.ts
import { auth } from "@/auth"

export type Role = "admin" | "user" | "guest"

export async function checkRole(allowedRoles: Role[]) {
  const session = await auth()
  
  if (!session?.user) {
    return false
  }

  const userRole = session.user.role as Role
  return allowedRoles.includes(userRole)
}

// Usage in Server Component
export default async function AdminPage() {
  const hasAccess = await checkRole(["admin"])
  
  if (!hasAccess) {
    redirect("/unauthorized")
  }

  return <div>Admin Dashboard</div>
}

// Usage in Server Action
export async function deleteUser(userId: string) {
  "use server"
  
  const hasAccess = await checkRole(["admin"])
  
  if (!hasAccess) {
    throw new Error("Unauthorized")
  }

  const { prisma } = await import("@/lib/prisma")
  await prisma.user.delete({ where: { id: userId } })
}
```

## Migration from v4 to v5

### Key Differences

1. **Import changes**: `next-auth` package remains the same, but imports are simplified
2. **Universal `auth()`**: Replace `getServerSession` with `auth()`
3. **Middleware**: Use `auth` as middleware directly
4. **Configuration**: More streamlined, fewer options needed

### Migration Steps

```typescript
// v4 (old)
import { getServerSession } from "next-auth/next"
import { authOptions } from "@/lib/auth"

export async function GET() {
  const session = await getServerSession(authOptions)
}

// v5 (new)
import { auth } from "@/auth"

export async function GET() {
  const session = await auth()
}
```

```typescript
// v4 middleware (old)
import { withAuth } from "next-auth/middleware"

export default withAuth({
  callbacks: {
    authorized: ({ token }) => !!token,
  },
})

// v5 middleware (new)
export { auth as middleware } from "@/auth"
```

## Troubleshooting

### Common Issues

**AUTH_SECRET not set**:
```
Error: AUTH_SECRET environment variable is not set
```
Generate and set `AUTH_SECRET` in `.env.local`

**Google OAuth redirect mismatch**:
```
Error: redirect_uri_mismatch
```
Ensure redirect URI in Google Console matches: `http://localhost:3000/api/auth/callback/google`

**Session not persisting**:
- Check `AUTH_URL` is set correctly
- Verify cookies are not blocked
- Ensure `sessionToken` cookie is being set (check browser DevTools)

**TypeScript errors with session**:
- Extend the `Session` and `JWT` types using module augmentation
- Run `pnpm tsc --noEmit` to check for type errors

**Credentials provider not working**:
- Ensure `session.strategy` is set to `"jwt"`
- Check `authorize` function returns correct user object with `id` field
- Verify password hashing/comparison logic

## Resources

- **Official Docs**: https://authjs.dev
- **GitHub**: https://github.com/nextauthjs/next-auth
- **Discord Community**: https://discord.gg/nextauth
- **Examples**: https://github.com/nextauthjs/next-auth/tree/main/apps/examples
- **Provider List**: https://authjs.dev/getting-started/providers
