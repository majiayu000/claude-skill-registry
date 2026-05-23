---
name: arcanea-typescript-expert
description: TypeScript strict mode expert patterns for the Arcanea stack. Use when writing TypeScript types, resolving type errors, designing type-safe APIs, working with generics, discriminated unions, Zod validation, or any TypeScript-heavy work. Triggers on: TypeScript, type error, any, generic, interface, type, discriminated union, Zod, type safety, strict mode, infer. Stack: TypeScript 5.5+ strict mode, Next.js 16, Supabase typed client, Vercel AI SDK 6, Zod.
license: MIT
metadata:
  author: Arcanea
  version: "1.0.0"
  stack: TypeScript 5.5+, strict mode, Next.js 16, Zod, Supabase
---

# Arcanea TypeScript Expert

> *"Lyria guards the Sight Gate at 639 Hz — Intuition, vision. TypeScript's type system is the Sight Gate of code: it reveals what cannot be seen at runtime."*

## Arcanea's TypeScript Rules

**Non-negotiable:**
- `strict: true` in tsconfig — always
- No `any` — use `unknown` and narrow it
- No type assertions (`as`) without a comment explaining why
- All function params and returns typed explicitly in public APIs
- Zod for runtime validation of external data (API responses, form data, env vars)

---

## Core Patterns

### Discriminated Unions — Arcanea Domain Types

```typescript
// The canonical pattern for Gate states
type GateStatus =
  | { status: 'locked' }
  | { status: 'unlocked'; unlockedAt: Date; score: number }
  | { status: 'mastered'; masteredAt: Date; score: number; mastery: string }

function renderGateStatus(gate: GateStatus) {
  switch (gate.status) {
    case 'locked':
      return 'Sealed by Malachar'
    case 'unlocked':
      return `Unlocked — Score: ${gate.score}`  // score is available
    case 'mastered':
      return `Mastered — ${gate.mastery}` // mastery is available
  }
}

// Result types (no thrown errors in async functions)
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E }

async function unlockGate(userId: string, gate: GateName): Promise<Result<GateStatus>> {
  try {
    const data = await db.unlockGate(userId, gate)
    return { success: true, data }
  } catch (error) {
    return { success: false, error: error instanceof Error ? error : new Error(String(error)) }
  }
}
```

### Literal Types for Arcanea Constants

```typescript
// Use const assertions for canonical data
const GATES = [
  'foundation', 'flow', 'fire', 'heart', 'voice',
  'sight', 'crown', 'shift', 'unity', 'source'
] as const

type GateName = typeof GATES[number]
// GateName = 'foundation' | 'flow' | 'fire' | ...

const ELEMENTS = ['earth', 'water', 'fire', 'wind', 'void', 'spirit'] as const
type Element = typeof ELEMENTS[number]

const MAGIC_RANKS = ['apprentice', 'mage', 'master', 'archmage', 'luminor'] as const
type MagicRank = typeof MAGIC_RANKS[number]

const GATE_FREQUENCIES: Record<GateName, number> = {
  foundation: 174, flow: 285, fire: 396, heart: 417, voice: 528,
  sight: 639, crown: 741, shift: 852, unity: 963, source: 1111,
}
```

### Branded Types — Prevent ID mixing

```typescript
// Prevent passing userId where gateId is expected
type UserId = string & { readonly __brand: 'UserId' }
type GuardianId = string & { readonly __brand: 'GuardianId' }
type PromptId = string & { readonly __brand: 'PromptId' }

function toUserId(id: string): UserId { return id as UserId }
function toGuardianId(id: string): GuardianId { return id as GuardianId }

// Functions are now type-safe against ID mixing
async function getUserProgress(userId: UserId): Promise<GateStatus[]> { ... }
async function getGuardian(guardianId: GuardianId): Promise<Guardian> { ... }

// This would be a compile error:
getUserProgress(toGuardianId('abc')) // Error: GuardianId is not UserId
```

### Generic Utilities

```typescript
// DeepPartial for nested update types
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T

// Pick with required — make subset of fields required
type RequiredPick<T, K extends keyof T> = Required<Pick<T, K>> & Omit<T, K>

// Paginated response type
type Paginated<T> = {
  data: T[]
  total: number
  page: number
  pageSize: number
  hasMore: boolean
}

// Async function return type extraction
type Awaited<T> = T extends Promise<infer U> ? U : T

// Extract Supabase row type
import type { Database } from '@/types/supabase'
type GuardianRow = Database['public']['Tables']['guardians']['Row']
type GuardianInsert = Database['public']['Tables']['guardians']['Insert']
type GuardianUpdate = Database['public']['Tables']['guardians']['Update']
```

---

## Zod — Runtime Validation

### API Route Validation
```typescript
// app/api/unlock-gate/route.ts
import { z } from 'zod'
import { NextRequest, NextResponse } from 'next/server'

const UnlockGateSchema = z.object({
  gate: z.enum(['foundation','flow','fire','heart','voice','sight','crown','shift','unity','source']),
  score: z.number().int().min(0).max(100),
  completedAt: z.string().datetime().optional(),
})

type UnlockGateInput = z.infer<typeof UnlockGateSchema>

export async function POST(req: NextRequest) {
  const body = await req.json()
  const parsed = UnlockGateSchema.safeParse(body)
  
  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Invalid request', details: parsed.error.flatten() },
      { status: 400 }
    )
  }
  
  const { gate, score } = parsed.data // fully typed
  // ...
}
```

### Environment Variables — Type-safe
```typescript
// lib/env.ts — validate at startup, not at use
import { z } from 'zod'

const EnvSchema = z.object({
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),
  NEXT_PUBLIC_APP_URL: z.string().url().default('http://localhost:3000'),
})

export const env = EnvSchema.parse(process.env)
// env.NEXT_PUBLIC_SUPABASE_URL is always a valid URL string
```

### Form Data Validation
```typescript
// lib/validations/gate-quiz.ts
import { z } from 'zod'

export const GateQuizAnswerSchema = z.object({
  questionId: z.string().uuid(),
  selectedOption: z.number().int().min(0).max(3),
  timeSpent: z.number().positive(), // seconds
})

export const GateQuizSubmissionSchema = z.object({
  gate: z.enum(['foundation','flow','fire','heart','voice','sight','crown','shift','unity','source']),
  answers: z.array(GateQuizAnswerSchema).min(1).max(20),
  startedAt: z.string().datetime(),
})

export type GateQuizSubmission = z.infer<typeof GateQuizSubmissionSchema>
```

---

## Narrowing — No More `any`

```typescript
// Type guard pattern
function isGuardian(value: unknown): value is Guardian {
  return (
    typeof value === 'object' &&
    value !== null &&
    'gate' in value &&
    'name' in value &&
    'frequency_hz' in value
  )
}

// Exhaustive checks
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(x)}`)
}

function getElementColor(element: Element): string {
  switch (element) {
    case 'earth': return '#4a7c59'
    case 'water': return '#78a6ff'
    case 'fire': return '#ff6b35'
    case 'wind': return '#e8e8e8'
    case 'void': return '#8b5cf6'
    case 'spirit': return '#ffd700'
    default: return assertNever(element) // compile error if new element added
  }
}
```

---

## React + TypeScript Patterns

### Component Props with Variants
```typescript
// Discriminated union props for flexible components
type GuardianCardProps =
  | { variant: 'compact'; guardian: Pick<Guardian, 'name' | 'gate' | 'element'> }
  | { variant: 'full'; guardian: Guardian; onUnlock?: () => void }
  | { variant: 'loading' }

function GuardianCard(props: GuardianCardProps) {
  if (props.variant === 'loading') return <GlassCardSkeleton />
  if (props.variant === 'compact') return <CompactView guardian={props.guardian} />
  return <FullView guardian={props.guardian} onUnlock={props.onUnlock} />
}
```

### Server Component typed params (Next.js 16)
```typescript
// Next.js 16: params are Promises
type PageProps = {
  params: Promise<{ gate: GateName }>
  searchParams: Promise<{ tab?: string }>
}

export default async function GatePage({ params, searchParams }: PageProps) {
  const { gate } = await params
  const { tab } = await searchParams
  // ...
}
```

### Typed event handlers
```typescript
import type { ChangeEvent, FormEvent, KeyboardEvent } from 'react'

// Explicit event types — no implicit any
function handleChange(e: ChangeEvent<HTMLInputElement>) {
  setValue(e.target.value)
}

function handleSubmit(e: FormEvent<HTMLFormElement>) {
  e.preventDefault()
  const data = new FormData(e.currentTarget)
}
```

---

## tsconfig.json — Arcanea Baseline

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "module": "esnext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Extra flags explained:**
- `noUncheckedIndexedAccess`: `arr[0]` is `T | undefined`, not `T`
- `exactOptionalPropertyTypes`: `{ a?: string }` means the key may not exist — not `string | undefined`
- `noImplicitReturns`: all code paths in functions must return
- `noFallthroughCasesInSwitch`: prevents missing `break` bugs

---

## Quick Checklist

Before any TypeScript PR in Arcanea:

- [ ] No `any` — use `unknown` + narrowing or proper types
- [ ] No `as` without a comment justifying the assertion
- [ ] External data (API, form, env) validated with Zod
- [ ] Discriminated unions for state machines (gate status, auth state)
- [ ] `const GATES = [...] as const` for canonical enum-like arrays
- [ ] Supabase typed client used (Database generic)
- [ ] Next.js 16 params typed as `Promise<{ ... }>`
- [ ] `assertNever` on switch default for exhaustive checks
