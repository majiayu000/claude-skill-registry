---
name: libraries-dependencies-mastery
description: Complete mastery of essential modern web development libraries and dependencies. Cover Next.js, React, TypeScript, Tailwind CSS, Firebase, Zustand, redux-toolkit, react-hook-form, Zod, shadcn/ui, lucide-react, Stripe, and more. Learn setup, integration patterns, advanced usage, performance optimization, troubleshooting, common pitfalls, and version management. Includes quick reference guides, in-depth tutorials, complete examples for e-commerce and SaaS, configuration files, type definitions, error handling, and production patterns. Master how libraries work together and solve real-world challenges.
---

# Libraries & Dependencies Mastery

## Overview

You are an expert in modern web development libraries and their integration. This skill provides complete mastery of the essential libraries powering modern full-stack applications: **Next.js**, **React**, **TypeScript**, **Tailwind CSS**, **Firebase**, **State Management** (Zustand, Redux Toolkit), **Forms** (react-hook-form, Zod), **UI/UX** (shadcn/ui, lucide-react), and **Payments** (Stripe). Learn setup, configuration, integration patterns, advanced usage, performance optimization, troubleshooting, version management, and common pitfalls.

## Core Library Mastery

### 1. Next.js 13+ Complete Mastery

**Setup & Configuration:**
- Installation and project initialization
- tsconfig.json configuration for strict TypeScript
- next.config.js customization
- Environment variables (.env, .env.local, .env.production)
- Path aliases (@/ imports)
- Monorepo setup with workspaces

**App Router (Next.js 13+):**
- File-based routing structure
- Route segments and dynamic routes ([id], [...slug])
- Route groups and layouts ((auth), (dashboard))
- Parallel routes and intercepting routes
- Loading states and error boundaries
- Not found and error.js pages
- Middleware and request handling
- Route handlers (GET, POST, PUT, DELETE, PATCH)
- Server Components vs Client Components
- Suspense and streaming
- Data fetching patterns (fetch, cache tags)
- Revalidation strategies (ISR, on-demand)

**Performance Optimization:**
- Image optimization with next/image
- Font optimization
- Script optimization and loading strategies
- Dynamic imports with React.lazy
- Code splitting and bundle analysis
- CSS optimization and minification
- Compression and gzip
- CDN configuration

**Common Pitfalls & Solutions:**
- Hydration mismatches (Server vs Client)
- Using client-only features in Server Components
- Incorrect caching strategies
- Image optimization issues
- Font loading performance
- Dynamic routes not rendering statically
- Environment variable scope

**Troubleshooting Guide:**
```
Issue: "Cannot find module" in builds
Solution: Check tsconfig paths, clear .next folder, rebuild

Issue: Hydration mismatch error
Solution: Use dynamic imports, wrap client code, check useEffect

Issue: Images not optimizing
Solution: Use next/image, configure domains, check sizes

Issue: Build time too long
Solution: Analyze with `next/bundle-analyzer`, use dynamic imports

Issue: Environment variables undefined
Solution: Prefix with NEXT_PUBLIC_ for client, restart dev server
```

**Version Management:**
- Upgrading from Pages Router to App Router
- Breaking changes between versions
- Migration guides
- Beta features and deprecations
- Staying updated with releases

---

### 2. React 18+ Complete Mastery

**Hooks Deep Dive:**
- useState: State management, state updates, batching
- useEffect: Side effects, cleanup, dependencies, common pitfalls
- useContext: Context creation, avoiding prop drilling
- useReducer: Complex state logic, reducer patterns
- useCallback: Memoization, dependency arrays
- useMemo: Expensive computations, memory management
- useRef: DOM access, persistent values, .current
- useLayoutEffect: DOM layout measurements
- useTransition: Concurrent rendering, isPending state
- useDeferredValue: Value debouncing, input optimization
- useId: Unique identifiers, accessibility
- useImperativeHandle: Custom instance values

**Component Patterns:**
- Functional components with hooks
- Custom hooks development and reusability
- Compound components
- Render props pattern
- Higher-order components
- Provider pattern
- Controlled vs uncontrolled components
- Composition over inheritance

**Performance Optimization:**
- React.memo for preventing rerenders
- useCallback with dependencies
- useMemo for expensive operations
- Lazy loading with React.lazy and Suspense
- Code splitting strategies
- List rendering with keys (importance of stable keys)
- Avoiding unnecessary renders
- Profiler API for performance measurement

**Concurrent Features:**
- Suspense boundaries
- useTransition for non-blocking updates
- useDeferredValue for value debouncing
- Streaming and progressive rendering
- Automatic batching of state updates

**Common Pitfalls & Solutions:**
- Missing dependency in useEffect
- Stale closures in hooks
- Memory leaks in useEffect
- Infinite loops with useEffect
- Using hooks conditionally
- Not returning cleanup functions
- Incorrect memo dependencies
- State batching confusion

**Troubleshooting Guide:**
```
Issue: Infinite loop in useEffect
Solution: Check dependencies, add return cleanup function

Issue: Stale state in callback
Solution: Include state in dependencies or use useCallback

Issue: Memory leak warning
Solution: Add cleanup function to useEffect, unsubscribe

Issue: Component rerending unnecessarily
Solution: Use React.memo, useCallback, useMemo

Issue: Hydration error with useId
Solution: Use proper key prop, wrap in Suspense
```

---

### 3. TypeScript Complete Mastery

**Fundamentals:**
- Primitive types (string, number, boolean, null, undefined)
- Union types and intersection types
- Type literals and literal types
- Enums and const assertions
- Type aliases vs interfaces
- Extending types and interfaces
- Optional properties (?) and nullish coalescing (??)

**Advanced Types:**
- Generic types and constraints
- Conditional types (extends ? :)
- Mapped types (Record, Partial, Required, etc.)
- Utility types (Pick, Omit, Exclude, Extract, etc.)
- Discriminated unions for exhaustive checking
- Type guards and type predicates (is keyword)
- Const type parameters
- Template literal types

**React + TypeScript:**
- Component prop typing
- Event handler typing
- Ref typing with Ref<HTMLInputElement>
- useState with initial values and TypeScript
- useReducer with typed actions
- useContext with typed values
- Custom hook typing
- Children prop typing

**Common Patterns:**
```typescript
// Discriminated union
type Action = 
  | { type: 'ADD'; payload: Item }
  | { type: 'REMOVE'; payload: string };

// Generic component
function List<T extends { id: string }>(props: { items: T[] }) {}

// Type guard
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

// Utility type usage
type User = { name: string; age: number; email: string };
type UserPreview = Pick<User, 'name' | 'age'>;
```

**Configuration:**
- tsconfig.json strict mode
- CompilerOptions for strict type checking
- Path mapping and aliases
- Module resolution settings
- Declaration file generation

**Common Pitfalls & Solutions:**
- Type inference failures
- Type assertion misuse
- Any type overuse
- Incorrect generic constraints
- Missing type definitions
- Circular type dependencies

**Troubleshooting Guide:**
```
Issue: Type 'X' is not assignable to type 'Y'
Solution: Check property names, use type assertion carefully, review interfaces

Issue: Cannot find name 'X'
Solution: Check imports, verify tsconfig paths, check node_modules

Issue: Property 'X' doesn't exist on type 'Y'
Solution: Check types, update interfaces, verify external package types

Issue: Generic type 'T' is too complex
Solution: Add constraints, break into simpler types, use keyof
```

---

### 4. Tailwind CSS Complete Mastery

**Core Concepts:**
- Utility-first CSS methodology
- JIT (Just-In-Time) compilation
- Responsive design with breakpoints (sm, md, lg, xl, 2xl)
- Hover, focus, and other state variants
- Dark mode implementation (class and prefers-color-scheme)
- Custom configuration (colors, spacing, fonts)
- Arbitrary values ([width: 343px])
- CSS layers and specificity

**Configuration & Customization:**
```javascript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

export default {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#your-color',
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [],
} satisfies Config
```

**Advanced Patterns:**
- Responsive design strategies
- Component extraction with @apply
- Conditional styling with clsx/classnames
- Dark mode toggling
- Custom plugins
- CSS variables integration
- Animation and transition utilities
- Theme switching with CSS custom properties

**Performance Optimization:**
- Purging unused styles in production
- Content configuration for tree-shaking
- CSS size analysis
- Critical CSS inline optimization
- Lazy loading stylesheets
- CSS compression

**Common Pitfalls & Solutions:**
- Utility conflicts and specificity issues
- Unresponsive images with Tailwind sizing
- Dark mode not working properly
- Build process including unused classes
- Custom color not applying
- Conflicting CSS and Tailwind classes

**Troubleshooting Guide:**
```
Issue: Styles not applying in production
Solution: Check content paths, rebuild, check purge config

Issue: Dark mode not toggling
Solution: Set darkMode: 'class' in config, add class to html

Issue: Custom colors not available
Solution: Update tailwind.config.ts theme.extend.colors

Issue: Build size too large
Solution: Verify content paths, use JIT, remove unused plugins

Issue: Responsive styles not working
Solution: Use correct breakpoint prefix (sm:, md:), check cascade
```

---

### 5. Firebase Complete Mastery

**Setup & Configuration:**
```typescript
// lib/firebase.ts
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
```

**Authentication:**
- Email/password signup and signin
- OAuth providers (Google, GitHub, Facebook)
- User profile management
- Custom claims for authorization
- Session persistence
- Token refresh and expiration
- MFA setup and verification
- Anonymous authentication

**Firestore Database:**
- Collection references and document references
- CRUD operations (create, read, update, delete)
- Real-time listeners with cleanup
- Batch writes and transactions
- Query operations (where, orderBy, limit)
- Pagination with startAt/endAt
- Subcollections vs root collections
- Data modeling and normalization

**Cloud Storage:**
- File upload with progress tracking
- Download URLs and signed URLs
- File deletion and management
- Access control and security rules
- Image optimization strategies
- Resumable uploads for large files

**Offline Persistence:**
- Local caching configuration
- Sync with server on reconnection
- Offline-first strategies
- Conflict resolution

**Common Pitfalls & Solutions:**
- Security rules blocking access
- Missing .onSnapshot cleanup
- Querying with unstable data
- Creating too many subcollections
- Not validating data before writes
- Inconsistent authentication state
- Storage rules preventing uploads

**Troubleshooting Guide:**
```
Issue: "Permission denied" errors
Solution: Check Security Rules, verify auth state, check custom claims

Issue: onSnapshot not updating
Solution: Verify listener attached, check firestore rules, cleanup properly

Issue: File upload failing
Solution: Check storage rules, verify file path, check bucket permissions

Issue: Auth state undefined on refresh
Solution: Wait for onAuthStateChanged before rendering, use loading state

Issue: Realtime listener consuming quota
Solution: Limit listeners, use oncemore, implement cleanup
```

---

### 6. State Management: Zustand & Redux Toolkit

**Zustand Complete:**
```typescript
// store/cartStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  getTotal: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (item) => set(state => ({
        items: [...state.items, item]
      })),
      removeItem: (id) => set(state => ({
        items: state.items.filter(i => i.id !== id)
      })),
      getTotal: () => {
        return get().items.reduce((sum, item) => 
          sum + item.price * item.quantity, 0
        );
      },
    }),
    { name: 'cart-storage' }
  )
);
```

**Redux Toolkit Complete:**
```typescript
// store/cartSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartState {
  items: CartItem[];
}

const cartSlice = createSlice({
  name: 'cart',
  initialState: { items: [] },
  reducers: {
    addItem: (state, action: PayloadAction<CartItem>) => {
      state.items.push(action.payload);
    },
    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(i => i.id !== action.payload);
    },
  },
});

export const { addItem, removeItem } = cartSlice.actions;
export default cartSlice.reducer;
```

**Comparison & When to Use:**
- Zustand: Lightweight, minimal boilerplate, easier for beginners
- Redux Toolkit: More powerful, better DevTools, larger apps
- Integration with other libraries
- Performance considerations

**Common Pitfalls & Solutions:**
- Mutating state directly in Zustand
- Not using persist middleware properly
- Redux selector performance issues
- Unnecessary renders from store changes
- DevTools not working

**Troubleshooting Guide:**
```
Issue: State not persisting in Zustand
Solution: Add persist middleware, check localStorage, verify name prop

Issue: Redux component not updating
Solution: Check selector, verify dispatch called, check middleware

Issue: Store data undefined on mount
Solution: Use loading state, wait for hydration, check persist

Issue: Memory leaks from listeners
Solution: Return unsubscribe function, cleanup in useEffect
```

---

### 7. Forms: react-hook-form + Zod

**react-hook-form Setup:**
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  );
}
```

**Zod Validation:**
```typescript
// Complete validation schema
const userSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().min(18).max(120),
  password: z.string().min(8),
  confirmPassword: z.string(),
  terms: z.boolean().refine(val => val === true),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});
```

**Advanced Patterns:**
- Multi-step forms with validation
- Dynamic field arrays
- Conditional field rendering
- Async validation (checking email availability)
- Custom validators
- Nested object validation
- File upload validation
- Form submission handling

**Common Pitfalls & Solutions:**
- Form not submitting with validation errors
- Async validation causing delays
- Zod schema not matching form structure
- Field array complexity
- Custom validation logic errors
- Form reset not working
- File upload validation failing

**Troubleshooting Guide:**
```
Issue: Form submitting even with errors
Solution: Check handleSubmit usage, verify resolver setup

Issue: Async validation taking too long
Solution: Add debounce, implement caching, optimize backend

Issue: Zod error: "Expected object, received undefined"
Solution: Verify schema matches form data structure

Issue: Dynamic fields not validating
Solution: Use z.array() properly, update schema dynamically

Issue: File validation not working
Solution: Use refine/superRefine, check file type validation
```

---

### 8. UI/UX: shadcn/ui & lucide-react

**shadcn/ui Setup & Usage:**
```typescript
// Using pre-built components
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';

export function MyComponent() {
  return (
    <Card>
      <Input placeholder="Enter text" />
      <Button>Submit</Button>
    </Card>
  );
}
```

**Available Components:**
- Buttons (variants, sizes, states)
- Input fields and forms
- Cards and containers
- Modals and dialogs
- Dropdowns and menus
- Tabs and accordions
- Data tables and lists
- Alerts and notifications
- Progress indicators
- Navigation components
- Tooltips and popovers

**lucide-react Icons:**
```typescript
import { Heart, ShoppingCart, Menu, X } from 'lucide-react';

export function IconExample() {
  return (
    <>
      <Heart size={24} />
      <ShoppingCart className="text-blue-600" />
      <Menu strokeWidth={1.5} />
    </>
  );
}
```

**Customization & Theming:**
- Tailwind CSS integration
- Color customization
- Size variants
- Animation options
- Dark mode support
- Custom component wrappers

**Common Pitfalls & Solutions:**
- Component styling conflicts
- Icon size inconsistencies
- Accessibility issues
- Theme not applying
- Custom styling overriding defaults

**Troubleshooting Guide:**
```
Issue: shadcn/ui component styles not applying
Solution: Check Tailwind config, verify CSS import, check className conflicts

Issue: Icons not showing or sizing incorrectly
Solution: Specify size prop, check import path, verify CSS classes

Issue: Dark mode not working with components
Solution: Set darkMode in tailwind.config, wrap with provider

Issue: Component variants not working
Solution: Check component prop names, verify version compatibility
```

---

### 9. Payments: Stripe Integration

**Stripe Setup:**
```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// Create payment intent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 1000, // in cents
  currency: 'usd',
  payment_method_types: ['card'],
});
```

**Client-Side Integration:**
```typescript
import { loadStripe } from '@stripe/js';
import { CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_KEY!);

function PaymentForm() {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (e) => {
    const { paymentIntent } = await stripe.confirmCardPayment(
      clientSecret,
      { payment_method: { card: elements.getElement(CardElement) } }
    );
  };

  return (
    <Elements stripe={stripePromise}>
      <CardElement />
      <button onClick={handleSubmit}>Pay</button>
    </Elements>
  );
}
```

**Webhooks & Server-Side:**
- Payment intent creation
- Webhook event handling
- Subscription management
- Customer management
- Invoice generation
- Refund processing

**Common Pitfalls & Solutions:**
- Missing publishable key environment variable
- Webhook signature verification failing
- Race conditions with payment status
- PCI compliance violations
- Testing with wrong API keys
- Missing error handling
- Race conditions in webhook processing

**Troubleshooting Guide:**
```
Issue: "publishable key not found" error
Solution: Check NEXT_PUBLIC_STRIPE_KEY env var, restart dev server

Issue: Webhook verification failing
Solution: Use correct webhook secret, check signature encoding

Issue: Payment processing twice
Solution: Implement idempotency keys, add retry logic, check order status

Issue: Test card not working
Solution: Use Stripe test cards (4242424242424242), check mode (test/live)
```

---

### 10. Other Essential Libraries

**react-hot-toast:**
```typescript
import toast from 'react-hot-toast';

// Success toast
toast.success('Order placed successfully!');

// Error toast
toast.error('Payment failed');

// Custom toast
toast((t) => (
  <div>
    Custom message
    <button onClick={() => toast.dismiss(t.id)}>Dismiss</button>
  </div>
));
```

**axios vs fetch:**
```typescript
// axios - automatic JSON handling, interceptors
import axios from 'axios';
const response = await axios.get('/api/products');

// fetch - native, no dependencies
const response = await fetch('/api/products');
const data = await response.json();
```

**clsx/classnames:**
```typescript
import clsx from 'clsx';

const buttonClass = clsx(
  'px-4 py-2 rounded',
  variant === 'primary' && 'bg-blue-600 text-white',
  variant === 'secondary' && 'bg-gray-200 text-gray-900',
  isLoading && 'opacity-50 cursor-not-allowed'
);
```

---

## Integration Patterns: Libraries Working Together

### E-Commerce Example
```typescript
// Components use shadcn/ui + lucide-react
// Forms use react-hook-form + Zod
// State with Zustand + persist
// API calls with axios
// Payments with Stripe
// Database with Firebase
// Styling with Tailwind CSS
// Routing with Next.js
```

### SaaS Example
```typescript
// Next.js for routing + SSR
// React for components
// TypeScript for type safety
// Firebase Auth + Firestore
// Redux Toolkit for complex state
// Tailwind + shadcn/ui for UI
// react-hook-form for user forms
// Stripe for subscriptions
```

---

## Dependency Management

**package.json Best Practices:**
- Version pinning strategies
- Semantic versioning
- Peer dependencies
- Dev vs production dependencies
- Monorepo workspaces
- Script automation

**Updating Dependencies:**
```bash
# Check outdated packages
npm outdated

# Update specific package
npm install package@latest

# Update all patch versions
npm update

# Check for vulnerabilities
npm audit
npm audit fix
```

**Common Issues:**
- Peer dependency conflicts
- Incompatible version combinations
- Breaking changes during updates
- Node version compatibility
- Platform-specific issues

---

## Performance Optimization Across Libraries

**Bundle Size Reduction:**
- Dynamic imports with Next.js
- Tree shaking with TypeScript
- Removing unused Tailwind classes
- Code splitting with React.lazy
- Analyzing with bundle-analyzer

**Runtime Performance:**
- React memo and callbacks
- Zustand selector optimization
- Redux reselect usage
- Lazy image loading with next/image
- Request deduplication with axios interceptors

**Database Performance:**
- Firestore query optimization
- Collection indexing
- Batch operations
- Caching strategies

---

## When to Use This Skill

✅ Understanding how to set up each library properly
✅ Learning integration patterns between libraries
✅ Troubleshooting library-specific issues
✅ Optimizing performance with libraries
✅ Upgrading and managing dependencies
✅ Finding solutions to common pitfalls
✅ Learning best practices for each library
✅ Making choices between similar libraries (Zustand vs Redux)
✅ Quick reference for library syntax and APIs
✅ Deep diving into advanced usage

---

## Quick Reference vs Deep Learning

**This skill includes:**
- ⚡ Quick lookup tables and syntax reference
- 📚 In-depth tutorials and explanations
- 🔧 Configuration file templates
- 🐛 Troubleshooting guides
- 🚀 Performance tips
- ⚠️ Common pitfalls and solutions
- 🔄 Integration patterns
- 📊 Comparison guides
- 💡 Real-world examples
- 🎯 Best practices

---

## Resources & References

### Quick Reference Guides
- **next-js-quick-ref.md** - Commands, config, routing
- **react-hooks-reference.md** - All hooks with examples
- **typescript-quick-ref.md** - Common patterns, syntax
- **tailwind-utilities-ref.md** - All utility classes
- **firebase-methods-ref.md** - All Firebase methods
- **zod-validators-ref.md** - All Zod validators
- **stripe-api-ref.md** - Stripe API methods

### In-Depth Guides
- **next-js-advanced.md** - Advanced patterns, optimization
- **react-performance.md** - Rendering optimization
- **typescript-advanced.md** - Complex types, patterns
- **tailwind-advanced.md** - Custom plugins, design systems
- **firebase-patterns.md** - Architecture patterns
- **zustand-vs-redux.md** - Comparison and when to use
- **form-validation-deep.md** - Complex validation patterns
- **stripe-complete.md** - Full Stripe implementation

### Troubleshooting & Common Issues
- **common-errors.md** - Error messages and solutions
- **dependency-conflicts.md** - Resolving version conflicts
- **performance-issues.md** - Identifying and fixing slowness
- **type-errors.md** - TypeScript error solutions
- **build-issues.md** - Next.js build troubleshooting

### Integration Examples
- **ecommerce-integration.md** - Complete e-commerce setup
- **saas-integration.md** - SaaS platform setup
- **authentication-flows.md** - Auth integration patterns
- **payment-integration.md** - Payment processing setup

---

## Technology Stack Details

**Versions Covered:**
- Next.js 13+
- React 18+
- TypeScript 4.5+
- Tailwind CSS 3+
- Firebase SDK (latest)
- Zustand 4+
- Redux Toolkit 1.9+
- react-hook-form 7+
- Zod 3+
- Stripe (latest)

**Upgrade Paths:**
- Next.js 12 → 13 → 14
- React 17 → 18
- Tailwind CSS 2 → 3
- TypeScript updates and breaking changes
- Firebase SDK v8 → v9 (modular SDK)

---

This comprehensive skill gives you complete mastery of the essential libraries and how they work together!