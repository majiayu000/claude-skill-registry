---
name: task
description: Execute complex tasks with planning, parallel subagents, atomic commits, and documentation updates. Use when the user asks to implement a feature, refactor code, or complete multi-step work.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, TodoWrite
---

# Task Skill - Worker

**This skill does the actual implementation work. It is invoked by subagents from /feature and /fix-pr.**

---

## Step 1: Read Project Context (MANDATORY)

Before any implementation, understand the project:

```
wouterwisse.com/                # Next.js personal website
├─ src/
│  ├─ app/                     # Next.js app router (pages, layouts)
│  ├─ components/              # React components
│  ├─ config/                  # Configuration files (themes, etc.)
│  ├─ hooks/                   # Custom React hooks
│  ├─ types/                   # TypeScript type definitions
│  └─ utils/                   # Utility functions
├─ public/                     # Static assets
└─ scripts/                    # Image generation scripts
```

Key files to reference:
- `src/config/` - Theme colors, blur placeholders, settings
- `src/hooks/` - Custom hooks for time, theme, etc.
- `src/components/` - Reusable UI components

---

## Step 2: Determine Testing Requirements

| Code Type | Testing Requirement |
|-----------|---------------------|
| Utility functions, hooks with logic | Unit tests recommended |
| Complex components with state | Unit tests recommended |
| Simple components, pages | Manual testing sufficient |
| Config, scripts, styling | No tests required |

---

## Step 3: If TDD Required (Red-Green-Refactor)

Follow this cycle strictly:

1. **RED**: Write failing test FIRST
2. **Run test** → Verify it FAILS (if it passes, test is wrong)
3. **GREEN**: Implement minimum code to pass
4. **Run test** → Verify it PASSES
5. **REFACTOR**: Clean up while keeping tests green

---

## Step 4: Make Changes

- Follow existing patterns in the codebase
- Copy patterns from similar implementations
- Do NOT invent new patterns
- Keep changes focused on the task scope

### Tech Stack Reference

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS 4
- **Animation**: Framer Motion
- **State**: React hooks (useState, useEffect, etc.)

### Patterns to Follow

**Pages** (`app/*/page.tsx`):
```typescript
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title',
}

export default function Page() {
  return (
    <main>
      {/* Content */}
    </main>
  )
}
```

**Server Components** (default in app/):
```typescript
export default async function Component() {
  // Can use async/await, access server resources
  return <div>...</div>
}
```

**Client Components**:
```typescript
'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

export function Component() {
  const [state, setState] = useState()
  // ...
}
```

**Custom Hooks** (`hooks/*.ts`):
```typescript
import { useState, useEffect } from 'react'

export function useCustomHook() {
  const [value, setValue] = useState()

  useEffect(() => {
    // Effect logic
  }, [])

  return value
}
```

---

## Step 5: Quality Checks (MANDATORY before commit)

Run these checks and fix any violations:

```bash
# TypeScript check
npx tsc --noEmit

# Lint check
npm run lint

# Check for forbidden patterns
grep -rn 'TODO\|FIXME\|HACK' --include='*.ts' --include='*.tsx' src/
```

Also verify:
- Build passes: `npm run build`
- No uncommitted debug code (console.log in production code)
- No hardcoded secrets or API keys

---

## Step 6: Create Atomic Commit (NO PUSH)

```bash
git add -A && git commit -m "<type>(<scope>): <description>"
```

**Commit types:** feat, fix, refactor, test, docs, chore, style

**IMPORTANT:** Do NOT push. Commits are collected and pushed once at the end by the orchestrator skill (/feature or /fix-pr). This reduces GitHub Action triggers.

---

## Step 7: Build & Lint Verification

```bash
# TypeScript compilation
npx tsc --noEmit

# Lint
npm run lint

# Build (includes type checking)
npm run build
```

---

## Output Format

When called by an orchestrator skill, return this structured summary:

```yaml
---
STATUS: SUCCESS | FAILURE
COMMIT: [short hash, e.g., abc1234]
FILES_CHANGED:
  - [file1]
  - [file2]
BUILD: PASSED | FAILED
LINT: PASSED | FAILED
TESTS: PASSED | FAILED | SKIPPED
TDD_FOLLOWED: true | false | N/A
ERRORS: [if FAILURE, list specific errors - NOT full logs]
---
```

---

## Handling Failures

If something fails:
1. Read the error message carefully
2. Fix the issue
3. Re-run the failing step
4. If still failing after 2 attempts, report the specific error

---

## Escalation

**Stop and ask for help if:**
- Task requires new dependencies you're unsure about
- Task conflicts with existing patterns
- Requirements are ambiguous

---

## Key Principles

1. **Understand context first** - read existing code before changing
2. **TDD for logic** - tests before implementation
3. **Quality checks** - no TODOs, no lint errors
4. **Atomic commits** - one logical change per commit
5. **Never push** - orchestrator pushes once at the end
6. **Follow patterns** - copy existing code, don't invent

---

## Example Subagent Prompt

```
Implement the new theme toggle component.

Context:
- This is step 2 of 4 in adding theme support
- The project uses Next.js with TypeScript
- Framer Motion is available for animations

Task:
- Create src/components/ThemeToggle.tsx
- Use the existing useTheme hook from src/hooks/
- Follow patterns from src/components/

Do NOT commit - just implement and verify it works.
```
