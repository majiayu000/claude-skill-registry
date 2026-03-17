---
name: web-nextjs
cluster: web-dev
description: "Next.js 15: App Router, server actions, ISR/SSG/SSR, middleware, turbopack, Vercel deployment"
tags: ["nextjs","react","fullstack","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "nextjs app router server components ssr ssg deployment turbopack"
---

# web-nextjs

## Purpose
This skill provides expertise in building and deploying web applications with Next.js 15, focusing on modern features like App Router, server actions, and optimized rendering strategies.

## When to Use
Use this skill for projects requiring fast, SEO-friendly React apps with server-side logic; ideal for e-commerce sites needing SSR, blogs with SSG, or dynamic apps with ISR; avoid for simple static sites where plain React suffices.

## Key Capabilities
- App Router: Enables file-based routing in the /app directory for better organization; example: create a route with app/about/page.jsx.
- Server Actions: Perform mutations on the server without API routes; define as async functions in forms, e.g., 'use server' directive in components.
- ISR/SSG/SSR: Configure ISR via revalidatePath() in server actions; SSG with getStaticProps; SSR with getServerSideProps for dynamic data fetching.
- Middleware: Write edge functions in middleware.js to handle authentication or redirects, e.g., checking user sessions before page loads.
- Turbopack: Speeds up development with incremental bundling; enable via next.config.js with experimental: { turbopack: true }.
- Vercel Deployment: Deploy apps with zero-config via Vercel CLI; supports automatic ISR invalidation through webhooks.

## Usage Patterns
To build a Next.js app, start by creating a project: run `npx create-next-app@latest my-app --typescript` and navigate to the /app directory for routing. For server actions, import and use them in forms: e.g., in a component, add `async function addItem() { 'use server'; await db.insert(item); }`. Implement SSR by exporting getServerSideProps from a page: export async function getServerSideProps() { const data = await fetchData(); return { props: { data } }; }. For ISR, use revalidate in actions: e.g., revalidatePath('/posts') after updating content. Example 1: Build a blog with SSG—create app/posts/[id]/page.jsx with getStaticProps to fetch posts, then run `next build` for static output. Example 2: Add authentication middleware—create middleware.js with export function middleware(request) { if (!request.cookies.token) return NextResponse.redirect('/login'); } and test with `next dev`.

## Common Commands/API
- Create project: `npx create-next-app@latest my-app --app` to use App Router; add --typescript for TypeScript support.
- Development server: `next dev --port 3001` to run on a specific port with hot reloading.
- Build and deploy: `next build` for production build, then `vercel --prod` for deployment; use Vercel API endpoint like POST https://api.vercel.com/v13/now/deployments?teamId=$VERCEL_TEAM_ID with JSON body { "name": "my-app" }.
- API routes: Define in app/api/route.js, e.g., export async function GET(request) { const data = await fetch('https://api.example.com'); return Response.json(data); }.
- Config formats: Edit next.config.js for custom settings, e.g., module.exports = { images: { domains: ['example.com'] }, experimental: { appDir: true } }; use .env.local for env vars like NEXT_PUBLIC_API_URL="https://api.example.com".
- Turbopack commands: Enable in next.config.js and run `next dev` for faster iterations.

## Integration Notes
Integrate databases like PostgreSQL via Prisma: install @prisma/client, run `npx prisma migrate dev`, and use in server actions with env var $DATABASE_URL for connection strings. For auth, use NextAuth.js: install next-auth, configure in [...nextauth].js, and set $NEXTAUTH_SECRET in .env; example: import NextAuth from 'next-auth'; export default NextAuth({ providers: [] }). Link with Vercel for CI/CD by adding vercel.json with { "routes": [{ "src": "/api/(.*)", "dest": "/api/$1" }] }. If API keys are needed, store as env vars like $STRIKE_API_KEY and access via process.env.STRIKE_API_KEY in components.

## Error Handling
Handle 404s by creating app/404.js with a custom page: export default function NotFound() { return <h1>404 - Page Not Found</h1>; }. Use error boundaries in components: wrap with <ErrorBoundary fallback={<div>Error occurred</div>}>; in App Router, add error.js files per route. For build errors, check next.config.js for misconfigurations; common fix: ensure all imports are correct in server components. Debug SSR issues by running `next build --debug` and inspecting logs; for API errors, use try/catch in actions, e.g., try { await fetchData(); } catch (error) { console.error(error.message); return NextResponse.json({ error: 'Fetch failed' }, { status: 500 }); }.

## Graph Relationships
- Related to cluster: web-dev (e.g., shares resources with other web-dev skills like frontend-react).
- Connected via tags: nextjs (links to advanced-react skills), react (integrates with state-management tools), fullstack (overlaps with backend-node skills), web (connects to deployment-vercel skills).
