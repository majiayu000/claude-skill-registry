---
name: casper-design-system
description: >
  Casper Studios internal design system for generating consistent, production-grade SaaS UI.
  Use this skill whenever generating UI code for internal tools, client apps, dashboards,
  POCs, prototypes, or any visual interface — even quick mockups or artifacts. Apply it
  any time the output is a React component, page, or layout. If the user mentions "our
  design system", "Casper style", "match our look", or asks you to build any kind of app
  or interface, use this skill. Also trigger when restyling or theming existing UI to match
  Casper's visual language. This skill takes priority over generic frontend-design guidance.
---

# Casper Studios Design System

A clean, elevated SaaS design system built on **shadcn/ui**, **Tailwind CSS v4**, and **React (Vite)**. Every interface generated for Casper Studios — whether a client demo, internal tool, or quick prototype — must follow these rules to maintain a consistent, professional visual identity across the team.

Before generating any UI code, read this file completely **and** the reference files listed below. You **MUST** read the reference files — they contain rules and code examples that are required for correct output. Skipping them will produce incorrect, off-brand UI.

**Required for EVERY project:**

- **`references/components.md`** — ALWAYS read. Reusable pieces: stat cards, list items, filter bars, kanban boards, profile cards, product cards, activity feeds, toast notifications, form validation states. Required whenever building UI elements inside a layout.
- **`references/theme.css`** — ALWAYS read. Tailwind CSS v4 theme tokens. Copy this file into your project as-is.
- **`assets/`** — Contains Casper Studios logo SVGs in 4 variants (default, variant, mono-black, mono-white). Use the correct variant based on background color — see the Logo section below.

**Required based on platform:**

- **`references/web-layouts.md`** — MUST read when the project is a **web application**. Web-specific responsive rules + code examples: app shell, sidebar nav, dashboard grid, data table page, page header.
- **`references/mobile.md`** — MUST read when the project is a **mobile application**. Mobile-specific rules + code examples: device frame, top bar, bottom tab navigation, form patterns, pinned-button layout, list views, card stacks, full screen compositions, contextual actions (menus + bottom sheets).

> **Non-negotiable:** Do not generate UI without reading the platform reference file first. If you are unsure whether the project is web or mobile, ask the user before proceeding.

---

## Before You Generate: Required Context

Before producing any UI code, confirm the following with the user. If their prompt already answers these clearly, proceed without asking. If not, ask before generating anything.

1. **Platform** — Is this a web application or a mobile application? (Determines which reference file to follow.)
2. **Dark mode** — Should the interface support dark mode, or is it light mode only? (Determines whether to implement `.dark` class overrides, use `bg-neutral-0` for surfaces, and include the mono-white logo variant.)

Do NOT assume defaults for these. If the user says "build me a dashboard," you don't know if it's web or mobile, or if it needs dark mode. Ask.

---

## Summary

The Casper aesthetic is **clean authority** — a professional SaaS style that feels premium without trying too hard. It uses generous whitespace, a restrained purple accent, and soft rounded surfaces to create interfaces that feel trustworthy and modern. Think Linear meets Notion: structured, breathable, quietly confident.

---

## Core Principles

1. **Whitespace is a feature.** Generous padding, breathing room between sections. Never cram.
2. **One accent, used sparingly.** Brand purple (`#5900FF`) appears on active states, primary buttons, and key CTAs — nowhere else. If everything is purple, nothing is.
3. **Rounded but not bubbly.** 10px default radius for cards (shadcn default). Buttons and inputs use 8px. Feels modern without feeling like a toy.
4. **Flat with depth hints.** No heavy shadows. Use `shadow-sm` for cards, `shadow-md` for popovers. Never use `shadow-lg` on in-page elements.
5. **Content over chrome.** The UI should disappear. Users notice the data, not the design.

---

## Tech Stack

- **React** (Vite) with TypeScript
- **Tailwind CSS v4** — Use the theme file at `references/theme.css` as Casper brand overrides
- **shadcn/ui** — Initialize a standard shadcn/ui project first (`shadcn init`), then layer Casper brand tokens from `references/theme.css` on top. The shadcn semantic layer (`bg-background`, `text-foreground`, `bg-primary`, `border-border`, etc.) is the base — Casper's theme.css adds brand colors, typography, shadows, and spacing on top of it, not as a replacement. Use shadcn components directly. Do NOT create custom base components that duplicate shadcn functionality
- **Lucide React** — Icon library. Always use Lucide, never Heroicons or FontAwesome
- **Fonts** — `DM Sans` with `sans-serif` as fallback for all UI text. Load via Google Fonts or bundle

---

## Color System

The palette is intentionally restrained. Most of the UI is neutral gray + white, with purple as a sharp accent.

### Usage Rules

| Role             | Token         | Hex       | When to use                                                                                       |
| ---------------- | ------------- | --------- | ------------------------------------------------------------------------------------------------- |
| **Brand accent** | `brand-500`   | `#5900FF` | Active nav items, primary buttons, links, focus rings                                             |
| **Brand subtle** | `brand-50`    | `#EEE5FF` | Active nav background, selected row highlight, hover tints                                        |
| **Brand light**  | `brand-100`   | `#DECCFF` | Icon circle backgrounds, soft tag fills                                                           |
| **Default text** | `neutral-950` | `#0A0A0A` | Page titles, headings                                                                             |
| **Body text**    | `neutral-900` | `#171717` | Primary body text                                                                                 |
| **Subtext**      | `neutral-500` | `#737373` | Metadata, timestamps, secondary labels                                                            |
| **Borders**      | `neutral-200` | `#E5E5E5` | Card borders, dividers, table lines                                                               |
| **Surface**      | `neutral-50`  | `#FAFAFA` | Page background behind cards                                                                      |
| **Card surface** | `neutral-0`   | `#FFFFFF` | Card backgrounds, panels (use `bg-neutral-0` for dark mode compatibility — see Dark Mode section) |

### Semantic Colors

Use these ONLY for status indicators, badges, and contextual feedback — never as decorative accents.

- **Success** — `success-500` (`#22C55E`) for badges/icons, `success-50` for pill backgrounds
- **Error** — `error-500` (`#EF4444`) for badges/icons, `error-50` for pill backgrounds
- **Warning** — `warning-500` (`#F59E0B`) for badges/icons, `warning-50` for pill backgrounds

### What NOT to do

- Do NOT use brand purple for backgrounds on large surfaces
- Do NOT use semantic colors decoratively
- Do NOT introduce new colors. If you need a new shade, use the neutral scale
- Do NOT use opacity-based colors when a token exists (e.g., don't do `text-black/50`, use `neutral-500`)

---

## Typography

All text is set in **DM Sans** with **sans-serif** as fallback (`font-family: 'DM Sans', sans-serif`). Monospace (`font-mono`) is acceptable for code blocks, data labels, and IDs only.

### Scale

| Style            | Size | Weight | Line Height | Use                                      |
| ---------------- | ---- | ------ | ----------- | ---------------------------------------- |
| **Heading 1**    | 30px | 500    | 36px        | Page titles only. One per view.          |
| **Heading 2**    | 20px | 500    | 24px        | Section titles within a page             |
| **Heading 3**    | 16px | 500    | 20px        | Card titles, subsection labels           |
| **Body**         | 14px | 400    | 20px        | Default paragraph and UI text            |
| **Body Bold**    | 14px | 500    | 20px        | Emphasis within body text, table headers |
| **Caption**      | 12px | 400    | 16px        | Timestamps, helper text, metadata        |
| **Caption Bold** | 12px | 500    | 16px        | Badge labels, small category tags        |

### Rules

- Headings are always `medium` weight (500), never bold (700)
- NEVER use all-caps except for tiny metadata labels (e.g., "STATUS", "OWNER" in table column headers) set at caption size
- Links use `brand-500` color with no underline by default, underline on hover
- Do NOT vary font size beyond this scale. If something feels wrong, adjust spacing not font size

---

## Spacing & Layout

### Spacing Scale

Use Tailwind's default spacing scale. Key values:

- `4px` (p-1) — icon padding, tight gaps
- `8px` (p-2) — badge padding, small gaps
- `12px` (p-3) — input padding, card internal gaps
- `16px` (p-4) — card padding, section gaps
- `24px` (p-6) — between cards, content sections
- `32px` (p-8) — major section separation
- `48px` (p-12) — page-level padding on large screens

### Layout Rules

- Page background: `neutral-50` (`#FAFAFA`)
- Content is always organized inside **Cards** (white background, border, rounded)
- Maximum content width: `1280px` centered
- On pages with a sidebar, sidebar is `240px` fixed width
- Main content area uses remaining space with `24px` padding

---

## Shadows & Elevation

The design is predominantly flat. Shadows are used to indicate layers, not to add decoration.

| Token            | Use                                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| `shadow-sm`      | Cards, inputs at rest                                                                                      |
| `shadow-md`      | Dropdown menus, popovers, tooltips                                                                         |
| `shadow-lg`      | Modals, command palettes, overlays ONLY                                                                    |
| `shadow-overlay` | Semantic alias for `shadow-lg` — identical value. Use on modals/sheets so the intent reads clearly in code |

NEVER apply `shadow-lg` (or its alias `shadow-overlay`) to cards or in-page elements. These are reserved for floating layers only.

---

## Border Radius

The theme file (`references/theme.css`) uses the **shadcn/ui radius system** — a single `--radius` base variable in `:root` that controls the entire scale via `calc()`. This is mapped into Tailwind classes via `@theme inline`. No Tailwind v4 defaults are overridden.

| Token               | Tailwind Class | Default Value | Use                                                        |
| ------------------- | -------------- | ------------- | ---------------------------------------------------------- |
| `--radius-sm`       | `rounded-sm`   | 6px           | Inner elements, nav items, small nested controls           |
| `--radius-md`       | `rounded-md`   | 8px           | **Buttons, inputs**, popovers, tooltips, chart tooltips    |
| `--radius-lg`       | `rounded-lg`   | 10px          | Cards, panels, large containers                            |
| `--radius-xl`       | `rounded-xl`   | 14px          | Modal containers, dialogs, hero cards                      |
| (Tailwind built-in) | `rounded-full` | 9999px        | Badges, pills, avatars, icon circles                       |

The base value `--radius: 0.625rem` (10px) is the shadcn default. To make the entire UI sharper or rounder, change this single value — all tokens recalculate automatically.

Cards always use `rounded-lg` (10px). Buttons and inputs always use `rounded-md` (8px). Nested elements inside cards should use `rounded-sm` (6px) for non-interactive elements to maintain visual hierarchy — the inner radius should always be smaller than the outer.

---

## Iconography

- Use **Lucide React** exclusively. Import as: `import { IconName } from "lucide-react"`
- Default icon size: `16px` for inline, `20px` for standalone
- Icon color follows its text context (e.g., `neutral-500` for subtext, `brand-500` for active)
- For icons inside circular backgrounds (common in lists and dashboards):
  - Circle: `40px` diameter, `brand-50` or `brand-100` background, `rounded-full`
  - Icon: `20px`, `brand-500` color
  - For semantic contexts, swap to the matching semantic color pair (e.g., `error-50` bg + `error-500` icon)

---

## Casper Studios Logo

The Casper Studios logo has four variants stored in `assets/`. Use the correct variant based on the background it sits on:

| Variant                  | File                               | When to use                                                                                                                                                    |
| ------------------------ | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Default (full color)** | `assets/logo-on-white-default.svg` | Light/white backgrounds. Gradient icon + purple "CASPER" + dark "STUDIOS". This is the primary logo — use it whenever possible.                                |
| **Variant (full color)** | `assets/logo-on-white-variant.svg` | Light/white backgrounds when you want all-black text instead of purple + dark gray. Same gradient icon.                                                        |
| **Mono Black**           | `assets/logo-mono-black.svg`       | Light backgrounds where color is unavailable (e.g., print, grayscale contexts). Grayscale icon + near-black text.                                              |
| **Mono White**           | `assets/logo-mono-white.svg`       | **Dark backgrounds only.** Gray icon + white text. Use this whenever the logo sits on a dark surface (dark nav bars, dark hero sections, overlays, dark mode). |

### Rules

- **Light mode** (default): Use `logo-on-white-default.svg` or `logo-on-white-variant.svg`
- **Dark mode** or dark surfaces: Use `logo-mono-white.svg` — never place the default or black logo on a dark background
- The logo should appear in the **sidebar header** (web) or **top bar** (mobile) at the sizes defined in those patterns
- Do NOT resize the logo disproportionately — maintain the original aspect ratio
- Do NOT place the logo on busy backgrounds or low-contrast surfaces. If contrast is insufficient, use the mono variant that provides the best visibility
- Minimum clear space around the logo: `8px` on all sides

---

## shadcn/ui Component Theming

Use shadcn/ui components as your base layer. Theme them using the CSS variables in `references/theme.css`. Here is how specific components should be configured:

### Button

- **Primary**: `brand-500` bg, `text-white` (literal white, not a token), `rounded-md`. Hover: `brand-600`.
- **Secondary**: White bg, `neutral-200` border, `neutral-900` text, `rounded-md`. Hover: `neutral-50` bg.
- **Ghost**: No bg, no border. `neutral-600` text, `rounded-md`. Hover: `neutral-100` bg.
- **Destructive**: `error-500` bg, `text-white`, `rounded-md`.
- All buttons: `rounded-md` (8px), `14px` font.
- **Default height**: `48px` (`h-12`). Use this on standalone pages, forms, modals, and any top-level content area.
- **Compact height**: `36px` (`h-9`). Use when the button lives inside a smaller container — cards, panels, table rows, sidebar nav, filter bars, inline actions. The tighter context calls for a tighter control.

### Badge

- `rounded-full` (pill shape). Height `22px`. Caption-bold text (12px, 500 weight).
- **Semantic badges**: Use pastel bg + darker text. E.g., success badge = `success-50` bg, `success-700` text.
- **Neutral badge**: `neutral-100` bg, `neutral-700` text.
- **Brand badge**: `brand-50` bg, `brand-700` text.
- Always include a small dot or icon before the label when indicating status.

### Card

- White background (`bg-neutral-0`). `1px` `neutral-200` border. `rounded-lg` (10px). `shadow-sm`.
- Internal padding: `16px` minimum, `24px` for spacious cards.
- Card headers: `Heading 3` (16px/500) with optional "View all" link aligned right.
- Separate header from content with a `1px` `neutral-200` divider.

### Table

- Use shadcn `<Table>`. No outer border on the table itself — let the parent Card provide the container.
- Column headers: Caption-bold (12px/500), `neutral-500` color, uppercase.
- Row height: `48-56px`. Rows separated by `1px` `neutral-200` bottom border.
- Row hover: `neutral-50` background.
- No alternating row colors.

### Input / Textarea

- `rounded-md` (8px). `1px` `neutral-200` border. `neutral-50` bg or white bg.
- Focus: `2px` `brand-500` ring (use Tailwind `ring-2 ring-brand-500`).
- **Labels MUST be visible and external** — render a `<label>` element above every input, never inside it. Labels use `14px`/400 in `neutral-900`. The gap between label and input is `6px` (`space-y-1.5`).
- **Placeholder text MUST be de-emphasized** — `neutral-400` color, normal weight (400), short hint text (e.g., "e.g. john@email.com"). Placeholders are supplementary hints, not labels.
- **Select inputs** follow the same pattern: visible label above, de-emphasized placeholder inside.
- **Spacing between fields**: `16px` (`space-y-4` or `gap-4`).
- **Default height**: `48px` (`h-12`). Use for inputs on standalone pages, forms, modals, and any top-level content area.
- **Compact height**: `36px` (`h-9`). Use when the input lives inside a smaller container — cards, panels, table rows, filter bars, inline search fields. Same logic as compact buttons.

### Sidebar (App Shell)

See `references/web-layouts.md` for the full sidebar code pattern. Key specs:

- Width: `240px`. White background. Right border: `1px` `neutral-200`.
- Nav items: `36px` height (compact — inside sidebar panel), `rounded-sm` (6px), `12px` left padding.
  - Default: `neutral-600` text. Active: `brand-50` bg, `brand-500` text, `font-weight: 500`. Hover: `neutral-100` bg.
- Group labels: Caption (12px/400), `neutral-400`, `24px` top margin between groups.
- On mobile: Sidebar collapses to a `Sheet` (slide-in from left).

### Tabs

- Use shadcn `<Tabs>`. Underline variant.
- Active tab: `brand-500` bottom border (2px), `neutral-900` text.
- Inactive tab: no border, `neutral-500` text. Hover: `neutral-900` text.

### Dialog / Sheet

- Overlay: `black/50` opacity.
- Container: white bg, `rounded-xl` (14px), `shadow-overlay`.
- Always include a close button (X icon) top-right.

---

## Composite Patterns

For rules and code examples, read the appropriate reference file:

- **`references/web-layouts.md`** — Responsive rules, App Shell, Sidebar Navigation, Dashboard Grid, Data Table Page, Page Header
- **`references/components.md`** — Stat Card, List Item Row, Filter Bar, Kanban Board, Profile/Discovery Card, Product Card, Activity Feed Item, Toast Notifications, Form Validation States
- **`references/mobile.md`** — Mobile rules, Device Frame Shell, Mobile Top Bar, Bottom Tab Navigation, Mobile Form Layout, Pinned Bottom Button, Mobile List View, Mobile Card Stack, Full Screen Composition, Contextual Actions

---

## Web vs Mobile Context

Every project is either a **web application** or a **mobile application** — the layout approach is fundamentally different. You MUST have already read the appropriate platform reference file (as instructed at the top of this document) before reaching this point. If you haven't, stop and read it now:

- **Web application** → `references/web-layouts.md` (responsive breakpoints, sidebar behavior, layout patterns)
- **Mobile application** (native app, iOS, Android, phone-based experience) → `references/mobile.md` (device frame, touch targets, pinned buttons, navigation, mobile-specific rules)

Do NOT treat a mobile app as a responsive web page. Mobile apps render inside a device frame and follow entirely different navigation, spacing, and interaction patterns.

---

## Image Placeholders

When no real image is available, use **soft gradient mesh backgrounds** — NOT gray boxes. These should feel like abstract art, not loading states.

Gradient recipes (CSS `linear-gradient` or `radial-gradient` combos):

- **Mint/Teal**: `linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #a8edea 100%)`
- **Peach/Coral**: `linear-gradient(135deg, #f6d5c5 0%, #e8b4b8 50%, #d4a0a0 100%)`
- **Purple/Pink**: `linear-gradient(135deg, #c3b1e1 0%, #f0c4d0 50%, #e0aed0 100%)`
- **Teal/Emerald**: `linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)`

Apply `rounded-lg` to image containers. These are placeholders — they should look intentional and beautiful.

---

## Transitions & Animations

Every state change should feel smooth and intentional — no hard cuts. This applies across both web and mobile:

- **Interactive elements** (buttons, inputs, cards): Use `transition-colors` or `transition-all` with Tailwind's default duration (~150ms). State changes like hover, focus, and active should never feel instantaneous.
- **Page transitions**: When navigating between views, apply a subtle slide or fade. A `150–300ms` ease-out transition keeps things feeling responsive without sluggish.
- **Modals, Dialogs, Sheets**: Always animate in and out. Sheets slide from their edge (left, right, bottom), dialogs/modals fade + scale up slightly from ~95% to 100%. The overlay backdrop should fade in (`opacity 0→50%`), not appear instantly.
- **Lists and content loading**: When new items appear (e.g., after a fetch), a subtle fade-in or stagger is preferred over a hard pop-in.

Nothing on screen should ever just "appear" or "disappear" — every visual change gets a brief, smooth transition.

---

## Empty, Error & Loading States

Every screen has at least three faces: populated, empty, and broken. AI-generated interfaces almost always show only the happy path with fake data. A polished interface acknowledges the other two.

### Empty State

When a list, table, or content area has no data yet (first-time use, zero results, cleared filters):

- Center a Lucide icon (`48px`, `neutral-300`) + a short heading (`Heading 3`) + one line of body text (`neutral-500`) vertically in the content area
- Optionally include a primary action button below the text (e.g., "Create your first project")
- Do NOT show an empty table with headers and no rows — that looks like a bug, not a feature
- Do NOT use illustrations or complex graphics. Keep it text + icon. Minimal.

### Error State

When something goes wrong (network failure, permission denied, server error):

- Same centered layout as empty state, but use `error-500` for the icon color
- Icon: contextual — `WifiOff` for network errors, `ShieldX` for permission, `AlertTriangle` as a generic fallback
- Heading: brief, human-readable ("Something went wrong", "Couldn't load projects")
- Body: one sentence explaining what to do ("Check your connection and try again")
- Include a "Retry" button (`secondary` variant) when the action is retryable

### Loading State

When content is being fetched:

- **For initial page loads**: Show a single centered spinner (`Loader2` icon with `animate-spin`, `24px`, `neutral-400`). No skeleton screens unless explicitly requested — they add complexity without clarifying the design
- **For inline updates** (e.g., submitting a form, loading more items): Swap the trigger button's label to a spinner + "Loading…" and disable the button
- **For pull-to-refresh or lazy loading**: A small spinner at the top or bottom of the list, `neutral-400`

The anti-pattern rule "No animated skeletons or shimmer effects in static mockups" still stands — but a simple `animate-spin` on a loader icon is fine for interactive interfaces.

---

## Form Validation & Error Feedback

Inputs need to clearly communicate when something is wrong. This applies to both web and mobile. For code examples, see the Form Validation States section in `references/components.md`.

### Behavioral Rules

- Validate on blur (when the user leaves the field), not on every keystroke — keystroke validation feels aggressive
- Show errors inline, directly below the relevant field. Never collect errors at the top of the form — users shouldn't have to hunt
- When the user corrects the input and the field is valid, remove the error state immediately (on change, not on blur)
- If the form is submitted with errors, scroll to the first invalid field and focus it

### Success Confirmation (Post-Submit)

After a successful form submission, provide clear feedback. Don't just silently navigate away:

- **Option A**: Toast notification confirming the action + navigate to the next logical screen
- **Option B**: Inline success message replacing the form content (useful for single-purpose screens like "Reset password")

---

## Toast Notifications

Transient feedback messages that confirm actions, surface errors, or provide information. Use shadcn's `Sonner` toast component. For code examples and the full variant table, see the Toast Notification section in `references/components.md`.

### Positioning & Behavior

- **Web**: Bottom-right corner, `16px` from the edge
- **Mobile**: Top-center, below the status bar / top bar area
- **Duration**: `4000ms` default, `6000ms` for messages with an action link. Error toasts should persist until dismissed
- **Stacking**: Max 3 visible at once. New toasts push older ones up (web) or down (mobile)
- **Animation**: Slide in from the edge + fade. Slide out + fade on dismiss. Should feel like the Transitions & Animations section — smooth, never instant

---

## Data Visualization Palette

When rendering charts (Recharts, Chart.js, etc.), use this ordered color sequence so data visualizations feel native to the brand. The palette starts with the brand purple and fans out through distinguishable hues:

| Order | Name  | Hex       | Use                                         |
| ----- | ----- | --------- | ------------------------------------------- |
| 1     | Brand | `#5900FF` | Primary data series, single-metric charts   |
| 2     | Teal  | `#14B8A6` | Secondary series                            |
| 3     | Amber | `#F59E0B` | Tertiary series                             |
| 4     | Rose  | `#F43F5E` | Fourth series, or "negative" in comparisons |
| 5     | Sky   | `#0EA5E9` | Fifth series                                |
| 6     | Lime  | `#84CC16` | Sixth series                                |

### Rules

- For single-metric charts (one bar, one line, one donut), always use `Brand` (`#5900FF`)
- For two-series comparisons, use `Brand` + `Teal`
- Apply colors in order — don't skip or shuffle. Consistency across charts makes dashboards feel cohesive
- Use `10%` opacity fills for area charts (e.g., `#5900FF1A` for brand area fill)
- Gridlines: `neutral-200`. Axis labels: `neutral-500`, caption size (12px). Axis lines: `neutral-300`
- Tooltips: White bg, `shadow-md`, `rounded-md`, `neutral-200` border — same treatment as popovers
- Never use brand purple for "negative" or "declining" values — use Rose for that. Purple is always neutral-to-positive

---

## Dark Mode

Dark mode is **off by default**. Only implement it when explicitly requested by the user or client. When dark mode is requested, follow these rules — do NOT improvise an inverted palette.

### How It Works

The theme file (`references/theme.css`) includes a `.dark` class block that overrides CSS custom properties. Adding `class="dark"` to `<html>` or a wrapper element flips the entire color system without changing any component code. The neutral scale inverts so existing utilities (`text-neutral-900`, `bg-neutral-50`, `border-neutral-200`) automatically produce the correct dark-mode values.

### Token Behavior in Dark Mode

You don't change token names in your code — the `.dark` override changes the values behind them. Here's what each token resolves to:

| Token (unchanged in code) | Light Mode Value         | Dark Mode Value              | Notes                            |
| ------------------------- | ------------------------ | ---------------------------- | -------------------------------- |
| `bg-neutral-50`           | `#FAFAFA` (light gray)   | `#171717` (near-black)       | Page background                  |
| `bg-neutral-0`            | `#FFFFFF` (white)        | `#0A0A0A` (near-black)       | Card surfaces                    |
| `border-neutral-200`      | `#E5E5E5` (light gray)   | `#404040` (dark gray)        | Borders / dividers               |
| `text-neutral-950`        | `#0A0A0A` (near-black)   | `#FFFFFF` (white)            | Page titles                      |
| `text-neutral-900`        | `#171717` (near-black)   | `#FAFAFA` (near-white)       | Body text                        |
| `text-neutral-500`        | `#737373` (mid-gray)     | `#737373` (mid-gray)         | Stays the same — mid-range       |
| `text-neutral-400`        | `#A3A3A3` (light gray)   | `#A3A3A3` (stays same)       | Subtext — readable on dark       |
| `bg-brand-500`            | `#5900FF`                | `#7A33FF` (lighter)          | Brighter for contrast on dark bg |
| `bg-brand-50`             | `#EEE5FF` (light purple) | `#120033` (very dark purple) | Tinted backgrounds invert        |

### `bg-white` vs `bg-neutral-0` — Critical Distinction

Tailwind's built-in `white` and `black` are **NOT overridden** in dark mode. They always resolve to literal `#FFFFFF` and `#000000`.

- Use **`text-white`** when you mean actual white — e.g., button text on a `brand-500` background. This stays white in both modes. ✅
- Use **`bg-neutral-0`** (not `bg-white`) for surfaces that should invert in dark mode — e.g., card backgrounds, sidebars, top bars. `bg-neutral-0` maps to `#FFFFFF` in light and `#0A0A0A` in dark. ✅
- Use **`bg-neutral-50`** for page backgrounds. Maps to `#FAFAFA` in light, `#171717` in dark. ✅

If you use `bg-white` on a card, it will stay bright white in dark mode — blinding. Use `bg-neutral-0` instead.

### Shadows in Dark Mode

Shadows are nearly invisible on dark surfaces. The `.dark` block increases shadow opacity so elevation is still perceptible, but cards should primarily rely on their `neutral-200` border (which maps to a subtle dark gray divider in dark mode) for definition.

### Logo

Use `assets/logo-mono-white.svg` — the only variant approved for dark surfaces.

### What NOT to Do in Dark Mode

- Do NOT manually set dark colors in component code — rely on the `.dark` class override
- Do NOT use `bg-white` for surfaces — use `bg-neutral-0` so they invert properly
- Do NOT use `brand-500` for large tinted surfaces — use `brand-50` (which maps to a dark purple in dark mode)
- Do NOT change spacing, radius, or typography — the spatial system is mode-independent

---

## Anti-Patterns (Do NOT)

- **No gradients on buttons.** Flat solid colors only.
- **No colored page backgrounds.** Background is always `neutral-50` or `neutral-0`.
- **No heavy borders.** Max `1px` for structural borders. Never 2px+.
- **No rounded-full on cards.** Cards are `rounded-lg` (10px), never circles.
- **No custom fonts.** DM Sans / sans-serif only. Monospace for code.
- **Prefer icon + label navigation** on desktop. Icon-only sidebars are acceptable if a tooltip with the label appears on hover or focus.
- **No dark mode** unless explicitly requested. Default is always light.
- **No animated skeletons or shimmer effects** in static mockups.
- **No drop shadows on text.** Ever.
- **No border-radius mixing.** Don't use the same radius token at different hierarchy levels — e.g., `rounded-lg` cards should contain `rounded-sm` children, not `rounded-lg` children. The inner radius should always be smaller than the outer.
- **No floating labels or placeholder-as-label.** Labels must always be visible above inputs. Placeholders are hints, not labels — they vanish on focus and users lose context.
- **No emojis in the UI.** Icons only. The only exception is user-generated content — if a user typed an emoji, display it. But never add emojis to labels, headings, buttons, nav items, placeholders, or any system-generated text.

---

## Checklist Before Output

Before delivering any UI code, verify:

- [ ] Uses `DM Sans` font family (with `sans-serif` fallback)
- [ ] Brand purple only on interactive/active elements
- [ ] Cards have `bg-neutral-0` + `neutral-200` border + `rounded-lg` + `shadow-sm`
- [ ] No unauthorized colors, fonts, or shadows
- [ ] All icons from Lucide React
- [ ] shadcn components used where available (not custom recreations)
- [ ] Spacing feels generous — nothing cramped
- [ ] Page background is `neutral-50`, not white
- [ ] Empty states are handled (not just the happy path with fake data)
- [ ] Form inputs show error styling on validation failure (red border + message below)
- [ ] Actions provide feedback via toast or inline confirmation
- [ ] Charts (if present) use the data visualization palette in order
- [ ] All form inputs have visible external labels (not inside the input)
- [ ] Placeholder text is de-emphasized (`neutral-400`, normal weight)
- [ ] Casper Studios logo uses the correct variant for the background (default on light, mono-white on dark)
- [ ] If dark mode was requested: `.dark` class applied, logo uses mono-white variant, surfaces use `bg-neutral-0` (not `bg-white`)
- [ ] Border-radius: buttons/inputs use `rounded-md` (8px), cards use `rounded-lg` (10px), nav items/inner elements use `rounded-sm` (6px)
- [ ] Button/input heights: `48px` (`h-12`) by default, `36px` (`h-9`) when inside cards, panels, tables, or other compact containers

### Additional checks for Web Applications:

- [ ] Sidebar follows the 240px / grouped nav / active state pattern
- [ ] Responsive: works at 1280px, 768px, and 375px

### Additional checks for Mobile Applications:

- [ ] Rendered inside iPhone 16 device frame (393×852, 40px outer radius, 8px bezel)
- [ ] Primary action button is pinned to bottom with safe area padding
- [ ] Navigation uses bottom tab bar, not sidebar
- [ ] Buttons and inputs are `48px` height (same as global default — no mobile override needed)
- [ ] Most tap targets are 44×44px or larger (smaller is OK in dense UI, but not the default)
- [ ] Single-column layout only — no multi-column grids
- [ ] Typography uses mobile scale (H1: 24px, H2: 18px)
