---
name: faion-javascript-developer
description: "JavaScript/TypeScript: React, Node.js, Next.js, modern JS patterns."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# JavaScript Developer Skill

JavaScript and TypeScript development covering React, Node.js, Next.js, and modern JS ecosystem.

## Purpose

Handles all JavaScript/TypeScript development including React frontends, Node.js backends, Next.js full-stack apps, and modern JS tooling.

---

## Context Discovery

### Auto-Investigation

Detect JS/TS stack from project files:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `package.json` | `Read("package.json")` | Dependencies, scripts, type |
| React | `Grep("react", "package.json")` | React framework used |
| Next.js | `Grep("next", "package.json")` | Next.js framework |
| Express | `Grep("express", "package.json")` | Express backend |
| Fastify | `Grep("fastify", "package.json")` | Fastify backend |
| TypeScript | `Glob("**/tsconfig.json")` | TypeScript enabled |
| Bun | `Glob("**/bun.lockb")` | Bun runtime |
| ESLint config | `Glob("**/.eslintrc*")` | Linting setup |
| Jest/Vitest | `Grep("jest\|vitest", "package.json")` | Test framework |

**Read existing patterns:**
- Check src/ structure for architecture
- Read existing components for patterns
- Check tsconfig.json for strictness level

### Discovery Questions

#### Q1: Project Type

```yaml
question: "What type of JS/TS project is this?"
header: "Type"
multiSelect: false
options:
  - label: "React frontend (SPA)"
    description: "Client-side React application"
  - label: "Next.js full-stack"
    description: "Server components, API routes, SSR"
  - label: "Node.js backend"
    description: "Express, Fastify, or plain Node"
  - label: "Library/package"
    description: "Reusable npm package"
```

**Routing:**
- "React" → react-*, component architecture
- "Next.js" → nextjs-app-router, server components
- "Node.js" → nodejs-express or nodejs-fastify
- "Library" → TypeScript strict, build config

#### Q2: TypeScript Strictness

```yaml
question: "What TypeScript strictness level?"
header: "TypeScript"
multiSelect: false
options:
  - label: "Strict mode (recommended)"
    description: "Full type safety, no any"
  - label: "Standard"
    description: "Basic type checking"
  - label: "JavaScript only"
    description: "No TypeScript"
  - label: "Match existing config"
    description: "Follow tsconfig.json"
```

#### Q3: State Management (if React)

```yaml
question: "How do you manage state?"
header: "State"
multiSelect: false
options:
  - label: "React hooks (useState, useContext)"
    description: "Built-in React state"
  - label: "Zustand"
    description: "Lightweight global state"
  - label: "Redux/RTK"
    description: "Full Redux toolkit"
  - label: "Server state (React Query/SWR)"
    description: "Remote data fetching"
  - label: "Not sure / recommend"
    description: "I'll suggest based on needs"
```

---

## When to Use

- React applications (hooks, components, state)
- Node.js backends (Express, Fastify)
- Next.js full-stack applications
- TypeScript strict mode and patterns
- Modern JavaScript (ES2024+)
- Bun runtime

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **React** |
| Component architecture | React component patterns, composition | react-component-architecture.md |
| React hooks | useState, useEffect, custom hooks | react-hooks.md |
| React patterns | Modern React patterns, best practices | react-patterns.md |
| React decomposition | Breaking down React apps | decomposition-react.md |
| **Next.js** |
| Next.js App Router | App router, server components, routing | nextjs-app-router.md |
| **Node.js** |
| Node.js Express | Express.js patterns, middleware | nodejs-express.md |
| Node.js Fastify | Fastify framework, plugins, hooks | nodejs-fastify.md |
| Node.js patterns | Async patterns, error handling | nodejs-patterns.md |
| Node.js service layer | Service layer architecture | nodejs-service-layer-architecture.md |
| Node.js service implementation | Service layer implementation | nodejs-service-layer-implementation.md |
| **TypeScript** |
| TypeScript patterns | TS best practices, generics | typescript-patterns.md |
| TypeScript strict mode | Strict configuration, type safety | typescript-strict-mode.md |
| TypeScript React 2026 | TS 5.x + React 19 + Next.js 15 | typescript-react-2026.md |
| **JavaScript** |
| JavaScript basics | ES6+, async/await, modules | javascript.md |
| JavaScript modern | ES2024+ features, modern patterns | javascript-modern.md |
| JavaScript testing | Jest, Vitest patterns | javascript-testing.md |
| **Runtime** |
| Bun runtime | Bun.js patterns, performance | bun-runtime.md |
| Bun simple | Quick Bun reference | bun-runtime-simple.md |

## Tools

- **Frameworks:** React 19, Next.js 15, Express, Fastify
- **Runtime:** Node.js 20+, Bun 1.x
- **Testing:** Jest, Vitest, React Testing Library
- **Bundlers:** Vite, Turbopack, webpack
- **Package managers:** pnpm, npm, yarn, bun

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-frontend-developer | UI components, styling |
| faion-api-developer | API design and integration |
| faion-testing-developer | Testing strategies |
| faion-devtools-developer | Build tools, monorepos |

## Integration

Invoked by parent skill `faion-software-developer` when working with JavaScript/TypeScript code.

---

*faion-javascript-developer v1.0 | 18 methodologies*
