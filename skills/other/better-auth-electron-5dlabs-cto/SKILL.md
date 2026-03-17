---
name: better-auth-electron
description: Better Auth integration for Electron desktop apps with secure IPC, context isolation, and encrypted session storage
agents: [spark]
triggers: [auth, login, electron, desktop, ipc, contextbridge]
context7_libraries:
  - /better-auth/better-auth
llm_docs:
  - better-auth
---

# Better Auth - Electron Desktop Integration

**Better Auth** works seamlessly with Electron using the React client in the renderer process with secure IPC patterns.

## AI Tooling

**IMPORTANT**: Before implementing Better Auth in Electron, consult:

- **AI Documentation**: `https://better-auth.com/llms.txt`
- **MCP Server**: `https://mcp.chonkie.ai/better-auth/better-auth-builder/mcp`

Use Context7 to look up Better Auth patterns:

```
get_library_docs({ libraryName: "better-auth", topic: "react client" })
get_library_docs({ libraryName: "better-auth", topic: "session management" })
```

---

## Installation

```bash
# Install Better Auth and electron-store for session persistence
npm install better-auth electron-store
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Main Process                         │
│  - Session validation via IPC                        │
│  - Secure token storage (electron-store)             │
│  - Auth state management                             │
└───────────────────┬─────────────────────────────────┘
                    │ IPC (contextBridge)
┌───────────────────▼─────────────────────────────────┐
│              Preload Script                          │
│  - Expose safe auth APIs to renderer                 │
│  - No direct Node.js access                          │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│              Renderer Process                        │
│  - Better Auth React client                          │
│  - UI components (React/shadcn)                      │
│  - Uses window.authApi from preload                  │
└─────────────────────────────────────────────────────┘
```

---

## Backend Configuration

Your Electron app needs a Better Auth backend (can be local or remote):

**Backend (`server/auth.ts`):**

```typescript
import { betterAuth } from "better-auth"
import { drizzleAdapter } from "better-auth/adapters/drizzle"
import { db } from "./db"

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "sqlite" }),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
  // Trust Electron app origin
  trustedOrigins: [
    "app://.",          // Electron custom protocol
    "file://",          // File protocol
    "http://localhost", // Dev server
  ],
})
```

---

## Main Process

**`main.ts`:**

```typescript
import { app, BrowserWindow, ipcMain, shell } from "electron"
import Store from "electron-store"
import path from "path"

// Secure persistent storage for auth state
const store = new Store({
  name: "auth",
  encryptionKey: "your-encryption-key",  // Use secure key management
})

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,   // REQUIRED - security
      nodeIntegration: false,   // REQUIRED - security
      sandbox: true,            // RECOMMENDED
    },
  })

  // Open OAuth callbacks in external browser
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("http")) {
      shell.openExternal(url)
      return { action: "deny" }
    }
    return { action: "allow" }
  })

  win.loadFile("index.html")
}

// IPC handlers for auth operations
ipcMain.handle("auth:get-stored-session", async () => {
  return store.get("session", null)
})

ipcMain.handle("auth:store-session", async (_, session) => {
  store.set("session", session)
})

ipcMain.handle("auth:clear-session", async () => {
  store.delete("session")
})

ipcMain.handle("auth:get-api-url", async () => {
  return process.env.AUTH_API_URL || "http://localhost:3000"
})

app.whenReady().then(createWindow)
```

---

## Preload Script

**`preload.ts`:**

```typescript
import { contextBridge, ipcRenderer } from "electron"

// Expose secure auth API to renderer
contextBridge.exposeInMainWorld("authApi", {
  // Session persistence
  getStoredSession: () => ipcRenderer.invoke("auth:get-stored-session"),
  storeSession: (session: unknown) => ipcRenderer.invoke("auth:store-session", session),
  clearSession: () => ipcRenderer.invoke("auth:clear-session"),
  
  // Config
  getApiUrl: () => ipcRenderer.invoke("auth:get-api-url"),
  
  // Events
  onAuthStateChange: (callback: (session: unknown) => void) => {
    ipcRenderer.on("auth:state-changed", (_, session) => callback(session))
  },
})

// Type declarations for renderer
declare global {
  interface Window {
    authApi: {
      getStoredSession: () => Promise<unknown>
      storeSession: (session: unknown) => Promise<void>
      clearSession: () => Promise<void>
      getApiUrl: () => Promise<string>
      onAuthStateChange: (callback: (session: unknown) => void) => void
    }
  }
}
```

---

## Renderer Process (React)

**Auth Client (`src/lib/auth-client.ts`):**

```typescript
import { createAuthClient } from "better-auth/react"

// Get API URL from main process
const getAuthClient = async () => {
  const baseURL = await window.authApi.getApiUrl()
  
  return createAuthClient({
    baseURL,
    // Custom fetch to handle Electron environment
    fetchOptions: {
      credentials: "include",
    },
  })
}

// Export singleton
let authClientPromise: ReturnType<typeof getAuthClient> | null = null

export const getClient = () => {
  if (!authClientPromise) {
    authClientPromise = getAuthClient()
  }
  return authClientPromise
}

// Hook for components
export function useAuthClient() {
  const [client, setClient] = useState<Awaited<ReturnType<typeof getAuthClient>> | null>(null)
  
  useEffect(() => {
    getClient().then(setClient)
  }, [])
  
  return client
}
```

**Simplified Client (if API URL is static):**

```typescript
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: "http://localhost:3000",  // Your auth server
})

export const { signIn, signUp, signOut, useSession } = authClient
```

---

## Sign In Component

```typescript
import { useState } from "react"
import { authClient } from "@/lib/auth-client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function SignIn() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const { data, error } = await authClient.signIn.email({
      email,
      password,
    })

    if (error) {
      setError(error.message)
    } else if (data?.session) {
      // Persist session to main process store
      await window.authApi.storeSession(data.session)
    }
    
    setLoading(false)
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Sign In</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSignIn} className="space-y-4">
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="text-sm text-destructive">{error}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Signing in..." : "Sign In"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
```

---

## Session Management

```typescript
import { useEffect } from "react"
import { authClient } from "@/lib/auth-client"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function UserMenu() {
  const { data: session, isPending } = authClient.useSession()

  // Sync session changes to main process
  useEffect(() => {
    if (session) {
      window.authApi.storeSession(session)
    }
  }, [session])

  const handleSignOut = async () => {
    await authClient.signOut()
    await window.authApi.clearSession()
  }

  if (isPending) {
    return <div className="h-8 w-8 animate-pulse rounded-full bg-muted" />
  }

  if (!session) {
    return <Button variant="outline">Sign In</Button>
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
          <Avatar className="h-8 w-8">
            <AvatarImage src={session.user.image || ""} />
            <AvatarFallback>
              {session.user.name?.[0]?.toUpperCase()}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem className="font-medium">
          {session.user.name}
        </DropdownMenuItem>
        <DropdownMenuItem className="text-muted-foreground">
          {session.user.email}
        </DropdownMenuItem>
        <DropdownMenuItem onClick={handleSignOut}>
          Sign Out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

---

## Restore Session on App Launch

```typescript
// App.tsx - Restore session when app starts
import { useEffect, useState } from "react"
import { authClient } from "@/lib/auth-client"

export function App() {
  const [initialized, setInitialized] = useState(false)

  useEffect(() => {
    async function restoreSession() {
      // Check for stored session from previous launch
      const storedSession = await window.authApi.getStoredSession()
      
      if (storedSession) {
        // Validate session with server
        const { data: currentSession } = await authClient.getSession()
        
        if (!currentSession) {
          // Session expired, clear stored data
          await window.authApi.clearSession()
        }
      }
      
      setInitialized(true)
    }
    
    restoreSession()
  }, [])

  if (!initialized) {
    return <div>Loading...</div>
  }

  return <MainApp />
}
```

---

## OAuth in Electron

For OAuth flows, open the auth URL in the system browser and handle the callback:

```typescript
import { shell } from "electron"  // Main process only

// In main process - handle OAuth callback
app.setAsDefaultProtocolClient("myapp")  // Register custom protocol

app.on("open-url", (event, url) => {
  // Handle OAuth callback: myapp://auth/callback?code=...
  if (url.includes("/auth/callback")) {
    mainWindow.webContents.send("auth:oauth-callback", url)
  }
})
```

---

## Security Best Practices

1. **Always use contextIsolation** - Never expose Node.js to renderer
2. **Encrypt stored sessions** - Use electron-store with encryption
3. **Validate sessions on startup** - Check with server before trusting local state
4. **Handle OAuth via system browser** - More secure than in-app browser
5. **Use sandbox mode** - Additional security layer
6. **Clear sensitive data on sign out** - Both in-memory and persistent storage

**Documentation**: https://better-auth.com/docs
