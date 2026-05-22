---
name: ui-generator
description: |
  Generate UI components from natural language descriptions.
  Use when: user asks for a page, component, or UI element.
  Triggers: "create page", "add component", "show form", "make button",
  "страница", "компонент", "форма".
---

# UI Generator

Create beautiful UI from descriptions. Integrates with theme-factory.

## Process

1. **Understand request**
   - "Login page" → form with email/password
   - "Dashboard" → stats cards, charts, tables
   - "Settings" → form sections, toggles

2. **Apply theme**
   - Load current theme from theme-factory
   - Use theme colors and fonts
   - Follow frontend-design principles

3. **Generate code**
   - React/Next.js components
   - Tailwind CSS styling
   - Responsive by default

4. **Preview**
   - Hot reload in browser
   - User sees result immediately

## Component Patterns

| Request | Components |
|---------|------------|
| "login page" | Form, inputs, button, link |
| "dashboard" | Stats cards, chart, table |
| "settings" | Sections, toggles, form |
| "landing page" | Hero, features, CTA, footer |
| "pricing" | Tier cards, comparison table |
| "profile" | Avatar, info, edit form |

## Design Rules

From frontend-design skill:
- No Inter, Roboto, Arial
- No purple gradients on white
- Distinctive, memorable aesthetics
- Motion and micro-interactions

## Usage

User says: "Add a pricing page with 3 tiers"

1. Generate PricingPage component
2. Create PricingTier subcomponent
3. Apply current theme
4. Add to routes
5. Show preview: "Here's your pricing page"
