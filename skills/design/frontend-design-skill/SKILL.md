---
name: nextjs-frontend-design
description: Create distinctive, production-grade Next.js applications with expert TypeScript architecture and exceptional visual design. Use this skill when building Next.js projects, React Server Components, full-stack TypeScript applications, or any frontend requiring both architectural excellence and visual distinction. Covers App Router patterns, type-safe APIs, Server Actions, and modern styling. Critically, this skill ensures Claude avoids generic "AI slop" aesthetics (Inter fonts, purple gradients, predictable layouts) and instead creates memorable, intentional interfaces. Triggers on requests for Next.js apps, dashboards, landing pages, SaaS applications, e-commerce sites, or any project needing both technical and aesthetic excellence.
---

# Next.js Frontend Design Skill

Create distinctive, production-grade Next.js applications combining expert TypeScript architecture with exceptional visual design.

<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- **Backgrounds**: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>

## Design Philosophy

Before writing ANY code, commit to a **BOLD aesthetic direction**:

1. **Purpose**: What problem does this interface solve? Who uses it?
2. **Tone**: Pick an extreme and commit fully:
   - Brutally minimal, maximalist chaos, retro-futuristic, organic/natural
   - Luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw
   - Art deco/geometric, soft/pastel, industrial/utilitarian, terminal/code
3. **Differentiation**: What's the ONE thing someone will remember?

**CRITICAL**: Bold maximalism and refined minimalism both work—the key is intentionality, not intensity. Half-measures produce mediocrity.

**For comprehensive design guidance, see:** `references/design-philosophy.md`

---

## Typography Quick Reference

**NEVER use**: Inter, Roboto, Open Sans, Lato, Arial, system fonts

**DO use**:
- Code aesthetic: JetBrains Mono, Fira Code, IBM Plex Mono
- Editorial: Playfair Display, Crimson Pro, Newsreader, Fraunces
- Technical: IBM Plex Sans, Source Sans 3, Source Serif 4
- Distinctive: Bricolage Grotesque, Syne, Outfit, DM Serif Display

**Pairing principle**: High contrast = interesting. Display + monospace, serif + geometric sans.

**Use extremes**: Weight 100/200 vs 800/900 (not 400 vs 600). Size jumps of 3x+ (not 1.5x).

```tsx
// app/layout.tsx - Font setup
import { Bricolage_Grotesque, JetBrains_Mono } from 'next/font/google';

const fontDisplay = Bricolage_Grotesque({
  subsets: ['latin'],
  variable: '--font-display',
  weight: ['200', '400', '800'],
});

const fontMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
});
```

---

## Project Architecture

### Directory Structure (App Router)

```
src/
├── app/                    # App Router
│   ├── layout.tsx          # Root layout with fonts
│   ├── page.tsx            # Homepage
│   ├── globals.css         # Global styles + CSS variables
│   ├── (routes)/           # Route groups
│   └── api/                # API routes (when needed)
├── components/
│   ├── ui/                 # Reusable UI primitives
│   └── features/           # Feature-specific components
├── lib/                    # Utilities (cn, constants, validations)
├── hooks/                  # Custom React hooks
├── types/                  # TypeScript definitions
├── actions/                # Server Actions
└── services/               # External API integrations
```

### TypeScript Essentials

**Type everything explicitly**—avoid `any`:

```typescript
// ✅ Explicit interfaces
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

// ✅ Zod for runtime validation
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;
```

### Server vs Client Components

**Default to Server Components** unless you need:
- Event handlers (onClick, onChange)
- useState, useEffect, useReducer
- Browser APIs

```typescript
// Server Component (default) - async data fetching
async function UserProfile({ userId }: { userId: string }) {
  const user = await fetchUser(userId);
  return <ProfileCard user={user} />;
}

// Client Component - only when needed
'use client';
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Server Actions

```typescript
// actions/user.ts
'use server';
import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const UpdateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function updateUser(formData: FormData) {
  const validated = UpdateUserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  if (!validated.success) {
    return { error: validated.error.flatten() };
  }

  await db.user.update({ data: validated.data });
  revalidatePath('/profile');
  return { success: true };
}
```

---

## Styling Implementation

### CSS Variables Setup

```css
/* globals.css */
:root {
  /* Typography */
  --font-display: 'Bricolage Grotesque', sans-serif;
  --font-body: 'Source Sans 3', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Colors - Commit to an aesthetic */
  --color-bg: #0a0a0a;
  --color-surface: #141414;
  --color-text: #e8e8e8;
  --color-muted: #6b6b6b;
  --color-accent: #ff3e00;
  --color-border: #2a2a2a;

  /* Animation easings */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Animation Patterns

```css
/* Page load stagger */
.animate-stagger > * {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeUp 0.6s var(--ease-out-expo) forwards;
}

.animate-stagger > *:nth-child(1) { animation-delay: 0ms; }
.animate-stagger > *:nth-child(2) { animation-delay: 100ms; }
.animate-stagger > *:nth-child(3) { animation-delay: 200ms; }
.animate-stagger > *:nth-child(4) { animation-delay: 300ms; }

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Hover with personality */
.card {
  transition: transform 0.3s var(--ease-out-back);
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
}
```

### Background Atmosphere

```css
/* Gradient mesh - creates depth */
.hero-bg {
  background: 
    radial-gradient(ellipse at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(255, 62, 0, 0.2), transparent 50%),
    linear-gradient(180deg, var(--color-bg) 0%, var(--color-surface) 100%);
}

/* Noise texture overlay */
.textured::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/noise.svg');
  opacity: 0.03;
  pointer-events: none;
}
```

---

## Reference Files

**For detailed patterns, see:**
- `references/design-philosophy.md` — Complete aesthetics guide, theme recipes, anti-patterns
- `references/typescript-patterns.md` — Advanced TypeScript patterns, API types, hooks
- `references/component-library.md` — Production component implementations
- `references/animation-recipes.md` — Motion design patterns, scroll effects

---

## Anti-Patterns Checklist

Before shipping, verify you have NOT:

**Typography:**
- [ ] Used Inter, Roboto, Arial, or system fonts
- [ ] Font weights only differ by 200

**Color:**
- [ ] Purple gradient on white background
- [ ] Evenly distributed pastel palette

**Layout:**
- [ ] Perfectly centered everything
- [ ] Equal padding everywhere
- [ ] Standard Bootstrap-like grid

**Animation:**
- [ ] Default `ease` timing function
- [ ] No page load orchestration

**Backgrounds:**
- [ ] Solid white or #f5f5f5
- [ ] No texture or depth

---

## Final Reminder

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

**Remember**: Claude is capable of extraordinary creative work. Don't hold back—show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
