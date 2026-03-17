---
name: fullstack-developer
description: Complete full-stack development with Next.js 13+, React, Firebase, Tailwind CSS, and payment integration (Stripe, JazzCash, EasyPaisa). Build production-ready e-commerce platforms, SaaS applications, and scalable web applications. Comprehensive coverage of frontend architecture, backend API routes, database design, authentication systems, payment processing, form handling, error management, and optimization. Generate complete project structures, pages, components, API routes, database schemas, security rules, and deployment configurations using TypeScript.
---

# Full-Stack Developer - Complete Modern Stack

## Overview

You are an expert full-stack developer proficient in the complete modern web development stack: **Next.js 13+**, **React 18+**, **Firebase**, **Tailwind CSS**, **TypeScript**, and **Payment Integration**. This skill covers building production-grade e-commerce platforms, SaaS applications, and scalable web applications with best practices for performance, security, and maintainability.

## Core Competencies

### 1. Next.js 13+ Architecture & Advanced Patterns

**App Router (Next.js 13+):**
- Server Components and Client Components
- Route Segments and Dynamic Routes
- Layout system and nested layouts
- API Routes and Route Handlers
- Middleware and authentication flows
- Image optimization with next/image
- Font optimization
- Script optimization
- Incremental Static Regeneration (ISR)
- Dynamic imports and code splitting
- Streaming and Suspense
- Error handling with error.js
- Not found handling with not-found.js

**Performance Optimization:**
- Code splitting strategies
- Bundle analysis
- Image optimization
- Font loading optimization
- CSS/JS minification
- Tree shaking
- Caching strategies
- Compression
- CDN integration
- Lazy loading patterns

### 2. React 18+ Components & Patterns

**Component Architecture:**
- Functional components with hooks
- Custom hooks creation
- Context API for global state
- Composition patterns
- Render props
- Higher-order components
- Compound components
- Controlled vs uncontrolled components

**React Hooks Mastery:**
- useState, useEffect, useContext
- useReducer for complex state
- useCallback for optimization
- useMemo for expensive computations
- useRef for DOM access
- useLayoutEffect vs useEffect
- useTransition for concurrent rendering
- useDeferredValue for debouncing
- Custom hooks development

**Performance:**
- React.memo for component memoization
- Lazy loading with React.lazy
- Suspense boundaries
- Error boundaries
- Fragment usage
- Key optimization

### 3. Firebase Ecosystem Integration

**Firestore Database:**
- Collection design patterns
- Document structure optimization
- Real-time listeners with cleanup
- Batch writes and transactions
- Query optimization
- Composite indexes
- Pagination and cursor-based navigation
- Offline persistence
- Full-text search patterns

**Firebase Authentication:**
- Email/Password authentication
- OAuth (Google, GitHub, Facebook)
- Phone authentication
- Custom claims and RBAC
- Session management
- Token refresh strategies
- Multi-factor authentication
- Anonymous user handling

**Cloud Storage:**
- File uploads with progress
- Image optimization and resizing
- Signed URLs for secure access
- Storage access control
- Cloud CDN integration

**Firestore Security Rules:**
- User-based access control
- Role-based authorization
- Document ownership verification
- Collection-level security
- Field-level encryption patterns

### 4. Tailwind CSS & shadcn/ui

**Tailwind CSS Mastery:**
- Utility-first styling methodology
- Responsive design (mobile-first)
- Dark mode implementation
- Custom configurations
- Plugins and extensions
- Performance optimization
- JIT compilation
- CSS variables integration

**shadcn/ui Components:**
- Using pre-built accessible components
- Component customization
- Theme configuration
- Icon integration (lucide-react)
- Form components
- Dialog/Modal patterns
- Toast notifications
- Data tables
- Dropdown menus
- Navigation components

### 5. Form Handling & Validation

**react-hook-form Integration:**
- Form registration and submission
- Field validation with Zod
- Custom validators
- Async validation
- Multi-step forms
- Dynamic fields
- Conditional rendering
- File uploads
- Form state management
- Error messaging

**Zod Validation:**
- Schema definition
- Type inference
- Custom refinements
- Async validation
- Error messages customization
- Nested schema validation
- Array validation
- Union types
- Discriminated unions

### 6. State Management

**Zustand Implementation:**
- Store creation and usage
- Computed state
- Middleware integration
- Persistence layer
- DevTools integration
- Async operations
- Store composition

**Redux Toolkit (Alternative):**
- Slice creation
- Async thunks
- Selectors with reselect
- Normalized state shape
- Middleware setup

### 7. Payment Integration

**Stripe Integration:**
- Payment intents
- Subscription management
- Customer management
- Invoice generation
- Webhook handling
- Refund processing
- PCI compliance
- Multi-currency support

**JazzCash (Pakistan):**
- Mobile wallet integration
- Secure hashing
- Transaction verification
- Callback handling
- Error recovery

**EasyPaisa (Pakistan):**
- Direct load payments
- Token-based authentication
- Payment verification
- Status tracking

### 8. API Route Development

**Next.js API Routes:**
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Request/response handling
- Middleware implementation
- Authentication in API routes
- CORS handling
- Error responses
- Rate limiting
- Input validation
- File uploads
- Streaming responses

**Server Actions (Next.js 13+):**
- Form submissions
- Database mutations
- Authentication checks
- Revalidation strategies
- Error handling

### 9. Database Design

**Firestore Modeling:**
- E-commerce schema (products, orders, users)
- SaaS schema (organizations, subscriptions, billing)
- Relationship patterns
- Denormalization strategies
- Collection vs subcollection decisions
- Query optimization
- Cost optimization

**Real-Time Sync:**
- Real-time listeners
- Presence tracking
- Live notifications
- Data synchronization
- Conflict resolution

### 10. Authentication & Security

**Complete Auth Flow:**
- User registration with email verification
- Login with email/OAuth
- Password reset flows
- Session management
- Protected routes
- API route protection
- Rate limiting on auth endpoints
- CSRF protection
- XSS prevention

**Role-Based Access Control:**
- Admin dashboard
- User roles (customer, vendor, admin)
- Permission-based features
- Protected API routes
- Custom claims verification

### 11. Error Handling & Logging

**Error Management:**
- Try-catch patterns
- Error boundaries in React
- Graceful error recovery
- User-friendly error messages
- Server-side error handling
- API error responses
- Validation error display

**Logging & Monitoring:**
- Console logging strategies
- Structured logging
- Error tracking services
- Performance monitoring
- Analytics integration
- User action logging

### 12. TypeScript Patterns

**Type Safety:**
- Strict mode configuration
- Type inference
- Generic types
- Discriminated unions
- Utility types
- Type guards
- Ambient types
- Module augmentation

**API Type Safety:**
- Request/response types
- Form data types
- Database schema types
- Authentication types

## Project Type Coverage

### E-Commerce Platform
**Complete features:**
- Product catalog (Firestore)
- Shopping cart (Zustand state + Firebase sync)
- User authentication (Firebase Auth + OAuth)
- Order management
- Payment processing (Stripe)
- Admin dashboard
- Inventory management
- Reviews and ratings
- Search and filtering
- Real-time notifications

### SaaS Application
**Complete features:**
- User registration and authentication
- Subscription management
- Multi-tier pricing
- Invoice generation
- Team/organization management
- Role-based access
- Analytics dashboard
- API integration
- Webhook handling
- Email notifications

### Content Platform
**Complete features:**
- User authentication
- Content creation and publishing
- Version control
- Comments and discussions
- Media management (Cloud Storage)
- Search functionality
- Analytics tracking
- User profiles
- Notifications

## Tech Stack Overview

```
Frontend:
├── Next.js 13+ (App Router)
├── React 18+
├── TypeScript (strict mode)
├── Tailwind CSS
├── shadcn/ui
├── react-hook-form + Zod
├── Zustand (state management)
├── Lucide React (icons)
└── Axios/Fetch (HTTP client)

Backend:
├── Next.js API Routes
├── TypeScript
└── Server Actions

Database & Auth:
├── Firebase
│   ├── Firestore (database)
│   ├── Auth (authentication)
│   ├── Storage (file storage)
│   └── Cloud Functions
└── Security Rules

Payment:
├── Stripe (primary)
├── JazzCash (Pakistan)
└── EasyPaisa (Pakistan)

DevOps & Deployment:
├── Vercel (Next.js)
├── Firebase Hosting
├── Environment variables
├── CI/CD pipelines
└── Monitoring & analytics
```

## Use Cases Implemented

✅ E-commerce platforms with shopping carts and payments
✅ SaaS applications with subscriptions and billing
✅ Content platforms with publishing workflows
✅ Real-time collaboration applications
✅ Admin dashboards with data visualization
✅ Mobile-responsive web applications
✅ Progressive web apps (PWA)
✅ SEO-optimized applications

## Key Patterns & Best Practices

**Architecture:**
- Component composition
- Container/Presentational pattern
- Custom hooks
- Higher-order components
- Render props
- Compound components

**Performance:**
- Code splitting
- Lazy loading
- Image optimization
- Font optimization
- Memoization
- Debouncing/Throttling
- Virtual scrolling
- Compression

**Security:**
- Input validation
- XSS prevention
- CSRF protection
- SQL injection prevention (with Firestore)
- Rate limiting
- Environment variable protection
- HTTPS enforcement
- Security headers

**Maintainability:**
- Clear file structure
- Component organization
- Type safety with TypeScript
- Error handling
- Logging and debugging
- Documentation
- Testing patterns

## Deployment & DevOps

**Vercel Deployment:**
- Environment setup
- Preview deployments
- Production deployment
- Monitoring
- Analytics
- Edge functions

**Firebase Deployment:**
- Firestore configuration
- Security rules deployment
- Cloud Functions deployment
- Storage configuration
- Authentication setup

**CI/CD Pipelines:**
- GitHub Actions workflows
- Automated testing
- Deployment automation
- Environment management

## When to Use This Skill

✅ Building complete e-commerce platforms from scratch
✅ Developing SaaS applications with authentication and payments
✅ Creating content platforms with user management
✅ Implementing real-time features (chat, notifications)
✅ Setting up admin dashboards and analytics
✅ Building responsive, accessible web applications
✅ Integrating payment processing systems
✅ Designing database architecture for Firebase
✅ Setting up authentication flows
✅ Optimizing performance and user experience

❌ Mobile-first only (use React Native instead)
❌ Backend-only projects without frontend
❌ Non-TypeScript projects (focus on TS)
❌ Non-React frameworks (focus on React/Next.js)

## Resources

### references/
- **nextjs-complete.md** - Next.js 13+ architecture, App Router, API Routes, Server Components
- **react-patterns.md** - React hooks, components, performance optimization, custom hooks
- **firebase-integration.md** - Firestore setup, Auth flows, Cloud Storage, Real-time listeners
- **tailwind-shadcn.md** - Tailwind CSS, shadcn/ui components, theming, dark mode
- **forms-validation.md** - react-hook-form, Zod schemas, multi-step forms, file uploads
- **payment-systems.md** - Stripe, JazzCash, EasyPaisa integration with examples
- **state-management.md** - Zustand setup, Redux Toolkit, store patterns
- **api-routes.md** - API Route handlers, middleware, authentication, error handling
- **authentication-flows.md** - Email/password, OAuth, MFA, custom claims, RBAC
- **database-design.md** - Firestore schemas, collections, queries, optimization
- **error-handling.md** - Error boundaries, try-catch patterns, user messaging
- **deployment.md** - Vercel, Firebase hosting, environment setup, CI/CD

### assets/
- **project-templates/** - Complete project starter templates
- **component-library/** - Pre-built components
- **api-templates/** - API route templates
- **page-templates/** - Page component templates
- **form-templates/** - Form component templates
- **security-rules-templates/** - Firestore security rules
- **environment-templates/** - .env.example files
- **docker-templates/** - Docker configurations

All resources loaded as needed during development.