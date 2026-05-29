---
name: sikhaid-overview
description: Use when needing project architecture, tech stack info, folder structure, or setup instructions for SikhAid Charitable Trust website. Covers SvelteKit configuration, build tools, environment variables, and overall project organization.
allowed-tools: Read, Glob, Grep
---

# SikhAid Project Overview

## Project Identity
**Name:** SikhAid Charitable Trust - Landing Page Application
**Type:** Non-profit charity website with donation, volunteering, and campaign management
**Repository:** /Users/ayushj/Desktop/SikhAidSinglePage

## Tech Stack

### Frontend Framework
- **Svelte 5.0.0** - Reactive component framework
- **SvelteKit 2.22.0** - Meta-framework with file-based routing and SSR
- **TypeScript 5.0.0** - Type-safe JavaScript

### Styling & UI
- **Tailwind CSS 3.4.17** - Utility-first CSS framework
- **PostCSS 8.5.6** + **Autoprefixer 10.4.21** - CSS processing
- **Iconify Svelte 5.0.2** - Icon system
- **Custom CSS animations** - fade-in, slide-up, bounce-in with delays

### Backend & Database
- **Firebase 12.4.0** - Backend as a Service
  - **Firestore** - Cloud NoSQL database
  - **Firebase Auth** - Authentication system
  - **Cloud Storage** - File storage

### Payment Integration
- **Razorpay** - Indian payment gateway for donations
  - Loaded via CDN in layout
  - Configured with environment variables

### Build Tools
- **Vite 7.0.4** - Fast build tool and dev server
- **SvelteKit Adapter Auto** - Automatic deployment adapter

## Project Structure

```
SikhAidSinglePage/
├── .claude/
│   └── skills/              # Claude Code skills (this folder)
│
├── src/
│   ├── lib/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── home/        # Home page specific components
│   │   │   ├── admin/       # Admin-specific components
│   │   │   ├── Header.svelte
│   │   │   ├── Footer.svelte
│   │   │   ├── PaymentForm.svelte
│   │   │   └── ...
│   │   ├── stores/          # Svelte stores for state management
│   │   │   ├── donation.ts
│   │   │   ├── contact.ts
│   │   │   ├── volunteering.ts
│   │   │   └── csr.ts
│   │   ├── data/            # Static data (campaigns, blogs)
│   │   ├── types/           # TypeScript type definitions
│   │   ├── assets/          # Images and static assets
│   │   ├── firebase.ts      # Firebase initialization
│   │   ├── firestore.ts     # Firestore database functions
│   │   └── razorpay.ts      # Payment integration
│   │
│   ├── routes/              # SvelteKit file-based routing
│   │   ├── +layout.svelte   # Root layout (Header/Footer wrapper)
│   │   ├── +page.svelte     # Home page
│   │   ├── about/
│   │   ├── campaigns/
│   │   ├── blog/
│   │   ├── contact/
│   │   ├── donate/
│   │   ├── volunteering/
│   │   ├── csr/
│   │   ├── payment/
│   │   └── admin/           # Protected admin routes
│   │
│   ├── app.css              # Global styles & design tokens
│   ├── app.html             # HTML entry point
│   └── app.d.ts             # App type definitions
│
├── static/                  # Static assets (favicon, robots.txt)
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite build configuration
├── svelte.config.js         # SvelteKit configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── postcss.config.js        # PostCSS configuration
└── .env                     # Environment variables (not committed)
```

## Key Configuration Files

### package.json
**Scripts:**
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run check` - Type check Svelte components

### Environment Variables (.env)
```
VITE_FIREBASE_API_KEY=...
VITE_FIREBASE_AUTH_DOMAIN=...
VITE_FIREBASE_PROJECT_ID=...
VITE_FIREBASE_STORAGE_BUCKET=...
VITE_FIREBASE_MESSAGING_SENDER_ID=...
VITE_FIREBASE_APP_ID=...

VITE_RAZORPAY_KEY_ID=...
VITE_ORGANIZATION_NAME=Sikh Aid Charitable Trust
VITE_SITE_URL=www.sikhaid.ngo
VITE_ENVIRONMENT=production
```

### tsconfig.json
- Strict mode enabled
- Module resolution: bundler
- Extends SvelteKit's generated config

### vite.config.ts
- Uses `@sveltejs/kit/vite` plugin
- Default Vite configuration

## Architecture Patterns

### Component Architecture
1. **Layout Components** - Root layout with Header/Footer
2. **Page Components** - Route-specific pages in `/routes`
3. **Feature Components** - Reusable sections (Hero, CampaignCarousel)
4. **UI Components** - Small reusable elements (PaymentForm, Modal)

### Data Flow Pattern
```
User Input → Svelte Store → Component Reactivity → UI Update
                ↓
        Firestore Write → Async Feedback
```

### Routing Pattern
- File-based routing: `/routeshttps://donate.sikhaid.ngo//+page.svelte` → `https://donate.sikhaid.ngo/`
- Dynamic routes: `/routes/campaigns/[slug]/+page.svelte` → `/campaigns/:slug`
- Nested layouts: `+layout.svelte` files for shared wrappers

### State Management Pattern
- Svelte writable stores for form data
- Store functions for actions (e.g., `setDonationAmount()`)
- Direct Firestore integration from components

## Development Workflow

### Setup
```bash
npm install              # Install dependencies
npm run dev             # Start dev server (http://localhost:5173)
```

### Type Checking
```bash
npm run check           # Check types across all files
npm run check:watch     # Watch mode for type checking
```

### Build & Deploy
```bash
npm run build           # Build for production (outputs to .svelte-kit/output)
npm run preview         # Preview production build locally
```

## Git Information
- **Current branch:** main
- **Recent commits:**
  - 545b459: admin route added. form submissions connected to firestore
  - 7c79783: firestore setup done and tested
  - 5424583: added volunteering and csr routes

## Design Philosophy
- **Mobile-first** responsive design with Tailwind breakpoints
- **Component reusability** - DRY principle throughout
- **Type safety** - TypeScript interfaces for all data structures
- **Progressive enhancement** - Works without JavaScript for core content
- **Accessibility** - Semantic HTML, ARIA labels, keyboard navigation

## Security Notes
⚠️ **Known Issues:**
- Admin password hardcoded in Footer.svelte (should use env var)
- Client-side session authentication (consider backend auth)
- Firebase config visible in browser (requires Firestore security rules)

## When to Use This Skill
- Setting up the project for the first time
- Understanding the overall architecture
- Locating where specific functionality lives
- Adding new major features or routes
- Configuring build tools or environment variables
- Onboarding new developers or AI assistants

## Related Skills
- `sikhaid-components` - Component patterns and organization
- `sikhaid-routing` - Routes and navigation
- `sikhaid-data` - Firebase, Firestore, and state management
