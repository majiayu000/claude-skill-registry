---
name: nextjs
description: Next.js development including App Router, Server Components, API routes, and deployment. Activate for Next.js apps, SSR, SSG, and React Server Components.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Next.js Skill

Provides comprehensive Next.js development capabilities for modern web applications.

## When to Use This Skill

Activate this skill when working with:
- Next.js App Router
- Server Components and Client Components
- API Routes and Server Actions
- Static Site Generation (SSG)
- Server-Side Rendering (SSR)

## Project Structure (App Router)

\`\`\`
app/
├── layout.tsx              # Root layout
├── page.tsx                # Home page
├── loading.tsx             # Loading UI
├── error.tsx               # Error handling
├── not-found.tsx           # 404 page
├── globals.css
├── agents/
│   ├── page.tsx           # /agents
│   ├── [id]/
│   │   ├── page.tsx       # /agents/[id]
│   │   └── edit/
│   │       └── page.tsx   # /agents/[id]/edit
│   └── new/
│       └── page.tsx       # /agents/new
├── api/
│   └── agents/
│       ├── route.ts       # /api/agents
│       └── [id]/
│           └── route.ts   # /api/agents/[id]
└── (dashboard)/           # Route group
    ├── layout.tsx
    └── settings/
        └── page.tsx
\`\`\`

## Server Components (Default)

\`\`\`tsx
// app/agents/page.tsx - Server Component
async function AgentsPage() {
  // Direct database access (no API needed)
  const agents = await db.query('SELECT * FROM agents');

  return (
    <div>
      <h1>Agents</h1>
      <ul>
        {agents.map(agent => (
          <li key={agent.id}>{agent.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default AgentsPage;
\`\`\`

## Client Components

\`\`\`tsx
// components/AgentSelector.tsx
'use client';

import { useState } from 'react';

export function AgentSelector({ agents }: { agents: Agent[] }) {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <select
      value={selected || ''}
      onChange={(e) => setSelected(e.target.value)}
    >
      <option value="">Select an agent</option>
      {agents.map(agent => (
        <option key={agent.id} value={agent.id}>
          {agent.name}
        </option>
      ))}
    </select>
  );
}
\`\`\`

## Data Fetching

### Server Component Data Fetching
\`\`\`tsx
// Automatic request deduplication
async function getAgent(id: string) {
  const res = await fetch(`${process.env.API_URL}/agents/${id}`, {
    cache: 'force-cache',      // Default: cache forever
    // cache: 'no-store',      // Never cache
    // next: { revalidate: 60 } // Revalidate every 60s
  });
  return res.json();
}

export default async function AgentPage({ params }: { params: { id: string } }) {
  const agent = await getAgent(params.id);
  return <AgentDetails agent={agent} />;
}
\`\`\`

### Revalidation
\`\`\`tsx
// Time-based revalidation
export const revalidate = 60; // Revalidate every 60 seconds

// On-demand revalidation
import { revalidatePath, revalidateTag } from 'next/cache';

async function updateAgent(id: string, data: FormData) {
  'use server';
  await db.update('agents', id, data);
  revalidatePath('/agents');
  revalidateTag('agents');
}
\`\`\`

## Server Actions

\`\`\`tsx
// app/agents/new/page.tsx
import { redirect } from 'next/navigation';

async function createAgent(formData: FormData) {
  'use server';

  const name = formData.get('name') as string;
  const type = formData.get('type') as string;

  await db.insert('agents', { name, type });

  revalidatePath('/agents');
  redirect('/agents');
}

export default function NewAgentPage() {
  return (
    <form action={createAgent}>
      <input name="name" placeholder="Agent name" required />
      <select name="type">
        <option value="claude">Claude</option>
        <option value="gpt">GPT</option>
      </select>
      <button type="submit">Create Agent</button>
    </form>
  );
}
\`\`\`

## API Routes

\`\`\`tsx
// app/api/agents/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const type = searchParams.get('type');

  const agents = await db.query(
    'SELECT * FROM agents WHERE type = $1',
    [type]
  );

  return NextResponse.json(agents);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const agent = await db.insert('agents', body);

  return NextResponse.json(agent, { status: 201 });
}

// app/api/agents/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const agent = await db.query('SELECT * FROM agents WHERE id = $1', [params.id]);

  if (!agent) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json(agent);
}
\`\`\`

## Layouts and Loading States

\`\`\`tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <nav>Navigation</nav>
        <main>{children}</main>
        <footer>Footer</footer>
      </body>
    </html>
  );
}

// app/agents/loading.tsx
export default function Loading() {
  return <div className="spinner">Loading agents...</div>;
}

// app/agents/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
\`\`\`

## Middleware

\`\`\`tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Authentication check
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');

  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
\`\`\`

## Environment Variables

\`\`\`bash
# .env.local
DATABASE_URL=postgresql://...
API_URL=http://localhost:8000

# Public (exposed to browser)
NEXT_PUBLIC_APP_URL=http://localhost:3000
\`\`\`

\`\`\`tsx
// Server-only
const dbUrl = process.env.DATABASE_URL;

// Client-accessible
const appUrl = process.env.NEXT_PUBLIC_APP_URL;
\`\`\`

## Build Commands

\`\`\`bash
# Development
npm run dev

# Production build
npm run build
npm start

# Static export
npm run build
# next.config.js: output: 'export'
\`\`\`
