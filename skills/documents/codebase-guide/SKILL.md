---
name: codebase-guide
description: Master guide for this TanStack Start e-commerce application. Use when onboarding, exploring architecture, or needing context about how systems connect.
---

# Codebase Guide

Master reference for this TanStack Start e-commerce application.

## Quick Reference

| Need                | Skill        |
| ------------------- | ------------ |
| Create API endpoint | `api-routes` |
| Build admin page    | `admin-crud` |
| Add form            | `forms`      |
| Modify database     | `database`   |
| Add translations    | `i18n`       |
| Write tests         | `testing`    |
| Fix checkout issues | `checkout`   |
| Security review     | `security`   |
| Debug issues        | `debugging`  |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend                                 │
├──────────────────┬──────────────────┬──────────────────────────┤
│   Customer UI    │    Admin UI      │      Shared UI           │
│   /$lang/*       │    /admin/*      │   /components/ui/*       │
│                  │                  │                          │
│  • Product pages │  • Dashboard     │  • Button, Input, Card   │
│  • Cart/Checkout │  • Orders table  │  • Dialog, Badge, Tabs   │
│  • Account       │  • Product CRUD  │  • FNForm (forms)        │
└────────┬─────────┴────────┬─────────┴────────────┬─────────────┘
         │                  │                      │
         ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      State Management                            │
├──────────────────┬──────────────────┬──────────────────────────┤
│     Zustand      │   React Query    │    TanStack Form         │
│                  │                  │                          │
│  • useCartStore  │  • Server state  │  • Form validation       │
│  • useAuthStore  │  • Caching       │  • Field management      │
│  • localStorage  │  • Mutations     │  • Submit handling       │
└────────┬─────────┴────────┬─────────┴────────────┬─────────────┘
         │                  │                      │
         ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API Layer                                  │
│                    /routes/api/*                                 │
├──────────────────┬──────────────────┬──────────────────────────┤
│   Auth APIs      │   CRUD APIs      │    Webhooks              │
│                  │                  │                          │
│  • /auth/login   │  • /products     │  • /webhooks/stripe      │
│  • /auth/logout  │  • /orders       │  • /webhooks/paypal      │
│  • /auth/me      │  • /customers    │                          │
└────────┬─────────┴────────┬─────────┴────────────┬─────────────┘
         │                  │                      │
         ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Server Layer                                 │
│                      /src/server/*                               │
├──────────────────┬──────────────────┬──────────────────────────┤
│   Business Logic │   Utilities      │    Integrations          │
│                  │                  │                          │
│  • orders.ts     │  • auth.ts       │  • stripe.ts             │
│  • products.ts   │  • api.ts        │  • paypal.ts             │
│  • checkout.ts   │  • rate-limit.ts │  • cloudinary.ts         │
└────────┬─────────┴────────┬─────────┴────────────┬─────────────┘
         │                  │                      │
         ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer                              │
│                  Drizzle ORM + PostgreSQL                        │
├──────────────────┬──────────────────┬──────────────────────────┤
│   Auth Tables    │   Store Tables   │    Order Tables          │
│                  │                  │                          │
│  • users         │  • products      │  • orders                │
│  • sessions      │  • variants      │  • orderItems            │
│  • customers     │  • collections   │  • checkouts             │
└──────────────────┴──────────────────┴──────────────────────────┘
```

## Tech Stack

| Layer        | Technology                   | Purpose                       |
| ------------ | ---------------------------- | ----------------------------- |
| Framework    | TanStack Start               | SSR/SSG with Vite + Nitro     |
| Router       | TanStack Router              | File-based routing            |
| Database     | Drizzle + PostgreSQL         | Type-safe ORM                 |
| State        | Zustand                      | Client state with persistence |
| Server State | React Query                  | Caching, mutations            |
| Forms        | TanStack Form + FNForm       | Validation, field management  |
| UI           | Radix + shadcn + Tailwind v4 | Accessible components         |
| i18n         | i18next                      | Multi-language (en, fr, id)   |
| Payments     | Stripe + PayPal              | Checkout processing           |
| Media        | Cloudinary                   | Image upload/optimization     |
| Email        | SendGrid                     | Transactional emails          |

## Directory Structure

```
src/
├── routes/                    # File-based routing
│   ├── $lang/                 # Localized customer pages
│   │   ├── index.tsx          # Homepage
│   │   ├── products/          # Product catalog
│   │   ├── cart.tsx           # Shopping cart
│   │   ├── checkout/          # Checkout flow
│   │   └── account/           # Customer account
│   ├── admin/                 # Admin dashboard
│   │   ├── index.tsx          # Dashboard home
│   │   ├── products/          # Product management
│   │   ├── orders/            # Order management
│   │   └── login.tsx          # Admin login
│   └── api/                   # REST API endpoints
│       ├── auth/              # Authentication
│       ├── products/          # Product CRUD
│       ├── orders/            # Order management
│       ├── checkout/          # Checkout flow
│       └── webhooks/          # Payment webhooks
├── components/
│   ├── ui/                    # Reusable UI (shadcn pattern)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── fn-form.tsx        # Centralized form component
│   │   └── ...
│   ├── admin/                 # Admin-specific components
│   │   ├── products/          # Product management UI
│   │   ├── orders/            # Order management UI
│   │   └── media/             # Media library
│   └── checkout/              # Checkout components
├── hooks/
│   ├── useAuth.ts             # Authentication state
│   ├── useCart.ts             # Cart state (Zustand)
│   ├── useCheckout.ts         # Checkout state
│   └── useDataTable.ts        # Admin table state
├── lib/
│   ├── auth.ts                # Auth utilities
│   ├── api.ts                 # Response helpers
│   ├── stripe.ts              # Stripe client
│   ├── paypal.ts              # PayPal client
│   ├── rate-limit.ts          # Rate limiting
│   ├── csrf.ts                # CSRF protection
│   ├── i18n.ts                # i18n setup
│   └── utils.ts               # General utilities
├── db/
│   ├── index.ts               # Database client
│   └── schema.ts              # Drizzle schema
├── server/
│   ├── orders.ts              # Order business logic
│   └── products.ts            # Product business logic
└── i18n/
    └── locales/               # Translation files
        ├── en.json
        ├── fr.json
        └── id.json
```

## Key Patterns

### 1. API Routes

All API routes use TanStack Router server handlers:

```typescript
export const Route = createFileRoute('/api/resource')({
  server: { handlers: { GET, POST, PATCH, DELETE } },
})
```

### 2. Authentication

Session-based with HTTP-only cookies. Check with `requireAuth(request)` or `requireAdmin(request)`.

### 3. Localized Content

Database stores JSONB: `{ en: "English", fr?: "French", id?: "Indonesian" }`

### 4. Forms

Use `FNForm` component for all forms. Supports grid layouts, validation, custom fields.

### 5. State

- **Zustand**: Cart, auth (persistent)
- **React Query**: Server data (cached)
- **TanStack Form**: Form state

### 6. Security

- Rate limiting on all endpoints
- CSRF tokens for mutations
- Input validation
- Timing-safe comparisons

## Common Tasks

| Task              | Files to Modify                              |
| ----------------- | -------------------------------------------- |
| Add API endpoint  | `src/routes/api/`                            |
| Add admin page    | `src/routes/admin/`, `src/components/admin/` |
| Add customer page | `src/routes/$lang/`                          |
| Modify schema     | `src/db/schema.ts`, run `yarn db:generate`   |
| Add translation   | `src/i18n/locales/*.json`                    |
| Add utility       | `src/lib/`                                   |
| Add hook          | `src/hooks/`                                 |

## Development Commands

```bash
yarn dev          # Start dev server (port 3000)
yarn build        # Production build
yarn test         # Run tests
yarn typecheck    # Type checking
yarn db:generate  # Generate migrations
yarn db:migrate   # Apply migrations
yarn db:studio    # Database GUI
yarn locales:scan # Scan for translation keys
```
