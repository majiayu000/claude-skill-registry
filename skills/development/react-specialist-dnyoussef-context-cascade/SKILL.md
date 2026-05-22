/*============================================================================*/
/* REACT-SPECIALIST SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: react-specialist
version: 1.0.0
description: |
  [assert|neutral] Modern React development specialist for React 18+ with hooks, context, suspense, server components (Next.js 13+), state management (Redux/Zustand/Jotai), performance optimization (React.memo, useMemo, [ground:given] [conf:0.95] [state:confirmed]
category: Frontend Specialists
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute react-specialist workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic Frontend Specialists processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "react-specialist",
  category: "Frontend Specialists",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["react-specialist", "Frontend Specialists", "workflow"],
  context: "user needs react-specialist capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# React Specialist

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Expert React development for modern, performant, and maintainable frontend applications.

## Purpose

Provide comprehensive React expertise including React 18+ features (concurrent rendering, suspense, server components), performance optimization, state management patterns, and production-grade component architecture. Ensures React applications follow best practices and leverage the latest React capabilities.

## When to Use This Skill

- Building React applications with modern patterns
- Optimizing React performance (re-renders, bundle size, lazy loading)
- Implementing complex state management (global state, server state)
- Creating reusable component libraries with TypeScript
- Migrating to React 18+ or Next.js App Router
- Setting up React testing with React Testing Library and Jest
- Implementing accessibility (a11y) in React components

## Prerequisites

**Required**: JavaScript ES6+, TypeScript basics, HTML/CSS, npm/yarn/pnpm

**Agent Assignments**: `coder` (implementation), `tester` (React Testing Library), `mobile-dev` (React Native if needed)

## Core Workflows

### Workflow 1: Next.js 13+ App Router with Server Components

**Step 1: Initialize Next.js Project**

```bash
npx create-next-app@latest my-app --typescript --tailwind --app --no-src-dir
cd my-app
pnpm install
```

**Step 2: Create Server Component (RSC)**

```tsx
// app/users/page.tsx (Server Component by default)
import { Suspense } from 'react';
import { UserList } from './user-list';
import { UserSkeleton } from './user-skeleton';

async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 60 } // ISR: revalidate every 60s
  });
  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();

  return (
    <main>
      <h1>Users</h1>
      <Suspense fallback={<UserSkeleton />}>
        <UserList users={users} />
      </Suspense>
    </main>
  );
}
```

**Step 3: Create Client Component with Interactivity**

```tsx
// app/users/user-list.tsx
'use client'; // Marks as Client Component

import { useState } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

export function UserList({ users }: { users: User[] }) {
  const [filter, setFilter] = useState('');

  const filtered = users.filter(u =>
    u.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Filter users..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="border p-2 mb-4"
      />
      <ul>
        {filtered.map(user => (
          <li key={user.id}>{user.name} ({user.email})</li>
        ))}
      </ul>
    </div>
  );
}
```

**Step 4: Implement Server Actions**

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  await fetch('https://api.example.com/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email }),
  });

  revalidatePath('/users'); // Revalidate users page
}
```

### Workflow 2: State Management with Zustand

**Step 1: Install Zustand**

```bash
pnpm add zustand
```

**Step 2: Create Type-Safe Store**

```tsx
// stores/user-store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface User {
  id: number;
  name: string;
}

interface UserState {
  users: User[];
  addUser: (user: User) => void;
  removeUser: (id: number) => void;
  clearUsers: () => void;
}

export const useUserStore = create<UserState>()(
  devtools(
    persist(
      (set) => ({
        users: [],
        addUser: (user) => set((state) => ({
          users: [...state.users,

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/Frontend Specialists/react-specialist/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "react-specialist-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>REACT_SPECIALIST_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
