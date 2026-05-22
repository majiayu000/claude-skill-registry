---
name: better-auth-expo
description: Better Auth integration for Expo/React Native with SecureStore, deep linking, and native provider SDKs
agents: [tap]
triggers: [auth, login, expo, mobile, securestore, deep link]
context7_libraries:
  - /better-auth/better-auth
llm_docs:
  - better-auth
---

# Better Auth - Expo/React Native Integration

**Better Auth** provides first-class Expo support via the `@better-auth/expo` plugin for secure mobile authentication.

## AI Tooling

**IMPORTANT**: Before implementing Better Auth in Expo, consult:

- **AI Documentation**: `https://better-auth.com/llms.txt`
- **MCP Server**: `https://mcp.chonkie.ai/better-auth/better-auth-builder/mcp`

Use Context7 to look up Better Auth Expo patterns:

```
get_library_docs({ libraryName: "better-auth", topic: "expo integration" })
get_library_docs({ libraryName: "better-auth", topic: "expo social sign-in" })
get_library_docs({ libraryName: "better-auth", topic: "expo secure store" })
```

---

## Installation

```bash
# Server dependencies (backend)
npx expo install better-auth @better-auth/expo

# Client dependencies (Expo app)
npx expo install better-auth @better-auth/expo expo-secure-store expo-linking expo-web-browser expo-constants
```

## Environment Variables

```bash
# .env (backend)
BETTER_AUTH_SECRET=your-secret-key-at-least-32-chars
BETTER_AUTH_URL=http://localhost:8081
```

---

## Server Configuration

**Backend (`lib/auth.ts`):**

```typescript
import { betterAuth } from "better-auth"
import { expo } from "@better-auth/expo"
import { drizzleAdapter } from "better-auth/adapters/drizzle"
import { db } from "@/db"

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg" }),
  plugins: [expo()],  // Enable Expo support
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    apple: {
      clientId: process.env.APPLE_CLIENT_ID!,
      clientSecret: process.env.APPLE_CLIENT_SECRET!,
    },
  },
  // Trust your app's deep link scheme
  trustedOrigins: [
    "myapp://",
    // Development mode (Expo's exp:// scheme)
    ...(process.env.NODE_ENV === "development" ? [
      "exp://",
      "exp://**",
    ] : []),
  ],
})
```

**Expo API Route (`app/api/auth/[...auth]+api.ts`):**

```typescript
import { auth } from "@/lib/auth"

const handler = auth.handler
export { handler as GET, handler as POST }
```

---

## Client Configuration

**Auth Client (`lib/auth-client.ts`):**

```typescript
import { createAuthClient } from "better-auth/react"
import { expoClient } from "@better-auth/expo/client"
import * as SecureStore from "expo-secure-store"

export const authClient = createAuthClient({
  baseURL: process.env.EXPO_PUBLIC_API_URL || "http://localhost:8081",
  plugins: [
    expoClient({
      scheme: "myapp",           // Must match app.json scheme
      storagePrefix: "myapp",    // Prefix for secure storage keys
      storage: SecureStore,      // Secure credential storage
    }),
  ],
})

export const { signIn, signUp, signOut, useSession } = authClient
```

---

## App Configuration

**`app.json`:**

```json
{
  "expo": {
    "scheme": "myapp",
    "plugins": [
      "expo-router",
      "expo-secure-store"
    ]
  }
}
```

**Metro Config (`metro.config.js`):**

```javascript
const { getDefaultConfig } = require("expo/metro-config")

const config = getDefaultConfig(__dirname)
config.resolver.unstable_enablePackageExports = true  // Required for Better Auth

module.exports = config
```

---

## Sign In Component

```typescript
import { useState } from "react"
import { View, TextInput, Button, Text, StyleSheet } from "react-native"
import { authClient } from "@/lib/auth-client"
import { router } from "expo-router"

export default function SignIn() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSignIn = async () => {
    setLoading(true)
    setError(null)
    
    const { error } = await authClient.signIn.email({
      email,
      password,
      callbackURL: "/dashboard",  // Converts to myapp://dashboard
    })
    
    if (error) {
      setError(error.message)
    } else {
      router.replace("/dashboard")
    }
    setLoading(false)
  }

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      {error && <Text style={styles.error}>{error}</Text>}
      <Button 
        title={loading ? "Signing in..." : "Sign In"} 
        onPress={handleSignIn}
        disabled={loading}
      />
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center" },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 12, marginBottom: 12, borderRadius: 8 },
  error: { color: "red", marginBottom: 12 },
})
```

---

## Social Sign-In

```typescript
import { Button, View } from "react-native"
import { authClient } from "@/lib/auth-client"

export default function SocialSignIn() {
  const handleGoogleSignIn = async () => {
    await authClient.signIn.social({
      provider: "google",
      callbackURL: "/dashboard",  // Deep links to myapp://dashboard
    })
  }

  const handleAppleSignIn = async () => {
    await authClient.signIn.social({
      provider: "apple",
      callbackURL: "/dashboard",
    })
  }

  return (
    <View style={{ gap: 12 }}>
      <Button title="Continue with Google" onPress={handleGoogleSignIn} />
      <Button title="Continue with Apple" onPress={handleAppleSignIn} />
    </View>
  )
}
```

**IdToken Sign-In (Native Provider SDKs):**

```typescript
// Use when authenticating via native Google/Apple SDKs
await authClient.signIn.social({
  provider: "google",
  idToken: {
    token: "id-token-from-native-sdk",
    nonce: "optional-nonce",
  },
  callbackURL: "/dashboard",
})
```

---

## Session Hook

```typescript
import { View, Text, Button, ActivityIndicator } from "react-native"
import { authClient } from "@/lib/auth-client"
import { router } from "expo-router"

export default function Profile() {
  const { data: session, isPending } = authClient.useSession()

  if (isPending) {
    return <ActivityIndicator />
  }

  if (!session) {
    router.replace("/sign-in")
    return null
  }

  const handleSignOut = async () => {
    await authClient.signOut()
    router.replace("/sign-in")
  }

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>
        Welcome, {session.user.name}!
      </Text>
      <Text style={{ color: "#666", marginTop: 8 }}>
        {session.user.email}
      </Text>
      <Button title="Sign Out" onPress={handleSignOut} />
    </View>
  )
}
```

---

## Authenticated API Requests

Better Auth stores session cookies in SecureStore. For authenticated API requests:

```typescript
import { authClient } from "@/lib/auth-client"

async function fetchProtectedData() {
  const cookies = authClient.getCookie()  // Get session cookies
  
  const response = await fetch("http://localhost:8081/api/protected", {
    headers: {
      Cookie: cookies,
    },
    credentials: "omit",  // Don't let fetch manage cookies
  })
  
  return response.json()
}
```

**With tRPC:**

```typescript
import { authClient } from "@/lib/auth-client"

const trpcClient = api.createClient({
  links: [
    httpBatchLink({
      url: `${API_URL}/trpc`,
      headers() {
        const cookies = authClient.getCookie()
        return cookies ? { Cookie: cookies } : {}
      },
    }),
  ],
})
```

---

## Protected Routes with Expo Router

```typescript
// app/(auth)/_layout.tsx
import { Redirect, Stack } from "expo-router"
import { authClient } from "@/lib/auth-client"
import { ActivityIndicator, View } from "react-native"

export default function AuthLayout() {
  const { data: session, isPending } = authClient.useSession()

  if (isPending) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" />
      </View>
    )
  }

  if (!session) {
    return <Redirect href="/sign-in" />
  }

  return <Stack />
}
```

---

## Best Practices

1. **Always use SecureStore** for credential storage on mobile
2. **Configure trustedOrigins** with your app scheme for deep linking
3. **Enable `unstable_enablePackageExports`** in Metro config
4. **Use native provider SDKs** (Google Sign-In, Apple Sign-In) with idToken for best UX
5. **Cache sessions** - Better Auth caches in SecureStore automatically
6. **Handle offline gracefully** - sessions persist across app restarts
7. **Clear cache on logout** - `authClient.signOut()` handles this

**Documentation**: https://better-auth.com/docs/integrations/expo
