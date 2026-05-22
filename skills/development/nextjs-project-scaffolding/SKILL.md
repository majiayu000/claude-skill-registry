---
name: nextjs-project-scaffolding
version: "1.0"
description: >
  Opinionated Next.js 14+ project structure and configuration for scaffolding new projects.
  PROACTIVELY activate for: (1) setting up new Next.js projects, (2) configuring tsconfig.json with strict mode, (3) establishing folder structure patterns.
  Triggers: "new project", "scaffold", "project structure"
group: foundation
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Next.js Project Scaffolding

## Recommended Folder Structure

```
project-root/
├── src/
│   ├── app/                 # Next.js App Router (routes, layouts, pages)
│   │   ├── api/            # API route handlers
│   │   ├── actions/        # Server Actions
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Home page
│   ├── components/
│   │   ├── ui/             # Reusable UI components
│   │   ├── forms/          # Form components
│   │   └── layouts/        # Layout components (headers, footers)
│   ├── lib/
│   │   ├── utils/          # Utility functions
│   │   └── validations/    # Zod schemas
│   ├── types/
│   │   ├── api/            # API types
│   │   └── models/         # Data model types
│   ├── hooks/              # Custom React hooks
│   └── styles/             # Global styles
├── public/                  # Static assets
├── docs/
│   └── adr/                # Architecture Decision Records
├── tsconfig.json           # TypeScript config (strict mode)
├── next.config.js          # Next.js config
├── .env.local              # Environment variables (gitignored)
└── .env.example            # Environment variable template
```

## Key Configuration: tsconfig.json (Strict Mode)

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "target": "ES2022",
    "lib": ["ES2022", "dom", "dom.iterable"],
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Critical settings**:
- `"strict": true` - Enables all strict type-checking
- `"noUncheckedIndexedAccess": true` - Array access returns `T | undefined`
- `"@/*"` path alias for clean imports

## Baseline Dependencies

**Production**:
- `next@^14.0.0`
- `react@^18.2.0`
- `typescript@^5.3.0`
- `zod@^4.1.12` (validation)
- `zustand@^5.0.2` (state management)

**Development**:
- `prettier@^3.0.0`
- `eslint-config-prettier`
- `@types/node@^20`

## Rationale for `/src` Directory

Using the `/src` directory:
- **Separates** source code from configuration files (cleaner root)
- **Standard convention** in modern Next.js projects
- **Improves** project navigation and organization

## For More Details

For full project setup including environment variables, scripts, and step-by-step instructions, reference the `/setup-project` command or see the complete template in `skills/nextjs-project-scaffolding/resources/full-template.md`.
