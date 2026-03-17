---
description: Helper for building landing pages and marketing sites using Tailark components.
deps: ["ui-handler"]
---

# Page Builder Skill

This skill helps you construct high-quality marketing pages by selecting and composing pre-built "Tailark" components.

## Workflow

1.  **Analyze Requirement**: Determine the type of page (Landing, Pricing, About, Contact) and the sections needed (Hero, Features, Social Proof, etc.).
2.  **Select Components**: Consult `reference.md` to pick the most suitable components for each section.
3.  **Implementation**:
    -   Import the chosen components into your `page.tsx`.
    -   **Copy & Customize**: Do not just import; feel free to copy the component code into a new local component (e.g., `src/components/landing/my-hero.tsx`) if you need to change text, images, or layout significantly.
    -   **Composition**: Stack them in a semantic `<main>` tag.

## Component Selection Strategy

-   **Landing Page**: `HeroSection` -> `LogoCloud` -> `Features-12` -> `WallOfLoveSection` -> `CallToAction`.
-   **Pricing Page**: `Pricing` or `PricingComparator` -> `FAQs`.
-   **About Page**: `Content-2` -> `StatsSection` -> `TeamSection`.
-   **Contact Page**: `ContactSection`.

## Customization

All components are built with Tailwind CSS and Shadcn UI.
-   **Icons**: Uses `lucide-react`.
-   **Images**: Uses `next/image`. Replace placeholders with real assets.
-   **Colors**: Respects the global theme.

## Reference
See `reference.md` for a complete list of available components with visual descriptions and recommendations.

