---
name: cermont.frontend.tailwind-css-v4-mastery
description: >
  Expert guidance for leveraging Tailwind CSS V4's new Oxide engine, CSS-first
  configuration, and modern styling paradigms. Transforms agent into Tailwind V4 
  architecture specialist, capable of designing component systems, optimizing 
  performance, and executing complex styling challenges with precision.
  
triggers:
  - tailwind v4
  - tailwind 4
  - css-first configuration
  - oxide engine
  - "@theme directive"
  - tailwind migration
  - tailwind component
  - style system
role: PRIMARY
scope: frontend
version: 1.0.0
license: MIT
---

<!-- Cermont Project Fit -->
## Project Fit

| Attribute | Value |
|-----------|-------|
| **Applies to** | frontend |
| **Requires** | Angular, TailwindCSS, PostCSS |
| **Not for this repo** | Vite (React), Next.js, Vue |
| **Status** | ✅ PRIMARY for UI/Styling family |

### Guardrails

**Does NOT do:**
- Install dependencies without user approval
- Modify pnpm-lock.yaml directly
- Change postcss.config.js automatically

**Safety Checklist:**
```bash
pnpm --filter @cermont/frontend lint
pnpm --filter @cermont/frontend build
# Rollback: git restore -SW .
```

### Angular Integration Note
Cermont uses Angular CLI with PostCSS. Replace Vite examples with:
- `@tailwindcss/vite` → `@tailwindcss/postcss`
- Configure in `angular.json` with custom webpack builder
<!-- End Project Fit -->

---

## Core Conceptual Landscape

### 1. The Oxide Engine Revolution

**What Changed:**
```
v3: JavaScript → JavaScript Parser → CSS Output
v4: CSS @theme → Rust/Oxide Engine → Optimized CSS Output
```

**Why It Matters:**
- **Performance:** 10-100x faster build times, 15-30x faster HMR
- **Simplicity:** One language (CSS) instead of two (JS + CSS)
- **Future-Proofing:** Aligned with native browser capabilities

**Mental Model:** Think of the Oxide engine as a compiler, not a preprocessor. It compiles CSS declarations into optimized output.

### 2. CSS-First Configuration Paradigm

**The Core Shift:**

| Aspect | v3 | v4 |
|--------|-----|-----|
| Config Format | JavaScript Object | CSS `@theme {}` Block |
| Location | `tailwind.config.js` | `styles.css` |
| Execution | Node.js at build time | Oxide engine |
| Debugging | Console logs, file inspection | CSS DevTools |
| Scope | Global import | CSS cascade-aware |

**Why This Matters:** CSS-first configuration is more maintainable, debuggable, and aligned with how browsers actually work. You're no longer fighting a layer of abstraction.

### 3. Browser Requirements & Modern CSS Features

Tailwind V4 **requires** modern browser capabilities:
- **Safari 16.4+** (OKLch color space, `@property`)
- **Chrome 111+** (`color-mix()`)
- **Firefox 128+** (CSS nesting)

This is intentional. V4 **assumes** modern CSS and optimizes around it. Legacy support requires v3.4.x.

---

## Procedural Workflows

### Workflow 1: Migration from V3 to V4

**Trigger:** User wants to upgrade existing Tailwind project from v3 to v4

**Steps:**

1. **Audit Phase**
   - List all `tailwind.config.js` overrides
   - Identify custom utilities and components
   - Scan for deprecated utility usage (opacity, flex-shrink, etc.)
   - Check browser support requirements

2. **Installation Phase**
   ```bash
   npm install -D tailwindcss@latest
   npm install -D @tailwindcss/vite  # (or @tailwindcss/postcss or @tailwindcss/cli)
   ```

3. **Configuration Migration**
   - Convert `theme: {}` → `@theme { --var: value; }`
   - Convert `extend: {}` → Additional `--var` in `@theme`
   - Replace `@tailwind base/components/utilities` → `@import "tailwindcss"`

4. **Utility Refactoring**
   - `.shadow` → `.shadow-sm`
   - `.rounded` → `.rounded-sm`
   - `.outline-none` → `.outline-hidden`
   - `.bg-opacity-*` → `.bg-black/*` (slash syntax)

5. **Validation**
   - Test responsive breakpoints
   - Verify dark mode
   - Check custom components
   - Performance baseline

**Decision Tree:**
```
Is this a new project?
  ├─ YES → Use V4 directly with @theme config
  └─ NO → Execute migration workflow above
     ├─ Does v3 use custom config extensively?
     │  ├─ YES → Allocate migration time, go step-by-step
     │  └─ NO → Quick migration, 30 mins
     └─ Are you on legacy browsers?
        ├─ YES → Stay on v3.4
        └─ NO → Proceed with v4
```

### Workflow 2: Component System Design

**Trigger:** User wants to build reusable component library with Tailwind V4

**Steps:**

1. **Define Component Scope**
   - List component primitives (Button, Card, Input, etc.)
   - Identify shared styling patterns
   - Plan for theme customization

2. **Create Base Theme**
   ```css
   @import "tailwindcss";
   
   @theme {
     /* Color system */
     --color-primary-*: oklch(...);
     --color-neutral-*: oklch(...);
     
     /* Spacing scale */
     --spacing-xs: 0.25rem;
     --spacing-sm: 0.5rem;
     --spacing-md: 1rem;
     
     /* Typography */
     --font-display: "Custom", sans-serif;
     --font-body: "System", sans-serif;
   }
   ```

3. **Build Component Classes**
   ```css
   @layer components {
     .btn-primary {
       @apply px-4 py-2 rounded-sm bg-primary text-white
              font-semibold transition-all hover:opacity-90;
     }
     
     .card {
       @apply p-6 rounded-lg bg-white shadow-md border border-gray-200;
     }
   }
   ```

4. **Establish Modifier Conventions**
   - Size modifiers: `.btn-sm`, `.btn-lg`
   - State modifiers: `.btn-disabled`, `.btn-loading`
   - Variant modifiers: `.btn-primary`, `.btn-secondary`

5. **Document & Export**
   - Create component reference
   - Provide usage examples
   - Document theme variables

**Output:** Production-ready component library CSS file

### Workflow 3: Performance Optimization

**Trigger:** User needs to optimize Tailwind V4 performance

**Steps:**

1. **Baseline Measurement**
   - Measure current build time
   - Check CSS file size
   - Monitor HMR speed

2. **Plugin Selection**
   - Use `@tailwindcss/vite` (fastest option)
   - Enable Lightning CSS if using PostCSS
   - Disable unnecessary optimizations

3. **Configuration Tuning**
   ```javascript
   // vite.config.ts
   import tailwindcss from "@tailwindcss/vite";
   
   export default defineConfig({
     plugins: [react(), tailwindcss()]
   });
   ```

4. **CSS Variable Optimization**
   - Use native CSS variables instead of computed values
   - Leverage cascade for scoped themes
   - Minimize `@theme` block duplication

5. **Validation**
   - Verify build time improvement
   - Check file size reduction
   - Confirm visual consistency

**Expected Outcomes:**
- Build time: 100-500ms (vs 5-10s in v3)
- Hot reload: 50-200ms (vs 3s in v3)
- CSS size: -15-20% reduction

---

## Critical Decision Trees

### Decision 1: Plugin Selection

```
What build tool do you use?
├─ Vite (React, Vue, Svelte)
│  └─ Use @tailwindcss/vite (fastest, recommended)
├─ Webpack (NextJS, CRA)
│  └─ Use @tailwindcss/postcss
├─ Standalone/No bundler
│  └─ Use @tailwindcss/cli
└─ PostCSS pipeline
   └─ Use @tailwindcss/postcss
```

### Decision 2: Configuration Approach

```
How complex is your theme?
├─ Simple (5-10 color overrides)
│  └─ Use inline @theme block in styles.css
├─ Moderate (custom colors, spacing, fonts)
│  └─ Use single @theme block with organization
├─ Complex (multi-theme, extensive customization)
│  └─ Split into @layer base blocks with [data-theme] selectors
└─ Enterprise (multiple brands)
   └─ Use CSS variable strategy with fallbacks
```

### Decision 3: Component Extraction

```
When should I use @layer components?
├─ Recurring utility combinations
│  └─ YES → Extract to .btn-primary, .card, etc.
├─ One-off layouts
│  └─ NO → Use utilities directly in HTML
├─ Design system compliance needed
│  └─ YES → Extract as component class
└─ User will customize per instance
   └─ NO → Leave as utility composition
```

---

## Common Gotchas & Solutions

### Gotcha 1: Expecting `tailwind.config.js` to Still Work
**Problem:** File is ignored in v4.  
**Solution:** Use `@theme {}` in CSS instead.  
**Prevention:** Delete `tailwind.config.js` early in migration.

### Gotcha 2: Default Border Color Breaking Layouts
**Problem:** v3 used `currentColor` (inherits text), v4 uses `#e5e7eb`.  
**Solution:** Use `.border-current` if you need inherited color.  
**Prevention:** Test all border utilities during migration.

### Gotcha 3: Ring Width Changed (3px → 1px)
**Problem:** Existing `.ring` classes now have thinner outlines.  
**Solution:** Use `.ring-3` for old 3px behavior, `.ring-1` for new default.  
**Prevention:** Find/replace `.ring` → `.ring-1` during migration.

### Gotcha 4: CSS Variables Must Have `--` Prefix
**Problem:** `@theme { color-primary: value; }` is ignored.  
**Solution:** Use `@theme { --color-primary: value; }`.  
**Prevention:** Always use `--` in `@theme` blocks.

### Gotcha 5: Opacity Utilities Removed
**Problem:** `.bg-opacity-50` no longer exists.  
**Solution:** Use CSS color modifiers: `.bg-black/50`.  
**Prevention:** Search codebase for opacity utilities and replace during migration.

---

## Reference Materials

All detailed references are stored in `references/`:

- **breaking-changes.md** — Complete list of API removals and renames
- **configuration-guide.md** — Comprehensive `@theme` setup patterns
- **utility-migration-table.md** — v3 → v4 utility mappings
- **color-space-guide.md** — OKLch, HSL, and color migration strategies
- **performance-tuning.md** — Optimization techniques and measurements

---

## When to Use This Skill

✅ **Use this skill when:**
- User asks about Tailwind V4 specifically (not v3)
- Designing component systems or styling architectures
- Migrating from Tailwind v3 to v4
- Optimizing Tailwind performance
- Troubleshooting CSS-first configuration issues
- Building design systems with Tailwind V4
- Creating custom theme configurations

❌ **Don't use this skill when:**
- User asks about Tailwind v3 or older (use general CSS knowledge)
- Question is about HTML/JavaScript/Framework-specific issues (not Tailwind's domain)
- User needs general CSS tutoring (use CSS fundamentals instead)
- Building non-web projects

---

## Execution Standards

When activated by user query:

1. **Clarify Intent** — Ask what they're building and why (component? migration? optimization?)
2. **Choose Workflow** — Route to appropriate procedural path
3. **Provide References** — Link to relevant reference materials
4. **Show Code Examples** — Concrete, copy-paste-ready examples
5. **Explain Trade-offs** — Why certain decisions matter
6. **Test Assumptions** — Verify understanding before deep work

---

## Advanced Capabilities

This skill enables Claude to:

- **Design component systems** that leverage Tailwind V4's architecture
- **Execute migrations** from v3 to v4 with minimal risk
- **Optimize builds** using Oxide engine capabilities
- **Debug CSS-first configuration** issues systematically
- **Teach Tailwind V4** philosophy to teams
- **Architect design systems** using CSS variables + Tailwind
- **Handle edge cases** around browser support and feature detection

---

## Resources & References

- Official Docs: https://tailwindcss.com/docs
- GitHub: https://github.com/tailwindlabs/tailwindcss
- Playground: https://play.tailwindcss.com
- Discord: https://tailwindcss.com/discord

---

**Skill Version:** 1.0.0  
**Last Updated:** 2025-01-01  
**Status:** Production Ready
