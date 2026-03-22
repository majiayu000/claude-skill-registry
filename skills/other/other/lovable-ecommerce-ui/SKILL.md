---
name: lovable-ecommerce-ui
description: "Generate high-converting, visually rich e-commerce UIs in Lovable with product layouts, cart interactions, checkout flows, and trust-building patterns."
homepage: https://lovable.dev
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🛒"}}
---

# Lovable E-Commerce UI

## Purpose

Generate e-commerce UIs in Lovable covering product listing pages, product detail pages, shopping carts, checkout flows, category browsers, and storefront landing pages. Enforces conversion-optimized layouts, trust-building patterns, and commerce-specific micro-interactions.

> **Platform context**: Lovable generates React + TypeScript + Tailwind CSS + shadcn/ui apps on Vite. Payments integrate via Stripe. Backend via Supabase (PostgreSQL + Auth + Storage for product images). Use shadcn components for forms, dialogs, sheets, and UI primitives.

## Inputs

| Parameter        | Required | Values                                                                          | Default      |
|------------------|----------|---------------------------------------------------------------------------------|--------------|
| `store_type`     | yes      | fashion, electronics, artisan_goods, food_beverage, digital_products, subscription_box, general_retail | — |
| `brand_tone`     | yes      | luxury, playful, minimalist, bold, eco-conscious                                | —            |
| `primary_action` | no       | add_to_cart, subscribe, book_demo, buy_now                                       | add_to_cart  |
| `page_type`      | no       | listing, detail, cart, checkout, storefront                                      | storefront   |

## Workflow

### 1. Identify Store Category

Each store type triggers different layout defaults:

| Store Type       | Key Elements                                                    |
|------------------|-----------------------------------------------------------------|
| fashion          | Large imagery, lookbook grids, size/color selectors             |
| electronics      | Spec comparison tables, feature highlights, rating breakdowns   |
| artisan_goods    | Story-driven layout, maker profiles, handcraft textures         |
| food_beverage    | Ingredient showcases, dietary badges, subscription options      |
| digital_products | Feature demos, screenshot galleries, pricing tiers              |
| subscription_box | Unboxing previews, plan comparison, testimonial carousels       |
| general_retail   | Standard grid, category filters, versatile product cards        |

### 2. Apply Brand Tone to Aesthetics

| Tone           | Theme                                                                                     |
|----------------|-------------------------------------------------------------------------------------------|
| luxury         | Dark navy/black + gold/cream accents. Serif headings (Playfair Display). 80px+ section padding. Thin borders (0.5px). Subtle animations. |
| playful        | Bright pastels + saturated accent pops. Rounded corners (16px+). Bouncy easing. Illustrated icons. Rounded font (Nunito, Quicksand). |
| minimalist     | Neutral (white, warm gray, single accent). Strong typography hierarchy. Grid layouts. Minimal decoration. (Inter, Helvetica Neue). |
| bold           | High contrast B/W + one vibrant accent. Oversized type. Neobrutalist cards (2px borders, 4px offset shadows). Sharp corners. |
| eco-conscious  | Earth tones (sage, terracotta, cream). Organic shapes. Textured/paper backgrounds. Serif + sans-serif pairing. |

### 3. Structure Pages by Type

**Listing Page**:
- Masonry or bento grid with hover-reveal quick-add buttons.
- Animated filter sidebar (slide-in, 300ms).
- Sticky sort/filter bar at top.
- Infinite scroll or paginated with smooth transitions.

**Detail Page**:
- 60% image gallery (left) / 40% product info (right) on desktop.
- Swipeable gallery with dot indicators.
- Sticky add-to-cart section on scroll.
- Accordion for description, shipping, reviews (use shadcn Accordion).
- Related products carousel at bottom.

**Cart** (shadcn Sheet as slide-in drawer):
- Slide-in from right (300ms ease-out).
- Item cards with quantity adjusters (+/- with count animation).
- Swipe-to-remove on mobile.
- Order summary with expandable line items.
- Persistent checkout CTA at bottom.

**Checkout** (multi-step form):
- Steps: Shipping → Payment → Review.
- Horizontal progress indicator.
- Inline field validation (gentle shake on error).
- Sticky order summary sidebar on desktop.
- Trust badges grouped near payment CTA.
- Stripe Elements integration for payment.

**Storefront**:
- Hero with featured product/collection.
- Bento grid of category cards.
- Trending products horizontal scroll.
- Social proof section with review highlights.
- Newsletter signup with minimal friction.

### 4. Define Commerce Interactions

- **Add-to-cart**: Button text morphs to checkmark (200ms). Cart badge count increments with scale pulse (300ms).
- **Product images**: Scale 1.05 on hover (200ms). Gallery: swipe + click with crossfade (300ms).
- **Quantity selector**: Smooth increment/decrement with number fade. Minus disabled at qty 1.
- **Wishlist toggle**: Heart icon scales 1.3 → 1.0 (bouncy, 400ms). Outline fill transition.
- **Price display**: Sale price in accent color. Original gets animated strikethrough (200ms left-to-right).
- **Filter interactions**: Checkbox toggles trigger smooth grid re-layout (300ms). Active filters as removable chips.

### 5. Apply Trust & Conversion Patterns

- **Social proof**: Star ratings with review count. Staggered fade-in (80ms per element).
- **Stock indicators**: "Only X left" with subtle opacity pulse. Never fake urgency or countdown timers.
- **Shipping info**: Expandable inline text. Not popup modals.
- **Security badges**: Horizontal row near checkout CTA with soft highlight background.
- **Return policy**: Accordion section, not hidden in footer.
- **Payment icons**: Visa, Mastercard, Amex, PayPal icons near payment form.

### 6. Apply Typography & Color

- Product names: weight 500, 1rem (grid) / 1.5rem+ (detail).
- Prices: weight 700, sale in accent, original in muted + strikethrough.
- CTAs: High contrast, min 48px height. Primary uses brand color, secondary uses outlined.
- Body: weight 400, 1rem, line-height 1.6.

## Output Format

Complete e-commerce page or component set with HTML structure, Tailwind CSS, interactive states, and animations. Uses shadcn Sheet for cart drawer, shadcn Accordion for product details, shadcn Form for checkout. Responsive and mobile-first. Ready for Supabase data connection and Stripe payment integration.

## Guardrails

- Never use aggressive urgency — no countdown timers, no fake scarcity, no "Buy NOW."
- All interactive elements ≥ 48px × 48px touch targets on mobile.
- Prices must be clear — sale and original visually distinct.
- All product images must have alt text placeholders: `alt="[Product] - [view]"`.
- Cart interactions must give clear feedback for every state change.
- Never auto-add items to cart or auto-open cart without user action.
- Color contrast meets WCAG AA (4.5:1 body, 3:1 large text).
- Use shadcn components for forms, dialogs, sheets. Don't build custom modals.
- Payments via Stripe integration. Don't build custom payment forms.

## Failure Handling

| Problem | Follow-up Prompt |
|---------|-----------------|
| Generic grid without commerce | "Enhance product cards: hover-reveal quick-add button (slides up, 200ms), wishlist heart toggle (bouncy), image zoom on hover (scale 1.05). Add sticky filter/sort bar." |
| Cart lacks interactivity | "Add quantity +/- with number transition, swipe-to-remove on cards, order summary that updates totals with count-up animation." |
| Missing trust indicators | "Add security badges (SSL, payment icons, return guarantee) in a highlighted row above the Place Order button." |
| Checkout not multi-step | "Split checkout into 3 steps: Shipping → Payment → Review. Add horizontal progress bar. Validate inline with gentle shake on error." |
| Product gallery not interactive | "Make gallery swipeable with dot indicators. Add thumbnail strip below. Main image uses crossfade transition (300ms). Support pinch-to-zoom on mobile." |

## Examples

### Example 1: Luxury Fashion Storefront

**Input**: `store_type=fashion`, `brand_tone=luxury`, `page_type=storefront`

**Prompt to Lovable**:
```
Build a luxury fashion storefront:

STYLE: Dark navy (#0a0e1a) background with cream (#f5f0e8) text and gold (#c9a96e) accents. Playfair Display for headings, Inter for body. Thin borders (0.5px), generous spacing (80px sections). Subtle smooth animations.

HERO: Full-width with featured collection image. Large serif headline "New Season" with cream text. Minimal CTA button with gold border.

CATEGORIES: Bento grid with 4 category cards (Women, Men, Accessories, New In). Large images with text overlay on hover. Smooth scale 1.03 on hover.

TRENDING: Horizontal scroll of product cards. Each card: product image with hover zoom (1.05), product name (500 weight), price in cream. Wishlist heart icon overlay.

SOCIAL PROOF: "As seen in" logos bar + featured review with 5 stars.

NEWSLETTER: Minimal input + "Subscribe" button at bottom. Gold accent on focus.

Mobile: Stack all sections vertically. Hero becomes 60vh. Categories become 2-column grid.
```

### Example 2: Electronics Product Detail

**Input**: `store_type=electronics`, `brand_tone=minimalist`, `page_type=detail`

**Prompt to Lovable**:
```
Build an electronics product detail page:

LAYOUT: 60/40 split. Left: image gallery with thumbnail strip below, main image crossfade on click. Right: product info.

PRODUCT INFO: Name (1.75rem/600), star rating with review count, price ($999, bold), color selector (circle swatches), storage selector (pill buttons).

ADD TO CART: Full-width primary button (blue, 48px height). Below it: "Free shipping" and "30-day returns" with check icons.

SPECS: shadcn Accordion sections — Overview, Technical Specs (table format), What's in the Box, Reviews (star breakdown bar chart + review cards).

RELATED: "You might also like" carousel at bottom with 4 product cards.

INTERACTIONS: Gallery thumbnails highlight on click. Color/storage selectors show selected state. Add-to-cart morphs to checkmark on click. Quantity adjuster with +/- buttons.

All text high contrast (min 4.5:1). Touch targets min 48px.
```

## Security & Privacy

This skill generates text prompts only. It does not access external endpoints, process payments, or execute code. All output is prompt text intended for the Lovable.dev platform. Actual payment processing requires separate Stripe integration.

## Trust Statement

This skill contains no executable scripts. It produces Lovable-compatible e-commerce generation prompts. It does not access the filesystem, network, or any external service. Payment references are prompt-level instructions for Stripe integration, not direct payment processing.
