---
name: kaicalls-design
description: Build KaiCalls-compliant UI components and pages using the KaiCalls design system. Use when creating new dashboard pages, components, forms, tables, cards, badges, or any UI within the KaiCalls admin panel. Ensures dark-first aesthetic, proper color tokens, typography classes, motion standards, and B2B SaaS best practices. Triggers on "build a page", "create a component", "add a dashboard", "design a form", or any frontend work in the adminpanelnew codebase.
---

# kaicalls-design — UI that belongs in the KaiCalls admin panel

## Objective

UI that a KaiCalls user cannot tell was added later: dark-first, built from design-system tokens and shadcn/ui components, with every interactive element giving feedback the user can feel.

The product target is a Minimum Lovable Product — zero support required (so intuitive nobody opens docs), every click invokes emotion, micro-celebrations reward tedious work, conversational copy and helpful empty states make the software feel like a teammate, and the whole surface reads premium in the register of Linear, Notion, and Stripe.

Two rules pull against each other and both hold: **every interactive element gives emotional feedback**, and **that feedback stays subtle**. Our users include older professionals who spend long hours on screen; nothing flashes, strobes, or strains eyes.

## Done when

Work type `product-ui` — floor **E5/C4/O3** (`harness/eco-floors.yaml`).

- **E5** — the change is live in the product and a non-actor loaded the real screen at the real breakpoints. A green build and a deploy marked ready are E1 and E4; neither proves the screen renders.
- **C4** — the design field standard, verified before ship: hierarchy, WCAG AA contrast and focus order, token compliance over hardcoded values, responsive behavior at actual viewing sizes, and every loading, empty, and error state. Deviations need an explicit expiring waiver. The project's own tests plus this checklist are the C bar:

- Every button has emotional feedback: hover, active, and success states
- Feedback is subtle — no flashing, strobing, or harsh contrast
- Design-system color tokens throughout, no hardcoded hex
- Typography uses semantic classes (`heading-*`, `text-body-*`), not ad-hoc sizes
- Loading states use skeletons, not spinners
- Empty states carry helpful copy and a CTA
- Success actions show a micro-celebration (toast, animation, or color change)
- Destructive actions have confirmation plus reassurance afterward
- Animations run at 60fps and stay under 300ms
- `prefers-reduced-motion` respected via `motion-safe` / `motion-reduce`
- Dark-mode compatible — no light-only colors
- Mobile responsive down to 375px
- shadcn/ui components used wherever one exists

- **O3** — name the user behavior the change was supposed to move (task completion rate, time to first action, support tickets on that surface, drop-off) with a baseline, threshold, owner, and a 30-day window, recorded *before* building. A UI change that shipped and moved nothing is SHIPPED, not CLOSED.

## Constraints

- **Tokens, never hex.** Every color comes from the CSS variables or `kai-*` Tailwind classes below. A hardcoded hex is a defect even when it matches.
- **Motion budget is hard.** Micro-interactions (toggles, buttons) 120–160ms ease-out · small transitions 200–240ms ease-out · screen transitions 300–400ms `cubic-bezier(0.4, 0, 0.2, 1)`. Tokens: `--transition-fast: 150ms`, `--transition-normal: 200ms`, `--transition-slow: 300ms`.
- **Forbidden feedback:** bright flashes, strobing, high-contrast pops (white on dark), large jarring movement, anything over 300ms, anything that pulls attention off the task. Use soft glows, gentle scale (1.02–1.05x), muted color transitions, and spring physics with high damping.
- **Eye comfort:** muted success green (`#34D399` at ~60% opacity) rather than bright green · soft error red (`#FF4B4B` with transparency), never pure red · confetti and particles sparse and low-contrast · prefer opacity transitions to color flashes.
- **Never ship "No data found."** An empty state carries an optional illustration, copy explaining what belongs there, and a CTA that populates it.
- **Errors speak plainly.** "Something went wrong. We're looking into it. Try refreshing the page." — never a raw status code.
- **Destructive actions name their consequences** in the confirm dialog (what is deleted, what goes with it, that it cannot be undone), and reassure immediately after.

## Context

| Need | Load |
|---|---|
| Complete CSS variable and Tailwind class list | `references/full-color-tokens.md` |
| Real-world dashboard, table, and form patterns | `references/component-examples.md` |

**Core color tokens**

```css
/* Surfaces */          /* Brand */                    /* Text */
--background: #12121A   --kai-blue: #5C8CFF            --foreground: #F7F7FA
--card: #181B23         --kai-purple: #C68BF8          --muted-foreground: #A7A9BE
--secondary: #23263B    --kai-btn-primary: #3575F6     --kai-text-placeholder: #6B6D76
--surface-elevated: #2A2D3E

/* Status */
--kai-success-text: #34D399   --kai-error-text: #FF4B4B
--kai-warning-text: #FFC04B   --kai-info-text: #5C8CFF
```

**Tailwind classes.** Surfaces: `bg-background` (page), `bg-card` (cards), `bg-secondary` (inputs and secondary surfaces). Text: `text-foreground` (primary), `text-muted-foreground` (secondary), `text-kai-blue`, `text-kai-purple`. Borders: `border-border`, `border-kai-table-border`.

**Typography.** Headings `heading-xl` (2xl bold white, page title) · `heading-lg` (xl semibold, section) · `heading-md` (lg semibold, card) · `heading-sm` (base semibold, subsection). Body `text-body-primary` (white) · `text-body-secondary` (slate-400) · `text-body-tertiary` (slate-500, timestamps). Labels `label-uppercase` (xs uppercase tracking-wide slate-400) · `label-default` (sm medium slate-400) · `stat-label` (xs uppercase slate-400). Values use `data-value`.

**Components.** All from `@/components/ui/*`.

- **Card** — `Card` / `CardHeader` / `CardTitle` / `CardDescription` / `CardContent`. Base: `rounded-lg border-slate-700/50 bg-slate-800/60 text-white shadow-sm`.
- **Button** — variants `default` (primary), `secondary`, `outline`, `destructive`, `ghost`, `link`; sizes `sm`, `default`, `lg`, `icon`.
- **Badges** — temperature: `badge-hot` (bg `#FF4B4B33`, text `#FF6B6B`), `badge-warm` (`#FFC04B33` / `#FFD76B`), `badge-cold` (`#4B7BFF33` / `#6B93FF`). Status: `status-success`, `status-error`, `status-warning`, `status-info`. All badges: `rounded-full px-2.5 py-0.5 font-semibold`.
- **Tables** — `table-row hover:bg-kai-hover-row`, `table-row-selected`, cells `px-4 py-3`, headers `text-kai-text-table-heading` (`#B0B2C3`).
- **Inputs** — `Input` + `Label` wrapped in `space-y-2`. Base `bg-secondary border-border text-foreground`, focus `ring-kai-blue`.
- **Dialogs** — `DialogContent className="bg-modal-bg border-modal-border"` with `DialogHeader` / `DialogTitle` / `DialogDescription`. Destructive flows use `AlertDialog` with a keep-it action and a consequence-naming confirm action.
- **Elevation** — `shadow-elevation-sm` (subtle), `-md` (cards), `-lg` (dropdowns), `-xl` (modals). Z-index: `z-dropdown` 50, `z-modal` 100, `z-toast` 150.
- **Gradient** — `bg-gradient-kai` and `text-gradient-kai`, both `linear-gradient(90deg, #5C8CFF 0%, #C68BF8 100%)`.
- **Animation classes** — `skeleton-shimmer` for loading, `collapsible-content` and `collapsible-chevron` for disclosure.

**Micro-celebration triggers**

| Action | Feedback | Implementation |
|---|---|---|
| Task complete | Soft checkmark fade-in | Icon opacity 0→1 over 200ms |
| Form submit | Gentle green tint, quiet toast | Subtle bg shift, no flash |
| Delete / archive | Smooth slide away | Slide-out 250ms with opacity fade |
| Toggle on | Soft snap into place | Spring, damping 0.8 |
| Save success | Soft glow around button | Box-shadow fade in/out over 400ms |
| Error | Gentle wobble + muted red | 2–3px horizontal shake, soft red |

**Hover and focus.** Buttons `hover:scale-[1.02] hover:brightness-105 transition-all duration-150`. Cards `hover:shadow-elevation-md hover:-translate-y-0.5 transition-all duration-200`. Links `hover:text-kai-purple/80 transition-colors duration-150`. Reduced motion: `motion-safe:hover:scale-[1.02] motion-reduce:hover:opacity-80`, or check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` in JS.

**Button states.** A success button flips to a `Check` icon with `bg-kai-success-text scale-105` for ~1500ms, then reverts. A loading button is `disabled` and shows `<Loader2 className="mr-2 h-4 w-4 animate-spin" />` with an anticipatory label ("Saving...").

**Toasts** come from `sonner`, with a title and a description that says what actually happened — `toast.success("Agent created!", { description: "Your AI assistant is ready to take calls." })`. Milestones may carry an emoji icon. After a destructive action, the toast reassures: "Agent deleted — don't worry, your leads are still safe."

**Page layout.** A page is `space-y-6`: a header row (`flex items-center justify-between`) holding `heading-xl` plus a `text-body-secondary mt-1` description on the left and the primary action button on the right, followed by content in `grid gap-6 md:grid-cols-2 lg:grid-cols-3`.

**Stat card.** `CardContent className="p-6"` containing a `flex items-center justify-between` row with `stat-label` and a muted icon, then `mt-2` with `data-value` and a delta in `text-kai-success-text text-sm ml-2`.

**Loading.** Skeletons match content shape — a card skeleton mirrors header and body block heights (`h-6 w-48`, `h-4 w-32 mt-2`, `h-24 w-full`); a table skeleton repeats rows of column-width bars.

## Escalate when

- The design calls for a color, spacing value, or component that no token or shadcn/ui component covers — the system extends deliberately, not inline.
- Feedback strong enough to be noticed would breach the eye-comfort rules.
- A pattern is needed that `references/component-examples.md` does not cover and would set precedent across the admin panel.
- A flow requires a destructive action without a safe undo or a clear consequence statement.
- Accessibility (contrast, focus order, reduced motion) and the requested aesthetic conflict.
