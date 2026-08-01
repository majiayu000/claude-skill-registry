---
name: auth-scaffold
description: '> Generate Complete Auth System: Login, register, forgot password, and
  session management.'
---

# Auth Scaffold Skill

> **Generate Complete Auth System**: Login, register, forgot password, and session management.

---

## 🎯 Purpose

When user says: "Add authentication" or "Create login/signup"

Generate a complete authentication system with:
- Login page
- Register page
- Forgot password
- Session management
- Protected routes

---

## 📁 Generated Structure

```
src/
├── app/
│   ├── (auth)/
│   │   ├── layout.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── forgot-password/
│   │       └── page.tsx
│   └── (protected)/
│       └── layout.tsx
├── components/
│   └── auth/
│       ├── login-form.tsx
│       ├── register-form.tsx
│       ├── forgot-password-form.tsx
│       ├── user-button.tsx
│       └── auth-provider.tsx
├── lib/
│   ├── auth.ts
│   └── validations/
│       └── auth.ts
└── auth.ts (NextAuth config)
```

---

## 🔐 NextAuth Configuration

```typescript
// auth.ts
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import Credentials from "next-auth/providers/credentials"
import { PrismaAdapter } from "@auth/prisma-adapter"
import { db } from "@/lib/db"
import bcrypt from "bcryptjs"

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: { strategy: "jwt" },
  pages: {
    signIn: "/login",
    error: "/login",
  },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    Credentials({
      credentials: {
        email: { type: "email" },
        password: { type: "password" },
      },
      authorize: async (credentials) => {
        const { email, password } = credentials

        const user = await db.user.findUnique({
          where: { email: email as string },
        })

        if (!user || !user.passwordHash) return null

        const isValid = await bcrypt.compare(
          password as string,
          user.passwordHash
        )

        if (!isValid) return null

        return { id: user.id, email: user.email, name: user.name }
      },
    }),
  ],
  callbacks: {
    jwt: async ({ token, user }) => {
      if (user) token.id = user.id
      return token
    },
    session: async ({ session, token }) => {
      if (session.user) session.user.id = token.id as string
      return session
    },
  },
})
```

---

## 📝 Login Form

```tsx
// components/auth/login-form.tsx
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { signIn } from "next-auth/react"
import { useRouter, useSearchParams } from "next/navigation"
import { useState } from "react"

const loginSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

export function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [error, setError] = useState("")

  const form = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  })

  const onSubmit = async (data: z.infer<typeof loginSchema>) => {
    setError("")

    const result = await signIn("credentials", {
      email: data.email,
      password: data.password,
      redirect: false,
    })

    if (result?.error) {
      setError("Invalid email or password")
      return
    }

    router.push(searchParams.get("callbackUrl") || "/dashboard")
    router.refresh()
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-100 text-red-600 rounded">{error}</div>
      )}

      <div>
        <label>Email</label>
        <input type="email" {...form.register("email")} className="w-full p-2 border rounded" />
        {form.formState.errors.email && (
          <p className="text-red-500 text-sm">{form.formState.errors.email.message}</p>
        )}
      </div>

      <div>
        <label>Password</label>
        <input type="password" {...form.register("password")} className="w-full p-2 border rounded" />
        {form.formState.errors.password && (
          <p className="text-red-500 text-sm">{form.formState.errors.password.message}</p>
        )}
      </div>

      <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded">
        Sign In
      </button>

      <div className="relative my-4">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="bg-white px-2 text-gray-500">Or continue with</span>
        </div>
      </div>

      <button
        type="button"
        onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
        className="w-full py-2 border rounded flex items-center justify-center gap-2"
      >
        <GoogleIcon /> Google
      </button>
    </form>
  )
}
```

---

## 📝 Register Form

```tsx
// components/auth/register-form.tsx
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useRouter } from "next/navigation"
import { useState } from "react"

const registerSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

export function RegisterForm() {
  const router = useRouter()
  const [error, setError] = useState("")

  const form = useForm({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: z.infer<typeof registerSchema>) => {
    const res = await fetch("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    })

    if (!res.ok) {
      const error = await res.json()
      setError(error.message)
      return
    }

    router.push("/login?registered=true")
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      {/* Form fields similar to login */}
      <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded">
        Create Account
      </button>
    </form>
  )
}
```

---

## 🔒 Protected Layout

```tsx
// app/(protected)/layout.tsx
import { auth } from "@/auth"
import { redirect } from "next/navigation"

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth()

  if (!session?.user) {
    redirect("/login")
  }

  return <>{children}</>
}
```

---

## 📋 Scaffold Checklist

- [ ] NextAuth config created
- [ ] Prisma User schema updated
- [ ] Login page created
- [ ] Register page created
- [ ] Forgot password page created
- [ ] Protected layout created
- [ ] Auth forms created
- [ ] Environment variables added
- [ ] Migration run

---

**Auth ready in minutes!**
