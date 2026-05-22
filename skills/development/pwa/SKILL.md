---
name: pwa
description: PWA - native app parity, offline-first, engagement. Use when building installable web apps.
---

# PWA Guideline

## Tech Stack

* **Framework**: Next.js (with Turbopack)
* **Service Worker**: Serwist (Next.js integration)
* **Platform**: Vercel

## Non-Negotiables

* Service worker must not cache personalized/sensitive/authorized content
* Cache invalidation on deploy must be correct (no stale content)
* Offline experience must be functional, not just a fallback page
* Installation prompt must be contextual (after value demonstrated)
* Complete manifest.webmanifest with all required fields
* All required icons present (favicon, apple-touch-icon, PWA icons, maskable)

## Context

PWA goal: users forget they're in a browser. The gap between "website" and "app" is measured in micro-interactions — haptics, gestures, offline resilience, and engagement hooks.

A bad PWA is worse than no PWA. But a great PWA can match 90% of native with 10% of the effort.

## Driving Questions

* What breaks when the user goes offline mid-action?
* What would make users install this instead of bookmarking?
* Which native gestures (swipe, pull, long-press) are missing?
* What local notifications would drive daily engagement?
* Where does the app feel "webby" instead of native?
* What's the first thing users see when they open the installed app?
