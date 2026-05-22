---
name: t4-stack
version: "1.0.0"
description: T4 Stack - Full-stack TypeScript starter for React Native + Web with Tamagui, tRPC, Cloudflare edge deployment, and universal code sharing across iOS, Android, and PWA
---

# T4 Stack Skill

The **T4 Stack** is a full-stack, type-safe starter kit for building universal applications across iOS, Android, Web, and Desktop from a single TypeScript codebase. Created by Tim Miller, it emphasizes developer experience, rapid deployment, and edge-first architecture with Cloudflare.

**Key Value Proposition**: Build once, deploy everywhere - iOS, Android, Web (PWA), macOS, Windows, and Linux with 6-second installs, 30-second backend deployments, and end-to-end type safety.

## When to Use This Skill

- Building cross-platform apps with shared codebase (React Native + Web)
- Creating full-stack TypeScript applications with tRPC
- Deploying to Cloudflare Workers and D1 edge database
- Setting up Expo + Next.js monorepo projects
- Implementing Tamagui UI components across platforms
- Configuring Supabase authentication for mobile + web
- Working with Drizzle ORM and SQLite at the edge
- Building Progressive Web Apps with native-like experience

## When NOT to Use This Skill

- For backend-only Node.js projects (use standard Node.js patterns)
- For React-only web apps without mobile (use Next.js directly)
- For React Native-only apps without web (use Expo directly)
- For non-TypeScript projects (T4 is TypeScript-first)
- For AWS/GCP deployment (T4 is Cloudflare-focused)

---

## Core Concepts

### Technology Stack Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         T4 Stack                                 │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │   Shared Codebase    │
                    │  /packages/app       │
                    │  /packages/ui        │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼───────┐    ┌────────▼────────┐    ┌───────▼───────┐
│   Next.js     │    │     Expo        │    │    Tauri      │
│   (Web/PWA)   │    │  (iOS/Android)  │    │   (Desktop)   │
└───────────────┘    └─────────────────┘    └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼───────────┐
                    │   Cloudflare Edge    │
                    │  - Workers (API)     │
                    │  - D1 (SQLite DB)    │
                    │  - Pages (Frontend)  │
                    └──────────────────────┘
```

### Stack Components

| Layer | Technology | Purpose |
|-------|------------|---------|
| **UI Framework** | Tamagui | Cross-platform components with design system |
| **Web** | Next.js | React framework for web + PWA |
| **Mobile** | Expo + Expo Router | React Native for iOS/Android |
| **Desktop** | Tauri (optional) | Native desktop apps |
| **Navigation** | Solito | Unified navigation across platforms |
| **API** | tRPC + Hono | Type-safe API with edge-compatible server |
| **Data Fetching** | TanStack Query | Server state management |
| **State** | Jotai | Lightweight global state |
| **Database** | Cloudflare D1 + Drizzle | SQLite at the edge with ORM |
| **Validation** | Valibot | Lightweight runtime type checking |
| **Auth** | Supabase Auth | Authentication across platforms |
| **Performance** | Million.js, PattyCake | React optimization, pattern matching |
| **Code Quality** | Biome | Fast linting and formatting |

---

## Installation

### Prerequisites

- **Bun v1.0+** (required)
- Node.js 20+ (for some tooling)
- Cloudflare account (for deployment)
- Supabase account (for authentication)

### Quick Start

```bash
# Create new T4 project (interactive)
bun create t4-app

# Create with specific project name
bun create t4-app my-app

# Create with Tauri desktop support (experimental)
bun create t4-app --tauri

# Create with Lucia Auth instead of Supabase
bun create t4-app --lucia
```

### Post-Installation

```bash
cd my-app

# Install dependencies
bun install

# Start development servers
bun dev

# Start web only
bun dev:web

# Start mobile (Expo)
bun dev:native
```

---

## Project Structure

```
my-app/
├── apps/
│   ├── next/                 # Next.js web application
│   │   ├── app/              # App Router pages
│   │   ├── public/           # Static assets
│   │   └── next.config.mjs   # Next.js configuration
│   │
│   ├── expo/                 # Expo mobile application
│   │   ├── app/              # Expo Router screens
│   │   ├── assets/           # Mobile assets
│   │   └── app.config.ts     # Expo configuration
│   │
│   └── tauri/                # Desktop app (if --tauri flag used)
│
├── packages/
│   ├── app/                  # Shared application code
│   │   ├── features/         # Feature modules (screens)
│   │   │   ├── home/
│   │   │   │   └── screen.tsx
│   │   │   └── settings/
│   │   │       ├── screen.tsx
│   │   │       ├── screen.native.tsx  # Native-specific
│   │   │       └── screen.web.tsx     # Web-specific
│   │   ├── provider/         # App providers (auth, theme)
│   │   └── utils/            # Shared utilities
│   │
│   ├── ui/                   # Shared UI components
│   │   ├── src/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── index.ts
│   │   └── tamagui.config.ts
│   │
│   ├── api/                  # Backend API (Hono + tRPC)
│   │   ├── src/
│   │   │   ├── router/       # tRPC routers
│   │   │   ├── context.ts    # tRPC context
│   │   │   └── index.ts      # API entry point
│   │   └── wrangler.toml     # Cloudflare Workers config
│   │
│   └── db/                   # Database schema (Drizzle)
│       ├── schema/
│       │   └── users.ts
│       ├── migrations/
│       └── drizzle.config.ts
│
├── .env.example              # Environment template
├── biome.json                # Linting/formatting config
├── turbo.json                # Turborepo configuration
└── package.json              # Root package.json
```

### Platform-Specific File Extensions

| Extension | Target Platform | Example |
|-----------|-----------------|---------|
| `.tsx` | Shared (all platforms) | `screen.tsx` |
| `.native.tsx` | React Native only | `screen.native.tsx` |
| `.web.tsx` | Next.js only | `screen.web.tsx` |

---

## Creating Features

### Adding a New Screen

```bash
# 1. Create feature folder
mkdir -p packages/app/features/profile

# 2. Create shared screen
touch packages/app/features/profile/screen.tsx
```

```typescript
// packages/app/features/profile/screen.tsx
import { YStack, H1, Paragraph, Button } from '@my-app/ui'
import { useRouter } from 'solito/router'

export function ProfileScreen() {
  const { push } = useRouter()

  return (
    <YStack flex={1} padding="$4" space="$4">
      <H1>Profile</H1>
      <Paragraph>Welcome to your profile!</Paragraph>
      <Button onPress={() => push('/settings')}>
        Go to Settings
      </Button>
    </YStack>
  )
}
```

```typescript
// apps/next/app/profile/page.tsx
import { ProfileScreen } from '@my-app/app/features/profile/screen'

export default function ProfilePage() {
  return <ProfileScreen />
}
```

```typescript
// apps/expo/app/profile.tsx
import { ProfileScreen } from '@my-app/app/features/profile/screen'

export default function ProfileRoute() {
  return <ProfileScreen />
}
```

### Platform-Specific Code

```typescript
// packages/app/features/camera/screen.native.tsx
import { Camera } from 'expo-camera'

export function CameraScreen() {
  return <Camera style={{ flex: 1 }} />
}
```

```typescript
// packages/app/features/camera/screen.web.tsx
export function CameraScreen() {
  return (
    <div>
      <video ref={videoRef} autoPlay />
      {/* Web camera implementation */}
    </div>
  )
}
```

---

## tRPC API Setup

### Router Definition

```typescript
// packages/api/src/router/user.ts
import { router, protectedProcedure, publicProcedure } from '../trpc'
import { v } from 'valibot'
import { users, insertUserSchema } from '@my-app/db/schema'

export const userRouter = router({
  // Public procedure
  getById: publicProcedure
    .input(v.object({ id: v.string() }))
    .query(async ({ ctx, input }) => {
      return ctx.db.query.users.findFirst({
        where: eq(users.id, input.id)
      })
    }),

  // Protected procedure (requires auth)
  updateProfile: protectedProcedure
    .input(v.object({
      name: v.string(),
      bio: v.optional(v.string())
    }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.update(users)
        .set(input)
        .where(eq(users.id, ctx.user.id))
    }),
})
```

### Root Router

```typescript
// packages/api/src/router/index.ts
import { router } from '../trpc'
import { userRouter } from './user'
import { postRouter } from './post'

export const appRouter = router({
  user: userRouter,
  post: postRouter,
})

export type AppRouter = typeof appRouter
```

### Client Usage

```typescript
// packages/app/features/profile/screen.tsx
import { trpc } from '@my-app/app/utils/trpc'

export function ProfileScreen() {
  const { data: user, isLoading } = trpc.user.getById.useQuery({
    id: 'user-123'
  })

  const updateProfile = trpc.user.updateProfile.useMutation({
    onSuccess: () => {
      // Handle success
    }
  })

  if (isLoading) return <Spinner />

  return (
    <YStack>
      <H1>{user?.name}</H1>
      <Button onPress={() => updateProfile.mutate({ name: 'New Name' })}>
        Update Name
      </Button>
    </YStack>
  )
}
```

---

## Tamagui UI Components

### Basic Component Usage

```typescript
import {
  YStack,
  XStack,
  H1,
  H2,
  Paragraph,
  Button,
  Input,
  Card,
  Image,
  Separator,
  Sheet,
  Dialog,
} from '@my-app/ui'

function MyComponent() {
  return (
    <YStack flex={1} padding="$4" space="$4">
      <XStack justifyContent="space-between" alignItems="center">
        <H1>Title</H1>
        <Button size="$3" theme="active">
          Action
        </Button>
      </XStack>

      <Card elevate padded>
        <Card.Header>
          <H2>Card Title</H2>
        </Card.Header>
        <Paragraph>Card content goes here.</Paragraph>
        <Card.Footer>
          <XStack space="$2">
            <Button flex={1}>Cancel</Button>
            <Button flex={1} theme="active">Confirm</Button>
          </XStack>
        </Card.Footer>
      </Card>

      <Input placeholder="Enter text..." />
    </YStack>
  )
}
```

### Theme Configuration

```typescript
// packages/ui/tamagui.config.ts
import { createTamagui, createTokens } from '@tamagui/core'
import { shorthands } from '@tamagui/shorthands'
import { themes, tokens } from '@tamagui/themes'

export const config = createTamagui({
  themes,
  tokens,
  shorthands,
  fonts: {
    // Custom fonts
  },
})

export type AppConfig = typeof config

declare module '@tamagui/core' {
  interface TamaguiCustomConfig extends AppConfig {}
}
```

---

## Authentication with Supabase

### Environment Configuration

```bash
# .env.local (Next.js)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# .dev.vars (Cloudflare Workers)
JWT_VERIFICATION_KEY=your-jwt-secret-from-supabase
```

### Auth Provider Setup

```typescript
// packages/app/provider/auth.tsx
import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../utils/supabase'
import type { User, Session } from '@supabase/supabase-js'

type AuthContextType = {
  user: User | null
  session: Session | null
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setUser(session?.user ?? null)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) throw error
  }

  const signUp = async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
    })
    if (error) throw error
  }

  const signOut = async () => {
    await supabase.auth.signOut()
  }

  return (
    <AuthContext.Provider value={{ user, session, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
```

### OAuth Login (Google, Apple, Discord)

```typescript
// packages/app/features/auth/login.tsx
import { Button, YStack } from '@my-app/ui'
import { supabase } from '../../utils/supabase'
import * as WebBrowser from 'expo-web-browser'
import { makeRedirectUri } from 'expo-auth-session'

export function LoginScreen() {
  const signInWithGoogle = async () => {
    const redirectUrl = makeRedirectUri()

    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: redirectUrl,
      },
    })

    if (data?.url) {
      await WebBrowser.openAuthSessionAsync(data.url, redirectUrl)
    }
  }

  return (
    <YStack space="$4" padding="$4">
      <Button onPress={signInWithGoogle} icon={GoogleIcon}>
        Sign in with Google
      </Button>
      <Button onPress={signInWithApple} icon={AppleIcon}>
        Sign in with Apple
      </Button>
    </YStack>
  )
}
```

---

## Database with Drizzle

### Schema Definition

```typescript
// packages/db/schema/users.ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'
import { createInsertSchema, createSelectSchema } from 'drizzle-valibot'

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name'),
  avatarUrl: text('avatar_url'),
  createdAt: integer('created_at', { mode: 'timestamp' })
    .notNull()
    .default(sql`(unixepoch())`),
})

// Valibot schemas for validation
export const insertUserSchema = createInsertSchema(users)
export const selectUserSchema = createSelectSchema(users)
```

### Migrations

```bash
# Generate migration from schema changes
bun db:generate

# Push migrations to D1
bun db:push

# Run migrations locally
bun db:migrate
```

### Database Context in tRPC

```typescript
// packages/api/src/context.ts
import { drizzle } from 'drizzle-orm/d1'
import * as schema from '@my-app/db/schema'

export function createContext(env: Env, user?: User) {
  const db = drizzle(env.DB, { schema })

  return {
    db,
    user,
  }
}
```

---

## Deployment

### Cloudflare Workers (Backend)

```toml
# packages/api/wrangler.toml
name = "my-app-api"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "my-app-db"
database_id = "xxx-xxx-xxx"
```

```bash
# Deploy backend
cd packages/api
bun run deploy
# OR
wrangler deploy
```

### Cloudflare Pages (Frontend)

```bash
# Deploy Next.js to Pages
cd apps/next
bun run build
wrangler pages deploy .next
```

### Expo (Mobile)

```bash
# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to App Store
eas submit --platform ios

# Submit to Play Store
eas submit --platform android
```

### GitHub Actions (CI/CD)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run db:migrate
      - run: wrangler deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CF_API_TOKEN }}

  deploy-web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run build:web
      - uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          projectName: my-app
          directory: apps/next/.next
```

---

## Troubleshooting

### Common Issues

**Bun version mismatch:**
```bash
# Check Bun version (must be 1.0+)
bun --version

# Update Bun
curl -fsSL https://bun.sh/install | bash
```

**Tamagui styles not applying:**
```bash
# Clear Metro cache
cd apps/expo
bun expo start --clear

# Clear Next.js cache
cd apps/next
rm -rf .next
bun dev
```

**tRPC type errors after schema change:**
```bash
# Regenerate types
bun turbo build --filter=@my-app/api

# Restart TypeScript server in IDE
```

**D1 database not found:**
```bash
# Create D1 database
wrangler d1 create my-app-db

# Update wrangler.toml with returned database_id
```

**Supabase auth not working on mobile:**
```typescript
// Ensure deep link handling in app.config.ts
export default {
  scheme: 'my-app',
  // ...
}
```

---

## Resources

### Official Documentation
- [T4 Stack Docs](https://docs.t4stack.com/)
- [GitHub Repository](https://github.com/timothymiller/t4-app)
- [Live Demo](https://app.t4stack.com/)

### Technology Documentation
- [Tamagui](https://tamagui.dev/)
- [tRPC](https://trpc.io/)
- [Expo](https://docs.expo.dev/)
- [Next.js](https://nextjs.org/docs)
- [Drizzle ORM](https://orm.drizzle.team/)
- [Cloudflare Workers](https://developers.cloudflare.com/workers/)
- [Supabase](https://supabase.com/docs)

### Community
- [Discord](https://discord.gg/t4stack)
- [GitHub Discussions](https://github.com/timothymiller/t4-app/discussions)

---

## Version History

- **1.0.0** (2026-01-12): Initial skill release
  - Complete T4 Stack framework documentation
  - Project structure and file conventions
  - tRPC API patterns with Valibot validation
  - Tamagui UI component examples
  - Supabase authentication integration
  - Drizzle ORM database setup
  - Cloudflare deployment configuration
  - Expo mobile development workflow
  - Troubleshooting guide
