---
name: code-wizard
description: Codebase exploration and location finder for the Raamattu Nyt monorepo. Use when finding where specific functionality is implemented, locating constants/tokens/config values, discovering file patterns, or answering "where is X coded?" questions. Helps other skills and agents locate code quickly.
---

# Code Wizard

Find what-is-where in the Raamattu Nyt monorepo.

## Context Files (Read First)

For structure and layout, read from `Docs/context/`:
- `Docs/context/repo-structure.md` - Full directory layout
- `Docs/context/packages-map.md` - Package boundaries and imports

## Quick Directory Map

```
raamattu-nyt/
├── apps/
│   ├── raamattu-nyt/src/      # Main Bible app
│   │   ├── pages/             # Route components
│   │   ├── components/        # UI components
│   │   ├── hooks/             # React hooks
│   │   ├── lib/               # Business logic, services
│   │   └── integrations/      # External services (Supabase)
│   └── idea-machina/     # AI prompting app
├── packages/
│   ├── ui/                    # Shared shadcn components
│   ├── shared-auth/           # Auth hooks, session
│   ├── shared-content/        # Shared content utils
│   ├── shared-history/        # Reading history
│   ├── shared-voice/          # Audio/TTS
│   └── ai/                    # AI utilities
├── supabase/
│   ├── migrations/            # Database DDL
│   └── functions/             # Edge Functions
└── Docs/                      # Project documentation
```

## Common Search Patterns

### Find Constants/Tokens

```bash
# Static string tokens
grep -r "const.*TOKEN\|const.*KEY\|const.*SECRET" --include="*.ts" --include="*.tsx"

# Environment variables
grep -r "import.meta.env\|process.env\|Deno.env" --include="*.ts" --include="*.tsx"

# Query keys (React Query)
grep -r "queryKey.*\[" --include="*.ts" --include="*.tsx"
```

### Find Feature Implementation

```bash
# Hooks
grep -r "export.*function use\|export const use" --include="*.ts" --include="*.tsx"

# Services
grep -r "export.*async function\|export const.*= async" apps/raamattu-nyt/src/lib/

# Components
grep -r "export.*const.*=.*\(\)" apps/raamattu-nyt/src/components/
```

### Find Database/API Usage

```bash
# Supabase table queries
grep -r "\.from\(['\"]" --include="*.ts" --include="*.tsx"

# RPC function calls
grep -r "\.rpc\(['\"]" --include="*.ts" --include="*.tsx"

# Edge Function invocations
grep -r "functions.invoke\|/functions/v1/" --include="*.ts"
```

## Where Things Are

### By Feature Type

| Looking For | Location | Pattern |
|-------------|----------|---------|
| React hooks | `apps/*/src/hooks/` | `use*.ts` |
| UI components | `apps/*/src/components/` | `*.tsx` |
| Page routes | `apps/*/src/pages/` | `*Page.tsx` |
| Business logic | `apps/*/src/lib/` | `*Service.ts` |
| Supabase types | `apps/*/src/integrations/supabase/` | `types.ts` |
| DB migrations | `supabase/migrations/` | `*.sql` |
| Edge Functions | `supabase/functions/` | `*/index.ts` |
| Shared UI | `packages/ui/src/` | `*.tsx` |
| Auth logic | `packages/shared-auth/` | `*.ts` |

### By Domain

| Domain | Key Files |
|--------|-----------|
| Bible text | `lib/bibleService.ts`, `lib/verseParser.ts`, `lib/searchService.ts` |
| Audio/TTS | `lib/audioService.ts`, `packages/shared-voice/` |
| AI features | `lib/aiSummaryService.ts`, `hooks/useAIQuota.ts`, `supabase/functions/ai-orchestrator/` |
| Topics | `lib/topicEditorUtils.ts`, `pages/TopicPage.tsx`, `pages/AdminTopicsPage.tsx` |
| User data | `hooks/useFeedback.ts`, `lib/activityLogger.ts` |
| Admin | `pages/Admin*.tsx`, `components/admin/` |

## Useful Grep Commands

### Find All Query Keys
```bash
grep -roh "queryKey: \[.*\]" apps/ | sort -u
```

### Find All Routes
```bash
grep -r "path=\"/\|<Route" apps/raamattu-nyt/src/App.tsx
```

### Find All Supabase Tables Used
```bash
grep -roh "\.from(['\"][^'\"]*['\"])" apps/ | sort -u
```

### Find All RPC Functions Called
```bash
grep -roh "\.rpc(['\"][^'\"]*['\"])" apps/ | sort -u
```

### Find Environment Variables
```bash
grep -roh "import\.meta\.env\.[A-Z_]*\|Deno\.env\.get(['\"][^'\"]*['\"])" . | sort -u
```

### Find Exports from a File
```bash
grep "^export" <file_path>
```

## References

- **File locations by feature**: See [references/locations.md](references/locations.md)
- **Search patterns cookbook**: See [references/patterns.md](references/patterns.md)
