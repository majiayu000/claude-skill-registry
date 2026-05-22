---
name: uiux
description: UI/UX - design system, accessibility. Use when building interfaces.
---

# UI/UX Guideline

## Tech Stack

* **Framework**: Next.js (with Turbopack)
* **Components**: Radix UI (mandatory)
* **Styling**: Tailwind CSS
* **Icons**: @iconify-icon/react

## Radix UI (Mandatory)

If Radix has a primitive for it, you MUST use it. No exceptions. No custom implementations.
Any custom implementation of something Radix already provides is a bug.

## Non-Negotiables

* WCAG 2.1 AA compliance (keyboard navigation, screen readers, contrast)
* Touch targets minimum 44x44px on mobile
* Responsive design (mobile-first)
* Loading states for all async operations
* Error states must be actionable
* No layout shift on content load

## Context

UI/UX is about removing friction between users and value. Bad UX doesn't just feel bad — it costs conversion, retention, and trust.

## Driving Questions

* Where do users get confused or frustrated?
* What would a first-time user struggle with?
* Where are loading states missing or unhelpful?
* What accessibility issues exist?
* Where does the UI feel inconsistent?
* What would make the product feel more polished?
